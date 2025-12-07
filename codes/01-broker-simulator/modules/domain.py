# codes/01-broker-simulator/modules/domain.py

from dataclasses import dataclass

@dataclass
class Broker:
    name: str

@dataclass
class Client:
    id: str
    name: str

@dataclass
class TickerConfig:
    symbol: str
    currency: str = "USD"
    asset_class: str = "equity"  # for later use in migration