# codes/02-unified-wealth-migration/tests/test_migration.py

from flask import Flask
import pandas as pd

from settings.config import DB_URI, TEST_DATA_DIR
from modules.models import db, Account, Asset, Holding

def create_test_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def test_basic_counts_and_export():
    """
    Requires that:
      1) Module 1 has generated raw_positions.csv
      2) Module 2 main.py has been run to migrate data into portfolio.db

    This test both asserts row counts and writes CSV snapshots into data/test_data.
    """
    app = create_test_app()

    with app.app_context():
        acct_q = Account.query.all()
        asset_q = Asset.query.all()
        holding_q = Holding.query.all()

        # Basic assertions
        assert len(acct_q) > 0
        assert len(asset_q) > 0
        assert len(holding_q) > 0

        # Export to CSV in test_data
        accounts_df = pd.DataFrame(
            [
                {
                    "acct_id": a.acct_id,
                    "acct_name": a.acct_name,
                    "broker_name": a.broker_name,
                    "client_id": a.client_id,
                    "client_name": a.client_name,
                    "base_currency": a.base_currency,
                }
                for a in acct_q
            ]
        )
        assets_df = pd.DataFrame(
            [
                {
                    "at_id": s.at_id,
                    "at_ticker": s.at_ticker,
                    "at_name": s.at_name,
                    "at_class": s.at_class,
                    "at_currency": s.at_currency,
                }
                for s in asset_q
            ]
        )
        holdings_df = pd.DataFrame(
            [
                {
                    "hold_id": h.hold_id,
                    "acct_id": h.acct_id,
                    "at_id": h.at_id,
                    "hold_quantity": h.hold_quantity,
                    "hold_cost_basis": h.hold_cost_basis,
                }
                for h in holding_q
            ]
        )

        accounts_path = TEST_DATA_DIR / "accounts_snapshot.csv"
        assets_path = TEST_DATA_DIR / "assets_snapshot.csv"
        holdings_path = TEST_DATA_DIR / "holdings_snapshot.csv"

        accounts_df.to_csv(accounts_path, index=False)
        assets_df.to_csv(assets_path, index=False)
        holdings_df.to_csv(holdings_path, index=False)

        print(f"✅ Wrote {accounts_path}")
        print(f"✅ Wrote {assets_path}")
        print(f"✅ Wrote {holdings_path}")