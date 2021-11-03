# burgers.py
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User



bcrypt = Bcrypt(app)

#Login and Registration
@app.route("/")
def index():

    return render_template("index.html")

#------------------------------------------------------------------
#Login/Register classes
@app.route('/register_email', methods=["POST"])
def register_email():

    if not User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    
    email_check = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email_check)

    if user_in_db:
        flash("Email is already registered")
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.save(data)

    session['user_id'] = user_id

    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')


@app.route('/validate_email', methods=["POST"])
def validate_email():

    data = { "email_login" : request.form["email_login"] }
    user_in_db = User.check_existing_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password_login']):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

#Next two classes are used to see if the user has logged out and it clears the session info
@app.route("/dashboard")
def success_login():
    logged_in = bool(session)

    if not logged_in:
        return redirect('/')

    data = {
        'id': session['user_id']
    }

    user_name = User.get_one(data)

    return render_template("dashboard.html", user_name=user_name)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
