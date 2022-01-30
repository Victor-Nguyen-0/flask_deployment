from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "private_wall_schema"
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users ORDER BY first_name;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def is_valid(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >=1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Not a valid email.", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if re.search('[A-Z]', user['password']) is None:
            flash("Password must contain a capital letter.", "register")
            is_valid = False
        if re.search('[0-9]', user['password']) is None:
            flash("Password must contain a digit.", "register")
            is_valid = False
        if re.search('[@$!%*#?&]', user['password']) is None:
            flash("Password must contain a special character.", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid

# PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$')


# if not PASSWORD_REGEX.match(user['password']):
#     flash("Password must be between 8-16 characters with capital/lowercase letters, a number, and a special character.", "register")
#     is_valid = False