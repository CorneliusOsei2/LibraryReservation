
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Day(db.Model):

    __tablename__ = "days"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)
    timeslots = db.relationship("Time", cascade="delete")

    def serialize(self):

        return [
            slot for slot in self.timeslots if slot.booked == False
        ]

class Time(db.Model):
    __tablename__ = "times"
    start = db.Column(db.String, nullable=False)
    booked = db.Column(db.Boolean)
    

class User(db.Model):
    pass