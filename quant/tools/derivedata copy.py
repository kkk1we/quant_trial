import requests
import pandas as pd

# API keys
api_key = "VX3LDRKN25J5R2RX"
api_key2 = "PXPLMS2XU05PJO88"
api_key3 = "KDBRL6FFWUC796RI"

# Fetch stock price data
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY&outputsize=full&apikey={api_key3}'
r = requests.get(url)
data = r.json()

# Fetch RSI data
url2 = f'https://www.alphavantage.co/query?function=RSI&symbol=SPY&interval=daily&time_period=14&series_type=close&apikey={api_key3}'
r2 = requests.get(url2)
data2 = r2.json()

# Validate API responses
if "Time Series (Daily)" not in data or "Technical Analysis: RSI" not in data2:
    print("Error: API response is invalid or incomplete.")
    exit()

# Extract data
time_series = data["Time Series (Daily)"]
technical_analysis_RSI = data2["Technical Analysis: RSI"]

# Get dates
time_series_dates = set(time_series.keys())
rsi_dates = set(technical_analysis_RSI.keys())
common_dates = time_series_dates.intersection(rsi_dates)

# Prepare data for DataFrame
data_list = []
for date in common_dates:
    stats = time_series[date]
    rsi_value = technical_analysis_RSI.get(date, {}).get("RSI", "N/A")
    data_list.append({
        "Date": date,
        "Open": stats["1. open"],
        "High": stats["2. high"],
        "Low": stats["3. low"],
        "Close": stats["4. close"],
        "Volume": stats["5. volume"],
        "RSI": rsi_value,
    })

# Create DataFrame
df = pd.DataFrame(data_list)

# Convert numeric columns to appropriate types
numeric_columns = ["Open", "High", "Low", "Close", "Volume", "RSI"]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert "Date" column to datetime
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date").reset_index(drop=True)

# Calculate SMAs
df["SMA10"] = df["Close"].rolling(window=10).mean()
df["SMA20"] = df["Close"].rolling(window=20).mean()
df["SMA50"] = df["Close"].rolling(window=50).mean()
df["SMA200"] = df["Close"].rolling(window=200).mean()

# Save to CSV
df.to_csv("daily_SNP_full.csv", index=False)

print("CSV file created successfully!")
