import unittest
from search import solve
from puzzle import GOAL, check_path, make_heuristic

class NhomTests(unittest.TestCase):
    def test_trang_thai_dau_trung_dich(self): #test 1
        start = (1, 2, 3, 4, 5, 6, 0, 7, 8) 
        goal = (1,2,3,4,5,6,0,7,8)
        r = solve(start, goal, model="unit", algorithm="astar") 
        self.assertEqual(r["status"], "solved") 
        self.assertEqual(r["steps"], 0) 
        self.assertEqual(r["cost"], 0) 
        self.assertEqual(r["path"], [goal]) 
        self.assertEqual(r["actions"], []) 
    def test_chuyen_dich_mot_buoc_ngang_doc(self): #test 2
        # 1. Trạng thái cách G' đúng 1 bước dọc (0 đi Down) có chi phí là 1: 
        start_doc = (1, 2, 3, 0, 5, 6, 4, 7, 8)
        goal = (1,2,3,4,5,6,0,7,8)
        r_doc = solve(start_doc, goal, model="directional", algorithm="astar") 
        self.assertEqual(r_doc["steps"], 1) 
        self.assertEqual(r_doc["cost"], 1) 
        self.assertEqual(r_doc["actions"], ["D"]) 
        # 2. Trạng thái cách G' đúng 1 bước ngang (0 đi Left) có chi phí là 2:
        start_ngang = (1, 2, 3, 4, 5, 6, 7, 0, 8) 
        r_ngang = solve(start_ngang, goal, model="directional", algorithm="astar") 
        self.assertEqual(r_ngang["steps"], 1) 
        self.assertEqual(r_ngang["cost"], 2)

    def test_dich_tuy_chinh(self): #test 3
        goal = (1, 2, 3, 4, 5, 6, 0, 7, 8)
        start = (6, 1, 3, 5, 0, 2, 4, 7, 8)
        r_unit = solve(start, goal, model='unit', heuristic='manhattan')
        self.assertEqual((r_unit["steps"], r_unit["cost"]), (16, 16))
        self.assertEqual(r_unit["status"], "solved")
        self.assertEqual(r_unit["goal"], goal)
        self.assertEqual(r_unit["path"][0], start)
        self.assertEqual(r_unit["path"][-1], goal)
        self.assertEqual(check_path(start, goal, r_unit["path"], r_unit["actions"]), 16)
        r_directional = solve(start, goal, model='directional', heuristic='weighted')
        self.assertEqual((r_directional["steps"], r_directional["cost"]), (16, 25))
        self.assertEqual(r_directional["status"], "solved")
        self.assertEqual(r_directional["goal"], goal)
        self.assertEqual(r_directional["path"][0], start)
        self.assertEqual(r_directional["path"][-1], goal)
        self.assertEqual(
            check_path(start, goal, r_directional["path"],
                        r_directional["actions"], "directional"),
            25,
        )
    
    def test_heuristic_bang_0_tai_dich_va_bo_qua_o_trong(self): #test 4
        goal = (1, 2, 3, 4, 5, 6, 0, 7, 8)
        state = GOAL # (1, 2, 3, 4, 5, 6, 7, 8, 0)
    
        # So sánh GOAL và goal tùy chỉnh: 7 và 8 lệch mỗi ô một bước, ô trống bị bỏ qua 
        # Vậy khoảng cách = chi phí = số ô sai vị trí = 2 với unit
        # Với directional nhân trọng số 2 do di chuyển ngang
        expected = {
            ("misplaced", "unit"): 2,   
            ("manhattan", "unit"): 2,   
            ("weighted", "unit"): 2,    
            ("weighted", "directional"): 4,     
        }
        # heuristic "zero" luôn bằng 0, không cần model
        self.assertEqual(make_heuristic(goal, name="zero")(goal), 0)
    
        for (name, model), value in expected.items():
            with self.subTest(heuristic=name, model=model):
                heuristic = make_heuristic(goal, name=name, model=model)
                self.assertEqual(heuristic(goal), 0)    # Kiểm tra: Tại goal, mọi heuristic bằng 0
                self.assertEqual(heuristic(state), value)   

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
    
    def test_dau_vao_bat_bien(self): #test 8
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

    def test_doi_chieu_astar_zero_va_ucs(self): #test 9
        start_state = (1, 3, 6, 5, 0, 2, 4, 7, 8)

        # Đối chiếu A* (h=0) vs UCS
        res_ucs = solve(start_state, algorithm='ucs', model='unit')
        res_astar_zero = solve(start_state, algorithm='astar', heuristic='zero', model='unit')

        metrics = ('path', 'cost', 'expanded', 'generated', 'pushed', 'popped')
        for key in metrics:
            self.assertEqual(res_ucs[key], res_astar_zero[key], 
                f"Chỉ số {key} giữa UCS và A*(h=0) không trung khớp!")

    def test_doc_lap_trace_va_gioi_han_tai_nguyen(self): #test 10
        start_state = (1, 3, 6, 5, 0, 2, 4, 7, 8)

        # Tính độc lập của trace 
        res_no_trace = solve(start_state, algorithm='astar', heuristic='manhattan')
        res_with_trace = solve(start_state, algorithm='astar', heuristic='manhattan', trace_limit=5)

        # Vết chạy phải lưu đúng tối đa 5 bản ghi
        self.assertIn('trace', res_with_trace)
        self.assertLessEqual(len(res_with_trace['trace']), 5)

        # Kết quả tìm kiếm chính không được thay đổi khi bật trace
        metrics = ('path', 'cost', 'expanded', 'generated', 'pushed', 'popped')
        for key in metrics:
            self.assertEqual(res_no_trace[key], res_with_trace[key],
                            f"Chỉ số {key} bị thay đổi khi bật trace_limit!")

        # Dừng do giới hạn tài nguyên (max_expanded)
        # Đặt max_expanded = 2
        res_limit = solve(start_state, algorithm='astar', heuristic='manhattan', max_expanded=2)
        self.assertEqual(res_limit['status' ], 'limit', "Khi vượt quá max_expanded, status phải trả về 'limit'.")
        self.assertEqual(res_limit['path'], [], "Khi chưa tìm thấy lời giải do chạm limit, path phải trả về rỗng [].")

if __name__=='__main__':unittest.main()
