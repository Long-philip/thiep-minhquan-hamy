# Hướng dẫn vận hành — Dịch vụ thiệp cưới online (miễn phí)

Repo này là **MẪU**. Mỗi khách = 1 repo riêng tạo từ mẫu này + 1 project Vercel.

---

## ⚙️ Cài đặt 1 lần (đã chuẩn bị sẵn trong repo)
- `docs/expiry.txt` — ngày hết hạn (1 nguồn duy nhất).
- `docs/expired.html` — trang "thiệp hết hạn" (nhớ sửa số ĐT/Zalo của bạn).
- Cổng hết hạn client-side đã chèn sẵn trong `docs/index.html` (tự đọc `expiry.txt`).
- `.github/workflows/expire.yml` — tự khóa server-side khi quá hạn (chạy mỗi ngày).
- `docs/vercel.json` — cấu hình phục vụ tĩnh.
- `customize.py` + `config.example.json` — công cụ điền thông tin nhanh & an toàn.

**Việc cần làm 1 lần trên GitHub/Vercel:**
1. GitHub → repo này → Settings → tick **Template repository**.
2. Tạo tài khoản **Vercel** (vercel.com), đăng nhập bằng GitHub.

---

## 🧾 Quy trình MỖI KHÁCH

### B1. Tạo repo riêng cho khách (private)
```bash
gh repo create wedding-tuanlinh --template Long-philip/thiep-cuoi-mau-2 --private --clone
cd wedding-tuanlinh
```

### B2. Điền thông tin khách
Copy `config.example.json` → `config.json`, điền giá trị, rồi:
```bash
python3 customize.py config.json --dry-run   # xem trước, kiểm tra số lần thay
python3 customize.py config.json             # áp dụng
```
> Cột `[ số ]` in ra là số lần thay. Nếu thấy `⚠️ KHÔNG TÌM THẤY` nghĩa là gõ sai chuỗi.

### B3. Thay FILE ẢNH (giữ NGUYÊN tên file — chỉ đè nội dung)
| Loại | Đường dẫn |
|---|---|
| QR chuyển khoản | `docs/w.ladicdn.com/s450x500/6833feb01c8070001239a3de/qr-thanhtoan.png` |
| Ảnh bìa mở đầu | `docs/cover/cover-mobile.png`, `docs/cover/cover-desktop.png` |
| Ảnh cặp đôi | `docs/w.ladicdn.com/.../atn*.jpg` (12 ảnh) |
| Ảnh album | `docs/w.ladicdn.com/.../album-*.png`, `album-studio-*.jpg` |
| Nhạc nền | `docs/pub-...r2.dev/Music/leduongnewver.mp3` |

### B4. Sửa liên hệ trên trang hết hạn
Trong `docs/expired.html`, sửa số ĐT + link Zalo (hoặc đã set qua `config.json`).

### B5. Kiểm tra còn sót thông tin mẫu
```bash
grep -o '>[^<]*2026[^<]*<' docs/index.html        # năm hiển thị còn sót?
grep -oiE 'Minh Quân|Hà My|Thọ Xuân|Bính Ngọ' docs/index.html   # còn tên/đp mẫu?
```

### B6. Đẩy lên & deploy
```bash
git add -A && git commit -m "Thông tin khách Tuấn & Linh" && git push
```
Lên **Vercel → Add New → Project → chọn repo** →
- **Root Directory = `docs`**
- **Project Name = tên cặp đôi** (vd `tuanlinh-wedding`)
- Deploy → link: `https://tuanlinh-wedding.vercel.app`

### B7. Gửi khách & ghi sổ
Gửi link. Ghi 1 dòng vào `KHACH.md`. Khi khách chốt/đổi tên → Vercel → Settings → rename project → URL đổi theo.

---

## ⏰ Cơ chế khóa sau 3 tuần
- **Ngày khóa** = giá trị trong `docs/expiry.txt` (vd `2026-12-24T23:59:00`).
  `customize.py` tự ghi theo `expiry` trong config.
- **Lớp 1 (tức thì):** trang tự đọc `expiry.txt`, quá hạn → chuyển sang `expired.html`.
- **Lớp 2 (khóa thật):** GitHub Action chạy mỗi ngày, quá hạn → thay `index.html` bằng trang hết hạn, đẩy file thật ra ngoài `docs/` → Vercel redeploy → không xem được nội dung.
- **Mở lại** (khách gia hạn): sửa `docs/expiry.txt` sang ngày mới; nếu đã bị Action khóa thì khôi phục:
  ```bash
  git mv index.real.html.bak docs/index.html && git commit -am "Mở lại thiệp" && git push
  ```

---

## ✅ Test trước khi bán
1. Đặt `expiry` = 2 phút sau → mở link → phải nhảy sang trang hết hạn (lớp 1).
2. GitHub → Actions → "Tự khóa thiệp" → **Run workflow** với `expiry.txt` ngày quá khứ → kiểm tra `index.html` bị thay (lớp 2).
3. Tạo 2 khách cùng lúc, 2 ngày khác nhau → 2 link độc lập, khóa độc lập.
4. Dán link vào Zalo/Messenger → preview hiện đúng tên cặp đôi.

---

## 💸 Miễn phí
- GitHub: repo private không giới hạn; Actions cron miễn phí.
- Vercel Hobby: project & `*.vercel.app` không giới hạn; deploy repo private miễn phí; 100GB băng thông/tháng.
- Tên miền thật (vd `tuanlinh.com`) thì PHẢI mua — không bắt buộc, mặc định dùng `*.vercel.app`.
