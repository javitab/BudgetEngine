import contextvars
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user


from ..BudgetEngine.acct import Acct, PtxLog
from ..BudgetEngine.projection import Projection as proj

from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

projs = Blueprint('projs', __name__)
context='acct'


@projs.route('/view', methods=['GET','POST'])
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

@projs.route('/edit', methods=['GET','POST'])
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

@projs.route('/new', methods=['GET','POST'])
@login_required
def new():
    #Collecting get and post values
    rec_mode='new'
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Projection): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    acctContextForm=contextFormData(
            Object=Projection(),
            rec_mode=rec_mode,
            FormName="projContextForm",
            DisplayName="New Projection",
            FormAction="/projs/submit"
            )
    return render_template("accts.j2",acct=acct,context=context,ContextForm=acctContextForm,user=current_user,rec_mode=rec_mode)
    
@projs.route('submit', methods=['POST'])
def submit():
    #Collecting get and post values
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Acct): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webPOST['form_submitted']=="edit":
        if webGET['acct_id']!=None:
            acct=Acct.objects.get(id=str(webGET['acct_id']))
        else:
            acct=Acct.objects.get(id=webPOST['acct_id'])
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
    else:
        acct=current_user.acctIds[0]
        return redirect(url_for('acct.view',context=context,acct_id=str(acct.id)))

    