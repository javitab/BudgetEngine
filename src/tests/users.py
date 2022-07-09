import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import random
from operator import concat
from bson import ObjectId

from BudgetEngine import users,data

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__))))
        from BudgetEngine import *
    
    ###
    ###Testing Account Creation
    ###

    test_run_id = concat(str(d.dtfunc('today','fulldate','int')),concat('-',str(random.randrange(111,999))))

    #Testing User Creation For standard_user_creation
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
        
        for i in ['62c8f237ed0befd90364b6b6','62c8f26271eeb79862d9f479','62a2c4875d353495c3c3ecee','62c8f237ed0befd90364b6b5']:
            print(testUser.addAcctIds(i).modified_count," records modified for ",i)
        print("[*Test Passed*]: standard_user_creation succeeded")
    except:
        print("[#Test Failed#]: standard_user_creation did not succeed")
    #Testing User Creation For duplicate_user_creation
    
    duplicate_user_creation_userid=concat("testuser",test_run_id)
    duplicate_user_creation_email=("janedoe%s@gmail.com" % test_run_id)
    duplicate_user_creation_first_name="Jane"
    duplicate_user_creation_last_name="Doe"
    duplicate_user_creation_password="##PASSWORDHASH##"

    duplicate_user_creation = u.User.create(userid=duplicate_user_creation_userid,email=duplicate_user_creation_email,first_name=duplicate_user_creation_first_name,last_name=duplicate_user_creation_last_name,password=duplicate_user_creation_password)
    if duplicate_user_creation=="Error: UserID already in use":
        print("[*Test Passed*]: duplicate_user_creation did not occur")