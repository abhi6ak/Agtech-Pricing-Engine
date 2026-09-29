import os
import json
import logging
from datetime import datetime, timedelta
import requests
import pandas as pd
# from airflow import DAG
# # from airflow.operators.python import PythonOperator
from minio import Minio
import io

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "dummy_key")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "password123")
BUCKET_NAME = "mandi-data"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

LOCATIONS = [
    {"lat": 20.0110, "lon": 73.7903, "name": "Nashik"},
    {"lat": 31.6340, "lon": 74.8723, "name": "Amritsar"}
]

def fetch_weather_data(ds, **kwargs):
    all_weather_data = []
    
    for loc in LOCATIONS:
        # Dummy API URL for OpenWeatherMap
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={loc['lat']}&lon={loc['lon']}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        logging.info(f"Fetching weather for {loc['name']}")
        
        try:
            # Mocking response
            mock_data = {
                "location": loc['name'],
                "date": ds,
                "temp": 28.5,
                "humidity": 65,
                "rainfall_mm": 0.0,
                "weather_main": "Clear"
            }
            all_weather_data.append(mock_data)
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            raise

    df = pd.DataFrame(all_weather_data)

    # Convert to Parquet
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)

    # Upload to MinIO
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    
    # Ensure bucket exists
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    date_obj = datetime.strptime(ds, '%Y-%m-%d')
    object_name = f"raw/weather/year={date_obj.year}/month={date_obj.month:02d}/date={date_obj.day:02d}/weather.parquet"
    
    client.put_object(
        BUCKET_NAME,
        object_name,
        parquet_buffer,
        length=parquet_buffer.getbuffer().nbytes,
        content_type="application/parquet"
    )
    logging.info(f"Successfully uploaded weather data to s3://{BUCKET_NAME}/{object_name}")

with DAG('weather_ingestion_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    ingest_task = PythonOperator(
        task_id='fetch_and_upload_weather_data',
        python_callable=fetch_weather_data,
        provide_context=True,
    )
