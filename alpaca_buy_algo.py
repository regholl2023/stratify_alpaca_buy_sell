# -*- coding: utf-8 -*-
"""
Created on Dec 21 2023

"""
import alpaca_trade_api as tradeapi
import math
import requests
import json
import os

def alpaca_custom_buy_order_market(api, symbol, est_value):
    ask = api.get_latest_quote(symbol)._raw['ap']
    bid = api.get_latest_quote(symbol)._raw['bp']
    mid = (bid + ask) / 2
    mid = round(mid, 2)
    qty = math.floor(est_value / mid)
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='day',
    )
    return None

def alpaca_custom_buy_order_limit(api, symbol, est_value):
    ask = api.get_latest_quote(symbol)._raw['ap']
    bid = api.get_latest_quote(symbol)._raw['bp']
    mid = (bid + ask) / 2
    mid = round(mid, 2)
    qty = math.floor(est_value / mid)
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='limit',
        time_in_force='day',
        limit_price=mid,
        extended_hours = True
    )
    return None

#Instantiate Alpaca API session
api = tradeapi.REST(
    os.environ['PAPER_ACPA_API_KEY_ID'],
    os.environ['PAPER_ACPA_API_SECRET_ID'],
    'https://paper-api.alpaca.markets'
)
#Obtain existing account and positions info from Alpaca
portfolio = api.list_positions()
list_positions = []
for position in portfolio:
    list_positions.append(position.symbol)
account = api.get_account()

#Get recommended buys.  This can come from any buy signal provider.  
#Stratify Consulting attempts to track historical returns of the trading strategy here: https://www.stratifydataconsulting.com/daily_analysis.html
url = "https://www.stratifydataconsulting.com/buys_json.html"
response = requests.get(url)
recommendation_list = json.loads(response.text)

#Execute buy orders
est_value = float(account.non_marginable_buying_power) / len(recommendation_list)
for ticker in recommendation_list:
    if ticker not in list_positions:
        try:
            print(alpaca_custom_buy_order_limit(api, ticker, est_value))
            print(f"success buying {ticker}")
        except:
            print(f"error buying {ticker}")
    else:
        print("already in portfolio")



