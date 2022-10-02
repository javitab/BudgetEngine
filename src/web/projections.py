from decimal import Decimal
from bson import ObjectId
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user



from ..BudgetEngine.projection import Projection
from ..BudgetEngine.acct import Acct,PtxLog
from ..BudgetEngine.exp import Exp
from ..BudgetEngine.rev import Rev
from ..BudgetEngine.datafunc import *
from ..BudgetEngine.dtfunc import *

from .webfunc import *

project = Blueprint('project', __name__)


@project.route('/view', methods=['GET'])
@login_required
def view_proj():
    declareVars=['acct_id','proj_id','start_date','end_date']
    GETargs=getArgs(declareVars)
    
    if request.method=='GET':
        if GETargs.proj_id==None:
            flash("Cannot display projection without proj_id", category='error')
        else:
            proj=Projection.objects.get(id=GETargs.proj_id)
            acct=proj.projection_acct

        return render_template("projections.html", proj=proj, acct=acct, user=current_user, projs=acctProjDict(acct_id=acct.id), action='view')

    if request.method=='POST':
        pass

@project.route('/new', methods=['POST','GET'])
@login_required
def new_proj():
    declareVars=['acct_id','start_date','end_date','proj_disp_name','proj_id']
    POSTvars=postForm(declareVars)
    setattr(POSTvars,'start_date',convDate(POSTvars.start_date))
    setattr(POSTvars,'end_date',convDate(POSTvars.end_date))
    GETargs=getArgs(declareVars)

    if request.method=='GET':
        if GETargs.acct_id!=None:
            currAcct=Acct.objects.get(id=GETargs.acct_id)
            newProj=Projection(
                projection_acct=currAcct.id,
                start_date=dt.now(),
                end_date=dt.utcnow().__add__(timedelta(days=90))
            )
            newProj.save()
            currAcct.projections.append(newProj.id)
            currAcct.save()
        proj=newProj
        acct=currAcct
        return render_template("projections.html", proj=proj, acct=acct, user=current_user, projs=acctProjDict(acct_id=currAcct.id), action='new')
    elif request.method=='POST':
        if POSTvars.proj_id!=None:
            proj=Projection.objects.get(id=POSTvars.proj_id)
            acct=Acct.objects.get(id=POSTvars.acct_id)
            proj.start_date=POSTvars.start_date
            proj.end_date=POSTvars.end_date
            proj.disp_name=POSTvars.proj_disp_name
            proj.save()
            proj.runProjection()
            proj.save()
        return render_template("projections.html", proj=proj, acct=acct, user=current_user, projs=acctProjDict(acct_id=acct.id), action='view')
