"""Không cài thư viện; chỉ kiểm Python và các tệp đi kèm."""
import sys
from pathlib import Path
if __name__=="__main__":
    print("Python:",sys.version,"\nThu muc:",Path(__file__).resolve().parent)
    if sys.version_info<(3,10):raise SystemExit("Can Python 3.10 tro len.")
    missing=[n for n in ("puzzle.py","search.py","run.py","data_cases.py","chay_mau.py")
             if not Path(__file__).with_name(n).is_file()]
    if missing:raise SystemExit("Thieu tep: "+", ".join(missing))
    from search import solve
    r=solve((1,2,3,4,5,6,7,0,8))
    assert r["cost"]==1
    print("OK: thu vien chuan du dung; khong can pip install.")
