import pandas as pd
import os

os.makedirs("data", exist_ok=True)

data = [
    {"state": "Delhi", "district": "Delhi", "market": "Azadpur", "commodity": "Onion", "min_price": 1600, "max_price": 2200, "modal_price": 1900, "arrival_date": "28/09/2026"},
    {"state": "Delhi", "district": "Delhi", "market": "Okhla", "commodity": "Onion", "min_price": 1650, "max_price": 2150, "modal_price": 1880, "arrival_date": "28/09/2026"},
    {"state": "Delhi", "district": "Delhi", "market": "Ghazipur", "commodity": "Onion", "min_price": 1580, "max_price": 2100, "modal_price": 1850, "arrival_date": "28/09/2026"},
    {"state": "Maharashtra", "district": "Nashik", "market": "Lasalgaon", "commodity": "Onion", "min_price": 1400, "max_price": 1950, "modal_price": 1700, "arrival_date": "28/09/2026"},
    {"state": "Punjab", "district": "Amritsar", "market": "Amritsar", "commodity": "Onion", "min_price": 1700, "max_price": 2300, "modal_price": 2000, "arrival_date": "28/09/2026"}
]

df = pd.DataFrame(data)
df.to_parquet("data/mandi_prices_live.parquet", index=False)
print("? Local data Parquet file successfully created at data/mandi_prices_live.parquet!")
