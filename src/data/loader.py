import os
import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Optional

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
            print(f"Loading {ticker} data from cache.")
            return pd.read_csv(cache_file, index_col='date', parse_dates=True)

        print(f"Fetching {ticker} data from FMP API.")
        url = f"{self.base_url}/historical-price-full/{ticker}?from={start_date}&to={end_date}&apikey={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()  # Raise an exception for bad status codes
                    data = await response.json()
                    
                    if not data or 'historical' not in data:
                        print(f"No historical data found for {ticker}")
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
            except aiohttp.ClientError as e:
                print(f"Error fetching data for {ticker}: {e}")
                return None

    async def get_multiple_tickers_data(self, tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches historical data for multiple tickers concurrently.

        Args:
            tickers (List[str]): A list of stock ticker symbols.
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: A DataFrame containing the adjusted close prices for all tickers.
        """
        tasks = [self.get_historical_data(ticker, start_date, end_date) for ticker in tickers]
        results = await asyncio.gather(*tasks)
        
        all_data = {}
        for ticker, df in zip(tickers, results):
            if df is not None and not df.empty:
                all_data[ticker] = df['adj_close']
        
        if not all_data:
            return pd.DataFrame()
            
        combined_df = pd.DataFrame(all_data)
        combined_df.sort_index(inplace=True)
        
        return combined_df

# Example usage:
async def main():
    # As per PRD, using 60 most liquid S&P 100 stocks
    # For this example, let's use a smaller list
    tickers = ['AAPL', 'MSFT', 'GOOG']
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    
    loader = FmpDataLoader()
    data = await loader.get_multiple_tickers_data(tickers, start_date, end_date)
    
    if not data.empty:
        print("Successfully fetched data:")
        print(data.head())
        print("\nData Info:")
        data.info()

if __name__ == '__main__':
    asyncio.run(main())
