#!/bin/env python3

import requests
import json
import argparse

TradeOgreBooks = 'https://tradeogre.com/api/v1/orders/%s-%s'

parser = argparse.ArgumentParser(description="TradeOgre - Order Books for Trading Pair")

parser.add_argument('coins', help="e.g python3 togrebks.py BTC OXEN", metavar='coin', nargs='+')
args = parser.parse_args()

coin1 = args.coins[0]
coin2 = args.coins[1]

to_response = requests.get(TradeOgreBooks % (coin1, coin2)) 
space=' '

with open('tradeogre.uni') as logoFile:
    logo = logoFile.readlines()
    

if to_response.status_code == 200:
    #print(ku_response.json)
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
        #print("%s.) %s - %s | %s - %s" % (i,togre_buys[i],togre_buys_qty[i], togre_sells[i],togre_sells_qty[i]))
        i += 1
    togre_buys.reverse()
    #togre_sells.reverse()
    togre_buys_qty.reverse()
    #togre_sells_qty.reverse()

          
    #print("                             TradeOgre                             ")
    for line in logo:
        print(8*space,line, end='')
    print("                                                                  ") 
    print("                            %4s - %4s                             " % (coin1, coin2))
    print("_____________BIDS_______________ | ______________ASKS_______________")
    k=0
    for bid,bamt,sell,samt in zip(togre_buys, togre_buys_qty, togre_sells, togre_sells_qty):
        if k == 20:
            break;
        print("%3.8f" % float(bid),space*4,"- %10.4f" %  float(bamt),space*5, " %3.8f" % float(sell), space*4, "-  %9.4f"  %   float(samt))
        k += 1
        
