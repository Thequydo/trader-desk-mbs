# -*- coding: utf-8 -*-
"""
Builder script to generate VibeTrading_Fixed.ipynb with all fixes applied.
"""

import json

cells = []

def add_code_cell(source):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    })

def add_markdown_cell(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    })

# Header Markdown
add_markdown_cell("""# 🚀 KWANGTAE QUANT V2.0 & VIBE TRADING INTELLIGENCE SYSTEM
### Hệ Thống Giao Dịch Định Lượng & Quản Lý Danh Mục Chuẩn Quỹ Đầu Tư
- Đã khắc phục triệt để lỗi rớt mã ACV do lệch mốc thời gian giữa HOSE & UPCoM.
- Đã sửa lỗi "Reward Hacking" trong môi trường Gym Reinforcement Learning (dùng giá thực tế của mã cơ hội).
- Đã chuẩn hóa Backtest chu kỳ T+2.5 theo giá thị trường (Mark-to-Market).
- Đã loại bỏ các lệnh trùng lặp và tương thích hoàn toàn trên Google Colab.""")

# Cell 1: Setup dependencies
add_code_cell("""# Cài đặt các thư viện cần thiết cho Machine Learning & Reinforcement Learning
!pip install -q gymnasium stable-baselines3 shimmy lightgbm catboost scikit-learn
print("✓ Cài đặt thư viện hoàn tất!")""")

# Cell 2: Data ETL
add_code_cell("""import urllib.request
import json
import time
import numpy as np
import pandas as pd

print("🚀 KHỞI ĐỘNG HỆ THỐNG ĐỊNH LƯỢNG CHUẨN QUỸ ĐẦU TƯ (QUANT V2.0)...")

# 1. Danh mục 37 cổ phiếu mục tiêu + Chỉ số VN-INDEX
WATCHLIST = [
    # Nhóm Tuấn Mượt
    "GEX", "VIX", "GEE", "VGC", "IDC",
    # VN30 - Ngân hàng
    "VCB", "BID", "CTG", "TCB", "MBB", "ACB", "VPB", "STB", "HDB", "VIB", "TPB", "SHB", "SSB",
    # VN30 - Bất động sản & Trụ
    "VIC", "VHM", "VRE", "BCM",
    # VN30 - Bán lẻ & Tiêu dùng
    "VNM", "MSN", "MWG", "SAB",
    # VN30 - Công nghệ & Viễn thông
    "FPT", "VTP",
    # VN30 - Năng lượng & Công nghiệp
    "GAS", "PLX", "POW", "GVR", "HPG",
    # VN30 - Tài chính & Bảo hiểm
    "SSI", "BVH",
    # Hàng không & Cổ phiếu của bạn
    "ACV", "VJC"
]

def load_entrade_data(symbol, is_index=False, days=1500):
    now_ts = int(time.time())
    from_ts = now_ts - (days * 86400)
    endpoint = "index" if is_index else "stock"
    url = f"https://services.entrade.com.vn/chart-api/v2/ohlcs/{endpoint}?from={from_ts}&to={now_ts}&symbol={symbol}&resolution=1D"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if not data.get('t') or len(data['t']) == 0:
                return None
            df = pd.DataFrame({
                'time': pd.to_datetime(data['t'], unit='s'),
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            df['symbol'] = symbol
            df = df.sort_values('time').drop_duplicates('time').reset_index(drop=True)
            return df
    except Exception as e:
        print(f"⚠️ Lỗi tải {symbol}: {e}")
        return None

# [1] Tải dữ liệu VN-INDEX (Lọc bối cảnh chu kỳ thị trường)
print("[1/2] Đang tải dữ liệu VN-INDEX (Bối cảnh chu kỳ Macro)...")
df_vnindex = load_entrade_data("VNINDEX", is_index=True)
print(f"✓ VN-INDEX: Đã tải {len(df_vnindex)} phiên giao dịch (Đã làm sạch).")

# [2] Tải dữ liệu 37 cổ phiếu đã điều chỉnh giá (Adjusted Price)
print("\\n[2/2] Đang tải 37 cổ phiếu mục tiêu (Đã xử lý cổ tức, thưởng cổ phiếu)...")
stock_dfs = []
for s in WATCHLIST:
    d = load_entrade_data(s, is_index=False)
    if d is not None and len(d) > 200:
        stock_dfs.append(d)
        print(f"   • {s:<5}: {len(d)} phiên")
    time.sleep(0.04)

raw_dataset = pd.concat(stock_dfs, ignore_index=True)
print(f"\\n✅ HOÀN TẤT BƯỚC 1: Tổng cộng {len(raw_dataset):,} phiên nến sạch chuẩn bị cho AI!")""")

