from bson import ObjectId
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user

from ..BudgetEngine.projection import Projection
from ..BudgetEngine.acct import Acct,PtxLog
from ..BudgetEngine.exp import Exp
from ..BudgetEngine.rev import Rev
from ..BudgetEngine.user import User
from ..BudgetEngine.dtfunc import convDate
from ..BudgetEngine.datafunc import acctProjDict

from .webfunc import *

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.j2")


@views.route('/profile')
def profile():

    declareVars=['message']
    webGET=getVars(declareVars)['get']

    return render_template("profile.html", message=webGET['message'])

