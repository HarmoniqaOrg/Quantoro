"""Tests for CVaR optimizer."""

import pytest
import numpy as np
import pandas as pd
from src.optimization.cvar_optimizer import CVaROptimizer


def test_cvar_optimizer_initialization():
    """Test CVaR optimizer initialization."""
    optimizer = CVaROptimizer(alpha=0.95, lasso_penalty=1.5)
    assert optimizer.alpha == 0.95
    assert optimizer.lasso_penalty == 1.5
    assert optimizer.max_weight == 0.05


def test_optimization_with_simple_data():
    """Test optimization with simple returns data."""
    # Create synthetic returns data
    np.random.seed(42)
    n_days = 252
    n_assets = 25  # Increased to 25 to make the 5% max_weight constraint feasible
    returns = pd.DataFrame(
        np.random.randn(n_days, n_assets) * 0.01,
        columns=[f'Asset_{i}' for i in range(n_assets)]
    )

    # Initialize optimizer with default constraints (max_weight=0.05)
    optimizer = CVaROptimizer(alpha=0.95)

    # Run optimization
    result = optimizer.optimize(returns)

    # Check results
    assert result.status in ["optimal", "optimal_inaccurate"], f"Optimization failed with status: {result.status}"
    assert result.weights is not None
    assert not np.isnan(result.weights).any(), "Weights should not be NaN"
    assert len(result.weights) == n_assets
    assert np.isclose(np.sum(result.weights), 1.0), "Weights should sum to 1"
    assert np.all(result.weights >= -1e-6), "No shorting allowed"
    assert np.all(result.weights <= optimizer.max_weight + 1e-6), "Weights must be below max_weight"


def test_portfolio_metrics():
    """Test portfolio metrics calculation."""
    # Create simple returns
    returns = pd.DataFrame({
        'Asset1': [0.01, -0.02, 0.03, -0.01, 0.02],
        'Asset2': [0.02, 0.01, -0.01, 0.02, -0.01]
    })
    weights = np.array([0.6, 0.4])
    
    optimizer = CVaROptimizer()
    metrics = optimizer.calculate_portfolio_metrics(returns, weights)
    
    assert 'annual_return' in metrics
    assert 'annual_volatility' in metrics
    assert 'sharpe_ratio' in metrics
    assert 'max_drawdown' in metrics
