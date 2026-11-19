# 2027학년도 수능 등급컷·예상 백분위 + 작년(2026) 비교 + 수험표 할인 → overlay/ipsi/suneung-2027.html
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = open(os.path.join(ROOT, 'overlay/ipsi/pyeonip-2027.html'), encoding='utf-8').read()
URL = 'https://honglife.co.kr/ipsi/suneung-2027.html'
TITLE = '2027 수능 등급컷·예상 백분위 + 작년 수능 비교 · 수험표 할인 총정리 | 홍라이프 도구'
DESC = ('2027학년도 수능(11월 19일) 예상 등급컷과 백분위를 작년 2026학년도 수능 실제 등급 구분 점수·누적 비율과 나란히 비교해요. '
        '표준점수·원점수로 내 등급과 추정 백분위를 바로 보고, 확인된 수능 수험표 할인 혜택을 공식 홈페이지·기사 링크와 함께 모았어요.')
UPDATED = '2026년 11월 19일 12시'

# 2026학년도 수능 채점 결과(평가원 2025-12-04 발표) — 등급 구분 점수, 등급별 비율
Y26 = {
 'kor': {'name': '국어', 'unit': '표준점수', 'max': 147,
         'cut': [133, 126, 117, 107, 94, 83, 73, 66, None],
         'pct': [4.67, 6.61, 12.56, 16.27, 21.14, 15.96, 12.30, 7.28, 3.20]},
 'math': {'name': '수학', 'unit': '표준점수', 'max': 139,
          'cut': [128, 124, 119, 111, 92, 79, 74, 71, None],
          'pct': [4.62, 8.66, 12.01, 15.69, 19.30, 17.03, 13.97, 5.01, 3.70]},
 'eng': {'name': '영어', 'unit': '원점수', 'max': 100,
         'cut': [90, 80, 70, 60, 50, 40, 30, 20, None],
         'pct': [3.11, 14.35, 26.30, 24.53, 13.28, 8.02, 5.64, 3.65, 1.13]},
 'his': {'name': '한국사', 'unit': '원점수', 'max': 50,
         'cut': [40, 35, 30, 25, 20, 15, 10, 5, None],
         'pct': [15.23, 13.00, 15.13, 15.67, 14.76, 12.18, 10.54, 3.13, 0.36]},
}
TAM26 = [('생활과 윤리',66,64,59,71),('윤리와 사상',66,64,59,70),('한국지리',68,65,59,72),('세계지리',68,63,59,73),
 ('동아시아사',65,62,59,68),('세계사',68,64,59,72),('경제',68,65,59,70),('정치와 법',65,62,59,67),('사회·문화',65,62,59,70),
 ('물리학Ⅰ',66,64,60,70),('화학Ⅰ',67,64,59,71),('생명과학Ⅰ',67,63,59,74),('지구과학Ⅰ',65,63,59,68),
 ('물리학Ⅱ',66,63,60,68),('화학Ⅱ',68,64,59,70),('생명과학Ⅱ',65,63,60,69),('지구과학Ⅱ',68,65,60,69)]
# 2027 예상 원점수 등급컷 — 입시기관 발표 후 채움 (None = 아직 발표 전)
Y27 = None

