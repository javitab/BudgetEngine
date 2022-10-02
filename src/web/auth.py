from bson import ObjectId
from flask import Blueprint,render_template, request, flash,redirect,url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..BudgetEngine.user import User
from ..BudgetEngine.data import *

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    userid = request.form.get('userid')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False


    user = User.objects.get(userid=userid)
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('views.profile'))

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

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
        else: 
            newuser=User(userid=userid,
            email=email,
            first_name=firstName,
            last_name=lastName,
            password=generate_password_hash(password1),
            timezone=timezone)
            newuser.save()
        print(generate_password_hash(password1))

    return render_template("signup.html")