"""Tệp đơn giản nhất: chỉ sửa START, GOAL, MODEL, HEURISTIC rồi chạy.
Có đầy đủ thuật toán trong search.py; không cần tự điền chỗ trống.
"""
import json
from pathlib import Path
from puzzle import GOAL, show
from search import solve

START = (1, 2, 3, 4, 0, 6, 7, 5, 8)
MODEL = "unit"                  # "unit" hoặc "directional"
HEURISTIC = "manhattan"          # "misplaced", "manhattan", "weighted"

if __name__ == "__main__":
    result = solve(START, GOAL, algorithm="astar", heuristic=HEURISTIC,
                   model=MODEL, trace_limit=6)
    print("status:", result["status"], "steps:", result["steps"],
          "cost:", result["cost"], "expanded:", result["expanded"])
    for step, state in enumerate(result["path"]):
        print("\nTrang thai", step)
        print(show(state))
    folder = Path(__file__).resolve().parent / "output"
    folder.mkdir(exist_ok=True)
    (folder / "demo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Da luu:", folder / "demo.json")
