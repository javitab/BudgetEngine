from bson import ObjectId
from flask import Blueprint,render_template, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..BudgetEngine.user import User

admin = Blueprint('admin', __name__)

@admin.route('/users', methods=['GET', 'POST'])
def users():
    userid = request.args.get('user')
    userid_post = request.form.get('userid_post')
    email_post = request.form.get('email_post')
    first_name_post = request.form.get('first_name_post')
    last_name_post = request.form.get('last_name_post')
    password_1_post = request.form.get('password_1_post')
    password_2_post = request.form.get('password_2_post')
    timezone_post = request.form.get('timezone_post')

    ###
    ### Evaluate variables
    ###

    try:
        if password_1_post==password_2_post:
            password=generate_password_hash(password_1_post)
        else:
            flash('Passwords do not match')
    except: pass
    

    try:
        users=User.objects()
    except:
        flash("Error getting users.", category='error')

    if userid=="" or userid==None:
        user=None
    elif userid!="" or userid!=None:
        user=User.objects.get(id=ObjectId(userid))
    
    try: user
    except NameError:
        user=None
    
    try: users
    except NameError:
        users=None

    return render_template("users.html", userid=userid, user=user, users=users)