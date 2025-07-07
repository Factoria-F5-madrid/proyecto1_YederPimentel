from flask import Flask # type:ignore
from flask_cors import CORS # type:ignore
from extensions import db # type:ignore
from db import db
from routes.auth_routes import auth_bp
from routes.trip_routes import trip_bp
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # puedes usar directamente Config

    CORS(app)
    db.init_app(app)

    with app.app_context():
        from models import user, trip  # 👈 asegura que las tablas se crean
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(trip_bp, url_prefix="/api/trips")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
