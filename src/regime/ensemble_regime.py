"""
Ensemble regime detection combining SMA and MRS-GARCH approaches
Implements findings from multiple papers for robust regime detection
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional
from .regime import SMARegimeDetector  # Original SMA detector
from .volatility_detector import VolatilityThresholdDetector



class EnsembleRegimeDetector:
    """
    Combines multiple regime detection methods for robustness
    Based on findings that ensemble approaches outperform single models
    """
    
    def __init__(self, 
                 short_window: int = 50, 
                 long_window: int = 200, 
                 sma_weight: float = 0.7, 
                 mrs_weight: float = 0.3):
        """
        Initialize ensemble with weights favoring proven SMA approach
        
        Args:
            short_window: Short window for SMA detector.
            long_window: Long window for SMA detector.
            sma_weight: Weight for SMA crossover (default 0.7)
            mrs_weight: Weight for MRS-GARCH (default 0.3)
        """
        self.sma_detector = SMARegimeDetector(short_window=short_window, long_window=long_window)
        self.mrs_detector = VolatilityThresholdDetector()
        self.sma_weight = sma_weight
        self.mrs_weight = mrs_weight
        
        # Ensure weights sum to 1
        total_weight = sma_weight + mrs_weight
        self.sma_weight /= total_weight
        self.mrs_weight /= total_weight
        

    
    def detect_regime(self, spy_prices: pd.Series) -> pd.DataFrame:
        """
        Detect market regime using ensemble of methods
        
        Returns:
            pd.DataFrame: Regime probabilities (0=risk-off, 1=risk-on)
        """
        # Get SMA regime (binary 0/1)
        sma_regime = self.sma_detector.detect_regime(spy_prices)
        # Get MRS-GARCH regime (continuous 0-1)
        # Fit on SPY returns for consistency
        spy_returns = spy_prices.pct_change().dropna()
        mrs_regime = self.mrs_detector.fit_predict(spy_returns)
            
        # Align indices
        common_idx = sma_regime.index.intersection(mrs_regime.index)
        sma_aligned = sma_regime.loc[common_idx]
        mrs_aligned = mrs_regime.loc[common_idx]
        
        # Weighted ensemble
        ensemble_regime = (self.sma_weight * sma_aligned + 
                          self.mrs_weight * mrs_aligned)
        

        
        # Create a standardized DataFrame for output
        output_df = pd.DataFrame({
            'risk_on_probability': ensemble_regime,
            'risk_off_probability': 1 - ensemble_regime
        })
        
        return output_df
