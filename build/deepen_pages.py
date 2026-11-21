"""검색 노출이 있는 기존 페이지를 조금씩 깊게 (2026-11-22).
작성자·확인일·출처 줄, '이 페이지 목차', 정적 표, 직접 계산한 예시, 자주 묻는 질문(+FAQPage JSON-LD)을 넣는다.
새 페이지는 만들지 않는다. 표시가 이미 있거나 넣을 자리를 못 찾으면 그 페이지는 건너뛴다.
Usage: python3 build/deepen_pages.py _site"""
import json, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else '_site'
DAY = '2026-11-22'
CSS = ('<style id="hl-deep-css">.hl-by{margin:10px 2px 0;font-size:13px;line-height:1.6;color:var(--muted,#4E5968)}'
       '.hl-by a{color:inherit;text-decoration:underline;text-underline-offset:2px}'
       '.hl-ptoc{margin:10px 0 4px;padding:12px 14px;background:rgba(255,255,255,.82);border:1px solid var(--line,#E5E8EB);border-radius:14px}'
       '.hl-ptoc b{display:block;font-size:14px;margin:0 0 8px;color:var(--head,#191F28)}'
       '.hl-ptoc .xp-toc{margin:0}.hl-ptoc .xp-toc a{white-space:normal}'
       '.xp .tbl-wrap{max-width:100%;overflow-x:auto}.xp .hl-ex{margin:6px 0 14px}'
       '.xp .hl-ex li{margin:3px 0}.hl-cap{font-size:13.5px;color:var(--muted,#4E5968);margin:2px 0 10px}</style>')
VIEWS = '<script src="/assets/hl-views.js" defer data-target=".hl-chart" data-lang="ko"></script>'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def table(head, rows, cls='tbl xp-tbl', chart=False):
    h = '<div class="tbl-wrap tblwrap"><table class="%s"><thead><tr>%s</tr></thead><tbody>' % (
        cls, ''.join('<th scope="col">%s</th>' % x for x in head))
    for r in rows:
        h += '<tr><th scope="row">%s</th>%s</tr>' % (r[0], ''.join(
            '<td data-l="%s">%s</td>' % (head[i + 1], v) for i, v in enumerate(r[1:])))
    h += '</tbody></table></div>'
    return '<div class="hl-chart">%s</div>' % h if chart else h


