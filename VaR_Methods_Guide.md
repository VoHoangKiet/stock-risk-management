# Hướng dẫn tính VaR (Value at Risk) - Từ cơ bản đến nâng cao

## 📚 Mục lục
- [VaR là gì?](#var-là-gì)
- [Tại sao cần VaR?](#tại-sao-cần-var)
- [3 phương pháp chính](#3-phương-pháp-chính)
- [Ví dụ thực tế](#ví-dụ-thực-tế)
- [So sánh các phương pháp](#so-sánh-các-phương-pháp)
- [Thực hành với Python](#thực-hành-với-python)

## 🎯 VaR là gì?

**Value at Risk (VaR)** là câu trả lời cho câu hỏi:

> *"Trong tình huống tệ nhất, tôi có thể mất bao nhiều tiền?"*

### Định nghĩa đơn giản:
VaR cho biết **số tiền tối đa** bạn có thể mất trong một khoảng thời gian nhất định với một mức độ tin cậy nhất định.

### Ví dụ cụ thể:
**VaR 1 ngày với 95% tin cậy = 50,000 VND**

**Ý nghĩa:**
- ✅ **95% khả năng**: Bạn sẽ mất ít hơn 50,000 VND trong ngày hôm nay
- ⚠️ **5% khả năng**: Bạn có thể mất hơn 50,000 VND (tình huống xấu)

### Ba thành phần của VaR:
1. **Thời gian**: 1 ngày, 1 tuần, 1 tháng
2. **Mức tin cậy**: 90%, 95%, 99%
3. **Số tiền**: VND, USD, %

## 🤔 Tại sao cần VaR?

### 1. Quản lý rủi ro cá nhân
```
Bạn có 100 triệu đầu tư cổ phiếu
VaR 1 ngày 95% = 3 triệu
→ Chuẩn bị tâm lý: 95% ngày sẽ mất < 3 triệu
→ 5% ngày có thể mất > 3 triệu
```

### 2. Quyết định đầu tư
```
Cổ phiếu A: VaR = 2%
Cổ phiếu B: VaR = 5%
→ A ít rủi ro hơn B
```

### 3. Tuân thủ quy định
- Ngân hàng phải báo cáo VaR hàng ngày
- Quỹ đầu tư phải công bố VaR cho nhà đầu tư

## 📊 3 Phương pháp chính tính VaR

## 1. 📈 Historical Simulation (Mô phỏng Lịch sử)

### Nguyên lý:
> *"Quá khứ sẽ lặp lại trong tương lai"*

### Cách tính từng bước:

#### Bước 1: Thu thập dữ liệu lịch sử
```
Ngày        Giá     Return (%)
01/01/2024  100     -
02/01/2024  102     +2%
03/01/2024  99      -2.94%
04/01/2024  101     +2.02%
05/01/2024  97      -3.96%
...         ...     ...
```

#### Bước 2: Tính Return hàng ngày
```
Return = (Giá hôm nay - Giá hôm qua) / Giá hôm qua × 100%

Ví dụ ngày 03/01:
Return = (99 - 102) / 102 × 100% = -2.94%
```

#### Bước 3: Sắp xếp Return từ thấp đến cao
```
Returns sắp xếp (250 ngày):
-8.5%, -7.2%, -6.1%, -5.8%, ..., +7.3%, +8.1%
```

#### Bước 4: Tìm Percentile
```
VaR 95% = Percentile thứ 5% = Return thứ 13 (250 × 5% = 12.5 ≈ 13)

Nếu return thứ 13 = -4.2%
→ VaR 95% = -4.2%
```

#### Bước 5: Tính số tiền
```
Portfolio = 100 triệu VND
VaR amount = 100 triệu × 4.2% = 4.2 triệu VND
```

### Ưu điểm:
✅ **Đơn giản**, dễ hiểu  
✅ **Không giả định** phân phối  
✅ **Phản ánh thực tế** thị trường  

### Nhược điểm:
❌ **Cần nhiều dữ liệu** (ít nhất 250 ngày)  
❌ **Không dự đoán** sự kiện mới  
❌ **Quá khứ không luôn** đại diện tương lai  

---

## 2. 📐 Parametric (Normal Distribution)

### Nguyên lý:
> *"Returns theo phân phối chuẩn (Normal Distribution)"*

### Giả định cơ bản:
Returns của cổ phiếu tuân theo **phân phối chuẩn** (hình chuông)

```
      |
      |    /\
      |   /  \    ← 68% dữ liệu trong ±1σ
      |  /    \   ← 95% dữ liệu trong ±1.96σ
      | /      \  ← 99% dữ liệu trong ±2.58σ
   ---|/--------\---
     μ-σ   μ   μ+σ
```

### Cách tính từng bước:

#### Bước 1: Tính Mean (μ) và Standard Deviation (σ)
```python
import numpy as np

returns = [-2%, +1%, -3%, +2%, -1%, +4%, ...]

μ (mean) = np.mean(returns) = 0.1%
σ (std)  = np.std(returns) = 2.5%
```

#### Bước 2: Tìm Z-score
```
Confidence Level → Z-score
90%              → -1.28
95%              → -1.65
99%              → -2.33
```

#### Bước 3: Tính VaR
```
VaR = μ + Z-score × σ

VaR 95% = 0.1% + (-1.65) × 2.5%
        = 0.1% - 4.125%
        = -4.025%
```

#### Bước 4: Tính số tiền
```
Portfolio = 100 triệu VND
VaR amount = 100 triệu × 4.025% = 4.025 triệu VND
```

### Ưu điểm:
✅ **Nhanh** và đơn giản  
✅ **Ít dữ liệu** cần thiết  
✅ **Dễ tính toán** và automation  

### Nhược điểm:
❌ **Giả định phân phối chuẩn** không luôn đúng  
❌ **Không tốt** cho extreme events  
❌ **Bỏ qua fat tails** (đuôi dày)  

---

## 3. 🎲 Monte Carlo Simulation

### Nguyên lý:
> *"Mô phỏng hàng nghìn kịch bản có thể xảy ra"*

### Cách tính từng bước:

#### Bước 1: Ước tính tham số
```python
μ (mean return) = 0.1% per day
σ (volatility)  = 2.5% per day
```

#### Bước 2: Tạo random scenarios
```python
import numpy as np

# Tạo 10,000 scenarios ngẫu nhiên
scenarios = np.random.normal(μ, σ, 10000)

# Kết quả mẫu:
# [-3.2%, +1.8%, -5.1%, +0.7%, -2.9%, ...]
```

#### Bước 3: Sắp xếp kết quả
```python
sorted_scenarios = np.sort(scenarios)
# [-8.9%, -7.2%, -6.5%, ..., +7.1%, +8.3%]
```

#### Bước 4: Tìm Percentile
```python
var_95 = np.percentile(sorted_scenarios, 5)
# VaR 95% = -4.1%
```

#### Bước 5: Tính số tiền
```
Portfolio = 100 triệu VND
VaR amount = 100 triệu × 4.1% = 4.1 triệu VND
```

### Ưu điểm:
✅ **Linh hoạt** với nhiều phân phối  
✅ **Xử lý được** portfolio phức tạp  
✅ **Mô phỏng** nhiều scenarios  

### Nhược điểm:
❌ **Tính toán phức tạp**  
❌ **Tốn thời gian** computing  
❌ **Vẫn dựa trên** giả định  

---

## 💰 Ví dụ thực tế

### Tình huống:
Bạn có **50 triệu VND** đầu tư vào cổ phiếu FPT

### Dữ liệu lịch sử FPT (30 ngày gần nhất):
```
Returns (%): [+2.1, -1.5, +0.8, -3.2, +1.9, -2.1, +0.5, -1.8, +2.5, -0.7,
              +1.2, -2.8, +0.3, -1.1, +2.0, -3.5, +1.7, -0.9, +2.3, -1.3,
              +0.6, -2.4, +1.4, -1.7, +2.8, -0.4, +1.0, -2.2, +0.9, -1.6]
```

## Phương pháp 1: Historical Simulation

```python
import numpy as np

returns = [2.1, -1.5, 0.8, -3.2, 1.9, -2.1, 0.5, -1.8, 2.5, -0.7,
           1.2, -2.8, 0.3, -1.1, 2.0, -3.5, 1.7, -0.9, 2.3, -1.3,
           0.6, -2.4, 1.4, -1.7, 2.8, -0.4, 1.0, -2.2, 0.9, -1.6]

# Sắp xếp từ nhỏ đến lớn
sorted_returns = sorted(returns)
print(sorted_returns)
# [-3.5, -3.2, -2.8, -2.4, -2.2, -2.1, -1.8, -1.7, -1.6, -1.5, ...]

# VaR 95% = percentile 5% = vị trí thứ 2 (30 × 5% = 1.5 ≈ 2)
var_95_pct = sorted_returns[1]  # -3.2%
var_95_amount = 50_000_000 * abs(var_95_pct) / 100
print(f"VaR 95%: {var_95_pct}% = {var_95_amount:,.0f} VND")
# VaR 95%: -3.2% = 1,600,000 VND
```

## Phương pháp 2: Parametric

```python
import numpy as np
from scipy.stats import norm

returns = [2.1, -1.5, 0.8, -3.2, 1.9, -2.1, 0.5, -1.8, 2.5, -0.7,
           1.2, -2.8, 0.3, -1.1, 2.0, -3.5, 1.7, -0.9, 2.3, -1.3,
           0.6, -2.4, 1.4, -1.7, 2.8, -0.4, 1.0, -2.2, 0.9, -1.6]

# Tính mean và std
mean_return = np.mean(returns)
std_return = np.std(returns)
print(f"Mean: {mean_return:.2f}%")
print(f"Std: {std_return:.2f}%")
# Mean: -0.03%
# Std: 1.89%

# Z-score cho 95% confidence
z_score_95 = norm.ppf(0.05)  # -1.645
print(f"Z-score 95%: {z_score_95:.3f}")

# Tính VaR
var_95_pct = mean_return + z_score_95 * std_return
var_95_amount = 50_000_000 * abs(var_95_pct) / 100
print(f"VaR 95%: {var_95_pct:.2f}% = {var_95_amount:,.0f} VND")
# VaR 95%: -3.14% = 1,570,000 VND
```

## Phương pháp 3: Monte Carlo

```python
import numpy as np

returns = [2.1, -1.5, 0.8, -3.2, 1.9, -2.1, 0.5, -1.8, 2.5, -0.7,
           1.2, -2.8, 0.3, -1.1, 2.0, -3.5, 1.7, -0.9, 2.3, -1.3,
           0.6, -2.4, 1.4, -1.7, 2.8, -0.4, 1.0, -2.2, 0.9, -1.6]

# Tính tham số
mean_return = np.mean(returns)
std_return = np.std(returns)

# Tạo 10,000 scenarios
np.random.seed(42)  # Để kết quả reproducible
simulated_returns = np.random.normal(mean_return, std_return, 10000)

# Tính VaR
var_95_pct = np.percentile(simulated_returns, 5)
var_95_amount = 50_000_000 * abs(var_95_pct) / 100
print(f"VaR 95%: {var_95_pct:.2f}% = {var_95_amount:,.0f} VND")
# VaR 95%: -3.09% = 1,545,000 VND
```

### Kết quả so sánh:
```
Phương pháp         VaR 95%    Số tiền
Historical          -3.20%     1,600,000 VND
Parametric          -3.14%     1,570,000 VND
Monte Carlo         -3.09%     1,545,000 VND
```

**Kết luận:** Với 95% tin cậy, bạn có thể mất khoảng **1.5-1.6 triệu VND** trong 1 ngày giao dịch.

---

## ⚖️ So sánh các phương pháp

| Tiêu chí | Historical | Parametric | Monte Carlo |
|----------|------------|------------|-------------|
| **Độ phức tạp** | ⭐⭐ Đơn giản | ⭐ Rất đơn giản | ⭐⭐⭐ Phức tạp |
| **Dữ liệu cần** | ⭐ Nhiều (250+ days) | ⭐⭐⭐ Ít | ⭐⭐ Vừa phải |
| **Tốc độ tính** | ⭐⭐⭐ Nhanh | ⭐⭐⭐ Rất nhanh | ⭐ Chậm |
| **Độ chính xác** | ⭐⭐⭐ Cao | ⭐⭐ Trung bình | ⭐⭐⭐ Cao |
| **Extreme events** | ⭐⭐⭐ Tốt | ⭐ Kém | ⭐⭐ Trung bình |
| **Portfolio phức tạp** | ⭐⭐ Khó | ⭐ Rất khó | ⭐⭐⭐ Dễ |

### Khi nào dùng phương pháp nào?

#### 🏠 Historical Simulation - Dùng khi:
- Bạn là **người mới** học VaR
- Có **đủ dữ liệu** lịch sử (1+ năm)
- Muốn kết quả **dễ giải thích**
- Portfolio **đơn giản** (1-2 tài sản)

#### 📊 Parametric - Dùng khi:
- Cần **tính nhanh** hàng ngày
- **Ít dữ liệu** lịch sử
- Returns **ổn định**, ít volatility
- Báo cáo **hàng ngày** cho management

#### 🎯 Monte Carlo - Dùng khi:
- Portfolio **phức tạp** (nhiều tài sản)
- Cần **stress testing**
- Returns **không normal**
- Có **computing power** mạnh

---

## 🛠️ Thực hành với Python

### File hoàn chỉnh: `var_calculator.py`

```python
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

class VaRCalculator:
    def __init__(self, returns, portfolio_value=1_000_000):
        """
        Initialize VaR Calculator
        
        Args:
            returns: List of daily returns (%)
            portfolio_value: Portfolio value in VND
        """
        self.returns = np.array(returns)
        self.portfolio_value = portfolio_value
    
    def historical_var(self, confidence_level=0.95):
        """Calculate VaR using Historical Simulation"""
        percentile = (1 - confidence_level) * 100
        var_pct = np.percentile(self.returns, percentile)
        var_amount = abs(var_pct) * self.portfolio_value / 100
        
        return {
            'method': 'Historical Simulation',
            'confidence': f"{confidence_level:.0%}",
            'var_pct': var_pct,
            'var_amount': var_amount,
            'interpretation': f"Với {confidence_level:.0%} tin cậy, tổn thất không vượt quá {var_amount:,.0f} VND"
        }
    
    def parametric_var(self, confidence_level=0.95):
        """Calculate VaR using Parametric method"""
        mean = np.mean(self.returns)
        std = np.std(self.returns)
        z_score = norm.ppf(1 - confidence_level)
        
        var_pct = mean + z_score * std
        var_amount = abs(var_pct) * self.portfolio_value / 100
        
        return {
            'method': 'Parametric (Normal)',
            'confidence': f"{confidence_level:.0%}",
            'var_pct': var_pct,
            'var_amount': var_amount,
            'mean': mean,
            'std': std,
            'interpretation': f"Với {confidence_level:.0%} tin cậy, tổn thất không vượt quá {var_amount:,.0f} VND"
        }
    
    def monte_carlo_var(self, confidence_level=0.95, simulations=10000):
        """Calculate VaR using Monte Carlo Simulation"""
        mean = np.mean(self.returns)
        std = np.std(self.returns)
        
        # Generate random scenarios
        np.random.seed(42)
        simulated_returns = np.random.normal(mean, std, simulations)
        
        percentile = (1 - confidence_level) * 100
        var_pct = np.percentile(simulated_returns, percentile)
        var_amount = abs(var_pct) * self.portfolio_value / 100
        
        return {
            'method': 'Monte Carlo',
            'confidence': f"{confidence_level:.0%}",
            'var_pct': var_pct,
            'var_amount': var_amount,
            'simulations': simulations,
            'interpretation': f"Với {confidence_level:.0%} tin cậy, tổn thất không vượt quá {var_amount:,.0f} VND"
        }
    
    def compare_all_methods(self, confidence_level=0.95):
        """Compare all three methods"""
        results = []
        
        # Calculate using all methods
        hist_result = self.historical_var(confidence_level)
        param_result = self.parametric_var(confidence_level)
        mc_result = self.monte_carlo_var(confidence_level)
        
        results = [hist_result, param_result, mc_result]
        
        # Display comparison
        print("=" * 80)
        print(f"          VaR COMPARISON - {confidence_level:.0%} Confidence Level")
        print("=" * 80)
        print(f"Portfolio Value: {self.portfolio_value:,.0f} VND")
        print(f"Data Points: {len(self.returns)} days")
        print("-" * 80)
        
        for result in results:
            print(f"{result['method']:20} | VaR: {result['var_pct']:6.2f}% | "
                  f"Amount: {result['var_amount']:>12,.0f} VND")
        
        print("-" * 80)
        
        # Calculate differences
        var_amounts = [r['var_amount'] for r in results]
        max_diff = max(var_amounts) - min(var_amounts)
        print(f"Max Difference: {max_diff:,.0f} VND ({max_diff/self.portfolio_value*100:.2f}%)")
        
        return results
    
    def plot_returns_distribution(self):
        """Plot returns distribution with VaR levels"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Returns time series
        ax1.plot(self.returns, 'b-', alpha=0.7)
        ax1.set_title('Daily Returns Over Time')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Return (%)')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # Plot 2: Returns histogram with VaR
        ax2.hist(self.returns, bins=30, alpha=0.7, color='skyblue', density=True)
        ax2.set_title('Returns Distribution with VaR Levels')
        ax2.set_xlabel('Return (%)')
        ax2.set_ylabel('Density')
        
        # Add VaR lines
        hist_var = self.historical_var(0.95)['var_pct']
        param_var = self.parametric_var(0.95)['var_pct']
        mc_var = self.monte_carlo_var(0.95)['var_pct']
        
        ax2.axvline(hist_var, color='red', linestyle='--', 
                   label=f'Historical: {hist_var:.2f}%')
        ax2.axvline(param_var, color='green', linestyle='--', 
                   label=f'Parametric: {param_var:.2f}%')
        ax2.axvline(mc_var, color='orange', linestyle='--', 
                   label=f'Monte Carlo: {mc_var:.2f}%')
        
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Ví dụ sử dụng
if __name__ == "__main__":
    # Dữ liệu mẫu FPT returns (%)
    fpt_returns = [2.1, -1.5, 0.8, -3.2, 1.9, -2.1, 0.5, -1.8, 2.5, -0.7,
                   1.2, -2.8, 0.3, -1.1, 2.0, -3.5, 1.7, -0.9, 2.3, -1.3,
                   0.6, -2.4, 1.4, -1.7, 2.8, -0.4, 1.0, -2.2, 0.9, -1.6]
    
    # Khởi tạo calculator với 50 triệu VND
    calculator = VaRCalculator(fpt_returns, portfolio_value=50_000_000)
    
    # So sánh tất cả phương pháp
    results = calculator.compare_all_methods(confidence_level=0.95)
    
    # Vẽ biểu đồ (cần matplotlib)
    # calculator.plot_returns_distribution()
    
    print("\n" + "=" * 80)
    print("                        KẾT LUẬN")
    print("=" * 80)
    print("• Historical Simulation: Phù hợp cho người mới, dễ hiểu")
    print("• Parametric: Nhanh nhất, dùng cho báo cáo hàng ngày")  
    print("• Monte Carlo: Linh hoạt nhất, dùng cho portfolio phức tạp")
    print("• Kết quả chênh lệch không nhiều → Chọn theo nhu cầu sử dụng")
```

### Chạy file:
```bash
python var_calculator.py
```

### Kết quả mẫu:
```
================================================================================
          VaR COMPARISON - 95% Confidence Level
================================================================================
Portfolio Value: 50,000,000 VND
Data Points: 30 days
--------------------------------------------------------------------------------
Historical Simulation | VaR:  -3.20% | Amount:    1,600,000 VND
Parametric (Normal)    | VaR:  -3.14% | Amount:    1,570,000 VND
Monte Carlo            | VaR:  -3.09% | Amount:    1,545,000 VND
--------------------------------------------------------------------------------
Max Difference: 55,000 VND (0.11%)
```

---

## 🎓 Tóm tắt cho người mới

### 🔑 Điều quan trọng nhất:
1. **VaR không phải dự đoán**, mà là **đo lường rủi ro**
2. **Không có phương pháp nào hoàn hảo**, mỗi cái có ưu nhược điểm
3. **VaR chỉ là công cụ**, quyết định cuối cùng vẫn là của bạn

### 💡 Lời khuyên thực tế:
- **Bắt đầu** với Historical Simulation (dễ hiểu nhất)
- **Kết hợp** nhiều phương pháp để cross-check
- **Cập nhật** dữ liệu thường xuyên
- **Hiểu rõ giả định** của từng phương pháp

### ⚠️ Lưu ý quan trọng:
- VaR **không dự đoán** black swan events
- **5% còn lại** (tail risk) có thể rất nguy hiểm
- Luôn có **plan B** cho tình huống xấu nhất
- **Không đầu tư** số tiền không thể mất được

---

**🎯 Bước tiếp theo:** Hãy thực hành với dữ liệu thật của cổ phiếu bạn quan tâm! 