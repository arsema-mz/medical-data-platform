import os
import json
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

CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma",
    "https://t.me/CheMed123"
    ]

RAW_DATA_DIR = "data/raw/telegram_messages"

async def scrape_channel(client, channel_url):
    today = datetime.now().strftime("%Y-%m-%d")
    channel_name = channel_url.split("/")[-1]
    output_dir = os.path.join(RAW_DATA_DIR, today)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{channel_name}.json")

    try:
        entity = await client.get_entity(channel_url)

        all_messages = []
        offset_id = 0
        limit = 100  # Telegram caps at 100 per call

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
                all_messages.append({
                    "id": msg.id,
                    "date": str(msg.date),
                    "text": msg.message,
                    "media": bool(msg.media),
                    "sender_id": getattr(msg.from_id, 'user_id', None),
                })

            offset_id = history.messages[-1].id

            # Optional: Sleep to avoid rate limits
            await asyncio.sleep(1)

        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_messages, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(all_messages)} messages from {channel_name}.")

    except Exception as e:
        print(f"Error scraping {channel_url}: {e}")

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        for channel in CHANNELS:
            await scrape_channel(client, channel)

if __name__ == "__main__":
    asyncio.run(main())
