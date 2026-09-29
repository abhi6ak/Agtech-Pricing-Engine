import os
import json
import logging
from datetime import datetime, timedelta
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

#from airflow import DAG
#from airflow.operators.python import PythonOperator
#from minio import Minio
#import io

DATA_GOV_API_KEY = os.getenv("DATA_GOV_IN_API_KEY")
if not DATA_GOV_API_KEY:
    raise ValueError(" api key ")

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

def fetch_mandi_data(ds, **kwargs):
    # Actual API URL for data.gov.in mandi prices
    url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={"579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"}&format=json&offset=0&limit=1000"
    
    # Hide the API key in the logs
    safe_url_log = url.replace(DATA_GOV_API_KEY, "******_HIDDEN_API_KEY_******")
    logging.info(f"Fetching LIVE data from actual Government URL: {safe_url_log}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        records = data.get('records', [])
        
        if not records:
            logging.warning("API returned no records!")
        else:
            logging.info("Successfully fetched live records. Here are the top 5 raw records for cross-checking:")
            for rec in records[:5]:
                logging.info(json.dumps(rec, indent=2))
        
        df = pd.DataFrame(records)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise

    # Convert to Parquet
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)

    os.makedirs("data", exist_ok=True)
    df.to_parquet("data/mandi_prices_live.parquet", index=False)
    print("✅ Live data successfully saved locally to data/mandi_prices_live.parquet")
    
    # Ensure bucket exists
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

    date_obj = datetime.strptime(ds, '%Y-%m-%d')
    object_name = f"raw/mandi/year={date_obj.year}/month={date_obj.month:02d}/date={date_obj.day:02d}/mandi_prices.parquet"
    
    client.put_object(
        BUCKET_NAME,
        object_name,
        parquet_buffer,
        length=parquet_buffer.getbuffer().nbytes,
        content_type="application/parquet"
    )
    logging.info(f"Successfully uploaded to s3://{BUCKET_NAME}/{object_name}")

if __name__ == "__main__":
    # Aaj ki date nikal kar function ko pass kar rahe hain
    today_date = datetime.now().strftime('%Y-%m-%d')
    print(f"Starting manual mandi ingestion for {today_date}...")
    fetch_mandi_data(ds=today_date)
    print("Mandi data ingestion complete!")