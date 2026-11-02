"""Accounts REST service application factory."""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman

from service.models import db
from service.routes import accounts


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///accounts.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FORCE_HTTPS=os.getenv("FORCE_HTTPS", "false").lower() == "true",
        CORS_ALLOWED_ORIGINS=[
            origin.strip()
            for origin in os.getenv(
                "CORS_ALLOWED_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000",
            ).split(",")
            if origin.strip()
        ],
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"], supports_credentials=False)
    Talisman(
        app,
        force_https=app.config["FORCE_HTTPS"],
        content_security_policy={
            "default-src": "'none'",
            "frame-ancestors": "'none'",
            "base-uri": "'none'",
        },
    )

    app.register_blueprint(accounts)

    @app.get("/")
    def index():
        return jsonify({"service": "Accounts REST API", "version": "1.0.0"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app
