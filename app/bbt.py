import bbdata as bb
import matplotlib.pyplot as plt
import pandas as pd
import http.server
import socketserver
import os


projEnd = '2021-12-31'

expenseacct = bb.acct('Expense')

expenseproj = expenseacct.projRev(projEnd)

expDf = expenseproj[2]

print("Expense account projected balance for",projEnd,"will be $",expenseproj[0])

expDf.plot(kind='line',x='Date',y='Balance',title='Expense account projected balances')
plt.savefig('./proj_output/output.png')

PORT = 8080
DIRECTORY = "proj_output"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

try:
    while True:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("Serving output at http://localhost:%s" % PORT)
            httpd.serve_forever()
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate")
    httpd.server_close()