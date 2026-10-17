"""Dữ liệu bài giao, không chứa đáp số. Đọc U/D/L/R theo hướng ô trống."""
from puzzle import GOAL
DEMO = (1, 2, 3, 4, 0, 6, 7, 5, 8)
HAND = (1, 3, 6, 5, 0, 2, 4, 7, 8)
CASES = {
    "M1": HAND,
    "M2": (1, 3, 8, 7, 2, 4, 5, 6, 0),
    "M3": (0, 8, 2, 4, 6, 3, 7, 1, 5),
    "M4": (7, 5, 1, 6, 8, 4, 2, 3, 0),
}
UNSOLVABLE = (1, 2, 3, 4, 5, 6, 8, 7, 0)
# Mỗi bàn có 4 cấu hình unit + 5 cấu hình directional = 9.
CONFIGS = [("unit", "bfs", "zero"), ("unit", "ucs", "zero"),
           ("unit", "astar", "misplaced"), ("unit", "astar", "manhattan"),
           ("directional", "bfs", "zero"), ("directional", "ucs", "zero"),
           ("directional", "astar", "misplaced"),
           ("directional", "astar", "manhattan"),
           ("directional", "astar", "weighted")]