SRC = {
 'v': ('베리타스알파 11/17', 'https://www.veritas-a.com/news/articleView.html?idxno=634890'),
 'm': ('마이데일리 11/19', 'https://www.mydaily.co.kr/page/view/2026111906374091972'),
}
# 확인된 수험표 할인 (두 기사 이상 또는 상세 조건까지 나온 것만)
DC = [
 # name, cat, benefit, period, condition, official url or '', src key
 ('에버랜드','park','수험생 이용권 2만 원, 동반 최대 3명 1인 3만 원','~12/31','스마트 예약 후 현장에서 수험표(또는 수시 합격증)+신분증','https://www.everland.com','v'),
 ('롯데월드 어드벤처(서울)','park','종합이용권 2만 7천 원','11/19~12/31','현장 매표소에서 수험표+신분증','https://adventure.lotteworld.com','v'),
 ('롯데월드 어드벤처 부산','park','이용권 2만 원','11/19~12/31','현장 매표소에서 수험표+신분증','','v'),
 ('서울랜드','park','본인·동반 최대 2명 각 2만 500원','11/1~12/31','수험표·접수증·수시 합격증 중 원본+신분증, 다른 할인과 중복 불가','https://www.seoulland.co.kr','v'),
 ('레고랜드 코리아','park','본인 40%, 동반 최대 3명 30% 할인','11/20~12/18','현장 매표소에서 수험표+신분증, 온라인 사전 구매는 제외','https://www.legoland.kr','v'),
 ('롯데월드 아쿠아리움','aqua','입장권 1만 8,500원','11/19~11/30','현장 매표소에서 수험표+신분증','','v'),
 ('씨라이프 코엑스 아쿠아리움','aqua','본인 입장권 50% (1만 7,500원)','11/19~12/18','예약 없이 입장 게이트에서 수험표','','v'),
 ('씨라이프 부산 아쿠아리움','aqua','본인 입장권 50% (1만 6,000원)','11/19~12/18','예약 없이 입장 게이트에서 수험표','','v'),
 ('서울스카이','aqua','입장권 1만 6,500원','11/19~11/30','현장 매표소에서 수험표+신분증','https://seoulsky.lotteworld.com','v'),
 ('아산스파비스','aqua','워터파크 종일권 1만 원, 동반 1인 2만 원','~12/31','입장 시 수험표, 동반 인원 제한 없음','','v'),
 ('CGV','movie','2D 일반 영화 7,000원, 콤보 50%','11/19~11/30','현장 매표소에서 수험표 또는 학생증','https://www.cgv.co.kr','m'),
 ('롯데시네마','movie','영화 7,000원 + 매점 할인 쿠폰','~11/30','‘수고했수능’ 이벤트 (수험생·청소년)','https://www.lottecinema.co.kr','m'),
 ('메가박스','movie','영화 7,000원','~12/2','매표소 수험표 인증 또는 앱 쿠폰','https://www.megabox.co.kr','m'),
 ('아웃백 스테이크하우스','food','코코넛 슈림프 7조각 무료','~12/11','수험표 지참','https://www.outback.co.kr','m'),
 ('샤브올데이','food','본인 1만 3,900원 (초등 요금)','11/19~11/22','수험표 원본, 1매당 1회, 동반자는 정가','','v'),
 ('라그릴리아','food','지정 스테이크·폭립 50%','~11/30','카카오톡 채널 추가 후 수험표 또는 접수증, 5만 원 이상 주문 시 테이블당 1회','','v'),
 ('스트릿','food','밀크티 또는 레몬에이드 1잔 무료','~11/30','수험표 또는 접수증 (공항점 등 일부 제외)','','v'),
 ('63레스토랑 3곳','food','워킹온더클라우드·슈치쿠·백리향 지정 코스 40%','11/19~11/30','사전 예약, 수험표+신분증','','m'),
 ('제주항공','trip','국내선 플렉스 운임 20%','예매 ~12/16 · 탑승 ~2/25','본인+동반 1명, 성수기 제외, 공항 카운터에서 원본 증빙','https://www.jejuair.net','v'),
 ('이스타항공','trip','국내선 25%, 국제선 최대 10%','구매 ~12/31 · 탑승 ~3/27','홈페이지 구매, 본인+동반 1명, 공항에서 수험표','https://www.eastarjet.com','v'),
 ('트리니티항공','trip','국내선 25%, 국제선 최대 20%','예매 ~1/31 · 탑승 ~2/21','본인+동반 1명, 노선별 제외 기간 있음','','v'),
 ('국립 산림복지시설 10곳','trip','숙박 주중 30%, 주말 10%','11/20~2/28','‘숲e랑’에서 사전 예약 후 현장에서 수험표','','v'),
 ('하이서울유스호스텔','trip','객실 50% (캡슐·1~3인실)','~11/30','만 24세 이하 응시자, 부모 전화 예약, 수험표+부모 동의서','','v'),
]
CAT = {'park': ('테마파크', '🎢', '#FFE3EC', '#C2255C'), 'aqua': ('아쿠아리움·전망대·워터파크', '🐠', '#E0F2FF', '#1864AB'),
       'movie': ('영화', '🎬', '#F3E8FF', '#6741D9'), 'food': ('외식', '🍽️', '#FFF1DB', '#B35C00'),
       'trip': ('항공·숙박', '✈️', '#E3FAEC', '#2B8A3E')}

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# ── 비교표 HTML (서버 렌더: 검색엔진·JS 없는 환경도 보이게)
PB = [4, 11, 23, 40, 60, 77, 89, 96, 100]  # 등급별 누적 상한(%) — 상대평가 기준
def cum(p):
    out, c = [], 0
    for x in p: c += x; out.append(round(c, 2))
    return out
