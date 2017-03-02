#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import requests
import json
import os


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def getPoint():
    #url = 'https://sandbox.api.kasikornbank.com:8243/gh/deposit/sight/transactions/1.0.0'
    url = 'https://sandbox.api.kasikornbank.com:8243/gh/creditcard/point/1.0.0'
    data = {"CARD_NO_ENCPT":"492141******6698"}
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    d = json.loads(r.text)
    speech = "Your credit card point is " + "{:,.1f}".format(d[0]["CRN_BAL_PTN_CTD"] ) + " points as of " + d[0]["SRC_PCS_DT"]
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-kplus-webhook-sample"
    }

def getStatementBalance():
    url = 'https://sandbox.api.kasikornbank.com:8243/gh/creditcard/point/1.0.0'
    data = {"CARD_NO_ENCPT":"492141******6698"}
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    d = json.loads(r.text)
    speech = "Your credit card balance is " + "{:,.2f}".format(d[0]["CRN_BAL_PTN_CTD"] ) + " Baht. The payment of your credit card is due " + d[0]["SRC_PCS_DT"]
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-kplus-webhook-sample"
    }

def processRequest(req):
    if req.get("result").get("action") == "getStatementBalance":
        return getStatementBalance()
    elif req.get("result").get("action") == "getPoint":
        return getPoint()
    else:
        return {
        "speech": "It's seem K Plus service is not available right now",
        "displayText": "It's seem K Plus service is not available right now",
        "source": "apiai-KPlus-webhook-sample"
        }
       
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
