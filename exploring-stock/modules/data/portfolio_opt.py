# modules/data/portfolio_opt.py

import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier

def compute_portfolios(companies_df):
    returns_df = companies_df.pct_change().dropna()

    # Task 1: 1/n benchmark
    # Calculate returns
    returns_df = companies_df.pct_change().dropna()

    # Calculate the 1/n portfolio weights
    portfolio_weights = 5 * [0.2]

    # Calculate the portfolio returns of the 1/n portfolio
    portfolio_returns = returns_df.dot(portfolio_weights)

    # Calculate the expected portfolio return
    benchmark_exp_return = portfolio_returns.mean()

    # Calculate the portfolio's Sharpe ratio
    benchmark_sharpe_ratio = (
        portfolio_returns.mean() / portfolio_returns.std() * np.sqrt(252)
    )

    # Task 2: min‑vol portfolio
    # Calculate the annualized expected returns and the covariance matrix
    avg_returns = returns_df.mean() * 252
    cov_mat = returns_df.cov() * 252

    # Instantiate the EfficientFrontier object
    ef = EfficientFrontier(avg_returns, cov_mat)

    # Find the weights that maximize the Sharpe ratio
    weights = ef.min_volatility()
    mv_portfolio = pd.Series(weights)

    # Find the minimized volatility
    mv_portfolio_vol = ef.portfolio_performance(risk_free_rate=0)[1]

    # Task 3: max‑Sharpe portfolio
    # Instantiate the EfficientFrontier object
    ef = EfficientFrontier(avg_returns, cov_mat)

    # Find the weights that maximize the Sharpe ratio
    weights = ef.max_sharpe(risk_free_rate=0)
    ms_portfolio = pd.Series(weights)

    # Find the maximized Sharpe ratio
    ms_portfolio_sharpe = ef.portfolio_performance(risk_free_rate=0)[2]

    return {
        "benchmark": {
            "weights": portfolio_weights,
            "expected_return": benchmark_exp_return,
            "sharpe": benchmark_sharpe_ratio,
        },
        "min_vol": {
            "weights": mv_portfolio.to_dict(),
            "volatility": mv_portfolio_vol,
        },
        "max_sharpe": {
            "weights": ms_portfolio.to_dict(),
            "sharpe": ms_portfolio_sharpe,
        },
    }