from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user


from ..BudgetEngine.rev import Rev

from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

revs = Blueprint('revs', __name__)
context='revs'


@revs.route('/view', methods=['GET','POST'])
@login_required
def view():
    rec_mode='view'
    declareVars=['acct_id','rev_id']
    for i in contextFormData.contextFormFieldNames(Rev): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webGET['rev_id']!=None:
        rev=Rev.objects.get(id=str(webGET['rev_id']))
    else:
        rev=Rev.objects.get(id=str(webPOST['id']))
    ptx=getAcctTableData(acct)
    ContextForm=contextFormData(
        Object=rev,
        rec_mode='view',
        FormName="revContextForm",
        DisplayName="View Revenue",
        FormAction="/revs/submit"
        )
    return render_template("accts.j2",rev=rev,context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=ContextForm,user=current_user,rec_mode=rec_mode)

@revs.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    #Collecting get and post values
    rec_mode='edit'
    declareVars=['acct_id','rev_id']
    for i in contextFormData.contextFormFieldNames(Rev): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webGET['rev_id']!=None: 
        rev=Rev.objects.get(id=str(webGET['rev_id']))
    else:
        rev=Rev.objects.get(id=str(webPOST['rev_id']))
    ContextForm=contextFormData(
            Object=rev,
            rec_mode=rec_mode,
            FormName="revContextForm",
            DisplayName="Edit Revenue",
            FormAction="/revs/submit"
            )
    return render_template("accts.j2",ptx=getAcctTableData(acct),rev=rev,context=context,acct=acct,ContextForm=ContextForm,user=current_user,rec_mode=rec_mode)

@revs.route('/new', methods=['GET','POST'])
@login_required
def new():
    #Collecting get and post values
    rec_mode='new'
    declareVars=['acct_id','rev_id']
    for i in contextFormData.contextFormFieldNames(Rev): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    ContextForm=contextFormData(
            Object=Rev(),
            rec_mode=rec_mode,
            FormName="expContextForm",
            DisplayName="New Revenue",
            FormAction="/revs/submit"
            )
    return render_template("accts.j2",context=context,ptx=getAcctTableData(acct),acct=acct,ContextForm=ContextForm,user=current_user,rec_mode=rec_mode)

@revs.route('submit', methods=['POST'])
@login_required
def submit():
    #Collecting get and post values
    declareVars=['acct_id','rev_id']
    for i in contextFormData.contextFormFieldNames(Rev): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webPOST['form_submitted']=="edit":
        if webGET['rev_id']!=None:
            rev=Rev.objects.get(id=webGET['id'])
        else:
            rev=Rev.objects.get(id=webPOST['id'])
        try:
            rev.display_name=webPOST['display_name']
            rev.amount=webPOST['amount']
            rev.frequency=webPOST['frequency']
            rev.start_date=webPOST['start_date']
            if rev.end_date!=None: rev.end_date=webPOST['end_date']
            rev.notes=webPOST['notes']
            rev.save()
            return redirect(url_for('revs.view',rev_id=str(rev.id),acct_id=str(acct.id)))
        except Exception as e:
            print(e)
    elif webPOST['form_submitted']=="new":
        try:
            rev=Rev()
            rev.display_name=webPOST['display_name']
            rev.amount=webPOST['amount']
            rev.frequency=webPOST['frequency']
            rev.start_date=webPOST['start_date']
            rev.end_date=webPOST['end_date']
            rev.notes=webPOST['notes']
            rev.save()
            acct.rev_ids.append(rev.id)
            acct.save()
            return redirect(url_for('revs.view',rev_id=str(rev.id),acct_id=str(acct.id)))
        except Exception as e:
            print(e)
    else:
        return redirect(url_for('revs.view',rev_id=str(rev.id),acct_id=str(acct.id)))

    