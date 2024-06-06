# from app import db
from __main__ import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True
    )
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    flagged = db.Column(db.Boolean, default=False)