def table(key):
    d = Y26[key]; c = cum(d['pct']); rel = key in ('kor', 'math')
    rows = []
    for g in range(9):
        cut = f"{d['cut'][g]} 이상" if d['cut'][g] is not None else f"{d['cut'][g-1]} 미만"
        y27 = '<td class="y27">발표 전</td>'
        rows.append(f'<tr><th>{g+1}</th><td class="b">{cut}</td><td>{d["pct"][g]:.2f}%</td><td>{c[g]:.2f}%</td>'
                    + (f'<td>{PB[g]}%</td>' if rel else '') + y27 + '</tr>')
    head = (f'<tr><th>등급</th><th>2026 등급컷<small>({d["unit"]})</small></th><th>2026 비율</th><th>2026 누적</th>'
            + ('<th>기준 누적</th>' if rel else '') + '<th>2027 예상<small>(원점수)</small></th></tr>')
    return f'<div class="sn-tw"><table class="sn-t" data-k="{key}"><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'

tabs = ''.join(f'<button role="tab" aria-selected="{"true" if k=="kor" else "false"}" data-k="{k}">{Y26[k]["name"]}</button>' for k in Y26) \
       + '<button role="tab" aria-selected="false" data-k="tam">탐구</button>'
panels = ''.join(f'<div class="sn-p" data-k="{k}"{"" if k=="kor" else " hidden"}>{table(k)}</div>' for k in Y26)
tam_rows = ''.join(f'<tr><th>{n}</th><td class="b">{a}</td><td>{b}</td><td>{c}</td><td>{m}</td></tr>' for n, a, b, c, m in TAM26)
panels += (f'<div class="sn-p" data-k="tam" hidden><div class="sn-tw"><table class="sn-t"><thead><tr><th>과목</th><th>1등급</th><th>2등급</th><th>3등급</th><th>최고점</th></tr></thead>'
           f'<tbody>{tam_rows}</tbody></table></div><p class="sn-s">2026학년도 탐구 등급 구분 표준점수예요. 4등급 이하는 공개 자료에서 확인하지 못해 뺐어요.</p></div>')

def card(x):
    n, cat, ben, per, cond, off, src = x
    cn, ic, bg, fg = CAT[cat]
    href = off or SRC[src][1]
    lab = '공식 홈페이지' if off else '근거 기사'
    return (f'<article class="dc" data-c="{cat}"><a class="im" href="{href}" target="_blank" rel="noopener" style="--bg:{bg};--fg:{fg}" aria-label="{esc(n)} {lab} 열기">'
            f'<span class="ic" aria-hidden="true">{ic}</span><span class="nm">{esc(n)}</span><span class="go">{lab} ↗</span></a>'
            f'<div class="tx"><b>{esc(ben)}</b><p><span class="pd">{esc(per)}</span> {esc(cond)}</p>'
            f'<p class="sr"><a href="{SRC[src][1]}" target="_blank" rel="noopener">근거: {SRC[src][0]}</a></p></div></article>')
