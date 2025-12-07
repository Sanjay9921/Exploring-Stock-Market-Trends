# Exploring Stock Market Trends with Multi‑Broker Wealth Data Migration and JSON API

## Overview

This project simulates a small wealth platform in three modules:

* **Broker simulator** – generates realistic broker CSV exports and OHLCV data using yfinance.
* **Unified wealth migration** – migrates broker CSVs into a normalized SQLite database with SQLAlchemy.
* **Consolidated JSON API** – exposes accounts, holdings, and market data as REST JSON (plus static JSON files) that reporting tools like Power BI can consume.

Everything lives in the existing Exploring‑Stock‑Market‑Trends repository under the ``codes/`` folder.

## Project Structure

```text
Exploring-Stock-Market-Trends/
├─ venv/                           # Virtualenv (not committed)
├─ requirements.txt
├─ README.md                       # This file
├─ codes/
│  ├─ 01-broker-simulator/
│  │   ├─ data/
│  │   │   ├─ raw_data/           # raw_positions.csv, raw_prices.csv
│  │   │   └─ ticker_data/        # companies.csv + per-ticker OHLCV CSVs
│  │   ├─ modules/
│  │   │   ├─ domain.py
│  │   │   ├─ companies_data.py
│  │   │   ├─ broker_raw_data.py
│  │   │   └─ main.py
│  │   ├─ settings/config.py
│  │   └─ main.py                 # entry point for Module 1
│  │
│  ├─ 02-unified-wealth-migration/
│  │   ├─ data/
│  │   │   ├─ migrated_data/      # portfolio.db + optional CSV snapshots
│  │   │   └─ test_data/          # test snapshot CSVs
│  │   ├─ modules/
│  │   │   ├─ models.py           # Account, Asset, Holding
│  │   │   └─ migrate_broker_data.py
│  │   ├─ settings/config.py
│  │   ├─ tests/
│  │   │   └─ test_migration.py
│  │   └─ main.py                 # entry point for Module 2
│  │
│  └─ 03-consolidated-data-json/
│      ├─ data/
│      │   └─ json_exports/       # accounts.json, holdings.json (static)
│      ├─ modules/
│      │   ├─ services/db_session.py
│      │   ├─ codes_02_models.py  # imports models from Module 2
│      │   └─ api/
│      │       ├─ accounts.py     # /api/accounts
│      │       ├─ holdings.py     # /api/holdings
│      │       ├─ marketdata.py   # /api/ohlcv
│      │       └─ export.py       # /api/export/json
│      ├─ settings/config.py
│      ├─ templates/index.html
│      └─ app.py                  # entry point for Module 3
```

## Concepts and data model

The normalized wealth schema in Module 2 uses three tables:

* Account: Represents a client account at a broker (e.g. “Client A – BrokerA Account”), with broker name, client id, and base currency.
* Asset: One row per ticker (AAPL, MSFT, TLT, etc.), including asset class (equity, bond, fund, alternative) and currency.
* Holding: Link table -> how many units of a given asset are held in a given account, and at which average cost basis.

This is enough to answer: “Who owns what, at which broker, and in which asset class?” and to compute simple portfolio views later.

## Modules

### Module 1 – Broker simulator

**Goal:** Pretend to be multiple brokers managing high‑net‑worth clients and exporting data as CSVs. Uses ``yfinance`` to fetch OHLCV prices.

**Key scripts**
    * ``settings/config.py``
        * Defines BROKERS, CLIENTS, UNIVERSE (list of tickers), START_DATE, END_DATE, BASE_CURRENCY.
    * ``modules/companies_data.py``
        * ``fetch_ticker_ohlcv(symbol, start, end)`` – fetches OHLCV for one ticker and standardizes columns (date, open, high, low, close, adj_close, volume, ticker).
        * ``build_companies_dataset()`` – loops over all tickers in UNIVERSE, aggregates them into ``companies.csv`` and also writes per‑ticker CSVs (AAPL.csv, MSFT.csv, etc.) in ``ticker_data/``.
    * ``modules/broker_raw_data.py``
        * ``build_raw_prices(companies_df)`` – adds broker_name to each OHLCV row to create ``raw_prices.csv``.
        * ``build_raw_positions(companies_df)`` – simulates positions for each broker × client × ticker using last close as reference price and random quantities and cost bases, writing ``raw_positions.csv``.
    * ``modules/main.py``
        * Orchestrates the above functions.

**Running Module 1**

```bash
python codes/01-broker-simulator/main.py # from the root repo
```

***Expected outputs***

