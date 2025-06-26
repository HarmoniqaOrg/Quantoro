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
from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display
from src.ml.regime import RegimeDetector

class RegimeAwareCVaROptimizer(CVaROptimizer):
    """An optimizer that adjusts parameters based on the market regime."""
    def optimize_with_regime(self, returns, benchmark_returns, regime, current_weights=None):
        if regime == 0:  # Risk-off
            self.alpha = 0.99
            self.lasso_penalty = 0.5  # Less sparsity, more diversification in crisis
            self.max_weight = 0.04    # Lower concentration
            logging.info(
                f"Entering RISK-OFF regime. Adjusting CVaR alpha to {self.alpha}, "
                f"LASSO to {self.lasso_penalty}, max_weight to {self.max_weight}."
            )
        else:  # Risk-on
            self.alpha = 0.95
            self.lasso_penalty = 2.0  # More sparsity, concentrate on winners
            self.max_weight = 0.05
            logging.info(
                f"Entering RISK-ON regime. Adjusting CVaR alpha to {self.alpha}, "
                f"LASSO to {self.lasso_penalty}, max_weight to {self.max_weight}."
            )
        
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
    BACKTEST_END_DATE = "2024-12-31"

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
    rebalance_dates = pd.date_range(start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq='BQ').to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]

    all_weights = {}
    current_weights = pd.Series(1/len(final_universe), index=final_universe)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        hist_benchmark = benchmark_returns.loc[start_window:date]
        current_regime = regime_signals.loc[date]

        try:
            # Pass numpy array for current_weights and use attribute access for results
            opt_result = regime_optimizer.optimize_with_regime(
                hist_returns, hist_benchmark, current_regime, current_weights.values
            )
            
            if opt_result and opt_result.status in ['optimal', 'optimal_inaccurate']:
                current_weights = pd.Series(opt_result.weights, index=hist_returns.columns)
                logging.info(f"Rebalanced on {date}: CVaR={opt_result.cvar:.4f}, Status={opt_result.status}")
            else:
                status = opt_result.status if opt_result else 'unknown failure'
                logging.warning(f"Optimization non-optimal on {date} with status {status}. Holding weights.")
        
        except Exception as e:
            logging.error(f"Optimization failed on {date}: {e}. Holding weights.")
        
        all_weights[date] = current_weights

    weights_df = pd.DataFrame(all_weights).T.reindex(asset_returns.index, method='ffill').dropna()
    portfolio_returns = (weights_df * asset_returns).sum(axis=1).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]

    logging.info("Backtest completed.")

    # --- Calculate and Save Performance Metrics ---
    aligned_benchmark = benchmark_returns.loc[portfolio_returns.index]
    raw_metrics = calculate_raw_metrics(portfolio_returns, aligned_benchmark)
    display_metrics = format_metrics_for_display(raw_metrics, portfolio_returns)
    
    # Print metrics to console
    logging.info("\n--- Regime-Aware Performance Metrics ---\n" + display_metrics.to_string())

    # --- Save Results ---
    logging.info("Saving Enhanced CVaR results...")
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Save weights and metrics
    weights_df = pd.DataFrame(all_weights).T
    weights_df.index.name = 'Date'
    weights_path = results_dir / 'enhanced_cvar_weights.csv'
    weights_df.to_csv(weights_path)
    logging.info(f"Enhanced CVaR weights saved to {weights_path}")
    
    raw_metrics.to_csv(results_dir / 'enhanced_cvar_performance_metrics.csv', header=True)
    logging.info(f"Enhanced CVaR metrics saved to {results_dir / 'enhanced_cvar_performance_metrics.csv'}")

    # --- Update Consolidated Returns ---
    logging.info(f"Updating consolidated returns file: {results_dir / 'daily_returns.csv'}")
    try:
        consolidated_returns_path = results_dir / 'daily_returns.csv'
        consolidated_returns = pd.read_csv(consolidated_returns_path, index_col=0, parse_dates=True)
        
        column_name = 'regime_aware_cvar_index'
        if column_name in consolidated_returns.columns:
            consolidated_returns = consolidated_returns.drop(columns=[column_name])
        
        portfolio_returns.name = column_name
        consolidated_returns = consolidated_returns.join(portfolio_returns, how='outer')
        consolidated_returns.to_csv(consolidated_returns_path)
        logging.info("Successfully updated consolidated returns.")

    except FileNotFoundError:
        logging.error("daily_returns.csv not found. It should be created by the baseline backtest first. Aborting.")
        return # Exit if the base file doesn't exist
    except Exception as e:
        logging.error(f"Failed to update consolidated returns: {e}")

    logging.info("--- Enhanced Backtest Complete ---")



if __name__ == "__main__":
    asyncio.run(main())
