import fs from 'fs';
import path from 'path';

const BOT_TOKEN = '8909883039:AAFT6ZgMJWKLt5jJOJjAx7zxEKIltTjwOSI';

const PROFILES = {
  ACV: {
    name: "TCT Cảng Hàng Không VN (UPCoM)",
    moat: "Độc quyền tự nhiên 22 cảng hàng không cả nước.",
    catalyst: "Đại dự án Sân bay Long Thành 2026; Khách quốc tế hồi phục mạnh.",
    risk: "Dư nợ ngoại tệ JPY/USD dễ bị lỗ tỷ giá.",
    advice: "Giữ chặt 1,000 cổ làm tài sản cất tủ dài hạn, bán 250 cổ lấy ~9.8tr tiền mặt."
  },
  VHM: {
    name: "CTCP Vinhomes (HOSE)",
    moat: "Nhà phát triển BĐS số 1 Việt Nam, quỹ đất khổng lồ.",
    catalyst: "Bàn giao Ocean Park 2-3, Vũ Yên, Cổ Loa; RSI quá bán cực sâu 17.3.",
    risk: "Áp lực nợ vay và đáo hạn trái phiếu lớn.",
    advice: "Vùng mua lướt sóng nhịp hồi kỹ thuật quanh 65.4k (mua 1 lô 100 cổ, vốn ~6.5tr)."
  },
  VTP: {
    name: "Tổng CTCP Bưu chính Viettel (HOSE)",
    moat: "Mạng lưới logistics phủ kín 63 tỉnh thành, công nghệ tự động hóa cao.",
    catalyst: "Hưởng lợi từ bùng nổ thương mại điện tử và cửa khẩu thông minh Việt - Trung.",
    risk: "Cạnh tranh giá cước gay gắt từ SPX, J&T.",
    advice: "Mã có Vol nổ mạnh nhất danh mục (4.86x), vùng canh mua quanh 52.5k."
  },
  GEX: {
    name: "Tập đoàn GELEX (HOSE - Tuấn Mượt)",
    moat: "Chiếm thị phần áp đảo thiết bị điện CADIVI, KCN Viglacera (VGC).",
    catalyst: "Dòng vốn FDI vào KCN phía Bắc; Thoái vốn điện gió thu lãi lớn.",
    risk: "Tính đầu cơ cao, biến động mạnh theo dòng tiền thị trường.",
    advice: "Đang tích lũy nền giá 23.x, đợi dòng tiền xác nhận bứt phá."
  }
};

async function sendTelegram(chatId, text) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text: text,
      parse_mode: 'HTML'
    })
  });
}

