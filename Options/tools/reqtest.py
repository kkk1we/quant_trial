import requests
import csv
import pandas as pd

url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=SPY&date=2025-01-09&apikey=VX3LDRKN25J5R2RX'
r = requests.get(url)
data = r.json()
optiondata = data["data"]

print(optiondata)