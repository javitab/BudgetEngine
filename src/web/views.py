from decimal import Decimal
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
    return render_template("home.html")

@views.route('/accts', methods=['GET','POST'])
@login_required
def accts():
    accountid = request.args.get('acct')
    acctedit = request.args.get('acctedit')
    acctid_post = request.form.get('acctid_post')
    acctname_post = request.form.get('acctname_post')
    acctinst_post = request.form.get('acctinst_post')
    acctnumber_post = request.form.get('acctnumber_post')
    acctrouting_post = request.form.get('acctrouting_post')
    acctlowbal_post = request.form.get('acctlowbal_post')
    acctstartbalance_post = request.form.get('acctstartbalance_post')

    user=current_user

    if accountid!='' or accountid!=None:
        try:
            acct=Acct.objects.get(id=ObjectId(accountid))
            ptx=acct.active_ptx_log_id.posted_txs
        except:
            acct=[]
            ptx=[]


    if request.method == 'POST':
        print(accountid)
        if acctedit=='true' and accountid!=None:
            try:
                acct.account_display_name=acctname_post
                acct.bank_name=acctinst_post
                acct.bank_account_number=acctnumber_post
                acct.bank_routing_number=acctrouting_post
                acct.low_balance_alert=acctlowbal_post
                acct.save()
            except Exception as e:
                flash('Error updating account', category='error')
                print(e)
        if acctedit=='true' and accountid==None:
            try:
                newacct=Acct(
                    account_display_name=acctname_post,
                    bank_name=acctinst_post,
                    bank_account_number=acctnumber_post,
                    bank_routing_number=acctrouting_post,
                    low_balance_alert=acctlowbal_post,
                    current_balance=acctstartbalance_post
                )
                newacct.save()
                newPtxLog=PtxLog()
                newPtxLog.save()
                newacct.history_ptx_log_ids.append(newPtxLog.id)
                newacct.active_ptx_log_id=newPtxLog.id
                newacct.save()
                user.acctIds.append(newacct.id)
                user.save()
            except Exception as e:
                flash('Error creating account', category='error')
                print(e)


    try:
        print(
                "_id: ", acct.id,
                "Display Name: ", acct.account_display_name,
                "Institution: ", acct.bank_name,
                "Account Number: ", acct.bank_account_number,
                "Routing Number: ", acct.bank_routing_number,
                "Low Balance: ", acct.low_balance_alert
            )
    except: pass

    if acct==[]:
        currUser=User.objects.get(id=current_user.id)
        accts=currUser.acctIds
        for i in accts:
            acct=i
        ptx=acct.active_ptx_log_id.posted_txs

    return render_template("accts.html", acct=acct, user=user, ptx=ptx, acctedit=acctedit, projs=acctProjDict(acct_id=acct.id))

@views.route('/profile')
def profile():

    declareGetArgs=['message']

    GETargs=getArgs(declareGetArgs)

    return render_template("profile.html", message=GETargs.message)

