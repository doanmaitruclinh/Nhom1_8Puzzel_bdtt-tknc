"""Hai ví dụ cách viết test. Sao chép thành test_nhom.py, thay/bổ sung dữ liệu
và khẳng định riêng; cần ít nhất 10 test có nội dung khác test_mau.py.
"""
import unittest
from search import solve
from puzzle import GOAL, check_path

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

if __name__=='__main__':unittest.main()
