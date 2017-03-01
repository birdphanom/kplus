#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    r = requests.post("https://sandbox.kasikornbank.com/webhook/balance", data = {'key': 'value'},verify=False)
    #req = request.get_json(silent=True, force=True)

    #result = urlopen("https://sandbox.kasikornbank.com/webhook/balance").read()
    #data = json.loads(result)
    #res = json.dumps(data, indent=4)
    
    # print(res)
    #r = make_response(res)
    #r.headers['Content-Type'] = 'application/json'
    return r
    
    


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
