import os
import json
import logging
from datetime import datetime
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATA_GOV_API_KEY = os.getenv("DATA_GOV_IN_API_KEY")
if not DATA_GOV_API_KEY:
    raise ValueError("DATA_GOV_IN_API_KEY environment variable is missing. Ensure it is set securely in your .env file.")

logging.basicConfig(level=logging.INFO)

def fetch_mandi_data(ds):
    url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={DATA_GOV_API_KEY}&format=json&offset=0&limit=100"
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
            logging.info("Successfully fetched live records. Top 5 records:")
            for rec in records[:5]:
                logging.info(json.dumps(rec, indent=2))
        
        df = pd.DataFrame(records)
        os.makedirs("data", exist_ok=True)
        df.to_parquet("data/mandi_prices_live.parquet", index=False)
        logging.info("Live data successfully saved locally to data/mandi_prices_live.parquet")
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise

if __name__ == "__main__":
    today = datetime.now().strftime('%Y-%m-%d')
    fetch_mandi_data(ds=today)
