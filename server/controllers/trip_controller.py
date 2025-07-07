from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from models.trip import Trip
from extensions import db

@jwt_required()
def save_trip(data):
    current_user_id = get_jwt_identity()

    trip = Trip(
        user_id=current_user_id,
        stopped_time=data["stopped_time"],
        moving_time=data["moving_time"],
        suitcase_count=data["suitcase_count"],
        total=data["total"]
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify({"message": "Trip saved"}), 201
