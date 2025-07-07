from urllib import request
from flask import jsonify  # type: ignore
from models.user import User
from extensions import db  # type: ignore
import bcrypt  # type: ignore
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity  # type: ignore
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

    # ✅ Crear token válido para flask_jwt_extended
    access_token = create_access_token(identity=str(user.id))


    return jsonify({
        "token": access_token, # type: ignore
        "username": user.username # type: ignore
    }), 200

@jwt_required()
def profile_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200
