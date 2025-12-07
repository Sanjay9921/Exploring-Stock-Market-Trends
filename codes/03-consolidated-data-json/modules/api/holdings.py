# codes/03-consolidated-data-json/modules/api/holdings.py

from flask import Blueprint, jsonify, request
from modules.services.db_session import db
from modules.codes_02_models import Account, Asset, Holding

holdings_bp = Blueprint("holdings_bp", __name__)


@holdings_bp.route("/api/holdings", methods=["GET"])
def get_holdings():
    """
    Return holdings for a given account, or all if acct_id not provided.
    """
    acct_id = request.args.get("acct_id", type=int)

    query = (
        db.session.query(Holding, Account, Asset)
        .join(Account, Holding.acct_id == Account.acct_id)
        .join(Asset, Holding.at_id == Asset.at_id)
    )
    if acct_id is not None:
        query = query.filter(Account.acct_id == acct_id)

    rows = query.all()

    result = []
    for hold, acct, asset in rows:
        result.append(
            {
                "hold_id": hold.hold_id,
                "acct_id": acct.acct_id,
                "acct_name": acct.acct_name,
                "broker_name": acct.broker_name,
                "client_name": acct.client_name,
                "ticker": asset.at_ticker,
                "asset_class": asset.at_class,
                "quantity": hold.hold_quantity,
                "cost_basis": hold.hold_cost_basis,
                "currency": asset.at_currency,
            }
        )

    return jsonify(result)
