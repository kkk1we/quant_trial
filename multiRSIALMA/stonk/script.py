import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import exp
from datetime import datetime

files = ["./Data/daily_DIS.csv", "./Data/daily_HPQ.csv", "./Data/daily_INTC.csv", "./Data/daily_MSFT.csv", "./Data/daily_NFLX.csv", "./Data/daily_PFE.csv", "./Data/daily_SBUX.csv"]
RSI_LONG_ENTRY = 30
RSI_SHORT_ENTRY = 70
TP = 0.02  # Take profit: 0.8%
SL = 0.005  # Stop loss: 0.5%

def main(data_file, rsi_interval, alma_window):

    def load_file(file_path):
        df = pd.read_csv(file_path, parse_dates=['timestamp'], date_format="%d/%m/%Y")
        df.sort_values(by='timestamp', inplace=True)
        return df

    df = load_file(data_file)

    def add_rsi(df, interval):
        delta = df["close"].diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(interval - 1), min_periods=interval).mean()
        _loss = down.abs().ewm(com=(interval - 1), min_periods=interval).mean()

        RS = _gain / _loss
        df['rsi'] = 100 - (100 / (1 + RS))
        return df

    df = add_rsi(df, rsi_interval)

    def calculate_alma(prices: list, window: int = alma_window, offset: float = 0.85, sigma: float = 6) -> float:
        m = int(offset * (window - 1))
        s = window / sigma
        weights = np.array([exp(-((k - m) ** 2) / (2 * (s ** 2))) for k in range(window)])
        
        if len(prices) < window:
            return None
        weighted_sum = weights * prices[-window:]
        alma = weighted_sum.sum() / weights.sum()
        return alma

    def add_alma_column(df: pd.DataFrame, window: int = alma_window) -> pd.DataFrame:
        alma_values = []
        for i in range(len(df)):
            prices = df['rsi'][:i+1].values
            alma = calculate_alma(prices, window)
            alma_values.append(alma)    

        df['alma'] = alma_values
        return df

    df = add_alma_column(df)

    profit_loss_log = []
    trade_log = []
    open_positions = []
    total_trades = 0
    winning_trades = 0
    days_open_position = 0
    format = "%Y-%m-%d"  # Define the format

    with open("trade_log.txt", "a") as log_file:

        for i, row in df.iterrows():
            close_price = row["close"]
            current_date = row["timestamp"] 
            rsi = row["alma"]

            updated_positions = []
            for position in open_positions:
                if position["type"] == "LONG":
                    tp_price = position["entry"] * (1 + TP)
                    sl_price = position["entry"] * (1 - SL)
                    if close_price >= tp_price or close_price <= sl_price:
                        # Calculate profit/loss
                        result = (
                            (tp_price - position["entry"]) / position["entry"] * 100
                            if close_price >= tp_price
                            else (sl_price - position["entry"]) / position["entry"] * 100
                        )
                        profit_loss_log.append(result)
                        trade_log.append(
                            f"Trade {total_trades + 1}: Entered LONG @ {position['entry']} on {position['entry_date']} "
                            f"and EXITED @ {close_price} on {current_date} for a profit/loss of {result:.2f}%\n"
                        )
                        delta_days = datetime.strptime(current_date, format) - datetime.strptime(position['entry_date'], format) 
                        days_open_position += delta_days.days
                        total_trades += 1
                        if result > 0:
                            winning_trades += 1
                    else:
                        updated_positions.append(position)
                elif position["type"] == "SHORT":
                    tp_price = position["entry"] * (1 - TP)
                    sl_price = position["entry"] * (1 + SL)
                    if close_price <= tp_price or close_price >= sl_price:
                        # Calculate profit/loss
                        result = (
                            (position["entry"] - tp_price) / position["entry"] * 100
                            if close_price <= tp_price
                            else (position["entry"] - sl_price) / position["entry"] * 100
                        )
                        profit_loss_log.append(result)
                        trade_log.append(
                            f"Trade {total_trades + 1}: Entered SHORT @ {position['entry']} on {position['entry_date']} "
                            f"and EXITED @ {close_price} on {current_date} for a profit/loss of {result:.2f}%\n"
                        )
                        delta_days = datetime.strptime(current_date, format) - datetime.strptime(position['entry_date'], format) 
                        days_open_position += delta_days.days
                        total_trades += 1
                        if result > 0:
                            winning_trades += 1
                    else:
                        updated_positions.append(position)

            open_positions = updated_positions

            # Check for new trades
            if rsi < RSI_LONG_ENTRY:
                open_positions.append(
                    {"type": "LONG", "entry": close_price, "entry_date": current_date}
                )
            elif rsi > RSI_SHORT_ENTRY:
                open_positions.append(
                    {"type": "SHORT", "entry": close_price, "entry_date": current_date}
                )

        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

        log_file.write(f"\nSummary Statistics for {data_file} RSI-Interval:{rsi_interval} ALMA:{alma_interval}\n")
        log_file.write("=" * 40 + "\n")
        log_file.write(f"Total Trades: {total_trades}\n")
        log_file.write(f"Win Rate: {win_rate:.2f}%\n")
        log_file.write(f"Total Profit/Loss: {sum(profit_loss_log):.2f}%\n")
        log_file.write(f"Avg P/L per Trade: {(win_rate * TP - (100-win_rate) * SL ):.2f}%\n")
        log_file.write(f"Avg Time in Trade: {days_open_position / total_trades :.2f} Days\n")
        return [(win_rate), (sum(profit_loss_log)), ((win_rate * TP - (100-win_rate) * SL ))]

for data_file in files:
    best = 0
    opti_rsi = 0
    opti_alma = 0
    for rsi_interval in range(7, 15):
        for alma_interval in range(10,31,2):
            res = main(data_file, rsi_interval, alma_interval)
            if res[2] > best:
                opti_rsi = rsi_interval
                opti_alma = alma_interval
                best = res[2]
    print(f"RSI for PL/trade: {opti_rsi} ALMA for PL/trade: {opti_alma}")
