import bbdata as d
import bbaccts as a
import bbrevenue as r
import bbexpenses as e
import bbposttx as t

if __name__ == '__main__':
    continueAppMenu = 1

    actions = [
        "1: Account Menu",
        "2: Expense Menu",
        "3: Revenue Menu",
        "4: Post Tx Menu"
    ]

    while continueAppMenu == 1:
        action = d.menuGen(actions,"Main Menu")
        if action == 'Q':
            continueAppMenu = 0
        if action == '1':
            a.acctMenu()
        if action == '2':
            e.expMenu()
        if action == '3':
            r.revMenu()
        if action == '4':
            t.postTxMenu()