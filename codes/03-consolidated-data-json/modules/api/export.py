# codes/03-consolidated-data-json/modules/api/export.py

from flask import Blueprint, jsonify
import json
from settings.config import EXPORT_DIR
from modules.services.db_session import db
from modules.codes_02_models import Account, Asset, Holding

export_bp = Blueprint("export_bp", __name__)


@export_bp.route("/api/export/json", methods=["POST", "GET"])
def export_json():
    """
    Export current accounts and holdings to static JSON files under data/json_exports.
    """
    # Accounts
    accounts = db.session.query(Account).order_by(Account.acct_id).all()
    accounts_payload = [
        {
            "acct_id": a.acct_id,
            "acct_name": a.acct_name,
            "broker_name": a.broker_name,
            "client_id": a.client_id,
            "client_name": a.client_name,
            "base_currency": a.base_currency,
        }
        for a in accounts
    ]
    (EXPORT_DIR / "accounts.json").write_text(
        json.dumps(accounts_payload, indent=2), encoding="utf-8"
    )

    # Holdings (joined)
    holdings = (
        db.session.query(Holding, Account, Asset)
        .join(Account, Holding.acct_id == Account.acct_id)
        .join(Asset, Holding.at_id == Asset.at_id)
        .all()
    )
    holdings_payload = [
        {
            "hold_id": h.hold_id,
            "acct_id": a.acct_id,
            "acct_name": a.acct_name,
            "broker_name": a.broker_name,
            "client_name": a.client_name,
            "ticker": s.at_ticker,
            "asset_class": s.at_class,
            "quantity": h.hold_quantity,
            "cost_basis": h.hold_cost_basis,
            "currency": s.at_currency,
        }
        for h, a, s in holdings
    ]
    (EXPORT_DIR / "holdings.json").write_text(
        json.dumps(holdings_payload, indent=2), encoding="utf-8"
    )

    return jsonify(
        {
            "status": "ok",
            "accounts_file": str(EXPORT_DIR / "accounts.json"),
            "holdings_file": str(EXPORT_DIR / "holdings.json"),
        }
    )
