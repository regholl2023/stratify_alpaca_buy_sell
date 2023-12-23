# -*- coding: utf-8 -*-
"""
Created on Dec 21 2023

"""
import alpaca_trade_api as tradeapi
import os

def alpaca_custom_sell_market(api, symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='day'
    )
    return None

api = tradeapi.REST(
    os.environ['PAPER_ACPA_API_KEY_ID'],
    os.environ['PAPER_ACPA_API_SECRET_ID'],
    'https://paper-api.alpaca.markets'
)

portfolio = api.list_positions()
for position in portfolio:
    print(alpaca_custom_sell_market(api, position.symbol, position.qty))