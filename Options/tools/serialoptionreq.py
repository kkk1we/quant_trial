import requests
import csv
import pandas as pd
import os
import holidays
base_dir = os.path.dirname(__file__)  # Directory of the current script
# Generate a date range from Jan 1, 2025, to Jan 10, 2025, with a daily interval
key1 = "VX3LDRKN25J5R2RX"
key2 = "S8FOMGX3NKTAIAE5"
key3 = "N0DW464099YOXYKU"
key4 = "E04UB1EK6HGCZMJ6"
key5 = "TJXC12U8ZRUZKXM5"
key6 = "75PE3Y1L869SRF40"
key7 = "8PXIO5S9C053YTZA"
key8 = "1GDJWQ66CS73CKXU"
key9 = "GDHJ264B339W6WKB"
key10 = "RCJK0DH5HDJ3QO60"  
key11 = "GFJ2DIJ50GG0E1UN"
key12 = "CDZ2NJ4QC63X0VGC"
key13 = "J3V04A5ONHAFEYNT"
key14 = "8LZPV7RD2FKB5KHP"
key15 = "FJ5DVNE7A0QP9FGA"
 
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
    write_to_csv(call_option, os.path.join(base_dir, f"../data/{ticker}/calls/c{date}.csv"))
    write_to_csv(put_option, os.path.join(base_dir, f"../data/{ticker}/puts/p{date}.csv"))


# Write to CSV
def write_to_csv(data, filename):
    dir_path = os.path.dirname(filename)
    os.makedirs(dir_path, exist_ok=True)
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


def get_trading_days(startdate,enddate):
    # Step 1: Define US stock market holidays for 2025 only
    us_holidays2025 = holidays.US(years=[2025])
    us_holidays2024 = holidays.US(years=[2024])
    # Step 2: Generate all business days (weekdays only)
    business_days = pd.date_range(start=startdate, end=enddate, freq="B")
    # Step 3: Convert holidays to pandas datetime format
    market_holidays = pd.to_datetime(list(us_holidays2024.keys()))  # Convert holiday dates
    print(market_holidays)
    # Step 4: Exclude holidays from business days
    global trading_days
    trading_days = business_days[~business_days.isin(market_holidays)]
    
#05-10 -> 06-10,20
get_trading_days("2024-04-07","2024-05-09")
symbol = 'SPY'
count = 0
for date in trading_days:
    datestr = date.strftime("%Y-%m-%d")
    req_write_data(key13,datestr,symbol)
    print(date)
    count +=1
    print(count)

print('file created')