filt = '<button aria-pressed="true" data-v="">전체 ' + str(len(DC)) + '</button>' + ''.join(
    f'<button aria-pressed="false" data-v="{k}">{v[0]} {sum(1 for d in DC if d[1]==k)}</button>' for k, v in CAT.items())

FAQ = [
 ('2027 수능 예상 등급컷은 언제 나오나요?', '시험 당일인 11월 19일 저녁부터 EBSi·메가스터디·이투스·종로학원·진학사 같은 입시기관이 가채점 표본으로 예상 등급컷을 내요. 표본이 쌓이며 며칠간 바뀌니 하루 이틀 뒤 값을 함께 보세요. 이 페이지도 발표되는 대로 2027 예상 칸을 채워요.'),
 ('확정 등급컷과 성적표는 언제 나오나요?', '2027학년도 수능 성적은 12월 11일(금)에 통지돼요. 국어·수학·탐구는 평가원이 원점수 등급컷을 따로 내지 않고 등급 구분 표준점수로 발표해요.'),
 ('작년 등급컷과 왜 같이 봐야 하나요?', '등급은 상대평가라 해마다 난이도에 따라 원점수 컷이 크게 움직여요. 작년 수능은 국어 표준점수 최고점이 147점일 만큼 어려웠고, 영어 1등급은 3.11%에 그쳤어요. 올해 예상컷이 작년보다 오르면 쉬웠던 것, 내리면 어려웠던 것으로 읽으면 돼요.'),
 ('백분위 4%·11%·23%는 무엇인가요?', '상대평가 과목의 등급 기준 누적 비율이에요. 1등급 상위 4%, 2등급 11%, 3등급 23%, 4등급 40%, 5등급 60%, 6등급 77%, 7등급 89%, 8등급 96%까지예요. 동점자가 있으면 실제 비율은 조금 넘어요.'),
 ('수험표 할인은 수험표만 있으면 되나요?', '대부분 수험표 원본과 신분증을 함께 보여줘야 하고, 에버랜드처럼 사전 예약이 필요하거나 동반 인원 제한이 있는 곳도 있어요. 수험표는 버리지 말고 연말까지 챙겨 두세요. 조건은 바뀔 수 있으니 방문 전 공식 안내를 확인하세요.'),
]
faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>' for q, a in FAQ)
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "WebApplication", "name": "2027 수능 등급컷·예상 백분위 + 작년 수능 비교", "url": URL, "applicationCategory": "EducationalApplication",
   "operatingSystem": "Any", "inLanguage": "ko", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": "https://honglife.co.kr/"},
   {"@type": "ListItem", "position": 2, "name": "입시", "item": "https://honglife.co.kr/ipsi/"},
   {"@type": "ListItem", "position": 3, "name": "2027 수능 등급컷", "item": URL}]},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}