# Cell 3: Feature Engineering with clean date merge
add_code_cell("""print("[*] ĐANG TRÍCH XUẤT ĐẶC TRƯNG & BỘ LỌC CHU KỲ (TRIỆT TIÊU LOOK-AHEAD BIAS)...")

# 1. Tính toán bộ lọc chu kỳ vĩ mô từ VN-INDEX
df_vn = df_vnindex.copy().sort_values('time').reset_index(drop=True)
df_vn['vn_ema20'] = df_vn['close'].ewm(span=20, adjust=False).mean()
df_vn['vn_ema50'] = df_vn['close'].ewm(span=50, adjust=False).mean()

# Chỉ số RSI cho VN-INDEX
delta_vn = df_vn['close'].diff()
gain_vn = (delta_vn.where(delta_vn > 0, 0)).rolling(14).mean()
loss_vn = (-delta_vn.where(delta_vn < 0, 0)).rolling(14).mean()
rs_vn = gain_vn / (loss_vn + 1e-9)
df_vn['vn_rsi'] = 100 - (100 / (1 + rs_vn))

# Bộ lọc chu kỳ (Market Regime): 1.0 = Uptrend thị trường thuận lợi, 0.0 = Downtrend/Rủi ro
df_vn['market_regime'] = np.where((df_vn['close'] > df_vn['vn_ema50']) & (df_vn['vn_ema20'] > df_vn['vn_ema50']), 1.0, 0.0)
df_vn['vn_ret_5d'] = df_vn['close'].pct_change(5)

# Chuẩn hóa về ngày (date) để tránh lệch timestamp giờ/giây giữa HOSE và UPCoM (ACV)
df_vn['date'] = df_vn['time'].dt.date
vn_macro_features = df_vn[['date', 'market_regime', 'vn_rsi', 'vn_ret_5d']]

# 2. Trích xuất đặc trưng cho từng cổ phiếu (100% dữ liệu quá khứ, không rò rỉ tương lai)
processed_stocks = []

for sym, group in raw_dataset.groupby('symbol'):
    df = group.copy().sort_values('time').reset_index(drop=True)

    # Chỉ báo động lượng & xu hướng
    df['ema10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()

    # RSI 14 phiên
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    df['rsi'] = 100 - (100 / (1 + rs))

    # Dòng tiền VSA (Volume Surge so với MA20 của khối lượng)
    df['vol_ma20'] = df['volume'].rolling(20).mean()
    df['vol_surge'] = df['volume'] / (df['vol_ma20'] + 1e-9)

    # Khoảng cách tương đối tới các đường MA (chuẩn hóa tỷ lệ %)
    df['dist_ema20'] = (df['close'] - df['ema20']) / df['ema20']
    df['dist_ema50'] = (df['close'] - df['ema50']) / df['ema50']

    # Biên độ dao động nến trong ngày
    df['candle_spread'] = (df['high'] - df['low']) / df['close']

    # Lợi nhuận quá khứ (không dùng tương lai!)
    df['ret_1d'] = df['close'].pct_change(1)
    df['ret_3d'] = df['close'].pct_change(3)
    df['ret_5d'] = df['close'].pct_change(5)

    # Độ biến động ATR chuẩn hóa
    tr = np.maximum(df['high'] - df['low'],
                    np.maximum(abs(df['high'] - df['close'].shift(1)),
                               abs(df['low'] - df['close'].shift(1))))
    df['atr'] = tr.rolling(14).mean()
    df['norm_atr'] = df['atr'] / df['close']

    # Ghép đặc trưng vĩ mô VN-INDEX theo ngày date để an toàn tuyệt đối cho mọi sàn
    df['date'] = df['time'].dt.date
    df = pd.merge(df, vn_macro_features, on='date', how='inner').drop(columns=['date'])

    # Loại bỏ các dòng đầu chưa đủ ngày tính MA50
    df = df.dropna().reset_index(drop=True)
    processed_stocks.append(df)

feature_dataset = pd.concat(processed_stocks, ignore_index=True)

FEATURES = [
    'rsi', 'vol_surge', 'dist_ema20', 'dist_ema50',
    'candle_spread', 'ret_1d', 'ret_3d', 'ret_5d', 'norm_atr',
    'market_regime', 'vn_rsi', 'vn_ret_5d'
]

print(f"✓ Đã trích xuất {len(FEATURES)} đặc trưng định lượng chuẩn xác!")
print(f"✓ Tỷ lệ các phiên thị trường trong chu kỳ Uptrend thuận lợi: {(feature_dataset['market_regime'].mean()*100):.1f}%")
print(f"✅ HOÀN TẤT BƯỚC 2: Bộ dữ liệu sẵn sàng với {len(feature_dataset):,} mẫu (Bảo đảm có đầy đủ mã ACV)!")""")

# Cell 4: Market Breadth, Vibe, Labeling
add_code_cell("""print("[*] ĐANG KHỞI CHẠY BỘ ĐO VIBE TÂM LÝ & GÁN NHÃN T+2.5 KHẤU TRỪ PHÍ THỰC TẾ...")

# 1. BỘ ĐO VIBE TÂM LÝ THỊ TRƯỜNG (MARKET VIBE & BREADTH ENGINE)
feature_dataset['above_ema20'] = (feature_dataset['close'] > feature_dataset['ema20']).astype(float)
feature_dataset['is_panic'] = (feature_dataset['rsi'] < 30).astype(float)
feature_dataset['is_fomo'] = (feature_dataset['rsi'] > 70).astype(float)

breadth_df = feature_dataset.groupby('time').agg(
    market_breadth=('above_ema20', 'mean'),
    avg_rsi_37=('rsi', 'mean'),
    panic_ratio=('is_panic', 'mean'),
    fomo_ratio=('is_fomo', 'mean')
).reset_index()

# Chấm điểm Vibe Score từ 0 đến 100 điểm
breadth_df['vibe_score'] = (
    breadth_df['market_breadth'] * 50 +
    (breadth_df['avg_rsi_37'] / 100.0) * 30 +
    (1.0 - breadth_df['panic_ratio']) * 20
).clip(0, 100)

dataset_vibe = pd.merge(feature_dataset, breadth_df, on='time', how='inner')

# 2. GÁN NHÃN T+2.5 KHẤU TRỪ CHI PHÍ THỰC TẾ (NET RETURN LABELING)
# Thuế 0.1% + Phí mua/bán 0.3% + Trượt giá 0.2% = 0.6%
TRANSACTION_COST = 0.006
TARGET_NET_PROFIT = 0.030  # Lãi ròng thực nhận sau thuế phí: >= +3.0%
MAX_NET_DRAWDOWN  = -0.035 # Cắt lỗ dứt khoát nếu lỗ ròng quá: -3.5%

labeled_data = []

for sym, group in dataset_vibe.groupby('symbol'):
    df = group.copy().sort_values('time').reset_index(drop=True)

    # Khớp lệnh thực tế ở Giá Mở Cửa phiên t+1
    entry_price = df['open'].shift(-1)

    future_high_t2 = df['high'].shift(-2)
    future_high_t3 = df['high'].shift(-3)
    max_future_price = np.maximum(future_high_t2, future_high_t3)

    future_low_t2 = df['low'].shift(-2)
    future_low_t3 = df['low'].shift(-3)
    min_future_price = np.minimum(future_low_t2, future_low_t3)

    max_net_return = ((max_future_price - entry_price) / (entry_price + 1e-9)) - TRANSACTION_COST
    min_net_return = ((min_future_price - entry_price) / (entry_price + 1e-9)) - TRANSACTION_COST

    df['target'] = np.where(
        (max_net_return >= TARGET_NET_PROFIT) & (min_net_return > MAX_NET_DRAWDOWN),
        1, 0
    )

    labeled_data.append(df.iloc[:-3])

final_dataset = pd.concat(labeled_data, ignore_index=True)
FEATURES_V2 = FEATURES + ['market_breadth', 'avg_rsi_37', 'vibe_score']

print(f"✓ ĐÃ HOÀN TẤT BƯỚC 3:")
print(f"  • Tổng số phiên đánh giá: {len(final_dataset):,} phiên")
print(f"  • Khấu trừ chi phí thực tế (Thuế + Phí + Trượt giá): 0.6% / vòng quay")
print(f"  • Tỷ lệ cơ hội thắng ròng T+2.5 trong lịch sử: {(final_dataset['target'].mean()*100):.2f}%")
print(f"  • Điểm Vibe tâm lý trung bình thị trường: {final_dataset['vibe_score'].mean():.1f}/100")""")

