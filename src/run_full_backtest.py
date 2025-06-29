import os
import logging
import pandas as pd
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env file
load_dotenv()

# Adjust path to import from src
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.loader import FmpDataLoader
from src.data.processor import DataProcessor
from src.optimization.cvar_optimizer import CVaROptimizer, RollingCVaROptimizer
from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display


async def main():
    """Main function to run the full backtest."""
    logging.info("--- Starting Full Backtest Script ---")
    # --- Parameters ---
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        logging.error("FMP_API_KEY not found. Please set it in your .env file.")
        return

    # Per assignment, use top 60 companies. We will use a fixed list of well-known S&P 100 companies.
    UNIVERSE_TICKERS = [
        "AAPL",
        "MSFT",
        "AMZN",
        "NVDA",
        "GOOGL",
        "GOOG",
        "META",
        "TSLA",
        "BRK-B",
        "JPM",
        "JNJ",
        "V",
        "UNH",
        "PG",
        "MA",
        "HD",
        "BAC",
        "CVX",
        "LLY",
        "XOM",
        "AVGO",
        "COST",
        "ABBV",
        "PFE",
        "MRK",
        "PEP",
        "KO",
        "ADBE",
        "CSCO",
        "WMT",
        "MCD",
        "ACN",
        "CRM",
        "TMO",
        "DIS",
        "LIN",
        "NFLX",
        "ABT",
        "DHR",
        "WFC",
        "CMCSA",
        "VZ",
        "NEE",
        "NKE",
        "PM",
        "TXN",
        "HON",
        "UPS",
        "LOW",
        "RTX",
        "MS",
        "INTC",
        "GS",
        "AMD",
        "IBM",
        "SBUX",
        "CAT",
        "DE",
        "UNP",
        "BA",
    ]
    logging.info(f"Using a fixed list of {len(UNIVERSE_TICKERS)} tickers for the backtest.")

    START_DATE = "2010-01-01"
    END_DATE = "2024-12-31"
    BENCHMARK_TICKER = "SPY"

    # --- Data Loading and Processing ---
    loader = FmpDataLoader(api_key=FMP_API_KEY)
    processor = DataProcessor()

    all_tickers = UNIVERSE_TICKERS + [BENCHMARK_TICKER]
    
    try:
        logging.info(
            f"Fetching price data for {len(all_tickers)} tickers from {START_DATE} to {END_DATE}..."
        )
        price_data = await loader.get_multiple_tickers_data(
            all_tickers, start_date=START_DATE, end_date=END_DATE
        )
        market_cap_data = await loader.get_multiple_tickers_market_cap(
            UNIVERSE_TICKERS, start_date=START_DATE, end_date=END_DATE
        )
    except Exception as e:
        logging.error(f"CRITICAL: Failed during asynchronous data fetching: {e}", exc_info=True)
        return

    # --- Save Price Data ---
    # This is needed by other scripts like the alpha backtest
    results_path = Path("results")
    results_path.mkdir(exist_ok=True)
    price_data_path = results_path / "sp500_prices_2010_2024.csv"
    try:
        logging.info(f"Saving raw price data to {price_data_path}...")
        price_data.to_csv(price_data_path)
        logging.info("Successfully saved raw price data.")
    except Exception as e:
        logging.error(f"Failed to save price data: {e}")

    returns_data = processor.calculate_returns(price_data)
    cleaned_returns = processor.clean_data(returns_data)

    # The actual universe is the set of tickers for which we successfully loaded data
    UNIVERSE_TICKERS = [ticker for ticker in cleaned_returns.columns if ticker != BENCHMARK_TICKER]
    logging.info(
        f"Successfully loaded data for {len(UNIVERSE_TICKERS)} tickers. Using this list as the final universe."
    )

    asset_returns = cleaned_returns[UNIVERSE_TICKERS]
    benchmark_returns = cleaned_returns[BENCHMARK_TICKER]

    logging.info("Data loaded and processed successfully.")

    # --- Run Rolling Backtest ---
    CVAR_ALPHA = 0.95
    TRANSACTION_COST = 0.001
    MAX_WEIGHT = 0.05
    cvar_optimizer = CVaROptimizer(
        alpha=CVAR_ALPHA,
        lasso_penalty=1.5,  # As per CLEIR paper - promotes sparsity
        transaction_cost=TRANSACTION_COST,
        max_weight=MAX_WEIGHT,
        solver="SCS",
    )
    rolling_optimizer = RollingCVaROptimizer(
        optimizer=cvar_optimizer,
        lookback_window=252,  # 1 year
        rebalance_frequency="Q",  # Quarterly
    )

    logging.info("Starting rolling backtest for the 2010-2024 period...")
    BACKTEST_START_DATE = "2010-01-01"
    BACKTEST_END_DATE = "2024-12-31"

    # The RollingCVaROptimizer's backtest method handles the rolling logic.
    rebalance_results, portfolio_returns, daily_weights = rolling_optimizer.backtest(
        returns=asset_returns,
        benchmark_returns=benchmark_returns,
        start_date=BACKTEST_START_DATE,
        end_date=BACKTEST_END_DATE,
    )

    logging.info("Backtest completed.")

    if portfolio_returns.empty:
        logging.error("Backtest returned no portfolio returns. Exiting.")
        return

    # --- Final Processing: Seeding, Cost Application, and Index Generation ---
    logging.info("Backtest method finished. Starting final processing...")
    logging.info(f"Portfolio returns received: {len(portfolio_returns)} days, from {portfolio_returns.index.min()} to {portfolio_returns.index.max()}")

    # 1. Seed the backtest for the pre-rebalance period (2010 to first rebalance)
    logging.info("Seeding backtest for the initial period...")
    first_rebalance_date = pd.to_datetime(rebalance_results.iloc[0]["date"])
    seed_period_returns = asset_returns.loc[BACKTEST_START_DATE:first_rebalance_date]
    
    initial_universe = rebalance_results.iloc[0]["universe"]
    ew_seed_weights = pd.Series(1.0 / len(initial_universe), index=initial_universe)
    
    seed_returns = (seed_period_returns[initial_universe] * ew_seed_weights).sum(axis=1)
    seed_returns = seed_returns.loc[seed_returns.index < first_rebalance_date]
    logging.info(f"Generated {len(seed_returns)} days of seed returns.")

    # 2. Combine seed returns with the cost-adjusted backtest returns
    logging.info("Combining seed returns with main backtest returns...")
    logging.info(f"Seed returns shape: {seed_returns.shape}, Index: {seed_returns.index.min()} to {seed_returns.index.max()}")
    logging.info(f"Portfolio returns shape: {portfolio_returns.shape}, Index: {portfolio_returns.index.min()} to {portfolio_returns.index.max()}")
    full_period_returns = pd.concat([seed_returns, portfolio_returns])
    full_period_returns.name = "Baseline_CVaR"
    logging.info(f"Full period returns generated. Shape: {full_period_returns.shape}, Index: {full_period_returns.index.min()} to {full_period_returns.index.max()}")

    # 4. Create a corresponding daily weights dataframe for the full period
    logging.info("Generating full period weights...")
    seed_weights_df = pd.DataFrame(0, index=seed_returns.index, columns=UNIVERSE_TICKERS)
    if not seed_weights_df.empty:
        seed_weights_df[initial_universe] = ew_seed_weights
        seed_weights_df = seed_weights_df.fillna(0)

    full_period_weights = pd.concat([seed_weights_df, daily_weights])
    full_period_weights = full_period_weights.loc[~full_period_weights.index.duplicated(keep='first')]
    full_period_weights = full_period_weights.reindex(full_period_returns.index, method='ffill').fillna(0)
    logging.info(f"Full period weights generated. Shape: {full_period_weights.shape}, Index: {full_period_weights.index.min()} to {full_period_weights.index.max()}")

    # 3. Generate Cumulative Index
    logging.info("Generating cumulative index...")
    index_level = (1 + full_period_returns.fillna(0)).cumprod() * 100
    index_level.iloc[0] = 100
    logging.info("Cumulative index generated.")

    # --- Save all results ---
    logging.info("Saving all backtest artifacts...")
    results_path = Path("results")
    results_path.mkdir(exist_ok=True)

    full_period_returns.to_csv(results_path / "baseline_daily_returns.csv", header=True)
    logging.info(f"Saved full period returns to {results_path / 'baseline_daily_returns.csv'}")

    index_level.to_csv(results_path / "baseline_cvar_index.csv", header=True)
    logging.info(f"Saved cumulative index to {results_path / 'baseline_cvar_index.csv'}")

    rebalance_df = pd.DataFrame(rebalance_results).set_index("date")

    # --- Calculate Quarterly-Rebalanced Equal-Weighted Benchmark (Net of Costs) ---
    logging.info("Calculating quarterly-rebalanced equal-weighted benchmark (net of costs)...")
    TRANSACTION_COST_BPS = 10  # Standard 10 bps transaction cost

    rebalance_dates = rebalance_df.index
    all_benchmark_weights = []

    # Manually create weights for the initial seed period (2010 to first rebalance)
    if not rebalance_dates.empty:
        first_rebalance_date_ew = rebalance_dates[0]
        initial_universe_ew = rebalance_df.loc[first_rebalance_date_ew, "universe"]
        num_assets_initial = len(initial_universe_ew)

        if num_assets_initial > 0:
            ew_seed_weights_val = pd.Series(1.0 / num_assets_initial, index=initial_universe_ew)
            seed_period_dates = asset_returns.loc[START_DATE:first_rebalance_date_ew].index
            # Exclude the rebalance date itself from the seed period
            seed_period_dates = seed_period_dates[seed_period_dates < first_rebalance_date_ew]

            if not seed_period_dates.empty:
                seed_weights_df = pd.DataFrame(index=seed_period_dates, columns=UNIVERSE_TICKERS).fillna(0)
                seed_weights_df[initial_universe_ew] = ew_seed_weights_val
                all_benchmark_weights.append(seed_weights_df)
                logging.info(f"Created seed weights for Equal-Weighted benchmark for {len(seed_period_dates)} days.")

    for i in range(len(rebalance_dates)):
        start_period = rebalance_dates[i]
        end_period = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else END_DATE
        current_universe = rebalance_df.loc[start_period, "universe"]
        num_assets = len(current_universe)
        if num_assets == 0:
            continue

        weights = pd.Series(1.0 / num_assets, index=current_universe)
        period_dates = asset_returns.loc[start_period:end_period].index
        period_weights = pd.DataFrame(index=period_dates, columns=UNIVERSE_TICKERS).fillna(0)
        period_weights[current_universe] = weights
        all_benchmark_weights.append(period_weights)

    if not all_benchmark_weights:
        logging.warning("No benchmark weights were generated. Skipping benchmark calculation.")
        ew_daily_weights = pd.DataFrame()
        net_ew_daily_returns = pd.Series()
    else:
        ew_daily_weights = pd.concat(all_benchmark_weights)
        ew_daily_weights = ew_daily_weights.loc[~ew_daily_weights.index.duplicated(keep='first')]
        ew_daily_weights = ew_daily_weights.reindex(asset_returns.index, method='ffill').fillna(0)
        ew_daily_weights = ew_daily_weights.loc[START_DATE:END_DATE]

        # Calculate gross daily returns for the benchmark
        gross_ew_daily_returns = (ew_daily_weights.shift(1) * asset_returns).sum(axis=1)

        # --- Calculate and Apply Transaction Costs from Rebalancing (Quarterly) ---
        net_ew_daily_returns = gross_ew_daily_returns.copy()
        logging.info("Applying quarterly transaction costs to Equal-Weighted benchmark...")

        for reb_date in rebalance_dates:
            # Find the day before the rebalance date
            prev_day_loc = ew_daily_weights.index.get_loc(reb_date) - 1
            if prev_day_loc < 0:
                continue

            prev_day_weights = ew_daily_weights.iloc[prev_day_loc]
            prev_day_returns = asset_returns.iloc[prev_day_loc]

            # Calculate drifted weights
            drifted_weights = prev_day_weights * (1 + prev_day_returns)
            drifted_weights /= drifted_weights.sum()

            # Calculate trade size and cost
            trade = (ew_daily_weights.loc[reb_date] - drifted_weights).abs().sum()
            cost = trade * (TRANSACTION_COST_BPS / 10000)
            net_ew_daily_returns.loc[reb_date] -= cost
            # logging.info(f"Applied cost of {cost:.4f} to EW benchmark on {reb_date.date()}")

        net_ew_daily_returns = net_ew_daily_returns.loc[START_DATE:END_DATE]
        logging.info("Finished applying quarterly transaction costs to benchmark.")

    # Ensure benchmark returns are aligned with portfolio returns for metric calculation
    aligned_benchmark = benchmark_returns.reindex(portfolio_returns.index).ffill()
    raw_metrics = calculate_raw_metrics(portfolio_returns, aligned_benchmark, daily_weights=daily_weights)
    display_metrics = format_metrics_for_display(raw_metrics, portfolio_returns)

    # --- Save Results ---
    try:
        results_path = Path("results")
        results_path.mkdir(exist_ok=True)

        # Save rebalance weights
        weights_path = results_path / "baseline_cvar_rebalance_weights_2010-2024.csv"
        logging.info(f"Attempting to save rebalance weights to {weights_path}...")
        rebalance_results_to_save = rebalance_results.copy()
        if "weights" in rebalance_results_to_save.columns:
            # Convert numpy arrays to a more CSV-friendly string format
            rebalance_results_to_save["weights"] = rebalance_results_to_save["weights"].apply(
                lambda w: ",".join(map(str, np.round(w, 8))) if isinstance(w, np.ndarray) else w
            )
        rebalance_results_to_save.to_csv(weights_path)

        # Save Equal-Weighted benchmark results
        ew_weights_path = results_path / "equal_weighted_daily_weights.csv"
        ew_returns_path = results_path / "equal_weighted_daily_returns.csv"
        ew_daily_weights.to_csv(ew_weights_path)
        net_ew_daily_returns.to_csv(ew_returns_path)
        logging.info("Successfully saved Equal-Weighted benchmark weights and returns.")

        # Save daily weights for turnover calculation
        daily_weights_path = results_path / "baseline_daily_weights.csv"
        if not full_period_weights.empty:
            logging.info(f"Daily weights DataFrame has shape {full_period_weights.shape}. Saving to {daily_weights_path}...")
            full_period_weights.to_csv(daily_weights_path)
            logging.info(f"Successfully saved daily weights to {daily_weights_path}")
        else:
            logging.error("Daily weights DataFrame is empty. Cannot save to file.")
            raise ValueError("Failed to generate daily weights, cannot proceed.")
        logging.info("Successfully saved rebalance weights.")

        # Save performance metrics
        metrics_path = results_path / "baseline_cvar_performance_metrics.csv"
        logging.info(f"Attempting to save metrics to {metrics_path}...")
        raw_metrics.to_csv(metrics_path, header=True)
        logging.info("Successfully saved metrics.")

        # Save daily returns for the full 2010-2024 period
        returns_path = results_path / "baseline_daily_returns.csv"
        logging.info(f"Attempting to save daily returns to {returns_path}...")

        # Align all series to the full backtest period for a comprehensive comparison file
        common_index = full_period_returns.index

        # Align SPY benchmark
        aligned_benchmark = benchmark_returns.reindex(common_index).ffill()

        # Align Equal Weighted returns
        equal_weight_returns = asset_returns.mean(axis=1).reindex(common_index).ffill()

        # Align Cap-Weighted returns
        aligned_market_caps = market_cap_data.reindex(common_index).ffill()
        common_columns = asset_returns.columns.intersection(aligned_market_caps.columns)
        aligned_asset_returns_final = asset_returns[common_columns].reindex(common_index).ffill()
        aligned_market_caps_final = aligned_market_caps[common_columns]
        daily_market_cap_sum = aligned_market_caps_final.sum(axis=1)
        daily_market_cap_sum.replace(0, np.nan, inplace=True)
        cap_weights = aligned_market_caps_final.div(daily_market_cap_sum, axis=0)
        cap_weight_returns = (aligned_asset_returns_final * cap_weights).sum(axis=1)

        all_returns = pd.DataFrame(
            {
                "Baseline_CVaR": full_period_returns,
                "SPY": aligned_benchmark,
                "Equal_Weighted": equal_weight_returns,
                "Cap_Weighted": cap_weight_returns,
            }
        )
        all_returns.fillna(0, inplace=True)  # Fill any remaining NaNs with 0
        all_returns.to_csv(returns_path)
        logging.info("Successfully saved daily returns.")

        logging.info(f"Results saved to {results_path.resolve()}")

    except Exception as e:
        logging.error(f"CRITICAL: Failed to save results to disk: {e}")

    logging.info("--- Full Backtest Script Finished ---")
    print("\n--- Baseline Performance Metrics (2010-2024) ---")
    print(display_metrics)


if __name__ == "__main__":
    asyncio.run(main())
