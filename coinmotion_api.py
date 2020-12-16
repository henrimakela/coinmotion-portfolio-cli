import time
import hmac
import hashlib
import json
import requests

def createHeaders(apiKey, signature):
    return { 'Content-Type': 'application/json',
            'X-COINMOTION-APIKEY' : apiKey,
            'X-COINMOTION-SIGNATURE': signature}

def createNonce():
    return str(int(time.time()))

def createSignature(payload, apiSecret):
    return hmac.new(apiSecret.encode('utf-8'),json.dumps(payload).encode('utf-8'), digestmod=hashlib.sha512).hexdigest()

def requestBalances(payload, headers, url):
    return requests.post(url, json = payload, headers = headers).json()['payload']

def getRates(url):
    return requests.get(url).json()['payload']