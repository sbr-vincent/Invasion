from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import pie
from flask_app import app
from flask_bcrypt import Bcrypt
import re	

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.magazines = []
    # Now we use class methods to query our database

#A function that combines the first and last name of the user using the User class
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

#Gets everything for one id in users table
    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL('pyderby_schema').query_db(query, user_id)
        users = []
        for user in results:    
            users.append( cls(user) )
        return users[0]

#Saves  a user to the users table           
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL('pyderby_schema').query_db( query, data )
    
#Deletes  a user from the users table 
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('pyderby_schema').query_db( query, data )

#Updates an entry for a user from the users table 
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('pyderby_schema').query_db( query, data)

#Gets all the recipes available with users info
    @classmethod
    def get_user_pies(cls, id):
        # query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.users_id WHERE users.id = %(id)s"
        query = "SELECT * FROM users LEFT JOIN votes ON users.id = votes.user_id LEFT JOIN pies ON pies.id = votes.pie_id WHERE users.id = %(id)s;"

        results = connectToMySQL('pyderby_schema').query_db(query, id)

        users = []
        for user in results:
            users.append(user)
        return users

    #Used for login to see if the email exists in database
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("pyderby_schema").query_db(query,data)
        # Didn't find a matching user

        if not result:
            return False

        return cls(result[0])

    
    @classmethod
    def check_existing_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email_login)s;"
        result = connectToMySQL("pyderby_schema").query_db(query,data)
        # Didn't find a matching user
        if not result:
            return False
        return cls(result[0])

#Validates if the login for the user
    @staticmethod
    def validate_user( login ):
        is_valid = True

        if len(login['first_name']) == 0:
            flash("First name can't be blank!")
            is_valid = False
        elif len(login['first_name']) < 3:
            flash("First name is too short!")
            is_valid = False
        elif not str.isalpha(login['first_name']):
            flash("Please use letters only!")
            is_valid = False

        if len(login['last_name']) == 0:
            flash("Last name can't be blank!")
            is_valid = False
        elif len(login['last_name']) < 3:
            flash("Last name is too short!")
            is_valid = False
        elif not str.isalpha(login['last_name']):
            flash("Please use letters only!")
            is_valid = False

        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(login['email']): 
            flash("Invalid email address!")
            is_valid = False
        
        if len(login['password']) == 0:
            flash("Password can't be blank!")
            is_valid = False
        elif len(login['password']) < 8:
            flash("Password is too short!")
            is_valid = False

        if login['password']  != login['password_confirm']:
            flash("Passwords do not match!")
            is_valid = False

        return is_valid

    @staticmethod
    def update_validate_user( update ):
        is_valid = True

        if len(update['fname']) == 0:
            flash("First name can't be blank!")
            is_valid = False
        elif len(update['fname']) < 3:
            flash("First name is too short!")
            is_valid = False
        
        if len(update['lname']) == 0:
            flash("Last name can't be blank!")
            is_valid = False
        elif len(update['lname']) < 3:
            flash("Last name is too short!")
            is_valid = False

        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(update['email']): 
            flash("Invalid email address!")
            is_valid = False

        return is_valid