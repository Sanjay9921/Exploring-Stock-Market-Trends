# modules/data/helper.py

"""Creates the `companies.csv` dataset using the Yahoo Finance Python API"""

import pandas as pd
import yfinance as yf
from modules.settings.config import DATA_DIR, OUTPUT_FILE, DEFAULT_START_DATE, DEFAULT_END_DATE, DEFAULT_TICKERS, DEAFULT_TICKER

COLUMN_MAP = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
}

def create_dataframe(ticker=DEAFULT_TICKER, start_date=DEFAULT_START_DATE, end_date=DEFAULT_END_DATE):

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False, # keep both "Close" and "Adj Close" if available
    )

    # ISSUE FIXED: for MultiIndex column of "Ticker"
    ## Flattening
    if isinstance(df.columns, pd.MultiIndex):
        # keep the first level, remove the second level of "Ticker"
        df.columns = df.columns.get_level_values(0)
    
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']) # convert the date column to date :)
    
    col_map = COLUMN_MAP
    
    df.rename(columns=col_map, inplace=True)
    df["company_ticker"] = ticker

    print(f"Dataframe created successfully for {ticker}!")
    
    return df

def create_csv_data(tickers=DEFAULT_TICKERS, start_date=DEFAULT_START_DATE, end_date=DEFAULT_END_DATE) -> None:

    dfs = []
    for ticker in tickers:
        df = create_dataframe(ticker, start_date, end_date) # one ticker, flat columns
        dfs.append(df)

    # row-wise stack
    df_final = pd.concat(dfs, axis=0, ignore_index=True)

    df_final.to_csv(f"./{DATA_DIR}/{OUTPUT_FILE}", index=False)
    print(f"Saved dataset to datasets/{OUTPUT_FILE}")