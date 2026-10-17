# README BÀI NỘP — [Tên nhóm]
Học phần: Biểu diễn tri thức và tìm kiếm nâng cao. Giảng viên: Nguyễn Bích Vân.

Đổi tên tệp thành `README_NHOM1.md` và thay các chỗ [Điền].

## Môi trường đã kiểm tra
- Hệ điều hành / phiên bản Python: [Điền]
- Máy của thành viên đã giải nén chạy lại: [Điền]
- Phần được dùng lại từ mã mẫu: [Điền tên tệp/hàm]
- Phần nhóm tự thay / viết / kiểm chứng: [Điền, không chỉ nêu đổi tên biến]

## Tái tạo kết quả
Mở Terminal trong thư mục đã giải nén. Tất cả mã ở cùng một thư mục.
```text
python kiem_tra_moi_truong.py
python -m unittest -v test_nhom
python run.py --suite --tag bat_buoc
python run.py --data du_lieu_nhom.json --suite --tag tu_tao
python run.py --case HAND --algo astar --heuristic manhattan --trace 6 --tag tinh_tay
```
Lệnh bổ sung minh chứng đổi thứ tự / phát hiện lỗi: [Điền]
Nếu có khảo sát thời gian: [Lệnh với --repeat 3, không có trace/step; hoặc ghi không thực hiện].

## Đầu ra
`output/bat_buoc.csv/.json`: 36 dòng; `output/tu_tao.csv/.json`: 18 dòng.
`output/ket_qua_test.txt`: log thực chạy test_nhom; không tự ghi “PASS” khi chưa chạy.
Tên tệp/bảng dùng cho mỗi nhận xét trong báo cáo: [Điền]

## Tạo dữ liệu riêng
Seed / số bước xáo trộn / goal / cách kiểm chứng: [Điền].
Độ dài xáo trộn không được dùng thay cho số bước tối ưu.

## Hạn chế và nguồn
[Dữ liệu/thuật toán/thư viện dùng lại; giới hạn tài nguyên; phần chưa làm hoặc kiểm thử chưa đạt.]
