# codes/02-unified-wealth-migration/main.py

from flask import Flask
from settings.config import DB_URI, DB_PATH, DATA_DIR
from modules.models import db
from modules.migrate_broker_data import run_migration

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def init_db(app):
    with app.app_context():
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Initializing database at {DB_PATH}")
        db.drop_all()
        db.create_all()
        print("Tables created (account, asset, holding)")

if __name__ == "__main__":
    app = create_app()
    init_db(app)
    run_migration(app)
    print("Module 2 (unified-wealth-migration) completed.")
