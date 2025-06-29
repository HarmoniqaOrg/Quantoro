import os
import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Optional, Dict
import logging
from tqdm.asyncio import tqdm as aio_tqdm
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()


class FmpDataLoader:
    """
    A class to download historical stock data and alternative signals from Financial Modeling Prep (FMP).
    """

    def __init__(self, api_key: Optional[str] = None, cache_dir: str = "data/cache"):
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FMP_API_KEY not found. Please set it in your .env file or pass it directly."
            )

        self.base_url = "https://financialmodelingprep.com/api"
        self.cache_dir = Path(cache_dir)
        self.signal_cache_dir = self.cache_dir / "signals"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.signal_cache_dir.mkdir(parents=True, exist_ok=True)

    async def get_historical_data(
        self, ticker: str, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        cache_file = self.cache_dir / f"{ticker}_{start_date}_{end_date}.csv"
        if cache_file.exists():
            return pd.read_csv(cache_file, index_col="date", parse_dates=True)

        url = f"{self.base_url}/v3/historical-price-full/{ticker}?from={start_date}&to={end_date}&apikey={self.api_key}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if not data or "historical" not in data:
                        return None
                    df = pd.DataFrame(data["historical"]).rename(columns={"adjClose": "adj_close"})
                    df["date"] = pd.to_datetime(df["date"])
                    df = df.set_index("date").sort_index()
                    df = df[["open", "high", "low", "close", "adj_close", "volume"]]
                    df.to_csv(cache_file)
                    return df
            except Exception as e:
                logging.error(f"Exception for {ticker} historical data: {e}")
                return None

    async def get_multiple_tickers_data(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> pd.DataFrame:
        tasks = [self.get_historical_data(ticker, start_date, end_date) for ticker in tickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_data = {
            ticker: res["adj_close"]
            for ticker, res in zip(tickers, results)
            if isinstance(res, pd.DataFrame) and not res.empty
        }
        return pd.concat(all_data, axis=1) if all_data else pd.DataFrame()

    async def get_historical_market_cap(
        self, ticker: str, start_date: str, end_date: str
    ) -> Optional[pd.Series]:
        """Fetches historical market capitalization for a single ticker using the correct endpoint."""
        cache_file = self.cache_dir / f"{ticker}_market_cap_{start_date}_{end_date}.csv"
        if cache_file.exists():
            df = pd.read_csv(cache_file, index_col="date", parse_dates=True)
            return df["marketCap"]

        # Note: FMP's historical market cap endpoint has a 'limit' parameter, not date ranges.
        # We'll fetch a large limit and then filter by date. A limit of ~4000 covers ~15 years.
        url = f"{self.base_url}/v3/historical-market-capitalization/{ticker}?limit=4000&apikey={self.api_key}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if not data:
                        logging.warning(f"No market cap data returned for {ticker}.")
                        return None
                    df = pd.DataFrame(data)
                    df["date"] = pd.to_datetime(df["date"])
                    df = df.set_index("date").sort_index()
                    df = df[["marketCap"]]
                    df.to_csv(cache_file)
                    # Filter to the requested date range using type-safe integer-location slicing
                    start_idx = df.index.searchsorted(pd.to_datetime(start_date), side="left")
                    end_idx = df.index.searchsorted(pd.to_datetime(end_date), side="right")
                    filtered_df = df.iloc[start_idx:end_idx]
                    return filtered_df["marketCap"] if not filtered_df.empty else None
            except Exception as e:
                logging.error(f"Exception for {ticker} market cap data: {e}")
                return None

    async def get_multiple_tickers_market_cap(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetches market capitalization for multiple tickers over a date range."""
        tasks = [self.get_historical_market_cap(ticker, start_date, end_date) for ticker in tickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_caps = {
            ticker: res
            for ticker, res in zip(tickers, results)
            if isinstance(res, pd.Series) and not res.empty
        }
        return pd.concat(all_caps, axis=1) if all_caps else pd.DataFrame()

    async def _fetch_signal_data(
        self, endpoint: str, ticker: str, params: Optional[Dict] = None
    ) -> Optional[pd.DataFrame]:
        """Generic method to fetch and cache signal data."""
        cache_file = self.signal_cache_dir / f"{ticker}_{endpoint}.csv"
        if cache_file.exists():
            return pd.read_csv(cache_file)

        url = f"{self.base_url}/v3/{endpoint}/{ticker}"
        query_params = {"apikey": self.api_key, **(params or {})}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=query_params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if not data:
                        return None
                    df = pd.DataFrame(data)
                    df.to_csv(cache_file, index=False)
                    return df
            except Exception as e:
                logging.error(f"Exception for {ticker} at {endpoint}: {e}")
                return None

    async def get_analyst_recommendations(self, ticker: str) -> Optional[pd.DataFrame]:
        return await self._fetch_signal_data("analyst-stock-recommendations", ticker)

    async def get_insider_trades(self, ticker: str) -> Optional[pd.DataFrame]:
        return await self._fetch_signal_data("insider-trading", ticker, params={"limit": 200})

    async def fetch_all_signals_for_ticker(self, ticker: str) -> Dict[str, pd.DataFrame]:
        """Fetches all defined signals for a single ticker."""
        tasks = {
            "analyst_recs": self.get_analyst_recommendations(ticker),
            "insider_trades": self.get_insider_trades(ticker),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        ticker_signals = {}
        for (name, res) in zip(tasks.keys(), results):
            if isinstance(res, pd.DataFrame):
                ticker_signals[name] = res
        return ticker_signals

    def fetch_all_signals_for_universe_sync(
        self, tickers: List[str]
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Synchronous wrapper to fetch all signals for a list of tickers."""

        async def _fetch_all_async():
            tasks = [self.fetch_all_signals_for_ticker(ticker) for ticker in tickers]
            results = await aio_tqdm.gather(*tasks, desc="Fetching FMP signals")
            return {
                ticker: signal_data for ticker, signal_data in zip(tickers, results) if signal_data
            }

        return asyncio.run(_fetch_all_async())


class GoogleTrendsLoader:
    """
    A class to download and cache Google Trends data for a list of tickers.
    """

    def __init__(self, cache_dir: str = "data/cache/trends"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # pytrends must be imported here to avoid issues with its global setup
        from pytrends.request import TrendReq

        self.pytrends = TrendReq(hl="en-US", tz=360)

    def _fetch_trends_for_ticker(
        self, ticker: str, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """Fetches and caches Google Trends data for a single ticker."""
        cache_file = self.cache_dir / f"{ticker}_trends.csv"
        if cache_file.exists():
            df = pd.read_csv(cache_file, index_col="date", parse_dates=True)
            # Use type-safe integer-location slicing to avoid mypy errors
            start_idx = df.index.searchsorted(pd.to_datetime(start_date), side="left")
            end_idx = df.index.searchsorted(pd.to_datetime(end_date), side="right")
            return df.iloc[start_idx:end_idx]

        try:
            # Build payload for the specific ticker and timeframe
            self.pytrends.build_payload(
                [ticker], cat=0, timeframe=f"{start_date} {end_date}", geo="", gprop=""
            )
            df = self.pytrends.interest_over_time()

            if df.empty:
                logging.warning(f"No Google Trends data found for {ticker}.")
                return None

            df = df.rename(columns={ticker: "interest"})
            df.drop(columns=["isPartial"], inplace=True, errors="ignore")
            df.to_csv(cache_file)
            logging.info(f"Successfully fetched and cached Google Trends for {ticker}.")
            return df

        except Exception as e:
            # Pytrends can be flaky and throw various errors, including ResponseError 429
            logging.error(f"Failed to fetch Google Trends for {ticker}: {e}")
            # Sleep to avoid hammering the API if we are being rate-limited
            import time

            time.sleep(5)
            return None

    def get_trends_for_universe(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> Dict[str, pd.DataFrame]:
        """Fetches Google Trends data for a universe of tickers, with caching."""
        all_trends = {}
        for ticker in tqdm(tickers, desc="Fetching Google Trends"):
            trends_df = self._fetch_trends_for_ticker(ticker, start_date, end_date)
            if trends_df is not None and not trends_df.empty:
                all_trends[ticker] = trends_df
        return all_trends
