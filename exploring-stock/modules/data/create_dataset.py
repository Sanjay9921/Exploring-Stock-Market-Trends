# modules/data/create_dataset.py

""" Builds `companies.csv` dataset by using the functions from `helper.py` module """

import pandas as pd
import yfinance as yf
from modules.settings.config import DATA_DIR, OUTPUT_FILE, DEFAULT_START_DATE, DEFAULT_END_DATE, DEFAULT_TICKERS
from modules.data.helper import create_csv_data

def main() -> None:
    create_csv_data(DEFAULT_TICKERS, DEFAULT_START_DATE, DEFAULT_END_DATE)

if __name__ == "__main__":
    main()