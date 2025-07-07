from flask import Blueprint, request # type:ignore
from controllers.trip_controller import save_trip

trip_bp = Blueprint("trip", __name__)

@trip_bp.route("/save", methods=["POST"])
def save():
    return save_trip(request.json)
