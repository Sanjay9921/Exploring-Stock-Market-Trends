# Exploring Stock Market (Plotly + Flask)

## Overview

This project ingests historical ``OHLCV`` (Open, High, Low, Close, Volume) data for a curated universe of highly liquid, exchange‑listed equities such as Domino’s Pizza, standardizes it into a tidy time‑series dataset, and exposes it through a Flask‑based REST API. The resulting data and APIs are designed for downstream analytics tasks typical in front‑office and risk roles, including return and volatility analysis, event‑ and corporate‑action‑aware performance evaluation, and large‑scale data preparation pipelines in Python.

## Project Structure

```text
exploring-stock/
├─ app.py                 # Flask entry point (APIs + UI)
├─ codes/
│  ├─ __init__.py
│  ├─ config.py           # global config: dates, tickers, data dir
│  ├─ data_loader.py      # yfinance download + tidy dataframe utilities
│  └─ build_dataset.py    # CLI script to build datasets/companies.csv
├─ datasets/
│  └─ companies.csv       # generated OHLCV data for all tickers
├─ images/                # screenshots used in the README / notebook
├─ templates/
│  └─ index.html          # Plotly front-end rendered by Flask
├─ main.ipynb             # notebook for ad‑hoc analysis and plots
└─ requirements.txt       # Python dependencies
```

## Features

* Downloads historical OHLCV data for a configurable universe of tickers via yfinance.
* Normalizes column names and concatenates all tickers row‑wise into a single tidy DataFrame.
* Exposes REST endpoints:
    * ``GET /api/tickers`` – list of available tickers.
    * ``GET /api/metrics`` – list of numeric metrics (open, high, low, close, adj_close, volume).
    * ``GET /api/history`` – raw time series for a ticker (optional date filters).
    * ``GET /api/figure`` – Plotly figure spec (JSON) for a ticker + metric.
* Simple HTML front‑end (``index.html``) that:
    * Loads tickers and metrics from the API.
    * Renders an interactive time‑series chart with Plotly.
    * Lets you switch ticker and metric from dropdowns.

## Setup

1. Clone the repository and move into the project folder:

```bash
git clone <your-repo-url> exploring-stock
cd exploring-stock
```

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Generate the dataset

All data settings live in ``codes/config.py``:

* ``DATA_DIR``: Location of the `.csv` dataset
* ``OUTPUT_FILE_NAME``: Final name of the `.csv` dataset
* ``DEFAULT_START``: Common start dates for all tickers
* ``DEFAULT_END``: Common end dates for all tickers
* ``DEFAULT_TIKCERS``: Default tickers of the companies

To (re)build ``datasets/companies.csv`` for the configured tickers and date range:

```bash
python -m codes.build_dataset
```

This uses ``codes.data_loader.fetch_ticker_history`` and ``build_universe`` to download and concatenate data, then saves a single CSV in ``datasets/``.

5. Run the Flask app

* From the project root:

```bash
python app.py
```

* Flask starts in development mode on ``http://127.0.0.1:5000/``.
    * Open ``http://127.0.0.1:5000/`` in a browser.
    * Use the Ticker dropdown to switch between companies.
    * Use the Metric dropdown to switch between ``open``, ``high``, ``low``, ``close``, ``adj_close``, and ``volume``.
    * The Plotly chart updates via the ``/api/figure`` endpoint.
    * You can also call the APIs directly, for example:
        * ``http://127.0.0.1:5000/api/tickers``
        * ``http://127.0.0.1:5000/api/metrics``
        * ``http://127.0.0.1:5000/api/history?ticker=DPZ``
        * ``http://127.0.0.1:5000/api/figure?ticker=DPZ&metric=close``

## Development notes

* Core data logic is isolated in ``codes/data_loader.py`` so it can be reused from the notebook and other backends.
* Configuration is centralized in ``codes/config.py``; changing tickers or date ranges there is enough to regenerate everything.