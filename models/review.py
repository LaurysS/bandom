from database.db import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255))
