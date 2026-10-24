# EfforthlessE

Ứng dụng học tiếng Anh theo phương pháp Effortless English, viết bằng HTML, CSS và JavaScript thuần (không framework, không cần build).

- **Khoá học:** tủ sách 9 khoá (Original, Flow, Business, Power, Real, Pronunciation, Pronunciation Workshop, Pimsleur, Phương pháp). Mỗi khoá là một cuốn sách, mỗi trang là một bài với nút nghe theo tên tệp gốc và bài đọc PDF.
- **Luyện thêm:** truyện ngắn, thẻ từ vựng, trò nghe và chọn hình, hỏi đáp nhanh.
- **Phát âm** và **Giao tiếp:** cặp âm dễ nhầm, trọng âm, nói đuổi, hội thoại nhập vai.

## Nguồn âm thanh và PDF

Repo này **không chứa** tệp nghe hay PDF của khoá học. App phát tệp từ thư mục Effortless English trên máy, hoặc từ kho tài liệu riêng khi đặt `window.EFF_BASE` (đường dẫn gốc của kho). Nếu mở `index.html` từ thư mục `F:\Effortless English` trên máy tính, app dùng tệp đã tải về. Trên điện thoại, bấm "Chọn thư mục Effortless English trên máy này" để app phát thẳng tệp đã chép vào điện thoại, không cần mạng.

## Cấu trúc

- `index.html`: app hoàn chỉnh (bản GitHub Pages).
- `src/template.html`: mã nguồn app, chưa có dữ liệu.
- `data/lib.json`: danh sách khoá, bài, tệp nghe và PDF.
- `tools/`: script tạo `lib.json` từ danh sách thư mục và gắn dữ liệu vào template.
