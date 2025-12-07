# codes/03-consolidated-data-json/modules/api/marketdata.py

from flask import Blueprint, jsonify, request
from pathlib import Path
import pandas as pd

from settings.config import COMPANIES_CSV

marketdata_bp = Blueprint("marketdata_bp", __name__)


@marketdata_bp.route("/api/ohlcv", methods=["GET"])
def get_ohlcv():
    """
    Return OHLCV time series for a given ticker and optional date range
    using companies.csv produced by Module 1.
    """
    ticker = request.args.get("ticker")
    start = request.args.get("start")  # ISO date or None
    end = request.args.get("end")

    if not ticker:
        return jsonify({"error": "ticker query parameter is required"}), 400

    if not COMPANIES_CSV.exists():
        return jsonify({"error": f"companies.csv not found at {COMPANIES_CSV}"}), 500

    df = pd.read_csv(COMPANIES_CSV, parse_dates=["date"])
    df = df[df["ticker"] == ticker]

    if start:
        df = df[df["date"] >= pd.to_datetime(start)]
    if end:
        df = df[df["date"] <= pd.to_datetime(end)]

    if df.empty:
        return jsonify([])

    df = df.sort_values("date")
    records = [
        {
            "date": d["date"].strftime("%Y-%m-%d"),
            "open": float(d["open"]),
            "high": float(d["high"]),
            "low": float(d["low"]),
            "close": float(d["close"]),
            "adj_close": float(d["adj_close"]),
            "volume": int(d["volume"]),
            "ticker": d["ticker"],
        }
        for _, d in df.iterrows()
    ]

    return jsonify(records)
