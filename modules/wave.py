# modules/wave.py
import pandas as pd
import pandas_ta as ta
import csv
from datetime import datetime
from modules.mind import LOGGER
import config

def log_trade_result(symbol, direction, entry_price, exit_price, size, pnl):
    file_path = 'trade_results.csv'
    headers = ['Timestamp', 'Symbol', 'Direction', 'EntryPrice', 'ExitPrice', 'PositionSize', 'PnL']
    try:
        with open(file_path, 'r') as f:
            pass
    except FileNotFoundError:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), symbol, direction,
            f"{entry_price:.2f}", f"{exit_price:.2f}", f"{size:.4f}", f"{pnl:.2f}"
        ])

class TradeManager:
    def __init__(self, api_client):
        self.api = api_client
        self.open_positions = {}

    def process_tick_data(self, symbol: str, price: float, historical_data: pd.DataFrame, direction: str):
        if symbol in self.open_positions:
            self._manage_open_position(symbol, price, historical_data)
        else:
            self._check_for_entry_signal(symbol, price, historical_data, direction)

    def _check_for_entry_signal(self, symbol: str, price: float, df: pd.DataFrame, direction: str):
        df.ta.bbands(length=config.WAVE_BBANDS_PERIOD, append=True)
        upper_band = df[f'BBU_{config.WAVE_BBANDS_PERIOD}_2.0'].iloc[-1]
        lower_band = df[f'BBL_{config.WAVE_BBANDS_PERIOD}_2.0'].iloc[-1]
        if direction == "LONG" and price > upper_band:
            LOGGER.info(f"ENTRY SIGNAL for {symbol}: Price {price:.2f} broke above upper BBand {upper_band:.2f}")
            self._execute_trade(symbol, "LONG", price, lower_band)
        elif direction == "SHORT" and price < lower_band:
            LOGGER.info(f"ENTRY SIGNAL for {symbol}: Price {price:.2f} broke below lower BBand {lower_band:.2f}")
            self._execute_trade(symbol, "SHORT", price, upper_band)

    def _execute_trade(self, symbol: str, direction: str, entry_price: float, stop_loss_price: float):
        LOGGER.info(f"--- EXECUTING TRADE: {direction} {symbol} at {entry_price:.2f} ---")
        total_capital = 100000
        risk_amount_per_trade = total_capital * config.WAVE_RISK_PER_TRADE
        risk_per_share = abs(entry_price - stop_loss_price)
        if risk_per_share == 0:
            LOGGER.warning("Risk per share is zero, aborting trade.")
            return
        position_size = risk_amount_per_trade / risk_per_share
        LOGGER.info(f"  Capital: ${total_capital}, Risk Per Trade: ${risk_amount_per_trade:.2f}")
        LOGGER.info(f"  Stop Loss: {stop_loss_price:.2f}, Risk/Share: ${risk_per_share:.2f}")
        LOGGER.info(f"  Calculated Position Size: {position_size:.4f} shares")
        self.open_positions[symbol] = {
            "direction": direction, "entry_price": entry_price,
            "stop_loss": stop_loss_price, "size": position_size
        }
        LOGGER.info(f"Trade for {symbol} is now LIVE.")

    def _manage_open_position(self, symbol: str, price: float, df: pd.DataFrame):
        df.ta.ema(length=10, append=True)
        ema_10 = df['EMA_10'].iloc[-1]
        position = self.open_positions[symbol]
        exit_signal = False
        if position['direction'] == "LONG" and price < ema_10:
            LOGGER.info(f"EXIT SIGNAL for {symbol}: Price {price:.2f} crossed below 10-EMA {ema_10:.2f}")
            exit_signal = True
        elif position['direction'] == "SHORT" and price > ema_10:
            LOGGER.info(f"EXIT SIGNAL for {symbol}: Price {price:.2f} crossed above 10-EMA {ema_10:.2f}")
            exit_signal = True
        if exit_signal:
            LOGGER.info(f"--- CLOSING TRADE for {symbol} at {price:.2f} ---")
            entry_price = position['entry_price']
            exit_price = price
            trade_size = position['size']
            if position['direction'] == "LONG":
                pnl = (exit_price - entry_price) * trade_size
            else:
                pnl = (entry_price - exit_price) * trade_size
            log_trade_result(symbol, position['direction'], entry_price, exit_price, trade_size, pnl)
            LOGGER.info(f"Trade P&L: ${pnl:.2f}")
            del self.open_positions[symbol]