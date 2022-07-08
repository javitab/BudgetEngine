sleep 5
mongorestore --host=mongo --archive=example --nsFrom=BudgetBalancer.* --nsTo=BudgetBalancer.* 