export default async function handler(req, res) {
  if (req.method === 'GET') {
    return res.status(200).send("KwangTae Telegram Webhook is Active!");
  }

  if (req.method !== 'POST') {
    return res.status(405).send("Method not allowed");
  }

  try {
    const update = req.body;
    if (!update || !update.message || !update.message.text) {
      return res.status(200).send("OK");
    }

    const chatId = update.message.chat.id;
    const rawText = update.message.text.trim();
    const textUpper = rawText.toUpperCase();

    // 1. Đọc dữ liệu Radar mới nhất
    let radarData = null;
    try {
      const filePath = path.join(process.cwd(), 'public', 'kwangtae_radar.json');
      if (fs.existsSync(filePath)) {
        radarData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      }
    } catch (e) {
      console.error(e);
    }

    // 2. Xử lý các câu hỏi phổ biến
    if (textUpper === '/START' || textUpper === 'HI' || textUpper === 'CHÀO EM' || textUpper === 'CHAO EM') {
      const reply = `👔 <b>CHÀO ANH THẾ! EM LÀ KWANGTAE BROKER!</b> 🚀\n\nEm đã sẵn sàng hỗ trợ anh. Anh có thể hỏi em bất cứ điều gì:\n\n• Gõ tên mã: <b>ACV, VHM, VTP, GEX, VIX...</b> để soi phân tích chuyên sâu.\n• Gõ <b>DANH MỤC</b>: Xem kế hoạch cơ cấu tài khoản của anh.\n• Gõ <b>THỊ TRƯỜNG</b>: Xem chỉ số Vibe và nhịp đập hôm nay.\n• Gõ <b>TOP 3</b>: Xem 3 mã đẹp nhất sàn hôm nay!`;
      await sendTelegram(chatId, reply);
      return res.status(200).send("OK");
    }

    if (textUpper.includes('DANH MỤC') || textUpper.includes('DANH MUC') || textUpper.includes('TÀI KHOẢN') || textUpper.includes('CO CAU') || textUpper.includes('CƠ CẤU')) {
      const reply = `💼 <b>KẾ HOẠCH CƠ CẤU TÀI KHOẢN ANH THẾ:</b>\n\n• <b>Hiện có:</b> 1,250 CP ACV (Giá vốn 45.899k) + 500k tiền mặt.\n• <b>Khuyến nghị KwangTae:</b>\n  1. Đặt bán <b>250 cổ ACV</b> quanh giá 39.4k ➔ Thu về ròng <b>~9.82 triệu</b>.\n  2. Giữ tròn <b>1,000 cổ ACV</b> cất tủ dài hạn ăn sóng Sân bay Long Thành.\n  3. Tổng hầu bao sau cơ cấu: <b>10.32 triệu tiền mặt</b> để rình mồi lướt sóng các mã bùng nổ!`;
      await sendTelegram(chatId, reply);
      return res.status(200).send("OK");
    }

    if (textUpper.includes('THỊ TRƯỜNG') || textUpper.includes('THI TRUONG') || textUpper.includes('VIBE')) {
      const vibe = radarData ? radarData.vibe_score : 54.7;
      const status = radarData ? radarData.vibe_status : "THẬN TRỌNG / TÍCH LŨY";
      const breadth = radarData ? radarData.market_breadth : 45.9;
      const reply = `📡 <b>NHỊP ĐẬP THỊ TRƯỜNG HÔM NAY (MARKET VIBE):</b>\n\n• <b>Chỉ số Vibe:</b> ${vibe}/100\n• <b>Trạng thái:</b> ${status}\n• <b>Độ rộng dòng tiền MA20:</b> ${breadth}%\n• <b>Đánh giá:</b> Thị trường đang phân hóa tích lũy thận trọng. KwangTae khuyên giữ tiền mặt phòng thủ, chỉ giải ngân thăm dò nhỏ các mã có tín hiệu đặc biệt!`;
      await sendTelegram(chatId, reply);
      return res.status(200).send("OK");
    }

    if (textUpper.includes('TOP 3') || textUpper.includes('TOP') || textUpper.includes('MUA GÌ') || textUpper.includes('MUA GI')) {
      let reply = `🔥 <b>TOP 3 CỔ PHIẾU ĐƯỢC KWANGTAE ĐÁNH GIÁ TỐT NHẤT:</b>\n\n`;
      if (radarData && radarData.top3 && radarData.top3.length > 0) {
        radarData.top3.forEach((t, i) => {
          reply += `<b>[${i+1}] ${t.symbol}</b> (Điểm AI: ${t.score}/100)\n• Giá: ${t.price}k | RSI: ${t.rsi} | Vol nổ: ${t.vol_surge}x\n• Vùng mua: ${t.entry_min} - ${t.entry_max}k\n• Target: ${t.target}k (+${t.reward_pct}%) | Cắt lỗ: ${t.stop_loss}k (-${t.risk_pct}%)\n• Gợi ý: ${t.action}\n\n`;
        });
      } else {
        reply += `• VHM: Vùng mua 65.4k (Bắt đáy sóng hồi RSI 17.3)\n• SSB: Vùng mua 20.0k\n• VTP: Canh mua 52.5k khi có dòng tiền bùng nổ!`;
      }
      await sendTelegram(chatId, reply);
      return res.status(200).send("OK");
    }

    // 3. Tìm kiếm theo mã cổ phiếu cụ thể (ví dụ: ACV, VHM, VTP, GEX, SSI...)
    const foundSym = Object.keys(PROFILES).find(s => textUpper.includes(s)) || (radarData && radarData.radar ? radarData.radar.find(r => textUpper.includes(r.symbol))?.symbol : null);

    if (foundSym) {
      const sym = foundSym.toUpperCase();
      const p = PROFILES[sym] || {
        name: `Cổ phiếu ${sym}`,
        moat: "Doanh nghiệp lớn trong rổ VN30/đầu ngành.",
        catalyst: "Hưởng lợi từ chu kỳ kinh tế vĩ mô.",
        risk: "Biến động chung theo thị trường.",
        advice: "Theo dõi chặt chẽ dòng tiền và tuân thủ điểm cắt lỗ kỷ luật."
      };

      const tech = radarData && radarData.radar ? radarData.radar.find(r => r.symbol === sym) : null;
      const curPrice = tech ? tech.price : "Đang cập nhật";
      const score = tech ? tech.score : 30;
      const rsi = tech ? tech.rsi : 50;
      const vol = tech ? tech.vol_surge : 1.0;

      const reply = `👔 <b>[KWANGTAE BROKER ADVISORY] - MÃ ${sym}</b>\n<i>${p.name}</i>\n━━━━━━━━━━━━━━━━━━━\n🏢 <b>HỒ SƠ DOANH NGHIỆP:</b>\n• <b>Lợi thế Moat:</b> ${p.moat}\n• <b>Động lực chính:</b> ${p.catalyst}\n• <b>Rủi ro cốt lõi:</b> ${p.risk}\n\n📈 <b>GÓC NHÌN KỸ THUẬT:</b>\n• Giá hiện tại: <b>${curPrice}k</b> | Điểm AI: <b>${score}/100</b>\n• RSI: <b>${rsi}</b> | Dòng tiền nổ: <b>${vol}x</b>\n\n💡 <b>LỜI KHUYÊN DÀNH CHO ANH:</b>\n👉 <i>${p.advice}</i>`;
      await sendTelegram(chatId, reply);
      return res.status(200).send("OK");
    }

    // Câu trả lời thông minh mặc định
    const defaultReply = `🤖 KwangTae nghe đây anh Thế ơi!\n\nAnh có thể nhắn em tên các mã cổ phiếu như <b>ACV, VHM, VTP, GEX, FPT...</b> hoặc gõ <b>DANH MỤC</b>, <b>THỊ TRƯỜNG</b>, <b>TOP 3</b> để em gửi báo cáo chi tiết cho anh ngay nhé!`;
    await sendTelegram(chatId, defaultReply);
    return res.status(200).send("OK");

  } catch (err) {
    console.error("Webhook error:", err);
    return res.status(500).send(err.message);
  }
}
