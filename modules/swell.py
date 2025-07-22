import pandas as pd
import pandas_ta as ta

from modules.mind import LOGGER
import config
from data_procurement import get_historical_data

def determine_strongest_swells(tide_state: str) -> (list, str):
    if tide_state == "NEUTRAL":
        """
        If the tide is neutral, we skip the swell analysis.
        This avoids unnecessary computations and logging.
        """
        LOGGER.info("Tide is NEUTRAL. Swell analysis skipped.")
        return [], None
    """
    Analyzes a universe of ETFs to find the top/bottom performers.
    Returns a list of target symbols and a trade direction.
    """
    if tide_state == "NEUTRAL":
        LOGGER.info("Tide is NEUTRAL. Swell analysis skipped.")
        return [], None

    LOGGER.info(f"Determining Swells for a {tide_state} environment...")
    
    universe_with_benchmark = config.SECTOR_UNIVERSE + [config.BENCHMARK_SYMBOL]
    historical_data = get_historical_data(universe_with_benchmark, days=config.SWELL_LOOKBACK_DAYS)
    spy_data = historical_data[config.BENCHMARK_SYMBOL]
    sector_data = {sym: df for sym, df in historical_data.items() if sym != config.BENCHMARK_SYMBOL}

    momentum_scores = []
    LOGGER.info("Calculating momentum scores for each sector...")

    for symbol, df in sector_data.items():
        # --- B1: Relative Strength ---
        sector_return = df['Close'].iloc[-1] / df['Close'].iloc[-90]
        spy_return = spy_data['Close'].iloc[-1] / spy_data['Close'].iloc[-90]
        rs_score = sector_return / spy_return

        # --- B2: Absolute Momentum ---
        # pandas_ta calculates Rate of Change and adds it as a column
        df.ta.roc(length=30, append=True)
        df.ta.roc(length=90, append=True)
        df.ta.roc(length=180, append=True)
        
        am_score = (
            (df['ROC_180'].iloc[-1] * 0.5) +
            (df['ROC_90'].iloc[-1] * 0.3) +
            (df['ROC_30'].iloc[-1] * 0.2)
        )

        # --- B3: Trend Health ---
        df.ta.sma(length=50, append=True)
        df.ta.sma(length=200, append=True)
        price = df['Close'].iloc[-1]
        
        th_score = 0
        if price > df['SMA_50'].iloc[-1] and price > df['SMA_200'].iloc[-1]: th_score = 1
        elif price < df['SMA_50'].iloc[-1] and price < df['SMA_200'].iloc[-1]: th_score = -1
        
        # --- Final Score ---
        # Note: In a real system, you would normalize these scores before weighting
        final_score = (
            rs_score * config.MOMENTUM_SCORE_WEIGHTS['Relative_Strength'] +
            am_score * config.MOMENTUM_SCORE_WEIGHTS['Absolute_Momentum'] +
            th_score * config.MOMENTUM_SCORE_WEIGHTS['Trend_Health']
        )
        momentum_scores.append({'symbol': symbol, 'score': final_score})

    # --- Rank and Select ---
    ranked_sectors = sorted(momentum_scores, key=lambda x: x['score'], reverse=True)
    
    LOGGER.info("--- Sector Momentum Ranking ---")
    for item in ranked_sectors:
        LOGGER.info(f"  {item['symbol']}: {item['score']:.4f}")

    if tide_state == "RISK_ON":
        target_sectors = [ranked_sectors[0]['symbol'], ranked_sectors[1]['symbol']]
        trade_direction = "LONG"
        LOGGER.info(f"Tide is RISK_ON. Top targets selected: {target_sectors}")
        return target_sectors, trade_direction
    
    elif tide_state == "RISK_OFF":
        target_sectors = [ranked_sectors[-1]['symbol'], ranked_sectors[-2]['symbol']]
        trade_direction = "SHORT"
        LOGGER.info(f"Tide is RISK_OFF. Weakest targets selected: {target_sectors}")
        return target_sectors, trade_direction
    
    return [], None

