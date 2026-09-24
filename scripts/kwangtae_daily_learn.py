import os
import json
import time
import urllib.request
import numpy as np
import pandas as pd
import lightgbm as lgb

print("🚀 [KWANGTAE CLOUD ENGINE] KHỞI ĐỘNG CHU TRÌNH TỰ HỌC TỰ ĐỘNG...")

WATCHLIST = [
    "GEX", "VIX", "GEE", "VGC", "IDC",
    "VCB", "BID", "CTG", "TCB", "MBB", "ACB", "VPB", "STB", "HDB", "VIB", "TPB", "SHB", "SSB",
    "VIC", "VHM", "VRE", "BCM",
    "VNM", "MSN", "MWG", "SAB",
    "FPT", "VTP",
    "GAS", "PLX", "POW", "GVR", "HPG",
    "SSI", "BVH",
    "ACV", "VJC"
]

def load_entrade_data(symbol, is_index=False, days=800):
    now_ts = int(time.time())
    from_ts = now_ts - (days * 86400)
    endpoint = "index" if is_index else "stock"
    url = f"https://services.entrade.com.vn/chart-api/v2/ohlcs/{endpoint}?from={from_ts}&to={now_ts}&symbol={symbol}&resolution=1D"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
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
            return df.sort_values('time').drop_duplicates('time').reset_index(drop=True)
    except Exception as e:
        print(f"⚠️ Lỗi tải {symbol}: {e}")
        return None

# 1. TẢI DỮ LIỆU SẠCH
print("[1/5] Đang nạp dữ liệu VN-INDEX & 37 cổ phiếu...")
df_vn = load_entrade_data("VNINDEX", is_index=True)
if df_vn is None or len(df_vn) < 100:
    print("❌ Lỗi dữ liệu VNINDEX, kết thúc chu trình.")
    exit(1)

df_vn['vn_ema20'] = df_vn['close'].ewm(span=20, adjust=False).mean()
df_vn['vn_ema50'] = df_vn['close'].ewm(span=50, adjust=False).mean()
delta_vn = df_vn['close'].diff()
gain_vn = (delta_vn.where(delta_vn > 0, 0)).rolling(14).mean()
loss_vn = (-delta_vn.where(delta_vn < 0, 0)).rolling(14).mean()
df_vn['vn_rsi'] = 100 - (100 / (1 + (gain_vn / (loss_vn + 1e-9))))
df_vn['market_regime'] = np.where((df_vn['close'] > df_vn['vn_ema50']) & (df_vn['vn_ema20'] > df_vn['vn_ema50']), 1.0, 0.0)
df_vn['vn_ret_5d'] = df_vn['close'].pct_change(5)
vn_features = df_vn[['time', 'market_regime', 'vn_rsi', 'vn_ret_5d']]

stock_dfs = []
for s in WATCHLIST:
    d = load_entrade_data(s, is_index=False)
    if d is not None and len(d) > 100:
        stock_dfs.append(d)
    time.sleep(0.02)

raw_data = pd.concat(stock_dfs, ignore_index=True)

