"""냉장고 털기 요리 추천 (/life/fridge-recipe.html)."""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'data'))
from fridge_recipes import ING, R
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
s = open(os.path.join(ROOT, 'overlay/life/taxi-fare.html'), encoding='utf-8').read()
a = s.find('<style id="hl-mt">'); b = s.find('</style>', a) + 8
i = s.find('<main'); j = s.find('</main>') + 7
head = s[:a]; between = s[b:i]
k = s.find('<script>window.HL_V=', j)
tail = s[k:] if k > 0 else '</body>\n</html>\n'
N = len(R)
URL = 'https://honglife.co.kr/life/fridge-recipe.html'
TITLE = f'냉장고 털기 · 있는 재료로 요리 추천 (집밥 {N}가지, 단계별 타이머)'
DESC = f'냉장고에 있는 재료를 누르면 지금 바로 만들 수 있는 집밥 {N}가지를 찾아 주고, 한두 가지만 더 있으면 되는 요리도 알려 줘요. 김치볶음밥·된장찌개·제육볶음·계란말이 등 1~2인분 레시피를 단계별 타이머와 함께 보여 주는 무료 도구예요.'
BASIC = '소금·간장·설탕·식초·식용유·참기름·다진 마늘·고춧가루·후추·깨'
FAQ = [
    ("어떤 재료가 '기본 양념'인가요?", f"{BASIC}는 웬만한 집에 다 있다고 보고 재료 고르기에서 뺐어요. 고추장·된장·굴소스·케첩·마요네즈·카레가루는 없는 집도 많아서 따로 고르게 했어요."),
    ("레시피는 몇 인분인가요?", "대부분 1~2인분 기준이에요. 찌개·국은 2~3인분, 닭볶음탕·찜닭은 닭 1마리(약 1kg) 기준이에요. 양을 늘리거나 줄이려면 '레시피 양 조절 계산기'로 계량을 한 번에 바꿀 수 있어요."),
    ("'1개만 더 있으면'은 무슨 뜻인가요?", "꼭 필요한 재료 가운데 하나만 빠진 요리예요. 무엇이 빠졌는지 보여 주니, 장 볼 때 그것만 사면 바로 만들 수 있어요. '빠진 재료 복사'를 누르면 장보기 메모로 붙여 넣을 수 있어요."),
    ("요리 모드는 무엇인가요?", "한 단계씩 큰 글씨로 보여 주고, 끓이기·졸이기처럼 시간이 필요한 단계에는 타이머 버튼이 붙어요. 타이머가 끝나면 소리와 진동으로 알려 주고, 요리하는 동안 화면이 꺼지지 않게 해요(지원하는 브라우저에서)."),
    ("고른 재료가 저장되나요?", "이 기기의 브라우저에만 저장돼서 다음에 열어도 그대로 남아 있어요. 서버로는 아무것도 보내지 않아요."),
    ("알레르기가 있으면 어떻게 하나요?", "재료 목록에 보이지 않는 양념이나 가공식품(어묵·햄·만두 등)에도 알레르기 성분이 들어 있을 수 있어요. 포장의 알레르기 표시를 꼭 확인해 주세요."),
]
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "냉장고 털기 요리 추천", "url": URL, "applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "inLanguage": "ko", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": "https://honglife.co.kr/"}, {"@type": "ListItem", "position": 2, "name": "생활·행정", "item": "https://honglife.co.kr/life/"}, {"@type": "ListItem", "position": 3, "name": "냉장고 털기 요리 추천", "item": URL}]},
    {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in FAQ]}]}
head = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | 홍라이프 도구</title>', head, count=1, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head, count=1)
head = head.replace('https://honglife.co.kr/life/taxi-fare.html', URL)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE + ' | 홍라이프 도구', head, count=1)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + DESC, head, count=1)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>', head, count=1, flags=re.S)

