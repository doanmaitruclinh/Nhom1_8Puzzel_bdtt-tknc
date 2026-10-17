"""Chạy một bài hoặc ma trận. Đường dẫn --data tính từ Terminal nếu tương đối.
Tệp kết quả luôn nằm ở output/ cạnh run.py. Chỉ dùng thư viện chuẩn.
"""
from __future__ import annotations
import argparse, csv, json, platform, sys
from pathlib import Path
from statistics import median
from puzzle import GOAL, validate_state, check_path
from search import solve
from data_cases import CASES, CONFIGS, DEMO, HAND, UNSOLVABLE

ROOT = Path(__file__).resolve().parent
SCALARS = ["case", "model", "algorithm", "heuristic", "order", "status", "steps", "cost",
           "expanded", "generated", "pushed", "popped", "stale_pops", "reopened",
           "max_frontier", "elapsed_ms"]


def read_cases(path: str):
    source = Path(path)
    obj = json.loads(source.read_text(encoding="utf-8"))
    goal = validate_state(obj.get("goal", list(GOAL)))
    cases = obj.get("cases")
    if not isinstance(cases, dict) or not cases:
        raise ValueError("JSON phai co 'cases': {ten: [9 so]}")
    return {str(k): validate_state(v) for k,v in cases.items()}, goal


def save(results, tag, config):
    if not tag or any(not (c.isalnum() or c in "_-") for c in tag):
        raise ValueError("Tag chi dung chu, so, _ hoac -")
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    payload = dict(config=config, environment=dict(python=sys.version, platform=platform.platform()), results=results)
    (output/f"{tag}.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    with (output/f"{tag}.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=SCALARS,extrasaction="ignore")
        writer.writeheader(); writer.writerows(results)
    for item in results:
        if item["trace"]:
            file=output/f"{tag}_{item['case']}_{item['model']}_{item['heuristic']}_trace.csv"
            with file.open("w",encoding="utf-8-sig",newline="") as f:
                fields=["index","event","label","state","g","h","f","frontier_before","frontier_after","updates","frontier"]
                w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader()
                for row in item["trace"]:
                    w.writerow({k: json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,tuple)) else v for k,v in row.items()})
    print("Da luu:", output/f"{tag}.csv", "va JSON", flush=True)


def main():
    p=argparse.ArgumentParser(description="8-puzzle: thay du lieu, chay, kiem chung")
    p.add_argument("--case",default="DEMO")
    p.add_argument("--data",help="JSON gom goal va cases; thay the du lieu mac dinh")
    p.add_argument("--suite",action="store_true",help="9 cau hinh moi ban; mac dinh M1-M4 = 36 dong")
    p.add_argument("--algo",choices=["bfs","ucs","astar"],default="astar")
    p.add_argument("--heuristic",choices=["zero","misplaced","manhattan","weighted"],default="manhattan")
    p.add_argument("--model",choices=["unit","directional"],default="unit")
    p.add_argument("--order",default="UDLR")
    p.add_argument("--trace",type=int,default=0,help="Luu N lan pop hop le dau, khong dung thuat toan")
    p.add_argument("--step",action="store_true")
    p.add_argument("--repeat",type=int,default=1)
    p.add_argument("--limit",type=int,default=200000)
    p.add_argument("--tag",default="run")
    a=p.parse_args()
    if a.repeat<1 or (a.repeat>1 and (a.step or a.trace)):
        p.error("repeat >= 1; khi lap do thoi gian phai tat trace/step")
    if a.suite and (a.step or a.trace):
        p.error("suite khong dung trace/step; hay chay mot case rieng")
    if a.data:
        cases,goal=read_cases(a.data)
    else:
        cases,goal=(dict(CASES) if a.suite else {**CASES,"DEMO":DEMO,"HAND":HAND,"UNSOLVABLE":UNSOLVABLE}),GOAL
    if a.suite:
        jobs=[(name,state,m,alg,h) for name,state in cases.items() for m,alg,h in CONFIGS]
    else:
        if a.case not in cases:p.error(f"Khong co case {a.case}. Chon: {list(cases)}")
        jobs=[(a.case,cases[a.case],a.model,a.algo,a.heuristic)]
    results=[]
    for k,(name,state,m,alg,h) in enumerate(jobs,1):
        samples=[solve(state,goal,alg,h,m,a.order,a.trace,a.step,a.limit) for _ in range(a.repeat)]
        result=samples[-1]
        result.update(case=name,elapsed_ms=median(r["elapsed_ms"] for r in samples))
        if result["status"]=="solved":
            if check_path(state,goal,result["path"],result["actions"],m)!=result["cost"]:
                raise AssertionError("Chi phi duong khong khop cost")
        results.append(result)
        print(f"[{k}/{len(jobs)}] {name} {m} {alg}/{h}: {result['status']} "
              f"steps={result['steps']} cost={result['cost']} expanded={result['expanded']}",flush=True)
    save(results,a.tag,vars(a))

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:
        print("\nDa dung; chua co ket qua hoan chinh.",file=sys.stderr);sys.exit(130)
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print("LOI:",exc,file=sys.stderr);sys.exit(2)
