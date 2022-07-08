"""
Module for acct data model
"""
from datetime import date
import BudgetEngine as be

class acct:
    """acct class for creating new and updating existing accounts
    """
    def __init__(self, oid):
        self.data = be.col_accounts.find_one({'_id':oid})
        self.id = self.data['_id']
        self.bank_name = self.data['bank_name']
        self.bank_routing_number = self.data['bank_routing_number']
        self.bank_account_number = self.data['bank_account_number']
        self.account_display_name = self.data['account_display_name']
        self.current_balance = float(round(self.data['current_balance'],2))
        self.low_balance_level = self.data['low_balance_level']
        self.tx_last_posted = self.data['tx_last_posted']

        def reset(self):
            """Reinitializes the current instance of the class. This should be done every time a new value is written to the DB.
            """
            self.__init__(self.id)
        
        def setCurrentBalance(self, newBalance: float):
            """Sets the accounts current balance without transactions
            """
            newBalance=input
            newBalance="{newBalance:.2f}".format(newBalance=input)

        def create(bank_name: str, bank_routing_number=None: str, bank_account_number=None: str, account_display_name: str, current_balance=None: float, low_balance_alart: float, tx_last_posted=None: date):
            """Create a new account after confirming no conflicts

            Args:
                bank_name (str): Name of bank holding account
                account_display_name (str): Display name of account
                low_balance_alart (float): Level at which to alert for a low balance
                bank_routing_number (_type_, optional): Bank routing number. Defaults to None:str.
                bank_account_number (_type_, optional): Bank account number. Defaults to None:str.
                current_balance (_type_, optional): Current balance as maintained by posted transactions. Defaults to None:float.
                tx_last_posted (_type_, optional): Date that a transaction was last posted, maintained by posted tx. Defaults to None:date.
            """
            print("Hello")