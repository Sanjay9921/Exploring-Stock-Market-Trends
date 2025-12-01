# codes/data_loader.py
from __future__ import annotations
from pathlib import Path
from typing import Iterable, List

import pandas as pd
import yfinance as yf

from .config import DATA_DIR, DEFAULT_START, DEFAULT_END


COLUMN_MAP = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
}


def fetch_ticker_history(
    ticker: str,
    start_date: str = DEFAULT_START,
    end_date: str = DEFAULT_END,
) -> pd.DataFrame:
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.rename(columns=COLUMN_MAP)
    df["company_ticker"] = ticker
    return df


def build_universe(
    tickers: Iterable[str],
    start_date: str = DEFAULT_START,
    end_date: str = DEFAULT_END,
) -> pd.DataFrame:
    frames: List[pd.DataFrame] = [
        fetch_ticker_history(t, start_date, end_date) for t in tickers
    ]
    return pd.concat(frames, axis=0, ignore_index=True)


def save_universe_to_csv(
    output_name: str,
    tickers: Iterable[str],
    start_date: str = DEFAULT_START,
    end_date: str = DEFAULT_END,
) -> Path:
    df = build_universe(tickers, start_date, end_date)
    out_path = Path(DATA_DIR) / output_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path