from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(), default=func.now())
    date_updated = db.Column(db.DateTime(), onupdate=func.now())
    score = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return f"Account({self.id}, {self.username}, {self.score}, {self.date_created}, {self.date_updated or 'Never'})"