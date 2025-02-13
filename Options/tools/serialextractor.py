import pandas as pd
import os
import plotly.express as px

def extract_date_from_filename(filename):
    """Extracts date from filename 'cYYYY-MM-DD.csv'."""
    try:
        return pd.to_datetime(filename[1:-4])  # Convert 'cYYYY-MM-DD.csv' to YYYY-MM-DD
    except Exception as e:
        print(f"Error extracting date from {filename}: {e}")
        return None

def extract_contract_data(folder_path, target_contract):
    """
    Extracts all records for a specific contractID across multiple files.
    Returns a DataFrame containing date, bid, ask, open_interest, implied_volatility, etc.
    """
    contract_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and (filename.startswith("c") or filename.startswith("p")):  # Ensure correct format
            file_path = os.path.join(folder_path, filename)
            observation_date = extract_date_from_filename(filename)  # Extract date from filename

            if observation_date:
                df = pd.read_csv(file_path, dtype={"contractID": str})  # Ensure contractID is a string
                
                # Check if contractID exists in this file
                filtered_df = df[df["contractID"] == target_contract]

                if not filtered_df.empty:
                    for _, row in filtered_df.iterrows():
                        contract_data.append({
                            "date": observation_date,
                            "strike": row["strike"],
                            "implied_volatility": row["implied_volatility"],
                            "open_interest": row["open_interest"],
                            "last_price": row["last"],
                            "bid": row["bid"],
                            "ask": row["ask"]
                        })

    return pd.DataFrame(contract_data)

# 📂 Define your folder path and contractID to extract
ticker = "NVDA"  
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, "..", "data", ticker,"calls")  # Example folder path

target_contract = "NVDA250221C00120000"  # Example contractID to extract

# 🔄 Extract contract data
df_contract = extract_contract_data(folder_path, target_contract)

# ✅ Sort data by date
df_contract = df_contract.sort_values(by="date")
print(df_contract)

# 🎨 Plot Open Interest Over Time (Using Plotly)
fig_oi = px.line(df_contract, x="date", y="open_interest", title=f"Open Interest for {target_contract} Over Time",
                 markers=True, labels={"date": "Date", "open_interest": "Open Interest"})
fig_oi.update_xaxes(tickangle=45, tickformat="%Y-%m-%d")
fig_oi.show()

# 🎨 Plot Implied Volatility Over Time (Using Plotly)
fig_iv = px.line(df_contract, x="date", y="implied_volatility", title=f"Implied Volatility for {target_contract} Over Time",
                 markers=True, labels={"date": "Date", "implied_volatility": "Implied Volatility"})
fig_iv.update_xaxes(tickangle=45, tickformat="%Y-%m-%d")
fig_iv.show()

# 🎨 Plot Bid Prices Over Time (Using Plotly)
fig_bid = px.line(df_contract, x="date", y="bid", title=f"Bid Prices for {target_contract} Over Time",
                  markers=True, labels={"date": "Date", "bid": "Bid Price"})
fig_bid.update_xaxes(tickangle=45, tickformat="%Y-%m-%d")
fig_bid.show()
