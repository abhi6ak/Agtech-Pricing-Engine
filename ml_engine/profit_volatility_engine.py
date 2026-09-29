import pandas as pd
import numpy as np

def calculate_net_profit(mandi_rate, logistics_cost, handling_fee, perishable_index, transit_hours, base_value):
    """
    Net Farmer Profit = Mandi Rate - (Logistics Cost + Handling Fee + Spoilage Risk)
    Spoilage Risk = Perishable Index (0 to 1) * Transit Time (Hours) * Crop Base Value.
    """
    spoilage_risk = perishable_index * transit_hours * base_value
    net_profit = mandi_rate - (logistics_cost + handling_fee + spoilage_risk)
    return net_profit

def detect_volatility(df, price_col='modal_price', window=3, threshold=0.15):
    """
    Identify >15-20% price fluctuations over a rolling 3-day window.
    """
    df = df.sort_values(by='arrival_date')
    df['rolling_min'] = df[price_col].rolling(window=window).min()
    df['rolling_max'] = df[price_col].rolling(window=window).max()
    
    df['fluctuation_pct'] = (df['rolling_max'] - df['rolling_min']) / df['rolling_min']
    df['is_volatile'] = df['fluctuation_pct'] > threshold
    return df[df['is_volatile'] == True]

if __name__ == "__main__":
    print("Net Profit Example:")
    profit = calculate_net_profit(1500, 100, 50, 0.05, 12, 1000)
    print(f"Calculated Profit: {profit}")
