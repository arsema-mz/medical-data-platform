from dagster import schedule
from medical_data_pipeline.definitions import daily_pipeline_job

@schedule(cron_schedule="0 0 * * *", job=daily_pipeline_job, execution_timezone="Africa/Addis_Ababa")
def daily_pipeline_schedule(context):
    return {}