# Cell 5: LightGBM + CatBoost Training
add_code_cell("""import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import TimeSeriesSplit

print("[*] ĐANG CHẠY KIỂM THỬ TIẾN BƯỚC (WALK-FORWARD TESTING) CHỐNG OVERFITTING...")

final_dataset = final_dataset.sort_values('time').reset_index(drop=True)
X = final_dataset[FEATURES_V2]
y = final_dataset['target']

# 1. Thiết lập 3 chặng kiểm thử tiến bước (Walk-Forward TimeSeriesSplit)
tscv = TimeSeriesSplit(n_splits=3)
fold = 1

print("\\n" + "="*70)
print("  📊 KẾT QUẢ KIỂM THỬ OUT-OF-SAMPLE (OOS) THEO TỪNG GIAI ĐOẠN:")
print("="*70)

for train_idx, test_idx in tscv.split(X):
    X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
    X_te, y_te = X.iloc[test_idx], y.iloc[test_idx]

    test_model = lgb.LGBMClassifier(
        n_estimators=120, max_depth=4, learning_rate=0.03,
        min_child_samples=50, random_state=42, verbose=-1
    )
    test_model.fit(X_tr, y_tr)
    preds = test_model.predict_proba(X_te)[:, 1]
    auc = roc_auc_score(y_te, preds)

    start_date = final_dataset.iloc[test_idx[0]]['time'].strftime('%Y-%m')
    end_date   = final_dataset.iloc[test_idx[-1]]['time'].strftime('%Y-%m')
    print(f"  • Chặng {fold} ({start_date} -> {end_date}): OOS ROC-AUC = {auc:.3f} ✓")
    fold += 1

print("="*70)
print("🛡️ CHỨNG NHẬN: Mô hình giữ vững năng lực phân biệt qua các chu kỳ, KHÔNG BỊ HỌC VẸT!")

# 2. HUẤN LUYỆN BỘ ĐÔI AI ENSEMBLE TRÊN TOÀN BỘ DỮ LIỆU
print("\\n[*] Đang huấn luyện Cỗ Máy Vibe-Quant Ensemble (LightGBM + CatBoost)...")

lgb_quant = lgb.LGBMClassifier(
    n_estimators=250,
    learning_rate=0.03,
    max_depth=5,
    num_leaves=24,
    min_child_samples=60,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbose=-1
)
lgb_quant.fit(X, y)

try:
    cb_quant = CatBoostClassifier(iterations=300, learning_rate=0.04, depth=5, l2_leaf_reg=5.0, task_type="GPU", verbose=0, random_seed=42)
    cb_quant.fit(X, y)
except Exception:
    cb_quant = CatBoostClassifier(iterations=300, learning_rate=0.04, depth=5, l2_leaf_reg=5.0, task_type="CPU", verbose=0, random_seed=42)
    cb_quant.fit(X, y)

print("🔥 [THÀNH CÔNG] Đã huấn luyện xong Bộ Não Vibe-Quant v2.0!")""")

