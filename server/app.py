from flask import Flask # type:ignore
from flask_cors import CORS # type:ignore
from extensions import db, jwt # type:ignore
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required 
#voy a importar JWTManager
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.trip_routes import trip_bp
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)  
    JWTManager(app)  

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(trip_bp, url_prefix="/api/trips")

    with app.app_context():
        from models import user, trip  # 
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
