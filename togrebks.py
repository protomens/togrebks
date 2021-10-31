#!/bin/env python3

import requests
import json
import argparse
from subprocess import call

space=' '


def tradeogre_logo():
    with open('tradeogre.uni') as logoFile:
        logo = logoFile.readlines()
    for line in logo:
        print(8*space,line, end='')
        
def get_tradeogre_order_books(coin1, coin2, args):
    TradeOgreBooks = 'https://tradeogre.com/api/v1/orders/%s-%s'
    to_response = requests.get(TradeOgreBooks % (coin1, coin2)) 

    try:
        trade_amt = float(args.amount)
        target_amt = float(args.target)
    except TypeError as e:
        if trade_amt:
            pass
        if not trade_amt and not target_amt:
            trade_amt = target_amt = None
        else:
            target_amt=None

    if to_response.status_code == 200:  #make sure response was succeeded
        try:
            ToJSON = json.loads(str(to_response.content.decode('utf-8')))
            
        except Exception as e:
            print("error reading JSON: %s" % str(e))
        i = 0
        togre_buys = [ ]
        togre_buys_qty = [ ]
        togre_sells = [ ]
        togre_sells_qty = [ ]
        for key,key2 in zip(ToJSON['buy'].keys(), ToJSON['sell'].keys()):
            togre_buys.append(key)
            togre_buys_qty.append(ToJSON['buy'][key])
            togre_sells.append(key2)
            togre_sells_qty.append(ToJSON['sell'][key2])
            i += 1
        togre_buys.reverse()
        togre_buys_qty.reverse()
              
        tradeogre_logo()
        print("                                                                  ") 
        print("                            %4s - %4s                             " % (coin1, coin2))
        print("_____________BIDS_______________ | ______________ASKS_______________")
        k=0
        for bid,bamt,sell,samt in zip(togre_buys, togre_buys_qty, togre_sells, togre_sells_qty):
            if k == 20:
                break;
            print("%3.8f" % float(bid),space*4,"- %10.4f" %  float(bamt),space*5, " %3.8f" % float(sell), space*4, "-  %9.4f"  %   float(samt))
            k += 1
        if trade_amt:
            expected_value = round(float(trade_amt / float(togre_sells[0])),12)
            print("\n", space*17, "Expected: %3.12f" % float(expected_value), flush=True)    
            minimum_value = round(float(trade_amt / float(togre_sells[-1])),12)
            print("\n", space*18, "Minimum: %3.12f" % float(minimum_value), flush=True)
        if target_amt and trade_amt:
            target_price = round(float(trade_amt / target_amt),12)
            print("\n", space*19, "Target: %3.12f" % float(target_price), flush=True)
        if target_amt and expected_value >= target_amt:
            while True:
                try:
                    call(['aplay', 'sounds/alarm.wav'])
                except:
                    print("alsa-utils not installed")
                    break;
            
    else:
        print("Error retrieving TradeOgre data")
        
    
def main():
    parser = argparse.ArgumentParser(description="TradeOgre - Order Books for Trading Pair")

    parser.add_argument('coins', help="e.g python3 togrebks.py BTC XMR", metavar='coin', nargs='+')
    parser.add_argument('-a', '--amount', help="Enter Amount Wanting to Trade", metavar='amount')
    parser.add_argument('-t', '--target', help="Target Amount Wanting to Receive", metavar='target')
    args = parser.parse_args()
    
    coin1 = args.coins[0]
    coin2 = args.coins[1]
    
    get_tradeogre_order_books(coin1, coin2, args)
    
if __name__ == "__main__":
    main()