"""BFS, UCS, A* hoàn chỉnh; sinh viên được dùng nguyên lõi và khai báo nguồn.
- Hòa độ ưu tiên: FIFO (serial tăng dần).
- best_g chỉ cập nhật khi chi phí tốt hơn HẲN.
- Node là bản ghi bất biến: tránh sửa cha làm biến đổi đường đã lưu.
- Đích được kiểm khi lấy bản ghi hợp lệ ra, không phải khi vừa sinh.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from heapq import heappush, heappop
from itertools import count
from time import perf_counter
from puzzle import State, GOAL, validate_state, validate_order, is_solvable, neighbors, make_heuristic, show


@dataclass(frozen=True)
class Node:
    state: State
    g: int
    depth: int
    parent: int | None
    action: str | None


def solve(start: State, goal: State = GOAL, algorithm: str = "astar",
          heuristic: str = "manhattan", model: str = "unit", order: str = "UDLR",
          trace_limit: int = 0, step: bool = False, max_expanded: int = 200000) -> dict:
    """Trả dict kết quả. BFS trên directional vẫn tối ưu số BƯỚC, không tối ưu giá.
    trace_limit chỉ giới hạn SỐ DÒNG LOG, không dừng tìm kiếm.
    max_expanded là giới hạn tài nguyên: status='limit' KHÁC 'unsolvable'.
    """
    start, goal = validate_state(start), validate_state(goal)
    validate_order(order)
    if algorithm not in ("bfs", "ucs", "astar"):
        raise ValueError("algorithm phai la bfs, ucs hoac astar")
    if model not in ("unit", "directional"):
        raise ValueError("model phai la unit hoac directional")
    if type(trace_limit) is not int or trace_limit < 0:
        raise ValueError("trace_limit phai la so nguyen khong am")
    if type(max_expanded) is not int or max_expanded < 0:
        raise ValueError("max_expanded phai la so nguyen khong am")
    h = make_heuristic(goal, heuristic if algorithm == "astar" else "zero", model)
    out = dict(algorithm=algorithm, heuristic=heuristic if algorithm == "astar" else "zero",
               model=model, order=order, start=start, goal=goal,
               status="unsolvable", steps=None, cost=None, path=[], actions=[],
               expanded=0, generated=0, pushed=0, popped=0, stale_pops=0,
               reopened=0, max_frontier=0, trace=[], elapsed_ms=0.0)
    # Kiểm parity là tiền xử lý, không tính như mở rộng một nút tìm kiếm.
    if not is_solvable(start, goal):
        return out
    t0 = perf_counter()
    nodes = [Node(start, 0, 0, None, None)]
    best_g = {start: 0}
    expanded_g: dict[State, int] = {}
    serial = count()
    queue = deque([0])
    heap: list[tuple[int, int, int]] = []
    if algorithm != "bfs":
        heappush(heap, (h(start), next(serial), 0))
    out["pushed"] = out["max_frontier"] = 1
    valid_index = 0

    def finish(status: str, node_id: int | None = None) -> dict:
        out["status"] = status
        if node_id is not None:
            end = nodes[node_id]
            path, actions = [], []
            current = node_id
            while current is not None:
                node = nodes[current]
                path.append(node.state)
                if node.action is not None:
                    actions.append(node.action)
                current = node.parent
            out.update(path=list(reversed(path)), actions=list(reversed(actions)),
                       steps=end.depth, cost=end.g)
        out["elapsed_ms"] = (perf_counter() - t0) * 1000
        return out

    def label(idx: int) -> str:
        actions = []
        while nodes[idx].parent is not None:
            actions.append(nodes[idx].action)
            idx = nodes[idx].parent
        return "S" + "".join("/" + a for a in reversed(actions))

    while queue if algorithm == "bfs" else heap:
        frontier_before = len(queue) if algorithm == "bfs" else len(heap)
        if algorithm == "bfs":
            node_id = queue.popleft()
        else:
            _, _, node_id = heappop(heap)
        out["popped"] += 1
        node = nodes[node_id]
        # Bản ghi cũ vẫn ở heap. Chỉ bỏ khi pop, không coi là expanded.
        if algorithm != "bfs" and (node.g != best_g[node.state] or
              (node.state in expanded_g and node.g >= expanded_g[node.state])):
            out["stale_pops"] += 1
            continue
        valid_index += 1
        row = dict(index=valid_index, state=node.state, g=node.g, h=h(node.state),
                   f=node.g + h(node.state), frontier_before=frontier_before,
                   event="POP", updates=[])
        if valid_index <= trace_limit:
            row["label"] = label(node_id)
        if node.state == goal:
            row["event"] = "GOAL"
            row["frontier_after"] = frontier_before - 1
            if valid_index <= trace_limit:
                out["trace"].append(row)
            if step:
                print("GOAL\n" + show(node.state))
            return finish("solved", node_id)
        if out["expanded"] >= max_expanded:
            return finish("limit")
        if node.state in expanded_g:
            out["reopened"] += 1
        expanded_g[node.state] = node.g
        out["expanded"] += 1
        # Khi step=True, dừng TRƯỚC khi sinh con tại mỗi lần mở rộng hợp lệ.
        if step:
            print(f"\nBuoc {valid_index}: g={node.g}, h={h(node.state)}, f={node.g+h(node.state)}")
            print(show(node.state))
            input("Du doan con tiep theo; Enter de mo rong (Ctrl+C dung): ")
        for action, new_state, edge_cost in neighbors(node.state, model, order):
            out["generated"] += 1
            new_g = node.g + edge_cost
            if algorithm == "bfs":
                improve = new_state not in best_g  # phát hiện ngay khi enqueue
            else:
                improve = new_g < best_g.get(new_state, float("inf"))
            if not improve:
                continue
            best_g[new_state] = new_g
            new_id = len(nodes)
            nodes.append(Node(new_state, new_g, node.depth+1, node_id, action))
            if algorithm == "bfs":
                queue.append(new_id)
            else:
                heappush(heap, (new_g + h(new_state), next(serial), new_id))
            out["pushed"] += 1
            if valid_index <= trace_limit:
                row["updates"].append(dict(action=action, state=new_state,
                                           g=new_g, h=h(new_state), f=new_g+h(new_state)))
        frontier_after = len(queue) if algorithm == "bfs" else len(heap)
        row["frontier_after"] = frontier_after
        out["max_frontier"] = max(out["max_frontier"], frontier_after)
        if valid_index <= trace_limit:
            # Thứ tự thực sự lấy tiếp (không phải thứ tự mảng heap nội bộ).
            ids = list(queue) if algorithm == "bfs" else [i for _, _, i in sorted(heap)]
            row["frontier"] = [dict(label=label(i), state=nodes[i].state,
                                    g=nodes[i].g, h=h(nodes[i].state),
                                    f=nodes[i].g+h(nodes[i].state)) for i in ids]
            # row và list updates tạo mới ở mỗi vòng; không tái dùng cùng dict.
            out["trace"].append(row)
    return finish("exhausted")
