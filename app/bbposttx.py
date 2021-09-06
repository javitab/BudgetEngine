import bbdata as bb

actions = [
    "1: View all posted transactions for account",
    "2: View posted transactions for account since date",
    "3: Post transactions",
    "4: Create posted transaction log for account"
]

def postTxMenu():
    continuePostLoop = 1

    while continuePostLoop == 1:
        action = bb.menuGen(actions,"Post Transactions Menu",0)
        if action == 'Q':
            continuePostLoop = 0
        if action == '1':
            print("View all posted transactions")
            bb.printAsDataFrame(bb.listCollection("accounts"))
            acctName = input("What account would you like to get transactions for? ")
            getTxData(acctName)
        if action == '2':
            print("View all posted transacations since date, work in progress")
        if action == '3':
            print("Post transactions, work in progress")
            bb.printAsDataFrame(bb.listCollection("accounts"))
            TxAccount = input("What account should the transaction be posted to? ")
            currAcct = bb.acct(TxAccount)
            TxType = input("What type of transaction is this? (credit/debit) ")
            if TxType == 'credit':
                bb.printAsDataFrame(bb.listRevenue(TxAccount))
                KnownRev = input("Is the transaction in the above list? If yes, please enter name, else, enter AdHoc ({Enter Name}/ AdHoc ) ")
                if KnownRev == 'AdHoc':
                    TxMemo = input("Please enter name of AdHoc transaction: ")
                    IsAdhoc = True
                    TxDate = bb.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                elif KnownRev != 'AdHoc':
                    IsAdhoc = False
                    revName = KnownRev
                    currTx = bb.revenue(revName)
                    TxMemo = currTx.name
                    TxAmountConf = input("Is the transaction amount $%s (y/n) " % currTx.amount)
                    if TxAmountConf == 'y': TxAmount = currTx.amount
                    if TxAmountConf == 'n': TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                    TxDateNext = bb.txIterate(currTx.Frequency,currTx.LastDatePosted)
                    TxDateConf = input("Is the date of the transaction %s?: (y/n)" % TxDateNext)
                    if TxDateConf == 'y': TxDate = TxDateNext
                    if TxDateConf == 'n': TxDate = bb.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    currTx.setLastPostedDate(TxDate)
                NewBalance = currAcct.CurrBalance + TxAmount
                currAcct.setCurrBalance(NewBalance)
            if TxType == 'debit':
                bb.printAsDataFrame(bb.listExpenses(TxAccount))
                KnownExp = input("Is the transaction in the above list? If yes, please enter name, else, enter AdHoc ({Enter Name}/ AdHoc ) ")
                if KnownExp == 'AdHoc':
                    TxMemo = input("Please enter name of AdHoc transaction: ")
                    IsAdhoc = True
                    TxDate = bb.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                elif KnownExp != 'AdHoc':
                    IsAdhoc = False
                    expName = KnownExp
                    currTx = bb.expense(expName)
                    TxMemo = currTx.name
                    TxAmountConf = input("Is the transaction amount $%s (y/n) " % currTx.amount)
                    if TxAmountConf == 'y': TxAmount = currTx.amount
                    if TxAmountConf == 'n': TxAmount = float(input("Please enter the amount of the transaction (XX.XX) "))
                    TxDateNext = bb.txIterate('Monthly',currTx.LastPostedDate)
                    TxDateConf = input("Is the date of the transaction %s?: (y/n)" % TxDateNext)
                    if TxDateConf == 'y': TxDate = TxDateNext
                    if TxDateConf == 'n': TxDate = bb.convDate(input("Please enter the date of the transaction (YYYY-MM-DD) "))
                    currTx.setLastPostedDate(TxDate)
                NewBalance = currAcct.CurrBalance - TxAmount
                currAcct.setCurrBalance(NewBalance)
            print("Account: %s Type: %s Date: %s Amount: $%s Memo: %s Adhoc: %s Balance: %s" % (TxAccount,TxType,TxDate,TxAmount,TxMemo,IsAdhoc,NewBalance))
            writeTx(TxAccount,TxType,TxDate,TxAmount,TxMemo,IsAdhoc,NewBalance)
        if action == '4':
            print("Create blank transaction log")
            acctName = input("What account would you like to create a transaction log for? ")
            CreateBlankTxLog(acctName)
        


def getTxData(acctName):
    "This function will get all transactions for a given account"
    #Get data for account
    acctTxData = bb.postedtx.aggregate([
    {
        '$match': {
            'acctName': acctName
        }
    }, {
        '$unwind': {
            'path': '$PostedTxs'
        }
    }, {
        '$project': {
            'PostedTxs.Memo': 1, 
            'PostedTxs.Amount': 1, 
            'PostedTxs.Date': 1, 
            'PostedTxs.TxType': 1, 
            'PostedTxs.AdHoc': 1,
            'PostedTxs.Balance': 1
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
])
    #Iterate through data
    for tx in acctTxData:
        postedTx = (tx['PostedTxs'])
        postedTxMemo = postedTx['Memo']
        postedTxAmount = postedTx['Amount']
        postedTxDate = postedTx['Date']
        postedTxType = postedTx['TxType']
        postedTxAdHoc = postedTx['AdHoc']
        postedTxBalance = postedTx['Balance']
        print("%s %s $%s %s AdHoc: %s Balance: $%s" % (postedTxDate,postedTxType,postedTxAmount,postedTxMemo,postedTxAdHoc,postedTxBalance))

def writeTx(TxAccount,TxType,TxDate,TxAmount,TxMemo,IsAdhoc,TxBalance):
    "This function will write posted transactions"
    postedTxAcctQuery = { 'acctName': TxAccount }
    postedTxToWrite = {'$push':
            {'PostedTxs':
                {   "Memo": TxMemo,
                    "Amount": TxAmount,
                    "Date": TxDate,
                    "TxType": TxType,
                    "AdHoc": IsAdhoc,
                    "Balance": TxBalance
                }}
        }
    x = bb.postedtx.update_one(postedTxAcctQuery,postedTxToWrite)

def CreateBlankTxLog(acctName):
    "This function will create a blank transaction log if it does not already exist"
    filter = { "acctName": acctName }
    TxLogCheck =  bb.postedtx.count_documents(filter, limit=1)
    if TxLogCheck == 1:
        print("TxLog already exists, please review for validity")
    if TxLogCheck < 1:
        print("TxLog does not exist, creating.")
        bb.postedtx.insert_one(
            {
                "acctName": acctName
            }
        )