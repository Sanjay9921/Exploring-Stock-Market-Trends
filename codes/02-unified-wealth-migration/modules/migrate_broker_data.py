# codes/02-unified-wealth-migration/modules/migrate_broker_data.py

import pandas as pd
from pathlib import Path

from settings.config import RAW_POSITIONS_PATH, DB_URI
from .models import db, Account, Asset, Holding

# Simple mapping from ticker to asset class (can be extended)
ASSET_CLASS_MAP = {
    "AAPL": "equity",
    "AMZN": "equity",
    "GOOGL": "equity",
    "META": "equity",
    "MSFT": "equity",
    "TLT": "bond",
    "VTI": "fund",
    "GLD": "alternative",
}

def infer_asset_class(ticker: str) -> str:
    return ASSET_CLASS_MAP.get(ticker, "equity")

def run_migration(app):
    """
    Main migration function: CSV from broker-simulator → SQLite tables.
    """
    with app.app_context():
        print(f"📥 Reading raw positions from {RAW_POSITIONS_PATH}")
        if not RAW_POSITIONS_PATH.exists():
            print("❌ raw_positions.csv not found. Run Module 1 first.")
            return

        raw_df = pd.read_csv(RAW_POSITIONS_PATH)

        required_cols = [
            "broker_name",
            "client_id",
            "client_name",
            "account_name",
            "ticker",
            "quantity",
            "avg_price",
            "currency",
        ]
        missing = [c for c in required_cols if c not in raw_df.columns]
        if missing:
            raise ValueError(f"Missing columns in raw_positions.csv: {missing}")

        # Drop rows with missing critical values
        raw_df = raw_df.dropna(subset=["broker_name", "client_id", "ticker"])
        print(f"📊 Raw positions rows after cleaning: {len(raw_df)}")

        # 1) Upsert Accounts
        account_cache = {}  # (broker_name, client_id, account_name) -> Account
        for _, row in raw_df[["broker_name", "client_id", "client_name", "account_name", "currency"]].drop_duplicates().iterrows():
            key = (row["broker_name"], row["client_id"], row["account_name"])
            if key in account_cache:
                continue

            acct = Account(
                acct_name=row["account_name"],
                broker_name=row["broker_name"],
                client_id=row["client_id"],
                client_name=row["client_name"],
                base_currency=row["currency"],
            )
            db.session.add(acct)
            db.session.flush()
            account_cache[key] = acct

        print(f"✅ Created {len(account_cache)} accounts")

        # 2) Upsert Assets
        asset_cache = {}  # ticker -> Asset
        for ticker, currency in raw_df[["ticker", "currency"]].drop_duplicates().itertuples(index=False):
            if ticker in asset_cache:
                continue
            asset = Asset(
                at_ticker=ticker,
                at_name=ticker,  # could be enriched later
                at_class=infer_asset_class(ticker),
                at_currency=currency,
            )
            db.session.add(asset)
            db.session.flush()
            asset_cache[ticker] = asset

        print(f"✅ Created {len(asset_cache)} assets")

        # 3) Create Holdings
        holding_rows = 0
        for _, row in raw_df.iterrows():
            acct_key = (row["broker_name"], row["client_id"], row["account_name"])
            account = account_cache[acct_key]
            asset = asset_cache[row["ticker"]]

            holding = Holding(
                acct_id=account.acct_id,
                at_id=asset.at_id,
                hold_quantity=float(row["quantity"]),
                hold_cost_basis=float(row["avg_price"]),
            )
            db.session.add(holding)
            holding_rows += 1

        db.session.commit()
        print(f"✅ Created {holding_rows} holdings")

        # Optional: quick stats
        print("📈 Migration summary:")
        print(f"   Accounts: {Account.query.count()}")
        print(f"   Assets:   {Asset.query.count()}")
        print(f"   Holdings: {Holding.query.count()}")
