from datetime import datetime, timedelta
import numpy as np

def get_interest_rate_vector():
    """Get interest rate trend from Fed data"""
    # In real implementation, fetch from Fed API
    return "STABLE"

def get_inflation_vector():
    """Get inflation trend from economic data"""
    # In real implementation, fetch from economic API
    return "STABLE"

def get_gdp_vector():
    """Get GDP trend from economic data"""
    # In real implementation, fetch from economic API
    return "STABLE"

def get_market_breadth():
    """Calculate market breadth from NYSE data"""
    try:
        # Get advance-decline data
        advancers = api.get_bars("$ADVN", TimeFrame.Day, limit=1).df['close'].iloc[-1]
        decliners = api.get_bars("$DECN", TimeFrame.Day, limit=1).df['close'].iloc[-1]
        
        ratio = advancers / (advancers + decliners)
        if ratio > 0.55:
            return "UPTREND"
        elif ratio < 0.45:
            return "DOWNTREND"
        return "MIXED"
    except:
        return "MIXED"

def get_credit_spreads():
    """Get credit spread trend from bond market"""
    try:
        # Compare high-yield to investment grade spreads
        hyg = api.get_bars("HYG", TimeFrame.Day, limit=2).df
        lqd = api.get_bars("LQD", TimeFrame.Day, limit=2).df
        
        spread_today = hyg['close'].iloc[-1] / lqd['close'].iloc[-1]
        spread_yesterday = hyg['close'].iloc[-2] / lqd['close'].iloc[-2]
        
        if spread_today < spread_yesterday:
            return "NARROWING"
        elif spread_today > spread_yesterday:
            return "WIDENING"
        return "STABLE"
    except:
        return "STABLE"