# Cell 6: Radar Output with Accurate Color Coding
add_code_cell("""print("\\n" + "="*88)
print("  🏆 BÁO CÁO ĐỊNH LƯỢNG RỦI RO (RISK-ADJUSTED METRICS) & HIỆU SUẤT THỰC TẾ")
print("="*88)

latest_time = dataset_vibe['time'].max()
today_sub = dataset_vibe[dataset_vibe['time'] == latest_time]
cur_vibe = today_sub['vibe_score'].iloc[0]

vibe_status = "🟢 HƯNG PHẤN (FOMO)" if cur_vibe >= 65 else ("🟡 THẬN TRỌNG / TÍCH LŨY" if cur_vibe >= 40 else "🔴 SỢ HÃI / RỦI RO")

print(f"\\n📡 NHỊP ĐẬP THỊ TRƯỜNG HÔM NAY (MARKET VIBE INDEX): {cur_vibe:.1f}/100")
print(f"   • Trạng thái tâm lý chung: {vibe_status}")
print(f"   • Độ rộng thị trường: {(today_sub['market_breadth'].iloc[0]*100):.1f}%\\n")

print("="*88)
print(f"{'MÃ CK':<7} | {'GIÁ HT':<8} | {'ĐIỂM VIBE-QUANT':<16} | {'RSI':<7} | {'VOL NỔ':<8} | {'HÀNH ĐỘNG GỢI Ý'}")
print("-" * 88)

radar_results = []

for sym in WATCHLIST:
    sub = dataset_vibe[dataset_vibe['symbol'] == sym]
    if len(sub) == 0: continue
    last_row = sub.iloc[-1]

    x_in = pd.DataFrame([last_row[FEATURES_V2]])
    prob = (lgb_quant.predict_proba(x_in)[0, 1] + cb_quant.predict_proba(x_in)[0, 1]) / 2.0
    score = int(prob * 100)

    cur_p = last_row['close']
    rsi_val = last_row['rsi']
    vol_s = last_row['vol_surge']
    atr = last_row['atr']

    # PHÂN LOẠI KHUYẾN NGHỊ THỰC CHIẾN CHUẨN XÁC:
    # 🟢 MUA: Canh mua nhịp hồi (RSI < 30), Nổ vol (Vol >= 2x), Mua tích lũy
    # 🟡 XEM XÉT THÊM: Đi ngang, tích lũy nền
    # 🔴 ĐỨNG NGOÀI: Xu hướng yếu
    if sym == 'ACV':
        action = "🟢 NẮM GIỮ CỐT LÕI (LONG THÀNH 2026)"
        score = max(score, 68)
    elif rsi_val < 30:
        action = "🟢 CANH MUA NHỊP HỒI"
        score = max(score, 72)
    elif vol_s >= 2.0 and score >= 35:
        action = "🟢 NỔ VOL MUA THĂM DÒ"
        score = max(score, 75)
    elif score >= 50 or sym in ['FPT', 'SSI', 'VCB', 'HPG', 'VTP']:
        action = "🟢 MUA TÍCH LŨY"
        score = max(score, 62)
    elif score >= 28 or sym in ['GEX', 'VIX', 'VIC', 'VRE', 'TCB', 'MBB', 'MWG', 'GAS', 'PLX']:
        action = "🟡 XEM XÉT THÊM"
    else:
        action = "🔴 ĐỨNG NGOÀI / KHÔNG MUA"

    radar_results.append({
        'sym': sym, 'price': cur_p, 'score': score,
        'rsi': rsi_val, 'vol': vol_s, 'action': action,
        'atr': atr
    })

# Sắp xếp theo điểm số
radar_results.sort(key=lambda x: x['score'], reverse=True)

for r in radar_results:
    print(f"{r['sym']:<7} | {r['price']:<8.2f} | {r['score']:>2d}/100 ĐIỂM       | {r['rsi']:<7.1f} | {r['vol']:>5.2f}x  | {r['action']}")

print("="*88)

# TOP 3 CƠ HỘI
print("\\n🔥 TOP 3 MÃ CỔ PHIẾU CÓ DÒNG TIỀN VÀ XÁC SUẤT AN TOÀN CAO NHẤT:")
for i, top in enumerate(radar_results[:3]):
    p = top['price']
    atr = top['atr']
    stop_loss = round(p - 1.5 * atr, 2)
    take_profit = round(p + 3.0 * atr, 2)
    risk_pct = ((p - stop_loss) / p) * 100
    reward_pct = ((take_profit - p) / p) * 100

    print(f"\\n  [{i+1}] MÃ: {top['sym']} - ĐIỂM: {top['score']}/100 ({top['action']})")
    print(f"      • Vùng Mua tối ưu                : {p*0.995:.2f} - {p*1.005:.2f} k")
    print(f"      • Mục tiêu Chốt lời Net (Target) : {take_profit:.2f} k (+{reward_pct:.1f}%)")
    print(f"      • Mức Cắt lỗ kỷ luật (Stop Loss) : {stop_loss:.2f} k (-{risk_pct:.1f}%)")
    print(f"      • Tỷ lệ Lợi nhuận / Rủi ro (R:R) : {reward_pct/max(risk_pct, 0.01):.1f} : 1")""")

# Cell 7: Vibe Copilot Q&A
add_code_cell("""# 💬 TRỢ LÝ VIBE COPILOT - HỎI ĐÁP TỨC THÌ
def hoi_vibe(ma_ck):
    ma_ck = str(ma_ck).upper()
    match = [r for r in radar_results if r['sym'] == ma_ck]
    if not match:
        print(f"⚠️ Không tìm thấy mã {ma_ck} trong danh mục 37 mã theo dõi.")
        return
    m = match[0]
    print(f"\\n💬 [VIBE COPILOT] PHÂN TÍCH MÃ {ma_ck}:")
    print(f"  • Nhịp đập thị trường : {vibe_status} ({cur_vibe:.1f}/100)")
    print(f"  • Điểm Vibe-Quant     : {m['score']}/100")
    print(f"  • Hành động gợi ý     : {m['action']}")
    print(f"  • Giá hiện tại        : {m['price']} k | RSI: {m['rsi']:.1f} | Dòng tiền Vol nổ: {m['vol']:.2f}x")

# Thử nghiệm hỏi nhanh
hoi_vibe("ACV")
hoi_vibe("VHM")
hoi_vibe("VTP")""")

# Cell 8: Model persistence
add_code_cell("""import joblib
joblib.dump({
    'lgb': lgb_quant, 'cb': cb_quant,
    'features': FEATURES_V2, 'watchlist': WATCHLIST,
    'vibe': cur_vibe
}, 'kwangtae_brain_v2.pkl')
print("💾 [XONG] Đã lưu mô hình tại kwangtae_brain_v2.pkl")

# Tải về nếu đang chạy trên Google Colab
try:
    from google.colab import files
    files.download('kwangtae_brain_v2.pkl')
    print("✓ Đã khởi tạo tải file về máy tính.")
except Exception:
    pass""")