CSS = '''<style id="hl-fr">
.fr input{font:inherit;font-size:16px;border:1px solid var(--line-s);border-radius:12px;min-height:44px;padding:9px 12px;width:100%;box-sizing:border-box;background:#fff;min-width:0}
.fr-hero{position:relative;overflow:hidden;border-radius:22px;padding:20px 18px;color:#fff;background:radial-gradient(130% 150% at 0% 0%,#FF9A62 0%,#FF5F6D 48%,#C2255C 100%);box-shadow:0 10px 28px rgba(194,37,92,.22)}
.fr-hero:after{content:"";position:absolute;right:-40px;top:-40px;width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.1)}
.fr-hin{position:relative;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:center;z-index:1}
.fr-k{display:inline-block;font-size:13px;font-weight:800;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:3px 12px}
.fr-big{font-size:32px;font-weight:900;line-height:1.2;margin:10px 0 4px;letter-spacing:-.6px;overflow-wrap:anywhere}
.fr-big b{color:#FFF3B0}
.fr-sub{font-size:14.5px;opacity:.95;overflow-wrap:anywhere}
.fr-fridge{font-size:64px;line-height:1;filter:drop-shadow(0 6px 10px rgba(0,0,0,.15))}
.fr-pick{margin-top:14px;display:flex;flex-wrap:wrap;gap:6px;min-height:34px;position:relative;z-index:1}
.fr-pick button{border:0;background:rgba(255,255,255,.95);color:#9F1239;border-radius:999px;padding:6px 10px 6px 12px;font:inherit;font-size:13.5px;font-weight:700;cursor:pointer;display:inline-flex;gap:4px;align-items:center}
.fr-pick button:after{content:"×";font-size:15px;opacity:.6}
.fr-pick em{font-style:normal;font-size:13.5px;opacity:.9}
.fr-bar{display:flex;gap:8px;align-items:center;margin-bottom:12px}
.fr-bar .x{flex:none;border:0;background:#F2F4F6;color:var(--ink);border-radius:12px;min-height:44px;padding:0 14px;font:inherit;font-size:14.5px;font-weight:700;cursor:pointer}
.fr-quick{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 6px}
.fr-quick button{border:1px dashed #E11D48;background:#FFF1F2;color:#BE123C;border-radius:999px;padding:6px 12px;font:inherit;font-size:13.5px;font-weight:700;cursor:pointer}
.fr-g{margin-top:14px}
.fr-g h3{font-size:14px;color:var(--muted);margin:0 0 8px;font-weight:800}
.fr-chips{display:flex;flex-wrap:wrap;gap:7px}
.fr-chip{border:1.5px solid var(--line-s);background:#fff;border-radius:14px;padding:7px 11px;font:inherit;font-size:14.5px;color:var(--head);cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:transform .12s,background .15s,border-color .15s;min-height:40px}
.fr-chip i{font-style:normal;font-size:17px}
.fr-chip[aria-pressed=true]{background:#FFF1F2;border-color:#E11D48;color:#9F1239;font-weight:800}
.fr-chip[aria-pressed=true]:before{content:"✓";font-weight:900;color:#E11D48}
.fr-chip:active{transform:scale(.95)}
.fr-chip.hid{display:none}
.fr-f{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.fr-f button{border:1px solid var(--line-s);background:#fff;border-radius:999px;padding:7px 13px;font:inherit;font-size:14px;cursor:pointer;color:var(--ink);min-height:38px}
.fr-f button[aria-pressed=true]{background:var(--head);border-color:var(--head);color:#fff;font-weight:700}
.fr-sec{font-size:15.5px;font-weight:900;color:var(--head);margin:18px 0 10px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.fr-sec span{font-size:13px;font-weight:700;color:var(--muted)}
.fr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.fr-card{white-space:normal;position:relative;display:grid;grid-template-columns:64px minmax(0,1fr);gap:12px;align-items:center;border:1px solid var(--line);border-radius:18px;padding:12px;background:#fff;cursor:pointer;text-align:left;font:inherit;color:inherit;width:100%;transition:box-shadow .15s,transform .15s}
.fr-card:hover{box-shadow:0 8px 22px rgba(17,24,39,.08);transform:translateY(-1px)}
.fr-em{width:64px;height:64px;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:34px;position:relative}
.fr-em svg{position:absolute;inset:-4px;width:72px;height:72px;transform:rotate(-90deg)}
.fr-card .n{font-size:16px;font-weight:900;color:var(--head);overflow-wrap:anywhere;padding-right:26px}
.fr-card .m{font-size:12.5px;color:var(--muted);margin-top:2px}
.fr-card .fst{display:block;white-space:normal;font-size:13px;font-weight:800;margin-top:5px;overflow-wrap:anywhere}
.fr-card .fst.sok{color:#1B64DA}.fr-card .fst.sms{color:#C2410C}.fr-card .fst.sno{color:var(--muted);font-weight:600}
.fr-fav{position:absolute;right:10px;top:10px;font-size:17px;line-height:1;opacity:.9}
.fr-none{text-align:center;color:var(--muted);padding:22px 10px;border:1px dashed var(--line-s);border-radius:16px;font-size:14.5px}
.fr-more{display:block;margin:12px auto 0;border:1px solid var(--line-s);background:#fff;border-radius:999px;padding:9px 18px;font:inherit;font-size:14.5px;font-weight:700;cursor:pointer;color:var(--ink)}
.fr-dlg{border:0;padding:0;border-radius:22px;width:min(560px,calc(100vw - 20px));max-height:calc(100vh - 30px);box-shadow:0 24px 70px rgba(0,0,0,.3);overflow:auto}
.fr-dlg::backdrop{background:rgba(17,24,39,.5)}
.fr-dh{display:grid;grid-template-columns:72px minmax(0,1fr) 40px;gap:12px;align-items:center;padding:18px 18px 12px;position:sticky;top:0;background:#fff;z-index:2;border-bottom:1px solid var(--line)}
.fr-dh .fr-em{width:72px;height:72px;font-size:40px}
.fr-dh h3{margin:0;font-size:20px;color:var(--head);overflow-wrap:anywhere}
.fr-dh p{margin:3px 0 0;font-size:13px;color:var(--muted)}
.fr-close{width:40px;height:40px;border-radius:50%;border:0;background:#F2F4F6;font-size:20px;cursor:pointer;align-self:start}
.fr-db{padding:14px 18px 18px}
.fr-ing{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 6px}
.fr-ing span{border-radius:10px;padding:5px 10px;font-size:14px;font-weight:700}
.fr-ing .h{background:#E8F3FF;color:#1957C2}.fr-ing .x{background:#FFF1F2;color:#BE123C;border:1px dashed #FDA4AF}.fr-ing .o{background:#F2F4F6;color:var(--muted);font-weight:600}.fr-ing .oh{background:#EEF2FF;color:#4338CA}
.fr-lb{font-size:13px;font-weight:800;color:var(--muted);margin:12px 0 6px}
.fr-steps{list-style:none;margin:0;padding:0;counter-reset:s}
.fr-steps li{position:relative;padding:10px 0 10px 40px;border-bottom:1px solid var(--line);font-size:15.5px;line-height:1.6;color:var(--ink)}
.fr-steps li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:10px;width:28px;height:28px;border-radius:50%;background:#FFE4E6;color:#BE123C;font-weight:900;font-size:14px;display:flex;align-items:center;justify-content:center}
.fr-tm{display:inline-flex;align-items:center;gap:4px;margin-left:6px;border:0;background:#FFF7ED;color:#C2410C;border-radius:999px;padding:3px 10px;font:inherit;font-size:13px;font-weight:800;cursor:pointer;vertical-align:1px}
.fr-acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.fr-b{border:0;border-radius:14px;min-height:48px;padding:0 18px;font:inherit;font-size:15.5px;font-weight:800;cursor:pointer;background:linear-gradient(135deg,#FF6B6B,#E11D48);color:#fff;flex:1 1 auto}
.fr-b.s{background:#F2F4F6;color:var(--ink);flex:0 1 auto}
.fr-note{font-size:12.5px;color:var(--muted);margin:10px 0 0}
.fr-cook{position:fixed;inset:0;z-index:100;background:#FFFBF7;display:flex;flex-direction:column}
.fr-cook[hidden]{display:none}
.fr-ct{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #F3E8E0}
.fr-ct b{flex:1;font-size:16px;color:var(--head);min-width:0;overflow-wrap:anywhere}
.fr-pg{height:5px;background:#F3E8E0}.fr-pg i{display:block;height:100%;background:linear-gradient(90deg,#FF8A5B,#E11D48);transition:width .35s}
.fr-cb{flex:1;overflow:auto;padding:24px 22px;display:flex;flex-direction:column;justify-content:center;max-width:680px;margin:0 auto;width:100%;box-sizing:border-box}
.fr-cn{font-size:14px;font-weight:900;color:#E11D48;letter-spacing:.5px}
.fr-cs{font-size:25px;line-height:1.55;font-weight:700;color:var(--head);margin:10px 0 22px;overflow-wrap:anywhere}
.fr-timer{display:flex;align-items:center;gap:16px;background:#fff;border:1px solid #F3E8E0;border-radius:20px;padding:14px 16px}
.fr-ring{position:relative;width:86px;height:86px;flex:none}
.fr-ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.fr-ring b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:20px;font-variant-numeric:tabular-nums;color:var(--head)}
.fr-timer .tb{display:flex;flex-direction:column;gap:6px;min-width:0;flex:1}
.fr-timer .tb span{font-size:13.5px;color:var(--muted)}
.fr-timer.done{animation:fl .8s 4}
@keyframes fl{50%{background:#FFE4E6}}
.fr-cf{display:grid;grid-template-columns:1fr 1.4fr;gap:10px;padding:14px 16px calc(14px + env(safe-area-inset-bottom));border-top:1px solid #F3E8E0;background:#fff}
.fr-cf button{min-height:54px;border-radius:16px;font:inherit;font-size:17px;font-weight:900;cursor:pointer;border:0}
.fr-cf .p{background:#F2F4F6;color:var(--ink)}.fr-cf .n{background:linear-gradient(135deg,#FF6B6B,#E11D48);color:#fff}
.fr-tbl{width:100%;border-collapse:collapse;font-size:14.5px}.fr-tbl th,.fr-tbl td{border-bottom:1px solid var(--line);padding:9px 6px;text-align:left;vertical-align:top}
.fr-tbl td:first-child{white-space:nowrap;font-weight:800;color:var(--head)}
.fr-toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%) translateY(30px);opacity:0;background:#191F28;color:#fff;border-radius:999px;padding:11px 18px;font-size:14.5px;font-weight:700;transition:.3s;z-index:120;pointer-events:none;max-width:calc(100vw - 30px);text-align:center}
.fr-toast.on{opacity:1;transform:translateX(-50%)}
@media(max-width:560px){.fr-big{font-size:26px}.fr-fridge{font-size:48px}.fr-grid{grid-template-columns:1fr}.fr-cs{font-size:21px}.fr-dh{grid-template-columns:60px minmax(0,1fr) 40px;padding:14px 14px 10px}.fr-dh .fr-em{width:60px;height:60px;font-size:32px}.fr-db{padding:12px 14px 16px}}
@media(max-width:360px){.fr-big{font-size:23px}.fr-chip{padding:6px 9px;font-size:14px}.fr-card{grid-template-columns:56px minmax(0,1fr);gap:10px}.fr-em{width:56px;height:56px;font-size:30px}.fr-em svg{width:64px;height:64px}}
@media(prefers-reduced-motion:reduce){.fr-card,.fr-chip{transition:none}.fr-timer.done{animation:none}}
</style>'''

