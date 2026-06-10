/**
 * RSVP -> Google Sheet (dịch vụ thiệp cưới nhiều khách)
 * ----------------------------------------------------------
 * Mỗi khách (tenant) = 1 TAB trong CÙNG 1 Google Sheet "sổ tổng".
 * Tab tự tạo khi khách đó có RSVP đầu tiên.
 *
 * ===== CÀI 1 LẦN =====
 * 1) Tạo 1 Google Sheet mới (sổ tổng chứa RSVP của MỌI khách).
 * 2) Trong Sheet: Extensions (Tiện ích mở rộng) -> Apps Script.
 *    Xoá nội dung mẫu, dán TOÀN BỘ file này vào, bấm Save (đĩa mềm).
 * 3) Deploy (Triển khai) -> New deployment (Triển khai mới):
 *      - Select type (bánh răng) = Web app (Ứng dụng web)
 *      - Execute as (Chạy bằng danh nghĩa): Me (chính bạn)
 *      - Who has access (Ai có quyền): Anyone (Bất kỳ ai)
 *    -> Deploy -> cấp quyền (Authorize) -> COPY "Web app URL" dạng
 *       https://script.google.com/macros/s/XXXX/exec
 * 4) Dán URL đó vào config.json của MỖI khách (khoá "rsvp_endpoint").
 *    Mỗi khách đặt "rsvp_tenant" KHÁC NHAU (vd "tuanlinh") -> tab riêng.
 *
 * ===== SỬA CODE SAU KHI ĐÃ DEPLOY =====
 * Sau khi sửa, phải Deploy -> Manage deployments -> (bút chì) ->
 * Version: New version -> Deploy, thì thay đổi mới có hiệu lực.
 * URL .../exec giữ NGUYÊN nên không cần đổi lại config của khách.
 */

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000); // tránh ghi đè khi nhiều người gửi cùng lúc
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var tab = sanitizeTab(data.tenant);
    var sh = ss.getSheetByName(tab);
    if (!sh) {
      sh = ss.insertSheet(tab);
      sh.appendRow(['Thời gian', 'Họ và tên', 'Tham dự', 'Nơi tham dự', 'Số người', 'Lời nhắn', 'Trang']);
      sh.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#f3e5e0');
      sh.setFrozenRows(1);
      sh.setColumnWidth(1, 150);
      sh.setColumnWidth(6, 320);
      sh.setColumnWidth(7, 260);
    }
    sh.appendRow([
      new Date(),
      str(data.name),
      str(data.attending),
      str(data.party),
      str(data.guests),
      str(data.message),
      str(data.page)
    ]);
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (e2) {}
  }
}

// Mở URL .../exec bằng trình duyệt sẽ thấy dòng này -> deploy OK.
function doGet() {
  return ContentService.createTextOutput('RSVP endpoint OK');
}

function str(v) {
  return v == null ? '' : String(v);
}

// Tên tab Google Sheet không được chứa: \ / ? * [ ] : ' và tối đa 100 ký tự.
function sanitizeTab(t) {
  t = str(t).trim() || 'khach';
  t = t.replace(/[\\\/\?\*\[\]:']/g, '-');
  return t.substring(0, 90);
}

function json(o) {
  return ContentService
    .createTextOutput(JSON.stringify(o))
    .setMimeType(ContentService.MimeType.JSON);
}
