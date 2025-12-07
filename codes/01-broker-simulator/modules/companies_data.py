# codes/01-broker-simulator/modules/companies_data.py

from pathlib import Path
import pandas as pd
import yfinance as yf

from settings.config import BROKERS, CLIENTS, UNIVERSE, START_DATE, END_DATE, BASE_CURRENCY
from modules.domain import TickerConfig

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw_data"
TICKER_DATA_DIR = DATA_DIR / "ticker_data"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
TICKER_DATA_DIR.mkdir(parents=True, exist_ok=True)

COLUMN_MAP = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
}

def fetch_ticker_ohlcv(ticker: str, start_date=START_DATE, end_date=END_DATE) -> pd.DataFrame:
    """Download OHLCV for a single ticker and save to ticker_data/."""
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False, # keep both "Close" and "Adj Close" if available
    )

    if df.empty:
        print(f"No data for {ticker}")
        return df

    # ISSUE FIXED: for MultiIndex column of "Ticker"
    ## Flattening
    if isinstance(df.columns, pd.MultiIndex):
        # keep the first level, remove the second level of "Ticker"
        df.columns = df.columns.get_level_values(0)
    
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']) # convert the date column to date :)
    
    col_map = COLUMN_MAP
    
    df.rename(columns=col_map, inplace=True)
    df["ticker"] = ticker
    
    out_path = TICKER_DATA_DIR / f"{ticker}.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved OHLCV for {ticker} to {out_path}")
    return df


def build_companies_dataset() -> pd.DataFrame:
    """
    Fetch OHLCV for all tickers in UNIVERSE and store one clean companies.csv
    plus per-ticker files in ticker_data/.
    """
    all_frames = []
    for ticker in UNIVERSE:
        df = fetch_ticker_ohlcv(ticker, START_DATE, END_DATE)
        if df.empty:
            continue
        all_frames.append(df)  # df already has columns: date, open, high, low, close, adj_close, volume, ticker

    if not all_frames:
        print("No ticker data collected, companies.csv not created")
        return pd.DataFrame()

    companies_df = pd.concat(all_frames, ignore_index=True)
    companies_df.to_csv(TICKER_DATA_DIR / "companies.csv", index=False)
    print(f"Wrote companies.csv with {len(companies_df)} rows")

    # Optional: keep one CSV per ticker for convenience
    for ticker, grp in companies_df.groupby("ticker"):
        grp.to_csv(TICKER_DATA_DIR / f"{ticker}.csv", index=False)

    return companies_df
