"""Hai ví dụ cách viết test. Sao chép thành test_nhom.py, thay/bổ sung dữ liệu
và khẳng định riêng; cần ít nhất 10 test có nội dung khác test_mau.py.
"""
import unittest
from search import solve
from puzzle import GOAL, check_path, validate_state, is_solvable, make_heuristic

def bad_heuristic_count_zero(state, goal):  
    pos_goal = {tile: divmod(i, 3) for i, tile in enumerate(goal)} 
    res = 0 
    for i, tile in enumerate(state): 
        # LỖI: Thiếu câu lệnh 'if tile == 0: continue' 
        r, c = divmod(i, 3) 
        rg,cg = pos_goal[tile]
        res += abs(r - rg) + abs(c - cg) 
        return res 
def bad_heuristic_fixed_goal(state, goal=None): 
    fixed_goal = (1, 2, 3, 4, 5, 6, 7, 8, 0) 
    pos_fixed = {tile: divmod(i, 3) for i, tile in enumerate(fixed_goal)} 
    res = 0 
    for i, tile in enumerate(state): 
        if tile == 0: 
            continue 
        r, c = divmod(i, 3) 
        rg, cg = pos_fixed[tile] 
        res += abs(r - rg) + abs(c - cg)
        return res 

class NhomTests(unittest.TestCase):
    def trang_thai_dau_trung_dich(self): #test 1
        start = (1, 2, 3, 4, 5, 6, 0, 7, 8) 
        r = solve(start, goal=GOAL, model="unit", algorithm="astar") 
        self.assertEqual(r["status"], "solved") 
        self.assertEqual(r["steps"], 0) 
        self.assertEqual(r["cost"], 0) 
        self.assertEqual(r["path"], [GOAL]) 
        self.assertEqual(r["actions"], []) 
    def chuyen_dich_mot_buoc_ngang_doc(self): #test 2
        # 1. Trạng thái cách G' đúng 1 bước dọc (0 đi Down) có chi phí là 1: 
        start_doc = (1, 2, 3, 0, 5, 6, 4, 7, 8) 
        r_doc = solve(start_doc, goal=GOAL, model="directional", algorithm="astar") 
        self.assertEqual(r_doc["steps"], 1) 
        self.assertEqual(r_doc["cost"], 1) 
        self.assertEqual(r_doc["actions"], ["D"]) 
        # 2. Trạng thái cách G' đúng 1 bước ngang (0 đi Left) có chi phí là 2:
        start_ngang = (1, 2, 3, 4, 5, 6, 7, 0, 8) 
        r_ngang = solve(start_ngang, goal=GOAL, model="directional", algorithm="astar") 
        self.assertEqual(r_ngang["steps"], 1) 
        self.assertEqual(r_ngang["cost"], 2)
    def bat_loi_heuristic_dem_ca_khong(self): 
        start = (1, 2, 3, 0, 5, 6, 4, 7, 8) 
        h_chuan = make_heuristic(GOAL, heuristic="manhattan", model="unit") 
        val_chuan = h_chuan(start) 
        val_sai = bad_heuristic_count_zero(start, GOAL) 
        self.assertEqual(val_chuan, 1) 
        self.assertEqual(val_sai, 2) 
        # Ô 0 lệch vị trí bị đếm thêm 1 
        self.assertGreater(val_sai, val_chuan, "Hàm sai đã vi phạm tính chấp nhận được khi lớn hơn h chuẩn!") 
    def bat_loi_heuristic_fixed_goal(self): 
        val_sai = bad_heuristic_fixed_goal(GOAL) 
        self.assertNotEqual(val_sai, 0, "Hàm sai không nhận biết được đích mới G'!") 
        self.assertEqual(val_sai, 2)  

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
    
    def test_heuristic_bang_0_tai_dich_va_bo_qua_o_trong(self): #test 5
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

    def test_astar_zero_equals_ucs_and_bfs_directional_cost(self): #test 9
        start_state = (1, 3, 6, 5, 0, 2, 4, 7, 8)

        # Đối chiếu A* (h=0) vs UCS
        res_ucs = solve(start_state, algorithm='ucs', model='unit')
        res_astar_zero = solve(start_state, algorithm='astar', heuristic='zero', model='unit')

        metrics = ('path', 'cost', 'expanded', 'generated', 'pushed', 'popped')
        for key in metrics:
            self.assertEqual(
                res_ucs[key], res_astar_zero[key], 
                f"Chỉ số {key} giữa UCS và A*(h=0) không trung khớp!"
            )

        # BFS không bao đảm chi phí tối ưu ở directional
        res_bfs_dir = solve(start_state, algorithm='bfs', model='directional')
        res_ucs_dir = solve(start_state, algorithm='ucs', model='directional')

        # BFS đạt số bước (steps) ít hơn hoặc bằng UCS
        self.assertLessEqual(
            res_bfs_dir['steps'], res_ucs_dir['steps'], 
            "BFS phải đạt số bước ít hơn hoặc bằng UCS."
        )

        # Nhưng chi phí (cost) của UCS phải nhỏ hơn hoặc bằng BFS
        self.assertLessEqual(
            res_ucs_dir['cost'], res_bfs_dir['cost'],
            "Chi phí của UCS phải nhỏ hơn hoặc bằng BFS trong mô hình directional."
        )

    def test_trace_independence_and_resource_limit(self): #test 10
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
            self.assertEqual(
                res_no_trace[key], res_with_trace[key],
                f"Chỉ số {key} bị thay đổi khi bật trace_limit!"
            )

        # Dừng do giới hạn tài nguyên (max_expanded)
        # Đặt max_expanded = 2
        res_limit = solve(start_state, algorithm='astar', heuristic='manhattan', max_expanded=2)

        self.assertEqual(
            res_limit['status' ], 'limit',
            "Khi vượt quá max_expanded, status phải trả về 'limit'."
        )

        self.assertEqual(
            res_limit['path'], [],
            "Khi chưa tìm thấy lời giải do chạm limit, path phải trả về rỗng []."
        )

if __name__=='__main__':unittest.main()
