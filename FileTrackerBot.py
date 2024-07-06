import os
import json
import zipfile
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events, sync

# Load settings from settings.json
with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

api_id = settings["api_id"]
api_hash = settings["api_hash"]
bot_token = settings["bot_token"]
admin_user_id = settings["admin_user_id"]
folder_paths = settings["folder_paths"]
check_interval = 300  # 5 minutes in seconds

# Create an instance of TelegramClient
client = TelegramClient("H0lyFanz", api_id, api_hash).start(bot_token=bot_token)

# Variables to keep track of the last check time and new files found
last_check_time = datetime.now()
new_files_found = False


# Function to display a welcome message and instructions
@client.on(events.NewMessage(pattern="/start"))
async def show_welcome(event):
    sender_id = event.sender_id
    sender_username = event.sender.username
    if sender_id == admin_user_id:
        chat_id = event.chat_id
        welcome_message = "Welcome to the File Tracker Bot!\n\n"
        welcome_message += "Use the following commands:\n\n"
        welcome_message += "/files - Display files in the specified folders\n"
        welcome_message += "/check - Check for new files in the specified folders\n"
        welcome_message += "/download [file_path] - Download a file\n"
        welcome_message += "/delete [file_path] - Delete a file\n"
        welcome_message += "/all - Download all available media files\n"
        welcome_message += (
            "/zip - Create zip files containing files from specified folders\n"
        )
        await client.send_message(chat_id, welcome_message)
    else:
        access_denied_message = "Access Denied!\n\n"
        access_denied_message += "You are not authorized to use this bot. This bot is designed to be used only by the authorized user."
        await client.send_message(sender_id, access_denied_message)
        admin_notification = f"🚨 Unauthorized Access Attempt 🚨\n\n"
        admin_notification += (
            f" User {sender_username}, with this ({sender_id}) user id\n"
        )
        admin_notification += f"Attempted to access the File Tracker Bot.\n\n"
        admin_notification += "Please take appropriate action if necessary."
        await client.send_message(admin_user_id, admin_notification)


# Function to display files in the specified folders
@client.on(events.NewMessage(pattern="/files"))
async def show_files(event):
    sender_id = event.sender_id
    if sender_id == admin_user_id:
        chat_id = event.chat_id
        message = "Files in the folders:\n\n"
        for folder_path in folder_paths:
            message += f"Folder `{folder_path}/`:\n"
            for file_name in os.listdir(folder_path):
                message += f"- `{file_name}`\n"
            message += "\n"
        await client.send_message(chat_id, message, parse_mode="markdown")


# Function to manually check for new files
@client.on(events.NewMessage(pattern="/check"))
async def manual_check(event):
    global last_check_time, new_files_found
    sender_id = event.sender_id
    if sender_id == admin_user_id:
        current_files = {}
        for folder_path in folder_paths:
            current_files[folder_path] = set(os.listdir(folder_path))
        new_files_found = await check_new_files(current_files)
        if not new_files_found:
            time_since_last_check = datetime.now() - last_check_time
            if time_since_last_check < timedelta(seconds=check_interval):
                await client.send_message(
                    admin_user_id, "No new files found since the last check."
                )
            else:
                await client.send_message(admin_user_id, "No new files found.")


# Function to download a file
@client.on(events.NewMessage(pattern="/download"))
async def download_file(event):
    sender_id = event.sender_id
    if sender_id == admin_user_id:
        chat_id = event.chat_id
        file_path = event.message.text.split()[1]  # Get the file path from the command
        try:
            await client.send_file(chat_id, file_path, caption="File is ready!")
        except Exception as e:
            await client.send_message(chat_id, f"Error downloading file: {str(e)}")


# Function to delete a file
@client.on(events.NewMessage(pattern="/delete"))
async def delete_file(event):
    sender_id = event.sender_id
    if sender_id == admin_user_id:
        chat_id = event.chat_id
        file_path = event.message.text.split()[1]  # Get the file path from the command
        try:
            os.remove(file_path)
            await client.send_message(
                chat_id,
                f"File `{file_path}` deleted successfully.",
                parse_mode="markdown",
            )
        except Exception as e:
            await client.send_message(chat_id, f"Error deleting file: {str(e)}")


# Function to download all available media files (images and videos)
@client.on(events.NewMessage(pattern="/all"))
async def download_all_files(event):
    sender_id = event.sender_id
    if sender_id == admin_user_id:
        chat_id = event.chat_id
        await client.send_message(
            chat_id,
            "Your command has been received. Please wait while the files are being downloaded.",
        )

        for folder_path in folder_paths:
            for folder_name, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(folder_name, file)
                    if file_path.endswith(
                        (
                            ".jpg",
                            ".jpeg",
                            ".png",
                            ".gif",
                            ".bmp",
                            ".svg",
                            ".mp4",
                            ".avi",
                            ".mkv",
                        )
                    ):
                        try:
                            await client.send_file(
                                chat_id,
                                file_path,
                                caption=f"File: `{file_path}`",
                                parse_mode="markdown",
                            )
                        except Exception as e:
                            await client.send_message(
                                chat_id, f"Error sending file: {str(e)}"
                            )

        await client.send_message(
            chat_id, "All available media files have been downloaded."
        )


# Function to create zip files based on user request
@client.on(events.NewMessage(pattern="/zip"))
async def create_zip(event):
    sender_id = event.sender_id
    if sender_id == admin_user_id:
        chat_id = event.chat_id
        await client.send_message(
            chat_id,
            "Your command has been received. Please wait while the files are being processed.",
        )
        zip_file_path_media = "media_files.zip"
        # Create a zip file containing all media files (images and videos)
        with zipfile.ZipFile(zip_file_path_media, "w") as zip_media:
            for folder_path in folder_paths:
                for folder_name, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(folder_name, file)
                        if file_path.endswith(
                            (
                                ".jpg",
                                ".jpeg",
                                ".png",
                                ".gif",
                                ".bmp",
                                ".svg",
                                ".mp4",
                                ".avi",
                                ".mkv",
                            )
                        ):
                            zip_media.write(
                                file_path, os.path.relpath(file_path, folder_path)
                            )
        await client.send_file(chat_id, zip_file_path_media, caption="Your Media Files")
        os.remove(zip_file_path_media)


# Function to monitor folders for new files
async def monitor_folders():
    global last_check_time, new_files_found
    current_files = {}
    for folder_path in folder_paths:
        current_files[folder_path] = set(os.listdir(folder_path))

    while True:
        new_files_found = await check_new_files(current_files)
        last_check_time = datetime.now()
        await asyncio.sleep(check_interval)


# Function to check for new files
async def check_new_files(current_files):
    global new_files_found
    new_files_found = False
    for folder_path in folder_paths:
        new_files = set(os.listdir(folder_path)) - current_files[folder_path]
        if new_files:
            new_files_found = True
            for file_name in new_files:
                file_path = os.path.join(folder_path, file_name)
                try:
                    await client.send_file(
                        admin_user_id,
                        file_path,
                        caption=f"New file created: `{file_path}`",
                        parse_mode="markdown",
                    )
                except Exception as e:
                    await client.send_message(
                        admin_user_id, f"Error sending file: {str(e)}"
                    )
            current_files[folder_path] = set(os.listdir(folder_path))
    return new_files_found


# Start the bot and the folder monitoring task
client.start()
print("Bot is ready to receive commands.")
client.loop.create_task(monitor_folders())
client.run_until_disconnected()
