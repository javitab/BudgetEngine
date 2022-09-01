from decimal import Decimal
from os import error
from pprint import PrettyPrinter
from textwrap import indent
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user
from BudgetEngine.data import *
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/accts', methods=['GET','POST'])
def accts():
    accountid = request.args.get('acct')
    userid = request.args.get('user')
    if accountid != None:
        acct=Acct.objects.get(id=ObjectId(accountid))
        ptx=acct.active_ptx_log_id.posted_txs
    else:
        acct=[]
        ptx=[]
    if userid != None:
        user=User.objects.get(id=ObjectId(userid))
    else:
        user=[]

    return render_template("accts.html", acct=acct, user=user, ptx=ptx)

@views.route('/newtx', methods=['GET','POST'])
def newtx():
    accountid = request.args.get('acct')
    userid = request.args.get('user')
    txtype_arg = request.args.get('txtype_arg')
    txtype_post = request.form.get('txtype_post')
    typeid_arg = request.args.get('typeid_arg')
    typeid_post = request.form.get('typeid_post')
    txamount_post = request.form.get('txamount_post')
    txdebit_post = request.form.get('txdebit_post')
    txdate_post = request.form.get('txdate_post')
    txmemo_post = request.form.get('txmemo_post')

    if accountid != None:
        acct=Acct.objects.get(id=ObjectId(accountid))
        ptx=acct.active_ptx_log_id.posted_txs
    else:
        acct=[]
        ptx=[]
    if userid != None:
        user=User.objects.get(id=ObjectId(userid))
    else:
        user=[]
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
    print("Pre Verify: ",txdate_post,txmemo_post,txamount_post,txdebit_post,typeid,txtype)
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

        try: 
            print("Post-Verify: postDate: ",postDate,"postMemo: ", postMemo, "postAmount: ",postAmount,"postTxType: ", postTxType,"postAdHoc: ", postAdHoc,"postBalance: ", postBalance)
        except:
            raise Exception("Invalid or missing values.")
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
    except:
        pass

    return render_template("newtx.html", acct=acct, user=user, ptx=ptx, txtype=txtype, typeid=typeid, typeid_options=typeid_options, txTypeData=txTypeData)

@views.route('/expense', methods=['GET','POST'])
def expense():
    accountid = request.args.get('acct')
    userid = request.args.get('user')
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

    if accountid!=None:
        acct=Acct.objects.get(id=accountid)
        ptx=acct.active_ptx_log_id.posted_txs
    if userid!=None:
        user=User.objects.get(id=userid)
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
            if (expid!=None):
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
def revenue():
    accountid = request.args.get('acct')
    userid = request.args.get('user')
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

    if accountid!=None:
        acct=Acct.objects.get(id=accountid)
        ptx=acct.active_ptx_log_id.posted_txs
    if userid!=None:
        user=User.objects.get(id=userid)
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