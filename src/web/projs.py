import contextvars
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user


from ..BudgetEngine.acct import Acct, PtxLog
from ..BudgetEngine.projection import Projection as Proj

from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

projs = Blueprint('projs', __name__)
context='projs'


@projs.route('/view', methods=['GET','POST'])
@login_required
def view():
    rec_mode='view'
    declareVars=['acct_id','proj_id']
    for i in contextFormData.contextFormFieldNames(Proj): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=current_user.acctIds[0]
    if webGET['proj_id']!=None:
        proj=Proj.objects.get(id=str(webGET['proj_id']))
    else:
        proj=Proj.objects.get(id=str(webPOST['proj_id']))
    projContextForm=contextFormData(
        Object=proj,
        rec_mode=rec_mode,
        FormName="projContextForm",
        DisplayName="View Projection",
        FormAction="/projs/submit"
        )
    return render_template("accts.j2",proj=proj,context=context,ptx=getProjectedTxTableData(proj),acct=acct,ContextForm=projContextForm,user=current_user,rec_mode=rec_mode)

@projs.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    #Collecting get and post values
    rec_mode='edit'
    declareVars=['acct_id','proj_id']
    for i in contextFormData.contextFormFieldNames(Proj): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    if webGET['proj_id']!=None:
        proj=Proj.objects.get(id=str(webGET['proj_id']))
    else:
        proj=Proj.objects.get(id=str(webPOST['proj_id']))
    projContextForm=contextFormData(
            Object=proj,
            rec_mode=rec_mode,
            FormName="projContextForm",
            DisplayName="Edit Projection",
            FormAction="/projs/submit"
            )
    
    return render_template("accts.j2",proj=proj,context=context,ptx=getProjectedTxTableData(proj),acct=acct,ContextForm=projContextForm,user=current_user,rec_mode=rec_mode)

@projs.route('/new', methods=['GET','POST'])
@login_required
def new():
    #Collecting get and post values
    rec_mode='new'
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Proj): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
        acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
        acct=Acct.objects.get(id=webPOST['acct_id'])
    projContextForm=contextFormData(
            Object=Proj(),
            rec_mode=rec_mode,
            FormName="projContextForm",
            DisplayName="New Projection",
            FormAction="/projs/submit"
            )
    return render_template("accts.j2",acct=acct,context=context,ContextForm=projContextForm,user=current_user,rec_mode=rec_mode)
    
@projs.route('submit', methods=['POST'])
def submit():
    #Collecting get and post values
    declareVars=['acct_id']
    for i in contextFormData.contextFormFieldNames(Proj): declareVars.append(i)
    vars=getVars(declareVars)
    webPOST=vars['post']
    webGET=vars['get']
    if webGET['acct_id']!=None:
            acct=Acct.objects.get(id=str(webGET['acct_id']))
    else:
            acct=Acct.objects.get(id=webPOST['acct_id'])
    if webPOST['form_submitted']=="edit":
        if webPOST['id']!=None:
            proj=Proj.objects.get(id=str(webPOST['id']))
        try:
            proj.disp_name=webPOST['disp_name']
            proj.end_date=webPOST['end_date']
            proj.notes=webPOST['notes']
            proj.save()
            return redirect(url_for('projs.view',context=context,proj_id=str(proj.id),acct_id=str(acct.id)))
        except Exception as e:
            print(e)
    elif webPOST['form_submitted']=="new":
        # try:
        proj = Proj(
            projection_acct=webPOST['acct_id'],
            disp_name=webPOST['disp_name'],
            start_date=dt.now(),
            end_date=webPOST['end_date'],
            notes=webPOST['notes'],
        )
        proj.save()
        proj.runProjection(acct)
        acct.proj_ids.append(proj.id)
        acct.save()
        return redirect(url_for('projs.view',context=context,proj_id=str(proj.id),acct_id=str(acct.id)))
        # except Exception as e:
        #     print(e)
    else:
        acct=current_user.acctIds[0]
        return redirect(url_for('projs.view',context=context,proj_id=str(proj.id),acct_id=str(acct.id)))

    