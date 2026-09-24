import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const filePath = path.join(process.cwd(), 'public', 'kwangtae_radar.json');
    if (!fs.existsSync(filePath)) {
      return res.status(200).json({
        status: "warming_up",
        message: "KwangTae đang nạp dữ liệu phiên đầu tiên...",
        vibe_score: 50,
        vibe_status: "ĐANG KHỞI ĐỘNG",
        top3: []
      });
    }

    const data = fs.readFileSync(filePath, 'utf-8');
    const json = JSON.parse(data);
    return res.status(200).json(json);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
