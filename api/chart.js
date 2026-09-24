// api/chart.js - Multi-year Stock Chart Data Proxy (Entrade / VPS / Fallback)
export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "s-maxage=120, stale-while-revalidate=600");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const { symbol = "ACV", resolution = "1D" } = req.query;
  const sym = (symbol || "ACV").toUpperCase().trim();
  const now = Math.floor(Date.now() / 1000);

  // Resolution mapping & time horizon (nhiều năm: 5-6 năm)
  let entradeRes = "1D";
  let fromTime = now - 6 * 365 * 86400; // 6 năm lịch sử

  if (resolution === "1W" || resolution === "W") {
    entradeRes = "1W";
    fromTime = now - 6 * 365 * 86400;
  } else if (resolution === "1m" || resolution === "1") {
    entradeRes = "1";
    fromTime = now - 5 * 86400;
  } else if (resolution === "5m" || resolution === "5") {
    entradeRes = "5";
    fromTime = now - 15 * 86400;
  } else if (resolution === "15m" || resolution === "15") {
    entradeRes = "15";
    fromTime = now - 45 * 86400;
  } else if (resolution === "1h" || resolution === "60" || resolution === "30") {
    entradeRes = "30";
    fromTime = now - 90 * 86400;
  }

  try {
    const url = `https://services.entrade.com.vn/chart-api/v2/ohlcs/stock?from=${fromTime}&to=${now}&symbol=${sym}&resolution=${entradeRes}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 6000);

    const response = await fetch(url, {
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" },
      signal: controller.signal
    });
    clearTimeout(timeout);

    if (response.ok) {
      const json = await response.json();
      if (json && Array.isArray(json.t) && json.t.length > 0) {
        const isDailyOrWeekly = entradeRes === "1D" || entradeRes === "1W";
        const rawBars = [];

        for (let i = 0; i < json.t.length; i++) {
          const t = json.t[i];
          const o = parseFloat(json.o[i]);
          const h = parseFloat(json.h[i]);
          const l = parseFloat(json.l[i]);
          const c = parseFloat(json.c[i]);
          const v = parseInt(json.v[i]) || 0;

          if (isNaN(t) || isNaN(c)) continue;

          let timeKey;
          if (isDailyOrWeekly) {
            timeKey = new Date(t * 1000).toISOString().split("T")[0];
          } else {
            timeKey = t;
          }

          rawBars.push({
            time: timeKey,
            open: o,
            high: h,
            low: l,
            close: c,
            volume: v
          });
        }

        // Sort ascending and strictly deduplicate dates (yêu cầu bắt buộc của Lightweight Charts)
        rawBars.sort((a, b) => (a.time > b.time ? 1 : a.time < b.time ? -1 : 0));
        const seen = new Set();
        const candles = [];
        const volumes = [];

        for (const bar of rawBars) {
          if (!seen.has(bar.time)) {
            seen.add(bar.time);
            candles.push({
              time: bar.time,
              open: bar.open,
              high: bar.high,
              low: bar.low,
              close: bar.close
            });
            volumes.push({
              time: bar.time,
              value: bar.volume,
              color: bar.close >= bar.open ? "rgba(16, 185, 129, 0.45)" : "rgba(218, 2, 14, 0.45)"
            });
          }
        }

        // Calculate MA20 and MA50
        const ma20 = [];
        const ma50 = [];
        for (let i = 0; i < candles.length; i++) {
          if (i >= 19) {
            const sum = candles.slice(i - 19, i + 1).reduce((s, x) => s + x.close, 0);
            ma20.push({ time: candles[i].time, value: parseFloat((sum / 20).toFixed(2)) });
          }
          if (i >= 49) {
            const sum = candles.slice(i - 49, i + 1).reduce((s, x) => s + x.close, 0);
            ma50.push({ time: candles[i].time, value: parseFloat((sum / 50).toFixed(2)) });
          }
        }

        return res.status(200).json({
          symbol: sym,
          resolution,
          total: candles.length,
          candles,
          volumes,
          ma20,
          ma50,
          source: "Entrade Live Feed (Multi-Year)"
        });
      }
    }
  } catch (err) {
    console.warn("Chart fetch error, generating multi-year synthetic fallback:", err.message);
  }

  // Fallback: Generate multi-year realistic candles (5 years, ~1250 bars)
  const fallbackData = generateMultiYearFallback(sym, resolution);
  return res.status(200).json(fallbackData);
}

function generateMultiYearFallback(sym, resolution) {
  const baseMap = {
    ACV: 39.4, VHM: 65.4, VIC: 42.1, VRE: 24.15, FPT: 65.3, VCB: 58.1,
    HPG: 20.8, SSI: 20.85, GEX: 24.1, VIX: 12.75, GEE: 70.9, VTP: 52.6
  };
  const currentPrice = baseMap[sym] || 35.0;
  const isDailyOrWeekly = resolution === "1D" || resolution === "1W";
  const days = resolution === "1W" ? 260 : (resolution.includes("m") ? 60 : 1250); // ~5 years
  const candles = [];
  const volumes = [];
  const ma20 = [];
  const ma50 = [];

  const now = new Date();
  let p = currentPrice * 0.75;

  for (let i = days; i >= 1; i--) {
    const d = new Date(now.getTime() - i * 24 * 3600 * 1000);
    if (d.getDay() === 0 || d.getDay() === 6) continue;
    const timeKey = isDailyOrWeekly ? d.toISOString().split("T")[0] : Math.floor(d.getTime() / 1000);

    const drift = (currentPrice - p) / (i + 10);
    const chg = drift + (Math.random() - 0.49) * (p * 0.022);
    const closeP = parseFloat(Math.max(5, p + chg).toFixed(2));
    const openP = parseFloat((p + (Math.random() - 0.5) * (p * 0.01)).toFixed(2));
    const highP = parseFloat((Math.max(openP, closeP) + Math.random() * (p * 0.012)).toFixed(2));
    const lowP = parseFloat((Math.min(openP, closeP) - Math.random() * (p * 0.012)).toFixed(2));
    const vol = Math.floor(150000 + Math.random() * 1500000);

    candles.push({ time: timeKey, open: openP, high: highP, low: lowP, close: closeP });
    volumes.push({
      time: timeKey,
      value: vol,
      color: closeP >= openP ? "rgba(16, 185, 129, 0.45)" : "rgba(218, 2, 14, 0.45)"
    });
    p = closeP;
  }

  // Today candle
  const todayKey = isDailyOrWeekly ? now.toISOString().split("T")[0] : Math.floor(now.getTime() / 1000);
  const todayCandle = {
    time: todayKey,
    open: currentPrice,
    high: parseFloat((currentPrice * 1.012).toFixed(2)),
    low: parseFloat((currentPrice * 0.988).toFixed(2)),
    close: currentPrice
  };
  candles.push(todayCandle);
  volumes.push({ time: todayKey, value: 850000, color: "rgba(16, 185, 129, 0.45)" });

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

  return {
    symbol: sym,
    resolution,
    total: candles.length,
    candles,
    volumes,
    ma20,
    ma50,
    source: "KwangTae Multi-Year Simulation"
  };
}
