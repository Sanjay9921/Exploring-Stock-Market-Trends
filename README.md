# Exploring Stock Market (Plotly + Flask)

## Overview

This project ingests historical ``OHLCV`` (Open, High, Low, Close, Volume) data for a curated universe of **highly liquid, exchange‑listed equities** (e.g., ``AAPL``, ``AMZN``, ``GOOGL``, ``META``, ``MSFT``), standardizes it into a tidy time‑series dataset, and exposes it through a Flask‑based ``REST API``. On top of the raw data API, the app now computes several **portfolio allocations (equal‑weight, minimum‑volatility, and maximum‑Sharpe)** using mean‑variance optimization techniques, and visualizes both single‑asset history and multi‑asset weights in a simple web UI.

## Project Structure

```text
exploring-stock/
├─ app.py                      # Flask entry point (APIs + UI)
├─ modules/
│  ├─ __init__.py
│  ├─ settings/
│  │   ├─ __init__.py
│  │   └─ config.py            # global config: dates, tickers, data dir
│  └─ data/
│      ├─ helper.py            # yfinance download + tidy dataframe utilities
│      ├─ create_dataset.py    # CLI script to build datasets/companies.csv
│      └─ portfolio_opt.py     # portfolio analytics with PyPortfolioOpt
├─ datasets/
│  └─ companies.csv            # generated OHLCV data for all tickers
├─ templates/
│  └─ index.html               # Plotly + portfolio allocations front-end
├─ venv/                       # virtual environment (local)
└─ requirements.txt            # Python dependencies
```

## Features

* Downloads historical ``OHLCV`` data for a configurable universe of tickers via ``yfinance``, and stores a unified ``companies.csv`` under ``datasets/``.​
* Normalizes column names and concatenates all tickers row‑wise into a single tidy DataFrame, with one row per ticker‑date.
* Builds a wide “prices × tickers” matrix from ``companies.csv`` and computes:
    * A 1/n equal‑weight benchmark portfolio.
    * A minimum‑volatility portfolio via ``EfficientFrontier.min_volatility``.
    * A maximum‑Sharpe portfolio via ``EfficientFrontier.max_sharpe``.​
* Exposes REST endpoints:
    * ``GET /api/tickers`` – list of available tickers.
    * ``GET /api/metrics`` – list of numeric metrics (``open``, ``high``, ``low``, ``close``, ``adj_close``, ``volume``).
    * ``GET /api/history`` – raw time series for a ticker (optional ``start/end`` filters).
    * ``GET /api/figure`` – Plotly figure spec (JSON) for a ticker + metric time series.
    * ``GET /api/allocations`` – JSON payload with weights and metrics for:
        * equal‑weight benchmark,
        * min‑volatility portfolio,
        * max‑Sharpe portfolio.​
* Simple HTML front‑end (``templates/index.html``) that:
    * Loads tickers and metrics from the API.
    * Renders an interactive Plotly time‑series chart for any ticker/metric pair.
    * Displays three portfolio allocation panels side‑by‑side, showing asset weights and key risk/return statistics.

## Setup

1. Clone the repository and move into the project folder:

```bash
git clone <your-repo-url> exploring-stock
cd exploring-stock
```

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate   # on Windows
# source venv/bin/activate  # on macOS / Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Generate the dataset

* All data settings live in ``modules/settings/config.py``:
    * ``DATA_DIR``: location of the ``.csv`` dataset directory.
    * ``OUTPUT_FILE``: file name for the final ``.csv`` dataset.
    * ``DEFAULT_START_DATE``: common start date for all tickers.
    * ``DEFAULT_END_DATE``: common end date for all tickers.
    * ``DEFAULT_TICKERS``: default list of tickers to download.
* To (re)build ``datasets/companies.csv`` for the configured tickers and date range:

```bash
python -m modules.data.create_dataset
```

* This uses helper functions in ``modules/data/helper.py`` to download and concatenate data, then writes a single CSV under ``datasets/``.

5. Run the Flask app

* From the project root:

```bash
python app.py
```

* Flask starts in development mode on ``http://127.0.0.1:5000/``.
    * Open ``http://127.0.0.1:5000/`` in a browser.
    * Use the **Ticker dropdown** to switch between companies.
    * Use the **Metric dropdown** to switch between ``open``, ``high``, ``low``, ``close``, ``adj_close``, and ``volume``.
    * The Plotly chart updates via the ``/api/figure`` endpoint.
    * Inspect the **three portfolio cards** at the top of the page to see:
        * equal‑weight benchmark expected return and Sharpe ratio,
        * min‑volatility portfolio weights and volatility,
        * max‑Sharpe portfolio weights and Sharpe ratio
    * You can also call the APIs directly, for example:
        * ``http://127.0.0.1:5000/api/tickers``
        * ``http://127.0.0.1:5000/api/metrics``
        * ``http://127.0.0.1:5000/api/history?ticker=AAPL``
        * ``http://127.0.0.1:5000/api/figure?ticker=AAPL&metric=close``
        * ``http://127.0.0.1:5000/api/allocations``

## Development notes

* Core data loading and CSV generation logic is isolated in ``modules/data/helper.py`` and ``modules/data/create_dataset.py``, so it can be reused from other scripts or notebooks.
* Portfolio optimization logic is encapsulated in ``modules/data/portfolio_opt.py``, which computes returns, covariance, and optimized weights using PyPortfolioOpt’s ``EfficientFrontier`` APIs.​
* Configuration (tickers, date ranges, file paths) is centralized in ``modules/settings/config.py``, so changing a few constants is enough to regenerate the dataset and recompute all portfolio allocations.