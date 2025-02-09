import pandas as pd

data = {"close": [100, 102, 101, 103, 105]}
df = pd.DataFrame(data)
delta = df["close"].diff()

# Assign delta to up and down without copy
up = delta
down = delta

up[up < 0] = 0  # Modifies the original delta
down[down > 0] = 0  # Further modifies the original delta

print(delta)