from flask import jsonify # type:ignore
from models.user import User
from extensions import db # type:ignore
from werkzeug.security import generate_password_hash, check_password_hash # type:ignore
import jwt # type:ignore
import datetime
from flask import current_app as app # type:ignore

def register_user(data):
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token, "username": user.username}), 200
