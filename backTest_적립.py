import pyupbit
import pandas as pd

# apikey=open("api-key", "r")
# access=apikey.readline().strip()
# secret=apikey.readline().strip()
# apikey.close()

# upbit = pyupbit.Upbit(access, secret)

df=pd.read_csv("./data/201901-20220217.csv")

bitcoin=0
buy=True
buyprice=0
buyleverage=0
money=0
allmoney=0

def Sell(now, ticker="KRW-BTC", amount="all"):
  global money
  global bitcoin
  global buyleverage
  global buyprice

  if amount == "all":
    money=(now.open-buyprice)*0.9995*bitcoin*buyleverage+buyprice*bitcoin+money
    bitcoin=0
  
  
def Buy(now, ticker="KRW-BTC", amount="all", leverage=1):
  global money
  global bitcoin
  global buyleverage
  global buyprice
  
  if amount=="all":
    bitcoin=bitcoin+money/now.open*0.9995
    money=0
    buyprice=now.open
    buyleverage=leverage
  else:
    bitcoin=bitcoin+money/now.open*0.9995
    money=0
    
  print(f"Sell and buy at {now['index']} at {now.open} 이익율 {bitcoin*now.open/allmoney*100} 현재비트코인: {bitcoin}")

flowup=0
flowdown=0
for loc in range(1,len(df)):
  if df.iloc[loc]['index'][8:19]=='01 00:01:00': 
    money=money+1000000
    allmoney=allmoney+1000000
    print("Money Added")

  if df.iloc[loc].open>=df.iloc[loc-1].open:
    flowup=flowup+1
    if flowdown>=1: flowdown=flowdown-1
  else:
    flowdown=flowdown+1
    if flowup>=1: flowup=flowup-1

  if flowup>=10 and buyleverage<=0:
    Sell(df.iloc[loc])
    Buy(df.iloc[loc], leverage=1)
    flowup=0

  if flowdown>=10 and buyleverage>=0:
    Sell(df.iloc[loc])
    Buy(df.iloc[loc], leverage=-1)
    flowdown=0

  
  #print(df.iloc[loc].open)
  # if (df.iloc[loc].open>=df.iloc[loc-1440].open*1.03) & (buy==False):
  #   money=money*(df.iloc[loc].open/df.iloc[loc-1440].open)
  #   money=money*0.9995
  #   buy=True
  #   print(f"Buy at {df.iloc[loc]['index']} 수익률 {money/10000}")
  # elif (df.iloc[loc].open<=df.iloc[loc-1440].open*0.98) & (buy==True):
  #   money=money*(df.iloc[loc].open/df.iloc[loc-1440].open)
  #   money=money*0.9995
  #   buy=False
  #   print(f"Sell at {df.iloc[loc]['index']} 수익률 {money/10000}")