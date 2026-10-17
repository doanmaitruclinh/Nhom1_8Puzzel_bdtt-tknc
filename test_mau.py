"""Kiểm thử mẫu công khai. Nhóm viết test_nhom.py riêng, ít nhất 10 test.
Không đổi tên các test này thành kiểm thử mới của nhóm.
"""
import unittest
from puzzle import GOAL, validate_state, is_solvable, neighbors, make_heuristic, check_path
from search import solve
from astar_toi_gian import astar

ONE_H = (1,2,3,4,5,6,7,0,8)
ONE_V = (1,2,3,4,5,0,7,8,6)
DEMO = (1,2,3,4,0,6,7,5,8)

class ModelTests(unittest.TestCase):
    def test_validate_duplicate(self):
        with self.assertRaises(ValueError):validate_state((0,1,2,3,4,5,6,7,7))
    def test_validate_bool(self):
        with self.assertRaises(ValueError):validate_state((False,1,2,3,4,5,6,7,8))
    def test_corner_neighbors(self):
        self.assertEqual([a for a,s,c in neighbors(GOAL)], ["U","L"])
    def test_center_neighbors(self):
        self.assertEqual([a for a,s,c in neighbors(DEMO)], list("UDLR"))
    def test_directional_costs(self):
        self.assertEqual({a:c for a,s,c in neighbors(DEMO,'directional')},dict(U=1,D=1,L=2,R=2))
    def test_no_input_mutation(self):
        old=DEMO;list(neighbors(DEMO));self.assertEqual(DEMO,old)
    def test_unsolvable_parity(self):
        self.assertFalse(is_solvable((1,2,3,4,5,6,8,7,0)))
    def test_different_goal(self):
        self.assertTrue(is_solvable(ONE_H,(1,2,3,4,5,6,0,7,8)))
    def test_goal_heuristics_zero(self):
        for name in ('misplaced','manhattan','weighted'):
            self.assertEqual(make_heuristic(name=name,model='directional')(GOAL),0)
    def test_exclude_zero(self):
        self.assertEqual(make_heuristic(name='misplaced')(ONE_V),1)
        self.assertEqual(make_heuristic(name='manhattan')(ONE_V),1)
    def test_weighted_hv(self):
        h=make_heuristic(name='weighted',model='directional')
        self.assertEqual(h(ONE_H),2);self.assertEqual(h(ONE_V),1)
    def test_reject_bad_path(self):
        with self.assertRaises(ValueError):check_path(ONE_H,GOAL,[ONE_H,GOAL],["U"])

class SearchTests(unittest.TestCase):
    def test_already_goal(self):
        r=solve(GOAL);self.assertEqual((r['steps'],r['cost'],r['expanded']),(0,0,0))
        self.assertEqual(r['popped'],1)
    def test_zero_limit_goal(self):
        self.assertEqual(solve(GOAL,max_expanded=0)['status'],'solved')
    def test_limit_not_unsolvable(self):
        self.assertEqual(solve(DEMO,max_expanded=0)['status'],'limit')
    def test_unsolvable_no_search(self):
        r=solve((1,2,3,4,5,6,8,7,0));self.assertEqual(r['status'],'unsolvable')
        self.assertEqual(r['popped'],0)
    def test_one_horizontal(self):
        r=solve(ONE_H,model='directional',heuristic='weighted')
        self.assertEqual((r['steps'],r['cost']),(1,2));self.assertEqual(r['actions'],['R'])
    def test_one_vertical(self):
        self.assertEqual(solve(ONE_V,model='directional')['cost'],1)
    def test_demo_all(self):
        for alg,h in [('bfs','zero'),('ucs','zero'),('astar','misplaced'),('astar','manhattan')]:
            r=solve(DEMO,algorithm=alg,heuristic=h)
            self.assertEqual((r['steps'],r['cost']),(2,2))
    def test_demo_path_cost(self):
        r=solve(DEMO,model='directional',heuristic='weighted')
        self.assertEqual(check_path(DEMO,GOAL,r['path'],r['actions'],'directional'),3)
    def test_goal_parameter(self):
        g=(1,2,3,4,5,6,0,7,8);r=solve(ONE_H,g)
        self.assertEqual((r['steps'],r['actions']),(1,['L']))
    def test_zero_equals_ucs(self):
        a=solve(DEMO,algorithm='ucs');b=solve(DEMO,heuristic='zero')
        for k in ('path','cost','expanded','generated','pushed','popped'):
            self.assertEqual(a[k],b[k])
    def test_fifo_bfs_equals_ucs_unit(self):
        a=solve(DEMO,algorithm='ucs');b=solve(DEMO,algorithm='bfs')
        for k in ('path','cost','expanded','generated','pushed','popped'):
            self.assertEqual(a[k],b[k])
    def test_trace_independent(self):
        r=solve(DEMO,trace_limit=10)
        self.assertIsNot(r['trace'][0],r['trace'][1])
        self.assertNotEqual(r['trace'][0]['state'],r['trace'][1]['state'])
    def test_trace_no_result_change(self):
        a=solve(DEMO);b=solve(DEMO,trace_limit=2)
        for k in ('path','cost','expanded','generated','pushed','popped'):self.assertEqual(a[k],b[k])
    def test_minimal_matches_main(self):
        path,cost=astar(DEMO);r=solve(DEMO)
        self.assertEqual((path,cost),(r['path'],r['cost']))
    def test_repeat_deterministic(self):
        a=solve(DEMO);b=solve(DEMO)
        for k in a:
            if k!='elapsed_ms':self.assertEqual(a[k],b[k])
    def test_invalid_order(self):
        with self.assertRaises(ValueError):solve(DEMO,order='UDLL')

if __name__=='__main__':unittest.main()
