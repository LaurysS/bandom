from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from database.db import db
from app import app

from models.cart import Cart
from models.prekes import Product
from models.users import User
from models.cartitems import CartItem
from models.review import Review

#gali reiket papildymo
@app.route('/admin')
@login_required
def admin():
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)


@app.route('/admin/add_product', methods=['POST'])
@login_required
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    description = request.form['description']
    new_product = Product(name=name, price=price, stock=stock, description=description)
    try:
        db.session.add(new_product)
        db.session.commit()
        flash('Prekė sėkmingai pridėta!', 'success')
        return redirect(url_for('product_list'))
    except Exception as e:
        db.session.rollback()
        flash('Klaida: ' + str(e), 'danger')

    return render_template('admin_dashboard.html')

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.name = request.form['name']
    product.price = request.form['price']
    product.description = request.form['description']
    db.session.commit()
    flash('Prekė atnaujinta sėkmingai!')
    return redirect(url_for('admin_dashboard.html'))

@app.route('/admin/admin_delete/<int:product_id>', methods=['POST'])
@login_required
def admin_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Prekė pašalinta.')
    return redirect(url_for('admin_dashboard.html'))
