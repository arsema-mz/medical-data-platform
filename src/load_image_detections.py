import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv


load_dotenv()


# Load the CSV
csv_path = 'data/processed/image_detections.csv'
df = pd.read_csv(csv_path)

# Extract message_id from image_path
df['message_id'] = df['image_path'].str.extract(r'_(\d+)').astype(float)

# Replace NaN with None
df = df.where(pd.notnull(df), None)

# Convert to list of tuples with native Python types
records = [
    (
        str(row.image_path),
        str(row.detected_object_class),
        float(row.confidence_score),
        int(row.message_id) if row.message_id is not None else None
    )
    for row in df.itertuples(index=False)
]

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),      
    dbname=os.getenv('DB_NAME'),   
    user=os.getenv('DB_USER'),      
    password=os.getenv('DB_PASSWORD'), 
    port=os.getenv('DB_PORT')        
)
cur = conn.cursor()

# Insert query
insert_query = """
INSERT INTO raw.image_detections (image_path, detected_object_class, confidence_score, message_id)
VALUES %s
"""

# Execute insertion
execute_values(cur, insert_query, records)

# Finalize
conn.commit()
cur.close()
conn.close()

print("✅ Data loaded successfully into raw.image_detections.")
