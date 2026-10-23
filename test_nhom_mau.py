"""Hai ví dụ cách viết test. Sao chép thành test_nhom.py, thay/bổ sung dữ liệu
và khẳng định riêng; cần ít nhất 10 test có nội dung khác test_mau.py.
"""
import unittest
from search import solve
from puzzle import GOAL, check_path, make_heuristic

class NhomTests(unittest.TestCase):
    def test_tinh_tay_ba_buoc(self):
        # Tự suy: D,R,R đưa ô trống về đích, đúng 3 bước.
        start=(1,2,3,0,5,6,4,7,8)
        r=solve(start)
        self.assertEqual(r['cost'],3)
        self.assertEqual(check_path(start,GOAL,r['path'],r['actions']),3)
    def test_so_sanh_chi_phi_dich_moi(self):
        goal=(1,2,3,4,5,6,0,7,8)
        start=(1,2,3,4,5,6,7,8,0)
        r=solve(start,goal,model='directional',heuristic='weighted')
        # Hai bước L giá 2 mỗi bước; tính trước khi chạy.
        self.assertEqual(r['steps'],2)
        self.assertEqual(r['cost'],4)
    def test_dich_tuy_chinh(self):
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

    def test_heuristic_bang_0_tai_dich_va_bo_qua_o_trong(self):
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

if __name__=='__main__':unittest.main()
