# codes/02-unified-wealth-migration/modules/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = "account"
    acct_id = db.Column(db.Integer, primary_key=True)
    acct_name = db.Column(db.String(200), nullable=False)
    broker_name = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.String(50), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    base_currency = db.Column(db.String(3), nullable=False, default="USD")

    holdings = relationship("Holding", back_populates="account")

class Asset(db.Model):
    __tablename__ = "asset"
    at_id = db.Column(db.Integer, primary_key=True)
    at_ticker = db.Column(db.String(20), unique=True, nullable=False)
    at_name = db.Column(db.String(200), nullable=False)
    at_class = db.Column(db.String(50), nullable=False, default="equity")
    at_currency = db.Column(db.String(3), nullable=False, default="USD")

    holdings = relationship("Holding", back_populates="asset")

class Holding(db.Model):
    __tablename__ = "holding"
    hold_id = db.Column(db.Integer, primary_key=True)
    acct_id = db.Column(db.Integer, db.ForeignKey("account.acct_id"), nullable=False)
    at_id = db.Column(db.Integer, db.ForeignKey("asset.at_id"), nullable=False)
    hold_quantity = db.Column(db.Float, nullable=False)
    hold_cost_basis = db.Column(db.Float, nullable=False)  # per-unit average cost

    account = relationship("Account", back_populates="holdings")
    asset = relationship("Asset", back_populates="holdings")