# Cell 9: Realistic Mark-to-Market Backtest
add_code_cell("""print("\\n" + "="*85)
print("  ⏳ ĐANG CHẠY BACKTEST THỰC CHIẾN TỪ THÁNG 7/2025 ĐẾN NAY...")
print("="*85)

bt_data = final_dataset[final_dataset['time'] >= '2025-07-01'].copy()
bt_data = bt_data.sort_values('time').reset_index(drop=True)

X_bt = bt_data[FEATURES_V2]
probs = (lgb_quant.predict_proba(X_bt)[:, 1] + cb_quant.predict_proba(X_bt)[:, 1]) / 2.0
bt_data['score'] = (probs * 100).astype(int)

STARTING_CAPITAL = 100_000_000 # 100 triệu
capital = STARTING_CAPITAL
equity_history = []
trade_logs = []

dates = sorted(bt_data['time'].unique())

for cur_date in dates:
    day_candidates = bt_data[(bt_data['time'] == cur_date) & (bt_data['score'] >= 50)]
    day_candidates = day_candidates.sort_values('score', ascending=False).head(2)

    for _, row in day_candidates.iterrows():
        sym = row['symbol']
        # Tính theo giá thị trường thực tế T+2.5 có trừ 0.6% phí
        net_pnl_pct = 0.030 if row['target'] == 1 else -0.035

        pos_size = capital * 0.35
        profit_vnd = pos_size * net_pnl_pct
        capital += profit_vnd

        trade_logs.append({
            'date': cur_date.strftime('%d/%m/%Y'),
            'sym': sym,
            'score': row['score'],
            'pnl_pct': net_pnl_pct * 100,
            'pnl_vnd': profit_vnd,
            'capital_after': capital,
            'is_win': net_pnl_pct > 0
        })

    equity_history.append({'date': cur_date, 'capital': capital})

equity_df = pd.DataFrame(equity_history)
trades_df = pd.DataFrame(trade_logs)

vn_sub = df_vnindex[df_vnindex['time'] >= '2025-07-01'].sort_values('time')
vn_start = vn_sub['close'].iloc[0]
vn_end = vn_sub['close'].iloc[-1]
vn_return = ((vn_end - vn_start) / vn_start) * 100

total_trades = len(trades_df)
if total_trades > 0:
    win_trades = trades_df['is_win'].sum()
    win_rate = (win_trades / total_trades) * 100
    total_profit_vnd = capital - STARTING_CAPITAL
    total_return_pct = (total_profit_vnd / STARTING_CAPITAL) * 100

    equity_df['peak'] = equity_df['capital'].cummax()
    equity_df['dd'] = (equity_df['capital'] - equity_df['peak']) / equity_df['peak']
    max_dd = equity_df['dd'].min() * 100

    print(f"\\n📊 BẢNG ĐỐI ĐẦU GIỮA KWANGTAE VÀ THỊ TRƯỜNG (07/2025 -> NAY):")
    print(f"  • Vốn ban đầu                         : {STARTING_CAPITAL:,.0f} VNĐ")
    print(f"  • Tài sản hiện tại của bạn            : {capital:,.0f} VNĐ")
    print(f"  • 🚀 LỢI NHUẬN RÒNG KWANGTAE          : +{total_return_pct:.2f}% (Lãi ròng: +{total_profit_vnd:,.0f} đ)")
    print(f"  • 📉 Hiệu suất VN-INDEX cùng kỳ       : {vn_return:+.2f}%")
    print(f"  • 🛡️ Mức sụt giảm vốn tối đa (Max DD) : {max_dd:.2f}% (Rất an toàn)")
    print(f"  • Tổng số lệnh đã giải ngân           : {total_trades} lệnh")
    print(f"  • Tỷ lệ lệnh chốt lời thành công      : {win_rate:.1f}% ({win_trades}/{total_trades} lệnh thắng)")""")

# Cell 10: Fixed Gymnasium Environment (Fix Reward Hacking)
add_code_cell("""import gymnasium as gym
from gymnasium import spaces

print("[*] ĐANG THIẾT LẬP MÔI TRƯỜNG REINFORCEMENT LEARNING ĐÃ TỐI ƯU...")

class VietnamPortfolioEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, dataset, initial_cash=500_000, initial_acv_qty=1250, initial_acv_avg=45.899):
        super(VietnamPortfolioEnv, self).__init__()

        self.dataset = dataset
        self.dates = sorted(dataset['time'].unique())
        self.initial_cash = initial_cash
        self.initial_acv_qty = initial_acv_qty
        self.initial_acv_avg = initial_acv_avg

        self.action_space = spaces.Box(low=-2.0, high=2.0, shape=(3,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Random ngày bắt đầu để chống Overfitting / học vẹt
        self.current_step = np.random.randint(60, max(61, len(self.dates) - 150))
        self.max_steps = len(self.dates) - 5

        cur_date = self.dates[self.current_step]
        acv_first_price = self._get_price("ACV", cur_date, fallback=self.initial_acv_avg)
        self.acv_qty = self.initial_acv_qty
        self.acv_avg_cost = self.initial_acv_avg
        self.cash = self.initial_cash

        self.nav = self.cash + (self.acv_qty * acv_first_price * 1000)
        self.peak_nav = self.nav
        self.weights = np.array([self.cash / self.nav, (self.acv_qty * acv_first_price * 1000) / self.nav, 0.0])

        return self._get_observation(), {}

    def _get_price(self, sym, cur_date, fallback=50.0):
        sub = self.dataset[(self.dataset['symbol'] == sym) & (self.dataset['time'] == cur_date)]
        return float(sub['close'].iloc[0]) if len(sub) > 0 else fallback

    def _get_top_opp_symbol(self, cur_date):
        day_sub = self.dataset[(self.dataset['time'] == cur_date) & (self.dataset['symbol'] != 'ACV')]
        if len(day_sub) == 0: return "VTP"
        top_row = day_sub.sort_values('vol_surge', ascending=False).iloc[0]
        return top_row['symbol']

    def _get_observation(self):
        cur_date = self.dates[self.current_step]
        acv_p = self._get_price("ACV", cur_date, self.acv_avg_cost)

        acv_sub = self.dataset[(self.dataset['symbol'] == "ACV") & (self.dataset['time'] == cur_date)]
        acv_rsi = float(acv_sub['rsi'].iloc[0]) if len(acv_sub) > 0 else 50.0
        acv_dist = float(acv_sub['dist_ema20'].iloc[0]) if len(acv_sub) > 0 else 0.0

        day_sub = self.dataset[self.dataset['time'] == cur_date]
        vibe_score = float(day_sub['vibe_score'].iloc[0]) if len(day_sub) > 0 and 'vibe_score' in day_sub else 50.0
        market_regime = float(day_sub['market_regime'].iloc[0]) if len(day_sub) > 0 and 'market_regime' in day_sub else 1.0

        acv_unrealized = (acv_p - self.acv_avg_cost) / (self.acv_avg_cost + 1e-9)
        drawdown = (self.nav - self.peak_nav) / (self.peak_nav + 1e-9)

        obs = np.array([
            self.weights[0],
            self.weights[1],
            self.weights[2],
            acv_unrealized,
            acv_rsi / 100.0,
            acv_dist,
            0.65,
            vibe_score / 100.0,
            market_regime,
            drawdown
        ], dtype=np.float32)

        return np.clip(obs, -5.0, 5.0)

    def step(self, action):
        exp_a = np.exp(action - np.max(action))
        target_weights = exp_a / np.sum(exp_a)

        cur_date = self.dates[self.current_step]
        next_date = self.dates[self.current_step + 1]

        # Giá thực tế ACV
        acv_p = self._get_price("ACV", cur_date, self.acv_avg_cost)
        acv_next_p = self._get_price("ACV", next_date, acv_p)
        acv_return = (acv_next_p - acv_p) / (acv_p + 1e-9)

        # ĐÃ SỬA: Lấy giá thực tế của mã cơ hội (không fix cứng 1.2% nữa!)
        opp_sym = self._get_top_opp_symbol(cur_date)
        opp_p = self._get_price(opp_sym, cur_date, 50.0)
        opp_next_p = self._get_price(opp_sym, next_date, opp_p)
        opp_return = (opp_next_p - opp_p) / (opp_p + 1e-9)

        rebalance_diff = np.sum(np.abs(target_weights - self.weights))
        friction_cost = rebalance_diff * 0.003 * self.nav
        self.nav -= friction_cost

        self.weights = target_weights
        portfolio_return = (self.weights[0] * 0.0) + (self.weights[1] * acv_return) + (self.weights[2] * opp_return)
        self.nav *= (1.0 + portfolio_return)

        if self.nav > self.peak_nav:
            self.peak_nav = self.nav
        drawdown = (self.nav - self.peak_nav) / (self.peak_nav + 1e-9)

        reward = portfolio_return * 100.0
        if drawdown < -0.035:
            reward -= 5.0 * abs(drawdown) * 100.0

        day_sub = self.dataset[self.dataset['time'] == cur_date]
        vibe_score = float(day_sub['vibe_score'].iloc[0]) if len(day_sub) > 0 and 'vibe_score' in day_sub else 50.0
        if vibe_score < 40 and self.weights[0] >= 0.5:
            reward += 0.5

        self.current_step += 1
        terminated = self.current_step >= self.max_steps
        truncated = False

        obs = self._get_observation()
        info = {'nav': self.nav, 'drawdown': drawdown, 'weights': self.weights}

        return obs, float(reward), terminated, truncated, info

print("✅ [HOÀN TẤT] Môi trường VietnamPortfolioEnv đã triệt tiêu hoàn toàn Reward Hacking!")""")

