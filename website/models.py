from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startdate = db.Column(db.DateTime)
    enddate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    members = db.relationship('Member')
    availabilities = db.relationship('Availability')




