# tests/test_cvar_optimizer.py

import pytest
import numpy as np
import pandas as pd
from src.optimization.cvar_optimizer import CVaROptimizer


@pytest.fixture
def sample_returns_data():
    """Creates a sample returns DataFrame for testing."""
    np.random.seed(42)
    dates = pd.date_range(start="2020-01-01", periods=100)
    assets = [f"Asset_{i}" for i in range(10)]
    data = np.random.randn(100, 10) / 100
    return pd.DataFrame(data, index=dates, columns=assets)


def test_cvar_optimizer_initialization():
    """Test CVaR optimizer initialization."""
    optimizer = CVaROptimizer(alpha=0.95, lasso_penalty=1.5, max_weight=0.2)
    assert optimizer.alpha == 0.95
    assert optimizer.lasso_penalty == 1.5
    assert optimizer.max_weight == 0.2


def test_optimization_constraints(sample_returns_data):
    """Test that optimization respects all weight constraints."""
    optimizer = CVaROptimizer(alpha=0.95, max_weight=0.25, solver="SCS")
    result = optimizer.optimize(sample_returns_data)

    assert result.status in ["optimal", "optimal_inaccurate"], f"Optimization failed: {result.status}"
    weights = result.weights
    assert weights is not None
    assert not np.isnan(weights).any(), "Weights should not contain NaN values."

    # 1. Test for fully invested constraint (sum of weights = 1)
    assert np.isclose(np.sum(weights), 1.0, atol=1e-4), "Weights must sum to 1."

    # 2. Test for long-only constraint (weights >= 0)
    assert np.all(weights >= -1e-5), "Weights must be non-negative (long-only)."

    # 3. Test for max weight constraint (weights <= max_weight)
    assert np.all(weights <= optimizer.max_weight + 1e-5), f"All weights must be <= max_weight ({optimizer.max_weight})."


def test_max_weight_constraint_is_active():
    """
    Test that the max_weight constraint is active and binding when it should be.
    We create a scenario with one asset having clearly superior returns, which would
    receive a high allocation if not for the constraint.
    """
    np.random.seed(42)
    n_days = 252
    n_assets = 5
    columns = [f"Asset_{i}" for i in range(n_assets)]
    returns = pd.DataFrame(np.random.randn(n_days, n_assets) * 0.02, columns=columns)
    # Make one asset clearly outperform to attract a higher weight
    returns["Asset_0"] += 0.005

    # Set a restrictive max_weight that is binding
    max_w = 0.25
    optimizer = CVaROptimizer(alpha=0.95, max_weight=max_w, solver="SCS")
    result = optimizer.optimize(returns)

    assert result.status in ["optimal", "optimal_inaccurate"], f"Optimization failed: {result.status}"
    weights = result.weights

    # Check that the constraint is respected
    assert np.all(weights <= max_w + 1e-5), f"Weights must be below max_weight ({max_w})."

    # Check that at least one weight is *close* to the max_weight, proving the constraint was active
    assert np.any(np.isclose(weights, max_w, atol=1e-4)), "At least one weight should be close to the max_weight, proving the constraint is active."
