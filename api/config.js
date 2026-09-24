// api/config.js - Vercel Serverless Function cho Trader Desk Pro
let inMemoryConfig = {
  stocks: "VN-INDEX,ACV,GEE,VIC,VCB,GEX,VTP,MBB,VHM,VIX",
  owned: "ACV",
  qty: 1250,
  avg: 45.899,
  cash: 500000,
  holdings: {
    "ACV": { symbol: "ACV", qty: 1250, avgPrice: 45.899, curPrice: 39.4, name: "TCT Cảng Hàng Không VN" }
  },
  transactions: [
    { id: "GD1001", time: "24/09/2026 09:15", type: "deposit", amount: 500000, desc: "Số dư khởi tạo tài khoản", status: "Thành công" }
  ],
  session: "ONLINE",
  time: ""
};

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // 1. XỬ LÝ LƯU CẤU HÌNH (POST /save HOẶC POST /api/config)
  if (req.method === "POST") {
    let body = req.body;
    if (typeof body === "string") {
      try {
        body = JSON.parse(body);
      } catch (_) {
        const params = new URLSearchParams(body);
        body = Object.fromEntries(params.entries());
      }
    }

    if (body) {
      if (body.stocks) inMemoryConfig.stocks = body.stocks;
      if (body.owned) inMemoryConfig.owned = body.owned;
      if (body.qty) inMemoryConfig.qty = parseInt(body.qty) || inMemoryConfig.qty;
      if (body.avg) inMemoryConfig.avg = parseFloat(body.avg) || inMemoryConfig.avg;
      if (body.cash !== undefined) inMemoryConfig.cash = parseFloat(body.cash);
      if (body.holdings) inMemoryConfig.holdings = body.holdings;
      if (body.transactions) inMemoryConfig.transactions = body.transactions;
    }

    // Nếu có biến môi trường KV / Upstash Redis -> Lưu vào đám mây vĩnh viễn
    if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
      try {
        await fetch(`${process.env.KV_REST_API_URL}/set/trader_cfg`, {
          headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` },
          method: "POST",
          body: JSON.stringify(inMemoryConfig)
        });
      } catch (err) {
        console.error("KV save error:", err);
      }
    }

    return res.status(200).json({ status: "ok", msg: "Đã lưu thành công lên Vercel Cloud!" });
  }

  // 2. XỬ LÝ ĐỌC CẤU HÌNH & BẢNG GIÁ REALTIME (GET /api/config)
  if (req.method === "GET") {
    // Nếu có KV -> Đọc cấu hình từ KV
    if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
      try {
        const kvRes = await fetch(`${process.env.KV_REST_API_URL}/get/trader_cfg`, {
          headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` }
        });
        const kvData = await kvRes.json();
        if (kvData && kvData.result) {
          const parsed = typeof kvData.result === "string" ? JSON.parse(kvData.result) : kvData.result;
          inMemoryConfig = { ...inMemoryConfig, ...parsed };
        }
      } catch (err) {
        console.error("KV read error:", err);
      }
    }

    let items = [];
    const stockList = inMemoryConfig.stocks.split(",").map(s => s.trim().toUpperCase()).filter(s => s !== "VN-INDEX");

    try {
      // 1. Kéo VN-INDEX
      if (inMemoryConfig.stocks.includes("VN-INDEX")) {
        try {
          const idxRes = await fetch("https://bgapidatafeed.vps.com.vn/getlistindexdetail/10", {
            headers: { "User-Agent": "Mozilla/5.0" }
          });
          const idxData = await idxRes.json();
          if (idxData && idxData.length > 0) {
            const cIdx = parseFloat(idxData[0].cIndex) || 0;
            const chg = parseFloat(idxData[0].changePercent) || 0;
            items.push({ sym: "VN-INDEX", price: cIdx, chg: chg, vol: 0 });
          }
        } catch (_) {
          items.push({ sym: "VN-INDEX", price: 1775.09, chg: 0.0, vol: 0 });
        }
      }

      // 2. Kéo danh sách cổ phiếu từ VPS
      if (stockList.length > 0) {
        const vpsRes = await fetch(`https://bgapidatafeed.vps.com.vn/getliststockdata/${stockList.join(",")}`, {
          headers: { "User-Agent": "Mozilla/5.0" }
        });
        const vpsData = await vpsRes.json();
        for (const s of vpsData) {
          const last = parseFloat(s.lastPrice) || parseFloat(s.r) || 0;
          const chg = parseFloat(s.changePc) || 0;
          const vol = (parseFloat(s.lot) || 0) / 1000000;
          items.push({ sym: s.sym, price: last, chg: chg, vol: vol });
        }
      }
    } catch (e) {
      console.error("VPS proxy error:", e);
    }

    const now = new Date();
    const vnTime = now.toLocaleTimeString("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" });

    return res.status(200).json({
      stocks: inMemoryConfig.stocks,
      owned: inMemoryConfig.owned,
      qty: inMemoryConfig.qty,
      avg: inMemoryConfig.avg,
      ip: "Vercel Cloud",
      session: "CHOT PHIEN",
      time: vnTime,
      items: items
    });
  }

  return res.status(405).json({ error: "Method not allowed" });
}
