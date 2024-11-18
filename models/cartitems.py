from models.prekes import Product
from database.db import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    # cart = db.relationship('carts', backref=db.backref('cart_items', lazy=True))


    def __repr__(self):
        return f'<CartItem {self.product.name}, Quantity: {self.quantity}>'
