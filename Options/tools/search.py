import pandas as pd
import os
listed =[]
def process_files(folder_path, column_name):
    # List all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):  # Only process CSV files
            file_path = os.path.join(folder_path, filename)

            # Read CSV file
            df = pd.read_csv(file_path)

            # Check if the column exists in the file
            if column_name in df.columns:
                print(f"File: {filename} - Column '{column_name}':")
                listed = df[column_name].tolist() 
                print("-" * 40)  # Separator for readability
            else:
                print(f"File: {filename} - Column '{column_name}' not found!")

# Example usage
folder_path = "C:/Quant/quant_trial/Options/data/puts"  # Change this to your folder path
column_name = "open_interest"  # Column to retrieve

process_files(folder_path, column_name)
