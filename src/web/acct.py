from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user
from bson import ObjectId


from ..BudgetEngine.acct import Acct, PtxLog, Tx

from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

acct = Blueprint('acct', __name__)
context='acct'


@acct.route('/view', methods=['GET','POST'])
@login_required
def view():
    rec_mode='view'
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Acct): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=current_user.acctIds[0]
    ptx=getAcctTableData(acct)
    acctContextForm=contextFormData(
        Object=acct,
        rec_mode='view',
        FormName="acctContextForm",
        DisplayName="View Account",
        FormAction="/accts/submit"
        )
    return render_template("accts.j2",context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=acctContextForm,user=current_user,rec_mode='view')

@acct.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    #Collecting get and post values
    rec_mode='edit'
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Acct): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    acctContextForm=contextFormData(
            Object=acct,
            rec_mode=rec_mode,
            FormName="acctContextForm",
            DisplayName="View Account",
            FormAction="/accts/submit"
            )
    
    return render_template("accts.j2",context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=acctContextForm,user=current_user,rec_mode=rec_mode)

@acct.route('/new', methods=['GET','POST'])
@login_required
def new():
    #Collecting get and post values
    rec_mode='new'
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Acct): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    acctContextForm=contextFormData(
            Object=Acct(),
            rec_mode=rec_mode,
            FormName="acctContextForm",
            DisplayName="New Account",
            FormAction="/accts/submit"
            )
    return render_template("accts.j2",context=context,ContextForm=acctContextForm,user=current_user,rec_mode=rec_mode)

@acct.route('/newtx', methods=['GET','POST'])
@login_required
def newtx():
    #Collecting get and post values
    rec_mode='view'
    declareVars=['acct_id','tx_type','type_id']
    for i in contextFormData.contextFormFieldNames(Acct): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    new_tx_data={}
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webGET['tx_type']=='exp':
        exp=Exp.objects.get(id=webGET['type_id'])
        new_tx_data.update(
            {
                'type':'exp',
                'type_friendly': 'Expense',
                'type_id':exp.id,
                'next_date':exp.next_date(),
                'amount':exp.amount,
                'memo':exp.display_name,
            })
    elif webGET['tx_type']=='rev':
        rev=Rev.objects.get(id=webGET['type_id'])
        new_tx_data.update(
            {
                'type':'rev',
                'type_friendly': 'Revenue',
                'type_id':rev.id,
                'next_date':rev.next_date(),
                'amount':rev.amount,
                'memo':rev.display_name
            })
    else:
        new_tx_data='adhoc'
        
    return render_template("accts.j2",ptx=getAcctTableData(acct),new_tx_data=new_tx_data,acct=acct,context='newtx',user=current_user,rec_mode=rec_mode)
    
@acct.route('submit', methods=['POST'])
def submit():
    #Collecting get and post values
    declareVars=['acct_id','type_id','tx_type','date','memo','amount','form_submitted','adhoc_type']
    for i in contextFormData.contextFormFieldNames(Acct): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webPOST['form_submitted']=="edit":
        if webGET['acct_id']!=None:
            acct=Acct.objects.get(id=str(webGET['acct_id']))
        else:
            acct=Acct.objects.get(id=str(webPOST['acct_id']))
        try:
            acct.account_display_name=webPOST['account_display_name']
            acct.bank_name=webPOST['bank_name']
            acct.bank_account_number=webPOST['bank_account_number']
            acct.bank_routing_number=webPOST['bank_routing_number']
            acct.low_balance_alert=webPOST['low_balance_alert']
            acct.notes=webPOST['notes']
            acct.save()
            return redirect(url_for('acct.view',context=context,acct_id=str(acct.id)))
        except Exception as e:
            print(e)
    elif webPOST['form_submitted']=="new":
        try:
            acct = Acct(
                bank_name=webPOST['bank_name'],
                bank_routing_number=webPOST['bank_routing_number'],
                bank_account_number=webPOST['bank_account_number'],
                account_display_name=webPOST['account_display_name'],
                current_balance=webPOST['current_balance'],
                low_balance_alert=webPOST['low_balance_alert'],
                notes=webPOST['notes']
                )
            acct.save()
            current_user.acctIds.append(acct.id)
            current_user.save()
            ptx = PtxLog()
            ptx.save()
            acct.history_ptx_log_ids.append(ptx.id)
            acct.active_ptx_log_id = ptx.id
            acct.save()
            return redirect(url_for('acct.view',context=context,acct_id=str(acct.id)))
        except Exception as e:
            print(e)
    elif webPOST['form_submitted']=="newtx":
        if webGET['acct_id']!=None:
            acct=Acct.objects.get(id=str(webGET['acct_id']))
        else:
            acct=Acct.objects.get(id=str(webPOST['acct_id']))

        if webPOST['tx_type']=='exp': 
            tx_type='debit'
            balance=acct.current_balance-webPOST['amount']
            exp=Exp.objects.get(id=webPOST['type_id'])
            exp.last_date=webPOST['date']
            ad_hoc=False
        if webPOST['tx_type']=='rev': 
            tx_type='credit'
            balance=acct.current_balance+webPOST['amount']
            rev=Rev.objects.get(id=webPOST['type_id'])
            rev.last_date=webPOST['date']
            ad_hoc=False
        if webPOST['tx_type']=='adhoc':
            if webPOST['adhoc_type']=='on':
                tx_type='debit'
                balance=acct.current_balance-webPOST['amount']
            else:
                tx_type='credit'
                balance=acct.current_balance+webPOST['amount']
            ad_hoc=True

        ptx=acct.active_ptx_log_id.posted_txs
        ptx.create(
            txID=ObjectId(),
            date=webPOST['date'],
            memo=webPOST['memo'],
            amount=webPOST['amount'],
            tx_type=tx_type,
            ad_hoc=ad_hoc,
            balance=balance
        )
        ptx.save()
        acct.save()
        return redirect(url_for('acct.view',context=context,acct_id=str(acct.id)))

    else:
        acct=current_user.acctIds[0]
        return redirect(url_for('acct.view',context=context,acct_id=str(acct.id)))

    