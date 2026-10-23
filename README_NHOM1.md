# README BÀI NỘP — Nhóm 1
Học phần: Biểu diễn tri thức và tìm kiếm nâng cao. Giảng viên: Nguyễn Bích Vân.

Đổi tên tệp thành `README_NHOM1.md` và thay các chỗ [Điền].

## Môi trường đã kiểm tra
- Hệ điều hành / phiên bản Python: Windows 11 / 3.12.10
- Máy của thành viên đã giải nén chạy lại: Đoàn Mai Trúc Linh
- Phần được dùng lại từ mã mẫu: puzzle.py, run.py, tao_du_lieu.py, search.py, dong_goi.py, kiem_tra_moi_truong.py, data_case.py bao gồm thuật toán BFS, UCS, A*, cơ chế sinh con `neighbors`, kiểm tra `is_solvable`, `validate_state` và khởi tạo `make_heuristic`.
- Phần nhóm tự thay / viết / kiểm chứng:
* `du_lieu_nhom.json`: Tự sinh dữ liệu riêng cho 2 bàn N1, N2 dùng chung một trạng thái đích mới G' = (1, 2, 3, 4, 5, 6, 0, 7, 8). 
* `test_nhom.py`: Xây dựng 10 unit test tự động (mỗi thành viên 2 test) 
* `DongGop.csv`: Khai báo phân công công việc và % đóng góp của 5 thành viên. 
* `TinhTay.pdf`, `BaoCao.pdf`, `ThuyetTrinh.pdf`.

## Tái tạo kết quả
Mở Terminal trong thư mục đã giải nén. Tất cả mã ở cùng một thư mục.
```text
python kiem_tra_moi_truong.py
python -m unittest -v test_nhom
python run.py --suite --tag bat_buoc
python run.py --data du_lieu_nhom.json --suite --tag tu_tao
python run.py --case HAND --algo astar --heuristic manhattan --trace 6 --tag tinh_tay
```
Lệnh bổ sung minh chứng đổi thứ tự / phát hiện lỗi: 
* Lệnh đổi thứ tự mở rộng con sang RDLU trên trạng thái H: `python run.py --case HAND --order RDLU --trace 6 --tag doi_thu_tu`
* Lệnh xuất tệp log kiểm thử thực tế vào thư mục output/: `python -m unittest -v test_nhom *> output/ket_qua_test.txt`
Nếu có khảo sát thời gian: [Lệnh với --repeat 3, không có trace/step; hoặc ghi không thực hiện].

## Đầu ra
`output/bat_buoc.csv/.json`: 36 dòng; `output/tu_tao.csv/.json`: 18 dòng.
`output/ket_qua_test.txt`: log thực chạy test_nhom; không tự ghi “PASS” khi chưa chạy.
Tên tệp/bảng dùng cho mỗi nhận xét trong báo cáo:
* Bảng 36 cấu hình chung: `output/bat_buoc.csv` (dùng cho Mục 6 và 7 trong `BaoCao.pdf`).
* Bảng 18 cấu hình riêng: `output/tu_tao.csv` (dùng cho Mục 8 trong `BaoCao.pdf`).
* Log vết 6 bước tính tay H: `output/tinh_tay.json` và `output/tinh_tay.csv` (dùng cho Mục 4 trong `BaoCao.pdf`).
* Lệnh thử nghiệm RDLU: `output/doi_thu_tu.csv` (dùng cho Mục 9 trong `BaoCao.pdf`).
* Log kiểm thử: `output/ket_qua_test.txt` (dùng cho Mục 6 trong `BaoCao.pdf`).

## Tạo dữ liệu riêng
Seed / số bước xáo trộn / goal / cách kiểm chứng: 2026 / 16 / 123456078 / Chạy thuật toán BFS trên cả 2 bàn N1 và N2 (`python run.py --data du_lieu_nhom.json --case N1 --algo bfs --model unit` và N2). Kết quả BFS xác nhận độ dài lời giải tối ưu thực tế của N1 là 16 bước (`steps=16`) và N2 là 14 bước (`steps=14`), thỏa mãn điều kiện độ dài từ 6 đến 24 bước. Số bước xáo trộn 16 không được dùng thay cho số bước tối ưu.  .

## Hạn chế và nguồn
[Dữ liệu/thuật toán/thư viện dùng lại; giới hạn tài nguyên; phần chưa làm hoặc kiểm thử chưa đạt.]
- Nguồn: Toàn bộ khung mã mẫu từ data_case.py, puzzle.py, search.py,.. từ file ZIP có sẵn
- Giới hạn tài nguyên: Thuật toán BFS/UCS bị hạn chế về bộ nhớ biên `max_frontier` khi giải các trạng thái sâu (như M3, M4) do số lượng nút sinh ra tăng theo hàm mũ.

