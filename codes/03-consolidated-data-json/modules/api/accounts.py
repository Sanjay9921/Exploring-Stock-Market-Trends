# codes/03-consolidated-data-json/modules/api/accounts.py

from flask import Blueprint, jsonify
from modules.services.db_session import db
from modules.codes_02_models import Account  # see note below

accounts_bp = Blueprint("accounts_bp", __name__)

@accounts_bp.route("/api/accounts", methods=["GET"])
def get_accounts():
    """
    Return all accounts with basic metadata and holding counts.
    """
    accounts = (
        db.session.query(Account)
        .order_by(Account.acct_id)
        .all()
    )

    result = []
    for a in accounts:
        result.append(
            {
                "acct_id": a.acct_id,
                "acct_name": a.acct_name,
                "broker_name": a.broker_name,
                "client_id": a.client_id,
                "client_name": a.client_name,
                "base_currency": a.base_currency,
                "holding_count": len(a.holdings),
            }
        )

    return jsonify(result)