groups = ''.join(f'<div class="fr-g"><h3>{g}</h3><div class="fr-chips">' + ''.join(f'<button type="button" class="fr-chip" data-i="{n}" aria-pressed="false"><i>{e}</i>{n}</button>' for n, e in l) + '</div></div>' for g, l in ING)
kinds = ['밥', '면', '국', '반찬', '간식']
cnt = {kk: sum(1 for r in R if r['k'] == kk) for kk in kinds}
table = ''.join(f'<tr><td>{kk} ({cnt[kk]})</td><td>{", ".join(r["n"] for r in R if r["k"] == kk)}</td></tr>' for kk in kinds)

main = f'''<main class="wrap wide fr"><header class="top"><p class="crumb"><a href="/">홈</a> › <a href="/life/">생활·행정</a></p><h1>냉장고 털기 · 있는 재료로 요리 추천</h1><p class="lead">냉장고에 있는 재료를 누르기만 하면 <b>지금 바로 만들 수 있는 집밥</b>과 <b>한 가지만 더 있으면 되는 요리</b>를 찾아 드려요. 레시피는 한 단계씩 큰 글씨와 타이머로 따라 할 수 있어요.</p></header>
<section class="card tool" style="padding:14px"><div class="fr-hero"><div class="fr-hin"><div style="min-width:0"><span class="fr-k">🧊 집밥 {N}가지</span><div class="fr-big" id="hb">재료를 골라 주세요</div><div class="fr-sub" id="hs">아래에서 냉장고에 있는 재료를 눌러요. 기본 양념은 있다고 볼게요.</div></div><div class="fr-fridge" aria-hidden="true">🍳</div></div><div class="fr-pick" id="pick"></div></div></section>
<section class="card tool"><h2>냉장고에 있는 재료</h2>
<div class="fr-bar"><input id="q" placeholder="재료 찾기 (예: 두부)" aria-label="재료 찾기" autocomplete="off"><button type="button" class="x" id="clr">모두 빼기</button></div>
<div class="fr-quick"><button type="button" data-qk="달걀,양파,대파,김치,밥">+ 자주 있는 재료 한 번에</button><button type="button" data-qk="라면,달걀,대파">+ 라면 하나 있을 때</button></div>
{groups}
<p class="fr-note">기본 양념({BASIC})은 집에 있다고 보고 뺐어요.</p></section>
<section class="card tool" id="res"><h2>만들 수 있는 요리</h2>
<div class="fr-f" id="fk"><button type="button" data-k="" aria-pressed="true">전체</button>{''.join(f'<button type="button" data-k="{kk}" aria-pressed="false">{kk}</button>' for kk in kinds)}<button type="button" data-fav="1" aria-pressed="false">♥ 즐겨찾기</button></div>
<div class="fr-f" id="ft"><button type="button" data-t="0" aria-pressed="true">시간 상관없음</button><button type="button" data-t="15" aria-pressed="false">15분 이내</button><button type="button" data-t="30" aria-pressed="false">30분 이내</button></div>
<div id="out"></div></section>
<section class="card"><h2>이렇게 쓰세요</h2><ol class="xp">
<li><b>재료 누르기</b>: 냉장고를 열어 보이는 재료를 눌러요. 고른 재료는 위 빨간 카드에 모이고, 다음에 열어도 그대로 남아 있어요.</li>
<li><b>요리 고르기</b>: '바로 만들 수 있어요'가 먼저 나오고, 그다음 '○○만 있으면 돼요'가 나와요. 둥근 테두리는 필요한 재료가 얼마나 있는지 보여 줘요.</li>
<li><b>요리 모드</b>: 레시피에서 '요리 모드 시작'을 누르면 한 단계씩 큰 글씨로 보여 주고, 시간이 필요한 단계는 타이머를 눌러 맞출 수 있어요.</li></ol></section>
<section class="card"><h2>들어 있는 요리 {N}가지</h2><table class="fr-tbl"><tbody>{table}</tbody></table></section>
<section class="card"><h2>남은 재료 오래 두는 요령</h2><ul class="xp">
<li><b>대파</b>: 송송 썰어 지퍼백에 넣어 냉동하면 국·볶음밥에 바로 한 줌씩 쓸 수 있어요.</li>
<li><b>두부</b>: 쓰고 남은 두부는 밀폐 용기에 물을 채워 냉장하고, 물은 날마다 갈아 주세요. 2~3일 안에 먹는 게 좋아요.</li>
<li><b>밥</b>: 갓 지은 밥을 한 공기씩 랩이나 용기에 담아 냉동하면 데웠을 때 덜 말라요.</li>
<li><b>김치</b>: 시어진 김치는 김치찌개·김치전·김치볶음밥에 쓰면 오히려 맛있어요.</li>
<li><b>소비기한</b>: 포장에 적힌 날짜와 보관 방법(냉장·냉동)을 지키고, 냄새나 색이 이상하면 먹지 마세요.</li></ul></section>
<section class="card"><h2>자주 묻는 질문</h2><dl class="pe-faq">{''.join(f"<dt>{q}</dt><dd>{x}</dd>" for q, x in FAQ)}</dl></section>
<section class="card rel"><h2>함께 쓰면 좋은 도구</h2><ul class="tlist"><li><a href="/life/recipe-scale.html"><b>레시피 양 조절 계산기</b><span>2인분을 4인분으로, 계량 한 번에</span></a></li><li><a href="/life/cooking-measure.html"><b>요리 계량 변환</b><span>큰술·작은술·컵·g 바꾸기</span></a></li><li><a href="/life/lunch-menu.html"><b>점심 메뉴 추천</b><span>오늘 뭐 먹지? 랜덤 고르기</span></a></li><li><a href="/sheet/meal-plan.html"><b>식단표 엑셀</b><span>한 주 식단 미리 짜기</span></a></li></ul></section>
</main>
<div class="fr-toast" id="toast" role="status" aria-live="polite"></div>
<dialog class="fr-dlg" id="dlg" aria-labelledby="dt"></dialog>
<div class="fr-cook" id="cook" hidden role="dialog" aria-modal="true" aria-label="요리 모드"><div class="fr-ct"><b id="ck-t"></b><button type="button" class="fr-close" id="ck-x" aria-label="요리 모드 닫기">×</button></div><div class="fr-pg"><i id="ck-p"></i></div>
<div class="fr-cb"><div class="fr-cn" id="ck-n"></div><div class="fr-cs" id="ck-s"></div><div class="fr-timer" id="ck-tm" hidden><div class="fr-ring"><svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.9" fill="none" stroke="#F3E8E0" stroke-width="3.2"/><circle id="ck-rc" cx="18" cy="18" r="15.9" fill="none" stroke="#E11D48" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="100 100"/></svg><b id="ck-tv">0:00</b></div><div class="tb"><span id="ck-tl">이 단계 타이머</span><div style="display:flex;gap:8px;flex-wrap:wrap"><button type="button" class="fr-b" id="ck-go" style="min-height:44px;flex:0 1 auto">타이머 시작</button><button type="button" class="fr-b s" id="ck-rs" style="min-height:44px">처음부터</button></div></div></div></div>
<div class="fr-cf"><button type="button" class="p" id="ck-prev">이전</button><button type="button" class="n" id="ck-next">다음 단계</button></div></div>
'''

