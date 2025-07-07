from extensions import db # type:ignore
from datetime import datetime

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    stopped_time = db.Column(db.Float, nullable=False)
    moving_time = db.Column(db.Float, nullable=False)
    suitcase_count = db.Column(db.Integer, default=0)
    total = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="trips")
