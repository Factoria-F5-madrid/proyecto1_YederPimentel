from flask import Blueprint, request, jsonify # type:ignore
from flask_jwt_extended import jwt_required, get_jwt_identity # type:ignore
from controllers.auth_controller import register_user, login_user, profile_user
#voy a importar User de model
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user(request.json)

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user(request.json)

@auth_bp.route('/profile', methods=['GET'])
def profile():
    return profile_user()
