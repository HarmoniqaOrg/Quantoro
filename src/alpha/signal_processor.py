import pandas as pd
import numpy as np
from typing import Dict

class SignalProcessor:
    """
    Processes raw FMP signals into a composite alpha score.
    """

    def __init__(self, signals_data: Dict[str, Dict[str, pd.DataFrame]]):
        """
        Initializes the SignalProcessor.

        Args:
            signals_data (Dict): The raw signal data from FmpPremiumSignals.
        """
        self.signals_data = signals_data

    def _score_analyst_recs(self, ticker_data: Dict[str, pd.DataFrame]) -> float:
        """Scores analyst recommendations. Placeholder logic."""
        # Simple placeholder: count 'buy' vs 'sell'
        recs = ticker_data.get('analyst_recs', pd.DataFrame())
        if recs.empty:
            return 0.0
        
        score_map = {
            'strong buy': 2,
            'buy': 1,
            'hold': 0,
            'sell': -1,
            'strong sell': -2
        }
        # Ensure column exists and is lowercase
        if 'rating' in recs.columns:
            recs['rating_lower'] = recs['rating'].str.lower()
            scores = recs['rating_lower'].map(score_map).mean()
            return scores if not np.isnan(scores) else 0.0
        return 0.0

    def _score_insider_trades(self, ticker_data: Dict[str, pd.DataFrame]) -> float:
        """Scores insider transactions. Placeholder logic."""
        # Simple placeholder: net transaction value
        trades = ticker_data.get('insider_trades', pd.DataFrame())
        if trades.empty or 'transactionType' not in trades.columns or 'securitiesTransacted' not in trades.columns or 'price' not in trades.columns:
            return 0.0

        # Calculate transaction value as it's not provided directly
        trades['transactionValue'] = trades['securitiesTransacted'] * trades['price']

        buys = trades[trades['transactionType'] == 'P-Purchase']['transactionValue'].sum()
        sells = trades[trades['transactionType'] == 'S-Sale']['transactionValue'].sum()
        
        # Normalize by total volume to get a score between -1 and 1
        total_volume = buys + sells
        if total_volume == 0:
            return 0.0
        return (buys - sells) / total_volume

    def generate_composite_alpha_scores(self) -> pd.DataFrame:
        """
        Generates a composite alpha score for each ticker in the universe.
        
        Returns:
            pd.DataFrame: A DataFrame with tickers as index and 'alpha_score' as a column.
        """
        alpha_scores = {}
        for ticker, data in self.signals_data.items():
            analyst_score = self._score_analyst_recs(data)
            insider_score = self._score_insider_trades(data)
            
            # Combine scores (equal weight for now)
            composite_score = (analyst_score * 0.5) + (insider_score * 0.5)
            alpha_scores[ticker] = composite_score
            
        return pd.DataFrame.from_dict(alpha_scores, orient='index', columns=['alpha_score'])
