#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
customize.py — Điền thông tin 1 khách vào thiệp (an toàn, có đếm số lần thay).

Cách dùng:
    python3 customize.py config.json            # áp dụng
    python3 customize.py config.json --dry-run   # chỉ xem trước, không sửa file

Nguyên tắc an toàn:
- Chỉ thay theo các cặp [tìm, thay] bạn khai trong config (không thay mò "2026").
- In ra SỐ LẦN thay cho mỗi cặp -> nếu = 0 nghĩa là chuỗi không tồn tại (bạn gõ sai),
  nếu quá nhiều bất thường -> dừng kiểm tra.
- Đồng hồ đếm ngược (bT) tính theo giờ Việt Nam (UTC+7).
"""
import json, sys, re, io
from datetime import datetime, timezone, timedelta

INDEX = "docs/index.html"
EXPIRY_FILE = "docs/expiry.txt"
EXPIRED_PAGE = "docs/expired.html"
CURRENT_BT = "1782061200000"   # giá trị bT mẫu trong template

def read(p):  return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)

def main():
    if len(sys.argv) < 2:
        print("Dùng: python3 customize.py config.json [--dry-run]"); sys.exit(1)
    cfg = json.loads(read(sys.argv[1]))
    dry = "--dry-run" in sys.argv

    html = read(INDEX)
    total = 0
    print("=== THAY NỘI DUNG (docs/index.html) ===")
    for pair in cfg.get("replacements", []):
        old, new = pair[0], pair[1]
        n = html.count(old)
        flag = "  ⚠️ KHÔNG TÌM THẤY" if n == 0 else ""
        print(f"  [{n:>3}] '{old[:45]}' -> '{new[:45]}'{flag}")
        if n: html = html.replace(old, new); total += n

    # Đồng hồ đếm ngược
    if cfg.get("countdown"):
        vn = timezone(timedelta(hours=7))
        dt = datetime.strptime(cfg["countdown"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=vn)
        ms = int(dt.timestamp() * 1000)
        n = html.count('"bT":' + CURRENT_BT)
        print(f"\n=== ĐỒNG HỒ ĐẾM NGƯỢC ===\n  [{n}] bT {CURRENT_BT} -> {ms}  ({cfg['countdown']} giờ VN)")
        html = html.replace('"bT":' + CURRENT_BT, '"bT":' + str(ms))

    # Ngày hết hạn
    exp = cfg.get("expiry")
    if exp:
        print(f"\n=== NGÀY HẾT HẠN (docs/expiry.txt) ===\n  {exp}")

    # Liên hệ trên trang hết hạn
    expired = read(EXPIRED_PAGE)
    if cfg.get("lien_he_text"):
        expired = expired.replace("0000 000 000", cfg["lien_he_text"])
    if cfg.get("lien_he_link"):
        expired = expired.replace("https://zalo.me/0000000000", cfg["lien_he_link"])

    if dry:
        print("\n(--dry-run: KHÔNG ghi file. Bỏ --dry-run để áp dụng.)")
        return

    write(INDEX, html)
    if exp: write(EXPIRY_FILE, exp.strip() + "\n")
    write(EXPIRED_PAGE, expired)
    print(f"\n✅ Xong. Đã thay tổng cộng {total} chỗ trong index.html.")
    print("   Nhớ: thay các FILE ẢNH (QR, bìa, ảnh cưới) — giữ nguyên tên file.")
    print("   Kiểm tra còn '2026' hiển thị sót: grep -o '>[^<]*2026[^<]*<' docs/index.html")

if __name__ == "__main__":
    main()
