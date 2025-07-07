from flask import jsonify # type:ignore
from models.trip import Trip
from models.user import User
from extensions import db # type:ignore
import jwt # type:ignore
from flask import current_app as app, request # type:ignore

def save_trip(data):
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    try:
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    trip = Trip(
        user_id=user_id,
        stopped_time=data["stopped_time"],
        moving_time=data["moving_time"],
        suitcase_count=data["suitcase_count"],
        total=data["total"]
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify({"message": "Trip saved"}), 201
