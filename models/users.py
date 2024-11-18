
from flask_login import UserMixin
from database.db import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    
    # orders = db.relationship('Order', backref='users')
    # cart = db.relationship('CartItem', backref='users')