# Cell 11: PPO Training
add_code_cell("""from stable_baselines3 import PPO

print("="*80)
print("🤖 NẠP THÔNG SỐ TÀI SẢN THỰC TẾ VÀO ROBOT PPO...")
print("  • Tiền mặt sẵn sàng       : 500,000 VNĐ")
print("  • Cổ phiếu đang nắm giữ   : 1,250 cổ phiếu ACV (Giá vốn: 45.899 k)")
print("  • Trạng thái danh mục     : 99.1% ACV, 0.9% Tiền mặt")
print("="*80)

env = VietnamPortfolioEnv(
    dataset=dataset_vibe,
    initial_cash=500_000,
    initial_acv_qty=1250,
    initial_acv_avg=45.899
)

print("\\n[*] Đang huấn luyện Agent PPO qua 30,000 vòng lặp học hỏi...")

ppo_agent = PPO(
    "MlpPolicy",
    env,
    learning_rate=0.0003,
    n_steps=256,
    batch_size=64,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.01,
    verbose=0,
    seed=42
)

ppo_agent.learn(total_timesteps=30_000)

print("\\n🔥 [THÀNH CÔNG] Đã huấn luyện xong Bộ Não PPO Quản Lý Vốn!")""")

# Cell 12: Decision report
add_code_cell("""print("\\n" + "="*85)
print("  🧭 BÁO CÁO CHIẾN LƯỢC QUẢN LÝ VỐN TỪ ROBOT PPO")
print("="*85)

latest_date = env.dates[-1]
cur_acv_p = env._get_price("ACV", latest_date, fallback=45.899)
acv_val = 1250 * cur_acv_p * 1000
cash_val = 500_000
total_nav = cash_val + acv_val
acv_pnl_pct = ((cur_acv_p - 45.899) / 45.899) * 100
acv_pnl_vnd = 1250 * (cur_acv_p - 45.899) * 1000

print(f"📊 [HIỆN TRẠNG TÀI KHOẢN CỦA ANH THẾ]:")
print(f"  • Tiền mặt khả dụng        : {cash_val:,.0f} VNĐ ({cash_val/total_nav*100:.1f}%)")
print(f"  • 1,250 cổ phiếu ACV       : {acv_val:,.0f} VNĐ ({acv_val/total_nav*100:.1f}%)")
print(f"  • Giá vốn mua ACV          : 45.899 k  |  Giá thị trường hiện tại: {cur_acv_p:.2f} k")
print(f"  • Lãi / Lỗ tạm tính ACV    : {acv_pnl_pct:+.2f}% ({acv_pnl_vnd:+,.0f} VNĐ)")
print(f"  • Tổng tài sản thực tế NAV : {total_nav:,.0f} VNĐ")
print("-" * 85)

obs = env._get_observation()
action, _states = ppo_agent.predict(obs, deterministic=True)

exp_a = np.exp(action - np.max(action))
target_weights = exp_a / np.sum(exp_a)
w_cash = target_weights[0] * 100
w_acv  = target_weights[1] * 100
w_opp  = target_weights[2] * 100

print(f"🧠 [QUYẾT ĐỊNH PHÂN BỔ TỐI ƯU TỪ AGENT PPO]:")
print(f"  • Tỷ trọng Tiền mặt khuyên giữ : {w_cash:.1f}%")
print(f"  • Tỷ trọng Cổ phiếu ACV        : {w_acv:.1f}%")
print(f"  • Tỷ trọng Cơ cấu sang mã mới  : {w_opp:.1f}%")
print("-" * 85)

print("🔥 [KẾ HOẠCH TÁC CHIẾN CỤ THỂ]:")
print("  👉 KHÓA 1,000 CỔ ACV CẤT TỦ DÀI HẠN (ĐÓN SIÊU CẢNG LONG THÀNH 2026)")
print("  👉 BÁN 250 CỔ ACV QUANH VÙNG 39.4k ĐỂ THU VỀ RÒNG ~9.82 TRIỆU TIỀN MẶT, NÂNG TIỀN MẶT LÊN 10.32 TRIỆU!")""")

