from modules.mind import LOGGER
from modules.tide import determine_tide_state
from modules.swell import determine_strongest_swells

def run_surfer():
    LOGGER.info("--- Surfer Algorithm Initializing ---")
    
    # Run Module 1: The Tide
    current_tide = determine_tide_state()
    
    # Run Module 2: The Swell
    target_sectors, trade_direction = determine_strongest_swells(current_tide)
    
    # Later, we will pass these targets to Module 3
    if target_sectors:
        LOGGER.info(f"Final targets for today: {target_sectors} with direction: {trade_direction}")
    
    LOGGER.info("--- Surfer Algorithm Run Complete ---")

if __name__ == "__main__":
    run_surfer()