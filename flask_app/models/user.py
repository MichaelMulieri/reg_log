from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# from flask_bcrypt import Bcrypt        
# bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile((r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'))
# PASSWORD_REGEX = re.compile((r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$'))

class User:
    def __init__(self, data):
        self.id = data['id'] 
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.birthdate = data['birthdate']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, birthdate, email, password) VALUES \
            (%(first_name)s, %(last_name)s, %(birthdate)s, %(email)s, %(password)s);"
        return connectToMySQL('reg_log').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('reg_log').query_db(query)
        users =[]
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('reg_log').query_db(query, data)
        if len(results) <1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('reg_log').query_db(query, data)
        return cls(results[0])
        
    @staticmethod
    def validate_user(user_data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('reg_log').query_db(query, user_data)
        print(results)
        if len(results) >=1:
            flash("Email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user_data['first_name']) < 2:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(user_data['last_name']) < 2:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if user_data['birthdate'] > "2012-1-1":
            flash("You must be at least 10 years old to register")
            is_valid = False  
        # if not PASSWORD_REGEX.match(user_data)['password']:
        #     flash("Invalid Password")
        #     is_valid = False
        if len(user_data['password']) < 8:
            flash ("Password must be at least 8 characters")
            is_valid = False
        if user_data['password'] != user_data['confirm_password']:
            flash('Passwords do not match')
            is_valid = False
        return is_valid




        

        