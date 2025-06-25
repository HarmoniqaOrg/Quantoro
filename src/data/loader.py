import os
import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Optional
import logging

# Load environment variables from .env file
load_dotenv()

class FmpDataLoader:
    """
    A class to download historical stock data from Financial Modeling Prep (FMP).
    """

    def __init__(self, api_key: Optional[str] = None, cache_dir: str = "data/cache"):
        """
        Initializes the FmpDataLoader.

        Args:
            api_key (Optional[str]): The FMP API key. If None, it's read from the FMP_API_KEY env variable.
            cache_dir (str): The directory to store cached data.
        """
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError("FMP_API_KEY not found. Please set it in your .env file or pass it directly.")
        
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def get_historical_data(self, ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Fetches historical daily price data for a single ticker.

        Args:
            ticker (str): The stock ticker symbol.
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            Optional[pd.DataFrame]: A DataFrame with historical data, or None if an error occurs.
        """
        cache_file = self.cache_dir / f"{ticker}_{start_date}_{end_date}.csv"
        
        if cache_file.exists():
            logging.info(f"Loading {ticker} data from cache.")
            return pd.read_csv(cache_file, index_col='date', parse_dates=True)

        logging.info(f"Fetching {ticker} data from FMP API.")
        url = f"{self.base_url}/historical-price-full/{ticker}?from={start_date}&to={end_date}&apikey={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()  # Raise an exception for bad status codes
                    data = await response.json()
                    
                    if not data or 'historical' not in data:
                        logging.warning(f"No historical data found for {ticker}")
                        return None
                        
                    df = pd.DataFrame(data['historical'])
                    if df.empty:
                        return None
                        
                    df = df.rename(columns={'adjClose': 'adj_close'})
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.set_index('date')
                    df = df.sort_index()
                    
                    # Select only relevant columns
                    df = df[['open', 'high', 'low', 'close', 'adj_close', 'volume']]
                    
                    # Save to cache
                    df.to_csv(cache_file)
                    
                    return df
            except Exception as e:
                logging.error(f"An exception occurred while fetching data for {ticker}: {e}")
                return None

    async def get_multiple_tickers_data(self, tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches historical data for multiple tickers concurrently and handles exceptions gracefully.

        Args:
            tickers (List[str]): A list of stock ticker symbols.
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: A DataFrame containing the adjusted close prices for all tickers.
        """
        tasks = [self.get_historical_data(ticker, start_date, end_date) for ticker in tickers]
        # Use return_exceptions=True to prevent one failed request from stopping all others.
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_data = {}
        for ticker, res in zip(tickers, results):
            if isinstance(res, Exception):
                # Log the exception to understand why a ticker failed.
                logging.error(f"Failed to fetch data for {ticker}: {res}")
            elif res is not None and not res.empty:
                all_data[ticker] = res['adj_close']
        
        if not all_data:
            return pd.DataFrame()
            
        # Ensure consistent columns and handle potential all-NaN series
        combined_df = pd.concat(all_data, axis=1)
        return combined_df


# Example usage:
async def main():
    # Example: Fetch data for a few tickers
    loader = FmpDataLoader()
    tickers = ['AAPL', 'MSFT', 'GOOG']
    start = '2022-01-01'
    end = '2023-01-01'
    
    price_data = await loader.get_multiple_tickers_data(tickers, start, end)
    
    if not price_data.empty:
        print("Fetched data:")
        print(price_data.head())


if __name__ == '__main__':
    asyncio.run(main())
