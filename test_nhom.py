import unittest
from search import solve
from puzzle import GOAL, check_path, make_heuristic, validate_state, is_solvable, neighbors

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

    def test_vo_nghiem_do_parity(self):  # test 5
        # Z = (1,2,3,4,5,6,8,7,0): 1 nghịch thế (8 đứng trước 7) -> lẻ -> vô nghiệm với G
        Z = (1, 2, 3, 4, 5, 6, 8, 7, 0)
        r = solve(Z, goal=GOAL, algorithm="astar", heuristic="manhattan", model="unit")
        
        # 1) Kết luận vô nghiệm do parity, KHÔNG phải do hết tài nguyên
        self.assertEqual(r["status"], "unsolvable")
        # 2) Không mở rộng, không sinh con, không push gì (parity là tiền xử lý)
        self.assertEqual(r["expanded"], 0)
        self.assertEqual(r["generated"], 0)
        self.assertEqual(r["pushed"], 0)
        self.assertEqual(r["popped"], 0)
        self.assertEqual(r["path"], [])
        self.assertEqual(r["actions"], [])

        # 3) Phân biệt với "limit": nếu cho max_expanded = 0 thì vẫn phải unsolvable,
        #    vì parity bị loại TRƯỚC khi tìm kiếm.
        r_limit0 = solve(Z, goal=GOAL, algorithm="astar", max_expanded=0)
        self.assertEqual(r_limit0["status"], "unsolvable")

        # 4) Đổi goal thành chính Z thì Z là đích -> không còn vô nghiệm
        self.assertTrue(is_solvable(Z, Z))
        r2 = solve(Z, goal=Z, algorithm="astar")
        self.assertEqual(r2["status"], "solved")
        self.assertEqual((r2["steps"], r2["cost"]), (0, 0))

    def test_du_lieu_sai_va_hanh_dong_vuot_bien(self):  # test 6
        # --- 6a: validate_state phải raise ValueError ---
        bad_states = [
            (1, 2, 3, 4, 5, 6, 7, 8),          # thiếu 1 phần tử
            (0, 1, 2, 3, 4, 5, 6, 7, 9),       # có 9, thiếu 8
            (1, 1, 2, 3, 4, 5, 6, 7, 8),       # trùng số 1
            (False, 1, 2, 3, 4, 5, 6, 7, 8),   # bool không được nhận
        ]
        for bad in bad_states:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_state(bad)
                with self.assertRaises(ValueError):
                    solve(bad)

        # --- 6b: solve() với order sai ---
        with self.assertRaises(ValueError):
            solve(GOAL, order="UDLL")
        with self.assertRaises(ValueError):
            solve(GOAL, model="khong_ton_tai")
        with self.assertRaises(ValueError):
            solve(GOAL, algorithm="dfs")

        # --- 6c: hành động vượt biên bị neighbors lọc, check_path phải từ chối ---
        corner = (0, 1, 2, 3, 4, 5, 6, 7, 8)   # 0 ở góc trên trái
        actions = [a for a, _, _ in neighbors(corner)]
        self.assertEqual(actions, ["D", "R"])   # không sinh U, L

        # Tự tạo một "đường đi giả" dùng hành động U vượt biên -> check_path phải raise
        with self.assertRaises(ValueError):
            check_path(corner, corner, [corner, corner], ["U"])

        # --- 6d: check_path từ chối đường đi sai số trạng thái / sai đích ---
        start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        r = solve(start, goal=GOAL)
        # cắt bớt 1 trạng thái nhưng giữ nguyên actions -> sai len
        with self.assertRaises(ValueError):
            check_path(start, GOAL, r["path"][:-1], r["actions"])
        # đổi đích cuối -> sai đầu-cuối
        with self.assertRaises(ValueError):
            check_path(start, (1, 2, 3, 4, 5, 6, 8, 7, 0), r["path"], r["actions"])

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

    def test_h_dem_ca_o_trong(self):
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
