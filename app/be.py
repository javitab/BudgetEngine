from bedata import *
from beaccts import *
from berevenue import *
from beexpenses import *
from beposttx import *

if __name__ == '__main__':
    continueAppMenu = 1

    actions = [
        "1: Account Menu",
        "2: Expense Menu",
        "3: Revenue Menu",
        "4: Post Tx Menu"
    ]

    while continueAppMenu == 1:
        action = menuGen(actions,"Main Menu")
        if action == 'Q':
            continueAppMenu = 0
        if action == '1':
            acctMenu()
        if action == '2':
            expMenu()
        if action == '3':
            revMenu()
        if action == '4':
            postTxMenu()