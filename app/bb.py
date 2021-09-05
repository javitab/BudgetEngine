import bbdata as bb
import bbaccts as bba
import bbrevenue as bbr
import bbexpenses as bbe

continueAppMenu = 1

actions = [
    "1: Account Menu",
    "2: Expense Menu",
    "3: Revenue Menu"
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