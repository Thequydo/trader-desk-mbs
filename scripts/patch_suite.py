# -*- coding: utf-8 -*-
"""
Patch script to apply user's updates to build_full_suite.py:
1. Title: SINH VIÊN ĐÁNH CHỨNG • MAN UTD EDITION 🔱
2. Holdings P&L: Replace advice banner with interactive holdings & P&L table
3. Multi-year TradingView chart: API integration + multi-year simulation + range zoom controls (1T, 3T, 6T, 1N, 3N, Tất cả 6N)
"""

with open('scripts/build_full_suite.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update <title>
old_title_tag = r'<title>KwangTae Quant Terminal | Manchester United Fan Edition • Phân Nhóm Ngành & Trading Desk</title>'
new_title_tag = r'<title>Sinh Viên Đánh Chứng | Manchester United Fan Edition • Trading Terminal</title>'
assert old_title_tag in code, "old_title_tag not found"
code = code.replace(old_title_tag, new_title_tag, 1)

# 2. Update brand title
old_brand = r'''          <div class="brand-title">
            KWANGTAE QUANT TERMINAL • MAN UTD EDITION <span style="color:#fbe122;">🔱</span>
          </div>'''
new_brand = r'''          <div class="brand-title">
            SINH VIÊN ĐÁNH CHỨNG • MAN UTD EDITION <span style="color:#fbe122;">🔱</span>
          </div>'''
assert old_brand in code, "old_brand not found"
code = code.replace(old_brand, new_brand, 1)

# 3. Add CSS for holdings-pnl-card and range buttons
old_css_anchor = r'''.advice-banner strong { color: var(--mu-gold); }'''
new_css = r'''.advice-banner strong { color: var(--mu-gold); }

    /* DANH MỤC CỔ PHIẾU SỞ HỮU & LÃI LỖ (PORTFOLIO P&L) */
    .holdings-pnl-card {
      margin-top: 12px;
      background: rgba(10, 14, 26, 0.9);
      border: 1px solid rgba(218, 2, 14, 0.35);
      border-radius: 12px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .holdings-pnl-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .holdings-pnl-title {
      font-size: 12px;
      font-weight: 800;
      color: var(--mu-gold);
      display: flex;
      align-items: center;
      gap: 6px;
      letter-spacing: 0.3px;
    }
    .holdings-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
    }
    .holdings-table th {
      color: var(--text-dim);
      font-size: 9.5px;
      font-weight: 700;
      padding: 4px 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      white-space: nowrap;
    }
    .holdings-table td {
      padding: 6px;
      white-space: nowrap;
    }
    .holdings-footer-note {
      padding-top: 6px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 10.5px;
      line-height: 1.4;
      color: var(--text-dim);
    }
    .cp-range-group {
      display: flex;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }
    .cp-range-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .cp-range-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
    }
    .cp-range-btn.active {
      background: var(--mu-gold);
      color: #000;
      font-weight: 800;
    }'''
assert old_css_anchor in code, "old_css_anchor not found"
code = code.replace(old_css_anchor, new_css, 1)

# 4. Replace advice banner with holdings-pnl-card
old_advice_banner = r'''        <!-- ADVICE BANNER -->
        <div class="advice-banner">
          <strong>🎯 Kế hoạch tái cơ cấu đã thống nhất cùng KwangTae:</strong><br>
          1. <strong>Khóa 1,000 cổ ACV cất tủ dài hạn</strong>: Đón trọn chu kỳ khai trương Siêu Cảng Hàng Không Quốc Tế Long Thành 2026.<br>
          2. <strong>Bán 250 cổ ACV quanh 39.4k</strong>: Thu về ròng <strong>~9.82 triệu</strong>, dồn vào tổng tiền mặt <strong>10.32 triệu</strong> rình mồi lướt sóng nhịp hồi các mã quá bán sâu (như VHM RSI 17.3).
        </div>'''

new_holdings_card = r'''        <!-- DANH MỤC CỔ PHIẾU ĐANG SỞ HỮU & LÃI LỖ THỰC TẾ -->
        <div class="holdings-pnl-card">
          <div class="holdings-pnl-header">
            <div class="holdings-pnl-title">
              <span>💼</span> DANH MỤC CỔ PHIẾU SỞ HỮU & LÃI LỖ (PORTFOLIO P&L)
            </div>
            <span class="client-badge" style="font-size:9.5px; padding:2px 6px;">MBS: 2512T51</span>
          </div>

          <div style="overflow-x:auto;">
            <table class="holdings-table">
              <thead>
                <tr>
                  <th>MÃ CP</th>
                  <th style="text-align:right;">SỐ LƯỢNG</th>
                  <th style="text-align:right;">GIÁ VỐN</th>
                  <th style="text-align:right;">THỊ GIÁ</th>
                  <th style="text-align:right;">TỔNG GIÁ TRỊ</th>
                  <th style="text-align:right;">LÃI / LỖ (P&L)</th>
                  <th style="text-align:right;">TỶ TRỌNG</th>
                  <th style="text-align:center;">HÀNH ĐỘNG</th>
                </tr>
              </thead>
              <tbody id="holdingsTableBody">
                <tr>
                  <td>
                    <div style="display:flex; align-items:center; gap:5px;">
                      <strong style="color:#fff; font-family:var(--font-mono); font-size:12px;">ACV</strong>
                      <span class="sym-tag tag-core" style="font-size:8.5px; padding:1px 4px;">Cốt lõi</span>
                    </div>
                  </td>
                  <td style="text-align:right; font-family:var(--font-mono); font-weight:800; color:#fff;" id="holdingQtyCell">1,250 CP</td>
                  <td style="text-align:right; font-family:var(--font-mono); color:var(--text-muted);">45.899k</td>
                  <td style="text-align:right; font-family:var(--font-mono); font-weight:800; color:#fff;" id="holdingPriceCell">39.40k</td>
                  <td style="text-align:right; font-family:var(--font-mono); font-weight:800; color:var(--quant-green);" id="holdingValueCell">49,250,000 đ</td>
                  <td style="text-align:right; font-family:var(--font-mono); font-weight:800; color:var(--quant-red);" id="holdingPlCell">
                    -8,123,750 đ <span style="font-size:9.5px;">(-14.16%)</span>
                  </td>
                  <td style="text-align:right; font-family:var(--font-mono); font-weight:800; color:var(--mu-gold);">99.0%</td>
                  <td style="text-align:center;">
                    <button class="header-btn" style="padding:2px 8px; font-size:10px; display:inline-flex;" onclick="event.stopPropagation(); selectStock('ACV'); setObType('SELL'); document.getElementById('obQtyInput').value='250'; calcObTotal(); focusOrderPanel();">
                      Cơ cấu 250 CP
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="holdings-footer-note">
            🎯 <strong>Chiến lược tài sản:</strong> Khóa <strong>1,000 cổ ACV</strong> cất tủ dài hạn đón Siêu Cảng Quốc Tế Long Thành 2026 • Kế hoạch cơ cấu bán <strong>250 cổ ACV</strong> quanh 39.4k thu về ròng ~9.82 Tr dồn tiền mặt lên <strong>10.32 triệu</strong>
          </div>
        </div>'''
assert old_advice_banner in code, "old_advice_banner not found"
code = code.replace(old_advice_banner, new_holdings_card, 1)

# 5. Add multi-year range buttons to chart top bar
old_chart_tf_bar = r'''            <div class="cp-tf-group">
              <button class="cp-tf-btn" onclick="setTf('1m', this)">1m</button>
              <button class="cp-tf-btn" onclick="setTf('5m', this)">5m</button>
              <button class="cp-tf-btn" onclick="setTf('15m', this)">15m</button>
              <button class="cp-tf-btn" onclick="setTf('1h', this)">1h</button>
              <button class="cp-tf-btn active" onclick="setTf('1D', this)">1D</button>
              <button class="cp-tf-btn" onclick="setTf('1W', this)">1W</button>
            </div>
          </div>'''

new_chart_tf_bar = r'''            <div class="cp-tf-group">
              <button class="cp-tf-btn" onclick="setTf('1m', this)">1m</button>
              <button class="cp-tf-btn" onclick="setTf('5m', this)">5m</button>
              <button class="cp-tf-btn" onclick="setTf('15m', this)">15m</button>
              <button class="cp-tf-btn" onclick="setTf('1h', this)">1h</button>
              <button class="cp-tf-btn active" onclick="setTf('1D', this)">1D</button>
              <button class="cp-tf-btn" onclick="setTf('1W', this)">1W</button>
            </div>
            <div class="cp-range-group" style="display:flex; gap:2px; margin-left:8px;">
              <button class="cp-range-btn" onclick="zoomChartRange('1M', this)">1T</button>
              <button class="cp-range-btn" onclick="zoomChartRange('3M', this)">3T</button>
              <button class="cp-range-btn" onclick="zoomChartRange('6M', this)">6T</button>
              <button class="cp-range-btn" onclick="zoomChartRange('1Y', this)">1N</button>
              <button class="cp-range-btn" onclick="zoomChartRange('3Y', this)">3N</button>
              <button class="cp-range-btn active" onclick="zoomChartRange('ALL', this)">Tất cả (6N)</button>
            </div>
          </div>'''
assert old_chart_tf_bar in code, "old_chart_tf_bar not found"
code = code.replace(old_chart_tf_bar, new_chart_tf_bar, 1)

# 6. Update generateCandles and loadStockData for multi-year data
old_generate_candles = r'''    function generateCandles(baseP, tf = '1D') {
      const candles = [];
      const volumes = [];
      const ma20 = [];
      const ma50 = [];
      let p = baseP * 0.93;
      const now = new Date();

      const days = tf === '1W' ? 40 : (tf === '1m' ? 30 : 60);
      for (let i = days; i >= 1; i--) {
        const d = new Date(now.getTime() - i * 24 * 3600 * 1000);
        if (d.getDay() === 0 || d.getDay() === 6) continue;
        const timeStr = d.toISOString().split('T')[0];

        const chg = (Math.random() - 0.49) * (p * 0.024);
        const closeP = parseFloat((p + chg).toFixed(2));
        const openP = parseFloat((p + (Math.random() - 0.5) * (p * 0.01)).toFixed(2));
        const highP = parseFloat((Math.max(openP, closeP) + Math.random() * (p * 0.012)).toFixed(2));
        const lowP = parseFloat((Math.min(openP, closeP) - Math.random() * (p * 0.012)).toFixed(2));
        const vol = Math.floor(200000 + Math.random() * 1200000);

        candles.push({ time: timeStr, open: openP, high: highP, low: lowP, close: closeP });
        volumes.push({ time: timeStr, value: vol, color: closeP >= openP ? 'rgba(16, 185, 129, 0.35)' : 'rgba(218, 2, 14, 0.35)' });
        p = closeP;
      }

      const todayStr = now.toISOString().split('T')[0];
      const todayCandle = {
        time: todayStr,
        open: baseP,
        high: parseFloat((baseP * 1.01).toFixed(2)),
        low: parseFloat((baseP * 0.99).toFixed(2)),
        close: baseP
      };
      candles.push(todayCandle);
      currentCandleData = todayCandle;
      volumes.push({ time: todayStr, value: 750000, color: 'rgba(16, 185, 129, 0.4)' });

      for (let i = 0; i < candles.length; i++) {
        if (i >= 19) {
          const avg = candles.slice(i - 19, i + 1).reduce((s, c) => s + c.close, 0) / 20;
          ma20.push({ time: candles[i].time, value: parseFloat(avg.toFixed(2)) });
        }
        if (i >= 49) {
          const avg = candles.slice(i - 49, i + 1).reduce((s, c) => s + c.close, 0) / 50;
          ma50.push({ time: candles[i].time, value: parseFloat(avg.toFixed(2)) });
        }
      }

      return { candles, volumes, ma20, ma50 };
    }

    function loadStockData(sym) {
      if (!candleSeries) return;
      const data = liveQuotes[sym] || liveQuotes.ACV;
      const gen = generateCandles(data.price, currentTf);

      candleSeries.setData(gen.candles);
      if (volumeSeries) volumeSeries.setData(gen.volumes);
      if (ma20Series) ma20Series.setData(gen.ma20);
      if (ma50Series) ma50Series.setData(gen.ma50);
      tvChart.timeScale().fitContent();

      const dec = data.market === 'UPCoM' ? 1 : 2;
      document.getElementById('chartActiveSym').innerText = sym;
      document.getElementById('chartMarketBadge').innerText = data.market;
      document.getElementById('obSymLabel').innerText = sym;
      document.getElementById('obMarketLabel').innerText = `(${data.market})`;
      document.getElementById('obBandLabel').innerText = data.market === 'UPCoM' ? '±15%' : (data.market === 'HNX' ? '±10%' : '±7%');

      document.getElementById('ohlcO').innerText = data.open.toFixed(dec);
      document.getElementById('ohlcH').innerText = data.high.toFixed(dec);
      document.getElementById('ohlcL').innerText = data.low.toFixed(dec);
      document.getElementById('ohlcC').innerText = data.price.toFixed(dec);

      const col = data.ot > 0 ? 'var(--quant-green)' : (data.ot < 0 ? 'var(--quant-red)' : 'var(--mu-gold)');
      const sign = data.ot >= 0 ? '+' : '';
      const chgEl = document.getElementById('ohlcChg');
      chgEl.innerText = `${sign}${data.ot.toFixed(dec)} (${sign}${data.chg.toFixed(2)}%)`;
      chgEl.style.color = col;
      document.getElementById('ohlcC').style.color = col;

      document.getElementById('obPriceInput').value = data.price.toFixed(dec);
      updateTickNotice(data.market, data.price);
      calcObTotal();

      document.getElementById('ma20Val').innerText = (data.price * 1.01).toFixed(dec);
      document.getElementById('ma50Val').innerText = (data.price * 1.04).toFixed(dec);
    }'''

new_generate_candles = r'''    let allCandlesData = [];

    // HÀM TẠO DỮ LIỆU NẾN LỊCH SỬ NHIỀU NĂM (5-6 NĂM, 1250+ PHIÊN)
    function generateCandles(baseP, tf = '1D') {
      const candles = [];
      const volumes = [];
      const ma20 = [];
      const ma50 = [];
      let p = baseP * 0.78;
      const now = new Date();

      const isDailyOrWeekly = tf === '1D' || tf === '1W';
      // 1D: 1250 phiên (~5 năm), 1W: 260 tuần (~5 năm), Intraday: 90 phiên
      const days = tf === '1W' ? 260 : (tf.includes('m') ? 90 : 1250);

      for (let i = days; i >= 1; i--) {
        const d = new Date(now.getTime() - i * 24 * 3600 * 1000);
        if (d.getDay() === 0 || d.getDay() === 6) continue;
        const timeKey = isDailyOrWeekly ? d.toISOString().split('T')[0] : Math.floor(d.getTime() / 1000);

        const drift = (baseP - p) / (i + 15);
        const chg = drift + (Math.random() - 0.49) * (p * 0.022);
        const closeP = parseFloat(Math.max(5, p + chg).toFixed(2));
        const openP = parseFloat((p + (Math.random() - 0.5) * (p * 0.01)).toFixed(2));
        const highP = parseFloat((Math.max(openP, closeP) + Math.random() * (p * 0.012)).toFixed(2));
        const lowP = parseFloat((Math.min(openP, closeP) - Math.random() * (p * 0.012)).toFixed(2));
        const vol = Math.floor(180000 + Math.random() * 1500000);

        candles.push({ time: timeKey, open: openP, high: highP, low: lowP, close: closeP });
        volumes.push({ time: timeKey, value: vol, color: closeP >= openP ? 'rgba(16, 185, 129, 0.4)' : 'rgba(218, 2, 14, 0.4)' });
        p = closeP;
      }

      const todayKey = isDailyOrWeekly ? now.toISOString().split('T')[0] : Math.floor(now.getTime() / 1000);
      const todayCandle = {
        time: todayKey,
        open: baseP,
        high: parseFloat((baseP * 1.012).toFixed(2)),
        low: parseFloat((baseP * 0.988).toFixed(2)),
        close: baseP
      };
      candles.push(todayCandle);
      currentCandleData = todayCandle;
      volumes.push({ time: todayKey, value: 750000, color: 'rgba(16, 185, 129, 0.4)' });

      for (let i = 0; i < candles.length; i++) {
        if (i >= 19) {
          const avg = candles.slice(i - 19, i + 1).reduce((s, c) => s + c.close, 0) / 20;
          ma20.push({ time: candles[i].time, value: parseFloat(avg.toFixed(2)) });
        }
        if (i >= 49) {
          const avg = candles.slice(i - 49, i + 1).reduce((s, c) => s + c.close, 0) / 50;
          ma50.push({ time: candles[i].time, value: parseFloat(avg.toFixed(2)) });
        }
      }

      return { candles, volumes, ma20, ma50 };
    }

    // TẢI DỮ LIỆU CỔ PHIẾU ĐA NIÊN ĐẠI (MULTI-YEAR REAL DATA TỪ SÀN)
    async function loadStockData(sym) {
      if (!candleSeries) return;
      const data = liveQuotes[sym] || liveQuotes.ACV;
      const dec = data.market === 'UPCoM' ? 1 : 2;

      document.getElementById('chartActiveSym').innerText = sym;
      document.getElementById('chartMarketBadge').innerText = data.market || 'HOSE';
      document.getElementById('obSymLabel').innerText = sym;
      document.getElementById('obMarketLabel').innerText = `(${data.market || 'HOSE'})`;
      document.getElementById('obBandLabel').innerText = data.market === 'UPCoM' ? '±15%' : (data.market === 'HNX' ? '±10%' : '±7%');

      document.getElementById('ohlcO').innerText = (data.open || data.price).toFixed(dec);
      document.getElementById('ohlcH').innerText = (data.high || data.price * 1.01).toFixed(dec);
      document.getElementById('ohlcL').innerText = (data.low || data.price * 0.99).toFixed(dec);
      document.getElementById('ohlcC').innerText = data.price.toFixed(dec);

      const col = data.ot > 0 ? 'var(--quant-green)' : (data.ot < 0 ? 'var(--quant-red)' : 'var(--mu-gold)');
      const sign = data.ot >= 0 ? '+' : '';
      const chgEl = document.getElementById('ohlcChg');
      if (chgEl) {
        chgEl.innerText = `${sign}${data.ot.toFixed(dec)} (${sign}${data.chg.toFixed(2)}%)`;
        chgEl.style.color = col;
      }
      document.getElementById('ohlcC').style.color = col;

      document.getElementById('obPriceInput').value = data.price.toFixed(dec);
      updateTickNotice(data.market || 'HOSE', data.price);
      calcObTotal();

      // Kéo dữ liệu thực tế nhiều năm qua API /api/chart
      try {
        const res = await fetch(`/api/chart?symbol=${sym}&resolution=${currentTf}`);
        if (res.ok) {
          const json = await res.json();
          if (json && json.candles && json.candles.length > 0) {
            allCandlesData = json.candles;
            candleSeries.setData(json.candles);
            if (volumeSeries && json.volumes) volumeSeries.setData(json.volumes);
            if (ma20Series && json.ma20) ma20Series.setData(json.ma20);
            if (ma50Series && json.ma50) ma50Series.setData(json.ma50);

            currentCandleData = json.candles[json.candles.length - 1];

            if (json.ma20 && json.ma20.length > 0) {
              document.getElementById('ma20Val').innerText = json.ma20[json.ma20.length - 1].value.toFixed(dec);
            }
            if (json.ma50 && json.ma50.length > 0) {
              document.getElementById('ma50Val').innerText = json.ma50[json.ma50.length - 1].value.toFixed(dec);
            }

            const total = json.candles.length;
            if (total > 150) {
              tvChart.timeScale().setVisibleLogicalRange({
                from: total - 120,
                to: total + 5
              });
            } else {
              tvChart.timeScale().fitContent();
            }
            return;
          }
        }
      } catch (e) {
        console.warn('Lỗi gọi API chart, sử dụng dữ liệu mô phỏng nhiều năm:', e);
      }

      // Fallback nếu không có mạng
      const gen = generateCandles(data.price, currentTf);
      allCandlesData = gen.candles;
      candleSeries.setData(gen.candles);
      if (volumeSeries) volumeSeries.setData(gen.volumes);
      if (ma20Series) ma20Series.setData(gen.ma20);
      if (ma50Series) ma50Series.setData(gen.ma50);

      document.getElementById('ma20Val').innerText = (data.price * 1.01).toFixed(dec);
      document.getElementById('ma50Val').innerText = (data.price * 1.04).toFixed(dec);
      tvChart.timeScale().fitContent();
    }

    // ZOOM NHANH THEO MỐC THỜI GIAN NHIỀU NĂM (1T, 3T, 6T, 1N, 3N, TẤT CẢ)
    function zoomChartRange(range, btn) {
      document.querySelectorAll('.cp-range-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      if (!tvChart || !allCandlesData || allCandlesData.length === 0) return;

      const total = allCandlesData.length;
      if (range === 'ALL') {
        tvChart.timeScale().fitContent();
        return;
      }
      let bars = 120;
      if (range === '1M') bars = 22;
      else if (range === '3M') bars = 66;
      else if (range === '6M') bars = 130;
      else if (range === '1Y') bars = 250;
      else if (range === '3Y') bars = 750;

      tvChart.timeScale().setVisibleLogicalRange({
        from: Math.max(0, total - bars),
        to: total + 5
      });
    }'''
assert old_generate_candles in code, "old_generate_candles not found"
code = code.replace(old_generate_candles, new_generate_candles, 1)

# 7. Update updatePortfolioUI to refresh the holdings-pnl-card
old_update_portfolio = r'''      const plSub = document.getElementById('navPlSub');
      const plSign = totalPL >= 0 ? '+' : '';
      plSub.innerText = `${plSign}${(totalPL / 1000000).toFixed(2)} Tr (${plSign}${plPercent}%)`;
      plSub.style.color = totalPL >= 0 ? 'var(--quant-green)' : 'var(--quant-red)';
    }'''

new_update_portfolio = r'''      const plSub = document.getElementById('navPlSub');
      const plSign = totalPL >= 0 ? '+' : '';
      plSub.innerText = `${plSign}${(totalPL / 1000000).toFixed(2)} Tr (${plSign}${plPercent}%)`;
      plSub.style.color = totalPL >= 0 ? 'var(--quant-green)' : 'var(--quant-red)';

      // Cập nhật bảng Danh mục sở hữu & Lãi lỗ thực tế
      const holdingPriceCell = document.getElementById('holdingPriceCell');
      const holdingValueCell = document.getElementById('holdingValueCell');
      const holdingPlCell = document.getElementById('holdingPlCell');
      const holdingQtyCell = document.getElementById('holdingQtyCell');

      const acv = holdings['ACV'];
      if (acv && holdingPriceCell && holdingValueCell && holdingPlCell) {
        const curP = liveQuotes['ACV'] ? liveQuotes['ACV'].price : 39.4;
        const curVal = acv.qty * curP * 1000;
        const costVal = acv.qty * acv.avgPrice * 1000;
        const pl = curVal - costVal;
        const plPct = costVal > 0 ? (pl / costVal) * 100 : 0;
        const sSign = pl >= 0 ? '+' : '';

        if (holdingQtyCell) holdingQtyCell.innerText = `${acv.qty.toLocaleString()} CP`;
        holdingPriceCell.innerText = `${curP.toFixed(1)}k`;
        holdingValueCell.innerText = `${Math.round(curVal).toLocaleString('vi-VN')} đ`;
        holdingPlCell.innerHTML = `${sSign}${Math.round(pl).toLocaleString('vi-VN')} đ <span style="font-size:9.5px;">(${sSign}${plPct.toFixed(2)}%)</span>`;
        holdingPlCell.style.color = pl >= 0 ? 'var(--quant-green)' : 'var(--quant-red)';
      }
    }'''
assert old_update_portfolio in code, "old_update_portfolio not found"
code = code.replace(old_update_portfolio, new_update_portfolio, 1)

with open('scripts/build_full_suite.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied successfully to scripts/build_full_suite.py!")
