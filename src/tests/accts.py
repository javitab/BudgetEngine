import sys
from os import path


sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import random
from operator import concat
from bson import ObjectId
from pprint import pprint

from BudgetEngine import accts,data,ptxLog
from testfx import *


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
        from BudgetEngine import *
        

    ###
    ### Declaring test_run_id and test_bank_name to identify testing runs
    ### and creating test user to make owner for accounts
    ###

    test_run_id = concat(data.dtfunc('today','fulldate','str'),concat('-',str(random.randrange(111,999))))
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
        print("Current User _id: ",testUser.id)
        test(name="standard_user_creation",test=1,outcome=True)
    except:
        test(name="standard_user_creation",test=1,outcome=False)
    

    ###
    ###Testing Account Creation
    ###



    #Generating Account Info for First Account

    first_bank_routing_number = random.randrange(1000000,9999999)
    first_bank_account_number = random.randrange(1000000,9999999)
    first_account_display_name = ('TestAccount-%s' % test_run_id)

    #Create First Account
    first_account_creation = accts.Acct.create(bank_name=test_bank_name, account_display_name=first_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=first_bank_routing_number, bank_account_number=first_bank_account_number)
    if type(first_account_creation)==ObjectId:
        test(name="first_account_creation",test=1,outcome=True)
    else:
        test(name="first_account_creation",test=1,outcome=False)
    
    #Attempt Duplicate Account Creation
    first_duplicate_account_creation = accts.Acct.create(bank_name=test_bank_name, account_display_name=first_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=first_bank_routing_number, bank_account_number=first_bank_account_number)
    if first_duplicate_account_creation=='Error: account with same bank_account_number and bank_routing_number already exists':
        test(name="first_duplicate_account_creation",test=2,outcome=True)
    else:
        test(name="first_duplicate_account_creation",test=2,outcome=False)

    #Create Account with missing_bank_name
    try:
        missing_bank_name_bank_routing_number = random.randrange(1000000,9999999)
        missing_bank_name_bank_account_number = random.randrange(1000000,9999999)
        missing_bank_name_account_display_name = ('TestAccount%s' % test_run_id)

        missing_bank_name_account_creation = accts.Acct.create(account_display_name=missing_bank_name_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=missing_bank_name_bank_routing_number, bank_account_number=missing_bank_name_bank_account_number)
        print(missing_bank_name_account_creation)
    except:
        test(name="missing_bank_name",test=2,outcome=True)
    #Create Account with missing_account_display_name
    try:
        missing_account_display_name_bank_routing_number = random.randrange(1000000,9999999)
        missing_account_display_name_bank_account_number = random.randrange(1000000,9999999)
        missing_account_display_name_account_display_name = ('TestAccount%s' % test_run_id)

        missing_account_display_name_account_creation = accts.Acct.create(bank_name=test_bank_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=missing_account_display_name_bank_routing_number, bank_account_number=missing_account_display_name_bank_account_number)
        print(missing_account_display_name_account_creation)
    except:
        test(name="missing_account_display",test=2,outcome=True)
    #Create Account with missing_low_balance_alert
    try:
        missing_low_balance_alert_bank_routing_number = random.randrange(1000000,9999999)
        missing_low_balance_alert_bank_account_number = random.randrange(1000000,9999999)
        missing_low_balance_alert_account_display_name = ('TestAccount%s' % test_run_id)

        missing_low_balance_alert_account_creation = accts.Acct.create(bank_name=test_bank_name, owning_user=standard_user_creation, missing_low_balance_alert_account_display_name=missing_low_balance_alert_account_display_name,bank_routing_number=missing_low_balance_alert_bank_routing_number, bank_account_number=missing_low_balance_alert_bank_account_number)
        print(missing_low_balance_alert_account_creation)
    except:
        test(name="missing_low_balance_alert",test=2,outcome=True)
    

    
    ###
    ### Testing pushing to sub arrays
    ###

    #Create Account with push_revIds_array
    
    push_revIds_array_bank_routing_number = random.randrange(1000000,9999999)
    push_revIds_array_bank_account_number = random.randrange(1000000,9999999)
    push_revIds_array_account_display_name = ('TestAccount-push_revIds_array-%s' % test_run_id)

    push_revIds_array_account_creation = accts.Acct.create(bank_name=test_bank_name,account_display_name=push_revIds_array_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=push_revIds_array_bank_routing_number, bank_account_number=push_revIds_array_bank_account_number, current_balance=0, tx_last_posted=None)
    #print(push_revIds_array_account_creation)
    
    #Output data in class components

    testAcctRevIds = accts.Acct(push_revIds_array_account_creation)

    for i in ['62c8f237ed0befd90364b6b6','62c8f26271eeb79862d9f479','62a2c4875d353495c3c3ecee','62c8f237ed0befd90364b6b5']:
        testAcctRevIds.addRevIds(i)
        #testAcctRevIds.addExpIds(i)

    rev_ids_total=0
    for i in testAcctRevIds.rev_ids():
        rev_ids_total = rev_ids_total + 1
    if rev_ids_total==4:
        test(name="push_revIds_array",test=1,outcome=True)
    else:
        test(name="push_revIds_array",test=1,outcome=False)

    
    #Create Account with push_ExpIds_array
    
    push_ExpIds_array_bank_routing_number = random.randrange(1000000,9999999)
    push_ExpIds_array_bank_account_number = random.randrange(1000000,9999999)
    push_ExpIds_array_account_display_name = ('TestAccount-push_ExpIds_array-%s' % test_run_id)

    push_ExpIds_array_account_creation = accts.Acct.create(bank_name=test_bank_name,account_display_name=push_ExpIds_array_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=push_ExpIds_array_bank_routing_number, bank_account_number=push_ExpIds_array_bank_account_number, current_balance=0, tx_last_posted=None)
    testAcctExpIds = accts.Acct(push_ExpIds_array_account_creation)

    for i in ['62c8f237ed0befd90364b6b6','62c8f26271eeb79862d9f479','62a2c4875d353495c3c3ecee','62c8f237ed0befd90364b6b5']:
        testAcctExpIds.addExpIds(i)
    exp_ids_total=0
    for i in testAcctExpIds.exp_ids():
        exp_ids_total = exp_ids_total + 1
    if exp_ids_total==4:
        test(name="push_expIds_array",test=1,outcome=True)
    else:
        test(name="push_expIds_array",test=1,outcome=False)

    #Create Account with write_posted_transactions
    
    write_posted_transactions_bank_routing_number = random.randrange(1000000,9999999)
    write_posted_transactions_bank_account_number = random.randrange(1000000,9999999)
    write_posted_transactions_account_display_name = ('TestAccount-write_posted_transactions-%s' % test_run_id)

    write_posted_transactions_account_creation = accts.Acct.create(bank_name=test_bank_name,account_display_name=write_posted_transactions_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=write_posted_transactions_bank_routing_number, bank_account_number=write_posted_transactions_bank_account_number, current_balance=0, tx_last_posted=None)
    testAcctPostedTx = accts.Acct(write_posted_transactions_account_creation)

    ptx_counter=0
    while ptx_counter < 5:
        try:
            testAcctPostedTx.writePtx(memo=f"Test Transaction {ptx_counter}",amount=420.69,date=data.dtfunc(period='today',component='fulldate',fmt='dt'),tx_type=1,ad_hoc=True,balance=5023.23)
            ptx_counter = ptx_counter+1
        except:
            test(name="write_posted_tx",test=1,outcome=False)
    
    testAcctPostedTxLog=ptxLog.ptxLog(testAcctPostedTx.ptx_log_id)
    transactions = testAcctPostedTxLog.transactions
    if testAcctPostedTxLog.iter_ptx()==5:
        test("write_posted_txs",test=1,outcome=True)
    else:
        test("write_posted_txs",test=1,outcome=False)
        