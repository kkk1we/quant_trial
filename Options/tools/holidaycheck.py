import pandas as pd
import holidays
import csv
import pandas as pd
import os
base_dir = os.path.dirname(__file__)
#years=[2025]
# Step 1: Define US stock market holidays for 2025 only
us_holidays24 = holidays.US(years=[2024])  # Ensure only 2025 holidays are included
us_holidays25 = holidays.US(years=[2025])
# Step 2: Generate all business days (weekdays only)
business_days = pd.date_range(start="2025-01-01", end="2025-12-31", freq="B")
print(business_days)
# Step 3: Convert holidays to pandas datetime format
market_holidays = pd.to_datetime(list(us_holidays25.keys()))  # Convert holiday dates
print(market_holidays)
# Step 4: Exclude holidays from business days
trading_days = business_days[~business_days.isin(market_holidays)]
formatted_trading_days = trading_days.strftime("%Y-%m-%d")
# Debugging: Print first 10 trading days and check if "2025-01-01" is present
print(trading_days[:10])
print("2025-01-01 in trading_days:", "2025-01-01" in trading_days.strftime("%Y-%m-%d"))


with open(os.path.join(base_dir, f"../data/hol25.csv"), "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(formatted_trading_days)