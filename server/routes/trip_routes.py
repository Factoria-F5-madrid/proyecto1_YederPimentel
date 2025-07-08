from flask import Blueprint, request
from controllers.trip_controller import save_trip, get_trips
from flask_jwt_extended import jwt_required

trip_bp = Blueprint('trip', __name__)

@trip_bp.route('', methods=['POST'])  # URL: /api/trips
@jwt_required()
def trip():
    data = request.json
    return save_trip(data)

@trip_bp.route('/trip', methods=['GET'])  # ✅ nueva ruta
@jwt_required()
def get_user_trips():
    return get_trips()
