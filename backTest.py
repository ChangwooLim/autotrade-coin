import pyupbit
import pandas as pd

# apikey=open("api-key", "r")
# access=apikey.readline().strip()
# secret=apikey.readline().strip()
# apikey.close()

# upbit = pyupbit.Upbit(access, secret)

df=pd.read_csv("./data/201901-20220217.csv")

money=1000000
bitcoin=0
buy=False
buyprice=0
buyleverage=0
allmoney=1000000

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
    
flowup=0
flowdown=0
for loc in range(1441,len(df)): 
  if df.iloc[loc]['index'][8:19]=='01 00:01:00': 
    money=money+1000000
    allmoney=allmoney+1000000
    print("Money Added")
    print(f"현재자산: {money}원 비트코인 {bitcoin}개")
  
  if (buy==False) & (df.iloc[loc].open>=df.iloc[loc-1440].open*1.015):
    Buy(df.iloc[loc], leverage=1)
    buy=True
    value=(money+bitcoin*df.iloc[loc].open)
    print(f"Buy at {df.iloc[loc]['index']} 수익률 {value/allmoney} 레버리지 {buyleverage}")
  elif (buy==False) & (df.iloc[loc].open<=df.iloc[loc-1440].open*0.985):
    Buy(df.iloc[loc], leverage=-1)
    buy=True
    value=(money+bitcoin*df.iloc[loc].open)
    print(f"Buy at {df.iloc[loc]['index']} 수익률 {value/allmoney} 레버리지 {buyleverage}")

  if (buy==True) & ((df.iloc[loc].open>=buyprice*1.015) | (df.iloc[loc].open<=buyprice*0.985)):
    print(f"Sell at {df.iloc[loc]['index']}")
    Sell(df.iloc[loc])
    buy=False



  
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