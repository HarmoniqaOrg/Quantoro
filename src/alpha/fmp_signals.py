import os
import pandas as pd
import aiohttp
import asyncio
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FmpPremiumSignals:
    """
    Fetches and processes premium alpha signals from the FMP API.
    This includes signals like insider trading, institutional ownership, and analyst ratings.
    """
    BASE_URL = "https://financialmodelingprep.com/api"

    def __init__(self, api_key: str):
        """
        Initializes the FmpPremiumSignals client.

        Args:
            api_key (str): Your Financial Modeling Prep API key.
        """
        if not api_key:
            raise ValueError("FMP API key is required.")
        self.api_key = api_key

    async def _fetch_signal(self, session: aiohttp.ClientSession, endpoint: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Asynchronously fetches data for a single endpoint.
        """
        if params is None:
            params = {}
        url = f"{self.BASE_URL}/{endpoint}"
        params['apikey'] = self.api_key
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                if not data:
                    logging.warning(f"No data returned from {endpoint} with params {params}")
                    return []
                return data
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching {url}: {e}")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred for {url}: {e}")
            return []

    async def get_analyst_recommendations(self, session: aiohttp.ClientSession, ticker: str, limit: int = 5) -> pd.DataFrame:
        """Fetches analyst recommendations for a ticker."""
        endpoint = f"v3/analyst-stock-recommendations/{ticker}"
        params = {'limit': limit}
        data = await self._fetch_signal(session, endpoint, params)
        return pd.DataFrame(data)

    async def get_insider_transactions(self, session: aiohttp.ClientSession, ticker: str, limit: int = 100) -> pd.DataFrame:
        """Fetches insider transactions for a ticker."""
        endpoint = "v4/insider-trading"
        params = {'symbol': ticker, 'limit': limit}
        data = await self._fetch_signal(session, endpoint, params)
        return pd.DataFrame(data)

    async def get_institutional_ownership(self, session: aiohttp.ClientSession, ticker: str) -> pd.DataFrame:
        """Fetches institutional ownership for a ticker."""
        endpoint = f"v3/institutional-holder/{ticker}"
        data = await self._fetch_signal(session, endpoint)
        return pd.DataFrame(data)

    async def get_all_signals_for_ticker(self, session: aiohttp.ClientSession, ticker: str) -> Dict[str, pd.DataFrame]:
        """Fetches all defined signals for a single ticker."""
        logging.info(f"Fetching all premium signals for {ticker}...")
        tasks = {
            "analyst_recs": self.get_analyst_recommendations(session, ticker),
            "insider_trades": self.get_insider_transactions(session, ticker),
            "institutional_holders": self.get_institutional_ownership(session, ticker),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        processed_results = {}
        for name, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                logging.error(f"Failed to fetch {name} for {ticker}: {result}")
                processed_results[name] = pd.DataFrame() # Return empty dataframe on error
            else:
                processed_results[name] = result
        return processed_results

    async def get_all_signals_for_universe(self, tickers: List[str], concurrency_limit: int = 5) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Fetches all signals for a universe of tickers with controlled concurrency to avoid rate limiting.
        
        Args:
            tickers (List[str]): The list of stock tickers.
            concurrency_limit (int): The maximum number of concurrent API requests.

        Returns:
            Dict[str, Dict[str, pd.DataFrame]]: A nested dictionary where the outer key is the ticker
                                               and the inner key is the signal type.
        """
        all_signals = {}
        semaphore = asyncio.Semaphore(concurrency_limit)

        async def fetch_with_semaphore(session, ticker):
            """Wrapper to control concurrency for each ticker's signal fetching."""
            async with semaphore:
                return await self.get_all_signals_for_ticker(session, ticker)

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_with_semaphore(session, ticker) for ticker in tickers]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for ticker, signal_data in zip(tickers, results):
                if isinstance(signal_data, Exception):
                    logging.error(f"Failed to fetch all signals for {ticker}: {signal_data}")
                    all_signals[ticker] = {}  # Ensure failed tickers have an entry
                else:
                    all_signals[ticker] = signal_data
                    
        logging.info("Successfully fetched all premium signals for the universe.")
        return all_signals
