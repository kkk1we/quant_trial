import requests
import csv
import holidays

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=SPY&date=2025-02-07&apikey=S8FOMGX3NKTAIAE5'
r = requests.get(url)
data = r.json()

# Extract the SMA data
optiondata = data["data"]

# Write to CSV
def write_to_csv(data, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["contractID",
                "symbol",
                "expiration",
                "strike",
                "type",
                "last",
                "mark",
                "bid",
                "bid_size",
                "ask",
                "ask_size",
                "volume",
                "open_interest",
                "date",
                "implied_volatility",
                "delta",
                "gamma",
                "theta",
                "vega",
                "rho"])
        # Write rows
        for row in data:
            writer.writerow([
                row["contractID"],
                row["symbol"],
                row["expiration"],
                row["strike"],
                row["type"],
                row["last"],
                row["mark"],
                row["bid"],
                row["bid_size"],
                row["ask"],
                row["ask_size"],
                row["volume"],
                row["open_interest"],
                row["date"],
                row["implied_volatility"],
                row["delta"],
                row["gamma"],
                row["theta"],
                row["vega"],
                row["rho"]
            ])

# call_options = [row for row in data if row["type"].lower() == "call"]
# put_options = [row for row in data if row["type"].lower() == "put"]
call_option = []
put_option = []
for i in range(len(optiondata)):
    type = optiondata[i].get("type")
    if type == "call":
        call_option.append(optiondata[i])
    else:
        put_option.append(optiondata[i])

write_to_csv(call_option, 'call.csv')
write_to_csv(put_option, 'put.csv')
print('file created')

print(data)