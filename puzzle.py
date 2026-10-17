"""Luật xếp hình 8 ô. Các hàm không sửa trạng thái đầu vào.
Mọi tên hành động U/D/L/R đều chỉ hướng di chuyển của Ô TRỐNG.
"""
from __future__ import annotations
from typing import Callable, Iterable

State = tuple[int, ...]
GOAL: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)
ORDER = "UDLR"
DELTAS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def validate_state(state: Iterable[int]) -> State:
    """Chỉ nhận đúng chín số nguyên 0..8, mỗi số một lần (không nhận bool)."""
    try:
        s = tuple(state)
    except TypeError as exc:
        raise ValueError("Trang thai phai la day gom 9 so nguyen.") from exc
    if len(s) != 9 or any(type(v) is not int for v in s) or set(s) != set(range(9)):
        raise ValueError("Trang thai phai chua dung moi so 0..8 mot lan.")
    return s


def validate_order(order: str) -> str:
    if not isinstance(order, str) or len(order) != 4 or set(order) != set(ORDER):
        raise ValueError("Thu tu phai la hoan vi cua UDLR.")
    return order


def is_solvable(start: State, goal: State = GOAL) -> bool:
    """Quy tắc cho bàn 3x3: số nghịch thế so với thứ tự goal phải chẵn.
    Bỏ số 0 trước khi đếm. Hàm KHÔNG dùng quy tắc này cho bàn 4x4.
    """
    s, g = validate_state(start), validate_state(goal)
    rank = {tile: i for i, tile in enumerate(t for t in g if t != 0)}
    sequence = [rank[t] for t in s if t != 0]
    inversions = sum(sequence[i] > sequence[j]
                     for i in range(8) for j in range(i + 1, 8))
    return inversions % 2 == 0


def neighbors(state: State, model: str = "unit", order: str = ORDER):
    """Sinh (action, new_state, cost). state đã được kiểm ở cửa vào solve.
    unit: mọi bước giá 1; directional: U/D giá 1, L/R giá 2.
    """
    if model not in ("unit", "directional"):
        raise ValueError("model chi nhan unit hoac directional")
    validate_order(order)
    zero = state.index(0)
    r, c = divmod(zero, 3)
    for action in order:
        dr, dc = DELTAS[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            target = 3 * nr + nc
            new = list(state)
            new[zero], new[target] = new[target], new[zero]
            cost = 2 if model == "directional" and dc else 1
            yield action, tuple(new), cost


def make_heuristic(goal: State = GOAL, name: str = "manhattan",
                   model: str = "unit") -> Callable[[State], int]:
    """zero / misplaced / manhattan / weighted. Tuyệt đối không đếm số 0."""
    goal = validate_state(goal)
    if model not in ("unit", "directional"):
        raise ValueError("Sai mo hinh chi phi")
    if name not in ("zero", "misplaced", "manhattan", "weighted"):
        raise ValueError("Heuristic khong hop le")
    position = {tile: divmod(i, 3) for i, tile in enumerate(goal)}
    def h(state: State) -> int:
        if name == "zero":
            return 0
        if name == "misplaced":
            return sum(t != 0 and t != goal[i] for i, t in enumerate(state))
        result = 0
        horizontal_weight = 2 if name == "weighted" and model == "directional" else 1
        for i, tile in enumerate(state):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            rg, cg = position[tile]
            result += abs(r - rg) + horizontal_weight * abs(c - cg)
        return result
    return h


def show(state: State) -> str:
    return "\n".join(" ".join(str(v) if v else "." for v in state[i:i+3])
                     for i in (0, 3, 6))


def check_path(start: State, goal: State, path: list[State], actions: list[str],
               model: str = "unit") -> int:
    """Kiểm từng bước; trả tổng chi phí thật. Lỗi nếu đường đi không hợp lệ."""
    if not path or tuple(path[0]) != tuple(start) or tuple(path[-1]) != tuple(goal):
        raise ValueError("Duong di thieu dau hoac dich.")
    if len(path) != len(actions) + 1:
        raise ValueError("So trang thai phai bang so hanh dong + 1.")
    total = 0
    for state, action, successor in zip(path, actions, path[1:]):
        choices = {a: (s, c) for a, s, c in neighbors(tuple(state), model)}
        if action not in choices or choices[action][0] != tuple(successor):
            raise ValueError("Phat hien buoc di khong hop le.")
        total += choices[action][1]
    return total
