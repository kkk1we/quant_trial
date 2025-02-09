
import pandas as pd

# Convert to a DataFrame
df = pd.read_csv("tools/daily_SNP_full.csv")
df = df.iloc[::-1].reset_index(drop=True)
# Add an SMA column for a 3-day period
sma = [10,20,50,200]
for i in sma:
    sma_period = i
    df[f"SMA{sma_period}"] = df["Close"].rolling(window=sma_period).mean()

# Save the data to a CSV for inspection
output_file = "tools/SNP_SMA_calculated.csv"
df.to_csv(output_file, index=False)

df  # Display the DataFrame for reference


