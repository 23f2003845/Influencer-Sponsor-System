# from app import db
from __main__ import db


class Sponsors(db.Model):
    __tablename__ = "sponsor"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    campaigns = db.relationship("campaign", backref="sponsor")
