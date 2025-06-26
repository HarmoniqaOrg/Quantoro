import os
import logging
import pandas as pd
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Adjust path to import from src
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.loader import FmpDataLoader
from src.data.processor import DataProcessor
from src.optimization.cvar_optimizer import CVaROptimizer, RollingCVaROptimizer
from src.backtesting.metrics import calculate_performance_metrics
from src.ml.regime import RegimeDetector

class RegimeAwareCVaROptimizer(CVaROptimizer):
    """An optimizer that adjusts parameters based on the market regime."""
    def optimize_with_regime(self, returns, benchmark_returns, regime, current_weights=None):
        if regime == 0:  # Risk-off
            logging.info("Regime: Risk-Off. Using conservative parameters.")
            self.alpha = 0.99
            self.lasso_penalty = 0.005
        else:  # Risk-on
            logging.info("Regime: Risk-On. Using standard parameters.")
            self.alpha = 0.95
            self.lasso_penalty = 0.01
        
        return self.optimize(returns, benchmark_returns, current_weights)

async def main():
    """Main function to run the enhanced backtest."""
    logging.info("--- Starting Enhanced (Regime-Aware) Backtest Script ---")
    # --- Parameters ---
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        logging.error("FMP_API_KEY not found.")
        return

    UNIVERSE_TICKERS = [
        'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'GOOG', 'META', 'TSLA',
        'BRK-B', 'JPM', 'JNJ', 'V', 'UNH', 'PG', 'MA', 'HD',
        'BAC', 'CVX', 'LLY', 'XOM', 'AVGO', 'COST', 'ABBV', 'PFE',
        'MRK', 'PEP', 'KO', 'ADBE', 'CSCO', 'WMT', 'MCD', 'ACN',
        'CRM', 'TMO', 'DIS', 'LIN', 'NFLX', 'ABT', 'DHR', 'WFC',
        'CMCSA', 'VZ', 'NEE', 'NKE', 'PM', 'TXN', 'HON', 'UPS',
        'LOW', 'RTX', 'MS', 'INTC', 'GS', 'AMD', 'IBM', 'SBUX',
        'CAT', 'DE', 'UNP', 'BA'
    ]
    BENCHMARK_TICKER = "SPY"
    START_DATE = "2019-01-01"  # Start earlier to have enough data for long SMA
    END_DATE = "2024-12-31"
    BACKTEST_START_DATE = "2020-01-01"

    # --- Data Loading and Processing ---
    loader = FmpDataLoader(api_key=FMP_API_KEY)
    processor = DataProcessor()

    all_tickers = UNIVERSE_TICKERS + [BENCHMARK_TICKER]
    price_data = await loader.get_multiple_tickers_data(all_tickers, start_date=START_DATE, end_date=END_DATE)
    
    # --- Regime Detection ---
    regime_detector = RegimeDetector(lookback_short=50, lookback_long=200)
    spy_prices = price_data[BENCHMARK_TICKER]
    regime_signals = regime_detector.detect_regime(spy_prices)

    # --- Process Returns ---
    returns_data = processor.calculate_returns(price_data)
    cleaned_returns = processor.clean_data(returns_data)

    final_universe = [t for t in cleaned_returns.columns if t != BENCHMARK_TICKER]
    asset_returns = cleaned_returns[final_universe]
    benchmark_returns = cleaned_returns[BENCHMARK_TICKER]

    # --- Run Rolling Backtest with Regime Awareness ---
    regime_optimizer = RegimeAwareCVaROptimizer()
    
    # Custom backtest loop to include regime
    logging.info("Starting regime-aware rolling backtest...")
    lookback = 252
    rebalance_dates = pd.date_range(start=BACKTEST_START_DATE, end=END_DATE, freq='BQ').to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]

    all_weights = {}
    current_weights = pd.Series(1/len(final_universe), index=final_universe)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        hist_benchmark = benchmark_returns.loc[start_window:date]
        current_regime = regime_signals.loc[date]

        try:
            opt_result = regime_optimizer.optimize_with_regime(hist_returns, hist_benchmark, current_regime, current_weights)
            if opt_result['status'] == 'optimal':
                current_weights = opt_result['weights']
            else:
                logging.warning(f"Optimization non-optimal on {date}. Holding weights.")
        except Exception as e:
            logging.error(f"Optimization failed on {date}: {e}. Holding weights.")
        
        all_weights[date] = current_weights

    weights_df = pd.DataFrame(all_weights).T.reindex(asset_returns.index, method='ffill').dropna()
    portfolio_returns = (weights_df * asset_returns).sum(axis=1).loc[BACKTEST_START_DATE:]

    logging.info("Backtest completed.")

    # --- Calculate and Save Performance Metrics ---
    aligned_benchmark = benchmark_returns.loc[portfolio_returns.index]
    performance_metrics = calculate_performance_metrics(portfolio_returns, aligned_benchmark)

    results_path = Path("results")
    (results_path).mkdir(exist_ok=True)
    metrics_path = results_path / "enhanced_cvar_performance_metrics.csv"
    performance_metrics.to_csv(metrics_path)

    logging.info(f"Enhanced performance metrics saved to {metrics_path}")
    print("\n--- Enhanced Performance Metrics ---")
    print(performance_metrics)

if __name__ == "__main__":
    asyncio.run(main())
