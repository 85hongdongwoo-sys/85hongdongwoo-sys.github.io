# 공공데이터 지도 도구 10종: 수집한 데이터로 '지역별 현황' 표와 '이렇게 쓰세요'를 페이지 HTML에 미리 넣는다
# (목록은 화면에서 그려져 구글이 못 읽으므로, 숫자 요약을 글로 넣어 페이지 내용을 채움)
# 사용: python3 build/pubdata/summary.py _site   (fetch.py 다음에 실행)
import json, os, re, sys, html
from datetime import datetime, timedelta, timezone

SITE = sys.argv[1] if len(sys.argv) > 1 else '_site'
PUB = os.path.join(SITE, 'data/pub')
SIDO = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
KST = datetime.now(timezone.utc) + timedelta(hours=9)
MARK = '<section class="card"><h2>자주 묻는 질문</h2>'
CSS = ('<style>.sum-w{overflow-x:auto;margin-top:10px;-webkit-overflow-scrolling:touch}'
       '.sum-t{width:100%;border-collapse:collapse;font-size:13.5px;min-width:300px}'
       '.sum-t th,.sum-t td{border-bottom:1px solid var(--line-s,#e5e8eb);padding:7px 6px;text-align:right;white-space:nowrap}'
       '.sum-t th{font-size:12.5px;color:var(--muted,#6b7684);font-weight:700;background:#F8F9FA}'
       '.sum-t th:first-child,.sum-t td:first-child{text-align:left}.sum-t tr.tot td{font-weight:800;background:#F4F7FB}'
       '.sum-p{font-size:15px;line-height:1.7;margin:8px 0 0;word-break:keep-all}.how{margin:8px 0 0;padding-left:1.3em;line-height:1.75;font-size:15px}'
       '.how li{margin:4px 0;word-break:keep-all}</style>\n')


def load_split(key):
    try:
        meta = json.load(open(os.path.join(PUB, key, 'meta.json'), encoding='utf-8'))
    except Exception:
        return None, {}
    cols, by = meta.get('cols') or [], {}
    for s in SIDO:
        try:
            rows = json.load(open(os.path.join(PUB, key, s + '.json'), encoding='utf-8'))
        except Exception:
            rows = []
        by[s] = [dict(zip(cols, r)) for r in rows]
    return meta, by


def load_one(name):
    try:
        j = json.load(open(os.path.join(PUB, name), encoding='utf-8'))
        return j, [dict(zip(j['cols'], r)) for r in j['rows']]
    except Exception:
        return None, []


def hm(x):
    x = re.sub(r'[^0-9]', '', str(x or ''))
    return int(x) if len(x) >= 3 else None


def num(x):
    try:
        v = float(str(x).replace(',', '').strip())
        return v
    except Exception:
        return None


def n(x):
    return f'{x:,}'


def pct(a, b):
    return f'{a / b * 100:.0f}%' if b else '-'


