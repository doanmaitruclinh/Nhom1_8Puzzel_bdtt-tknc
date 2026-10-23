"""Hai ví dụ cách viết test. Sao chép thành test_nhom.py, thay/bổ sung dữ liệu
và khẳng định riêng; cần ít nhất 10 test có nội dung khác test_mau.py.
"""
import unittest
from search import solve
from puzzle import GOAL, check_path

class NhomTests(unittest.TestCase):
    

    def test_duong_di_hop_le_va_dau_vao_bat_bien(self):   # gộp test 7 + 8
        # Phần 1: đường đi hợp lệ, cost khớp luật chuyển trạng thái (đầu vào tuple)
        with self.subTest("duong_di_hop_le"):
            start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
            r = solve(start, goal=GOAL, algorithm='astar', heuristic='manhattan', model='unit')
            self.assertEqual(r['status'], 'solved')
            # check_path trả tổng chi phí thật, hoặc raise ValueError nếu đường đi sai
            cost_thuc = check_path(start, GOAL, r['path'], r['actions'], model='unit')
            self.assertEqual(cost_thuc, r['cost'],
                "Chi phí solve báo không khớp chi phí kiểm lại theo luật chuyển trạng thái.")
            self.assertEqual(r['cost'], 2)

        # Phần 2: đầu vào dạng list (kiểu sửa được) không bị solve sửa tại chỗ
        with self.subTest("dau_vao_bat_bien"):
            start_list = [1, 2, 3, 4, 0, 6, 7, 5, 8]
            snapshot = list(start_list)
            r2 = solve(start_list, goal=GOAL, algorithm='astar', heuristic='manhattan', model='unit')
            self.assertEqual(start_list, snapshot, "solve đã sửa trực tiếp đầu vào!")
            self.assertEqual(r2['path'][0], tuple(snapshot))
            self.assertEqual(r2['cost'], 2)     
        


    def test_bfs_khong_toi_uu_gia_o_directional(self):
        M3 = (0, 8, 2, 4, 6, 3, 7, 1, 5)
        r_bfs = solve(M3, algorithm='bfs', model='directional')
        r_ucs = solve(M3, algorithm='ucs', model='directional')
        self.assertEqual(r_bfs['status'], 'solved')
        self.assertEqual(r_ucs['status'], 'solved')
        self.assertEqual(r_bfs['steps'], 20)               # ít bước nhất
        self.assertEqual(r_ucs['cost'], 28)                # giá tối ưu
        self.assertGreater(r_bfs['cost'], r_ucs['cost'])   # BFS đắt hơn

    
        
        
if __name__=='__main__':unittest.main()
