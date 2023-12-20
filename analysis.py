import pandas as pd
import yfinance as yf
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

stocks = pd.read_csv("all_stocks.csv")
results_stock = []

for i, row in stocks.iterrows():
    ticker = row["Symbol"]

    try:
        data = yf.download(f"{ticker}.NS")
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        continue

    try:
        pivot_point = (data['High'][-1] + data['Low'][-1] + data['Close'][-1]) / 3
        support_l1 = (pivot_point * 2) - data['High'][-1]
        support_l2 = pivot_point - (data['High'][-1] - data['Low'][-1])
        resistance_l1 = (pivot_point * 2) - data['Low'][-1]
        resistance_l2 = pivot_point + (data['High'][-1] - data['Low'][-1])
        
        results_stock.append({
                "Ticker": ticker,
                "LTP": data["Close"][-1],
                'Support Level 1': support_l1,
                'Support Level 2': support_l2,
                'Pivot Point': pivot_point,
                'Resistance Level 1': resistance_l1,
                'Resistance Level 2': resistance_l2
        })
    
    except Exception as e:
        continue

result_df = pd.DataFrame(results_stock)
filterd_df = result_df[result_df["LTP"] <= result_df['Support Level 1']]
print(filterd_df)