import bbdata as bb
import matplotlib.pyplot as plt
import pandas as pd
import http.server
import socketserver
import os

projEnd = '2022-12-31'
acctName = 'Joint'
acct = bb.acct(acctName)

proj = acct.projRev(projEnd)

expDf = proj[2]

print(acctName,"account projected balance for",projEnd,"will be $",proj[0])

expDf.plot(kind='line',x='Date',y='Balance',title=('%s account projected balances, $%s' % (acctName, proj[0])))
plt.savefig('/projoutput/output.png')

PORT = 8080
DIRECTORY = "/projoutput"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving output at http://localhost:%s" % PORT)
        print("Press Ctrl-C to terminate")
        httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()