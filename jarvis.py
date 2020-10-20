import alpaca_trade_api as tradeapi
from datetime import datetime
from pytz import timezone
from datetime import datetime, time
import generate_report
import sys
import time as t
import push_alert

ticker_symbol = sys.argv[1]
trades_taken = []
postion_size = 100

tz = timezone('EST')
datetime.now(tz) 

api = tradeapi.REST('', '', base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
account = api.get_account()
print(account.status)

def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if check_time > begin_time and check_time < end_time:
        trading_time = True
    else:
        trading_time = False
    print(trading_time)
    return trading_time

def get_high(ticker_symbol):
    high = ''
    while is_time_between(time(13,20), time(14,30)):
        barset = api.get_barset(ticker_symbol, 'day', limit=1)
        bars = barset[ticker_symbol]
        for bar in bars:
            high = bar.h
            print(high)
    return high

# def get_low(ticker_symbol):
#     while is_time_between(time(21,25), time(21,26)):
#         barset = api.get_barset(ticker_symbol, 'day', limit=1)
#         bars = barset[ticker_symbol]
#         for bar in bars:
#             low = bar.l
#             print(low)
#         return low

def get_current(ticker_symbol):
    current = ''
    barset = api.get_barset(ticker_symbol, 'day', limit=1)
    bars = barset[ticker_symbol]
    for bar in bars:
        current = bar.c
        print('Current price of ' + ticker_symbol + ': ' + str(current))
    return current

if get_current(ticker_symbol) == '':
    print('Ticker not found: ' + ticker_symbol)
    sys.exit()
pre_market_high = get_high(ticker_symbol)
print('Premarket high ' + ticker_symbol + ': ' + pre_market_high)
t.sleep(2)
# pre_market_low = get_low(ticker_symbol)


def check_for_crossover(ticker_symbol):
    order_type = ''
    if float(get_current(ticker_symbol)) >= float(pre_market_high):
        print('Place long order now')
        order_type = 'Long'
    # if get_current(ticker_symbol) <= pre_market_low:
    #     print('Place short order now')
    #     order_type = 'Short'
    return order_type

def submit_order(ticker_symbol, side):
    current_price = get_current(ticker_symbol)
    qty = postion_size/current_price
    api.submit_order(
        symbol=ticker_symbol,
        qty=1,
        # qty=round(qty),
        side=side,
        type='market',
        time_in_force='gtc'
    )

def check_for_open_position(ticker_symbol):
    open_position = ''
    positions = api.list_positions()
    if not positions:
        open_position = "NoOpenPosition"
    else:
        for position in positions:
            if int(position.qty) > 0:
                open_position = "PositiveOrder"
            if int(position.qty) < 0:
                open_position = "NegativeOrder"
    return open_position


def place_order(ticker_symbol):
    if check_for_open_position(ticker_symbol) == "NoOpenPosition":
        if check_for_crossover(ticker_symbol) == 'Long':
            submit_order(ticker_symbol, 'buy')
            # t.sleep(4)
            print("Placed long order")
            push_alert.pushbullet_message('Bought', 'Bought 1 shares of ' + ticker_symbol)

        # if check_for_crossover(ticker_symbol) == 'Short':
        #     submit_order(ticker_symbol, 'sell')
        #     # t.sleep(4)
        #     print("Placed short order")

    if check_for_open_position(ticker_symbol) == "PositiveOrder":
        positions = api.list_positions()
        current_price = ''
        for position in positions:
            current_price = position.avg_entry_price
        if current_price:
            if float(get_current(ticker_symbol)) >= float(current_price) + (float(current_price) * 2/100):
                submit_order(ticker_symbol, 'sell')
                # t.sleep(4)
                print('Sell for profit here')
                push_alert.pushbullet_message('Sold for profit here', 'Sold 1 shares of ' + ticker_symbol)
                trades_taken.append(ticker_symbol)
            if float(get_current(ticker_symbol)) <= float(current_price) - (float(current_price) * 2/100):
                submit_order(ticker_symbol, 'sell')
                # t.sleep(4)
                print('Sell for loss here')
                push_alert.pushbullet_message('Sold for loss here', 'Sold 1 shares of ' + ticker_symbol)
                trades_taken.append(ticker_symbol)

    if check_for_open_position(ticker_symbol) == "NegativeOrder":
        positions = api.list_positions()
        current_price = ''
        for position in positions:
            current_price = position.avg_entry_price
        if current_price:
            if float(get_current(ticker_symbol)) <= float(current_price) - (float(current_price) * 0.5/100):
                submit_order(ticker_symbol, 'buy')
                t.sleep(4)
                print('Sell for profit here')
                trades_taken.append(ticker_symbol)
            if float(get_current(ticker_symbol)) >= float(current_price) - (float(current_price) * 0.5/100):
                submit_order(ticker_symbol, 'buy')
                t.sleep(4)
                print('Sell for profit here')
                trades_taken.append(ticker_symbol)



while is_time_between(time(13,30), time(20,00)):
    place_order(ticker_symbol)
    # t.sleep(4)
    if ticker_symbol in trades_taken:
        sys.exit()