* ``codes/01-broker-simulator/data/ticker_data/companies.csv`` – base OHLCV dataset (all tickers).
* ``codes/01-broker-simulator/data/ticker_data/*.csv`` – per‑ticker OHLCV files.
* ``codes/01-broker-simulator/data/raw_data/raw_prices.csv`` – broker‑style price export.
* ``codes/01-broker-simulator/data/raw_data/raw_positions.csv`` – broker‑style positions export.

### Module 2 – Unified wealth migration

**Goal:** Migrate Module 1’s broker CSVs into a unified wealth schema using SQLite + SQLAlchemy. This simulates a central portfolio platform consolidating data from multiple brokers.

**Key scripts**
    * ``settings/config.py``
        * Locates ``raw_positions.csv`` from Module 1.
        * Defines ``DB_PATH`` pointing to ``codes/02-unified-wealth-migration/data/migrated_data/portfolio.db``.
    * ``modules/models.py``
        * Account, Asset, Holding models using db = SQLAlchemy() and relationship(back_populates=...).
    * ``modules/migrate_broker_data.py``
        * Reads ``raw_positions.csv`` into pandas.
        * Cleans and validates required columns.
        * Inserts unique accounts (per broker/client/account_name).
        * Inserts unique assets (per ticker), inferring asset class via a simple mapping.
        * Inserts holdings (quantity, cost basis) linking accounts and assets.
    * ``main.py``
        * Creates the Flask app, initializes the DB (``db.drop_all()`` + ``db.create_all()``), then calls ``run_migration(app)``.
    * ``tests/test_migration.py``
        * Uses Flask + SQLAlchemy to query ``Account``, ``Asset``, ``Holding``, assert non‑zero counts, and exports CSV snapshots into ``data/test_data/``.

**Running Module 2**

```bash
python codes/02-unified-wealth-migration/main.py # from root repo
```

**Expected outputs**
    * ``codes/02-unified-wealth-migration/data/migrated_data/portfolio.db`` – unified wealth database.
    * ``codes/02-unified-wealth-migration/data/test_data/*.csv`` – optional test snapshots via pytest.

**PyTest Check**

```bash
pytest codes/02-unified-wealth-migration/tests/test_migration.py -v # from the root repo
```

### Module 3 – Consolidated JSON API

**Goal:** Provide a clean JSON interface over the unified DB and OHLCV data, and *optionally export static JSON snapshots for tools like Power BI*.

**Key scripts**
    * ``settings/config.py``
        * Computes DB_URI pointing to Module 2’s ``portfolio.db`` in ``data/migrated_data/``.
        * Points to Module 1’s ``companies.csv``.
        * Defines ``EXPORT_DIR`` for static JSON files.
    * ``modules/services/db_session.py``
        * Holds a shared ``SQLAlchemy()`` instance used in Module 3.
    * ``modules/codes_02_models.py``
        * Adds Module 2 directory to ``sys.path`` and imports ``Account``, ``Asset``, ``Holding`` from ``02-unified-wealth-migration/modules/models.py``.
    * ``modules/api/accounts.py`` – **/api/accounts**
        * Returns all accounts with broker, client, base currency, and number of holdings.
    * ``modules/api/holdings.py`` – **/api/holdings**
        * Returns joined holdings view with account and asset info.
        * Supports ``?acct_id=``... filter.
    * ``modules/api/marketdata.py`` – **/api/ohlcv**
        * Reads OHLCV from ``companies.csv``.
        * Query parameters: ticker (required), optional start, end dates.
        * Returns a JSON array of OHLCV rows for one ticker.
    * ``modules/api/export.py`` – **/api/export/json**
        * Exports current accounts and holdings into static JSON files:
        * ``data/json_exports/accounts.json``
        * ``data/json_exports/holdings.json``
    * ``app.py``
        * Creates Flask app, configures ``SQLAlchemy`` with ``DB_URI``, registers all blueprints.
        * Additional routes:
            * ``/`` – HTML index page with documentation and links.
            * ``/debug/db`` – quick DB health check (db_path, account count).
            * ``/static-json/accounts`` – serves ``accounts.json`` over HTTP.
    * ``templates/index.html``
        * Lists all live API endpoints and ``export/static`` URLs, with short descriptions.

**Running Module 3**

```bash
python codes/03-consolidated-data-json/app.py # from root repo
```

**Key URLs**

* Index: ``http://localhost:5000/``
* Accounts: ``http://localhost:5000/api/accounts``
* Holdings: ``http://localhost:5000/api/holdings``
* Holdings by account: ``http://localhost:5000/api/holdings?acct_id=1``
* OHLCV: ``http://localhost:5000/api/ohlcv?ticker=AAPL``
* Export static JSON: ``http://localhost:5000/api/export/json``
* Static accounts JSON over HTTP: ``http://localhost:5000/static-json/accounts``

## End‑to‑end run order

```bash
# from the root repo

# 1. Simulate brokers and generate CSVs + OHLCV
python codes/01-broker-simulator/main.py

# 2. Migrate broker CSVs into unified wealth database
python codes/02-unified-wealth-migration/main.py

# 3. Start consolidated JSON API
python codes/03-consolidated-data-json/app.py

```

Once Flask is running, open ``http://localhost:5000/`` and follow the links.

## Guides

TBD