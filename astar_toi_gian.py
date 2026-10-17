"""A* ngắn, chạy độc lập cùng puzzle.py để đọc ý tưởng trước bản có thống kê.
Hòa f dùng FIFO; h nhất quán; chỉ thay cha khi g tốt hơn hẳn.
"""
from heapq import heappush, heappop
from itertools import count
from puzzle import GOAL, neighbors, make_heuristic, validate_state, is_solvable


def astar(start, goal=GOAL, model="unit", heuristic="manhattan"):
    start, goal = validate_state(start), validate_state(goal)
    if not is_solvable(start, goal):
        return None
    h = make_heuristic(goal, heuristic, model)
    serial = count()
    frontier = [(h(start), next(serial), 0, start)]
    best_g, parent = {start: 0}, {start: None}
    while frontier:
        f, _, g, state = heappop(frontier)           # 1. Chọn f nhỏ nhất
        if g != best_g[state]:                     # 2. Bỏ bản ghi cũ
            continue
        if state == goal:                          # 3. Chỉ dừng ở đây
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return list(reversed(path)), g
        for action, child, cost in neighbors(state, model):
            new_g = g + cost                       # 4. Giá tới con
            if new_g < best_g.get(child, float("inf")):
                best_g[child], parent[child] = new_g, state
                heappush(frontier, (new_g+h(child), next(serial), new_g, child))
    return None

if __name__ == "__main__":
    start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    answer = astar(start)
    if answer is None:
        print("Khong co loi giai")
    else:
        path, cost = answer
        print("So buoc:", len(path)-1, "Chi phi:", cost)
        print(*path, sep="\n")
