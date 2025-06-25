# Product Requirements Document - Quantoro

## Project Overview
Implementation of CVaR-LASSO Enhanced Index Replication (CLEIR) with ML enhancements for eToro Alpha Pods assignment.

## Current Sprint: Project Setup
- **Objective**: Initialize project structure and development environment
- **Success Criteria**: All files created, dependencies installed, initial commit pushed
- **Design Decisions**: 
  - Using CVXPy for optimization (proven CVaR support)
  - PyTorch for ML models (better transformer support)
  - Async architecture for data fetching (FMP rate limits)

## Architecture Decisions Log
- **2024-01-XX**: Selected 60 most liquid S&P 100 stocks to balance diversification and liquidity
- **2024-01-XX**: Chose quarterly rebalancing to minimize transaction costs while maintaining responsiveness

## Technical Specifications
- **CVaR Confidence Level**: 95% (α = 0.95)
- **Max Position Size**: 5%
- **Transaction Costs**: 10 bps per side
- **Rebalancing**: Quarterly
- **Lookback Window**: 252 trading days
