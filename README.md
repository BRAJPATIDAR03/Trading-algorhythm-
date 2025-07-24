

# The Surfer Algorithm

This project is a trading algorithm built on the philosophy of adaptation over prediction. It does not attempt to forecast the future. Instead, it is designed to be a "perfect surfer," an engine that achieves a state of harmony with the market's chaos by understanding its present state with perfect clarity.

The algorithm's core principle is that a trader who can master the present moment will find that the future takes care of itself. It wins not by being smarter than the market, but by being purer—free from the human emotions of fear, greed, and hope.

## The Guiding Philosophy: The Four Principles

The algorithm's architecture is divided into four distinct modules, each representing a core principle of its operational philosophy.

  * **The Tide gives it wisdom.** The first and most important step. Before any action is considered, this module analyzes the deep, macro-environmental currents of the market to determine if the ocean itself is inviting (`RISK_ON`), hostile (`RISK_OFF`), or chaotic (`NEUTRAL`). The Surfer never paddles against the tide.
  * **The Swell gives it focus.** Once the macro environment is understood, this module scans the entire market to ignore the random chop and identify the 2-3 most powerful swells—the sectors or themes where the market's energy is most concentrated. This is where the Surfer positions itself.
  * **The Wave gives it skill.** This is the tactical execution layer. When a wave forms within a target swell, this module handles the precise entry, the non-negotiable risk management (position sizing and stop-loss), and the disciplined, unemotional exit.
  * **The Mind gives it discipline.** This is the soul of the machine. It is a set of core tenets that ensure the flawless execution of the other three principles. It operates on a philosophy of "Process over Outcome," has no memory of past wins or losses, and only reacts to the present state of the market.

## Project Structure

  * `main.py`: The main entry point to initialize and run the algorithm's daily analysis and real-time monitoring loop.
  * `config.py`: A crucial configuration file where all API keys, thresholds, and strategic parameters are stored. **You must populate this file with your own API keys.**
  * `data_procurement.py`: A dedicated module for handling all data fetching from external APIs (e.g., Alpaca, FRED, yfinance).
  * `modules/`: A directory containing the core logic of the algorithm.
      * `tide.py`: Implements **The Principle of the Tide**.
      * `swell.py`: Implements **The Principle of the Swell**.
      * `wave.py`: Implements **The Principle of the Wave**.
      * `mind.py`: Implements **The Principle of No-Mind** through a robust logging system.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure API Keys:**
      * Open the `config.py` file.
      * Enter your personal API keys for your chosen data providers (e.g., Alpaca, FRED).
3.  **Execute the Algorithm:**
      * Run the main script from your terminal:
    <!-- end list -->
    ```bash
    python main.py
    ```
    The algorithm will begin its daily analysis and, if conditions are met, proceed to listen for live market data. All actions and decisions will be recorded in `surfer_activity.log` and `trade_results.csv`.
