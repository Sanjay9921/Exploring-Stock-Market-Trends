# app.py
from pathlib import Path

from flask import Flask, jsonify, render_template, request
import pandas as pd
import plotly.express as px
import json
import plotly
from codes.config import DATA_DIR, OUTPUT_FILE_NAME
from codes.data_loader import COLUMN_MAP

app = Flask(__name__)

DATA_PATH = Path(DATA_DIR) / OUTPUT_FILE_NAME
companies = pd.read_csv(DATA_PATH, parse_dates=["date"])

VALUE_COLS = ["open", "high", "low", "close", "adj_close", "volume"] # OHLCV values


@app.get("/api/tickers")
def get_tickers():
    tickers = sorted(companies["company_ticker"].unique())
    return jsonify({"tickers": tickers})


@app.get("/api/metrics")
def get_metrics():
    return jsonify({"metrics": VALUE_COLS})


@app.get("/api/history")
def get_history():
    ticker = request.args.get("ticker", "AAPL")
    start = request.args.get("start")
    end = request.args.get("end")

    sub = companies[companies["company_ticker"] == ticker].copy()
    if start:
        sub = sub[sub["date"] >= start]
    if end:
        sub = sub[sub["date"] <= end]

    sub = sub.sort_values("date")
    return sub.to_json(orient="records", date_format="iso")


@app.get("/api/figure")
def get_figure():
    ticker = request.args.get("ticker", "AAPL")
    metric = request.args.get("metric", "close")

    if metric not in VALUE_COLS:
        return jsonify({"error": "invalid metric"}), 400

    sub = companies[companies["company_ticker"] == ticker].sort_values("date")
    fig = px.line(sub, x="date", y=metric, title=f"{ticker} – {metric.capitalize()}")

    # make it JSON‑serializable
    fig_json = json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
    return jsonify(fig_json)


@app.get("/")
def index():
    return render_template("index.html")
    

if __name__ == "__main__":
    app.run(debug=True)