# BudgetBalancer

### Brief Description

Python/MongoDB app that forecasts account balances based on current values and maintains a ledger of posted transactions for accounts given recurring and ad hoc expenses and revenue.

### Development

- ✅ .env file for external IP address
- ✅ set start and end date for expenses
- ✅ exclusion dates for recurring revenues
- 🟡 REST API to access application
- 🟡 Wiki documentation
- ☑️ Web Frontend

# Getting Started

Below are the steps to get started. The repository includes a sample dataset to demo the functionality.

## vars file

The app/vars.py file takes install/environment-specific variables. This will come prefilled with 127.0.0.1, however, be sure to update with any values as appropriate.

## Build docker image

You will first need to build the docker image for the python container with the appropriate requirements and dependencies:

```
sudo docker build BudgetBalancer
```

## Start docker environment with docker-compose

```
sudo docker-compose up -d
```

## Connecting to the python instance

Connect to the docker container running the python instance.

```
sudo docker exec -it bb_python bash
```

## (Optional) Load Sample DB data
If you wish to use test data, run the below commands. Otherwise, proceed to the next step and begin entering your own data. Assuming you are already within the docker container:

```
sh ./loadExampleData.sh
```

## Launch the application within the python instance
Run the python app to get started!

```
>python bb.py

=== Printing available options for Main Menu===
1: Account Menu
2: Expense Menu
3: Revenue Menu
4: Post Tx Menu
Q: Quit
What would you like to do? 
```

## You're in!
You can either start exploring from here, or read the further documentation in the Wiki (Work in Progress 🚧).
