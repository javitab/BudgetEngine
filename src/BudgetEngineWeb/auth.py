from bson import ObjectId
from flask import Blueprint,render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from BudgetEngine import *

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        userid=request.form.get('userid')
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        timezone=request.form.get('timezone')

        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 1 characters', category='error')
        elif len(lastName) < 2:
            flash('Last Name must be greater than 1 characters', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            pass
        else: 
            newuser=u.User.create(userid=userid,email=email,first_name=firstName,last_name=lastName,password=generate_password_hash(password1),timezone=timezone)
            if type(newuser)==ObjectId:
                flash(f'New user created, objectID: {newuser}', category='success')
            else:
                flash(f"User not created: {newuser}", category='error')

    return render_template("signup.html")