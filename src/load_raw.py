import os
import json
import psycopg2
from glob import glob
from dotenv import load_dotenv


load_dotenv()


conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id SERIAL PRIMARY KEY,
    channel TEXT,
    message JSONB,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

json_files = glob("data/raw/telegram_messages/**/*.json", recursive=True)

for filepath in json_files:
    channel_name = os.path.basename(filepath).replace(".json", "")
    with open(filepath, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cursor.execute(
                "INSERT INTO raw.telegram_messages (channel, message) VALUES (%s, %s)",
                (channel_name, json.dumps(msg))
            )

conn.commit()
cursor.close()
conn.close()
print("Done loading raw messages.")