from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from database.db import db



from models.cart import Cart
from models.prekes import Product
from models.users import User
from models.cartitems import CartItem
from models.review import Review

from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
@login_required
def user_login():
    products = Product.query.all()
    return render_template('user_dashboard.html', product_id=products )


@user_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if product.stock <= 0:
        flash('Prekės nėra sandėlyje.', 'warning')
        return redirect(url_for('product_list_all'))

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += 1  # Padidiname kiekį
    else:
        cart_item = CartItem(product_id=product.id, cart_id=cart.id, quantity=1)
        db.session.add(cart_item)

    product.stock -= 1  # Sumažiname prekių kiekį sandėlyje
    db.session.commit()
    flash('Prekė pridėta į krepšelį.', 'success')
    return redirect(url_for('product_list_all'))

@user_bp.route('/cart')
@login_required
def cart_list():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all() if cart else []
    return render_template('cart.html', cart_items=cart_items)

@user_bp.route('/delete_cart/<int:product_id>', methods=['POST'])
def delete_product(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if cart_item.cart_id != cart.id:
        flash('Neturite teisės pašalinti šios prekės.', 'danger')
        return redirect(url_for('cart'))

    # Grąžiname prekę į sandėlį
    product = Product.query.get(cart_item.product_id)
    product.stock += cart_item.quantity

    db.session.delete(cart_item)
    db.session.commit()
    flash('Prekė pašalinta iš krepšelio.', 'info')
    return redirect(url_for('cart'))

