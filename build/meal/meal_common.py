# 급식 랭킹 페이지 공통: 시도 목록, 정적 렌더(HTML 조각)
import html
SIDO = [('seoul', '서울'), ('busan', '부산'), ('daegu', '대구'), ('incheon', '인천'), ('gwangju', '광주'), ('daejeon', '대전'), ('ulsan', '울산'),
        ('sejong', '세종'), ('gyeonggi', '경기'), ('gangwon', '강원'), ('chungbuk', '충북'), ('chungnam', '충남'), ('jeonbuk', '전북'),
        ('jeonnam', '전남'), ('gyeongbuk', '경북'), ('gyeongnam', '경남'), ('jeju', '제주')]
FULL = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시',
        '세종': '세종특별자치시', '경기': '경기도', '강원': '강원특별자치도', '충북': '충청북도', '충남': '충청남도', '전북': '전북특별자치도', '전남': '전라남도',
        '경북': '경상북도', '경남': '경상남도', '제주': '제주특별자치도'}
e = lambda s: html.escape(str(s), quote=True)
def n(x): return f'{x:,}'

def rank_html(rows, unit='곳', empty='이번 주 데이터를 모으는 중이에요.'):
    if not rows: return f'<p class="mr-empty">{empty}</p>'
    mx = max(r[1] for r in rows) or 1
    return '<ol class="mr-rank">' + ''.join(
        f'<li><span class="rk">{i+1}</span><span class="nm">{e(r[0])}</span><span class="ct">{n(r[1])}{unit}</span>'
        f'<i class="bar" style="width:{max(4, round(r[1]*100/mx))}%"></i></li>' for i, r in enumerate(rows)) + '</ol>'

def rising_html(rows):
    if not rows: return '<p class="mr-empty">지난주보다 크게 늘어난 메뉴가 아직 없어요.</p>'
    return '<ol class="mr-rank rise">' + ''.join(
        f'<li><span class="rk">{i+1}</span><span class="nm">{e(r[0])}</span><span class="ct">{n(r[1])}곳<small>지난주 {n(r[2])}곳</small></span></li>'
        for i, r in enumerate(rows)) + '</ol>'

def sido_grid(idx, cur=None):
    by = {s['slug']: s for s in idx.get('sido', [])}
    out = []
    for slug, name in SIDO:
        s = by.get(slug); t = (s['top'][0][0] if s and s.get('top') else '준비 중')
        cls = ' class="on"' if slug == cur else ''
        out.append(f'<li{cls}><a href="/study/meal/{slug}.html"><b>{name}</b><span>{e(t)}</span></a></li>')
    return '<ul class="mr-sido">' + ''.join(out) + '</ul>'
