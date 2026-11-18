"""전국무인교통단속카메라표준데이터(CSV) → 0.1도 칸별 JSON (/assets/cam/{위도칸}_{경도칸}.json)
한 줄: [위도, 경도, 제한속도, 종류, 보호구역]  종류: s=과속, g=신호+과속, l=신호, z=구간단속(시작), e=구간단속(끝)
보호구역: c=어린이, o=노인, ''=없음.  주정차 단속은 뺀다."""
import csv, json, os, sys, collections
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
T = collections.defaultdict(list); n = 0
for x in csv.DictReader(open(src, encoding='utf-8')):
    try: la, ln = float(x['위도']), float(x['경도'])
    except: continue
    if not (33 < la < 39 and 124 < ln < 132): continue
    k = x['단속구분'].replace('0', '') if x['단속구분'] not in ('01+02',) else '1+2'
    sp = int(x['제한속도'] or 0) if (x['제한속도'] or '0').isdigit() else 0
    if k == '4': continue
    pos = x['단속구간위치구분'].lstrip('0')
    if pos in ('1', '2'): t = 'z' if pos == '1' else 'e'
    elif k == '2': t = 's'
    elif k in ('1+2',): t = 'g'
    elif k == '1': t = 'g' if sp else 'l'
    elif k == '99' and sp: t = 's'
    elif k == '3': t = 'g' if sp else 'l'
    else: continue
    if t in ('s', 'g', 'z') and not sp: t = 'l' if t == 'g' else None
    if not t: continue
    z = {'2': 'c', '02': 'c', '1': 'o', '01': 'o'}.get(x['보호구역구분'], '')
    T[(int(la * 10), int(ln * 10))].append([round(la, 5), round(ln, 5), sp, t, z]); n += 1
for (a, b), v in T.items():
    json.dump(v, open(f'{out}/{a}_{b}.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print('cams', n, 'tiles', len(T), 'kb', sum(os.path.getsize(f'{out}/{f}') for f in os.listdir(out)) // 1024)
