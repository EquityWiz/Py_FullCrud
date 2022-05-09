from unittest import result
from winreg import QueryInfoKey
from flask import flash, request, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.make = data['make']
        self.model = data['model']
        self.price = data['price']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_purchase = []
    @classmethod
    def save(cls, data):
        data = {
        "make": request.form['make'],
        "description": request.form['description'],
        "model": request.form['model'],
        "price": request.form['price'],
        "year": request.form['year'],
        "user_id": session['id_user']
    }
        query = "INSERT INTO cars ( make , description , model , price , year , user_id , created_at , updated_at ) VALUES ( %(make)s , %(description)s , %(model)s , %(price)s , %(year)s , %(user_id)s , NOW() , NOW() );"
        return connectToMySQL('register').query_db(query, data)
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        result = connectToMySQL('register').query_db(query, data)
        if result:
            temp_sight = cls(result[0])
            temp_sight.publisher = user.User(result[0])
            return temp_sight
    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET make = %(make)s , description = %(description)s , model = %(model)s , price = %(price)s , year = %(year)s WHERE id = %(id)s;"
        connectToMySQL('register').query_db(query, data)
        return data['id']
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s"
        connectToMySQL('register').query_db(query, data)
    @classmethod
    def show_all(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        result = connectToMySQL('register').query_db(query)
        cars = []
        if result:
            for row in result:
                temp_car = cls(row)
                publisher_data = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }
                temp_car.publisher = user.User(publisher_data)
                cars.append(temp_car)
        return cars
    @classmethod
    def get_car_with_user(cls, data):
        query = "SELECT * FROM cars LEFT JOIN purchases ON purchases.car_id = cars.id LEFT JOIN users ON purchases.user_id = users.id WHERE cars.id = %(id)s;"
        result = connectToMySQL('register').query_db(query, data)
        car = cls(result[0])
        for row in result:
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            car.user_purchase.append(user.User(user_data))
        return car
    @staticmethod
    def form_valid(user):
        is_valid = True
        if not len(user['make']) > 1:
            flash('Make is invalid.')
            is_valid = False
        if not len(user['description']) > 1:
            flash('Tell us more.')
            is_valid = False
        if not len(user['model']) > 1:
            flash('Model is invalid.')
            is_valid = False
        if not int(user['price']) > 0 :
            flash('Minimum of $1 price required.')
            is_valid = False
        if not int(user['year']) > 0 :
            flash('Year is invalid.')
            is_valid = False
        return is_valid