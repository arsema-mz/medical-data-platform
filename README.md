# 🩺 Medical Data Platform – Telegram Pipeline

This project extracts and processes medical-related messages from public Ethiopian Telegram channels. It uses PostgreSQL, dbt, FastAPI, and Dagster to build a robust, automated data pipeline.


## Data Ingestion

- Scrape messages from Telegram via `src/scrape.py`
- Raw messages are saved to:
```
data/raw/telegram\_messages/YYYY-MM-DD/channel\_name.json

```
- Load into PostgreSQL table `raw.telegram_messages` using `src/load_raw.py`


## Data Modeling (dbt)

- DBT project: `telegram_project` (schema: `analytics`)
- **Staging Models:**
- `stg_telegram_messages.sql`
- `stg_image_detections.sql`
- **Fact Models:**
- `fct_image_detections.sql`
- `fct_all_messages.sql`
- `fct_top_products.sql`
- `fct_channel_activity.sql`
- Data quality tests and documentation included


## Data Enrichment

- YOLOv8 used to detect medical objects in images
- Detected classes + confidence stored in `image_detections.csv`
- Enriched data loaded into PostgreSQL using `src/load_image_detections.py`


## Analytical API (FastAPI)

- Created RESTful API in `api/` folder using FastAPI
- Connected to dbt models via SQLAlchemy
- Endpoints:
- `/api/reports/top-products?limit=10`
- `/api/channels/{channel_name}/activity`
- `/api/search/messages?query=keyword`


## Pipeline Orchestration (Dagster)

- Defined Dagster `job` to orchestrate:
- `scrape_telegram_data`
- `load_raw_to_postgres`
- `run_dbt_transformations`
- `run_yolo_enrichment`
- Dagster UI launched via `dagster dev`
- Added daily schedule for pipeline execution


## ⚙️ Tech Stack

- Python, FastAPI, SQLAlchemy, Telethon, YOLOv8
- PostgreSQL, dbt-core, dbt-postgres
- Dagster for orchestration
- Pandas, NumPy, Pydantic, Loguru


## ✅ Status

- FastAPI running at `http://localhost:8000`
- Dagster UI available at `http://localhost:3000`


## Deployment

This project is Dockerized for easy deployment and consistent environment setup.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop)

### How to run locally

1. Clone the repo:
   ```bash
   git clone https://github.com/arsema-mz/medical-data-platform.git
   cd medical-data-platform
````

2. Build and start the FastAPI container:

   ```bash
   docker-compose up --build
   ```