@views.route('/newtx', methods=['GET','POST'])
@login_required
def newtx():
    accountid = request.args.get('acct')
    txtype_arg = request.args.get('txtype_arg')
    txtype_post = request.form.get('txtype_post')
    typeid_arg = request.args.get('typeid_arg')
    typeid_post = request.form.get('typeid_post')
    txamount_post = request.form.get('txamount_post')
    txdebit_post = request.form.get('txdebit_post')
    txdate_post = request.form.get('txdate_post')
    txmemo_post = request.form.get('txmemo_post')

    user=current_user

    if accountid != None:
        acct=Acct.objects.get(id=ObjectId(accountid))
        ptx=acct.active_ptx_log_id.posted_txs
    else:
        acct=[]
        ptx=[]

    try: txtype_post
    except NameError: txtype_post=None
    try: txtype_arg
    except NameError: txtype_arg=None
    if txtype_post != None:
        txtype_arg=None

    ###
    ### Determining which method of txtype identification to use
    ###

    if txtype_arg!=None:
        if txtype_arg=="exp":
            txtype="Expense"
        elif txtype_arg=="rev":
            txtype="Revenue"
        elif txtype_arg=="adhoc":
            txtype="AdHoc"
    if txtype_post=="Expense":
        txtype="Expense"
    elif txtype_post=="Revenue":
        txtype="Revenue"
    elif txtype_post=="AdHoc":
        txtype="AdHoc"

    ###
    ### Getting typeid options based on txtype input
    ###

    if txtype=="Expense":
        typeid_options=acct.exp_ids
    elif txtype=="Revenue":
        typeid_options=acct.rev_ids
    elif txtype=="AdHoc":
        typeid_options=[]

    ###
    ### Determining which method of typeid identification to use
    ###
    
    try: typeid_arg
    except NameError: typeid_arg=None
    try: typeid_post
    except NameError: typeid_post=None

    if typeid_post!=None:
        typeid_arg=None
        typeid=typeid_post
    else:
        typeid=typeid_arg

    if txtype!=None and typeid!=None:
        if txtype=="Expense":
            txTypeData=Exp.objects.get(id=typeid)
        elif txtype=="Revenue":
            txTypeData=Rev.objects.get(id=typeid)
        elif txtype=="AdHoc":
            txTypeData=None
    else:
        txTypeData=None

    ###
    ### If all values are present and vaild, write transaction to PtxLog
    ###

    ### Prepare and validate input data
    try:
        try:
            postDate=convDate(txdate_post)
        except:
            raise Exception("Invalid date format. Please use YYYY-MM-DD.")

        try:
            if txtype=="Expense":
                postMemo=Exp.objects.get(id=typeid).display_name
            if txtype=="Revenue":
                postMemo=Rev.objects.get(id=typeid).display_name
            if txtype=="AdHoc":
                postMemo=txmemo_post
        except:
            raise Exception("Memo invalid.")

        try:
            postAmount=Decimal(txamount_post)
        except:
            raise Exception("Amount invalid.")

        try:
            if txtype=="AdHoc" and txdebit_post=="on": postTxType="debit"
            if txtype=="AdHoc" and txdebit_post!="on": postTxType="credit"
            if txtype=="Expense": postTxType="debit"
            if txtype=="Revenue": postTxType="credit"
        except:
            raise Exception("Transaction type invalid.")

        try:
            if txtype=="AdHoc":
                postAdHoc=True
            else:
                postAdHoc=False
        except:
            raise Exception("AdHoc invalid.")
        
        try:
            if postTxType=="debit": postBalance=acct.current_balance-postAmount
            if postTxType=="credit": postBalance=acct.current_balance+postAmount
        except:
            raise Exception("Balance invalid.")

    except:
       flash("Please fill in missing values before clicking submit.", category="warning")

    # Attempt to write tx to PtxLog
    try:
        if (postDate!=None and postMemo!=None and postAmount!=None and postTxType!=None and postAdHoc!=None and postBalance!=None):
            ptx.create(
                txID=ObjectId(),
                date=postDate,
                memo=postMemo,
                amount=postAmount,
                tx_type=postTxType,
                ad_hoc=postAdHoc,
                balance=postBalance
            )
            ptx.save()
            acct.current_balance=postBalance
            acct.save()
            if txtype=="Expense":
                exp=Exp.objects.get(id=typeid)
                exp.last_posted_date=postDate
                exp.save()
            if txtype=="Revenue":
                rev=Rev.objects.get(id=typeid)
                rev.last_posted_date=postDate
                rev.save()
            flash("Transaction successfully added.", category="success")
            return render_template("accts.html", acct=acct, user=user, ptx=ptx)
    except Exception as e:
        flash("Unable to write transaction to database. Please try again.", category="danger")
        print(e)

    return render_template("newtx.html", acct=acct, user=user, ptx=ptx, txtype=txtype, typeid=typeid, typeid_options=typeid_options, txTypeData=txTypeData)

@views.route('/expense', methods=['GET','POST'])
@login_required
def expense():
    accountid = request.args.get('acct')
    expid_arg = request.args.get('expid_arg')
    expid_post = request.form.get('expid_post')
    dispname_arg = request.args.get('dispname_arg')
    dispname_post = request.form.get('dispname_post')
    amount_arg = request.args.get('amount_arg')
    amount_post = request.form.get('amount_post')
    frequency_arg = request.args.get('frequency_arg')
    frequency_post = request.form.get('frequency_post')
    start_date_arg = request.args.get('start_date_arg')
    start_date_post = request.form.get('start_date_post')
    end_date_arg = request.args.get('end_date_arg')
    end_date_post = request.form.get('end_date_post')

    ###
    ### Evaluating arguments received
    ###

    user=current_user

    if accountid!=None:
        acct=Acct.objects.get(id=accountid)
        ptx=acct.active_ptx_log_id.posted_txs
    if expid_post!=None:
        expid=expid_post
        expid_arg=None
    if expid_arg!=None:
        expid=expid_arg
    if expid_arg==None and expid_post==None:
        expid=None
    

    if dispname_post!=None:
        dispname_arg=None
        dispname=dispname_post
    elif dispname_arg!=None:
        dispname=dispname_post
    
    if amount_post!=None:
        amount_arg=None
        amount=amount_post
    elif amount_arg!=None:
        amount=amount_post

    if frequency_post!=None:
        frequency_arg=None
        frequency=frequency_post
    elif frequency_arg!=None:
        frequency=frequency_post
    
    if start_date_post!=None:
        start_date_arg=None
        start_date=start_date_post
    elif start_date_arg!=None:
        start_date=start_date_post
    
    if end_date_post!=None:
        end_date_arg=None
        end_date=end_date_post
    elif end_date_arg!=None:
        end_date=end_date_post
    try:
        if end_date=="": end_date=None
    except:
        end_date=None

    if expid=="":
        exp=None
    elif expid!=None:
        try:
            exp=Exp.objects.get(id=expid)
        except:
            exp=None
            flash("Unable to create object.", category="warning")

    try:
        if (dispname!=None and amount!=None and frequency!=None and start_date!=None):
            if (expid!=""):
                print("expid: ",type(expid),"dispname: ",dispname,"amount: ",amount,"frequency: ",frequency,"start_date: ",start_date,"end_date: ",end_date)
                try:
                    exp=Exp.objects.get(id=expid)
                    exp.display_name=dispname
                    exp.amount=amount
                    exp.frequency=frequency
                    exp.start_date=start_date
                    if end_date!=None: exp.end_date=end_date
                    exp.save()
                except:
                    flash("Unable to update existing exp object.", category="error")
            if (expid==""):
                exp=Exp(display_name=dispname, amount=amount, frequency=frequency, start_date=start_date)
                exp.save()
                acct.exp_ids.append(exp.id)
                acct.save()
                print("exp.id: ",exp.id,"exp.display_name: ",exp.display_name,"exp.amount: ",exp.amount,"exp.frequency: ",exp.frequency,"exp.start_date: ",exp.start_date,"exp.end_date: ",exp.end_date)
    except:
        flash("Ensure all fields are filled in before submitting.", category="warning")

    try:
        exp
    except NameError: exp=None

    return render_template("expense.html", exp=exp, acct=acct, user=user, ptx=ptx, expid=expid)

    
