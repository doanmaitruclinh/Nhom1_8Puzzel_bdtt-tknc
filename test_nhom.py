"""Hai ví dụ cách viết test. Sao chép thành test_nhom.py, thay/bổ sung dữ liệu
và khẳng định riêng; cần ít nhất 10 test có nội dung khác test_mau.py.
"""
import unittest
from search import solve
from puzzle import GOAL, check_path

class NhomTests(unittest.TestCase):
    def test_zero_equals_ucs(self):
        a=solve(,algorithm='ucs');b=solve(,heuristic='zero')
        for k in ('path','cost','expanded','generated','pushed','popped'):
            self.assertEqual(a[k],b[k])
    def test_trace_no_result_change(self):
        a=solve(DEMO);b=solve(DEMO,trace_limit=2)
        for k in ('path','cost','expanded','generated','pushed','popped'):self.assertEqual(a[k],b[k])
    def test_trace_independent(self):
        r=solve(DEMO,trace_limit=10)
        self.assertIsNot(r['trace'][0],r['trace'][1])
        self.assertNotEqual(r['trace'][0]['state'],r['trace'][1]['state'])
    def test_zero_limit_goal(self):
        self.assertEqual(solve(GOAL,max_expanded=0)['status'],'solved')
    def test_limit_not_unsolvable(self):
        self.assertEqual(solve(DEMO,max_expanded=0)['status'],'limit')
if __name__=='__main__':unittest.main()
