# The Crypto Wizard
# An Automated Trading Bot by Zachary Vogt
# Aimed at Small % Flips

import robin_stocks as r
from settings import *
import time
import datetime

# Have to log in before loading functions
login = r.robinhood.login(RH_USERNAME, RH_PASSWORD)


def add(x, y):
    return x + y


def load_portfolio():
    return r.robinhood.account.load_portfolio_profile()


def limit_buy(symbol, quantity, limit_price):
    return r.robinhood.order_buy_crypto_limit_by_price(symbol, quantity, limit_price, timeInForce='gtc', jsonify=True)


def limit_sell(symbol, quantity, limit_price):
    return r.robinhood.order_sell_crypto_limit(symbol, quantity, limit_price, timeInForce='gtc', jsonify=True)


def get_crypto_history(symbol):
    symbol_history = r.robinhood.crypto.get_crypto_historicals(symbol)
    symbol_close = []
    for close in symbol_history:
        if close['close_price']:
            symbol_close.append(float(close['close_price']))
    return sum(symbol_close) / len(symbol_close)


def get_current_price(symbol):
    current_price = r.robinhood.crypto.get_crypto_quote(symbol)['ask_price']
    return current_price


def get_crypto_positions():
    return r.robinhood.crypto.get_crypto_positions()


if __name__ == '__main__':
    print(f"Welcome to Zak's Crypto Bot.")
    # need to exist outside of while loop.
    list_of_recent_btc = []
    list_of_recent_doge = []
    btc_preferred = False
    doge_preferred = False
    buy_counter = 0
    sell_counter = 0
    while True:
        print(f"Looking at current prices. Comparing them to past month's closes and current hourly figures.\n")
        now = datetime.datetime.now()
        print(f"Time: {now}")
        print(f"Buys: {buy_counter}.")
        print(f"Sells: {sell_counter}.\n")
        # Load Portfolio Data
        portfolio_data = load_portfolio()

        # How Much Can We Spend?
        acct_equity = float(portfolio_data['equity'])

        # Get Current Positions
        crypto_positions = get_crypto_positions()

        # Loop Through Positions and Assign to Respective code names
        counter = 0
        for i in crypto_positions:
            if (crypto_positions[counter]['currency']['code']) == "BTC":
                BTC = crypto_positions[counter]
            if (crypto_positions[counter]['currency']['code']) == "DOGE":
                DOGE = crypto_positions[counter]
            counter += 1

        # Get Averages for btc and doge
        BTC_AVG = get_crypto_history('BTC')
        DOGE_AVG = get_crypto_history('DOGE')
        print(f"BTC AVG = {BTC_AVG}.\n"
              f"DOGE AVG = {DOGE_AVG}.\n")

        # Compare current price to averages
        BTC_CURRENT = get_current_price('BTC')
        DOGE_CURRENT = get_current_price('DOGE')

        # Hourly Average for Bitcoin
        list_of_recent_btc.append(float(BTC_CURRENT))
        if len(list_of_recent_btc) >= 240:
            del list_of_recent_btc[0]
        HOURLY_BTC_AVG = sum(list_of_recent_btc)/len(list_of_recent_btc)
        HOURLY_BTC_WEIGHT = float(BTC_CURRENT) / HOURLY_BTC_AVG

        # Hourly Average for Doge
        list_of_recent_doge.append(float(DOGE_CURRENT))
        if len(list_of_recent_doge) >= 240:
            del list_of_recent_doge[0]
        HOURLY_DOGE_AVG = sum(list_of_recent_doge) / len(list_of_recent_doge)
        HOURLY_DOGE_WEIGHT = float(DOGE_CURRENT) / HOURLY_DOGE_AVG

        # Calculate a weight based on difference
        MONTHLY_BTC_WEIGHT = float(BTC_CURRENT) / BTC_AVG
        # Print(f"HOURLY BTC WEIGHT - {HOURLY_BTC_WEIGHT}")
        # Print(f"MONTHLY BTC WEIGHT - {MONTHLY_BTC_WEIGHT}\n")

        MONTHLY_DOGE_WEIGHT = float(DOGE_CURRENT) / DOGE_AVG
        # Print(f"HOURLY DOGE WEIGHT - {HOURLY_DOGE_WEIGHT}")
        # Print(f"MONTHLY DOGE WEIGHT - {MONTHLY_DOGE_WEIGHT}\n")

        print(f"BTC Weights: Hourly: {HOURLY_BTC_WEIGHT}, Monthly: {MONTHLY_BTC_WEIGHT}.\n")
        print(f"DOGE Weights: Hourly: {HOURLY_DOGE_WEIGHT}, Monthly: {MONTHLY_DOGE_WEIGHT}.\n")

        # Compare BTC weight to DOGE weight.
        if add(HOURLY_BTC_WEIGHT, MONTHLY_BTC_WEIGHT) < 2 and add(HOURLY_BTC_WEIGHT, MONTHLY_BTC_WEIGHT) < add(HOURLY_DOGE_WEIGHT, MONTHLY_DOGE_WEIGHT):
            btc_good_deal = True
            btc_preferred = True
            doge_preferred = False
            print("BTC > DOGE for profitability.\n")
        else:
            btc_good_deal = False

        if add(HOURLY_DOGE_WEIGHT, MONTHLY_DOGE_WEIGHT) < 2 and add(HOURLY_DOGE_WEIGHT, MONTHLY_DOGE_WEIGHT) < add(HOURLY_BTC_WEIGHT, MONTHLY_BTC_WEIGHT):
            doge_good_deal = True
            btc_preferred = False
            doge_preferred = True
            print("DOGE < BTC for profitability.\n")
        else:
            doge_good_deal = False

        time.sleep(15)

# Buy/Sell Logic - Needs Refactoring
'''
        # if trade certainty > whatever
        if btc_preferred and btc_good_deal and (acct_equity != 0) and len(list_of_recent_btc) > 10:
            print(limit_buy('BTC', float(acct_equity), round(float(BTC_CURRENT), 7)))
            print(f"The Wizard has purchased {acct_equity} of magical BTC.")
            buy_counter += 1

        if doge_preferred and doge_good_deal and (acct_equity != 0) and len(list_of_recent_doge) > 10:
            print(limit_buy('DOGE', float(acct_equity), round(float(DOGE_CURRENT), 7)))
            print(f"The Wizard has purchased {acct_equity} of magical DOGE.")
            buy_counter += 1

        # if stock price > our trade:
        if float(BTC_CURRENT) - (float(BTC['cost_bases'][0]['direct_cost_basis'])/float(BTC['cost_bases'][0]['direct_quantity'])) > 0.01:
            print(limit_sell('BTC', float(BTC['cost_bases'][0]['direct_quantity']), round(float(BTC_CURRENT), 7)))
            print(f"The Wizard sold some charged BTC.")
            sell_counter += 1

        if float(DOGE_CURRENT) - (float(DOGE['cost_bases'][0]['direct_cost_basis'])/float(DOGE['cost_bases'][0]['direct_quantity'])) > 0.01:
            print(limit_sell('DOGE', float(DOGE['cost_bases'][0]['direct_quantity']), round(float(DOGE_CURRENT), 7)))
            print("The Wizard sold some charged DOGE.")
            sell_counter += 1
'''