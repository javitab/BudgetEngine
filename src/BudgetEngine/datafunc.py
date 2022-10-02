from datetime import datetime as dt
from datetime import timedelta
import calendar as cal
from optparse import Values

from .acct import Acct
from .projection import Projection

def acctProjDict(acct_id:str):
    '''
    Given an account id, will return a dictionary list of projections and names for the account
    '''
    output=[]
    selectedAcct=Acct.objects.get(id=acct_id)
    for i in selectedAcct.projections:
        dict={}
        iProj=Projection.objects.get(id=i)
        dict={
            "id": iProj.id,
            "disp_name": iProj.disp_name
            }
        output.append(dict)
    for i in output:
        print("Id: ",i['id'])
        print("name: ",i['disp_name'])
    return output