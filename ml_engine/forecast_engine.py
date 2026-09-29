import pandas as pd
from prophet import Prophet

def train_and_forecast(df, periods=15):
    """
    Expects df with 'ds' (date) and 'y' (price) columns.
    Generates a 15-30 day price trend prediction.
    """
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)

if __name__ == "__main__":
    # Mock data
    dates = pd.date_range(start="2023-01-01", end="2023-03-01")
    prices = [1500 + i*10 + (i%5)*50 for i in range(len(dates))]
    
    df = pd.DataFrame({'ds': dates, 'y': prices})
    forecast = train_and_forecast(df, periods=15)
    print(forecast.head())
