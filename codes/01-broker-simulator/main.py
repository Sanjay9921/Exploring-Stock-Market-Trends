# codes/01-broker-simulator/main.py

from modules.companies_data import build_companies_dataset
from modules.broker_raw_data import build_raw_prices, build_raw_positions
from settings.config import START_DATE, END_DATE, UNIVERSE

def run():
    print("Running broker simulator (Module 1)")
    print(f"Date range: {START_DATE} → {END_DATE}")
    print(f"Tickers: {', '.join(UNIVERSE)}")

    companies_df = build_companies_dataset()
    if companies_df.empty:
        print("Aborting: no ticker data")
        return

    prices_df = build_raw_prices(companies_df)
    positions_df = build_raw_positions(companies_df)

    print("Module 1 finished.")
    print(f"companies.csv rows:     {len(companies_df)}")
    print(f"raw_prices.csv rows:    {len(prices_df)}")
    print(f"raw_positions.csv rows: {len(positions_df)}")

if __name__ == "__main__":
    run()