# 👔 KWANGTAE QUANT TERMINAL & AI BROKER

Cổng thông tin Cố vấn Quản lý Danh mục Định lượng & AI Broker 24/7 chuyên biệt cho nhà đầu tư **Quang Thế (`QTheee`)**.

---

## 🏛️ Các Tính Năng Cốt Lõi

1. **Quản Lý Danh Mục Cá Nhân Hóa (VIP Portfolio)**:
   - Theo dõi cổ phiếu cốt lõi **ACV** (1,250 CP) và lộ trình cơ cấu dài hạn đón sóng Siêu Cảng Hàng Không Quốc Tế Long Thành 2026.
   - Quản trị thanh khoản và điều phối nguồn vốn rình mồi lướt sóng.

2. **Cỗ Máy Định Lượng KwangTae Quant Radar**:
   - Chỉ số **Market Vibe** & Độ rộng dòng tiền thị trường MA20.
   - Cổng kiểm duyệt mô hình **Shadow AUC $\ge 0.58$** (thực tế đạt 0.631).
   - Cầu dao tự ngắt bảo vệ rủi ro Thiên nga đen (**Black Swan Circuit Breaker**).

3. **Ma Trận Tín Hiệu & Khuyến Nghị Cổ Phiếu (Signal Matrix)**:
   - Tự động phân tích nhóm cổ phiếu: VN30 + Nhóm Tuấn Mượt (`GEX, VIX, GEE, VGC, IDC`) + `ACV, VTP`.
   - Vùng mua Entry, Mục tiêu chốt lời Target, Cắt lỗ Stop-loss dựa trên biến động ATR thực tế.

4. **Trợ Lý AI Broker 24/7 Trên Telegram (`@kwangtae_broker_bot`)**:
   - Vận hành trên máy chủ đám mây Vercel Serverless kết hợp **Google Gemini 3.6 Flash**.
   - Phân tích và trò chuyện tự nhiên 24/7/365, không phụ thuộc vào máy tính cá nhân.

---

## ⚙️ Chu Trình Tự Động Hóa MLOps (Daily Post-Close)

- Cứ đúng **15:35 mỗi ngày** sau phiên ATC (Thứ 2 - Thứ 6), GitHub Actions sẽ tự động kích hoạt:
  1. Cào dữ liệu giá đóng cửa mới nhất của toàn bộ danh mục theo dõi.
  2. Tính toán lại bộ chỉ báo kỹ thuật trên cửa sổ trượt 700 phiên.
  3. Kiểm định Shadow Gatekeeper.
  4. Xuất bản tệp dữ liệu `public/kwangtae_radar.json`.
  5. Đồng bộ hóa trực tiếp lên Web Terminal và gửi báo cáo phân tích cho anh Thế qua Telegram.
