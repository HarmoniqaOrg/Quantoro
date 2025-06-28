import os
import asyncio
import logging
from dotenv import load_dotenv

# Add project root to Python path to resolve module imports
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.alpha.fmp_signals import FmpPremiumSignals
from src.alpha.signal_processor import SignalProcessor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def main():
    """Main function to test the FmpPremiumSignals class."""
    load_dotenv()
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        logging.error("FMP_API_KEY not found in environment variables.")
        return

    signal_fetcher = FmpPremiumSignals(api_key=FMP_API_KEY)

    test_tickers = ["AAPL", "MSFT"]

    logging.info(f"Fetching premium signals for: {test_tickers}")
    all_signals = await signal_fetcher.get_all_signals_for_universe(test_tickers)

    logging.info("--- Signal Fetching Test Complete ---")

    # --- Process Signals and Generate Alpha Scores ---
    logging.info("Processing raw signals into alpha scores...")
    processor = SignalProcessor(signals_data=all_signals)
    alpha_scores = processor.generate_composite_alpha_scores()

    logging.info("--- Alpha Score Generation Complete ---")
    print("\n--- Composite Alpha Scores ---")
    print(alpha_scores)


if __name__ == "__main__":
    asyncio.run(main())
