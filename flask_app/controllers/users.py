from msilib.schema import PublishComponent
from re import L
from turtle import pu
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.car import Car

@app.route('/')
def login():
    if 'id_user' in session:
        return redirect('/dashboard')
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'id_user' in session:
        data = { "id": session['id_user'] }
        listings = Car.show_all()
        logged_user = User.get_user({"id": session['id_user']})
        return render_template("dash.html", listings=listings, logged_user=logged_user)
    return redirect('/')

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register/success', methods=['POST'])
def registered():
    if not User.register_valid(request.form):
        return redirect('/register')
    hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hash
    }
    user_id = User.create(data)
    session['id_user'] = user_id
    return redirect('/dashboard')

@app.route('/login/success', methods=['POST'])
def logged():
    data = {
        "email": request.form['email']
    }
    user_db = User.get_email(data)
    if not user_db:
        flash("Email or Password invalid")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash("Email or Password invalid")
        return redirect('/')
    session['id_user'] = user_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

