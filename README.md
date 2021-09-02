Brief description, more to follow

Python/MongoDB app that is capable of forecasting account balances based upon definied revenues and expenses per account.

If you wish to use test data, run the below commands: 

"sudo docker exec -it budgetbalancer_python_1 bash" 
"mongorestore --host=mongo --archive=example --nsFrom=BudgetBalancer.* --nsTo=BudgetBalancer.*"