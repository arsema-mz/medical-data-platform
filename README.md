# Medical Data Platform – Telegram Pipeline

This project extracts raw medical-related messages from public Ethiopian Telegram channels and transforms them into a structured, queryable format using PostgreSQL and dbt.


## Task 1: Data Ingestion (Raw)

- **Raw JSON files** collected via a Python scraper are stored in:
```

data/raw/telegram\_messages/YYYY-MM-DD/channel\_name.json

```

- A Python ETL script loads the messages into a PostgreSQL table:

**Script:** `src/load_raw.py`  
**Target Table:** `raw.telegram_messages`  
- Structure:
  - `channel`: channel name
  - `message`: raw message as JSONB
  - `load_timestamp`: insert time

---

## Task 2: Data Modeling and Transformation (dbt)

### 🛠 DBT Setup

- Initialized a dbt project: `telegram_project`
- Connected it to local PostgreSQL using the `analytics` schema
- Configured staging models to materialize as **views**

### Staging Models

**Model:** `stg_telegram_messages.sql`  
- Cleans and extracts key fields from `raw.telegram_messages`:
- `message_id`
- `message_text`
- `message_date`
- `channel`
- `has_image`
- `message_length`

**Schema:** `staging`  
**Materialization:** View


## Next Steps

- Build **fact and dimension tables** for a star schema:
  - `dim_channels`, `dim_dates`, `fct_messages`
- Add **data quality tests** with dbt (unique, not_null, custom tests)
- Generate dbt documentation

## Requirements

- Python 3.10+
- PostgreSQL (local)
- dbt-postgres
- psycopg2
