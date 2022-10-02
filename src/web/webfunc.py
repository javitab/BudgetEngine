from flask import request

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
