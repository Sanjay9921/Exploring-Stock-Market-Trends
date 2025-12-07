# codes/01-broker-simulator/modules/broker_raw_data.py

from pathlib import Path
import random
import pandas as pd

from settings.config import BROKERS, CLIENTS, UNIVERSE, START_DATE, END_DATE, BASE_CURRENCY
from modules.domain import Broker, Client

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw_data"
TICKER_DATA_DIR = DATA_DIR / "ticker_data"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
TICKER_DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_raw_prices(companies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Take companies.csv (ticker OHLCV) and attach a broker_name column to
    simulate a broker-style raw_prices.csv.
    """
    if companies_df.empty:
        print("companies_df empty; raw_prices.csv not created")
        return pd.DataFrame()

    prices_df = companies_df.copy()
    prices_df["broker_name"] = "BrokerA"  # or choose per ticker if you like

    cols = [
        "broker_name",
        "ticker",
        "date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]
    prices_df = prices_df[cols]

    out_path = RAW_DATA_DIR / "raw_prices.csv"
    prices_df.to_csv(out_path, index=False)
    print(f"Wrote raw_prices.csv with {len(prices_df)} rows")
    return prices_df

def build_raw_positions(companies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate positions per broker, client, and ticker using last available close as reference.
    """
    if companies_df.empty:
        print("No companies data; cannot generate positions")
        return pd.DataFrame()

    latest_prices = (
        companies_df.sort_values("date").groupby("ticker")["close"].last().to_dict()
    )

    rows = []
    for broker in BROKERS:
        for client in CLIENTS:
            for ticker in UNIVERSE:
                if ticker not in latest_prices:
                    continue
                last_price = latest_prices[ticker]
                qty = random.choice([5, 10, 15, 20, 50])
                avg_price = round(last_price * random.uniform(0.8, 1.2), 2)

                rows.append(
                    {
                        "broker_name": broker,
                        "client_id": client["id"],
                        "client_name": client["name"],
                        "account_name": f"{client['name']} - {broker} Account",
                        "ticker": ticker,
                        "quantity": qty,
                        "avg_price": avg_price,
                        "currency": BASE_CURRENCY,
                    }
                )

    positions_df = pd.DataFrame(rows)
    out_path = RAW_DATA_DIR / "raw_positions.csv"
    positions_df.to_csv(out_path, index=False)
    print(f"Wrote raw_positions.csv with {len(positions_df)} rows")
    return positions_df