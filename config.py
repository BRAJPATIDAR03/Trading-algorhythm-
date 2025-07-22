# config.py

# --- API Keys & Endpoints ---
# IMPORTANT: Make sure these keys are correct and have the necessary permissions.
ALPACA_API_KEY = 'PK5DGDYI3USJT5573VNR'
ALPACA_SECRET_KEY = 'l49Q5thKGHI8D5F27Feg4yZeJYeXjklG9OeoR4hy'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'
FRED_API_KEY = '2f914084f2b27a61035bc279ba069e59'

# --- Module 1: The Tide Parameters ---
TIDE_SCORE_THRESHOLDS = {
    'RISK_ON': 3,
    'RISK_OFF': -3
}
TIDE_INDICATOR_WEIGHTS = {
    'Interest_Rates': 1.2,
    'Inflation': 1.0,
    'GDP': 0.8,
    'VIX': 1.5,
    'Market_Trend': 1.5,
    'Market_Breadth': 1.0,
    'USD_Strength': 0.8,
    'Credit_Spreads': 1.2
}
VIX_THRESHOLDS = {
    'FEAR': 30,
    'CALM': 20
}

# --- Module 2: The Swell Parameters ---
SECTOR_UNIVERSE = ['XLK', 'XLF', 'XLV', 'XLE', 'XLI', 'XLC', 'XLY', 'XLP', 'XLU']
BENCHMARK_SYMBOL = 'SPY'
SWELL_LOOKBACK_DAYS = 200
MOMENTUM_SCORE_WEIGHTS = {
    'Relative_Strength': 0.4,
    'Absolute_Momentum': 0.4,
    'Trend_Health': 0.2
}

# --- Module 3: The Wave Parameters ---
WAVE_RISK_PER_TRADE = 0.01 # Risk 1% of total capital per trade
WAVE_BBANDS_PERIOD = 20
WAVE_EMA_PERIOD = 10