# 2. TÍNH ĐẶC TRƯNG & VIBE THỊ TRƯỜNG
print("[2/5] Đang trích xuất đặc trưng & tính Vibe Index...")
processed = []
for sym, group in raw_data.groupby('symbol'):
    df = group.copy().sort_values('time').reset_index(drop=True)
    df['ema10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['rsi'] = 100 - (100 / (1 + (gain / (loss + 1e-9))))
    
    df['vol_ma20'] = df['volume'].rolling(20).mean()
    df['vol_surge'] = df['volume'] / (df['vol_ma20'] + 1e-9)
    df['dist_ema20'] = (df['close'] - df['ema20']) / df['ema20']
    df['dist_ema50'] = (df['close'] - df['ema50']) / df['ema50']
    df['candle_spread'] = (df['high'] - df['low']) / df['close']
    df['ret_1d'] = df['close'].pct_change(1)
    df['ret_3d'] = df['close'].pct_change(3)
    df['ret_5d'] = df['close'].pct_change(5)
    
    tr = np.maximum(df['high'] - df['low'], 
                    np.maximum(abs(df['high'] - df['close'].shift(1)), 
                               abs(df['low'] - df['close'].shift(1))))
    df['atr'] = tr.rolling(14).mean()
    df['norm_atr'] = df['atr'] / df['close']
    
    df = pd.merge(df, vn_features, on='time', how='inner')
    df = df.dropna().reset_index(drop=True)
    processed.append(df)

dataset = pd.concat(processed, ignore_index=True)

# Vibe Market Breadth
dataset['above_ema20'] = (dataset['close'] > dataset['ema20']).astype(float)
dataset['is_panic'] = (dataset['rsi'] < 30).astype(float)
dataset['is_fomo'] = (dataset['rsi'] > 70).astype(float)

breadth = dataset.groupby('time').agg(
    market_breadth=('above_ema20', 'mean'),
    avg_rsi_37=('rsi', 'mean'),
    panic_ratio=('is_panic', 'mean'),
    fomo_ratio=('is_fomo', 'mean')
).reset_index()

breadth['vibe_score'] = (
    breadth['market_breadth'] * 50 + 
    (breadth['avg_rsi_37'] / 100.0) * 30 + 
    (1.0 - breadth['panic_ratio']) * 20
).clip(0, 100)

dataset = pd.merge(dataset, breadth, on='time', how='inner')

# 3. GÁN NHÃN T+2.5 VỚI 0.6% PHÍ
print("[3/5] Gán nhãn T+2.5 và trừ 0.6% thuế phí/trượt giá...")
TRANSACTION_COST = 0.006 
TARGET_NET_PROFIT = 0.030
MAX_NET_DRAWDOWN  = -0.035

labeled = []
for sym, group in dataset.groupby('symbol'):
    df = group.copy().sort_values('time').reset_index(drop=True)
    entry_p = df['open'].shift(-1)
    max_p = np.maximum(df['high'].shift(-2), df['high'].shift(-3))
    min_p = np.minimum(df['low'].shift(-2), df['low'].shift(-3))
    
    max_ret = ((max_p - entry_p) / (entry_p + 1e-9)) - TRANSACTION_COST
    min_ret = ((min_p - entry_p) / (entry_p + 1e-9)) - TRANSACTION_COST
    
    df['target'] = np.where((max_ret >= TARGET_NET_PROFIT) & (min_ret > MAX_NET_DRAWDOWN), 1, 0)
    labeled.append(df.iloc[:-3])

train_df = pd.concat(labeled, ignore_index=True).sort_values('time').reset_index(drop=True)

FEATURES = [
    'rsi', 'vol_surge', 'dist_ema20', 'dist_ema50', 
    'candle_spread', 'ret_1d', 'ret_3d', 'ret_5d', 'norm_atr',
    'market_regime', 'vn_rsi', 'vn_ret_5d',
    'market_breadth', 'avg_rsi_37', 'vibe_score'
]

# 4. TỰ ĐỘNG HUẤN LUYỆN & HỌC HỎI TRỌNG SỐ MỚI
print("[4/5] Đang tái huấn luyện bộ não KwangTae...")
model = lgb.LGBMClassifier(
    n_estimators=220, learning_rate=0.03, max_depth=5,
    num_leaves=24, min_child_samples=60, subsample=0.8,
    colsample_bytree=0.8, random_state=42, verbose=-1
)
model.fit(train_df[FEATURES], train_df['target'])

# 5. XUẤT RADAR HÔM NAY CHO VERCEL VÀ ESP32
print("[5/5] Đang tạo báo cáo & file API public/kwangtae_radar.json...")
latest_t = dataset['time'].max()
today_sub = dataset[dataset['time'] == latest_t]
cur_vibe = float(today_sub['vibe_score'].iloc[0])
breadth_val = float(today_sub['market_breadth'].iloc[0]) * 100

vibe_status = "HƯNG PHẤN (FOMO)" if cur_vibe >= 65 else ("THẬN TRỌNG / TÍCH LŨY" if cur_vibe >= 40 else "SỢ HÃI / RỦI RO")

radar_list = []
for sym in WATCHLIST:
    sub = dataset[dataset['symbol'] == sym]
    if len(sub) == 0: continue
    last_r = sub.iloc[-1]
    
    x_in = pd.DataFrame([last_r[FEATURES]])
    prob = float(model.predict_proba(x_in)[0, 1])
    score = int(prob * 100)
    cur_p = float(last_r['close'])
    rsi_v = float(last_r['rsi'])
    vol_s = float(last_r['vol_surge'])
    atr_v = float(last_r['atr'])
    
    if score >= 55:
        action = "🟢 MUA / CƠ HỘI ĐẸP"
    elif score >= 35:
        action = "🟡 QUAN SÁT / NẮM GIỮ"
    else:
        action = "🔴 ĐỨNG NGOÀI"
        
    radar_list.append({
        'symbol': sym,
        'price': round(cur_p, 2),
        'score': score,
        'rsi': round(rsi_v, 1),
        'vol_surge': round(vol_s, 2),
        'action': action,
        'atr': round(atr_v, 2),
        'entry_min': round(cur_p * 0.995, 2),
        'entry_max': round(cur_p * 1.005, 2),
        'target': round(cur_p + 3.0 * atr_v, 2),
        'stop_loss': round(cur_p - 1.5 * atr_v, 2),
        'reward_pct': round(((3.0 * atr_v) / cur_p) * 100, 1),
        'risk_pct': round(((1.5 * atr_v) / cur_p) * 100, 1)
    })

radar_list.sort(key=lambda x: x['score'], reverse=True)
top3 = radar_list[:3]

output_payload = {
    'updated_at': latest_t.strftime('%Y-%m-%d %H:%M'),
    'vibe_score': round(cur_vibe, 1),
    'vibe_status': vibe_status,
    'market_breadth': round(breadth_val, 1),
    'top3': top3,
    'radar': radar_list
}

os.makedirs('public', exist_ok=True)
with open('public/kwangtae_radar.json', 'w', encoding='utf-8') as f:
    json.dump(output_payload, f, ensure_ascii=False, indent=2)

print("\n🎉 [HOÀN TẤT] KwangTae đã tự học và cập nhật xong public/kwangtae_radar.json!")
print(f"• Vibe hôm nay : {cur_vibe:.1f}/100 ({vibe_status})")
print(f"• Top 1 mã đẹp : {top3[0]['symbol']} (Điểm: {top3[0]['score']}/100)")
