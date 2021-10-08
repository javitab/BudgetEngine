# BudgetBalancer

### Brief Description

Python/MongoDB app that is capable of forecasting account balances based upon defined revenues and expenses per account.

## env file

The docker-compose.yml file takes values in from a .env file. Below is a sample file to create. The only value in use at this time is as listed below. It allows for an accurate URL to be displayed in the terminal output when running an account balance projection

```
HOST_EXTERNAL_IP=127.0.0.1
```

### Sample DB data
If you wish to use test data, run the below commands: 

```
sudo docker exec -it bb_python bash
sh ./loadExampleData.sh
```
