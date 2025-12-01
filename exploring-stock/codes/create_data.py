import pandas as pd
import yfinance as yf

def create_dataframe(ticker:str="AAPL", start_date:str="2020-01-01", end_date:str="2021-01-01"):

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
    
    col_map = {
        "Date": "date", "Open":  "open",  "High": "high", "Low": "low", "Close": "close", "Adj Close": "adj_close", "Volume": "volume"
    }
    df.rename(columns=col_map, inplace=True)
    df["company_ticker"] = ticker

    print(f"Dataframe created successfully for {ticker}!")
    
    return df

def create_csv_data(output_file_name:str, tickers, start_date:str="2020-01-01", end_date:str="2021-01-01"):

    dfs = []
    for ticker in tickers:
        df = create_dataframe(ticker, start_date, end_date)   # one ticker, flat columns
        dfs.append(df)

    # row-wise stack
    df_final = pd.concat(dfs, axis=0, ignore_index=True)

    df_final.to_csv(f"../datasets/{output_file_name}", index=False)