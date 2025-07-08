from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from models.trip import Trip
from extensions import db

@jwt_required()
def save_trip(data):
    current_user_id = get_jwt_identity()

    stopped_time = data.get("tiempo_parado", 0)
    moving_time = data.get("tiempo_movimiento", 0)
    suitcase_count = data.get("maletas", 0)
    lluvia = data.get("lluvia", False)
    evento = data.get("evento", False)

    # Tarifas base
    tarifa_parado = 0.02
    tarifa_movimiento = 0.05
    precio_maleta = 1.0

    # Multiplicador por condiciones especiales
    multiplicador = 1.0
    if lluvia:
        multiplicador *= 1.25
    if evento:
        multiplicador *= 1.5

    # Cálculo de tarifa total
    tarifa_base = (stopped_time * tarifa_parado) + (moving_time * tarifa_movimiento)
    tarifa_maletas = suitcase_count * precio_maleta
    total = (tarifa_base + tarifa_maletas) * multiplicador

    trip = Trip(
        user_id=current_user_id,
        stopped_time=stopped_time,
        moving_time=moving_time,
        suitcase_count=suitcase_count,
        total=round(total, 2)
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify({
        "message": "Viaje guardado correctamente",
        "total": round(total, 2)
    }), 201

@jwt_required()
def get_trips():
    current_user_id = get_jwt_identity()
    trips = Trip.query.filter_by(user_id=current_user_id).order_by(Trip.timestamp.desc()).all()

    trip_list = [
        {
            "id": trip.id,
            "stopped_time": trip.stopped_time,
            "moving_time": trip.moving_time,
            "suitcase_count": trip.suitcase_count,
            "total": trip.total,
            "timestamp": trip.timestamp.isoformat()
        }
        for trip in trips
    ]

    return jsonify(trip_list), 200
