"""TESTS에 160문항 풀을 합치고 리드·라벨을 맞춘다 (gen_cats·make_cards 공용)"""
import re
from data_tests import TESTS
from data_tests_extra import EXTRA
from pools import build
LEADFIX = {
 'spending': '간편 40문항 또는 정밀 160문항으로 돈을 쓰는 습관을 충동·보상·계획·가치 네 가지 기준으로 살펴보고, 나와 가장 가까운 소비 유형과 바로 써먹을 관리 팁을 알려 줘요.',
 'brain': '간편 40문항 또는 정밀 160문항으로 논리·순서를 중시하는 “좌뇌형”인지, 직관·이미지를 중시하는 “우뇌형”인지 가볍게 알아봐요.',
 'career': '간편 40문항 또는 정밀 160문항으로 내가 끌리는 일의 종류를 현장형·탐구형·예술형·사회형·진취형·관습형 여섯 가지 흥미 유형으로 나눠 보고, 어울리는 직업 예시를 보여 줘요.',
}
for t in TESTS:
    if getattr(t, '_prepped', False) or t.get('_prepped'): continue
    t['q'] = build(t, EXTRA.get(t['slug'], []))
    if t['kind'] == 'phq9':
        t['qlabel'] = f"{len(t['q'])}문항"
    else:
        t['quick'] = 40
        t['qlabel'] = '40·160문항'
        t['lead'] = LEADFIX.get(t['slug']) or re.sub(r'\d+문항으로', '간편 40문항 또는 정밀 160문항으로', t['lead'])
    t['_prepped'] = True
