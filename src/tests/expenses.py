import sys
from os import path

from numpy import outer

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import random
from operator import concat
from bson import ObjectId

from BudgetEngine import users,data
from testfx import *

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
        from BudgetEngine import *
        from testfx import *


    ###
    ###Testing Expense Creation
    ###

    ###
    ### Declaring test_run_id and test_bank_name to identify testing runs
    ### and creating test user and test account for expenses to be attached to
    ###

    test_run_id = concat(d.dtfunc('today','fulldate','str'),concat('-',str(random.randrange(111,999))))
    test_bank_name = concat('TestBank-',test_run_id)

    try:
        standard_user_creation_userid=concat("testuser",test_run_id)
        standard_user_creation_email=("janedoe%s@gmail.com" % test_run_id)
        standard_user_creation_first_name="Jane"
        standard_user_creation_last_name="Doe"
        standard_user_creation_password="##PASSWORDHASH##"
        standard_user_creation_timezone="US/Eastern"

        standard_user_creation = u.User.create(userid=standard_user_creation_userid,email=standard_user_creation_email,first_name=standard_user_creation_first_name,last_name=standard_user_creation_last_name,password=standard_user_creation_password,timezone=standard_user_creation_timezone)
        testUser = u.User(standard_user_creation)
        print("Current UserID: ",testUser.userid)
        print("Current _id: ",testUser.id)
        test(name="standard_user_creation",test=1,outcome=True)
    except:
        test(name="standard_user_creation",test=1,outcome=False)

    #Generating Account Info for First Account
    #Test: account_creation

    bank_routing_number = random.randrange(1000000,9999999)
    bank_account_number = random.randrange(1000000,9999999)
    account_display_number = ('TestAccount-%s' % test_run_id)

    #Create First Account
    account_creation = a.Acct.create(bank_name=test_bank_name, account_display_name=account_display_number, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=bank_routing_number, bank_account_number=bank_account_number)
    if type(account_creation)==ObjectId:
        test(name="account_creation",test=1,outcome=True)
    else:
        test(name="account_creation",test=1,outcome=False)
    testAccount=a.Acct(account_creation)
    
    #Add an expense to account
    #Test: test_exp_acct_class

    test_exp_acct_class = testAccount.createExp(expense_display_name=("%s Exp-%s acct_class" % (account_display_number,random.randrange(111,999))),start_date=data.dtfunc('today','fulldate','dt'),end_date='',frequency=1,amount=420.69)

    if type(test_exp_acct_class)==ObjectId:
        test(name='test_exp_acct_class',test=1,outcome=True)
    else:
        test(name='test_exp_acct_class',test=1,outcome=False)

    #Add an expense to account from expense class
    #Test: test_exp_exp_class

    test_exp_exp_class = e.Exp.create(expense_display_name=("%s Exp-%s exp_class" % (account_display_number,random.randrange(111,999))),start_date=data.dtfunc('today','fulldate','dt'),end_date='',frequency=1,amount=420.69,linked_account=account_creation)

    if type(test_exp_exp_class)==ObjectId:
        test(name='test_exp_exp_class',test=1,outcome=True)
    else:
        test(name='test_exp_exp_class',test=1,outcome=False)