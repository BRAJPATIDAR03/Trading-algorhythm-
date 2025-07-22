# data_procurement.py
import pandas as pd
import yfinance as yf
from modules.mind import LOGGER
import config
import numpy as np

def get_historical_data(symbols: list, days: int):
    LOGGER.info(f"Fetching FREE historical data for {symbols} via yfinance...")
    try:
        # yfinance fetches data differently, so we adjust the period
        period = f"{days}d"
        # Download data for all symbols at once
        data = yf.download(symbols, period=period, progress=False)
        
        # If fetching a single symbol, the structure is simpler
        if len(symbols) == 1:
            return {symbols[0]: data}
            
        # For multiple symbols, we need to split the multi-level DataFrame
        data_dict = {symbol: data.xs(symbol, level=1, axis=1) for symbol in symbols}
        return data_dict
    except Exception as e:
        LOGGER.error(f"Failed to fetch yfinance data: {e}. Critical error.")
        return {}

# --- The Tide module's data fetcher can now be simplified ---
def get_live_tide_data():
    LOGGER.info("Fetching data for Tide module...")
    live_data = {}
    
    proxies = ['SPY'] 
    market_data = get_historical_data(proxies, 250)
    
    spy_df = market_data.get('SPY')
    if spy_df is not None and not spy_df.empty and len(spy_df) >= 200:
        spy_price = spy_df['Close'].iloc[-1]
        spy_200ma = spy_df['Close'].rolling(window=200).mean().iloc[-1]
        live_data['Market_Trend'] = "ABOVE" if spy_price > spy_200ma else "BELOW"
    else:
        live_data['Market_Trend'] = "NEUTRAL"
    
    # Set other proxies to neutral as they are harder to get reliably for free
    live_data['VIX_Level'] = 25 # Placeholder
    live_data['Credit_Spreads'] = "STABLE"
    live_data['Market_Breadth'] = "NEUTRAL"
    live_data['USD_Strength'] = "STABLE"
    live_data['Interest_Rate_Vector'] = "STABLE"
    live_data['Inflation_Vector'] = "STABLE"
    live_data['GDP_Vector'] = "STABLE"
    
    LOGGER.info(f"Live data obtained: {live_data}")
    return live_data