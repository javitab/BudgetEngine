from flask import Flask, app, request, json
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from flask import Response
import bbdata as bb
import bbposttx as bbp
import bbaccts as bba
import bbrevenue as bbr
import bbexpenses as bbe
from bson import json_util
app = Flask(__name__)

#ptx methods - Posted Transactions

@app.route('/ptx/searchTx', methods=['GET'])
def searchtxID():
    acctID = request.args.get('acctID')
    memo = request.args.get('memo')
    TxType = request.args.get('TxType')
    data = bb.postedTx.searchTxData(acctID,memo,TxType,True)
    return Response(data.to_json(orient="records"), mimetype='application/json')

@app.route('/ptx/txByID', methods=['GET'])
def txByID():
    TxID = request.args.get('TxID')
    txdata = bb.postedTx.searchTxID(TxID,True)
    data = txdata.to_json(orient='records')
    return Response(txdata.to_json(orient='records'), mimetype='application/json')

@app.route('/ptx/txAcct', methods=['GET'])
def txAcct():
    acctID = request.args.get('acctID')
    txdata = bb.postedTx.getTxData(acctID,True)
    data = txdata.to_json(orient='records')
    return Response(txdata.to_json(orient='records'), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='81')
    