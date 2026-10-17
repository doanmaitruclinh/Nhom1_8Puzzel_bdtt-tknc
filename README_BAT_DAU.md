# GIỮA KỲ 8-PUZZLE NÂNG CAO — 10 NGÀY, NHÓM 5
**Nguyễn Bích Vân | Biểu diễn tri thức và tìm kiếm nâng cao — IAI–UET–VNU**

## Đọc gì và chạy gì?
1. `Nhom1_8Puzzle.pdf`: đề chính.
2. `HuongDan_8Puzzle_Python.pdf`: 8 bước đọc mã, thay dữ liệu, chạy, kiểm thử, đóng gói.
3. `MauBaoCao/`: Word/LaTeX để điền và PDF xem bố cục; không có đáp án bài nộp.

Mã mẫu **đã hoàn chỉnh**, không có TODO hoặc hàm chưa cài. Được dùng nguyên lõi, ghi nguồn.
Mọi tệp chạy đặt ngay ở thư mục này: **không gõ `cd python`**. Giải nén cả gói.

```text
python kiem_tra_moi_truong.py
python chay_mau.py
python astar_toi_gian.py
python -m unittest -v test_mau
python run.py --case DEMO --step --tag demo_step
```

## Thay dữ liệu và thực nghiệm
```text
python tao_du_lieu.py --seed 2026 --steps 16 --goal "1,2,3,4,5,6,0,7,8" --out du_lieu_nhom.json
python run.py --suite --tag bat_buoc
python run.py --data du_lieu_nhom.json --suite --tag tu_tao
python run.py --case HAND --trace 6 --tag tinh_tay
python run.py --case HAND --order RDLU --trace 6 --tag doi_thu_tu
```
36 cấu hình chung + 18 cấu hình riêng = 54 dòng; không nhập từng dòng bằng tay.
Nhóm tự kiểm N1/N2 khác nhau, khác mẫu, có độ dài tối ưu 6–24; goal riêng khác goal chuẩn.
Số bước xáo trộn không thay cho kết quả BFS. Không dùng output ví dụ của giảng viên làm báo cáo tự chạy.

## Tệp cần hoàn thiện
- Tạo `du_lieu_nhom.json` với dữ liệu riêng (mẫu JSON chỉ minh họa cú pháp).
- Tạo `test_nhom.py`: ít nhất 10 test riêng; 2 test mỗi người; 3 kỳ vọng tính tay độc lập.
- Điền báo cáo Word hoặc LaTeX, xuất `BaoCao.pdf`; nộp `TinhTay.pdf` riêng.
- Đổi tên/điền `README_NHOM_MAU.md`, `DongGop_Mau.csv`.
- Tạo 6–8 slide `ThuyetTrinh.pptx` hoặc PDF; bảo vệ 15–20 phút.

```text
python -m unittest -v test_nhom
python -m unittest -v test_nhom > output/ket_qua_test.txt 2>&1
python dong_goi.py --group Nhom01
```

## Quy ước và lỗi thường gặp
U/D/L/R là hướng Ô TRỐNG. Bỏ 0 trong h. Hòa f theo FIFO. Unit mọi bước giá 1;
directional ngang 2, dọc 1. `generated` tính cả con trùng; `expanded` không tính đích.
`--trace 6` chỉ giới hạn log; `--step` dừng thật trước khi sinh con; `--limit` là giới hạn tài nguyên.
`limit` không đồng nghĩa vô nghiệm. Không đo thời gian khi đang in trace/chờ Enter.
Nếu `can't open file`: kiểm Terminal đúng thư mục. Nếu `>>>`: gõ `exit()` trước.
Code chỉ dùng thư viện chuẩn Python 3.10+; các số thời gian phụ thuộc máy.

