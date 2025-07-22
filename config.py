# --- API Keys & Endpoints (Replace with your actual keys later) ---
ALPACA_API_KEY = 'PK5DGDYI3USJT5573VNR'
ALPACA_SECRET_KEY = 'l49Q5thKGHI8D5F27Feg4yZeJYeXjklG9OeoR4hy'
ALPACA_BASE_URL = 'https://app.alpaca.markets/' # Use paper trading endpoint for development
FRED_API_KEY = 'e9e3d30f7eff81b9aeab42807c86728a'

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
WAVE_ATR_PERIOD = 14
WAVE_ATR_MULTIPLIER = 2.0 # For the trailing stop loss
WAVE_RSI_PERIOD = 14
WAVE_RSI_THRESHOLDS = {
    'LONG': 50,
    'SHORT': 50
}
WAVE_BBANDS_PERIOD = 20