"""Tạo 2 bàn mới từ goal bằng các bước hợp lệ; độ dài xáo trộn KHÔNG là tối ưu."""
import argparse,json,random
from pathlib import Path
from puzzle import GOAL, neighbors, validate_state


def scramble(goal,steps,seed):
    rng=random.Random(seed);state=goal;previous=None;history=[]
    for _ in range(steps):
        options=[(a,s) for a,s,c in neighbors(state) if s!=previous]
        action,new=rng.choice(options)
        previous,state=state,new;history.append(action)
    return state,history

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--seed",type=int,default=42)
    p.add_argument("--steps",type=int,default=16)
    p.add_argument("--goal",default=",".join(map(str,GOAL)))
    p.add_argument("--out",default="du_lieu_nhom.json")
    a=p.parse_args()
    if not 1<=a.steps<=24:p.error("Chon steps tu 1 den 24")
    g=validate_state([int(v) for v in a.goal.split(",")])
    cases={}; hist={}
    for i in (1,2):cases[f"N{i}"],hist[f"N{i}"]=scramble(g,a.steps,a.seed+i)
    obj={"goal":g,"cases":cases,"generation":{"seed":a.seed,"scramble_steps":a.steps,"history_from_goal":hist}}
    dest=Path(__file__).resolve().parent/a.out
    dest.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Da tao:",dest)
    print("Kiem tra hai ban khac nhau; so buoc toi uu phai do bang BFS, khong lay steps xao tron.")
