from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from database.db import db


from models.cart import Cart
from models.prekes import Product
from models.users import User
from models.cartitems import CartItem
from models.review import Review
from controler.users_manager import user_bp


app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix ='/user')

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{os.path.join(base_dir, "database", "store.db")}'
app.config['SECRET_KEY'] = 'nemokamai'


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Sėkmingai prisijungėte!', 'success')
            return redirect(url_for('product_list_all'))
        else:
            flash('Neteisingi prisijungimo duomenys.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registracija sėkminga!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Klaida bandant registruotis: {str(e)}")
            flash('Klaida: ' + str(e), 'danger')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Atsijungėte.', 'info')
    return redirect(url_for('login'))



@app.route('/products')
def product_list_all():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)


