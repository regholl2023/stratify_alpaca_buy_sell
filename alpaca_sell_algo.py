# -*- coding: utf-8 -*-
"""
Created on Dec 21 2023
"""
import alpaca_trade_api as tradeapi
import requests
import json
import os

def alpaca_custom_sell_order_limit(api, symbol, qty):
    ask = api.get_latest_quote(symbol)._raw['ap']
    bid = api.get_latest_quote(symbol)._raw['bp']
    mid = (bid + ask) / 2
    mid = round(mid, 2)

    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='limit',
        time_in_force='day',
        limit_price=mid,
        extended_hours = True
    )
    return None


def alpaca_custom_sell_order_market(api, symbol, qty):
    ask = api.get_latest_quote(symbol)._raw['ap']
    bid = api.get_latest_quote(symbol)._raw['bp']
    mid = (bid + ask) / 2
    mid = round(mid, 2)

    api.submit_order(
        symbol=symbol,
        qty=1,
        side='sell',
        type='market',
        time_in_force='day',
        limit_price=mid,
    )
    return None

os.environ['PAPER_ACPA_API_SECRET_ID']

api = tradeapi.REST(
    os.environ['PAPER_ACPA_API_KEY_ID'],
    os.environ['PAPER_ACPA_API_SECRET_ID'],
    'https://paper-api.alpaca.markets'
)

portfolio = api.list_positions()
list_positions = []
for position in portfolio:
    print(position)
    print(position.symbol)
    print(position._raw)
    print(position._raw['symbol'])
    list_positions.append(position.symbol)

#Adust this to your target percentage gain.  
#A future update to this is to slowly sell off in 3 tranches - leaving runners to gain up to 50% or more depending on their fundamental and technical levels.
target_pct_gain = .05

#Get recommended buys.  This can come from any buy signal provider.  
#Stratify Consulting attempts to track historical returns of the trading strategy here: https://www.stratifydataconsulting.com/daily_analysis.html
url = "https://www.stratifydataconsulting.com/buys_json.html"
response = requests.get(url)
recommendation_list = json.loads(response.text)

#Execute Sell orders
for position in portfolio:
    if float(position.unrealized_plpc) >= target_pct_gain and position.symbol not in recommendation_list:
        try:
            print(alpaca_custom_sell_order_limit(api, position.symbol, position.qty))
            print(f"success selling {position.symbol}")
        except:
            print(f"error selling {position.symbol}")
    else:
        print(f"not ready to sell yet {position.symbol}")

