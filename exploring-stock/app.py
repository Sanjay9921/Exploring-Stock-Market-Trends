from flask import Flask, jsonify, render_template, request
from pathlib import Path
from modules.data.portfolio_opt import compute_portfolios
from modules.settings.config import DATA_DIR, OUTPUT_FILE
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import json

# Flask App
app = Flask(__name__)

# Loading `companies.csv` into a dataframe
FILE_PATH = Path(DATA_DIR) / OUTPUT_FILE
companies_df = pd.read_csv(FILE_PATH, parse_dates=["date"])

# OHLCV
value_cols = ["open", "high", "low", "close", "adj_close", "volume"] 

# Assets Portfolio
stock_companies_df = companies_df.pivot_table(
    index="date",
    columns="company_ticker",
    values="close"
)
portfolio_data = compute_portfolios(stock_companies_df)

@app.get("/")
def index():

    return render_template("index.html", allocations=portfolio_data) # templates/index.html

@app.route("/api/health", methods=["GET"])
def get_health():

    return jsonify({"status":"Success"}), 200

# OHLCV metrics
@app.get("/api/metrics")
def get_metrics():
    return jsonify({"metrics": value_cols})

# Portfolio Tickers
@app.route("/api/tickers")
def get_tickers():
    tickers = companies_df["company_ticker"]
    tickers = sorted(tickers.unique())

    return jsonify({"tickers":tickers}), 200

# Portfolio Allocations
@app.route("/api/allocations")
def api_allocations():
    return portfolio_data

# Portfolio Historical Line Chart
@app.get("/api/history")
def get_history():
    ticker = request.args.get("ticker", "AAPL")
    start = request.args.get("start")
    end = request.args.get("end")

    sub = companies_df[companies_df["company_ticker"] == ticker].copy()
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

    if metric not in value_cols:
        return jsonify({"error": "invalid metric"}), 400

    sub = companies_df[companies_df["company_ticker"] == ticker].sort_values("date")
    fig = px.line(sub, x="date", y=metric, title=f"{ticker} – {metric.capitalize()}")

    # make it JSON‑serializable
    fig_json = json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
    return jsonify(fig_json)

if __name__ == "__main__":
    app.run(debug=True)