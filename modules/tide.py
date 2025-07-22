# modules/tide.py
from modules.mind import LOGGER
import config
from data_procurement import get_live_tide_data

def determine_tide_state():
    LOGGER.info("Determining Tide State...")
    data = get_live_tide_data()
    tide_score = 0.0
    # Scoring logic using data.get() for safety
    if data.get('Interest_Rate_Vector') == "FALLING": tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['Interest_Rates']
    elif data.get('Interest_Rate_Vector') == "RISING": tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['Interest_Rates']
    if data.get('VIX_Level', 25) < config.VIX_THRESHOLDS['CALM']: tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['VIX']
    elif data.get('VIX_Level', 25) > config.VIX_THRESHOLDS['FEAR']: tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['VIX']
    if data.get('Market_Trend') == "ABOVE": tide_score += 1 * config.TIDE_INDICATOR_WEIGHTS['Market_Trend']
    elif data.get('Market_Trend') == "BELOW": tide_score -= 1 * config.TIDE_INDICATOR_WEIGHTS['Market_Trend']
    LOGGER.info(f"Final Tide Score calculated: {tide_score:.2f}")
    if tide_score >= config.TIDE_SCORE_THRESHOLDS['RISK_ON']: final_state = "RISK_ON"
    elif tide_score <= config.TIDE_SCORE_THRESHOLDS['RISK_OFF']: final_state = "RISK_OFF"
    else: final_state = "NEUTRAL"
    LOGGER.info(f"Tide State for today is: {final_state}")
    return final_state