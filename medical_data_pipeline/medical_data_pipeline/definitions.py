from dagster import op, job
import subprocess

@op
def scrape_telegram_data_op():
    result = subprocess.run(["python", "src/scrape.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraping failed: {result.stderr}")
    return result.stdout

@op
def load_raw_to_postgres_op():
    result = subprocess.run(["python", "src/load_raw.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading raw data failed: {result.stderr}")
    return result.stdout

@op
def run_dbt_transformations_op():
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    return result.stdout

@op
def run_yolo_enrichment_op():
    result = subprocess.run(["python", "src/load_image_detections.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"YOLO enrichment failed: {result.stderr}")
    return result.stdout

@job
def daily_pipeline_job():
    scrape_telegram_data_op()
    load_raw_to_postgres_op()
    run_dbt_transformations_op()
    run_yolo_enrichment_op()
