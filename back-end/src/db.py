from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Week(db.Model):
    __tablename__ = "weeks"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    days = db.relationship("Day", cascade="delete")
    

    def serialize_for_week(self):
        return {
            "id": self.id,
            "number": self.number,
            "days": [day.serialize_for_week() for day in self.days]
        }

class Day(db.Model):
    __tablename__ = "days"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey("weeks.id"))
    week = db.relationship("Week", cascade="delete", back_populates="days")
    timeslots = db.relationship("Time", cascade="delete")

    def serialize_for_day(self):

        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "timeslots": [slot.serialize_for_day() for slot in self.timeslots]
        }

    def serialize_for_week(self):

        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
        }

class Time(db.Model):
    __tablename__ = "times"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String, nullable=False)
    booked = db.Column(db.Boolean)
    day_id =  db.Column(db.Integer, db.ForeignKey("days.id"))
    day = db.relationship("Day", cascade="delete")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.String, nullable=True)
    
    def serialize_for_time(self):

        return {
            "id": self.id,
            "start": self.start,
            "booked": self.booked,
            "user": self.user_id
        }

    def serialize_for_day(self):

        return {
            "id": self.id,
            "start": self.start,
            "booked": self.booked
        }
    
    def serialize_for_user(self):

        return {
            "id": self.id,
            "start": self.start,
        }

    
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    booked_times = db.relationship("Time", cascade="delete")
    role = db.Column(db.String, nullable=False)

    def serialize_for_user(self):
        return {
            "id": self.id,
            "booked_times": [time.serialize_for_user() for time in self.booked_times]
        }
    
    def serialize_for_time(self):
        return {
            "id": self.id
        }


class Staff(db.Model):
    __tablename__ = "staffs"
    id = db.Column(db.Integer, primary_key=True)
    booked_times = db.relationship("Time", cascade="delete")
    role = db.Column(db.String, nullable=False)

    def serialize_for_user(self):
        return {
            "id": self.id,
            "booked_times": [time.serialize_for_user() for time in self.booked_times]
        }
    
    def serialize_for_time(self):
        return {
            "id": self.id
        }

class Course(db.Model):
    pass