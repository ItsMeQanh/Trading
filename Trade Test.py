import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Load historical data
data = yf.download('BTC-USD', start='2020-01-01', end='2023-01-01')

# Calculate SMA
def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

data['SMA_50'] = calculate_sma(data, 50)
data['SMA_200'] = calculate_sma(data, 200)

# Calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

data['RSI'] = calculate_rsi(data)

# Implement trading strategy
def implement_strategy(data):
    buy_signals = []
    sell_signals = []
    position = False  # Initially not holding any stock

    for i in range(len(data)):
        if data['SMA_50'][i] > data['SMA_200'][i]:
            if not position:
                buy_signals.append(data['Close'][i])
                sell_signals.append(None)
                position = True
            else:
                buy_signals.append(None)
                sell_signals.append(None)
        elif data['SMA_50'][i] < data['SMA_200'][i]:
            if position:
                buy_signals.append(None)
                sell_signals.append(data['Close'][i])
                position = False
            else:
                buy_signals.append(None)
                sell_signals.append(None)
        else:
            buy_signals.append(None)
            sell_signals.append(None)

    return buy_signals, sell_signals

data['Buy_Signal'], data['Sell_Signal'] = implement_strategy(data)

# Plot data
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(data['SMA_50'], label='50-Day SMA', alpha=0.75)
plt.plot(data['SMA_200'], label='200-Day SMA', alpha=0.75)
plt.scatter(data.index, data['Buy_Signal'], label='Buy Signal', marker='^', color='green')
plt.scatter(data.index, data['Sell_Signal'], label='Sell Signal', marker='v', color='red')
plt.title('Trading Strategy Backtest')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()
