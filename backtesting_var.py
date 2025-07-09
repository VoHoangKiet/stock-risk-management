import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class VaRBacktester:
    def __init__(self, df: pd.DataFrame, portfolio_value: float = 1_000_000):
        """
        Khởi tạo VaR Backtester
        
        Args:
            df: DataFrame chứa dữ liệu giá cổ phiếu
            portfolio_value: Giá trị danh mục đầu tư
        """
        self.df = df.copy()
        self.portfolio_value = portfolio_value
        
    def prepare_data(self, ticker: str) -> pd.DataFrame:
        """Chuẩn bị dữ liệu cho một ticker cụ thể"""
        ticker_df = self.df[self.df['ticker'] == ticker].copy()
        ticker_df['time'] = pd.to_datetime(ticker_df['time'])
        ticker_df = ticker_df.sort_values(by='time')  # type: ignore
        ticker_df.set_index('time', inplace=True)
        
        # Tính lợi suất hàng ngày
        ticker_df['return'] = ticker_df['close'].pct_change()
        ticker_df = ticker_df.dropna()  # Xóa rows có NaN
        
        return ticker_df
    
    def calculate_var(self, returns: pd.Series, confidence_level: float) -> float:
        """Tính VaR cho một mức confidence level cụ thể"""
        if len(returns) == 0:
            return 0.0
        return float(np.percentile(returns, (1 - confidence_level) * 100))
    
    def backtest_var_single_level(self, ticker: str, confidence_level: float) -> Dict:
        """
        Backtest VaR cho một ticker với một confidence level
        
        Args:
            ticker: Mã cổ phiếu
            confidence_level: Mức confidence level
            
        Returns:
            Dict chứa kết quả backtest
        """
        ticker_df = self.prepare_data(ticker)
        returns = ticker_df['return']
        
        if len(returns) == 0:
            return {'ticker': ticker, 'error': 'Không đủ dữ liệu'}
        
        # Tính VaR
        var_pct = self.calculate_var(returns, confidence_level)  # type: ignore
        var_amt = abs(var_pct) * self.portfolio_value
        
        # Đếm số lần vi phạm (returns < VaR)
        violations = sum(returns < var_pct)
        total_days = len(returns)
        violation_rate = violations / total_days
        expected_violation_rate = 1 - confidence_level
        
        # Tính độ chính xác
        accuracy = 1 - abs(violation_rate - expected_violation_rate)
        
        return {
            'ticker': ticker,
            'confidence_level': confidence_level,
            'var_pct': var_pct,
            'var_amt': var_amt,
            'total_days': total_days,
            'violations': violations,
            'violation_rate': violation_rate,
            'expected_violation_rate': expected_violation_rate,
            'accuracy': accuracy,
            'min_return': returns.min(),
            'max_return': returns.max(),
            'mean_return': returns.mean(),
            'std_return': returns.std()
        }
    
    def find_optimal_confidence_level(self, ticker: str, confidence_levels: List[float]) -> Dict:
        """Tìm confidence level tối ưu cho một ticker"""
        best_result = None
        best_accuracy = -1
        
        results = []
        
        for cl in confidence_levels:
            result = self.backtest_var_single_level(ticker, cl)
            if 'error' not in result:
                results.append(result)
                if result['accuracy'] > best_accuracy:
                    best_accuracy = result['accuracy']
                    best_result = result
        
        return {
            'ticker': ticker,
            'optimal_result': best_result,
            'all_results': results
        }
    
    def run_backtest_all_tickers(self, confidence_levels: Optional[List[float]] = None) -> None:
        """Chạy backtest cho tất cả tickers và hiển thị kết quả"""
        if confidence_levels is None:
            confidence_levels = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
        
        tickers = self.df['ticker'].unique()
        
        print("=" * 80)
        print("                    VaR BACKTESTING RESULTS")
        print("=" * 80)
        print(f"Portfolio Value: {self.portfolio_value:,.0f} VND")
        print(f"Confidence Levels tested: {[f'{cl:.1%}' for cl in confidence_levels]}")
        print("=" * 80)
        
        all_optimal_results = []
        
        for i, ticker in enumerate(tickers):
            print(f"\n[{i+1}/{len(tickers)}] Đang phân tích {ticker}...")
            
            # Tìm confidence level tối ưu
            optimal_data = self.find_optimal_confidence_level(ticker, confidence_levels)
            
            if optimal_data['optimal_result'] is None:
                print(f"❌ {ticker}: Không đủ dữ liệu để phân tích")
                continue
            
            optimal = optimal_data['optimal_result']
            all_optimal_results.append(optimal)
            
            # Hiển thị thông tin cơ bản
            print(f"📊 Thống kê returns:")
            print(f"   • Tổng số ngày: {optimal['total_days']}")
            print(f"   • Return trung bình: {optimal['mean_return']:.4f} ({optimal['mean_return']:.2%})")
            print(f"   • Độ lệch chuẩn: {optimal['std_return']:.4f} ({optimal['std_return']:.2%})")
            print(f"   • Return thấp nhất: {optimal['min_return']:.4f} ({optimal['min_return']:.2%})")
            print(f"   • Return cao nhất: {optimal['max_return']:.4f} ({optimal['max_return']:.2%})")
            
            # Hiển thị VaR tối ưu
            print(f"🎯 VaR Tối Ưu:")
            print(f"   • Confidence Level: {optimal['confidence_level']:.1%}")
            print(f"   • VaR (%): {optimal['var_pct']:.4f} ({optimal['var_pct']:.2%})")
            print(f"   • VaR (Amount): {optimal['var_amt']:,.0f} VND")
            print(f"   • Violations: {optimal['violations']}/{optimal['total_days']} ({optimal['violation_rate']:.2%})")
            print(f"   • Expected: {optimal['expected_violation_rate']:.2%}")
            print(f"   • Accuracy: {optimal['accuracy']:.2%}")
            
            # Hiển thị bảng chi tiết cho tất cả confidence levels
            print(f"📋 Chi tiết tất cả Confidence Levels:")
            print("   Conf.Level | VaR (%)    | VaR (VND)      | Violations | Rate    | Accuracy")
            print("   " + "-" * 70)
            
            for result in optimal_data['all_results']:
                cl = result['confidence_level']
                var_pct = result['var_pct']
                var_amt = result['var_amt']
                violations = result['violations']
                total = result['total_days']
                rate = result['violation_rate']
                accuracy = result['accuracy']
                
                # Đánh dấu optimal
                marker = "⭐" if cl == optimal['confidence_level'] else "  "
                
                print(f"   {marker} {cl:6.1%}   | {var_pct:8.4f}  | {var_amt:12,.0f} | "
                      f"{violations:4d}/{total:3d}   | {rate:6.2%} | {accuracy:6.2%}")
        
        # Tóm tắt cuối
        print("\n" + "=" * 80)
        print("                        TÓM TẮT KẾT QUẢ")
        print("=" * 80)
        
        if all_optimal_results:
            optimal_df = pd.DataFrame(all_optimal_results)
            
            print(f"📈 Thống kê chung:")
            print(f"   • Số tickers phân tích: {len(all_optimal_results)}")
            print(f"   • Confidence level trung bình: {optimal_df['confidence_level'].mean():.1%}")
            print(f"   • Confidence level phổ biến nhất: {optimal_df['confidence_level'].mode().iloc[0]:.1%}")
            print(f"   • VaR trung bình: {optimal_df['var_pct'].mean():.4f} ({optimal_df['var_pct'].mean():.2%})")
            print(f"   • Accuracy trung bình: {optimal_df['accuracy'].mean():.2%}")
            
            # Phân loại theo confidence level
            print(f"\n📊 Phân bố Confidence Level:")
            confidence_counts = optimal_df['confidence_level'].value_counts().sort_index()
            for cl, count in confidence_counts.items():
                percentage = count / len(optimal_df) * 100
                print(f"   • {cl:.1%}: {count} tickers ({percentage:.1f}%)")
            
            # Top rủi ro cao nhất và thấp nhất
            print(f"\n⚠️  Top 3 rủi ro CAO NHẤT (VaR %):")
            top_risk = optimal_df.nlargest(3, 'var_pct')
            for idx, row in top_risk.iterrows():
                print(f"   • {row['ticker']}: {row['var_pct']:.4f} ({row['var_pct']:.2%}) - "
                      f"Conf: {row['confidence_level']:.1%}")
            
            print(f"\n✅ Top 3 rủi ro THẤP NHẤT (VaR %):")
            low_risk = optimal_df.nsmallest(3, 'var_pct')
            for idx, row in low_risk.iterrows():
                print(f"   • {row['ticker']}: {row['var_pct']:.4f} ({row['var_pct']:.2%}) - "
                      f"Conf: {row['confidence_level']:.1%}")
            
            # Lưu kết quả
            output_file = 'var_backtest_results.csv'
            optimal_df.to_csv(output_file, index=False)
            print(f"\n💾 Kết quả đã được lưu vào: {output_file}")
        
        print("=" * 80)

def main():
    """Hàm chính để chạy backtesting"""
    try:
        # Đọc dữ liệu
        print("📁 Đang đọc dữ liệu từ stock_data.csv...")
        df = pd.read_csv("stock_data.csv")
        print(f"✅ Đã đọc {len(df)} dòng dữ liệu cho {df['ticker'].nunique()} tickers")
        
        # Khởi tạo backtester
        backtester = VaRBacktester(df, portfolio_value=1_000_000)
        
        # Chạy backtest
        print("🚀 Bắt đầu backtesting...")
        backtester.run_backtest_all_tickers()
        
        print("\n🎉 Hoàn thành backtesting!")
        
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy file 'stock_data.csv'")
        print("   Vui lòng đảm bảo file dữ liệu tồn tại trong thư mục hiện tại.")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main() 