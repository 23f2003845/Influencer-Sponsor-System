# from app import db
from __main__ import db


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(10), default="private")
    goals = db.Column(db.Integer, nullable=False)
    advertisements = db.relationship("advertisement", backref="campaign")
    sponsor = db.Column(db.Integer, db.ForeignKey("sponsor.id"), nullable=False)
    flagged = db.Column(db.Boolean, default=False)
