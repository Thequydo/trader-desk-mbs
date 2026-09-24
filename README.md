# 🚀 Hướng Dẫn Đẩy Lên Vercel (1 Cú Click Chuột)

Dự án này đã được đóng gói hoàn chỉnh gồm:
- **`public/index.html`**: Giao diện MBS chuyên nghiệp (Thẻ tài sản, Bảng giá realtime, Quản lý mã chip).
- **`api/config.js`**: Vercel Serverless Function (Lưu cấu hình và tự động kéo giá trực tiếp từ VPS API).
- **`vercel.json`**: Cấu hình rewrite URL.

---

## Cách 1: Đẩy Qua GitHub Lên Vercel (Khuyên Dùng - Tự Động 100%)

### Bước 1: Tạo Repository Trên GitHub
1. Vào [github.com/new](https://github.com/new).
2. Đặt tên Repository (ví dụ: `trader-desk-mbs`) và chọn **Public** hoặc **Private**.
3. Bấm **Create repository**.
4. Copy đường link repo (dạng `https://github.com/<tên-bạn>/trader-desk-mbs.git`).

### Bước 2: Đẩy Code Lên
Mở CMD tại thư mục này và gõ:
```bash
git remote add origin <đường_link_github_của_bạn>
git branch -M main
git push -u origin main
```

### Bước 3: Deploy Trên Vercel
1. Đăng nhập [vercel.com](https://vercel.com).
2. Bấm nút **"Add New..."** -> Chọn **"Project"**.
3. Chọn repo `trader-desk-mbs` vừa tạo -> Bấm **"Deploy"**.
4. Sau 30 giây, Vercel sẽ cấp cho bạn đường link công khai miễn phí có HTTPS (ví dụ: `https://trader-desk-mbs.vercel.app`)!

---

## Đồng Bộ Với Board ESP32 Ở Nhà:
Khi bạn mở web Vercel ở trường hay ngoài đường để đổi mã:
ESP32 ở nhà sẽ kéo cấu hình từ link Vercel của bạn (`https://<tên-của-bạn>.vercel.app/api/config`) để cập nhật màn hình OLED!