DATA = {'ing': {n: e for g, l in ING for n, e in l}, 'r': [{'n': r['n'], 'e': r['e'], 'k': r['k'], 'm': r['m'], 'need': r['need'], 'opt': r['opt'], 's': r['s']} for r in R]}

JS = r'''<script>
(function(){
var D=__DATA__,$=function(i){return document.getElementById(i)},K='hl-fridge-v1';
var esc=function(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var KC={'밥':['#FFF4E6','#FFE0B8'],'면':['#FFF1F2','#FFD1D8'],'국':['#EEF4FF','#D3E3FF'],'반찬':['#F5F0FF','#E2D6FF'],'간식':['#FFF9DB','#FFEB99']};
var S;try{S=JSON.parse(localStorage.getItem(K)||'null')}catch(e){}if(!S||!S.have)S={have:[],fav:[]};
var HAVE={};S.have.forEach(function(x){if(D.ing[x])HAVE[x]=1});
var FK='',FT=0,FF=0,SHOW=12;
function save(){S.have=Object.keys(HAVE);try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}}
function toast(t){var e=$('toast');e.textContent=t;e.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(function(){e.classList.remove('on')},2000)}
function ok(x){return Array.isArray(x)?x.some(function(y){return HAVE[y]}):!!HAVE[x]}
function lab(x){return Array.isArray(x)?x.join('·'):x}
function score(r){var miss=r.need.filter(function(x){return !ok(x)}),oh=r.opt.filter(function(x){return HAVE[x]}).length;return {miss:miss,have:r.need.length-miss.length,oh:oh}}
function ring(p,c){var v=Math.round(p*100);return '<svg viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="16.5" fill="none" stroke="rgba(0,0,0,.06)" stroke-width="2.2"/><circle cx="18" cy="18" r="16.5" fill="none" stroke="'+c+'" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="'+(v*1.037).toFixed(1)+' 200"/></svg>'}
function card(r,i){var sc=score(r),p=sc.have/r.need.length,kc=KC[r.k]||KC['반찬'],st;
 if(!sc.miss.length)st='<span class="fst sok">✅ 바로 만들 수 있어요'+(sc.oh?' · 곁들임 '+sc.oh+'개 있음':'')+'</span>';
 else if(sc.miss.length===1)st='<span class="fst sms">🛒 '+esc(lab(sc.miss[0]))+'만 있으면 돼요</span>';
 else st='<span class="fst sno">'+sc.miss.length+'가지 더 필요해요</span>';
 return '<button type="button" class="fr-card" data-r="'+i+'"><span class="fr-em" style="background:linear-gradient(145deg,'+kc[0]+','+kc[1]+')">'+r.e+'</span><span style="min-width:0;display:block"><span class="n" style="display:block">'+esc(r.n)+'</span><span class="m" style="display:block">'+r.k+' · '+r.m+'분 · 꼭 필요한 재료 '+r.need.length+'개</span>'+st+'</span>'+(S.fav.indexOf(r.n)>=0?'<span class="fr-fav" aria-label="즐겨찾기">♥</span>':'')+'</button>'}
function render(){
 document.querySelectorAll('.fr-chip').forEach(function(b){b.setAttribute('aria-pressed',!!HAVE[b.dataset.i])});
 var hv=Object.keys(HAVE);
 $('pick').innerHTML=hv.length?hv.map(function(x){return '<button type="button" data-rm="'+esc(x)+'" aria-label="'+esc(x)+' 빼기">'+D.ing[x]+' '+esc(x)+'</button>'}).join(''):'<em>아직 고른 재료가 없어요</em>';
 var L=D.r.map(function(r,i){return {r:r,i:i,s:score(r)}}).filter(function(o){return (!FK||o.r.k===FK)&&(!FT||o.r.m<=FT)&&(!FF||S.fav.indexOf(o.r.n)>=0)});
 var ready=L.filter(function(o){return !o.s.miss.length}),one=L.filter(function(o){return o.s.miss.length===1}),rest=L.filter(function(o){return o.s.miss.length>1});
 var nAll=D.r.filter(function(r){return !score(r).miss.length}).length,nOne=D.r.filter(function(r){return score(r).miss.length===1}).length;
 if(hv.length){$('hb').innerHTML='바로 만들 수 있는 요리 <b>'+nAll+'가지</b>';$('hs').textContent='재료 '+hv.length+'개 골랐어요 · 한 가지만 더 있으면 되는 요리도 '+nOne+'가지 있어요.'}
 else{$('hb').textContent='재료를 골라 주세요';$('hs').textContent='아래에서 냉장고에 있는 재료를 눌러요. 기본 양념은 있다고 볼게요.'}
 var srt=function(a,b){return b.s.oh-a.s.oh||a.r.m-b.r.m};ready.sort(srt);one.sort(srt);rest.sort(function(a,b){return a.s.miss.length-b.s.miss.length||b.s.have-a.s.have||a.r.m-b.r.m});
 var h='';
 if(!hv.length){h='<p class="fr-sec">재료가 적게 드는 요리부터 <span>재료를 고르면 맞춰 드려요</span></p><div class="fr-grid">'+L.sort(function(a,b){return a.r.need.length-b.r.need.length||a.r.m-b.r.m}).slice(0,SHOW).map(function(o){return card(o.r,o.i)}).join('')+'</div>'+(L.length>SHOW?'<button type="button" class="fr-more" id="more">요리 더 보기 ('+(L.length-SHOW)+')</button>':'');$('out').innerHTML=h;return}
 h+='<p class="fr-sec">✅ 바로 만들 수 있어요 <span>'+ready.length+'가지</span></p>'+(ready.length?'<div class="fr-grid">'+ready.map(function(o){return card(o.r,o.i)}).join('')+'</div>':'<div class="fr-none">아직 없어요. 재료를 더 골라 보거나 아래 ‘한 가지만 더’를 확인하세요.</div>');
 if(one.length)h+='<p class="fr-sec">🛒 한 가지만 더 있으면 <span>'+one.length+'가지</span></p><div class="fr-grid">'+one.map(function(o){return card(o.r,o.i)}).join('')+'</div>';
 if(rest.length&&SHOW>12)h+='<p class="fr-sec">그 밖의 요리 <span>'+rest.length+'가지</span></p><div class="fr-grid">'+rest.map(function(o){return card(o.r,o.i)}).join('')+'</div>';
 else if(rest.length)h+='<button type="button" class="fr-more" id="more">나머지 요리 '+rest.length+'가지 보기</button>';
 $('out').innerHTML=h}
/* detail */
var CUR=null;
function openR(i){var r=D.r[i],sc=score(r),kc=KC[r.k]||KC['반찬'];CUR=i;
 var ing=r.need.map(function(x){var o=ok(x);return '<span class="'+(o?'h':'x')+'">'+(o?'✓ ':'✗ ')+esc(lab(x))+'</span>'}).join('');
 var op=r.opt.map(function(x){return '<span class="'+(HAVE[x]?'oh':'o')+'">'+(HAVE[x]?'✓ ':'')+esc(x)+'</span>'}).join('');
 var st=r.s.map(function(s,si){return '<li>'+esc(s[0])+(s[1]?' <button type="button" class="fr-tm" data-tm="'+si+'">⏱ '+s[1]+'분</button>':'')+'</li>'}).join('');
 var fv=S.fav.indexOf(r.n)>=0;
 $('dlg').innerHTML='<div class="fr-dh"><span class="fr-em" style="background:linear-gradient(145deg,'+kc[0]+','+kc[1]+')">'+r.e+'</span><div style="min-width:0"><h3 id="dt">'+esc(r.n)+'</h3><p>'+r.k+' · 약 '+r.m+'분 · '+(sc.miss.length?'<b style="color:#C2410C">'+sc.miss.length+'가지 부족</b>':'<b style="color:#1B64DA">재료 다 있어요</b>')+'</p></div><button type="button" class="fr-close" id="dx" aria-label="닫기">×</button></div>'+
  '<div class="fr-db"><p class="fr-lb" style="margin-top:0">꼭 필요한 재료</p><div class="fr-ing">'+ing+'</div>'+(op?'<p class="fr-lb">있으면 더 맛있어요</p><div class="fr-ing">'+op+'</div>':'')+'<p class="fr-note">+ 기본 양념(__BASIC__)</p>'+
  '<p class="fr-lb">만드는 순서</p><ol class="fr-steps">'+st+'</ol>'+
  '<div class="fr-acts"><button type="button" class="fr-b" id="cookgo">👩‍🍳 요리 모드 시작</button><button type="button" class="fr-b s" id="favb">'+(fv?'♥ 즐겨찾기 됨':'♡ 즐겨찾기')+'</button>'+(sc.miss.length?'<button type="button" class="fr-b s" id="cpy">빠진 재료 복사</button>':'')+'</div>'+
  '<p class="fr-note">1~2인분 기준이에요. 불 세기와 냄비 크기에 따라 시간이 달라질 수 있으니 익었는지 꼭 확인하세요.</p></div>';
 var d=$('dlg');if(d.showModal)d.showModal();else d.setAttribute('open','');d.scrollTop=0}
function closeD(){var d=$('dlg');if(d.close)d.close();else d.removeAttribute('open')}
/* cook mode */
var CS=0,TM=null,TL=0,TT=0,WL=null;
function beep(){try{var a=new (window.AudioContext||window.webkitAudioContext)();[0,.35,.7].forEach(function(t){var o=a.createOscillator(),g=a.createGain();o.frequency.value=880;o.connect(g);g.connect(a.destination);g.gain.setValueAtTime(.001,a.currentTime+t);g.gain.exponentialRampToValueAtTime(.3,a.currentTime+t+.02);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+t+.3);o.start(a.currentTime+t);o.stop(a.currentTime+t+.32)})}catch(e){}try{navigator.vibrate&&navigator.vibrate([300,150,300])}catch(e){}}
function fmt(s){s=Math.max(0,Math.ceil(s));return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
function stopT(){clearInterval(TM);TM=null}
function drawT(){$('ck-tv').textContent=fmt(TL);$('ck-rc').setAttribute('stroke-dasharray',(TT?TL/TT*100:100).toFixed(1)+' 100')}
function cstep(){var r=D.r[CUR],s=r.s[CS];stopT();
 $('ck-t').textContent=r.e+' '+r.n;$('ck-n').textContent='STEP '+(CS+1)+' / '+r.s.length;$('ck-s').textContent=s[0];$('ck-p').style.width=((CS+1)/r.s.length*100)+'%';
 var tm=$('ck-tm');tm.classList.remove('done');if(s[1]){tm.hidden=false;TT=TL=s[1]*60;drawT();$('ck-go').textContent='타이머 시작';$('ck-tl').textContent=s[1]+'분 타이머'}else tm.hidden=true;
 $('ck-prev').disabled=CS===0;$('ck-prev').style.opacity=CS===0?.4:1;$('ck-next').textContent=CS===r.s.length-1?'다 됐어요 🎉':'다음 단계'}
function openCook(){closeD();CS=0;$('cook').hidden=false;document.body.style.overflow='hidden';cstep();try{navigator.wakeLock&&navigator.wakeLock.request('screen').then(function(w){WL=w}).catch(function(){})}catch(e){}}
function closeCook(){stopT();$('cook').hidden=true;document.body.style.overflow='';try{WL&&WL.release()}catch(e){}WL=null}
$('ck-go').onclick=function(){if(TM){stopT();this.textContent='계속';return}if(TL<=0)TL=TT;var end=Date.now()+TL*1000;this.textContent='잠깐 멈춤';$('ck-tm').classList.remove('done');
 TM=setInterval(function(){TL=(end-Date.now())/1000;if(TL<=0){TL=0;stopT();drawT();$('ck-go').textContent='다시 시작';$('ck-tm').classList.add('done');beep();toast('⏰ 시간이 다 됐어요!');return}drawT()},250)};
$('ck-rs').onclick=function(){stopT();TL=TT;drawT();$('ck-go').textContent='타이머 시작'};
$('ck-prev').onclick=function(){if(CS>0){CS--;cstep()}};
$('ck-next').onclick=function(){var r=D.r[CUR];if(CS<r.s.length-1){CS++;cstep()}else{closeCook();toast('맛있게 드세요! 🍽️')}};
$('ck-x').onclick=closeCook;
document.addEventListener('keydown',function(e){if($('cook').hidden)return;if(e.key==='Escape')closeCook();if(e.key==='ArrowRight')$('ck-next').click();if(e.key==='ArrowLeft')$('ck-prev').click()});
/* events */
document.addEventListener('click',function(e){var t=e.target.closest?e.target.closest('button'):null;if(!t)return;var d=t.dataset;
 if(d.i){if(HAVE[d.i])delete HAVE[d.i];else HAVE[d.i]=1;save();render();return}
 if(d.rm){delete HAVE[d.rm];save();render();return}
 if(d.qk){d.qk.split(',').forEach(function(x){HAVE[x]=1});save();render();toast('재료를 넣었어요');return}
 if(d.k!==undefined){FK=d.k;FF=0;document.querySelectorAll('#fk button').forEach(function(b){b.setAttribute('aria-pressed',b===t)});render();return}
 if(d.fav){FF=FF?0:1;FK='';document.querySelectorAll('#fk button').forEach(function(b){b.setAttribute('aria-pressed',FF?b===t:b.dataset.k==='')});render();return}
 if(d.t!==undefined){FT=+d.t;document.querySelectorAll('#ft button').forEach(function(b){b.setAttribute('aria-pressed',b===t)});render();return}
 if(d.r!==undefined){openR(+d.r);return}
 if(t.id==='more'){SHOW=999;render();return}
 if(t.id==='dx')return closeD();
 if(t.id==='cookgo')return openCook();
 if(t.id==='favb'){var n=D.r[CUR].n,ix=S.fav.indexOf(n);if(ix>=0)S.fav.splice(ix,1);else S.fav.push(n);save();t.textContent=ix>=0?'♡ 즐겨찾기':'♥ 즐겨찾기 됨';render();return}
 if(t.id==='cpy'){var r=D.r[CUR],m=score(r).miss.map(lab);var txt='장보기: '+m.join(', ')+' ('+r.n+')';(navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){toast('복사했어요: '+m.join(', '))},function(){prompt('복사해 주세요',txt)});return}
 if(d.tm!==undefined){openCook();CS=+d.tm;cstep();return}
 if(t.id==='clr'){if(!Object.keys(HAVE).length)return;HAVE={};save();render();toast('모두 뺐어요');return}});
$('dlg').addEventListener('click',function(e){if(e.target===this)closeD()});
$('q').addEventListener('input',function(){var v=this.value.trim();document.querySelectorAll('.fr-chip').forEach(function(b){b.classList.toggle('hid',!!v&&b.dataset.i.indexOf(v)<0)});document.querySelectorAll('.fr-g').forEach(function(g){g.hidden=!!v&&!g.querySelector('.fr-chip:not(.hid)')})});
render();
})();
</script>
'''
JS = JS.replace('__DATA__', json.dumps(DATA, ensure_ascii=False, separators=(',', ':'))).replace('__BASIC__', BASIC)
out = head + CSS + between + main + JS + tail
dst = os.path.join(ROOT, 'overlay/life/fridge-recipe.html')
open(dst, 'w', encoding='utf-8').write(out)
print(dst, len(out))
