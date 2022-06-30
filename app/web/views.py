from pprint import PrettyPrinter
from textwrap import indent
from flask import Blueprint,render_template,request
from bson.json_util import dumps
import pandas as pd
import json
from bson import ObjectId, json_util
import bb
import pprint
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/accts')
def accts():
    account = request.args.get('acct')
    output = bb.t.getTxData(account)
    txdf = bb.d.mongoArrayDf(output,'PostedTxs')
    txdf = list(txdf.itertuples(index=True, name=None))
    return render_template("accts.html", txdata=txdf)