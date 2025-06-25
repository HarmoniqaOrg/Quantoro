import pandas as pd
import numpy as np
from typing import Optional

class DataProcessor:
    """
    A class for processing financial time series data.
    """

    def __init__(self):
        pass

    def calculate_returns(self, prices: pd.DataFrame, log_returns: bool = True) -> Optional[pd.DataFrame]:
        """
        Calculates returns from a DataFrame of prices.

        Args:
            prices (pd.DataFrame): DataFrame where each column is a ticker and rows are dates.
            log_returns (bool): If True, calculates log returns. Otherwise, calculates simple returns.

        Returns:
            Optional[pd.DataFrame]: A DataFrame of returns, or None if input is invalid.
        """
        if not isinstance(prices, pd.DataFrame) or prices.empty:
            print("Input prices must be a non-empty pandas DataFrame.")
            return None

        if log_returns:
            returns = np.log(prices / prices.shift(1))
        else:
            returns = prices.pct_change()
            
        # Drop the first row of NaNs
        return returns.dropna()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs basic data cleaning.
        - Forward-fills missing values.
        - Drops any remaining NaNs (e.g., at the beginning).

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        df_cleaned = df.ffill()
        df_cleaned = df_cleaned.dropna()
        return df_cleaned


# Example usage:
if __name__ == '__main__':
    # Create a sample price DataFrame
    dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=10))
    prices_data = {
        'AAPL': [150, 152, 151, 153, 155, 154, 156, 157, 158, 160],
        'MSFT': [300, 301, 303, np.nan, 305, 306, 304, 307, 309, 308]
    }
    prices = pd.DataFrame(prices_data, index=dates)
    print("Original Prices:")
    print(prices)
    
    processor = DataProcessor()
    
    # Clean data
    cleaned_prices = processor.clean_data(prices)
    print("\nCleaned Prices (forward-filled):")
    print(cleaned_prices)

    # Calculate log returns
    log_returns = processor.calculate_returns(cleaned_prices, log_returns=True)
    print("\nLog Returns:")
    print(log_returns.head())
    
    # Calculate simple returns
    simple_returns = processor.calculate_returns(cleaned_prices, log_returns=False)
    print("\nSimple Returns:")
    print(simple_returns.head())