@views.route('/revenue', methods=['GET','POST'])
@login_required
def revenue():
    accountid = request.args.get('acct')
    revid_arg = request.args.get('revid_arg')
    revid_post = request.form.get('revid_post')
    dispname_arg = request.args.get('dispname_arg')
    dispname_post = request.form.get('dispname_post')
    amount_arg = request.args.get('amount_arg')
    amount_post = request.form.get('amount_post')
    frequency_arg = request.args.get('frequency_arg')
    frequency_post = request.form.get('frequency_post')
    start_date_arg = request.args.get('start_date_arg')
    start_date_post = request.form.get('start_date_post')
    end_date_arg = request.args.get('end_date_arg')
    end_date_post = request.form.get('end_date_post')

    ###
    ### Evaluating arguments received
    ###

    user=current_user

    if accountid!=None:
        acct=Acct.objects.get(id=accountid)
        ptx=acct.active_ptx_log_id.posted_txs
    if revid_post!=None:
        revid=revid_post
        revid_arg=None
    if revid_arg!=None:
        revid=revid_arg
    if revid_arg==None and revid_post==None:
        revid=None
    

    if dispname_post!=None:
        dispname_arg=None
        dispname=dispname_post
    elif dispname_arg!=None:
        dispname=dispname_post
    
    if amount_post!=None:
        amount_arg=None
        amount=amount_post
    elif amount_arg!=None:
        amount=amount_post

    if frequency_post!=None:
        frequency_arg=None
        frequency=frequency_post
    elif frequency_arg!=None:
        frequency=frequency_post
    
    if start_date_post!=None:
        start_date_arg=None
        start_date=start_date_post
    elif start_date_arg!=None:
        start_date=start_date_post
    
    if end_date_post!=None:
        end_date_arg=None
        end_date=end_date_post
    elif end_date_arg!=None:
        end_date=end_date_post
    try:
        if end_date=="": end_date=None
    except:
        end_date=None

    if revid=="":
        rev=None
    elif revid!=None:
        try:
            rev=Rev.objects.get(id=revid)
        except:
            rev=None
            flash("Unable to create object.", category="warning")

    try:
        if (dispname!=None and amount!=None and frequency!=None and start_date!=None):
            if revid!="":
                try:
                    rev=Rev.objects.get(id=revid)
                    rev.display_name=dispname
                    rev.amount=amount
                    rev.frequency=frequency
                    rev.start_date=start_date
                    if end_date!=None: rev.end_date=end_date
                    rev.save()
                except:
                    flash("Unable to update existing rev object.", category="error")
            if revid=="":
                try:
                    rev=Rev(display_name=dispname, 
                    amount=amount, 
                    frequency=frequency, 
                    start_date=start_date)
                    rev.save()
                    acct.rev_ids.append(rev.id)
                    acct.save()
                except:
                    flash("Unable to create new rev object.", category="warning")

    except:
        flash("Ensure all fields are filled in before submitting.", category="warning")

    try:
        rev
    except NameError: rev=None

    return render_template("revenue.html", rev=rev, acct=acct, user=user, ptx=ptx, revid=revid)