CSS = '''<style id="hl-sn">
.sn-note{background:#FFF8E1;border:1px solid #F5D77A;border-radius:12px;padding:10px 12px;font-size:14px;line-height:1.6;color:#5C4400;margin-top:10px}
.sn-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 12px}
.sn-tabs button,.sn-f button{border:1px solid var(--line-s);background:#fff;border-radius:999px;padding:7px 14px;font:inherit;font-size:14px;min-height:38px;cursor:pointer;color:var(--ink)}
.sn-tabs button[aria-selected=true],.sn-f button[aria-pressed=true]{background:var(--acc);border-color:var(--acc);color:#fff;font-weight:700}
.sn-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line-s);border-radius:12px}
.sn-t{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
.sn-t th,.sn-t td{padding:8px 8px;border-bottom:1px solid var(--line-s);text-align:center;white-space:nowrap}
.sn-t thead th{background:#F4F7FB;font-size:13px;color:var(--head);line-height:1.3}
.sn-t thead small{display:block;font-weight:400;color:var(--muted);font-size:11.5px}
.sn-t tbody th{background:#FAFBFD;font-weight:800;color:var(--head)}
.sn-t td.b{font-weight:700;color:var(--head)}
.sn-t td.y27{color:#9A6B00;font-size:13px}
.sn-t tr.me td,.sn-t tr.me th{background:#E7F0FF}
.sn-s{font-size:13px;color:var(--muted);line-height:1.6;margin:8px 0 0}
.sn-calc{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.sn-calc label{display:flex;flex-direction:column;gap:5px;font-size:14px;font-weight:700;color:var(--head)}
.sn-calc select,.sn-calc input{font:inherit;font-size:16px;padding:10px;border:1px solid var(--line-s);border-radius:10px;min-height:44px;width:100%;box-sizing:border-box;background:#fff}
.sn-out{margin-top:12px;border-radius:14px;background:#F4F7FB;padding:14px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;text-align:center}
.sn-out div{background:#fff;border-radius:10px;padding:10px 4px}
.sn-out b{display:block;font-size:24px;color:var(--head);line-height:1.2}
.sn-out span{display:block;font-size:12.5px;line-height:1.35;color:var(--muted);word-break:keep-all}
.sn-msg{grid-column:1/-1;font-size:13.5px;line-height:1.6;color:var(--ink);text-align:left}
.sn-f{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.dcl{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.dc{border:1px solid var(--line-s);border-radius:14px;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.dc .im{display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;column-gap:10px;align-items:center;padding:14px;background:var(--bg);color:var(--fg);text-decoration:none;min-height:76px}
.dc .ic{grid-row:1/3;font-size:34px;line-height:1;width:52px;height:52px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 0 rgba(0,0,0,.06)}
.dc .nm{font-weight:800;font-size:16.5px;line-height:1.3;word-break:keep-all}
.dc .go{font-size:12.5px;font-weight:700;opacity:.85}
.dc .tx{padding:12px 14px 14px;display:flex;flex-direction:column;gap:6px}
.dc .tx b{font-size:15px;color:var(--head);line-height:1.45;word-break:keep-all}
.dc .tx p{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink);word-break:keep-all}
.dc .pd{display:inline-block;background:#F1F3F5;border-radius:6px;padding:1px 6px;font-weight:700;font-size:12.5px;margin-right:2px}
.dc .sr a{font-size:12.5px;color:var(--muted)}
.pe-faq dt{font-weight:700;margin-top:12px;color:var(--head)}.pe-faq dd{margin:4px 0 0;line-height:1.65;color:var(--ink)}
@media(max-width:520px){.sn-t{font-size:12.5px}.sn-t th,.sn-t td{padding:7px 3px}.sn-t thead th{white-space:normal;font-size:11.5px;word-break:keep-all}.sn-t thead small{font-size:10.5px}.sn-t td.y27{font-size:11.5px;white-space:normal}.sn-t thead th:first-child{white-space:nowrap}.sn-calc{grid-template-columns:1fr}.sn-out b{font-size:21px}}
</style>
'''

