from database.db import db

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    products = db.relationship('OrderProduct', backref='order')
    
    def __repr__(self):
        return f'<Order {self.id}>'