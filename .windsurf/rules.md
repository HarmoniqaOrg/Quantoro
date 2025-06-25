
# Quantoro • Windsurf Development Rules

## Project References
- **Assignment Requirements**: Always refer to `D:\Quantoro\docs\Alpha Pods-Home Assignment.md` for assignement task specifications
- **CLEIR Paper**: Consult `D:\Quantoro\docs\CVAR index replication.md` for methodology details
- **Progress Tracking**: Update `docs/PRD.md` and `docs/tasks.md` after each work session

## Working Principles

### 1. **Work in Small, Verifiable Chunks**
- Implement ONE function/class at a time
- Test immediately after implementation
- Commit after each successful addition
- Maximum 200 lines of code per iteration
- Always verify outputs before proceeding

### 2. **Documentation First**
- Update `docs/PRD.md` with design decisions BEFORE implementing
- Keep `docs/tasks.md` current with:
  - [ ] Pending tasks
  - [x] Completed tasks
  - [!] Blocked/issues
  - [@] In progress
- Add inline comments explaining "why" not just "what"

### 3. **Continuous Validation**
- After each implementation:
  1. Run unit tests
  2. Check output sanity
  3. Verify constraints (weights sum to 1, etc.)
  4. Update progress documentation
  5. Commit with descriptive message

## Core Development Standards

### 1. **Python Environment & Code Quality**
- **Python 3.9+** (compatible with Google Colab)
- **Code formatting**: `black . --line-length 100`
- **Type hints**: All functions must have type annotations
- **Docstrings**: Google-style for all classes and functions
- **Linting**: `flake8 --max-line-length 100 --extend-ignore E203,W503`

### 2. **Project Structure**
```
quantoro/
├── .windsurf/
│   └── rules.md
├── docs/
│   ├── CVAR index replication.md
│   ├── Alpha Pods-Home Assignment.md
│   ├── PRD.md
│   └── tasks.md
├── README.md
├── requirements.txt
├── environment.yml
├── .env.example
├── notebook.ipynb          # Main Jupyter notebook
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py       # Data fetching (yfinance, FMP)
│   │   └── processor.py    # Data preprocessing
│   ├── optimization/
│   │   ├── __init__.py
│   │   ├── cvar_base.py    # Task A: Baseline CVaR
│   │   └── lasso.py        # LASSO implementation
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── transformer.py  # Transformer tail risk
│   │   ├── regime.py       # Regime detection
│   │   └── ensemble.py     # Model ensemble
│   ├── alpha/
│   │   ├── __init__.py
│   │   ├── fmp_signals.py  # Task C: FMP premium signals
│   │   └── microstructure.py
│   ├── backtesting/
│   │   ├── __init__.py
│   │   ├── engine.py       # Backtesting framework
│   │   └── metrics.py      # Performance metrics
│   └── utils/
│       ├── __init__.py
│       └── visualization.py
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── results/
│   ├── baseline_cvar_index.csv
│   ├── enhanced_cvar_index.csv
│   └── performance_metrics.csv
└── report.pdf
```

### 3. **API Keys & Secrets Management**
- **Never commit secrets**: Use `.env` file (add to `.gitignore`)
- **Required keys**:
  ```
  FMP_API_KEY=your_key_here
  OPENAI_API_KEY=your_key_here  # If using GPT for analysis
  ```
- **Load with python-dotenv**:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  api_key = os.getenv('FMP_API_KEY')
  ```

### 4. **Data Management**
- **Cache API responses**: Save to `data/cache/` to avoid rate limits
- **Version data**: `data/raw/{ticker}_{date}.csv`
- **Validate data**: Check for NaN, outliers before processing

### 5. **Financial Computation Standards**
- **Returns calculation**: Always use log returns for statistical properties
- **Frequency conversion**: 
  - Annual return = daily_return * 252
  - Annual vol = daily_vol * sqrt(252)
- **Transaction costs**: Apply symmetrically (buy & sell)
- **Numerical precision**: Use `np.float64` for portfolio weights

### 6. **Testing Requirements**
- **Unit tests required** for:
  - CVaR calculation
  - Portfolio constraints (sum to 1, bounds)
  - Transaction cost application
- **Backtesting validation**:
  - No look-ahead bias
  - Proper alignment of dates
  - Realistic rebalancing

### 7. **Performance Optimization**
- **Vectorize operations**: Use NumPy/Pandas operations over loops
- **Async for API calls**: Use `aiohttp` for parallel data fetching
- **Memory efficiency**: Process data in chunks for large universes

### 8. **Documentation Standards**
- **Each module**: Module-level docstring explaining purpose
- **Complex algorithms**: Include mathematical formulation in docstring
- **Example usage**: Include in docstrings
- **README sections**:
  - Quick Start
  - Installation
  - API Keys Setup
  - Running the Analysis
  - Results Interpretation

### 9. **Git Workflow**
- **Branch naming**: `feature/task-a-baseline`, `feature/task-b-ml`, `feature/task-c-alpha`
- **Commit messages**: `feat: implement CVaR optimization`, `fix: handle missing data`
- **PR checklist**:
  - [ ] Tests pass
  - [ ] Code formatted with black
  - [ ] Type hints added
  - [ ] Docstrings complete
  - [ ] Results reproducible

### 10. **Reproducibility**
- **Random seeds**: Set for all random operations
  ```python
  np.random.seed(42)
  random.seed(42)
  torch.manual_seed(42)
  ```
- **Data snapshot**: Save exact data used for final results
- **Environment**: Freeze exact package versions

### 11. **Output Standards**
- **CSV files**: Include headers, use ISO date format
- **Plots**: High DPI (300), professional styling
- **Report**: LaTeX or Markdown → PDF, max 5 pages
- **Performance metrics**: Include confidence intervals

### 12. **Error Handling**
- **API failures**: Implement exponential backoff
- **Data issues**: Log and report data quality problems
- **Optimization errors**: Catch and log solver failures

### 13. **Communication**
- **Daily stand-up**: Post progress in team channel
- **Weekly report**: Summarize progress and next steps
- **PR descriptions**: Clearly explain changes and rationale
