import time
import json
import hmac
import hashlib
import requests
import base64
import os
import coinmotion_api as api
from portfolio_tools import BalanceExcelTool
import constants

URL_BALANCES = 'https://api.coinmotion.com/v1/balances'
URL_RATES = 'https://api.coinmotion.com/v2/rates'
sheetPath = "/Users/henrimakela/Desktop/balances.xls"

#1 Create a nonce. Uses unix timestamp
nonce = api.createNonce()

# Create a payload for the post request. Nonce is required, parameters are optional
payload = { 'nonce': nonce,'parameters': {}}

# Create a signature from the payload and the api secret (hmac SHA512)
signature = api.createSignature(payload, constants.apiSecret)

# Create headers that include apikey and the signature
headers = api.createHeaders(constants.apiKey, signature)

# Request balances 
balances = api.requestBalances(payload, headers, URL_BALANCES)

# Rates are public endpoint
rates = api.getRates(URL_RATES)

tool = BalanceExcelTool(sheetPath)
totalDeposits = tool.getTotalDeposits()

ethPrice = float(rates['ethEur']['buy'])
xrpPrice = float(rates['xrpEur']['buy'])

ethBalance = float(balances['eth_bal']) 
xrpBalance = float(balances['xrp_bal']) 

ethEur = ethPrice * ethBalance
xrpEur = xrpPrice * xrpBalance

total = ethEur + xrpEur

profit = total - totalDeposits
roe = (profit / totalDeposits) * 100

print("Tässä tietoa portfoliostasi: \n\n Omistukset: \n")
print("ETH: " + str(ethBalance) + "ETH / " + str(ethEur) + " €" )
print("XRP: " + str(xrpBalance) + "XRP / " + str(xrpEur) + " €" )
print("Talletukset: " + str(totalDeposits) + "€") 
print("Kokonaisarvo: " + str(total) + "€")
print("Tuotto euroina: " + str(profit))
print("Tuotto prosentteina: " + '{0:.1f}'.format(roe) + "%")

