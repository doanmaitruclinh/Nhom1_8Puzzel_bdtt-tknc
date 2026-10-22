"""Hai ví dụ cách viết test. Sao chép thành test_nhom.py, thay/bổ sung dữ liệu
và khẳng định riêng; cần ít nhất 10 test có nội dung khác test_mau.py.
"""
import unittest
from search import solve
from puzzle import GOAL, check_path

class NhomTests(unittest.TestCase):
    

    def test_kiem_tra_duong_di_va_chi_phi_hop_le(self): #test 7
        start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        r = solve(start, goal=GOAL, algorithm='astar', heuristic='manhattan', model='unit')

        self.assertEqual(r['status'], 'solved')
        # check_path trả tổng chi phí thật, hoặc raise ValueError nếu đường đi sai
        cost_thuc = check_path(start, GOAL, r['path'], r['actions'], model='unit')
        self.assertEqual(cost_thuc, r['cost'],
            "Chi phí solve báo không khớp chi phí kiểm lại theo luật chuyển trạng thái.")
        self.assertEqual(r['cost'], 2)
        # print(r['status'], r['cost'], r['steps'], r['actions'])
        # print("check_path =", cost_thuc)

    
    def test_dau_vao_bat_bien(self):  # test 8
        start = [1, 2, 3, 4, 0, 6, 7, 5, 8]
        snapshot = list(start)

        r = solve(start, goal=GOAL, algorithm='astar', heuristic='manhattan', model='unit')

        self.assertEqual(start, snapshot)                     
        self.assertEqual(r['path'][0], tuple(snapshot)) 
        


    def test_bfs_khong_toi_uu_gia_o_directional(self):
        M3 = (0, 8, 2, 4, 6, 3, 7, 1, 5)
        r_bfs = solve(M3, algorithm='bfs', model='directional')
        r_ucs = solve(M3, algorithm='ucs', model='directional')
        self.assertEqual(r_bfs['status'], 'solved')
        self.assertEqual(r_ucs['status'], 'solved')
        self.assertEqual(r_bfs['steps'], 20)               # ít bước nhất
        self.assertEqual(r_ucs['cost'], 28)                # giá tối ưu
        self.assertGreater(r_bfs['cost'], r_ucs['cost'])   # BFS đắt hơn

    def test_h_dem_ca_0(self):
       #test bắt lỗi heuristic đếm cả ô trống nếu khác vị trí
        state_V = (1, 2, 3, 4, 5, 6, 7, 0, 8)
        goal_G  = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        h_star = 1   # Chi phí thực tế tối thiểu từ V về G

        # Hàm heuristic đếm cả ô 0 nếu khác vị trí
        def h_dem_ca_0(state, goal):
            return sum(1 for i in range(9) if state[i] != goal[i])

        h_calculated = h_dem_ca_0(state_V, goal_G)
        
        # Khẳng định heuristic sai phạm tính chấp nhận được (h > h*)
        self.assertGreater(h_calculated, h_star)
        
        

    def test_h_dung_vi_tri_dich_co_dinh(self):
        # bắt lỗi 2: cố định goal thay vì goal tùy chỉnh
        goal_prime = (1, 2, 3, 4, 5, 6, 0, 7, 8)

        # Hàm heuristic sai: cố định tính Manhattan theo GOAL chuẩn thay vì goal_prime
        def h_wrong_fixed_goal(state, custom_goal):
            fixed_goal_pos = {tile: divmod(idx, 3) for idx, tile in enumerate(GOAL)}
            h_val = 0
            for idx, tile in enumerate(state):
                if tile == 0: continue
                r, c = divmod(idx, 3)
                rg, cg = fixed_goal_pos[tile]
                h_val += abs(r - rg) + abs(c - cg)
            return h_val

        h_at_goal = h_wrong_fixed_goal(goal_prime, custom_goal=goal_prime)
        
        # Khẳng định tại đích tùy chỉnh nhưng h khác 0
        self.assertNotEqual(h_at_goal, 0)
        
        
if __name__=='__main__':unittest.main()
