
from __main__ import db


class Influencer(db.Model):
    __tablename__ = "influencer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    niche = db.Column(db.String(255), nullable=False)
    advertisements = db.relationship("Advertisement", backref="influencer")
