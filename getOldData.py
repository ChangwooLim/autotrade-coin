import pandas as pd
import pyupbit
from datetime import datetime, time, date, timedelta
from calendar import monthrange
from time import sleep

apikey=open("api-key", "r")
access=apikey.readline().strip()
secret=apikey.readline().strip()
apikey.close()

upbit = pyupbit.Upbit(access, secret)

def get_upbit_ohlcv(now, ticker, year, month):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])

    # 해당 년월 1일부터
    from_date = date(year, month, 1)

    # 해당 년월 마지막 일(28일, 30일, 31일)
    end_day = monthrange(year, month)[1]
    to_date = date(year, month, end_day)
    
    # 해당 년월 마지막 일자가 현재 프로그램 수행일자보다 큰 경우
    if to_date >= now.date():
        to_date = now.date()
        end_day = to_date.day

    temp_list = []
    # 해당 년월 1일부터 말일(또는 프로그램 수행일자)까지 데이터 수집 실시
    for day in range(1, end_day+1):
        cnt = 200 # default
        base_time = datetime.combine(from_date, time(3, 20, 0))
        # print(base_time)
        for i in range(8):
            print(f"Getting Data {year} {month} {base_time}")
            try:
                df_temp = pyupbit.get_ohlcv(ticker, interval='minute1', count=cnt, to=base_time)
                # print(i, 'base_time:', base_time, 'shape:', df_temp.shape)
                df = pd.concat([df, df_temp], axis=0)
                if i == 6:
                    base_time += timedelta(hours=0, minutes=40)
                else:
                    base_time += timedelta(hours=3, minutes=20)
            except Exception as e:
                print('Exception:', e)
            
        from_date = from_date + timedelta(days=1)
        sleep(0.5)

    return df

def getSpecificMonthData(now, ticker, year, month):
  YYYYMM = str(year) + '{0:02d}'.format(month)
  end_day = monthrange(year, month)[1]

  df = get_upbit_ohlcv(now=now, ticker=ticker, year=year, month=month)

  df.reset_index(inplace=True)
  df.drop_duplicates('index', inplace=True)
  df = df[(datetime.combine(date(year, month, 1), time(0, 0, 0)) <= df['index']) & (df['index'] <= datetime.combine(date(year, month, end_day), time(23, 59, 59)))]

  fileName = '{}_{}_ohlcv.csv'.format(YYYYMM, ticker)
  df.to_csv('./data/'+fileName, index=None)

year = 2022
month = 12
now = datetime.now()

end_day = monthrange(year, month)[1]
ticker="KRW-BTC"

for i in range (1, 13):
  getSpecificMonthData(now, ticker, year, i)
  print(f"{year}년 {i}월 완료.")
