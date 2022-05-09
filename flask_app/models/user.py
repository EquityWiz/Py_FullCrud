import queue
from unittest import result
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models import car
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"
        return connectToMySQL('register').query_db(query, data)
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('register').query_db(query, data)
        if result: 
            return cls(result[0])
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('register').query_db(query, data)
        if result: 
            return cls(result[0])
    @classmethod
    def get_user_with_car(cls, data):
        query = "SELECT * FROM users LEFT JOIN purchases ON purchases.user_id = users.id LEFT JOIN cars ON purchases.car_id = cars.id WHERE users.id = %(id)s;"
        result = connectToMySQL('register').query_db(query, data)
        if result:
            user = cls(result[0])
            if result[0]["cars.id"]:
                for row in result:
                    car_data = {
                        "id": row['cars.id'],
                        "model": row['model'],
                        "make": row['make'],
                        "year": row['year'],
                        "price": row['price'],
                        "description": row['description'],
                        "created_at": row['cars.created_at'],
                        "updated_at": row['cars.updated_at'],
                        "user_id": row['cars.user_id']
                    }
                    user.cars.append(car.Car(car_data))
            return user
    @classmethod
    def purchase(data):
        query = "INSERT INTO purchases ( user_id , car_id ) VALUES ( %(user_id)s , %(car_id)s );"
        return connectToMySQL('register').query_db(query, data)
    @staticmethod
    def register_valid(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email')
            is_valid = False
        if not len(user['first_name']) > 2:
            flash('First name is too short.')
            is_valid = False
        if not len(user['last_name']) > 2:
            flash('Last name is too short.')
            is_valid = False
        if not len(user['password']) > 7:
            flash('Password must be at least 8 characters.')
            is_valid = False
        pot_email = { "email": user['email'] }
        if User.get_email(pot_email):
            flash('Email Already Taken')
            is_valid = False
        if not user['password'] == user['confirm']:
            flash('Passwords do not match!')
            is_valid = False
        return is_valid