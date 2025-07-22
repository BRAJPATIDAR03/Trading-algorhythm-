from modules.mind import LOGGER
import config
from data_procurement import get_simulated_tide_data

def determine_tide_state() -> str:
    """
    Analyzes macro data to determine the market's risk state.
    Uses a weighted scoring system from the config file.
    """
    LOGGER.info("Determining Tide State...")
    data = get_simulated_tide_data()
    tide_score = 0.0

    # --- Economic Scores ---
    if data['Interest_Rate_Vector'] == "FALLING":
        tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['Interest_Rates']
    elif data['Interest_Rate_Vector'] == "RISING":
        tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['Interest_Rates']

    if data['Inflation_Vector'] == "DECELERATING":
        tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['Inflation']
    elif data['Inflation_Vector'] == "ACCELERATING":
        tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['Inflation']
    
    # ... You can add more detailed logic for other indicators ...

    # --- Market Internal Scores ---
    if data['VIX_Level'] < config.VIX_THRESHOLDS['CALM']:
        tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['VIX']
    elif data['VIX_Level'] > config.VIX_THRESHOLDS['FEAR']:
        tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['VIX']
    
    if data['Market_Trend'] == "ABOVE":
        tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['Market_Trend']
    elif data['Market_Trend'] == "BELOW":
        tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['Market_Trend']
        
    # ... Add logic for Market_Breadth, etc. ...

    # --- Inter-Market Scores ---
    if data['USD_Strength'] == "FALLING":
        tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['USD_Strength']
    elif data['USD_Strength'] == "RISING":
        tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['USD_Strength']

    if data['Credit_Spreads'] == "NARROWING":
        tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['Credit_Spreads']
    elif data['Credit_Spreads'] == "WIDENING":
        tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['Credit_Spreads']

    # --- Determine Final State ---
    LOGGER.info(f"Final Tide Score calculated: {tide_score:.2f}")

    if tide_score >= config.TIDE_SCORE_THRESHOLDS['RISK_ON']:
        final_state = "RISK_ON"
    elif tide_score <= config.TIDE_SCORE_THRESHOLDS['RISK_OFF']:
        final_state = "RISK_OFF"
    else:
        final_state = "NEUTRAL"
        
    LOGGER.info(f"Tide State for today is: {final_state}")
    return final_state