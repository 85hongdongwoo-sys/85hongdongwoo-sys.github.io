"""노선 내비 안내 음성 문장 목록 → {파일이름: 문장}"""
DIST = {'100': '100미터', '150': '150미터', '200': '200미터', '250': '250미터', '300': '300미터', '400': '400미터', '500': '500미터',
        '600': '600미터', '700': '700미터', '800': '800미터', '1000': '1킬로미터'}
MAN = {'left': '좌회전', 'right': '우회전', 'uturn': '유턴', 'slight left': '왼쪽 방향', 'slight right': '오른쪽 방향',
       'straight': '직진', 'round': '회전교차로', 'sharp left': '왼쪽으로 크게 꺾기', 'sharp right': '오른쪽으로 크게 꺾기'}
def key(m): return m.replace(' ', '_')
P = {}
for d, dt in DIST.items():
    for m, mt in MAN.items():
        P[f'd{d}-{key(m)}'] = f'{dt} 앞에서 {mt}입니다.'
for m, mt in MAN.items():
    P[f'now-{key(m)}'] = f'{mt}하세요.' if m not in ('round', 'straight') else (f'{mt}입니다.')
for n in range(1, 61):
    P[f'soon-{n}'] = f'곧 {n}번 정류장입니다.'
    P[f'arr-{n}'] = f'{n}번 정류장에 도착했습니다.'
    P[f'next-{n}'] = f'다음은 {n}번 정류장입니다.'
    P[f'first-{n}'] = f'안내를 시작합니다. 첫 정류장은 {n}번입니다.'
P.update({'last': '마지막 정류장입니다. 수고하셨습니다.', 'reroute': '경로를 다시 탐색합니다.', 'start': '안내를 시작합니다.',
          'try': '안녕하세요. 홍라이프 노선 내비입니다. 300미터 앞에서 우회전입니다.'})
for sp in range(20, 130, 10):
    P[f'cam-{sp}'] = f'과속 단속 카메라가 있습니다. 제한속도 {sp}킬로미터입니다.'
    P[f'zs-{sp}'] = f'구간 단속이 시작됩니다. 제한속도 {sp}킬로미터입니다.'
for sp in (20, 30, 40, 50, 60):
    P[f'camc-{sp}'] = f'어린이보호구역입니다. 제한속도 {sp}킬로미터입니다.'
    P[f'camo-{sp}'] = f'노인보호구역입니다. 제한속도 {sp}킬로미터입니다.'
P['caml'] = '신호 단속 카메라가 있습니다.'
P['ze'] = '구간 단속이 끝났습니다.'
