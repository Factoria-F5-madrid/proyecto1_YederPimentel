from flask import Blueprint, request # type:ignore
from controllers.trip_controller import save_trip
from flask_jwt_extended import jwt_required # type:ignore

trip_bp = Blueprint('trip', __name__)

@trip_bp.route('/trip', methods=['POST'])
@jwt_required()
def trip():
    data = request.json
    return save_trip(data)
