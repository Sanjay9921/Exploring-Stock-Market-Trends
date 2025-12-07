# codes/03-consolidated-data-json/app.py

from flask import Flask, render_template
from flask_cors import CORS

from settings.config import DB_URI, DB_PATH, EXPORT_DIR
from modules.services.db_session import db
from modules.codes_02_models import Account  # to verify DB connection
from modules.api.accounts import accounts_bp
from modules.api.holdings import holdings_bp
from modules.api.marketdata import marketdata_bp
from modules.api.export import export_bp

from modules.api.export import export_bp

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(accounts_bp)
    app.register_blueprint(holdings_bp)
    app.register_blueprint(marketdata_bp)
    app.register_blueprint(export_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/debug/db")
    def debug_db():
        with app.app_context():
            return {
                "db_path": str(DB_PATH),
                "accounts": Account.query.count(),
            }
        
    @app.route("/static-json/accounts")
    def static_accounts():
        path = EXPORT_DIR / "accounts.json"
        return app.response_class(
            path.read_text(encoding="utf-8"),
            mimetype="application/json",
        )

    return app


if __name__ == "__main__":
    app = create_app()
    print(f"Starting Consolidated Data JSON API using DB at {DB_PATH}")
    app.run(debug=True, port=5000)
