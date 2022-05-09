from msilib.schema import PublishComponent
from re import L
from turtle import pu
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.car import Car

@app.route('/new')
def new():
    if 'id_user' not in session:
        return redirect('/')
    logged_user = User.get_user({"id": session['id_user']})
    return render_template("new.html", logged_user=logged_user)

@app.route('/edit/<int:id>')
def edit(id):
    if 'id_user' in session:
        data = { "id": id }
        car = Car.get_one(data)
        logged_user = User.get_user({"id": session['id_user']})
        if not car.user_id != session['id_user']:
            return render_template("edit.html", car=car, logged_user=logged_user)
    return redirect("/dashboard")

@app.route('/delete/<int:id>')
def delete(id):
    data = {"id": id}
    Car.delete(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def view(id):
    if 'id_user' in session:
        logged_user = User.get_user({"id": session['id_user']})
    data = { "id": id }
    car = Car.get_one(data)
    return render_template("show.html", car=car, logged_user=logged_user)

@app.route('/purchases')
def purchases():
    user = User.get_user_with_car({"id": session['id_user']})
    return render_template('purchase.html', user=user)

@app.route('/purchase/<int:id>')
def purchase(id):
    data = {
        "user_id": session['id_user'],
        "car_id": id
    }
    User.purchase(data)
    return redirect('/purchases')

# # # # Action Routes-----------------------------------------------------------------------------

@app.route('/new/success', methods=['POST'])
def new_added():
    if Car.form_valid(request.form):
        car_id = Car.save(request.form)
        return redirect('/dashboard')
    return redirect('/new')

@app.route('/edit/success', methods=['POST'])
def updated():
    if Car.form_valid(request.form):
        car_id = Car.update(request.form)
        return redirect(f"/show/{car_id}")
    car_id = request.form['id']
    return redirect(f"/edit/{car_id}")

