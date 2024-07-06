# File-Tracker-Bot-V1

FileTrackerBot is a Telegram bot that monitors specified folders for new files and provides various file management capabilities. It is a powerful Telegram bot designed for efficient remote file management. It monitors specified folders for new files, provides real-time notifications, and offers a range of file operations through simple commands.

## Key Features:
- Automatic file monitoring and notifications
- File listing and navigation
- Individual file download and deletion
- Bulk media file download
- Zip file creation for easy transfer
- Secure access limited to authorized admin

## Usage
Send the following commands to the bot:

`/start: Display welcome message and instructions`
`/files: Display files in the specified folders`
`/check: Manually check for new files`
`/download [file_path]: Download a specific file`
`/delete [file_path]: Delete a specific file`
`/all: Download all available media files`
`/zip: Create zip files containing files from specified folders`

## Setup

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `settings.json` file with your Telegram API credentials and bot token:
```json
{
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH",
    "bot_token": "YOUR_BOT_TOKEN",
    "admin_user_id": YOUR_USER_ID,
    "folder_paths": [
        "/path/to/folder1",
        "/path/to/folder2"
    ]
}
```

4. Run the bot:

```bash
python FileTrackerBot.py
```

## Security Note:
This bot is designed for personal use and should only be accessible by the authorized admin user. Ensure that your settings.json file is kept secure and not shared publicly.
