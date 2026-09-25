// api/vnindex-alert.js - Serverless Monitor for VN-INDEX (+/- 15 Points Telegram Alert)
const BOT_TOKEN = '8909883039:AAFT6ZgMJWKLt5jJOJjAx7zxEKIltTjwOSI';
const DEFAULT_CHAT_ID = 5951966097;

let lastAlertState = null;
let lastAlertTimestamp = 0;

async function sendTelegram(chatId, text) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: 'HTML'
      })
    });
    return res.ok;
  } catch (err) {
    console.error("sendTelegram error:", err);
    return false;
  }
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const { test = "false", chatId = DEFAULT_CHAT_ID } = req.query;
  const isTest = test === "true" || test === "1";

  try {
    // 1. Kéo dữ liệu chỉ số VN-INDEX thời gian thực từ VPS (mã 10)
    let curIndex = 0;
    let refIndex = 0;
    let diff = 0;
    let pct = 0;
    let timeStr = "";

    try {
      const vpsRes = await fetch('https://bgapidatafeed.vps.com.vn/getlistindexdetail/10', {
        headers: { "User-Agent": "Mozilla/5.0" }
      });
      if (vpsRes.ok) {
        const vpsData = await vpsRes.json();
        if (Array.isArray(vpsData) && vpsData.length > 0) {
          const item = vpsData[0];
          curIndex = parseFloat(item.oIndex) || 0;
          refIndex = parseFloat(item.cIndex) || curIndex;
          diff = curIndex - refIndex;
          pct = refIndex > 0 ? (diff / refIndex) * 100 : 0;
          timeStr = item.time || "";
        }
      }
    } catch (e) {
      console.warn("Lỗi kéo VPS index:", e);
    }

    // Fallback qua Entrade nếu VPS nghẽn
    if (curIndex === 0) {
      const now = Math.floor(Date.now() / 1000);
      const enRes = await fetch(`https://services.entrade.com.vn/chart-api/v2/ohlcs/index?from=${now - 86400 * 3}&to=${now}&symbol=VNINDEX&resolution=1D`);
      if (enRes.ok) {
        const enData = await enRes.json();
        if (enData && enData.c && enData.c.length > 1) {
          const len = enData.c.length;
          curIndex = parseFloat(enData.c[len - 1]);
          refIndex = parseFloat(enData.c[len - 2]);
          diff = curIndex - refIndex;
          pct = refIndex > 0 ? (diff / refIndex) * 100 : 0;
        }
      }
    }

    const THRESHOLD = 15.0;
    const isTriggered = Math.abs(diff) >= THRESHOLD || isTest;
    let alertSent = false;

    if (isTriggered) {
      const nowMs = Date.now();
      const alertType = diff >= 0 ? "UP_15" : "DOWN_15";

      // Kiểm tra cooldown 30 phút nếu không phải test
      const COOLDOWN_MS = 30 * 60 * 1000;
      const canSend = isTest || (lastAlertState !== alertType) || ((nowMs - lastAlertTimestamp) >= COOLDOWN_MS);

      if (canSend) {
        const isUp = diff >= 0;
        const sign = isUp ? "+" : "";
        const icon = isUp ? "🚀 🟢" : "⚠️ 🔴";
        const title = isUp ? "VN-INDEX BÙNG NỔ TĂNG TRÊN 15 ĐIỂM!" : "VN-INDEX GIẢM MẠNH TRÊN 15 ĐIỂM!";
        const advice = isUp
          ? "Thị trường hưng phấn mạnh! Cơ hội tuyệt vời để chủ động chốt lời từng phần hoặc cơ cấu danh mục giá xanh."
          : "Áp lực bán dâng cao toàn thị trường! Tuyệt đối không hoảng loạn bán tháo ở đáy, chuẩn bị tiền mặt canh bắt nhịp hồi.";

        const tgMsg = `${icon} <b>[KWANGTAE CẢNH BÁO BIẾN ĐỘNG THỊ TRƯỜNG]</b> ⚡\n\n` +
          `📊 <b>Chỉ số VN-INDEX:</b> <b>${curIndex.toFixed(2)} điểm</b>\n` +
          `📈 <b>Mức biến động:</b> <b>${sign}${diff.toFixed(2)} điểm</b> (${sign}${pct.toFixed(2)}%)\n` +
          `🎯 <b>Tham chiếu đầu phiên:</b> ${refIndex.toFixed(2)} điểm\n` +
          `⏱ <b>Thời điểm ghi nhận:</b> ${timeStr || new Date().toLocaleTimeString("vi-VN")}\n\n` +
          `💼 <b>LỜI KHUYÊN CHO ANH THẾ QUANG:</b>\n` +
          `• <b>Xu hướng:</b> ${advice}\n` +
          `• <b>Vị thế ACV:</b> Tiếp tục khóa chặt 1,000 cổ cốt lõi cất tủ dài hạn, bán 250 cổ cơ cấu thu tiền mặt quanh 39.4k.\n\n` +
          `🌐 <i>Theo dõi trực tiếp: https://trader-desk-mbs.vercel.app</i>`;

        alertSent = await sendTelegram(chatId, tgMsg);
        if (alertSent && !isTest) {
          lastAlertState = alertType;
          lastAlertTimestamp = nowMs;
        }
      }
    }

    return res.status(200).json({
      ok: true,
      vnindex: {
        current: curIndex,
        ref: refIndex,
        diff: parseFloat(diff.toFixed(2)),
        pct: parseFloat(pct.toFixed(2)),
        time: timeStr
      },
      threshold: THRESHOLD,
      isTriggered: Math.abs(diff) >= THRESHOLD,
      alertSent: alertSent,
      isTest: isTest
    });
  } catch (err) {
    return res.status(500).json({ ok: false, error: err.message });
  }
}
