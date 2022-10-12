from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user


from ..BudgetEngine.exp import Exp

from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

exps = Blueprint('exps', __name__)
context='exps'


@exps.route('/view', methods=['GET','POST'])
@login_required
def view():
    rec_mode='view'
    declareVars=['acct_id','exp_id']
    for i in contextFormData.contextFormFieldNames(Exp): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webGET['exp_id']!=None:
        exp=Exp.objects.get(id=str(webGET['exp_id']))
    else:
        exp=Exp.objects.get(id=str(webPOST['exp_id']))
    ContextForm=contextFormData(
        Object=exp,
        rec_mode=rec_mode,
        FormName="expContextForm",
        DisplayName="View Expense",
        FormAction="/exps/submit"
        )
    return render_template("accts.j2",exp=exp,context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=ContextForm,user=current_user,rec_mode=rec_mode)

@exps.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    #Collecting get and post values
    rec_mode='edit'
    declareVars=['acct_id','exp_id']
    for i in contextFormData.contextFormFieldNames(Exp): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webGET['exp_id']!=None: 
        exp=Exp.objects.get(id=str(webGET['exp_id']))
    else:
        exp=Exp.objects.get(id=str(webPOST['exp_id']))
    ContextForm=contextFormData(
            Object=exp,
            rec_mode=rec_mode,
            FormName="expContextForm",
            DisplayName="Edit Expense",
            FormAction="/exps/submit"
            )
    return render_template("accts.j2",exp=exp,context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=ContextForm,user=current_user,rec_mode=rec_mode)

@exps.route('/new', methods=['GET','POST'])
@login_required
def new():
    #Collecting get and post values
    rec_mode='new'
    declareVars=['acct_id','exp_id']
    for i in contextFormData.contextFormFieldNames(Exp): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    ContextForm=contextFormData(
            Object=Exp(),
            rec_mode=rec_mode,
            FormName="expContextForm",
            DisplayName="New Expense",
            FormAction="/exps/submit"
            )
    return render_template("accts.j2",context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=ContextForm,user=current_user,rec_mode=rec_mode)
    
@exps.route('submit', methods=['POST'])
def submit():
    #Collecting get and post values
    declareVars=['acct_id','exp_id']
    for i in contextFormData.contextFormFieldNames(Exp): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
            acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
            acct=Acct.objects.get(id=webPOST['acct_id'])
    if webPOST['form_submitted']=="edit":
        if webGET['exp_id']!=None:
            exp=Exp.objects.get(id=webGET['exp_id'])
        else:
            exp=Exp.objects.get(id=webPOST['id'])
        if webPOST['form_submitted']=="edit":
            try:
                exp.display_name=webPOST['display_name']
                exp.amount=webPOST['amount']
                exp.frequency=webPOST['frequency']
                exp.start_date=webPOST['start_date']
                if exp.end_date!=None: exp.end_date=webPOST['end_date']
                exp.notes=webPOST['notes']
                exp.save()
                return redirect(url_for('exps.view',exp_id=str(exp.id),acct_id=str(acct.id)))
            except Exception as e:
                print(e)
    elif webPOST['form_submitted']=="new":
        try:
            exp=Exp()
            exp.display_name=webPOST['display_name']
            exp.amount=webPOST['amount']
            exp.frequency=webPOST['frequency']
            exp.start_date=webPOST['start_date']
            exp.end_date=webPOST['end_date']
            exp.notes=webPOST['notes']
            exp.save()
            acct.exp_ids.append(exp.id)
            acct.save()
            return redirect(url_for('exps.view',exp_id=str(exp.id),acct_id=str(acct.id)))
        except Exception as e:
            print(e)
    else:
        return redirect(url_for('exps.view',exp_id=str(exp.id),acct_id=str(acct.id)))

    