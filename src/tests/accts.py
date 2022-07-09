import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import random
from operator import concat
from bson import ObjectId

from BudgetEngine import accts,data

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

    test_run_id = concat(d.dtfunc('today','fulldate','str'),concat('-',str(random.randrange(111,999))))
    test_bank_name = concat('TestBank-',test_run_id)

    try:
        standard_user_creation_userid=concat("testuser",test_run_id)
        standard_user_creation_email=("janedoe%s@gmail.com" % test_run_id)
        standard_user_creation_first_name="Jane"
        standard_user_creation_last_name="Doe"
        standard_user_creation_password="##PASSWORDHASH##"

        standard_user_creation = u.User.create(userid=standard_user_creation_userid,email=standard_user_creation_email,first_name=standard_user_creation_first_name,last_name=standard_user_creation_last_name,password=standard_user_creation_password)
        print(standard_user_creation)
        testUser = u.User(standard_user_creation)
        print("Current UserID: ",testUser.userid)
        print("Current _id: ",testUser.id)
        print("[*Test Passed*]: standard_user_creation succeeded")
    except:
        print("[#Test Failed#]: standard_user_creation did not succeed")
    

    ###
    ###Testing Account Creation
    ###



    #Generating Account Info for First Account

    first_bank_routing_number = random.randrange(1000000,9999999)
    first_bank_account_number = random.randrange(1000000,9999999)
    first_account_display_name = ('TestAccount-%s' % test_run_id)

    #Create First Account
    first_account_creation = accts.Acct.create(bank_name=test_bank_name, account_display_name=first_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=first_bank_routing_number, bank_account_number=first_bank_account_number)
    print(first_account_creation)
    
    #Attempt Duplicate Account Creation
    first_duplicate_account_creation = accts.Acct.create(bank_name=test_bank_name, account_display_name=first_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=first_bank_routing_number, bank_account_number=first_bank_account_number)
    print(first_duplicate_account_creation)

    #Create Account with missing_bank_name
    try:
        missing_bank_name_bank_routing_number = random.randrange(1000000,9999999)
        missing_bank_name_bank_account_number = random.randrange(1000000,9999999)
        missing_bank_name_account_display_name = ('TestAccount%s' % test_run_id)

        missing_bank_name_account_creation = accts.Acct.create(account_display_name=missing_bank_name_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=missing_bank_name_bank_routing_number, bank_account_number=missing_bank_name_bank_account_number)
        print(missing_bank_name_account_creation)
    except:
        print("Failed Successfully: Unable to create account with missing bank name")
    #Create Account with missing_account_display_name
    try:
        missing_account_display_name_bank_routing_number = random.randrange(1000000,9999999)
        missing_account_display_name_bank_account_number = random.randrange(1000000,9999999)
        missing_account_display_name_account_display_name = ('TestAccount%s' % test_run_id)

        missing_account_display_name_account_creation = accts.Acct.create(bank_name=test_bank_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=missing_account_display_name_bank_routing_number, bank_account_number=missing_account_display_name_bank_account_number)
        print(missing_account_display_name_account_creation)
    except:
        print("Failed Successfully: Unable to create account with missing acccount display name")
    #Create Account with missing_low_balalnce_alert
    try:
        missing_low_balalnce_alert_bank_routing_number = random.randrange(1000000,9999999)
        missing_low_balalnce_alert_bank_account_number = random.randrange(1000000,9999999)
        missing_low_balalnce_alert_account_display_name = ('TestAccount%s' % test_run_id)

        missing_low_balalnce_alert_account_creation = accts.Acct.create(bank_name=test_bank_name, owning_user=standard_user_creation, missing_low_balalnce_alert_account_display_name=missing_low_balalnce_alert_account_display_name,bank_routing_number=missing_low_balalnce_alert_bank_routing_number, bank_account_number=missing_low_balalnce_alert_bank_account_number)
        print(missing_low_balalnce_alert_account_creation)
    except:
        print("Failed Successfully: Unable to create account with missing low balance alert level")
    
    ###
    ### Testing pushing to sub arrays
    ###

    #Create Account with push_revIds_array
    
    push_revIds_array_bank_routing_number = random.randrange(1000000,9999999)
    push_revIds_array_bank_account_number = random.randrange(1000000,9999999)
    push_revIds_array_account_display_name = ('TestAccount-push_revIds_array-%s' % test_run_id)

    push_revIds_array_account_creation = accts.Acct.create(bank_name=test_bank_name,account_display_name=push_revIds_array_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=push_revIds_array_bank_routing_number, bank_account_number=push_revIds_array_bank_account_number, current_balance=0, tx_last_posted=None)
    print(push_revIds_array_account_creation)
    
    output = accts.Acct(push_revIds_array_account_creation).addRevIds(rev_id='62a2c4875d353495c3c3ecee')
    print('Account : ' + str(output.modified_count))

    #Output data in class components

    testAcct = accts.Acct(push_revIds_array_account_creation)

    for i in ['62c8f237ed0befd90364b6b6','62c8f26271eeb79862d9f479','62a2c4875d353495c3c3ecee','62c8f237ed0befd90364b6b5']:
        testAcct.addRevIds(i)
        testAcct.addExpIds(i)

    for i in testAcct.getRevIds():
        print(i)
    
    #Create Account with push_ExpIds_array
    
    push_ExpIds_array_bank_routing_number = random.randrange(1000000,9999999)
    push_ExpIds_array_bank_account_number = random.randrange(1000000,9999999)
    push_ExpIds_array_account_display_name = ('TestAccount-push_ExpIds_array-%s' % test_run_id)

    push_ExpIds_array_account_creation = accts.Acct.create(bank_name=test_bank_name,account_display_name=push_ExpIds_array_account_display_name, owning_user=standard_user_creation, low_balance_alert=100.00, bank_routing_number=push_ExpIds_array_bank_routing_number, bank_account_number=push_ExpIds_array_bank_account_number, current_balance=0, tx_last_posted=None)
    print(push_ExpIds_array_account_creation)
    
    output = accts.Acct(push_ExpIds_array_account_creation).addExpIds(exp_id='62a2c4875d353495c3c3ecee')
    print('Account : ' + str(output.modified_count))

    testAcct = accts.Acct(push_ExpIds_array_account_creation)

    for i in ['62c8f237ed0befd90364b6b6','62c8f26271eeb79862d9f479','62a2c4875d353495c3c3ecee','62c8f237ed0befd90364b6b5']:
        testAcct.addRevIds(i)
        testAcct.addExpIds(i)

    for i in testAcct.getExpIds():
        print(i)

    ###
    ### Initialize class while subarrays may be missing
    ###

    test_acct_no_arrays = accts.Acct(first_account_creation)

    print(test_acct_no_arrays.account_display_name)
    print(test_acct_no_arrays.bank_name)