def deepen(rel, byline_src, toc, section, faqs, views=False):
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        print('deepen: missing', rel); return 0
    s = open(p, encoding='utf-8').read()
    if 'id="hl-deep"' in s:
        print('deepen: already', rel); return 0
    need = ['</header>', '<section class="card guide">', '<section class="card faq">', '"@type":"FAQPage"']
    if not all(x in s for x in need) or s.count('<section class="card faq">') != 1:
        print('deepen: markers not found', rel); return 0
    # 1) 작성·확인일·출처 줄 + 이 페이지 목차 (머리 바로 아래)
    src = ' · '.join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (u, esc(n)) for n, u in byline_src)
    by = ('<p class="hl-by" id="hl-deep">작성 홍라이프 도구 · 확인일 <time datetime="%s">%s</time> · 출처 %s</p>' % (DAY, DAY, src))
    nav = ('<nav class="hl-ptoc" aria-label="이 페이지 목차"><b>이 페이지 목차</b><div class="xp-toc">%s</div></nav>'
           % ''.join('<a href="#%s">%s</a>' % (a, esc(t)) for a, t in toc))
    i = s.find('</header>', s.find('<main'))
    i += len('</header>')
    s = s[:i] + by + nav + s[i:]
    # 2) 본문 섹션: 설명(guide) 카드 바로 앞
    s = s.replace('<section class="card guide">', section + '<section class="card guide" id="guide">', 1)
    s = s.replace('<section class="card faq">', '<section class="card faq" id="faq">', 1)
    # 3) 자주 묻는 질문 추가 (화면 + JSON-LD)
    i = s.find('<section class="card faq"')
    j = s.find('</section>', i)
    s = s[:j] + ''.join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in faqs) + s[j:]
    m = re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema.org","@type":"FAQPage".*?)</script>', s, re.S)
    if m:
        try:
            d = json.loads(m.group(1))
            have = {x.get('name') for x in d.get('mainEntity', [])}
            for q, a in faqs:
                qt, at = re.sub('<[^>]+>', '', q), re.sub('<[^>]+>', '', a)
                if qt not in have:
                    d['mainEntity'].append({'@type': 'Question', 'name': qt, 'acceptedAnswer': {'@type': 'Answer', 'text': at}})
            s = s[:m.start(1)] + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
        except ValueError:
            print('deepen: FAQ JSON-LD parse failed', rel)
    # 4) 수정일
    s = re.sub(r'("@type": "WebPage", "url": "[^"]+", "dateModified": ")\d{4}-\d{2}-\d{2}', r"\g<1>" + DAY, s, count=1)
    extra = CSS + (VIEWS if views else '')
    s = s.replace('</head>', extra + '</head>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('deepen: ok', rel)
    return 1


# ───────────────────────── 학점 계산기 (/study/gpa.html) ─────────────────────────
# 검색어: 전공 평점 계산(법), 전공 학점 따로 계산, 학점 평균 계산기, gpa 환산, 학점 환산
def r2(x):  # 소수 셋째 자리에서 반올림
    return '%.2f' % (int(x * 100 + 0.5 + 1e-9) / 100)


def t2(x):  # 소수 둘째 자리 아래 버림
    return '%.2f' % (int(x * 100 + 1e-9) / 100)


CONV = [4.5, 4.3, 4.0, 3.8, 3.5, 3.3, 3.0, 2.5]
conv_rows = [[('%.1f' % g), t2(g * 4.3 / 4.5), t2(g * 4.0 / 4.5), '%.1f점' % (int(g / 4.5 * 1000 + 1e-9) / 10)] for g in CONV]
GPA_SEC = ('<section class="card xp" id="deep" aria-labelledby="dp-h"><h2 id="dp-h">전공 평점·누적 평점·환산, 예시로 계산해 보기</h2>'
 '<h3 id="dp-major">전공 평점만 따로 계산하는 법</h3>'
 '<p>전공 평점은 <b>전공 과목만 골라</b> ‘학점 × 등급 점수’를 더한 뒤 그 전공 과목들의 학점 합으로 나눈 값이에요. 교양·일반선택 과목은 분자와 분모 모두에서 빠져요. 위 계산기에서는 전공 칸에 체크한 줄만 모아 ‘전공 평점’ 칸에 따로 보여 줘요.</p>'
 + table(['과목', '학점', '성적(4.5 만점)', '학점 × 점수', '구분'], [
     ['전공 A', '3', 'A0 (4.0)', '12.0', '전공'], ['전공 B', '3', 'B+ (3.5)', '10.5', '전공'], ['전공 C', '2', 'A+ (4.5)', '9.0', '전공'],
     ['교양 D', '3', 'C+ (2.5)', '7.5', '교양'], ['교양 E', '2', 'A0 (4.0)', '8.0', '교양']]) +
 '<ul class="hl-ex"><li><b>전체 평점</b>: (12.0 + 10.5 + 9.0 + 7.5 + 8.0) ÷ 13학점 = 47 ÷ 13 = 3.615… → 버림 <b>3.61</b>, 셋째 자리 반올림 <b>3.62</b></li>'
 '<li><b>전공 평점</b>: (12.0 + 10.5 + 9.0) ÷ 8학점 = 31.5 ÷ 8 = 3.9375 → 버림 <b>3.93</b>, 반올림 <b>3.94</b></li></ul>'
 '<p>교양 C+ 한 과목이 전체 평점을 끌어내렸지만 전공 평점에는 영향이 없어요. 그래서 전공 평점을 따로 요구하는 장학·전과·대학원 서류에서는 두 값이 꽤 달라질 수 있어요.</p>'
 '<h3 id="dp-cum">여러 학기 학점 평균(누적 평점) 구하기</h3>'
 '<p>학기별 평점을 그냥 더해 학기 수로 나누면 안 돼요. 학기마다 들은 학점 수가 다르니 <b>학기 평점 × 그 학기 학점</b>을 더해 전체 학점으로 나눠야 해요.</p>'
 + table(['학기', '평점을 받은 학점', '학기 평점', '학점 × 평점'], [
     ['1학기', '18', '3.20', '57.6'], ['2학기', '12', '4.10', '49.2'], ['합계', '30', '—', '106.8']]) +
 '<ul class="hl-ex"><li><b>맞는 계산</b>: 106.8 ÷ 30 = <b>3.56</b></li><li><b>틀린 계산</b>: (3.20 + 4.10) ÷ 2 = 3.65 — 학점이 적은 2학기 성적이 실제보다 크게 반영돼요.</li></ul>'
 '<h3 id="dp-43">4.3 만점 학교 예시</h3>'
 '<p>4.3 만점은 A+ 4.3, A0 4.0, A- 3.7, B+ 3.3, B0 3.0, B- 2.7 …처럼 한 등급을 세 단계로 나눠요(서울대학교 성적 평가 기준). 3학점 A-, 3학점 B+, 2학점 A+, 1학점 P를 들었다면 (3×3.7 + 3×3.3 + 2×4.3) ÷ 8 = 29.6 ÷ 8 = <b>3.70</b>이고, P 1학점은 평점에서 빠지지만 이수 학점은 9학점이에요.</p>'
 '<h3 id="dp-goal">목표 평점까지 다음 학기에 얼마가 필요할까</h3>'
 '<p>지금까지 평점을 받은 학점이 60학점, 누적 평점이 3.40이고 다음 학기 18학점을 들어 누적 3.50을 만들고 싶다면, 필요한 학기 평점 x는 (60 × 3.40 + 18 × x) ÷ 78 = 3.50에서 나와요. 204 + 18x = 273이라 x = 3.833…, 곧 다음 학기에 <b>3.84 이상</b>을 받아야 해요(3.83이면 누적 3.499…로 3.50에 못 미쳐요).</p>'
 '<h3 id="dp-conv">GPA·학점 환산표 (비례 환산, 참고용)</h3>'
 '<p>아래 표는 평점을 만점 비율대로 옮긴 <b>단순 비례값</b>이에요(소수 둘째 자리 아래 버림). 학교·회사·해외 기관은 각자의 환산표나 과목별 등급 기준을 쓰는 경우가 많아서, 서류에 적을 때는 반드시 해당 기관 기준을 확인하세요.</p>'
 + table(['4.5 만점 평점', '4.3 만점 환산', '4.0 만점 환산', '100점 환산'], conv_rows) +
 '<p class="hl-cap">예: 3.8 ÷ 4.5 × 4.3 = 3.631… → 3.63, 3.8 ÷ 4.5 × 100 = 84.4점</p>'
 '<h3 id="dp-round">반올림과 버림, 학교마다 달라요</h3>'
 '<p>평점 평균을 소수 몇째 자리에서 어떻게 자르는지는 학칙에 따라 달라요. 예를 들어 명지대학교는 평점평균을 소수점 이하 셋째 자리에서 반올림한다고 안내해요. 위 계산기는 버림으로 보여 주니, 3.615처럼 경계에 걸리면 학교 방식으로 한 번 더 확인하세요.</p>'
 '</section>')
GPA_FAQ = [
 ('전공 평점은 어떻게 따로 계산하나요?', '전공 과목만 골라 (학점 × 등급 점수)의 합을 전공 과목 학점 합으로 나눠요. 교양 과목은 분자·분모 모두에서 빼요. 예: 전공 8학점의 점수 합이 31.5면 31.5 ÷ 8 = 3.9375예요.'),
 ('여러 학기 평균 학점은 학기 평점을 평균 내면 되나요?', '아니요. 학기 평점에 그 학기 학점을 곱해 더한 뒤 전체 학점으로 나눠야 해요. 18학점 3.20과 12학점 4.10이면 3.65가 아니라 106.8 ÷ 30 = 3.56이에요.'),
 ('4.5 만점 3.8은 4.3 만점으로 몇 점인가요?', '단순 비례로는 3.8 ÷ 4.5 × 4.3 = 3.63이에요. 다만 기관마다 환산표가 따로 있을 수 있어서 제출처 기준을 확인하세요.'),
 ('학점을 100점 만점으로 바꾸면 몇 점인가요?', '비례 환산은 평점 ÷ 만점 × 100이에요. 4.5 만점 3.5면 77.7점, 4.0이면 88.8점이에요(소수 둘째 자리 아래 버림). 학교별 백분율 환산표가 있으면 그 표가 우선이에요.'),
 ('목표 누적 평점을 맞추려면 다음 학기에 몇 점이 필요한가요?', '(지금 학점 × 지금 평점 + 다음 학기 학점 × x) ÷ 전체 학점 = 목표 평점을 x에 대해 풀면 돼요. 60학점 3.40에서 18학점을 더 들어 3.50을 만들려면 x는 약 3.84 이상이에요.'),
]

# ───────────────────────── 군 전역일 계산기 (/calendar/discharge.html) ─────────────────────────
import calendar as _cal, datetime as _dt, math as _m
_W = '월화수목금토일'


def _addm(d, n):
    y = d.year + (d.month - 1 + n) // 12; mo = (d.month - 1 + n) % 12 + 1
    return _dt.date(y, mo, min(d.day, _cal.monthrange(y, mo)[1]))


def _dis(s, n):
    e = _addm(s, n) - _dt.timedelta(1)
    return e, (e - s).days + 1


def _f(d):
    return '%d. %d. %d. (%s)' % (d.year, d.month, d.day, _W[d.weekday()])


mrows = []
for mo in range(1, 13):
    s = _dt.date(2026, mo, 1); r = ['2026. %d. 1.' % mo]
    for n in (18, 20, 21):
        e, tot = _dis(s, n); r.append('%s · %d일' % (_f(e), tot))
    mrows.append(r)
ex = []
for s, n, name in [(_dt.date(2026, 3, 9), 18, '육군'), (_dt.date(2026, 5, 18), 20, '해군'), (_dt.date(2026, 7, 14), 21, '공군'), (_dt.date(2026, 11, 2), 21, '사회복무요원')]:
    e, tot = _dis(s, n)
    half = s + _dt.timedelta(_m.ceil(tot / 2) - 1); d100 = s + _dt.timedelta(99); b100 = e - _dt.timedelta(100)
    ex.append((name, n, s, e, tot, half, d100, b100))
ex_html = ''.join('<li><b>%s %d개월, %s %s</b> → %s 예정일 <b>%s</b>, 전체 %d일. 100일째 %s, 반 꺾이는 날(복무율 50%%) %s, %s 100일 전 %s.</li>'
                  % (nm, n, _f(s), '소집' if nm == '사회복무요원' else '입대', '소집해제' if nm == '사회복무요원' else '전역', _f(e), tot, _f(d1), _f(h), '소집해제' if nm == '사회복무요원' else '전역', _f(b1)) for nm, n, s, e, tot, h, d1, b1 in ex)
DIS_SEC = ('<section class="card xp" id="deep" aria-labelledby="dp-h"><h2 id="dp-h">입대 날짜별 전역일, 표와 예시로 보기</h2>'
 '<h3 id="dp-month">2026년 입대 월별 전역 예정일 (매월 1일 입대 기준)</h3>'
 '<p>위 계산기와 같은 방식(입대일 + 복무 개월 − 1일)으로 계산한 값이에요. 칸 안의 일수는 입대일을 1일째로 센 전체 복무일이에요. 해병대·상근예비역은 육군과 같은 18개월, 사회복무요원은 공군과 같은 21개월 열을 보면 돼요.</p>'
 + table(['입대일', '육군·해병대 18개월', '해군 20개월', '공군·사회복무요원 21개월'], mrows) +
 '<p class="hl-cap">같은 18개월이라도 사이에 낀 달의 날수와 윤년(2028년 2월 29일) 때문에, 이 표(2026년 매월 1일 입대)에서 육군 전체 복무일은 546~549일로 조금씩 달라요.</p>'
 '<h3 id="dp-ex">직접 계산해 본 예시 4가지</h3><ul class="hl-ex">' + ex_html + '</ul>'
 '<p>복무율은 ‘오늘까지 복무한 날 ÷ 전체 복무일 × 100’이에요. 예를 들어 2026년 3월 9일 육군 입대자는 2026년 11월 22일이 259일째라 259 ÷ 549 × 100 = <b>47.17%</b>를 복무한 셈이에요.</p>'
 '<h3 id="dp-kind">복무 종류별 기간 (병무청 안내)</h3>'
 + table(['구분', '복무기간'], [
     ['육군·해병대 현역병', '18개월'], ['해군 현역병', '20개월'], ['공군 현역병', '21개월'], ['상근예비역', '18개월'],
     ['사회복무요원', '21개월'], ['대체복무요원', '36개월'], ['산업기능요원', '현역입영대상자 34개월, 사회복무요원소집대상자 23개월'], ['전문연구요원', '3년']]) +
 '<p>산업기능요원·전문연구요원처럼 목록에 없는 복무는 계산기에서 ‘직접 입력’을 고르고 개월 수(전문연구요원은 36)를 넣으면 같은 방식으로 날짜가 나와요.</p>'
 '</section>')
e0 = ex[0]
DIS_FAQ = [
 ('2026년에 입대하면 언제 전역하나요?', '입대일에 복무 개월을 더한 날의 전날이에요. 예를 들어 2026년 4월 1일 육군 입대면 2027년 9월 30일, 공군이면 2027년 12월 31일이에요. 위 월별 표에 매월 1일 입대 기준 날짜를 정리해 두었어요.'),
 ('육군 18개월은 며칠인가요?', '입대 날짜에 따라 달라요. 달마다 날수가 다르고 윤년(2월 29일)이 끼기도 해서예요. 2026년 매월 1일 입대 기준으로는 546~549일이고, 2026년 3월 9일 입대라면 %d일이에요.' % e0[4]),
 ('공군·해군은 복무기간이 몇 개월인가요?', '병무청 안내 기준으로 해군 20개월, 공군 21개월이에요. 육군·해병대는 18개월, 사회복무요원은 21개월이에요.'),
 ('군 복무 퍼센트(복무율)는 어떻게 계산하나요?', '오늘까지 복무한 날(입대일 포함) ÷ 전체 복무일 × 100이에요. 549일 중 259일째면 47.17%예요.'),
 ('산업기능요원이나 전문연구요원도 계산할 수 있나요?', '네. 복무 종류에서 ‘직접 입력’을 고르고 개월 수를 넣으면 돼요. 병무청 안내로 산업기능요원은 현역입영대상자 34개월·사회복무요원소집대상자 23개월, 전문연구요원은 3년이에요.'),
]

# ───────────────────────── 지연이자 계산기 (/legal/late-interest.html) ─────────────────────────
def _li(p, r, s, e):
    n = (e - s).days + 1
    return n, int(p * r * n / 365)


def won(x):
    return '{:,}원'.format(x)


D = _dt.date
a1 = _li(5_000_000, .05, D(2026, 1, 1), D(2026, 12, 31))
a2 = _li(20_000_000, .06, D(2026, 4, 1), D(2026, 6, 29))
b1 = _li(30_000_000, .05, D(2026, 3, 1), D(2026, 6, 15)); b2 = _li(30_000_000, .12, D(2026, 6, 16), D(2026, 11, 30))
c1 = _li(10_000_000, .05, D(2026, 1, 1), D(2026, 4, 10)); cp = 10_000_000 - (4_000_000 - c1[1]); c2 = _li(cp, .05, D(2026, 4, 11), D(2026, 9, 30))
drows = []
for p, nm in [(1_000_000, '100만 원'), (5_000_000, '500만 원'), (10_000_000, '1,000만 원'), (30_000_000, '3,000만 원'), (50_000_000, '5,000만 원'), (100_000_000, '1억 원')]:
    drows.append([nm, won(int(p * .05 / 365)), won(int(p * .05 * 30 / 365)), won(int(p * .05)), won(int(p * .06)), won(int(p * .12))])
LI_SEC = ('<section class="card xp" id="deep" aria-labelledby="dp-h"><h2 id="dp-h">지연이자, 금액별 표와 계산 예시</h2>'
 '<h3 id="dp-table">원금별 지연이자 한눈에 보기</h3>'
 '<p>‘원금 × 연 이율 × 일수 ÷ 365’로 계산하고 원 미만은 버렸어요. 하루치와 30일치는 연 5%(민사) 기준이고, 1년치는 이율별로 나눴어요.</p>'
 + table(['원금', '연 5% 하루', '연 5% 30일', '연 5% 1년', '연 6% 1년', '연 12% 1년'], drows) +
 '<p>같은 1,000만 원이라도 어떤 이율이 붙느냐에 따라 1년 이자가 두 배 넘게 차이 나요. 표와 막대그래프 중 편한 쪽으로 바꿔 보세요.</p>'
 + table(['1,000만 원을 1년 늦게 받을 때', '1년 지연이자'], [['민사 법정이율 연 5%', won(500000)], ['상사 법정이율 연 6%', won(600000)], ['소송촉진법 법정이율 연 12%', won(1200000)]], chart=True) +
 '<h3 id="dp-ex">직접 계산해 본 예시</h3><ul class="hl-ex">'
 '<li><b>개인 간 빌려준 돈 500만 원, 연 5%%, 1년</b> — 2026. 1. 1.~2026. 12. 31. %d일: 5,000,000 × 5%% × %d ÷ 365 = <b>%s</b></li>'
 '<li><b>물품 대금 2,000만 원, 상사 연 6%%, 90일</b> — 2026. 4. 1.~2026. 6. 29. %d일: 20,000,000 × 6%% × %d ÷ 365 = 295,890.4… → <b>%s</b></li>'
 '<li><b>돌려받지 못한 보증금 3,000만 원, 지급명령 송달일 2026. 6. 15.</b> — 2026. 3. 1.~6. 15. %d일 연 5%% = %s, 6. 16.~11. 30. %d일 연 12%% = %s, 합계 <b>%s</b></li>'
 '<li><b>중간에 일부를 갚은 경우</b> — 1,000만 원(연 5%%, 2026. 1. 1.부터)에서 4. 10.에 400만 원을 갚았다면, 그날까지 %d일 이자 %s에 먼저 충당하고(민법 제479조: 비용·이자·원본 순서) 남은 %s이 원금을 줄여 원금은 %s이 돼요. 4. 11.~9. 30. %d일 이자는 %s이에요.</li></ul>'
 % (a1[0], a1[0], won(a1[1]), a2[0], a2[0], won(a2[1]), b1[0], won(b1[1]), b2[0], won(b2[1]), won(b1[1] + b2[1]),
    c1[0], won(c1[1]), won(4_000_000 - c1[1]), won(cp), c2[0], won(c2[1])) +
 '<p>마지막 예시처럼 일부 변제가 있으면 이 계산기에 갚은 날을 끝날로 한 번, 그다음 날을 시작일로 줄어든 원금을 넣어 한 번 더 계산하면 같은 결과가 나와요.</p>'
 '<h3 id="dp-which">내 경우는 몇 %일까</h3>'
 + table(['상황', '송달 전', '소장·지급명령 송달 다음 날부터'], [
     ['개인 사이에 빌려준 돈', '연 5% (민법 제379조)', '연 12%'], ['상인 간 거래·물품 대금', '연 6% (상법 제54조)', '연 12%'],
     ['지연이율을 따로 약정함', '약정 이율', '연 12% (약정이 더 높으면 사안별로 다름)'], ['내용증명만 보냄', '연 5% 또는 6%', '해당 없음 (재판 서류 송달이 아님)']]) +
 '<p class="hl-cap">연 12%는 「소송촉진 등에 관한 특례법 제3조제1항 본문의 법정이율에 관한 규정」(2019. 6. 1. 시행)의 이율이에요. 판결·결정문에 이율이 적혀 있으면 그 내용이 기준이에요.</p>'
 '</section>')
LI_FAQ = [
 ('지연이자는 어떻게 계산하나요?', '원금 × 연 이율 × 일수 ÷ 365예요. 이자가 시작된 날과 끝날을 모두 넣어 일수를 세고, 이율이 바뀌는 날(송달 다음 날 등)마다 구간을 나눠 더해요.'),
 ('1,000만 원을 1년 늦게 받으면 지연이자는 얼마인가요?', '민사 연 5%%면 %s, 상사 연 6%%면 %s, 소송촉진법 연 12%% 구간이면 %s이에요.' % (won(500000), won(600000), won(1200000))),
 ('하루 지연이자는 얼마인가요?', '원금 × 연 이율 ÷ 365예요. 1,000만 원에 연 5%%면 하루 %s(원 미만 버림), 연 12%%면 하루 %s이에요.' % (won(int(10_000_000 * .05 / 365)), won(int(10_000_000 * .12 / 365)))),
 ('보증금을 늦게 돌려받으면 지연이자를 받을 수 있나요?', '돌려받기로 한 날 다음 날부터 보통 민사 법정이율 연 5%로 계산하고, 소장이나 지급명령이 송달된 다음 날부터는 연 12%를 구할 수 있어요. 실제 적용은 사건마다 다르니 상담을 받으세요.'),
 ('돈을 일부만 갚았으면 이자는 어떻게 되나요?', '민법 제479조에 따라 갚은 돈은 비용, 이자, 원본 순서로 충당돼요. 갚은 날까지의 이자를 먼저 빼고 남은 금액만큼 원금이 줄어든 뒤 다시 계산해요.'),
]

n = 0
n += deepen('study/gpa.html',
            [('서울대학교 성적 평가', 'https://www.snu.ac.kr/academics/resources/certificate/grading'),
             ('명지대학교 평점과 평점평균 계산법', 'https://www.mju.ac.kr/mjukr/12045/subview.do')],
            [('tool', '학점 계산기'), ('explain', '평점이 계산되는 과정'), ('dp-major', '전공 평점 따로 계산'), ('dp-cum', '여러 학기 누적 평점'),
             ('dp-43', '4.3 만점 예시'), ('dp-goal', '목표 평점 역산'), ('dp-conv', 'GPA·학점 환산표'), ('guide', '4.5·4.3 등급표'), ('faq', '자주 묻는 질문')],
            GPA_SEC, GPA_FAQ)
n += deepen('calendar/discharge.html',
            [('병무청 병역이행안내 개요', 'https://www.mma.go.kr/contents.do?mc=usr0000041')],
            [('tool', '전역일 계산기'), ('explain', '계산 원리'), ('dp-month', '2026년 입대 월별 전역일'), ('dp-ex', '계산 예시 4가지'),
             ('dp-kind', '복무 종류별 기간'), ('guide', '전역일 계산법 정리'), ('faq', '자주 묻는 질문')],
            DIS_SEC, DIS_FAQ)
n += deepen('legal/late-interest.html',
            [('국가법령정보센터 소송촉진법 법정이율 규정', 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%86%8C%EC%86%A1%EC%B4%89%EC%A7%84%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%ED%8A%B9%EB%A1%80%EB%B2%95%EC%A0%9C3%EC%A1%B0%EC%A0%9C1%ED%95%AD%EB%B3%B8%EB%AC%B8%EC%9D%98%EB%B2%95%EC%A0%95%EC%9D%B4%EC%9C%A8%EC%97%90%EA%B4%80%ED%95%9C%EA%B7%9C%EC%A0%95'),
             ('국가법령정보센터 민법', 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EB%AF%BC%EB%B2%95'),
             ('국가법령정보센터 상법', 'https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%83%81%EB%B2%95')],
            [('tool', '지연이자 계산기'), ('explain', '구간을 나누는 이유'), ('dp-table', '원금별 지연이자 표'), ('dp-ex', '계산 예시'),
             ('dp-which', '내 경우 이율'), ('guide', '이율 정리'), ('faq', '자주 묻는 질문')],
            LI_SEC, LI_FAQ, views=True)
print('deepened pages:', n)
