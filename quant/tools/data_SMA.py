import requests
import csv
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SMA&symbol=SPY&interval=daily&time_period=20&series_type=close&apikey=VX3LDRKN25J5R2RX'
r = requests.get(url)
data = r.json()


# Extract the SMA data
sma_data = data["Technical Analysis: SMA"]

# Write to CSV

with open("daily_SNP_closeSMA.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Date", "SMA"])
    # Write rows
    for date, value in sma_data.items():
        writer.writerow([date, value["SMA"]])

print('file created')

print(data)