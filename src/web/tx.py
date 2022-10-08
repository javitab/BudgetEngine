from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user
from bson import ObjectId
from decimal import Decimal



from ..BudgetEngine.projection import Projection
from ..BudgetEngine.acct import Acct
from ..BudgetEngine.exp import Exp
from ..BudgetEngine.rev import Rev

from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

tx = Blueprint('tx', __name__)


@tx.route('/new', methods=['GET','POST'])
@login_required
def newtx():
    declareVars=['acct_id','txtype','type_id','tx_amount','tx_debit','tx_date','tx_memo']
    POSTvars=getVars(declareVars,'post')
    GETvars=getVars(declareVars,'get')


    user=current_user

    if GETvars.acct_id != None:
        acct=Acct.objects.get(id=ObjectId(GETvars.acct_id))
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


    ###
    ### Getting typeid options based on txtype input
    ###

    if GETvars.txtype=="exp" or POSTvars.txtype=="exp":
        typeid_options=acct.exp_ids
    elif GETvars.txtype=="rev" or POSTvars.txtype=="rev":
        typeid_options=acct.rev_ids
    elif GETvars.txtype=="adhoc" or POSTvars.txtype=="adhoc":
        typeid_options=[]

    ###
    ### Determining which method of typeid identification to use
    ###
    


    if GETvars.txtype!=None and POSTvars.type_id!=None:
        if GETvars.txtype=="exp":
            txTypeData=Exp.objects.get(id=POSTvars.type_id)
        elif GETvars.txtype=="rev":
            txTypeData=Rev.objects.get(id=POSTvars.type_id)
        elif GETvars.txtype=="adhoc":
            txTypeData=None
    else:
        txTypeData=None

    ###
    ### If all values are present and vaild, write transaction to PtxLog
    ###

    ### Prepare and validate input data
    try:
        try:
            postDate=convDate(POSTvars.tx_date)
        except:
            raise Exception("Invalid date format. Please use YYYY-MM-DD.")

        try:
            if GETvars.txtype=="exp":
                postMemo=Exp.objects.get(id=POSTvars.type_id).display_name
            if GETvars.txtype=="rev":
                postMemo=Rev.objects.get(id=POSTvars.type_id).display_name
            if GETvars.txtype=="adhoc":
                postMemo=POSTvars.tx_memo
        except:
            raise Exception("Memo invalid.")

        try:
            postAmount=Decimal(POSTvars.tx_amount)
        except:
            raise Exception("Amount invalid.")

        try:
            if GETvars.txtype=="adhoc" and POSTvars.tx_debit=="on": postTxType="debit"
            if GETvars.txtype=="adhoc" and POSTvars.tx_debit!="on": postTxType="credit"
            if GETvars.txtype=="exp": postTxType="debit"
            if GETvars.txtype=="rev": postTxType="credit"
        except:
            raise Exception("Transaction type invalid.")

        try:
            if GETvars.txtype=="adhoc":
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
            if GETvars.txtype=="exp":
                exp=Exp.objects.get(id=POSTvars.type_id)
                exp.last_posted_date=postDate
                exp.save()
            if GETvars.txtype=="rev":
                rev=Rev.objects.get(id=POSTvars.type_id)
                rev.last_posted_date=postDate
                rev.save()
            flash("Transaction successfully added.", category="success")
            return render_template("accts.html", acct=acct, user=user, ptx=ptx)
    except Exception as e:
        flash("Unable to write transaction to database. Please try again.", category="danger")

    return render_template("newtx.html", acct=acct, user=user, ptx=ptx, txtype=GETvars.txtype, typeid=POSTvars.type_id, typeid_options=typeid_options, txTypeData=txTypeData)