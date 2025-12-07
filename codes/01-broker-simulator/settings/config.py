# codes/01-broker-simulator/settings/config.py

BROKERS = ["BrokerA", "BrokerB"]

CLIENTS = [
    {"id": "C001", "name": "Client A"},
    {"id": "C002", "name": "Client B"},
]

UNIVERSE = ["AAPL", "AMZN", "GOOGL", "META", "MSFT"]  # Tickers to simulate

START_DATE = "2024-01-01"
END_DATE = "2025-10-31"

BASE_CURRENCY = "USD"