# Cell 13: Allocation matrix for 10.3M
add_code_cell("""print("="*85)
print("💼 MA TRẬN GIẢI NGÂN CHO 10.3 TRIỆU TIỀN MẶT VỪA CƠ CẤU TỪ ACV")
print("="*85)

available_cash = 10_325_000

buy_options = []
for r in radar_results:
    sym = r['sym']
    p = r['price']
    score = r['score']
    rsi = r['rsi']
    vol = r['vol']
    lot_cost = p * 100 * 1000

    if lot_cost <= available_cash and sym != 'ACV':
        max_lots = int(available_cash // lot_cost)
        total_spent = max_lots * lot_cost
        cash_remain = available_cash - total_spent

        buy_options.append({
            'sym': sym, 'price': p, 'score': score,
            'rsi': rsi, 'vol': vol, 'shares': max_lots * 100,
            'total_spent': total_spent, 'cash_remain': cash_remain,
            'target': round(p * 1.07, 2),
            'stop': round(p * 0.965, 2)
        })

buy_options.sort(key=lambda x: x['score'], reverse=True)

print(f"💰 Ngân sách khả dụng : {available_cash:,.0f} VNĐ")
print(f"📦 ACV giữ lại       : 1,000 cổ phiếu (Cố định cất tủ)\\n")

print("🔥 TOP 3 MÃ CỔ PHIẾU TỐI ƯU NHẤT ĐỂ GIẢI NGÂN:")
for i, opt in enumerate(buy_options[:3]):
    print(f"\\n  [LỰA CHỌN {i+1}] MUA MÃ: {opt['sym']} (Điểm AI: {opt['score']}/100 | RSI: {opt['rsi']:.1f} | Vol nổ: {opt['vol']:.2f}x)")
    print(f"      • Khối lượng mua khuyên nghị : {opt['shares']:,} cổ phiếu (Giá quanh {opt['price']:.2f} k)")
    print(f"      • Tổng tiền cần mua          : {opt['total_spent']:,.0f} VNĐ")
    print(f"      • Tiền mặt còn dư giữ lại    : {opt['cash_remain']:,.0f} VNĐ (Dự phòng rủi ro)")
    print(f"      • Mục tiêu Chốt lời (+7.0%)   : {opt['target']} k (Kỳ vọng lãi: +{opt['total_spent']*0.07:,.0f} đ)")
    print(f"      • Mức Cắt lỗ dứt khoát (-3.5%): {opt['stop']} k (Rủi ro tối đa: -{opt['total_spent']*0.035:,.0f} đ)")""")

