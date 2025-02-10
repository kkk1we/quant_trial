# import holidays
# import pandas as pd
# from pandas.tseries.offsets import CustomBusinessDay
# dates = pd.date_range(start="2025-01-01", end="2025-01-10", freq="B")
# us_bd = CustomBusinessDay(holidays=us_holidays)
# print(dates)

# print(dates[0].strftime("%Y-%m-%d"))
# print(dates[1])

# trading_days = pd.date_range(start="2025-01-01", end="2025-12-31", freq=us_bd)


# print(trading_days[:10])


import pandas as pd
import holidays
#years=[2025]
# Step 1: Define US stock market holidays for 2025 only
us_holidays = holidays.US(years=[2025])  # Ensure only 2025 holidays are included

# Step 2: Generate all business days (weekdays only)
business_days = pd.date_range(start="2025-01-01", end="2025-12-31", freq="B")

# Step 3: Convert holidays to pandas datetime format
market_holidays = pd.to_datetime(list(us_holidays.keys()))  # Convert holiday dates
print(market_holidays)
# Step 4: Exclude holidays from business days
trading_days = business_days[~business_days.isin(market_holidays)]

# Debugging: Print first 10 trading days and check if "2025-01-01" is present
print(trading_days[:10])
print("2025-01-01 in trading_days:", "2025-01-01" in trading_days.strftime("%Y-%m-%d"))
