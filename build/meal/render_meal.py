#!/usr/bin/env python3
"""배포 때 실행: _site/data/meal/*.json 으로 급식 랭킹 페이지의 <!--M:x-->…<!--/M:x--> 칸을 채움 (검색엔진도 보는 정적 내용)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meal_common import *
root = sys.argv[1] if len(sys.argv) > 1 else '_site'
D = os.path.join(root, 'data', 'meal')
try: idx = json.load(open(os.path.join(D, 'index.json'), encoding='utf-8'))
except Exception: print('급식 데이터 없음 — 기본 문구 유지'); sys.exit(0)

def fill(path, parts):
    if not os.path.exists(path): return
    s = open(path, encoding='utf-8').read()
    for k, v in parts.items():
        s = re.sub(r'<!--M:' + k + r'-->.*?<!--/M:' + k + r'-->', lambda m: f'<!--M:{k}-->{v}<!--/M:{k}-->', s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)

N = idx.get('national', {})
_c = idx.get('cur') or ['', '']
_lab = ((f'{int(_c[0][4:6])}/{int(_c[0][6:])}~' + (f'{int(_c[1][6:])}' if _c[0][4:6] == _c[1][4:6] else f'{int(_c[1][4:6])}/{int(_c[1][6:])}')) if _c[0] else '')
base = {'label': e(_lab), 'updated': e(idx.get('updated', ''))}
fill(os.path.join(root, 'study', 'meal-ranking.html'), dict(base, served=n(N.get('served', 0)), cal=n(N.get('avgCal', 0)),
     top=rank_html(N.get('top', [])[:20]), dessert=rank_html(N.get('dessert', [])[:10]), rising=rising_html(N.get('rising', [])[:10]), sido=sido_grid(idx)))
for slug, name in SIDO:
    try: d = json.load(open(os.path.join(D, slug + '.json'), encoding='utf-8'))
    except Exception: continue
    fill(os.path.join(root, 'study', 'meal', slug + '.html'), dict(base, served=n(d.get('served', 0)), cal=n(d.get('avgCal', 0)),
         top=rank_html(d.get('top', [])[:20]), dessert=rank_html(d.get('dessert', [])[:10]), rising=rising_html(d.get('rising', [])[:10]), sido=sido_grid(idx, slug)))
print('급식 랭킹 채움:', idx.get('label'), '학교', N.get('served'))