MAIN = f'''<main class="wrap wide"><header class="top hub"><p class="crumb"><a href="/">홈</a> › <a href="/ipsi/">입시</a> › 2027 수능 등급컷</p>
<h1>2027 수능 등급컷·예상 백분위</h1>
<p class="lead">2027학년도 수능(2026년 11월 19일) 예상 등급컷을 작년 2026학년도 수능 실제 등급 구분 점수·비율과 나란히 놓고 비교해요. 점수를 넣으면 작년 기준 등급과 추정 백분위가 나오고, 아래에 확인된 수험표 할인을 모았어요.</p>
<p class="sn-note"><b>올해 예상 등급컷은 오늘 저녁 입시기관 발표 후 채워요.</b> 지금 보이는 숫자는 모두 작년(2026학년도) 평가원 채점 결과예요. 성적 통지는 12월 11일(금). 마지막 확인: {UPDATED}</p>
</header>
<section class="card"><h2>작년 수능 등급컷·백분위 비교표</h2>
<div class="sn-tabs" role="tablist" aria-label="영역">{tabs}</div>
{panels}
<p class="sn-s">국어·수학은 선택과목 조정을 거친 <b>표준점수</b> 기준이라 원점수 컷과 다르고, 평가원은 원점수 등급컷을 따로 발표하지 않아요. ‘기준 누적’은 상대평가 등급의 원래 누적 비율이고, ‘2026 누적’은 동점자 때문에 실제로 그 등급까지 든 비율이에요. 영어·한국사는 절대평가라 원점수로 등급이 정해져요.</p>
</section>
<section class="card tool"><h2>내 점수로 등급·추정 백분위 보기</h2>
<div class="sn-calc"><label>영역<select id="sk"><option value="kor">국어 (표준점수)</option><option value="math">수학 (표준점수)</option><option value="eng">영어 (원점수)</option><option value="his">한국사 (원점수)</option></select></label>
<label><span id="sl">표준점수</span><input id="sv" type="number" inputmode="numeric" min="0" max="200" placeholder="예: 128"></label></div>
<div class="sn-out" aria-live="polite"><div><b id="og">–</b><span>작년 기준 등급</span></div><div><b id="op">–</b><span>추정 백분위</span></div><div><b id="ot">–</b><span>상위 누적</span></div>
<p class="sn-msg" id="om">가채점 서비스나 성적표의 점수를 넣어 보세요. 국어·수학은 표준점수, 영어·한국사는 원점수예요.</p></div>
<p class="sn-s">추정 백분위는 작년 등급 구분 점수와 등급별 비율 사이를 직선으로 이어 계산한 대략값이에요. 실제 백분위는 성적표에서 확인하세요.</p>
</section>
<section class="card" id="discount"><h2>2027 수능 수험표 할인 모음</h2>
<p class="sn-s" style="margin:0 0 10px">기사로 조건까지 확인된 곳만 모았어요. 카드 위쪽 그림을 누르면 공식 홈페이지(없으면 근거 기사)로 이동해요. 대부분 <b>수험표 원본+신분증</b>이 필요하니 수험표를 버리지 마세요.</p>
<div class="sn-f" role="group" aria-label="분류">{filt}</div>
<div class="dcl" id="dcl">{"".join(card(x) for x in DC)}</div>
<p class="sn-s">혜택과 기간은 업체 사정으로 바뀌거나 조기 종료될 수 있어요. 방문·예약 전 공식 안내를 꼭 확인하세요.</p>
</section>
<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">{faq_html}</dl></section>
<section class="card"><h2>출처</h2><p class="pe-src">2026학년도 등급 구분 점수·비율: 한국교육과정평가원 2026학년도 수능 채점 결과(2025년 12월 4일 발표). 2027 일정: 평가원 시행 세부계획. 수험표 할인: <a href="{SRC['v'][1]}" target="_blank" rel="noopener">베리타스알파(11/17)</a>, <a href="{SRC['m'][1]}" target="_blank" rel="noopener">마이데일리(11/19)</a> 및 각 업체 안내.</p></section>
<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist"><li><a href="/ipsi/"><b>입시 도구 모음</b><span>정시·미대·편입 도구 전체 보기</span></a></li><li><a href="/ipsi/pyeonip-2027.html"><b>2027 편입 일정·경쟁률</b><span>수도권·거점국립대 71곳</span></a></li></ul></section>
</main>
'''

