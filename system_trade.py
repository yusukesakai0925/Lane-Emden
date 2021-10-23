import pybitflyer
import numpy as np
import pandas as pd
import time
from datetime import datetime
#from ipywidgets import FloatProgress
#from IPython.display import display, clear_output

# 成行買い注文
def buy_btc_mkt(amt):
    amt = int(amt*100000000)/100000000
    buy = api.sendchildorder(product_code="BTC_JPY", child_order_type="MARKET", side="BUY", size=amt, minute_to_expire=10, time_in_force="GTC")
    print("BUY ", amt, "BTC")
    print(buy)

# 成行売り注文
def sell_btc_mkt(amt):
    amt = int(amt*100000000)/100000000
    sell = api.sendchildorder(product_code="BTC_JPY", child_order_type="MARKET", side="SELL", size=amt, minute_to_expire=10, time_in_force="GTC")
    print("SELL ", amt, "BTC")
    print(sell)

# 指値買い注文
def buy_btc_lmt(amt, prc):
    amt = int(amt*100000000)/100000000
    buy = api.sendchildorder(product_code="BTC_JPY", child_order_type="LIMIT", price=prc, side="BUY", size=amt, minute_to_expire=10, time_in_force="GTC")
    print("BUY ", amt, "BTC")
    print(buy)

# 指値売り注文
def sell_btc_lmt(amt, prc):
    amt = int(amt*100000000)/100000000
    sell = api.sendchildorder(product_code="BTC_JPY", child_order_type="LIMIT", price=prc, side="SELL", size=amt, minute_to_expire=10, time_in_force="GTC")
    print("SELL ", amt, "BTC")
    print(sell)


def boli_algo(jpy,btc,tick):
    fee=0.0015
    
    if tick["ltp"]<ltps2.mean()-2*ltps2.std() and jpy>0 and ltps2.std*4>tick["ltp"]*fee:
        buy_btc_lmt((jpy)/2,tick["ltp"]*0.9999)
        logfile=open("logfile.txt", "w")
        logfile.write("buy\n")
        logfile.close()
        return 1
        
    elif tick["ltp"]>ltps2.mean()+2*ltps2.std() and btc>0 and ltps2.std*4>["ltp"]*fee:
        sell_btc_lmt((btc)/2,tick["ltp"]*1.0001)
        logfile=open("logfile.txt", "w")
        logfile.write("sell\n")
        logfile.close()
        return 1
  
    else:
        logfile=open("logfile.txt", "w")
        logfile.write("do nothing\n")
        logfile.close()
        return 0


api=pybitflyer.API(api_key="AH2xvJotMVV1Fgk5s5x81D",api_secret="XDoZZotEsY0Zd4HwVoRU6gqmwgRBdaBxarMdh2ssXnA=")


cnt=0


# 最終取引価格, 移動平均, 標準偏差を格納する配列
raws = []
sma1, sma2 = [], []
sgm1, sgm2 = [], []

# 移動平均を取る幅
itr1 = 30 # 15 mins
itr2 = 120  # 60 mins

# 60分間の最終取引価格の配列
current_price = api.ticker(product_code = "BTC_JPY")['ltp']
ltps2 = current_price*np.ones(itr2) 


while True:
    # 30秒ごとに稼働
    if datetime.now().strftime('%S') [0:2]== '00' or '30':
        tick = api.ticker(product_code = "BTC_JPY")
        # 最終取引価格の更新
        ltps2 = np.hstack((ltps2[1:itr2], tick['ltp']))
        ltps1 = ltps2[itr2-itr1:itr2]
        # プロット用データの更新
        raws = np.append(raws, [ltps1[itr1-1]])
        sma1 = np.append(sma1, [ltps1.mean()])
        sma2.append(ltps2.mean())
        sgm1 = np.append(sgm1, [ltps1.std()])
        sgm2 = np.append(sgm2, [ltps2.std()])

        
        balance=api.getbalance()
        jpy=balance[0]["available"]
        btc=balance[1]["available"]
        
        status=0
        cnt=cnt+1
        if status==0 and cnt>120:
            status=boli_algo(jpy,btc,tick)
        
        time.sleep(27)