from flask import request
from datetime import datetime as dt

class getArgs():
    def __init__(self,varsDeclare):
        for i in varsDeclare:
            setattr(self,i,None)
            setattr(self,i,request.args.get(f'{i}'))

class postForm():
    def __init__(self,varsDeclare):
        for i in varsDeclare:
            setattr(self,i,None)
            setattr(self,i,request.form.get(f'{i}'))

def makeDate(date):
    if date!=None:
        return dt.strptime(date, '%Y-%m-%d').date()
    elif date==None:
        return None
