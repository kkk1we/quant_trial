import pandas as pd
import os
import csv
def check_contract_in_files(folder_path, target_contract):
    """Checks if the target contract ID exists in each CSV file with advanced debugging."""
    contract_presence = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and filename.startswith("p"):  # Ensure correct format
            file_path = os.path.join(folder_path, filename)

            try:
                # 🛠 Read CSV with encoding handling
                df = pd.read_csv(file_path, dtype={"contractID": str}, encoding="utf-8")
                df.columns = df.columns.str.strip()  # Remove spaces from column names

                # 🛠 Debug: Print column names
                print(f"\n📂 Checking file: {filename}")
                print(f"🔹 Columns found: {df.columns.tolist()}")

                # 🛠 Ensure 'contractID' exists
                if "contractID" not in df.columns:
                    print(f"⚠️ ERROR: 'contractID' column missing in {filename}. Skipping.")
                    continue

                # 🛠 Normalize contract IDs
                df["contractID"] = df["contractID"].astype(str).str.strip()
                df["contractID"] = df["contractID"].str.replace("\u200b", "", regex=True)  # Remove zero-width spaces
                df["contractID"] = df["contractID"].str.encode("utf-8").str.decode("utf-8")  # Fix encoding issues
                df["contractID"] = df["contractID"].apply(lambda x: str(int(float(x))) if x.replace(".", "", 1).isdigit() else x)

                # 🛠 Debug: Print first 5 contract IDs
                print("🔍 First few contract IDs in this file:", df["contractID"].head(5).tolist())

                # 🛠 Debug: Check exact string match
                print(f"🔍 Target ContractID: '{target_contract}' | Length: {len(target_contract)}")
                for contract in df["contractID"].unique():
                    print(f"🔹 CSV ContractID: '{contract}' | Length: {len(contract)}")

                # 🛠 Check if contract ID exists
                matches = df["contractID"] == target_contract
                count = matches.sum()  # Count occurrences

                contract_presence[filename] = count  # Store count instead of just True/False

            except Exception as e:
                print(f"⚠️ Error reading {filename}: {e}")

    return contract_presence

# 📂 Define folder path and target contract ID
folder_path = "C:/Quant/quant_trial/Options/data/puts"
target_contract = "NVDA250221P00124000"

# 🔄 Check presence in all files
contract_results = check_contract_in_files(folder_path, target_contract)

# 📊 Print Results
print(f"\n🔍 **Checking for Contract ID: {target_contract}**\n")
for file, count in contract_results.items():
    status = f"✅ Found {count} times" if count > 0 else "❌ Not Found"
    print(f"{file}: {status}")
