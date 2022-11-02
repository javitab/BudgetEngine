from decimal import Decimal
from flask import request
from datetime import datetime as dt

from src.BudgetEngine.acct import Acct
from src.BudgetEngine.exp import Exp
from src.BudgetEngine.rev import Rev
from src.BudgetEngine.projection import Projection


def makeDate(date):
    if date!=None:
        return dt.strptime(date, '%Y-%m-%d').date()
    elif date==None:
        return None


def getVars(varsDeclare:list):
    post={}
    get={}
    for var in varsDeclare:
        if var in request.form:
            post.update({var:request.form[var]})
        else:
            post.update({var:None})
    for var in varsDeclare:
        if var in request.args:
            get.update({var:request.args[var]})
        else:
            get.update({var:None})
    for var in varsDeclare:
        if get[var]==None or post[var]==None:
            pass
        if get[var]=="":
            get.update({var:None})
        if post[var]=="":
            post.update({var:None})
        else: 
            if str('date') in var:
                try: get.update({var:makeDate(get[var])})
                except: pass
                try: post.update({var:makeDate(post[var])})
                except: pass
            if str('amount') in var:
                try: get.update({var:Decimal(str(get[var]).replace("$",""))})
                except: pass
                try: post.update({var:Decimal(str(post[var]).replace("$",""))})
                except: pass
    output={'get':get,'post':post}
    return output

class contextFormData():
    def __init__(self,Object,rec_mode:str,FormName:str,DisplayName:str,FormAction:str):
        """
        Generates neccessary array of data to display a form.
        Object: Object to base form on (must be object from known back end data model)
        rec_mode: 'new','view','edit'
        FormName: Internal Form Name
        DisplayName: Friendly Name for Form
        inputGroupFields: List of dictionaries of input groups and fields to display in each group
        """
        self.rec_mode=rec_mode
        self.inputGroups=[]
        self.FormName=FormName
        self.DisplayName=DisplayName
        self.ClassInputGroups=Object.FormInputGroups
        self.FormAction=FormAction
        
        listOfInputGroups=[]
        formData=[]

        #Get all input groups
        for field in self.ClassInputGroups:
            if field['input_group_name'] not in listOfInputGroups:
                listOfInputGroups.append(field['input_group_name'])
        
        for _group in listOfInputGroups:
            _groupData=[]
            _field={}
            for _field in self.ClassInputGroups:
                if _field['input_group_name']==_group:
                    #Evaluating field definitions and taking action on data accordingly
                    if _field['field_name'] in str('date'):
                        _field['value']=getattr(Object,_field['field_name']).strftime('%Y-%m-%d')
                    if _field['field_type']=='method':
                        _method=getattr(Object,_field['field_name'])
                        _method=str(_method())
                        _field['value']=_method
                    else:
                        _field.update({'value':getattr(Object,_field['field_name'])})
                    if self.rec_mode=='new':
                        _field['value']=""
                    _groupData.append(_field)
            formData.append(_groupData)
        self.formData=formData

    def contextFormFieldNames(Object):
        fieldNames=['form_submitted']
        for _field in Object.FormInputGroups:
            fieldNames.append(_field['field_name'])
        return fieldNames
        
class getAcctTableData():
    """
    Returns a list of dictionaries of data to display in account table
    """
    def __init__(self,Acct:object):
        self.rows=[]
        self.acct=Acct
        self.ptx=self.acct.active_ptx_log_id
        self.header=self.acct.TableHeaders
        PtxLog=self.acct.active_ptx_log_id
        for ptx in PtxLog.posted_txs:
            _row=[]
            _row.append(ptx.txID)
            _row.append(ptx.date.strftime('%Y-%m-%d'))
            _row.append(ptx.memo)
            _row.append(ptx.amount)
            _row.append(ptx.tx_type)
            _row.append(ptx.ad_hoc)
            _row.append(ptx.balance)
            self.rows.append(_row)

class getProjectedTxTableData():
    """
    Returns a list of dictionaries of data to display in projection table
    """
    def __init__(self,Projection:object):
        self.rows=[]
        self.projection=Projection
        self.header=self.projection.TableHeaders
        for ptx in self.projection.projected_txs:
            _row=[]
            _row.append(ptx.item_id)
            _row.append(ptx.seq)
            _row.append(ptx.date)
            _row.append(ptx.memo)
            if ptx.tx_type=='debit': _row.append(-ptx.amount)
            else: _row.append(ptx.amount)
            _row.append(ptx.ad_hoc)
            _row.append(ptx.balance)
            self.rows.append(_row)


def contextVars(acct=False,exp=False,rev=False,projection=False):
    if acct!=False:
        acct=Acct.objects.get(id=acct)
        ptx=getAcctTableData(acct)
        context_data={'acct':acct.id,'ptx':ptx}
        currContext={'context_id':'acct','context_friendly':'Account'}
    else:
        acct=False
        ptx=False
    if exp!=False:
        exp=Exp.objects.get(id=exp)
        context_data={'exp':exp.id}
        currContext={'context_id':'exp','context_friendly':'Expense'}
    else:
        exp=False
    if rev!=False:
        rev=Rev.objects.get(id=rev)
        context_data={'rev':rev.id}
        currContext={'context_id':'rev','context_friendly':'Revenue'}
    else:
        rev=False
    if projection!=False:
        projection=Projection.objects.get(id=projection)
        context_data={'projection':projection.id}
        currContext={'context_id':'proj','context_friendly':'Projection'}
    else:
        projection=False
 
    return context_data,currContext