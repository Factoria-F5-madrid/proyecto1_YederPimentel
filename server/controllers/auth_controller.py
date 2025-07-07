from flask import jsonify  # type: ignore
from models.user import User
from extensions import db  # type: ignore
import bcrypt  # type: ignore
import jwt  # type: ignore
import datetime
from flask import current_app as app  # type: ignore

def register_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Hash password con bcrypt
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generar token JWT
    token = jwt.encode({
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({
        "token": token,
        "username": user.username
    }), 200
