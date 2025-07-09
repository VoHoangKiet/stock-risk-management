import pandas as pd
import numpy as np

# Đọc file CSV
df = pd.read_csv("stock_data.csv")

def calculate_var(df: pd.DataFrame, confidence_level=0.95, portfolio_value=1_000_000):
    results = []

    for ticker in df['ticker'].unique():
        ticker_df = df[df['ticker'] == ticker].copy()
        ticker_df['time'] = pd.to_datetime(ticker_df['time'])
        ticker_df = ticker_df.sort_values(by='time')  # type: ignore
        ticker_df.set_index('time', inplace=True)

        # Tính lợi suất hàng ngày
        ticker_df['return'] = ticker_df['close'].pct_change()
        returns = ticker_df['return'].dropna()

        if len(returns) > 0:
            var_pct = np.percentile(returns, (1 - confidence_level) * 100)
            var_amt = abs(var_pct) * portfolio_value
            results.append({
                'ticker': ticker,
                'VaR_pct': var_pct,
                'VaR_amt': var_amt
            })

    return pd.DataFrame(results)

# Reset index nếu bạn đã set time làm index trước đó
df_reset = df.reset_index()

# Gọi hàm tính VaR
var_results = calculate_var(df_reset)
print(var_results)