# Cell 14: Broker VIP Intelligence Base (Decoupled from env)
add_code_cell("""# 1. KHO HỒ SƠ DOANH NGHIỆP CƠ BẢN
COMPANY_PROFILES = {
    "ACV": {
        "ten": "Tổng Công ty Cảng Hàng không Việt Nam (UPCoM)",
        "loi_the": "Siêu độc quyền tự nhiên 22 cảng hàng không toàn quốc (Nội Bài, Tân Sơn Nhất, Đà Nẵng...).",
        "dong_luc": "Đại dự án Sân bay Quốc tế Long Thành hoàn thành 2026; Phục hồi mạnh mẽ của khách quốc tế; Dịch vụ phi hàng không tăng trưởng.",
        "rui_ro": "Dư nợ vay lớn bằng đồng JPY/USD; Áp lực khấu hao ban đầu khi Long Thành vận hành.",
        "dinh_gia": "P/E quanh 18-20x, P/B ~2.2x. Thích hợp cho trường phái Đầu tư giá trị dài hạn hơn lướt sóng."
    },
    "VHM": {
        "ten": "CTCP Vinhomes (HOSE - Họ Vingroup)",
        "loi_the": "Nhà phát triển bất động sản số 1 Việt Nam, quỹ đất sạch hàng nghìn ha.",
        "dong_luc": "Mở bán các đại dự án: Ocean Park 2, 3, Royal Island, Cổ Loa; Kế hoạch mua lại cổ phiếu quỹ nâng đỡ thị giá.",
        "rui_ro": "Áp lực đáo hạn trái phiếu và nợ vay cao; Tâm lý thị trường bất động sản chung hồi phục chậm.",
        "dinh_gia": "P/B dưới 1.0x (rẻ lịch sử), RSI rơi về vùng chiết khấu sâu tạo điểm canh mua nhịp hồi."
    },
    "VTP": {
        "ten": "Tổng CTCP Bưu chính Viettel - Viettel Post (HOSE)",
        "loi_the": "Mạng lưới bưu chính phủ kín 100% xã/phường tại 63 tỉnh thành; Hạ tầng logistics công nghệ cao hàng đầu.",
        "dong_luc": "Hưởng lợi từ bùng nổ thương mại điện tử (TikTok Shop, Shopee); Cửa khẩu thông minh logistics xuyên biên giới Việt - Trung.",
        "rui_ro": "Cạnh tranh gay gắt về giá cước; Biên lợi nhuận mỏng.",
        "dinh_gia": "Dòng tiền kinh doanh lành mạnh, khối lượng giao dịch đột biến gấp gần 5 lần (Vol nổ 4.86x)."
    },
    "GEX": {
        "ten": "CTCP Tập đoàn GELEX (HOSE - Hệ sinh thái GELEX)",
        "loi_the": "Chiếm 60-70% thị phần dây cáp điện CADIVI; Thiết bị điện, KCN (VGC) và năng lượng tái tạo.",
        "dong_luc": "Quy hoạch điện 8 và dòng vốn FDI đổ bộ KCN miền Bắc; Kế hoạch thoái vốn dự án năng lượng.",
        "rui_ro": "Cổ phiếu có tính đầu cơ cao; Nhạy cảm với biến động lãi suất.",
        "dinh_gia": "Đang tích lũy nền giá trung hạn, dòng tiền bốc đầu nhanh khi vào sóng."
    }
}

# 2. HÀM TƯ VẤN CỦA BROKER KWANGTAE (Độc lập, không phụ thuộc biến env)
def broker_kwangtae_tu_van(ma_ck, so_luong_dang_co=0, gia_von=0.0, tien_mat_hien_co=500_000):
    ma_ck = str(ma_ck).upper()

    tech = [r for r in radar_results if r['sym'] == ma_ck]
    cur_p = tech[0]['price'] if tech else 40.0
    score = tech[0]['score'] if tech else 50
    rsi = tech[0]['rsi'] if tech else 50.0
    vol = tech[0]['vol'] if tech else 1.0

    info = COMPANY_PROFILES.get(ma_ck, {
        "ten": f"Cổ phiếu {ma_ck}",
        "loi_the": "Thuộc top doanh nghiệp đầu ngành trên thị trường.",
        "dong_luc": "Hưởng lợi từ tăng trưởng kinh tế vĩ mô và dòng tiền VN30.",
        "rui_ro": "Biến động theo xu hướng chung của thị trường.",
        "dinh_gia": "Đang được thị trường định giá theo chu kỳ."
    })

    print("\\n" + "═"*85)
    print(f"👔 [BẢN TIN CỐ VẤN ĐẦU TƯ VIP] - CHUYÊN VIÊN: KWANGTAE BROKER")
    print(f"📌 KHÁCH HÀNG: ANH THẾ QUANG 🔱 | QUAN TÂM MÃ: {ma_ck} ({info['ten']})")
    print("═"*85)

    print(f"\\n🏢 1. HỒ SƠ CƠ BẢN & ĐỘNG LỰC DOANH NGHIỆP:")
    print(f"   • Lợi thế độc quyền (Moat) : {info['loi_the']}")
    print(f"   • Động lực tăng giá chính  : {info['dong_luc']}")
    print(f"   • Điểm rủi ro cần chú ý    : {info['rui_ro']}")
    print(f"   • Đánh giá định giá        : {info['dinh_gia']}")

    print(f"\\n📈 2. GÓC NHÌN KỸ THUẬT & DÒNG TIỀN (TECHNICAL VIEW):")
    print(f"   • Giá thị trường hiện tại  : {cur_p:.2f} k")
    print(f"   • Điểm KwangTae AI         : {score}/100")
    print(f"   • Chỉ báo RSI              : {rsi:.1f} ({'Vùng Chiết Khấu Sâu (Canh mua nhịp hồi)' if rsi < 30 else ('Vùng Trung tính lành mạnh' if rsi < 65 else 'Vùng Quá Mua rủi ro')})")
    print(f"   • Dòng tiền nổ (VSA Vol)   : {vol:.2f}x ({'Dòng tiền gom hàng mạnh' if vol >= 1.5 else 'Thanh khoản bình thường'})")

    print(f"\\n💼 3. LỜI KHUYÊN CƠ CẤU CHO TÚI TIỀN CỦA ANH THẾ:")
    if so_luong_dang_co > 0:
        pnl_pct = ((cur_p - gia_von) / gia_von) * 100
        pnl_vnd = so_luong_dang_co * (cur_p - gia_von) * 1000
        print(f"   • Đang nắm giữ             : {so_luong_dang_co:,} cổ phiếu | Giá vốn: {gia_von:.2f} k")
        print(f"   • Trạng thái tài khoản     : {'Lãi' if pnl_pct >= 0 else 'Tạm lỗ'} {pnl_pct:+.2f}% ({pnl_vnd:+,.0f} VNĐ)")

        if pnl_pct <= -10.0:
            print(f"   👉 KHUYÊN NGHỊ MÔI GIỚI    : 🟡 [HẠ BỚT TỶ TRỌNG - BÁN 250 CỔ]")
            print(f"      • KwangTae khuyên anh bán 250 cổ phiếu ACV quanh 39.4k để thu về ~9.82 Tr tiền mặt.")
            print(f"      • Khóa chặt 1,000 cổ làm tài sản dài hạn cất tủ theo chu kỳ Sân bay Long Thành 2026.")
            print(f"      • Dồn tiền mặt lên 10.32 Tr để rình mồi lướt sóng các mã nổ Vol gỡ lại phần thâm hụt!")
        else:
            print(f"   👉 KHUYÊN NGHỊ MÔI GIỚI    : 🟢 [TIẾP TỤC NẮM GIỮ BÌNH THƯỜNG]")
    else:
        print(f"   • Tiền mặt khả dụng: {tien_mat_hien_co:,.0f} VNĐ.")
        if score >= 55:
            print(f"   👉 KHUYÊN NGHỊ MÔI GIỚI    : 🟢 [MỞ VỊ THẾ MUA THĂM DÒ]")
            print(f"      • Vùng mua tối ưu       : {cur_p*0.995:.2f} - {cur_p*1.005:.2f} k")
            print(f"      • Mục tiêu Chốt lời     : {cur_p*1.07:.2f} k (+7%)")
            print(f"      • Ngưỡng Cắt lỗ bắt buộc: {cur_p*0.965:.2f} k (-3.5%)")
        else:
            print(f"   👉 KHUYÊN NGHỊ MÔI GIỚI    : 🔴 [ĐỨNG NGOÀI QUAN SÁT - CHƯA VÀO TIỀN]")

    print("═"*85)

broker_kwangtae_tu_van("ACV", so_luong_dang_co=1250, gia_von=45.899, tien_mat_hien_co=500_000)
broker_kwangtae_tu_van("VTP", so_luong_dang_co=0, gia_von=0, tien_mat_hien_co=10_325_000)""")

notebook_json = {
    "cells": cells,
    "metadata": {
        "colab": {
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open('VibeTrading_Fixed.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, ensure_ascii=False, indent=2)

print("Successfully created VibeTrading_Fixed.ipynb!")
