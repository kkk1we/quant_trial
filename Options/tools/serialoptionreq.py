import requests
import csv
import pandas as pd
import os
import holidays
base_dir = os.path.dirname(__file__)  # Directory of the current script
# Generate a date range from Jan 1, 2025, to Jan 10, 2025, with a daily interval

optiondata = []

def req_write_data(apikey,date,ticker):
    call_option = []
    put_option = []
    url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}&date={date}&apikey={apikey}'
    r = requests.get(url)
    data = r.json()
    optiondata = data["data"]
    for i in range(len(optiondata)):
        type = optiondata[i].get("type")
        if type == "call":
            call_option.append(optiondata[i])
        else:
            put_option.append(optiondata[i])
    write_to_csv(call_option, os.path.join(base_dir, f"../data/c{date}.csv"))
    write_to_csv(put_option, os.path.join(base_dir, f"../data/p{date}.csv"))


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
# Step 1: Define US stock market holidays for 2025 only
us_holidays2025 = holidays.US(years=[2025])
us_holidays2024 = holidays.US(years=[2024])
# Step 2: Generate all business days (weekdays only)
business_days = pd.date_range(start="2025-01-25", end="2025-02-06", freq="B")
# Step 3: Convert holidays to pandas datetime format
market_holidays = pd.to_datetime(list(us_holidays2025.keys()))  # Convert holiday dates
print(market_holidays)
# Step 4: Exclude holidays from business days
trading_days = business_days[~business_days.isin(market_holidays)]
# Debugging: Print first 10 trading days and check if "2025-01-01" is present
print(trading_days[:10])
print("2025-01-01 in trading_days:", "2025-01-01" in trading_days.strftime("%Y-%m-%d"))


for date in trading_days:
    datestr = date.strftime("%Y-%m-%d")
    req_write_data('VX3LDRKN25J5R2RX',datestr,'NVDA')

print('file created')