from app import db
from datetime import datetime

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    class_type = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    allocations = db.relationship('Allocation', backref='car', lazy='dynamic')

    @property
    def is_available(self):
        today = datetime.now().date()
        return not Allocation.query.filter(
            Allocation.car_id == self.id,
            Allocation.start_date <= today,
            Allocation.end_date >= today
        ).first()

    def is_available_between(self, start_date, end_date):
        return not Allocation.query.filter(
            Allocation.car_id == self.id,
            Allocation.start_date <= end_date,
            Allocation.end_date >= start_date
        ).first()

class Allocation(db.Model):
    __tablename__ = 'allocations'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)

    @property
    def status(self):
        today = datetime.now().date()
        if self.start_date > today:
            return "Future"
        elif self.end_date < today:
            return "Past"
        else:
            return "Current"