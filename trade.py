from ast import AsyncFunctionDef
import pyupbit

apikey=open("api-key", "r")
access=apikey.readline().strip()
secret=apikey.readline().strip()
apikey.close()

#업비트 연결
upbit = pyupbit.Upbit(access, secret)

balance = upbit.get_balances()
print(balance)

ticker=pyupbit.get_tickers()
print(ticker, len(ticker))


print(pyupbit.get_current_price("KRW-BTC"))
