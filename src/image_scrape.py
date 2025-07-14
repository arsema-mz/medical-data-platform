import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("api_id"))
API_HASH = os.getenv("api_hash")
SESSION_NAME = os.getenv("SESSION_NAME")

MEDIA_CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/CheMed123"
]

# Central media folder
MEDIA_DIR = "data/raw/telegram_messages/media"
os.makedirs(MEDIA_DIR, exist_ok=True)

async def download_images(client, channel_url):
    channel_name = channel_url.split("/")[-1]

    try:
        entity = await client.get_entity(channel_url)
        offset_id = 0
        limit = 100
        count = 0

        while True:
            history = await client(GetHistoryRequest(
                peer=entity,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))

            if not history.messages:
                break

            for msg in history.messages:
                if msg.media:
                    try:
                        # Save media with channel and message ID to avoid filename conflict
                        filename_prefix = f"{channel_name}_{msg.id}"
                        file_path = os.path.join(MEDIA_DIR, filename_prefix)
                        saved_path = await client.download_media(msg, file=file_path)
                        if saved_path:
                            count += 1
                    except Exception as media_error:
                        print(f"⚠️ Failed to download media for message {msg.id}: {media_error}")

            offset_id = history.messages[-1].id
            await asyncio.sleep(1)

        print(f"Downloaded {count} media files from {channel_name}.")

    except Exception as e:
        print(f"Error downloading media from {channel_url}: {e}")

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        for channel in MEDIA_CHANNELS:
            await download_images(client, channel)

if __name__ == "__main__":
    asyncio.run(main())
