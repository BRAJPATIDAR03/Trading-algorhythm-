import pandas as pd
from modules.mind import LOGGER
import numpy as np

def get_simulated_tide_data() -> dict:
    """
    This function simulates the data fetching process for all indicators
    required by the Tide Module. It returns a dictionary with the
    current state of each indicator.
    """
    LOGGER.info("Fetching simulated data for Tide module...")
    
    # In a real scenario, each of these would be a separate API call.
    # We are simulating a 'RISK_ON' environment here for testing.
    # Change these values to test different scenarios.
    simulated_data = {
        'Interest_Rate_Vector': "FALLING",  # FALLING is bullish (+1)
        'Inflation_Vector': "STABLE",      # STABLE is neutral (0)
        'GDP_Vector': "ACCELERATING",      # ACCELERATING is bullish (+1)
        'VIX_Level': 17,                   # Below 20 is bullish (+1)
        'Market_Trend': "ABOVE",           # Above 200DMA is bullish (+1)
        'Market_Breadth': "UPTREND",       # UPTREND is bullish (+1)
        'USD_Strength': "FALLING",         # FALLING is bullish (+1)
        'Credit_Spreads': "NARROWING"      # NARROWING is bullish (+1)
    }
    
    LOGGER.info(f"Simulated data obtained: {simulated_data}")
    return simulated_data



def get_simulated_swell_data(universe: list, days: int = 200) -> dict:
    """
    Generates a dictionary of fake historical data for a list of ETF symbols.
    We'll make some sectors clear winners and others clear losers for testing.
    """
    LOGGER.info(f"Generating {days} days of simulated historical data for {universe}...")
    data_dict = {}
    date_range = pd.to_datetime(pd.date_range(end=pd.Timestamp.now(), periods=days))

    for symbol in universe:
        # Create a base trend
        if symbol in ['XLK', 'XLY']: # Make Tech and Discretionary strong
            trend = np.linspace(100, 150, days)
        elif symbol in ['XLU', 'XLP']: # Make Utilities and Staples weak
            trend = np.linspace(100, 90, days)
        else: # Others are neutral
            trend = np.linspace(100, 105, days)
        
        # Add some noise
        noise = np.random.normal(0, 2, days)
        close_price = trend + noise

        # Create a DataFrame
        df = pd.DataFrame(index=date_range)
        df['close'] = close_price
        # You can add fake 'open', 'high', 'low', 'volume' if needed for other indicators
        
        data_dict[symbol] = df

    return data_dict

# You will add real data fetching functions here later
# e.g., get_live_tide_data()