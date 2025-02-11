import pandas as pd
import os 
base_dir = os.path.dirname(__file__)
# Load the CSV into a DataFrame


def accessdata(filepath,searchtopic:str,searchkey:str,query:str):
    validsearchtopic = {"contractID","expiration","strike"}
    validquery = {"last","mark","bid","bid_size","ask","ask_size","volume","open_interest","date","implied_volatility","delta",
                  "gamma","theta","vega","rho"}
    
    if searchtopic in validsearchtopic and query in validquery:
        df = pd.read_csv(filepath, dtype={searchtopic: str})  # Force column as string
        filtered_df = df[df[searchtopic] == searchkey]
        
        if not filtered_df.empty:
            result = filtered_df.iloc[0][query]  # Retrieve the first matching row's query value
            print(f"{query} for {searchtopic} of {searchkey} is {result}")
        else:
            print(f"No matching data found for {searchtopic} = {searchkey}")
        
    else:
        print('no type')

filename = "c2025-02-05"
accessdata(os.path.join(base_dir, f"../data/{filename}.csv"),"strike","165.00","open_interest")
