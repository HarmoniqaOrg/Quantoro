**Alpha Pods – Take-Home Assignment** **Take-Home Assignment – 2025 Finalist Round** This assignment is designed to evaluate your technical, analytical, and creative skills in quantitative investing. It mirrors the way our internal Alpha Pods build strategies—starting from replicating something known, then pushing the boundaries of what’s possible. 

**Assignment Overview** 

**Stock Universe** 

60 liquid U.S. stocks from the S&P 100 \(freely available\) **Deadline** 

7 days from receipt of this brief \(by 23:59 UTC\) **Submission** 

Private GitHub repo \(we’ll send an invite\) or a zipped folder **Support** 

Reach out to alpha-recruit@etoro.com with any questions 

****

**Task A – Baseline CVaR Index \(Required\)** Rebuild the CVaR-based long-only index described in the attached paper. 

**Details: **

- Optimise for 95% daily CVaR


- Constraints: fully invested \(Σ weights = 1\), no shorting, max 5% per stock


- Rebalance quarterly 


- Apply transaction costs of 10 bps per side


- Use daily data from 1 Jan 2010 to 31 Dec 2024 

****





**What to Submit: **

• A CSV with daily index values 

• A table showing annual return, volatility, Sharpe, 95% CVaR, max drawdown, and turnover 

• A plot comparing your index to equal-weighted and cap-weighted benchmarks 

**Task B – Alpha Enhancement \(Required\)** Using any **ML, AI, or statistical method**, enhance the performance of your CVaR index. The goal is to improve risk-adjusted returns **out of sample**. 

You can build your own idea or choose from the examples below: **Idea Type **

**Examples **

Tail-risk modelling 

Quantile regression, EVT neural networks, LSTM for VaR 

Regime adaptation 

Classifiers that change constraints or weights based on macro regimes Alpha overlays 

Macro/factor/sentiment models that tilt exposures Rebalancing logic 

Reinforcement learning agents that trigger rebalance decisions **Requirements:** 

1. Use only publicly available data 2. Train using proper walk-forward methods \(no lookahead\) 3. Test window must cover **Jan 2020 – Dec 2024 ** 

4. Explain your model and provide basic interpretability \(e.g. feature importance, SHAP, etc.\)Include a method note \(≤400 words\) explaining the idea and results** ** 





**Task C – Alpha in the Wild \(Optional | \+20 pts\)** This extra-credit task is for those who want to go further. 

Use any non-traditional data source—like Google Trends, Reddit, news flow, blockchain data, or microstructure signals—and show how it adds alpha to your strategy. 

The goal is simple: find an edge that others might overlook, and prove its value. 

**Submission Package** 

Your repo or zip should include: 

● README.md – instructions to run everything 

● notebook.ipynb or scripts – clean and well-documented 

● report.pdf – max 5 pages with your methodology, results, and reflections 

● environment.yml or requirements.txt 

● results/ – CSV files with your daily index and enhancements



