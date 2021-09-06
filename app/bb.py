import bbdata as bb
import bbaccts as bba
import bbrevenue as bbr
import bbexpenses as bbe
import bbposttx as bbt

continueAppMenu = 1

actions = [
    "1: Account Menu",
    "2: Expense Menu",
    "3: Revenue Menu",
    "4: Post Tx Menu"
]

while continueAppMenu == 1:
    action = bb.menuGen(actions,"Main Menu")
    if action == 'Q':
        continueAppMenu = 0
    if action == '1':
        bba.acctMenu()
    if action == '2':
        bbe.expMenu()
    if action == '3':
        bbr.revMenu()
    if action == '4':
        bbt.postTxMenu()