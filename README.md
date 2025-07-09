# VaR Backtesting System - Hệ thống Kiểm thử Rủi ro Tài chính

## 📋 Mục lục
- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Cách sử dụng](#cách-sử-dụng)
- [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
- [Giải thích thuật toán](#giải-thích-thuật-toán)
- [Kết quả output](#kết-quả-output)
- [Ví dụ thực tế](#ví-dụ-thực-tế)

## 🎯 Giới thiệu

**VaR Backtesting System** là công cụ phân tích rủi ro tài chính chuyên nghiệp, giúp xác định **Value at Risk (VaR)** tối ưu cho từng cổ phiếu thông qua phương pháp backtesting.

### VaR là gì?
**Value at Risk (VaR)** là chỉ số đo lường tổn thất tối đa có thể xảy ra trong một khoảng thời gian nhất định với mức độ tin cậy nhất định.

**Ví dụ:** VaR 95% = -2.5% nghĩa là:
- Với 95% khả năng, tổn thất sẽ không vượt quá 2.5%/ngày
- Chỉ có 5% khả năng tổn thất lớn hơn 2.5%/ngày

### Tại sao cần Backtesting?
- **Kiểm tra độ chính xác** của mô hình VaR
- **Tối ưu hóa confidence level** cho từng cổ phiếu riêng biệt
- **Tuân thủ quy định** Basel II/III trong ngân hàng
- **Quản lý rủi ro** hiệu quả hơn

## 🛠️ Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8+
- Các thư viện trong `requirements.txt`

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Cấu trúc thư mục
```
risk-management/
├── main.py                 # File tính VaR cơ bản
├── backtesting_var.py      # File backtesting chính
├── requirements.txt        # Danh sách thư viện
├── stock_data.csv         # Dữ liệu giá cổ phiếu
├── README.md              # File hướng dẫn này
└── var_backtest_results.csv # Kết quả backtesting (tự tạo)
```

## 🚀 Cách sử dụng

### Chạy backtesting
```bash
python backtesting_var.py
```

### Tùy chỉnh portfolio value
Mở file `backtesting_var.py` và chỉnh sửa:
```python
backtester = VaRBacktester(df, portfolio_value=1_000_000)  # 1 triệu VND
```

### Tùy chỉnh confidence levels
```python
confidence_levels = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
backtester.run_backtest_all_tickers(confidence_levels)
```

## 📊 Cấu trúc dữ liệu

### Input: stock_data.csv
```csv
ticker,time,open,high,low,close,volume
FPT,2023-06-30T00:00:00,62.49,62.57,62.13,62.13,734840
FPT,2023-07-03T00:00:00,62.49,62.71,62.13,62.42,1041108
ACB,2023-06-30T00:00:00,15.37,15.44,15.26,15.37,5152098
...
```

**Các cột bắt buộc:**
- `ticker`: Mã cổ phiếu (VD: FPT, ACB, VNM)
- `time`: Thời gian (ISO format)
- `close`: Giá đóng cửa (để tính return)

### Output: var_backtest_results.csv
```csv
ticker,confidence_level,var_pct,var_amt,total_days,violations,violation_rate,accuracy
FPT,0.95,-0.0287,28700,497,23,0.046,0.954
ACB,0.93,-0.0321,32100,497,35,0.070,0.930
```

## 🧮 Giải thích thuật toán

### 1. Chuẩn bị dữ liệu
```python
def prepare_data(self, ticker: str) -> pd.DataFrame:
    # Lọc dữ liệu theo ticker
    ticker_df = self.df[self.df['ticker'] == ticker].copy()
    
    # Chuyển đổi thời gian
    ticker_df['time'] = pd.to_datetime(ticker_df['time'])
    ticker_df = ticker_df.sort_values(by='time')
    
    # Tính return hàng ngày
    ticker_df['return'] = ticker_df['close'].pct_change()
    ticker_df = ticker_df.dropna()  # Xóa ngày đầu tiên (NaN)
    
    return ticker_df
```

### 2. Tính VaR
```python
def calculate_var(self, returns: pd.Series, confidence_level: float) -> float:
    # VaR = Percentile tương ứng với (1 - confidence_level)
    # VD: Confidence 95% → Percentile 5%
    return float(np.percentile(returns, (1 - confidence_level) * 100))
```

**Công thức:**
- Return = (Giá hôm nay - Giá hôm qua) / Giá hôm qua
- VaR = Percentile((1 - Confidence Level) × 100)

### 3. Backtesting
```python
def backtest_var_single_level(self, ticker: str, confidence_level: float):
    # Tính VaR
    var_pct = self.calculate_var(returns, confidence_level)
    
    # Đếm violations (returns < VaR)
    violations = sum(returns < var_pct)
    violation_rate = violations / total_days
    
    # Tính accuracy
    expected_violation_rate = 1 - confidence_level
    accuracy = 1 - abs(violation_rate - expected_violation_rate)
    
    return results
```

### 4. Tìm Confidence Level tối ưu
```python
def find_optimal_confidence_level(self, ticker: str, confidence_levels: List[float]):
    best_accuracy = -1
    
    for cl in confidence_levels:
        result = self.backtest_var_single_level(ticker, cl)
        if result['accuracy'] > best_accuracy:
            best_accuracy = result['accuracy']
            best_result = result
    
    return best_result
```

**Tiêu chí tối ưu:** Accuracy cao nhất
- Accuracy = 1 - |Violation Rate thực tế - Violation Rate kỳ vọng|
- Càng gần 1 thì mô hình càng chính xác

## 📈 Kết quả output

### 1. Thông tin cho từng ticker

#### a) Thống kê Returns
```
📊 Thống kê returns:
   • Tổng số ngày: 497
   • Return trung bình: 0.0012 (0.12%)
   • Độ lệch chuẩn: 0.0287 (2.87%)
   • Return thấp nhất: -0.0856 (-8.56%)
   • Return cao nhất: 0.0743 (7.43%)
```

#### b) VaR tối ưu
```
🎯 VaR Tối Ưu:
   • Confidence Level: 95.0%
   • VaR (%): -0.0287 (-2.87%)
   • VaR (Amount): 28,700 VND
   • Violations: 23/497 (4.63%)
   • Expected: 5.00%
   • Accuracy: 99.63%
```

#### c) Bảng chi tiết tất cả Confidence Levels
```
📋 Chi tiết tất cả Confidence Levels:
   Conf.Level | VaR (%)    | VaR (VND)      | Violations | Rate    | Accuracy
   ----------------------------------------------------------------------
      90.0%   | -0.0198    |       19,800   |   52/497   |  10.46% |  89.54%
      91.0%   | -0.0213    |       21,300   |   45/497   |   9.05% |  90.95%
      92.0%   | -0.0228    |       22,800   |   41/497   |   8.25% |  91.75%
      93.0%   | -0.0245    |       24,500   |   35/497   |   7.04% |  92.96%
      94.0%   | -0.0265    |       26,500   |   28/497   |   5.63% |  94.37%
   ⭐ 95.0%   | -0.0287    |       28,700   |   23/497   |   4.63% |  95.37%
      96.0%   | -0.0312    |       31,200   |   18/497   |   3.62% |  96.38%
      97.0%   | -0.0342    |       34,200   |   14/497   |   2.82% |  97.18%
      98.0%   | -0.0387    |       38,700   |    9/497   |   1.81% |  98.19%
      99.0%   | -0.0456    |       45,600   |    5/497   |   1.01% |  98.99%
```

### 2. Tóm tắt tổng quan

#### a) Thống kê chung
```
📈 Thống kê chung:
   • Số tickers phân tích: 4
   • Confidence level trung bình: 94.5%
   • Confidence level phổ biến nhất: 95.0%
   • VaR trung bình: -0.0298 (-2.98%)
   • Accuracy trung bình: 95.67%
```

#### b) Phân bố Confidence Level
```
📊 Phân bố Confidence Level:
   • 93.0%: 1 tickers (25.0%)
   • 94.0%: 1 tickers (25.0%)
   • 95.0%: 2 tickers (50.0%)
```

#### c) Ranking rủi ro
```
⚠️  Top 3 rủi ro CAO NHẤT (VaR %):
   • ACB: -0.0356 (-3.56%) - Conf: 94.0%
   • BID: -0.0312 (-3.12%) - Conf: 95.0%
   • FPT: -0.0287 (-2.87%) - Conf: 95.0%

✅ Top 3 rủi ro THẤP NHẤT (VaR %):
   • BCM: -0.0237 (-2.37%) - Conf: 93.0%
   • FPT: -0.0287 (-2.87%) - Conf: 95.0%
   • BID: -0.0312 (-3.12%) - Conf: 95.0%
```

## 💡 Ví dụ thực tế

### Trường hợp 1: Nhà đầu tư cá nhân
**Portfolio:** 10 triệu VND đầu tư vào FPT

**Kết quả VaR 95%:** -2.87%
- **Ý nghĩa:** Với 95% khả năng, tổn thất không vượt quá 287,000 VND/ngày
- **Rủi ro:** Chỉ có 5% khả năng mất hơn 287,000 VND/ngày

### Trường hợp 2: Quỹ đầu tư
**Portfolio:** 1 tỷ VND phân bổ đều 4 cổ phiếu (250 triệu/ticker)

**VaR tổng hợp:**
- FPT: 250M × 2.87% = 7.175M VND
- ACB: 250M × 3.56% = 8.900M VND  
- BID: 250M × 3.12% = 7.800M VND
- BCM: 250M × 2.37% = 5.925M VND

**Tổng VaR:** ~29.8M VND (2.98% portfolio)

### Trường hợp 3: Ngân hàng (Basel III)
**Yêu cầu:** VaR 99% cho trading book

**Kết quả:**
- Tất cả tickers có VaR 99% từ -4.56% đến -5.23%
- Violations rate < 1% (đạt yêu cầu Basel)
- Cần buffer vốn tương ứng

## 🔧 Tùy chỉnh nâng cao

### 1. Thêm ticker mới
Chỉ cần thêm dữ liệu vào `stock_data.csv`:
```csv
VNM,2023-06-30T00:00:00,85.2,85.7,84.8,85.2,1234567
VNM,2023-07-03T00:00:00,85.2,86.1,85.0,85.8,987654
```

### 2. Thay đổi phương pháp tính VaR
Hiện tại sử dụng **Historical Simulation**. Có thể mở rộng:

```python
def calculate_var_parametric(self, returns: pd.Series, confidence_level: float) -> float:
    """VaR Parametric (Normal Distribution)"""
    from scipy.stats import norm
    mean = returns.mean()
    std = returns.std()
    z_score = norm.ppf(1 - confidence_level)
    return mean + z_score * std

def calculate_var_monte_carlo(self, returns: pd.Series, confidence_level: float, simulations: int = 10000) -> float:
    """VaR Monte Carlo Simulation"""
    mean = returns.mean()
    std = returns.std()
    simulated_returns = np.random.normal(mean, std, simulations)
    return float(np.percentile(simulated_returns, (1 - confidence_level) * 100))
```

### 3. Thêm Stress Testing
```python
def stress_test_var(self, ticker: str, stress_scenarios: List[float]) -> Dict:
    """Stress test với các scenarios khủng hoảng"""
    normal_var = self.calculate_var(returns, 0.95)
    
    stress_results = []
    for scenario in stress_scenarios:
        stressed_returns = returns + scenario  # Shock scenario
        stressed_var = self.calculate_var(stressed_returns, 0.95)
        stress_results.append({
            'scenario': scenario,
            'normal_var': normal_var,
            'stressed_var': stressed_var,
            'impact': stressed_var - normal_var
        })
    
    return stress_results
```

## ⚠️ Lưu ý quan trọng

### 1. Giả định của mô hình
- **Dữ liệu lịch sử** đại diện cho tương lai
- **Phân phối returns** không thay đổi theo thời gian
- **Không có autocorrelation** trong returns
- **Market liquidity** đủ để thực hiện giao dịch

### 2. Hạn chế
- **Black Swan events** không được dự đoán
- **Market stress** có thể làm mô hình sai lệch
- **Backtesting** chỉ dựa trên dữ liệu quá khứ
- **Model risk** luôn tồn tại

### 3. Khuyến nghị sử dụng
- **Kết hợp nhiều phương pháp** VaR
- **Regular backtesting** (hàng tháng/quý)
- **Stress testing** định kỳ
- **Professional review** bởi risk manager

## 📞 Hỗ trợ

Nếu gặp vấn đề hoặc cần tùy chỉnh:

1. **Kiểm tra dữ liệu đầu vào** có đúng format
2. **Đảm bảo đủ dữ liệu** (tối thiểu 252 ngày = 1 năm)
3. **Xem log lỗi** trong console
4. **Kiểm tra requirements.txt** đã cài đầy đủ

---

## 📜 Bản quyền

Hệ thống này được phát triển cho mục đích giáo dục và nghiên cứu. Vui lòng sử dụng có trách nhiệm và hiểu rõ rủi ro tài chính trước khi đưa ra quyết định đầu tư.

**⚠️ Disclaimer:** Kết quả VaR chỉ mang tính tham khảo. Không đảm bảo độ chính xác 100% và không chịu trách nhiệm về tổn thất tài chính. # stock-risk-management
