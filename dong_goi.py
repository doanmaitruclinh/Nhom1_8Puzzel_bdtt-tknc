"""Đóng gói bài nộp sau khi nhóm đã điền báo cáo và chạy kết quả.
Chỉ kiểm cấu trúc/số dòng; KHÔNG xác nhận nội dung báo cáo hay code là đúng.
"""
import argparse, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--group',default='Nhom01')
    args=parser.parse_args()
    if not args.group or not all(c.isalnum() or c in '_-' for c in args.group):
        parser.error('Ten nhom chi dung chu, so, _ hoac -')
    required=['BaoCao.pdf','TinhTay.pdf','test_nhom.py','du_lieu_nhom.json',
              'README_NHOM.md','DongGop.csv','output/bat_buoc.json','output/bat_buoc.csv',
              'output/tu_tao.json','output/tu_tao.csv','output/ket_qua_test.txt']
    absent=[name for name in required if not (ROOT/name).is_file()]
    slides=[ROOT/name for name in ('ThuyetTrinh.pptx','ThuyetTrinh.pdf') if (ROOT/name).is_file()]
    if not slides:absent.append('ThuyetTrinh.pptx hoac ThuyetTrinh.pdf')
    if absent:raise SystemExit('Chua du bai nop:\n- '+'\n- '.join(absent))
    for filename,count in [('bat_buoc.json',36),('tu_tao.json',18)]:
        rows=json.loads((ROOT/'output'/filename).read_text(encoding='utf-8'))['results']
        if len(rows)!=count:raise SystemExit(f'{filename}: can {count} dong, dang co {len(rows)}')
        if any(row.get('status')!='solved' for row in rows):
            raise SystemExit(f'{filename}: con lan chay chua solved; kiem tra du lieu/gioi han.')
    paths={ROOT/name for name in required}|set(slides)
    paths.update(ROOT.glob('*.py'))
    paths.update((ROOT/'output').glob('*'))
    # Không đưa mã/đáp án teacher hoặc PDF đề/hướng dẫn vào ZIP bài nộp.
    dest=ROOT/f'{args.group}_8Puzzle_GiuaKy.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(paths):
            if file.is_file():z.write(file,arcname=f'{args.group}_8Puzzle/'+str(file.relative_to(ROOT)))
    print('Da tao:',dest)
    print('Can giai nen sang thu muc khac va chay lai README truoc khi nop.')
