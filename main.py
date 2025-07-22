# main.py
import asyncio
from alpaca_trade_api.stream import Stream
import pandas as pd
import config
from modules.mind import LOGGER
from modules.tide import determine_tide_state
from modules.swell import determine_strongest_swells
from modules.wave import TradeManager
from data_procurement import get_historical_data, api

async def main():
    LOGGER.info("--- Surfer Algorithm Initializing (Live Mode) ---")
    current_tide = determine_tide_state()
    target_sectors, trade_direction = determine_strongest_swells(current_tide)

    if not target_sectors:
        LOGGER.info("--- No high-quality signals today. Algorithm is idle. ---")
        return

    LOGGER.info(f"Final targets for today: {target_sectors} with direction: {trade_direction}")

    trade_manager = TradeManager(api_client=api)
    historical_data_cache = get_historical_data(target_sectors, days=50)

    if not historical_data_cache:
        LOGGER.error("Could not fetch initial historical data. Shutting down.")
        return

    # This is the correct place for the data_feed argument
    stream = Stream(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY,
                    base_url=config.ALPACA_BASE_URL, data_feed='iex')

    async def trade_callback(t):
        LOGGER.info(f"LIVE TICK: {t.symbol} Price={t.price}")
        symbol = t.symbol
        new_price = t.price
        if symbol in historical_data_cache:
            new_row = pd.DataFrame([{'close': new_price}], index=[pd.Timestamp.now(tz='UTC')])
            historical_data_cache[symbol] = pd.concat([historical_data_cache[symbol].iloc[1:], new_row])
            trade_manager.process_tick_data(
                symbol=symbol, price=new_price,
                historical_data=historical_data_cache[symbol],
                direction=trade_direction
            )

    for sector in target_sectors:
        stream.subscribe_trades(trade_callback, sector)

    LOGGER.info("Connection established. Listening for live market data...")
    await stream.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Algorithm manually terminated.")
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred in main loop: {e}", exc_info=True)