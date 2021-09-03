# BudgetBalancer

### Brief Description

Python/MongoDB app that is capable of forecasting account balances based upon definied revenues and expenses per account.

### Sample DB data
If you wish to use test data, run the below commands: 

'sudo docker exec -it budgetbalancer_python_1 bash'
'mongorestore --host=mongo --archive=example --nsFrom=BudgetBalancer.* --nsTo=BudgetBalancer.*'

### TODO:
    - [ ] update bb-importexpenses.py to include means to delete and modify expenses
    - [ ] update bb-importaccts.py and bb-importrevenue.py to match bb-importexpenses.py
    - [ ] rework bb.py to be a better-suited entry point
    - [ ] create a method of confirming/posting transactions after they occur which will udpate the "LastPosted" field on expenses and revenues