def table(head, rows, total=None):
    e = html.escape
    h = '<tr>' + ''.join(f'<th>{e(c)}</th>' for c in head) + '</tr>'
    b = ''.join('<tr>' + ''.join(f'<td>{e(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    if total:
        b += '<tr class="tot">' + ''.join(f'<td>{e(str(c))}</td>' for c in total) + '</tr>'
    return f'<div class="sum-w"><table class="sum-t">{h}{b}</table></div>'


def section(title, para, tbl, src):
    return (f'<section class="card pub-sum"><h2>{html.escape(title)}</h2><p class="sum-p">{para}</p>{tbl}'
            f'<p class="pub-src">{html.escape(src)}</p></section>\n')


def how(steps):
    return '<section class="card"><h2>이렇게 쓰세요</h2><ol class="how">' + ''.join(f'<li>{s}</li>' for s in steps) + '</ol></section>\n'


def upd(meta):
    return (meta or {}).get('updated') or KST.strftime('%Y-%m-%d %H:%M')


# ── 도구별 요약 ──
def s_pharmacy():
    meta, by = load_split('pharmacy')
    if not meta: return ''
    rows, T = [], [0, 0, 0, 0]
    for s in SIDO:
        L = by[s]; c = [len(L), 0, 0, 0]
        for o in L:
            h = o.get('hours') or []
            if len(h) >= 8:
                if hm(h[6][0]) is not None: c[1] += 1
                if hm(h[7][0]) is not None: c[2] += 1
                late = False
                for d in h[:7]:
                    a, b = hm(d[0]), hm(d[1])
                    if a is not None and b is not None and (b >= 2200 or b < a): late = True
                c[3] += late
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(4)]
    para = (f'전국 약국 <b>{n(T[0])}곳</b> 가운데 일요일에 여는 곳은 <b>{n(T[1])}곳({pct(T[1], T[0])})</b>, '
            f'공휴일 영업시간을 따로 신고한 곳은 <b>{n(T[2])}곳({pct(T[2], T[0])})</b>이에요. '
            f'일주일 중 하루라도 밤 10시 넘어서까지 여는 약국은 <b>{n(T[3])}곳</b>이에요. 일요일·밤에 여는 약국은 많지 않으니 미리 위치를 알아 두면 좋아요.')
    return section('시도별 약국 영업 현황', para, table(['지역', '약국', '일요일', '공휴일', '밤 10시 이후'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 국립중앙의료원 전국 약국 정보. 영업시간은 약국이 신고한 시간이라 실제와 다를 수 있어요.') + how([
        '<b>‘내 위치’</b>를 누르거나 지역을 고르면 가까운 약국이 거리순으로 나와요.',
        '위쪽 버튼에서 <b>지금 영업 중·밤 10시 이후·일요일·공휴일</b>을 골라 걸러 보세요. 초록색 표시가 지금 열려 있는 곳이에요.',
        '목록에서 약국을 누르면 지도가 그 위치로 움직여요. <b>전화</b>로 영업 여부를 한 번 확인하고 <b>길찾기</b>로 가세요.',
        '<b>📷 가게 앞 보기</b>를 누르면 약국 주변 거리 사진(카카오 로드뷰)으로 입구를 미리 볼 수 있어요.'])


def s_er():
    meta, by = load_split('er')
    if not meta: return ''
    rows, T = [], [0, 0, 0]
    for s in SIDO:
        L = by[s]; info = [num(o.get('beds')) for o in L if num(o.get('beds')) is not None]
        c = [len(L), len(info), sum(1 for v in info if v > 0)]
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(3)]
    para = (f'전국 응급의료기관 <b>{n(T[0])}곳</b> 중 실시간 빈 병상 정보가 들어온 곳은 <b>{n(T[1])}곳</b>이고, '
            f'그중 응급실 일반 병상이 1개 이상 비어 있다고 알린 곳은 <b>{n(T[2])}곳</b>이에요. '
            '빈 병상 숫자는 병원이 입력한 값이라 몇 분 사이에도 바뀌어요. 위급하면 먼저 <b>119</b>에 전화하세요.')
    return section('시도별 응급실 현황', para, table(['지역', '응급실', '병상 정보', '빈 병상 있음'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 국립중앙의료원 응급의료정보. 매시간 갱신하며, 진단이나 치료를 대신하지 않아요.') + how([
        '<b>‘내 위치’</b>를 누르면 가까운 응급실이 거리순으로 나와요.',
        '각 병원의 <b>빈 병상 수</b>와 입력 시각을 확인하세요. 오래된 시각이면 실제와 다를 수 있어요.',
        '출발 전에 병원에 <b>전화</b>해서 지금 받을 수 있는지 물어보세요.',
        '숨쉬기 어렵거나 의식이 없는 등 위급한 상황이면 직접 가지 말고 <b>119</b>를 부르세요.'])


def s_ev():
    meta, by = load_split('ev')
    if not meta: return ''
    rows, T = [], [0, 0, 0, 0]
    for s in SIDO:
        L = by[s]
        c = [len(L), sum(int(o.get('total') or 0) for o in L), sum(int(o.get('fast') or 0) for o in L), sum(1 for o in L if str(o.get('parkFree')).upper() == 'Y')]
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(4)]
    para = (f'전국 전기차 충전소 <b>{n(T[0])}곳</b>에 충전기 <b>{n(T[1])}대</b>가 있고, 그중 급속 충전기는 <b>{n(T[2])}대({pct(T[2], T[1])})</b>예요. '
            f'충전하는 동안 주차가 무료인 충전소는 <b>{n(T[3])}곳</b>이에요. 급속 충전기는 빨리 차니 장거리 이동 때 먼저 찾아 두세요.')
    return section('시도별 전기차 충전소 현황', para, table(['지역', '충전소', '충전기', '급속', '주차 무료'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 한국환경공단 전기자동차 충전소 정보. 충전기 상태는 몇 시간마다 갱신돼요.') + how([
        '<b>‘내 위치’</b>를 누르면 가까운 충전소가 거리순으로 나와요.',
        '<b>지금 빈 충전기·급속 빈 충전기·주차 무료</b> 버튼으로 걸러 보세요.',
        '충전소마다 운영 기관과 이용 가능 시간이 달라요. 아파트·회사처럼 <b>이용 제한</b>이 있는 곳은 표시를 확인하세요.',
        '도착 직전에 다른 차가 쓸 수 있으니, 근처 충전소를 한두 곳 더 봐 두면 좋아요.'])


def s_parking():
    meta, by = load_split('parking')
    if not meta: return ''
    rows, T = [], [0, 0, 0, 0]
    for s in SIDO:
        L = by[s]
        sp = 0
        for o in L:
            v = num(o.get('spaces'))
            if v: sp += int(v)
        c = [len(L), sum(1 for o in L if '무료' in str(o.get('fee'))), sum(1 for o in L if '공영' in str(o.get('kind'))), sp]
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(4)]
    para = (f'전국 공영·민영 주차장 <b>{n(T[0])}곳</b>(주차면 약 <b>{n(T[3])}면</b>)의 정보를 모았어요. '
            f'요금이 무료로 등록된 곳은 <b>{n(T[1])}곳({pct(T[1], T[0])})</b>, 공영 주차장은 <b>{n(T[2])}곳</b>이에요. '
            '공영 주차장은 대체로 민영보다 요금이 싸요.')
    return section('시도별 주차장 현황', para, table(['지역', '주차장', '무료', '공영', '주차면'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 전국주차장정보표준데이터. 요금·운영시간은 바뀌었을 수 있으니 현장 안내를 확인하세요.') + how([
        '<b>‘내 위치’</b>를 누르거나 지역을 고르면 가까운 주차장이 나와요.',
        '<b>무료·공영</b> 버튼으로 걸러 보고, 기본 요금과 추가 요금을 비교하세요.',
        '오래 세울 때는 <b>1일 주차권</b> 금액이 있는지 확인하세요. 시간 요금보다 쌀 때가 많아요.',
        '주말·공휴일 운영시간이 평일과 다른 곳이 있으니 요일별 시간을 꼭 보세요.'])


def s_toilet():
    meta, by = load_split('toilet')
    if not meta: return ''
    rows, T = [], [0, 0, 0, 0]
    for s in SIDO:
        L = by[s]
        c = [len(L), sum(1 for o in L if re.search(r'24|상시', str(o.get('open')))), sum(1 for o in L if str(o.get('handicap')) == '1'),
             sum(1 for o in L if str(o.get('diaper')).upper() == 'Y')]
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(4)]
    para = (f'전국 공중화장실 <b>{n(T[0])}곳</b> 가운데 24시간·상시 개방으로 등록된 곳은 <b>{n(T[1])}곳({pct(T[1], T[0])})</b>이에요. '
            f'장애인 화장실이 있는 곳은 <b>{n(T[2])}곳</b>, 기저귀 교환대가 있는 곳은 <b>{n(T[3])}곳</b>이에요.')
    return section('시도별 공중화장실 현황', para, table(['지역', '화장실', '24시간', '장애인', '기저귀대'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 공중화장실정보표준데이터. 개방시간은 관리 기관이 등록한 값이에요.') + how([
        '<b>‘내 위치’</b>를 누르면 가장 가까운 화장실부터 나와요.',
        '<b>24시간·장애인 화장실·기저귀 교환대</b> 버튼으로 필요한 곳만 걸러 보세요.',
        '공원·역·관공서 화장실은 개방시간이 정해져 있어요. 밤에는 24시간 표시가 있는 곳을 고르세요.',
        '<b>길찾기</b>를 누르면 카카오맵으로 바로 안내돼요.'])


def s_air():
    j, L = load_one('air.json')
    if not j: return ''
    rows, all10, all25 = [], [], []
    for s in SIDO:
        R = [o for o in L if str(o.get('sido', '')).startswith(s)]
        a = [num(o.get('pm10')) for o in R]; a = [v for v in a if v is not None]
        b = [num(o.get('pm25')) for o in R]; b = [v for v in b if v is not None]
        all10 += a; all25 += b
        rows.append([s, n(len(R)), f'{sum(a) / len(a):.0f}' if a else '-', f'{sum(b) / len(b):.0f}' if b else '-'])
    m10 = sum(all10) / len(all10) if all10 else None
    m25 = sum(all25) / len(all25) if all25 else None
    para = (f'전국 측정소 <b>{n(len(L))}곳</b>의 최근 값을 모았어요. ' +
            (f'전국 평균은 미세먼지(PM10) <b>{m10:.0f}㎍/㎥</b>, 초미세먼지(PM2.5) <b>{m25:.0f}㎍/㎥</b>예요. ' if m10 is not None and m25 is not None else '') +
            '환경부 기준으로 미세먼지는 30 이하, 초미세먼지는 15 이하가 ‘좋음’이에요.')
    return section('시도별 미세먼지 평균', para, table(['지역', '측정소', 'PM10 평균', 'PM2.5 평균'], rows),
                   f'기준: {j.get("updated") or upd(None)} · 자료: 한국환경공단 에어코리아. 매시간 갱신하며, 측정소 점검 중에는 값이 비어요.') + how([
        '<b>‘내 위치’</b>를 누르면 우리 동네 측정소 값이 바로 나와요. 지역을 직접 골라도 돼요.',
        '위쪽 큰 숫자 두 개가 그 지역 평균이고, 아래 목록이 측정소별 값이에요.',
        '‘나쁨’ 이상이면 마스크(KF80 이상)를 쓰고, 오래 하는 야외 운동은 줄이세요.',
        '값은 1시간마다 바뀌니 외출 직전에 다시 확인하세요.'])


def s_festival():
    meta, by = load_split('festival')
    if not meta: return ''
    td = KST.strftime('%Y%m%d')
    rows, T = [], [0, 0]
    for s in SIDO:
        L = by[s]
        c = [sum(1 for o in L if str(o.get('start')) <= td <= str(o.get('end'))), sum(1 for o in L if str(o.get('start')) > td)]
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(2)]
    para = (f'{KST.month}월 {KST.day}일 기준으로 전국에서 <b>지금 열리고 있는 축제·행사는 {n(T[0])}개</b>, '
            f'곧 시작하는 행사는 <b>{n(T[1])}개</b>예요. 날씨나 사정으로 일정이 바뀔 수 있으니 출발 전에 주최 측 안내를 확인하세요.')
    return section('시도별 축제·행사 수', para, table(['지역', '진행 중', '시작 예정'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 한국관광공사 국문 관광정보(행사·축제). 매일 갱신해요.') + how([
        '<b>진행 중·이번 주말·전체</b> 버튼으로 기간을 고르세요.',
        '<b>‘내 위치’</b>를 누르면 가까운 축제부터 보여줘요. 지역을 골라 여행지 근처 행사도 찾을 수 있어요.',
        '축제를 누르면 지도에서 위치를 보여주고, 기간과 연락처를 함께 확인할 수 있어요.',
        '주차가 어려운 축제가 많아요. 근처 공영 주차장이나 대중교통을 미리 알아 두세요.'])


def s_camping():
    meta, by = load_split('camping')
    if not meta: return ''
    rows, T = [], [0, 0, 0, 0]
    for s in SIDO:
        L = by[s]
        c = [len(L), sum(1 for o in L if '글램핑' in str(o.get('type'))), sum(1 for o in L if '카라반' in str(o.get('type'))),
             sum(1 for o in L if str(o.get('pet', '')).startswith('가능'))]
        rows.append([s] + [n(x) for x in c]); T = [T[i] + c[i] for i in range(4)]
    para = (f'전국 등록 캠핑장 <b>{n(T[0])}곳</b> 가운데 글램핑이 있는 곳은 <b>{n(T[1])}곳</b>, 카라반이 있는 곳은 <b>{n(T[2])}곳</b>이에요. '
            f'반려견 동반이 가능하다고 등록한 곳은 <b>{n(T[3])}곳({pct(T[3], T[0])})</b>이에요. 반려견은 크기 제한이 있는 곳이 많으니 예약 전에 확인하세요.')
    return section('시도별 캠핑장 현황', para, table(['지역', '캠핑장', '글램핑', '카라반', '반려견 동반'], rows, ['전국'] + [n(x) for x in T]),
                   f'기준: {upd(meta)} · 자료: 한국관광공사 고캠핑. 시설 정보는 캠핑장이 등록한 값이에요.') + how([
        '지역을 고르거나 <b>‘내 위치’</b>를 눌러 가까운 캠핑장을 찾으세요.',
        '<b>글램핑·카라반·자동차야영장·반려견 동반</b> 버튼으로 원하는 형태만 걸러 보세요.',
        '캠핑장을 누르면 소개, 부대시설, 예약 링크를 볼 수 있어요.',
        '주말·성수기는 예약이 빨리 차요. 예약 링크나 전화로 빈자리를 먼저 확인하세요.'])


def s_fuel():
    meta, by = load_split('fuel')
    if not meta: return ''
    avg = {}
    for nm, pc, pr in meta.get('avg') or []:
        avg.setdefault(str(nm), {})[pc] = num(pr)
    def av(s, pc):
        for k, v in avg.items():
            if k.startswith(s) and v.get(pc): return f'{v[pc]:,.0f}'
        return '-'
    rows, gaps = [], []
    for s in SIDO:
        L = [o for o in by[s] if num(o.get('gasoline'))]
        low = min(L, key=lambda o: num(o['gasoline'])) if L else None
        g = None
        for k, v in avg.items():
            if k.startswith(s) and v.get('B027') and low: g = v['B027'] - num(low['gasoline'])
        if g is not None: gaps.append((g, s))
        rows.append([s, av(s, 'B027'), av(s, 'D047'), f'{num(low["gasoline"]):,.0f}' if low else '-', f'{g:,.0f}' if g is not None else '-'])
    na = avg.get('전국', {})
    gm = max(gaps) if gaps else None
    para = ((f'전국 평균 휘발유 값은 <b>리터당 {na["B027"]:,.0f}원</b>, 경유는 <b>{na["D047"]:,.0f}원</b>이에요. ' if na.get('B027') and na.get('D047') else '') +
            (f'시도 평균과 그 시도 최저가의 차이가 가장 큰 곳은 <b>{gm[1]}(리터당 {gm[0]:,.0f}원)</b>이에요. 50리터를 넣으면 약 {gm[0] * 50:,.0f}원 차이예요.' if gm else ''))
    return section('시도별 평균 기름값과 최저가', para, table(['지역', '휘발유 평균', '경유 평균', '휘발유 최저', '평균과 차이'], rows),
                   f'기준: {upd(meta)} · 자료: 한국석유공사 오피넷. 단위: 원/리터. 최저가는 시도별 상위 주유소 기준이에요.') + how([
        '<b>‘내 위치’</b>를 누르거나 지역을 고르세요.',
        '<b>휘발유 싼 순·경유 싼 순</b> 버튼으로 가격순으로 보거나, <b>가까운 순</b>으로 바꿔 보세요.',
        '가격은 몇 시간마다 갱신돼요. 셀프 주유소인지, 카드 할인이 되는지도 함께 보세요.',
        '멀리 있는 싼 주유소보다 가는 길에 있는 곳이 이득일 때가 많아요. 거리도 같이 보세요.'])


def s_rest():
    j, L = load_one('rest.json')
    if not j: return ''
    by = {}
    for o in L:
        r = str(o.get('route') or '기타')
        c = by.setdefault(r, [0, 0, 0]); c[0] += 1; c[1] += bool(o.get('oil')); c[2] += bool(o.get('foods'))
    top = sorted(by.items(), key=lambda kv: -kv[1][0])[:15]
    rows = [[r] + [n(x) for x in c] for r, c in top]
    oil = sum(1 for o in L if o.get('oil')); food = sum(1 for o in L if o.get('foods'))
    para = (f'한국도로공사 고속도로 휴게소 <b>{n(len(L))}곳</b>의 위치를 모았어요. 기름값 정보가 있는 곳은 <b>{n(oil)}곳</b>, '
            f'대표 메뉴 정보가 있는 곳은 <b>{n(food)}곳</b>이에요. 아래는 휴게소가 많은 노선 순서예요.')
    return section('노선별 휴게소 수', para, table(['노선', '휴게소', '기름값 있음', '메뉴 있음'], rows),
                   f'기준: {j.get("updated") or upd(None)} · 자료: 한국도로공사 공공데이터. 메뉴·가격은 휴게소 사정으로 바뀔 수 있어요.') + how([
        '<b>‘내 위치’</b>를 누르면 가까운 휴게소부터 나와요. 이동 중이면 가는 방향의 휴게소를 고르세요.',
        '<b>주유소 있음·대표 메뉴 있음</b> 버튼으로 걸러 보세요.',
        '휴게소를 누르면 대표 메뉴와 휘발유·경유·LPG 값을 볼 수 있어요.',
        '같은 이름이라도 상행·하행 휴게소가 따로 있어요. 방향을 꼭 확인하세요.'])


MORE = {
 'medical/pharmacy-open.html': ('밤·휴일에 약이 필요할 때', [
  '<b>편의점 안전상비의약품:</b> 24시간 편의점에서는 해열진통제, 감기약, 소화제, 파스 같은 안전상비의약품을 살 수 있어요. 한 번에 살 수 있는 양이 정해져 있고, 어린이용은 나이·몸무게에 맞는지 포장 설명을 꼭 확인하세요.',
  '<b>공공심야약국:</b> 지자체가 지정한 공공심야약국은 밤늦게까지 문을 열어요. 지정 약국과 시간은 지역마다 다르니 시·군·구 누리집이나 약국에 전화로 확인하세요.',
  '<b>명절 연휴:</b> 설·추석 연휴에는 평소 영업시간과 다르게 여는 약국이 많아요. 연휴에는 지자체가 안내하는 문 여는 약국 목록을 함께 보세요.',
  '<b>처방전 약:</b> 처방전에는 사용 기간이 적혀 있고, 기간이 지나면 다시 받아야 해요. 늦은 시간에는 처방 약이 없을 수 있으니 전화로 먼저 물어보세요.']),
 'medical/emergency-room.html': ('응급실 이용 전에 알아 둘 것', [
  '<b>응급실 종류:</b> 응급의료기관은 권역응급의료센터, 지역응급의료센터, 지역응급의료기관으로 나뉘어요. 권역센터는 중증 환자를 주로 보고, 가벼운 증상은 지역응급의료기관이나 야간 진료 병원이 더 빠를 수 있어요.',
  '<b>비용:</b> 응급이 아닌 증상으로 큰 응급센터에 가면 응급의료관리료를 본인이 모두 내야 할 수 있어요. 가벼운 증상이면 야간·휴일 진료 병원을 먼저 찾아보세요.',
  '<b>미리 전화하기:</b> 빈 병상이 있어도 전문의가 없거나 진료가 어려운 경우가 있어요. 출발 전에 병원에 전화해 받을 수 있는지 확인하세요.',
  '<b>119:</b> 의식이 없거나 숨쉬기 어렵거나 가슴 통증, 심한 출혈처럼 위급하면 직접 가지 말고 119를 부르세요. 119 구급대가 받을 수 있는 병원을 찾아 줘요. 이 페이지는 진단이 아니에요.']),
 'drive/ev-charger.html': ('전기차 충전 팁', [
  '<b>급속과 완속:</b> 이 페이지는 환경공단 자료에서 급속 방식(DC차데모·DC콤보·AC3상 등)이거나 출력 50kW 이상인 충전기를 급속으로 세요. 급속은 짧은 시간에 많이 채우고, 완속은 몇 시간이 걸려 집·회사에서 오래 세울 때 알맞아요.',
  '<b>80%까지만:</b> 급속 충전은 배터리가 80% 정도 차면 속도가 크게 느려져요. 장거리 이동 중이면 80%쯤에서 출발하는 게 시간상 이득일 때가 많아요.',
  '<b>충전 구역 주차:</b> 충전이 끝난 뒤 충전 구역에 오래 세워 두면 과태료가 나올 수 있어요. 다른 차가 기다릴 수 있으니 충전이 끝나면 차를 옮겨 주세요.',
  '<b>요금:</b> 충전 요금은 운영 기관과 회원 카드에 따라 달라요. 자주 가는 충전소의 운영 기관을 확인해 두면 좋아요.']),
 'drive/parking.html': ('주차 요금 아끼는 법', [
  '<b>공영 주차장:</b> 지자체가 운영하는 공영 주차장은 민영보다 요금이 싼 경우가 많아요. 시장·관광지 주변에는 주말에 무료로 여는 공영 주차장도 있어요.',
  '<b>할인 대상:</b> 공영 주차장은 지자체 조례에 따라 경차, 저공해 차량, 장애인·국가유공자 차량, 다자녀 가구 등에 요금 할인을 해 주는 곳이 많아요. 할인 조건은 지역마다 달라요.',
  '<b>요금 계산:</b> ‘기본 30분 1,000원, 추가 10분 500원’처럼 기본 시간과 추가 단위를 함께 보세요. 오래 세울 때는 1일 주차권이 더 쌀 수 있어요.',
  '<b>불법 주차 주의:</b> 소화전 주변, 교차로 모퉁이, 버스 정류소, 횡단보도는 주민 신고로 바로 과태료가 나올 수 있어요.']),
 'life/toilet.html': ('공중화장실 이용 팁', [
  '<b>개방시간:</b> 공원·역·관공서 화장실은 개방시간이 정해져 있는 곳이 많아요. 밤에는 24시간·상시 개방 표시가 있는 곳을 고르세요.',
  '<b>개방화장실:</b> 지자체가 지정한 민간 건물의 ‘개방화장실’도 누구나 쓸 수 있어요. 건물 입구에 표지판이 붙어 있어요.',
  '<b>안전:</b> 비상벨이 설치된 화장실은 누르면 경찰이나 관리실로 연결돼요. 늦은 밤에는 사람이 많은 곳에 있는 화장실을 이용하세요.',
  '<b>아이와 함께:</b> 기저귀 교환대가 있는 곳은 목록에서 따로 걸러 볼 수 있어요. 대형 마트·백화점·고속도로 휴게소에도 유아 휴게실이 있는 곳이 많아요.']),
 'life/air-quality.html': ('미세먼지 등급 보는 법', [
  '<b>미세먼지(PM10) 등급:</b> 좋음 0~30, 보통 31~80, 나쁨 81~150, 매우 나쁨 151 이상(단위 ㎍/㎥)이에요.',
  '<b>초미세먼지(PM2.5) 등급:</b> 좋음 0~15, 보통 16~35, 나쁨 36~75, 매우 나쁨 76 이상이에요. 초미세먼지는 더 작아서 몸 깊이 들어가니 더 주의하세요.',
  '<b>나쁨일 때:</b> 외출할 때 KF80 이상 보건용 마스크를 쓰고, 오래 하는 야외 운동은 줄이세요. 어린이, 어르신, 호흡기 질환이 있는 분은 특히 조심하세요.',
  '<b>환기:</b> 미세먼지가 나쁜 날에도 요리 뒤에는 짧게 환기하는 게 좋아요. 공기청정기 필터는 사용 설명서의 교체 주기를 지키세요.']),
 'trip/festival.html': ('축제 갈 때 알아 둘 것', [
  '<b>일정 변경:</b> 비나 태풍, 지역 사정으로 축제가 미뤄지거나 취소되는 일이 있어요. 출발 전에 주최 측 누리집이나 전화로 확인하세요.',
  '<b>교통:</b> 인기 축제는 행사장 주변 도로가 막히고 주차장이 금방 차요. 셔틀버스나 대중교통 안내가 있는지 먼저 보세요.',
  '<b>무료와 유료:</b> 대부분의 지역 축제는 입장이 무료지만, 체험 프로그램이나 공연은 따로 예약·요금이 필요한 경우가 있어요.',
  '<b>아이와 함께:</b> 사람이 많은 행사장에서는 아이 옷에 보호자 연락처를 적어 두면 길을 잃었을 때 도움이 돼요.']),
 'trip/camping.html': ('캠핑장 고를 때 알아 둘 것', [
  '<b>등록 야영장:</b> 관광진흥법에 따라 등록된 야영장은 안전·위생 기준을 지켜야 해요. 이 지도의 캠핑장은 한국관광공사 고캠핑에 등록된 곳이에요.',
  '<b>형태 차이:</b> 일반 야영장은 텐트를 직접 치고, 자동차야영장은 차를 사이트 옆에 세울 수 있어요. 글램핑·카라반은 잠자리와 기본 시설이 갖춰져 있어 장비가 적어도 돼요.',
  '<b>안전:</b> 텐트 안에서 숯·가스 난방기구를 쓰면 일산화탄소 중독 위험이 있어요. 난방은 전기 제품을 쓰고 환기를 자주 하세요.',
  '<b>반려견:</b> 반려견 동반 가능이라도 크기·마릿수 제한이나 추가 요금이 있는 곳이 많아요. 예약 전에 확인하세요.']),
 'drive/gas-station.html': ('기름값 아끼는 법', [
  '<b>가격 공개:</b> 주유소 판매 가격은 한국석유공사 오피넷에 공개돼요. 이 페이지의 가격도 오피넷 자료이고, 몇 시간마다 갱신돼요.',
  '<b>셀프 주유소:</b> 셀프 주유소는 같은 지역 일반 주유소보다 싼 경우가 많아요. 목록에서 가격과 거리를 함께 비교해 보세요.',
  '<b>카드 할인:</b> 주유 할인 카드나 포인트 적립을 쓰면 표시된 가격보다 더 아낄 수 있어요. 할인은 카드사·정유사마다 조건이 달라요.',
  '<b>거리도 비용:</b> 리터당 몇십 원 싼 곳을 찾아 멀리 돌아가면 오히려 손해일 수 있어요. 가는 길에 있는 싼 곳을 고르세요.']),
 'drive/rest-area.html': ('휴게소 이용 팁', [
  '<b>상행·하행:</b> 같은 이름의 휴게소라도 방향마다 따로 있고 메뉴와 기름값이 다를 수 있어요. 지금 가는 방향의 휴게소인지 확인하세요.',
  '<b>졸음쉼터:</b> 휴게소 사이 거리가 먼 구간에는 졸음쉼터가 있어요. 졸리면 참지 말고 가까운 쉼터나 휴게소에서 쉬세요.',
  '<b>기름값:</b> 고속도로 주유소 가격도 이 페이지에서 비교할 수 있어요. 휴게소 주유소마다 가격 차이가 있어요.',
  '<b>대표 메뉴:</b> 도로공사가 공개한 휴게소별 대표 메뉴와 가격을 보여줘요. 메뉴는 계절이나 휴게소 사정으로 바뀔 수 있어요.']),
}


def more(path):
    t = MORE.get(path)
    if not t: return ''
    return f'<section class="card"><h2>{t[0]}</h2>' + ''.join(f'<p class="sum-p">{x}</p>' for x in t[1]) + '</section>\n'


PAGES = [('medical/pharmacy-open.html', s_pharmacy), ('medical/emergency-room.html', s_er), ('drive/ev-charger.html', s_ev),
         ('drive/parking.html', s_parking), ('life/toilet.html', s_toilet), ('life/air-quality.html', s_air), ('trip/festival.html', s_festival),
         ('trip/camping.html', s_camping), ('drive/gas-station.html', s_fuel), ('drive/rest-area.html', s_rest)]

if __name__ == '__main__':
    for path, fn in PAGES:
        p = os.path.join(SITE, path)
        if not os.path.exists(p):
            print('skip (no page)', path); continue
        try:
            block = fn()
        except Exception as e:
            print('FAILED', path, repr(e)[:200]); continue
        if not block:
            print('skip (no data)', path); continue
        h = open(p, encoding='utf-8').read()
        if 'class="card pub-sum"' in h or MARK not in h:
            print('skip (marker)', path); continue
        h = h.replace(MARK, CSS + block + more(path) + MARK, 1)
        open(p, 'w', encoding='utf-8').write(h)
        print('summary', path, len(re.sub(r'<[^>]+>|\s', '', block)))
