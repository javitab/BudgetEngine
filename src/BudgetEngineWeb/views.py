from pprint import PrettyPrinter
from textwrap import indent
from flask import Blueprint,render_template,request,flash
from flask_login import login_required, current_user
from bson.json_util import dumps
import pandas as pd
import json
from bson import ObjectId, json_util
import BudgetEngine as be
import pprint
views = Blueprint('views', __name__)

@views.route('/')
def home():
    accts = be.listCollection("accounts")
    accts = be.convDf(accts)
    accts = list(accts.itertuples(index=True, name=None))
    return render_template("home.html", accts=accts)

@views.route('/accts', methods=['GET','POST'])
def accts():
    account = request.args.get('acct')
    if account != None:
        acct=be.acct(account).name
    else:
        acct=account
    if request.method == 'POST':
        NewTxMemo=request.form.get('NewTxMemo')
        NewTxAmount=float(request.form.get('NewTxAmount'))
        NewTxDate=request.form.get('NewTxDate')
        NewTxType=request.form.get('NewTxType')
        NewTxAdhoc=request.form.get('NewTxAdhoc')
        if NewTxType == 'credit':
            NewTxBalance=round(acct.CurrBalance+NewTxAmount,2)
        if NewTxType == 'debit':
            NewTxBalance=round(acct.CurrBalance-NewTxAmount,2)
        print(NewTxMemo,NewTxAmount,NewTxDate,NewTxType,NewTxAdhoc)
        NewTxAdhoc=bool(NewTxAdhoc=='True')
        be.writeTx(acct.name,NewTxType,NewTxDate,NewTxAmount,NewTxMemo,NewTxAdhoc,NewTxBalance)
    accts = be.listCollection("accounts")
    accts = be.convDf(accts)
    accts = list(accts.itertuples(index=True, name=None))
    output = be.getTxData(account)
    txdf = be.mongoArrayDf(output,'PostedTxs')
    txdf = list(txdf.itertuples(index=True, name=None))
    return render_template("accts.html", acct=acct, txdata=txdf, accts=accts)

@views.route('/rev', methods=['GET', 'POST'])
def rev():
    accts = be.listCollection("accounts")
    accts = be.convDf(accts)
    accts = list(accts.itertuples(index=True, name=None))
    if request.method == 'POST':
        NewRevName=request.form.get('NewRevName')
        NewRevInst=request.form.get('NewRevInst')
        NewRevAcct=request.form.get('NewRevAcct')
        NewRevAmount=request.form.get('NewRevAmount')
        NewRevFreq=request.form.get('NewRevFreq')
        NewRevStartDate=request.form.get('NewRevStartDate')
        NewRevEnd=request.form.get('NewRevEnd')

        if len(NewRevName) < 1:
            flash('NewRevName must be greater than 1 characters', category='error')
        elif len(NewRevInst) < 1:
            flash('NewRevInst must be greater than 1 characters', category='error')
        elif len(NewRevAcct) < 1:
            flash('NewRevAcct must be greater than 1 characters', category='error')
        elif len(NewRevAmount) < 1:
            flash('NewRevAmount must be greater than 1 characters', category='error')
        elif len(NewRevFreq) < 1:
            flash('NewRevFreq must be greater than 1 characters', category='error')
        elif len(NewRevStartDate) < 1:
            flash('NewRevStartDate must be greater than 1 characters', category='error')
        elif len(NewRevEnd) < 1:
            flash('NewRevEnd must be greater than 1 characters', category='error')
        else: 
            flash('Revenue Created!', category='success')
            print(NewRevName, NewRevInst, NewRevAcct, NewRevAmount, NewRevFreq, NewRevStartDate, NewRevEnd)
    return render_template("new-rev.html", accts=accts)