JS = '<script>\n(function(){\nvar Y=' + json.dumps(Y26, ensure_ascii=False) + ';\n' + r'''
function cum(p){var o=[],c=0;p.forEach(function(x){c+=x;o.push(c)});return o}
var tl=document.querySelector('.sn-tabs');
tl.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
 [].forEach.call(tl.children,function(x){x.setAttribute('aria-selected',x===b?'true':'false')});
 [].forEach.call(document.querySelectorAll('.sn-p'),function(p){p.hidden=p.dataset.k!==b.dataset.k});
 if(window.gtag)gtag('event','sn_tab',{k:b.dataset.k});});
var sk=document.getElementById('sk'),sv=document.getElementById('sv');
function calc(){
 var k=sk.value,d=Y[k],v=parseFloat(sv.value),rel=(k==='kor'||k==='math');
 document.getElementById('sl').textContent=d.unit;sv.placeholder=rel?'예: 128':(k==='eng'?'예: 85':'예: 42');sv.max=d.max;
 [].forEach.call(document.querySelectorAll('.sn-t tr.me'),function(r){r.classList.remove('me')});
 var G=document.getElementById('og'),P=document.getElementById('op'),T=document.getElementById('ot'),M=document.getElementById('om');
 if(isNaN(v)){G.textContent=P.textContent=T.textContent='–';M.textContent='가채점 서비스나 성적표의 점수를 넣어 보세요. 국어·수학은 표준점수, 영어·한국사는 원점수예요.';return}
 if(v>d.max||v<0){G.textContent=P.textContent=T.textContent='–';M.textContent=d.name+' '+d.unit+'는 0~'+d.max+'점 사이로 넣어 주세요. (작년 최고점 '+d.max+')';return}
 var g=8;for(var i=0;i<8;i++){if(v>=d.cut[i]){g=i;break}}
 var c=cum(d.pct),lo=g?c[g-1]:0,hi=c[g],top,hiS,loS;
 if(g===0){hiS=d.max;loS=d.cut[0]}else if(g===8){hiS=d.cut[7];loS=0}else{hiS=d.cut[g-1];loS=d.cut[g]}
 var f=hiS===loS?0.5:(hiS-v)/(hiS-loS);f=Math.max(0,Math.min(1,f));top=lo+(hi-lo)*f;
 G.textContent=(g+1)+'등급';T.textContent=top.toFixed(1)+'%';
 P.textContent=rel?Math.max(0,Math.min(100,Math.round(100-top))):'–';
 var tr=document.querySelector('.sn-t[data-k="'+k+'"] tbody').children[g];if(tr)tr.classList.add('me');
 M.textContent=rel?('작년 '+d.name+' '+(g+1)+'등급 구간('+(g===8?d.cut[7]+' 미만':d.cut[g]+' 이상')+')이에요. 추정 백분위는 대략값이니 참고만 하세요.')
  :(d.name+'은 절대평가라 올해도 '+(g===8?d.cut[7]+'점 미만':d.cut[g]+'점 이상')+'이면 '+(g+1)+'등급이에요. 상위 누적은 작년 비율 기준이에요. 영어·한국사는 백분위가 없어요.');
 if(window.gtag)gtag('event','sn_calc',{k:k});
}
sk.addEventListener('change',function(){sv.value='';calc();
 [].forEach.call(tl.children,function(x){if(x.dataset.k===sk.value)x.click()})});
sv.addEventListener('input',calc);calc();
var ff=document.querySelector('.sn-f');
ff.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;
 [].forEach.call(ff.children,function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
 [].forEach.call(document.querySelectorAll('.dc'),function(c){c.hidden=!!b.dataset.v&&c.dataset.c!==b.dataset.v});});
document.getElementById('dcl').addEventListener('click',function(e){var a=e.target.closest('a');if(a&&window.gtag)gtag('event','sn_discount',{t:a.textContent.slice(0,30)});});
})();
</script>
'''

# assemble from the pyeonip shell
i_ld = base.find('<script type="application/ld')
i_st = base.find('<style', i_ld); i_ste = base.find('</style>', i_st) + len('</style>\n')
i_main = base.find('<main'); i_mend = base.find('</main>') + len('</main>\n')
i_ft = base.find('<footer')
head = base[:i_ld]
head = re.sub(r'<title>.*?</title>', f'<title>{esc(TITLE)}</title>', head)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(DESC), head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(DESC), head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(TITLE), head)
head = head.replace('https://honglife.co.kr/ipsi/pyeonip-2027.html', URL).replace('<meta property="og:url" content="https://honglife.co.kr/ipsi/">', '')
out = (head + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS
       + base[i_ste:i_main] + MAIN + JS + base[i_ft:])
open(os.path.join(ROOT, 'overlay/ipsi/suneung-2027.html'), 'w', encoding='utf-8').write(out)
print('wrote', len(out))
