"""Overlay patch for honglife.co.kr: adds 입시·여행 to the top menu and the home page.
Runs in the deploy workflow after the tools bundle is unpacked into _site/."""
import os, sys, re, html
root = sys.argv[1] if len(sys.argv) > 1 else '_site'
OLD = '<a href="/design/">디자인</a>'
NEW = OLD + '<a href="/ipsi/">입시</a><a href="/trip/">여행</a>'
n = 0
for dp, dn, fn in os.walk(root):
    if os.path.relpath(dp, root).split(os.sep)[0] == 'trip':
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        s = open(p, encoding='utf-8').read()
        if OLD in s and '<a href="/trip/">여행</a>' not in s:
            open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW, 1)); n += 1
print('menu patched:', n)

p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
reps = [
 ('<title>홍라이프 도구 | 엑셀 수식·양식, PDF·이미지 변환, 문서 만들기 무료 도구</title>',
  '<title>홍라이프 도구 | 엑셀 수식·양식, PDF·이미지 변환, 입시·여행까지 무료 도구</title>'),
 ('<meta name="description" content="말로 쓰면 엑셀 수식,',
  '<meta name="description" content="엑셀 수식·양식, PDF·이미지 변환에 정시 입시 계산과 출발확정 여행 패키지까지. 말로 쓰면 엑셀 수식,'),
 ('<a href="/ipsi/"><img src="/assets/art/cat2-ipsi.svg" alt="" width="64" height="64"><b>입시</b><em>3개</em></a>',
  '<a href="/ipsi/"><img src="/assets/art/cat2-ipsi.svg" alt="" width="64" height="64"><b>입시</b><em>3개</em></a>'
  '<a href="/trip/"><img src="/assets/art/cat2-trip.svg" alt="" width="64" height="64"><b>여행·패키지</b><em>NEW</em></a>'),
]
for a, b in reps:
    if a in s and b not in s:
        s = s.replace(a, b, 1); print('index:', a[:30])
open(p, 'w', encoding='utf-8').write(s)

p = os.path.join(root, 'sitemap.xml')
s = open(p, encoding='utf-8').read()
if 'honglife.co.kr/trip/' not in s:
    s = s.replace('<url><loc>https://honglife.co.kr/excel/</loc>',
                  '<url><loc>https://honglife.co.kr/trip/</loc><lastmod>2026-11-15</lastmod></url>\n<url><loc>https://honglife.co.kr/excel/</loc>', 1)
    open(p, 'w', encoding='utf-8').write(s); print('sitemap patched')

# Remove the AI travel itinerary tool (/ai/travel-plan.html now redirects to /trip/ via overlay)
LI = re.compile(r'<li><a href="/ai/travel-plan\.html">.*?</a></li>')
JS = re.compile(r'\{"t":"AI로 여행 계획 짜기[^{}]*?"u":"/ai/travel-plan\.html"\}')
LD = re.compile(r',?\{"@type":"WebApplication","name":"AI로 여행 계획 짜기[^{}]*?travel-plan\.html"\}')
TRIP = '{"t":"홍라이프 여행픽 — 출발확정 해외 패키지 특가","d":"쇼츠로 보고 바로 예약하는 출발확정 여행 패키지와 여행 계산기","k":"여행 패키지 특가 출발확정 대마도 후쿠오카 오사카 스페인 해외여행 여행픽","c":"여행","u":"/trip/"}'
for rel in ['index.html', 'ai/index.html', '404.html']:
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read(); o = s
    s = LI.sub('', s)
    s = JS.sub(TRIP, s)
    s = LD.sub('', s)
    if rel == 'index.html':
        s = s.replace('<b>AI 활용</b><em>40개</em>', '<b>AI 활용</b><em>39개</em>')
    if rel == 'ai/index.html':
        s = s.replace('AI 활용 도구 40가지', 'AI 활용 도구 39가지')
    if s != o:
        open(p, 'w', encoding='utf-8').write(s); print('travel-plan removed from', rel)
p = os.path.join(root, 'sitemap.xml')
s = open(p, encoding='utf-8').read()
s2 = re.sub(r'<url><loc>https://honglife\.co\.kr/ai/travel-plan\.html</loc>.*?</url>\n?', '', s)
if s2 != s:
    open(p, 'w', encoding='utf-8').write(s2); print('travel-plan removed from sitemap')

# 2027 편입 도구 (/ipsi/pyeonip-2027.html, overlay) — add to the 입시 hub, home count and sitemap
PY = '/ipsi/pyeonip-2027.html'
LI_PY = ('<li><a href="/ipsi/pyeonip-2027.html"><b>2027 편입 일정·경쟁률·시험과목 (수도권·거점국립대 71곳)</b>'
         '<span>원서접수·필기·합격발표 시기, 필기 과목, 2026 모집인원·경쟁률</span></a></li>')
p = os.path.join(root, 'ipsi', 'index.html')
if os.path.exists(p):
    s = open(p, encoding='utf-8').read()
    if PY not in s.split('<section class="card rel">')[0]:
        s = s.replace('<ul class="tlist">', '<ul class="tlist">' + LI_PY, 1)
        s = re.sub(r'입시 도구 (\d+)가지', lambda m: f'입시 도구 {int(m.group(1)) + 1}가지', s, count=1)
        s = s.replace('"hasPart":[', '"hasPart":[{"@type":"WebApplication","name":"2027 편입 일정·경쟁률·시험과목","url":"https://honglife.co.kr/ipsi/pyeonip-2027.html"},', 1)
        open(p, 'w', encoding='utf-8').write(s); print('ipsi hub: pyeonip added')
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
if 'data-py="1"' not in s:
    s2 = re.sub(r'(<a href="/ipsi/"><img[^>]*><b>입시</b><em>)(\d+)개(</em>)',
                lambda m: f'{m.group(1)}{int(m.group(2)) + 1}개{m.group(3)}', s, count=1)
    if s2 != s:
        s2 = s2.replace('</head>', '<meta name="hl-py" data-py="1">\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(s2); print('home: 입시 count +1')
p = os.path.join(root, 'sitemap.xml')
s = open(p, encoding='utf-8').read()
if 'ipsi/pyeonip-2027.html' not in s:
    s = s.replace('<url><loc>https://honglife.co.kr/trip/</loc>',
                  '<url><loc>https://honglife.co.kr/ipsi/pyeonip-2027.html</loc><lastmod>2026-11-16</lastmod></url>\n<url><loc>https://honglife.co.kr/trip/</loc>', 1)
    open(p, 'w', encoding='utf-8').write(s); print('sitemap: pyeonip added')

# 2027 수능 등급컷·수험표 할인 (/ipsi/suneung-2027.html, overlay) — 입시 허브, 홈 개수, 사이트맵
LI_SN = ('<li><a href="/ipsi/suneung-2027.html"><b>2027 수능 등급컷·예상 백분위 + 수험표 할인</b>'
         '<span>작년 수능 등급컷·누적 비율 비교, 내 점수 등급 보기, 수험표 할인 모음</span></a></li>')
p = os.path.join(root, 'ipsi', 'index.html')
if os.path.exists(p):
    s = open(p, encoding='utf-8').read()
    if '/ipsi/suneung-2027.html' not in s.split('<section class="card rel">')[0]:
        s = s.replace('<ul class="tlist">', '<ul class="tlist">' + LI_SN, 1)
        s = re.sub(r'입시 도구 (\d+)가지', lambda m: f'입시 도구 {int(m.group(1)) + 1}가지', s, count=1)
        s = s.replace('"hasPart":[', '"hasPart":[{"@type":"WebApplication","name":"2027 수능 등급컷·예상 백분위","url":"https://honglife.co.kr/ipsi/suneung-2027.html"},', 1)
        open(p, 'w', encoding='utf-8').write(s); print('ipsi hub: suneung added')
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
if 'data-sn="1"' not in s:
    s2 = re.sub(r'(<a href="/ipsi/"><img[^>]*><b>입시</b><em>)(\d+)개(</em>)',
                lambda m: f'{m.group(1)}{int(m.group(2)) + 1}개{m.group(3)}', s, count=1)
    if s2 != s:
        s2 = s2.replace('</head>', '<meta name="hl-sn" data-sn="1">\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(s2); print('home: 입시 count +1 (sn)')
p = os.path.join(root, 'sitemap.xml')
s = open(p, encoding='utf-8').read()
if 'ipsi/suneung-2027.html' not in s:
    s = s.replace('<url><loc>https://honglife.co.kr/trip/</loc>',
                  '<url><loc>https://honglife.co.kr/ipsi/suneung-2027.html</loc><lastmod>2026-11-19</lastmod></url>\n<url><loc>https://honglife.co.kr/trip/</loc>', 1)
    open(p, 'w', encoding='utf-8').write(s); print('sitemap: suneung added')

# 홈: 상단 흰 배경 + 블루 계열 흐르는 애니메이션(칸 없이 화면 위쪽 전체, 아래로 자연스럽게 사라짐)
#      하단 도구 목록 = 줄마다 큰 색 카드 + 장면 그림(엑셀 창·핸드폰 화면·문서) 카드 가로 줄
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
if 'hl-flow' not in s:
    PAL = ['#FF8A5B', '#4F7CFF', '#2EC4B6', '#FFC94D', '#A06CFF', '#FF5D8F', '#3BB273', '#5BC0EB']
    FEAT = {'excel': '#1F9D55', 'sheet': '#0CA678', 'doc': '#3B5BDB', 'pdf': '#E03131', 'image': '#7048E8', 'convert': '#1098AD',
            'text': '#F08C00', 'ai': '#6741D9', 'calendar': '#F76707', 'qr': '#343A40', 'life': '#2F9E44', 'medical': '#E64980',
            'legal': '#5C6BC0', 'study': '#1C7ED6', 'ipsi': '#364FC7', 'dev': '#212529', 'net': '#1971C2', 'design': '#D6336C', 'shop': '#E8590C', 'pop': '#2563EB'}
    CSS = r"""<style id="hl-flow-css">
body{position:relative}
.hl-flow{position:absolute;left:0;right:0;top:0;height:min(1100px,150vh);overflow:hidden;z-index:0;pointer-events:none;background:#fff;-webkit-mask-image:linear-gradient(#000 50%,transparent);mask-image:linear-gradient(#000 50%,transparent)}
.hl-flow i{position:absolute;display:block;border-radius:50%}
.hl-flow .f1{width:62vw;height:560px;left:-8vw;top:20px;background:radial-gradient(closest-side,rgba(37,99,235,.55),rgba(37,99,235,0));animation:hlf1 20s ease-in-out infinite}
.hl-flow .f2{width:56vw;height:600px;right:-10vw;top:-40px;background:radial-gradient(closest-side,rgba(56,189,248,.6),rgba(56,189,248,0));animation:hlf2 24s ease-in-out infinite}
.hl-flow .f3{width:58vw;height:520px;left:22vw;top:300px;background:radial-gradient(closest-side,rgba(99,102,241,.45),rgba(99,102,241,0));animation:hlf3 28s ease-in-out infinite}
@keyframes hlf1{0%,100%{transform:translate(0,0) rotate(0) scale(1)}25%{transform:translate(14%,10%) rotate(30deg) scale(1.1)}50%{transform:translate(28%,-4%) rotate(70deg) scale(.95)}75%{transform:translate(10%,-8%) rotate(110deg) scale(1.05)}}
@keyframes hlf2{0%,100%{transform:translate(0,0) rotate(0) scale(1)}25%{transform:translate(-14%,14%) rotate(-40deg) scale(1.08)}50%{transform:translate(-30%,6%) rotate(-80deg) scale(.92)}75%{transform:translate(-16%,-6%) rotate(-120deg) scale(1.04)}}
@keyframes hlf3{0%,100%{transform:translate(0,0) rotate(0) scale(1)}33%{transform:translate(-26%,-14%) rotate(50deg) scale(1.1)}66%{transform:translate(22%,-18%) rotate(100deg) scale(.94)}}
.brandbar{position:relative;z-index:2;background:rgba(255,255,255,.55)!important;backdrop-filter:saturate(1.4) blur(10px);-webkit-backdrop-filter:saturate(1.4) blur(10px)}
main.wrap{position:relative;z-index:1}
.hero{background:transparent!important;background-image:none!important;box-shadow:none!important;border:0!important;border-radius:0!important;text-align:center;padding-top:64px!important;padding-bottom:56px!important}
.hero::before{display:none!important}
.hero h1,.hero h1 b{color:#111!important}
.hero p{color:#2b2f36!important;margin-left:auto;margin-right:auto}
.hero .safe{display:inline-flex;background:rgba(255,255,255,.7)!important;color:#1d3f7a!important}
.hero .search{max-width:640px;margin-left:auto;margin-right:auto;background:#fff;box-shadow:0 10px 30px -12px rgba(30,60,140,.35)}
.hero .sres,.hero .note{text-align:left;max-width:640px;margin-left:auto;margin-right:auto}
@media (prefers-reduced-motion:reduce){.hl-flow i{animation:none!important}}
.cats img{filter:saturate(1.6) brightness(1.02)}
ul.hl-cards{display:flex;grid-template-columns:none;gap:14px;overflow-x:auto;scroll-snap-type:x proximity;padding:4px 4px 28px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
ul.hl-cards::-webkit-scrollbar{display:none}
ul.hl-cards>li{flex:0 0 210px;scroll-snap-align:start}
ul.hl-cards a{display:flex!important;flex-direction:column;padding:0!important;overflow:hidden;background:#fff!important;border:0!important;border-radius:18px!important;box-shadow:0 2px 10px rgba(20,30,60,.07)!important;height:100%;transition:transform .2s,box-shadow .2s}
ul.hl-cards a:hover{transform:translateY(-3px);box-shadow:0 10px 24px -8px rgba(20,30,60,.22)!important}
ul.hl-cards .th{display:block;height:146px;flex:0 0 auto;position:relative}
ul.hl-cards .th img{width:100%;height:100%;display:block}
ul.hl-cards .th .pg{position:absolute;left:10px;top:10px;width:30px;height:30px;border-radius:9px;box-shadow:0 2px 6px rgba(0,0,0,.18);filter:saturate(1.6)}
ul.hl-cards a.tx{background:var(--tc)!important;padding:18px 16px!important;justify-content:flex-start}
ul.hl-cards a.tx .pg{width:34px;height:34px;border-radius:0;filter:none;box-shadow:none;background:none}
ul.hl-cards a.tx b{color:#fff!important;font-size:21px!important;line-height:1.3;margin:auto 0 0!important;-webkit-line-clamp:4}
ul.hl-cards a.tx span{color:rgba(255,255,255,.92)!important;margin:8px 0 0!important;font-size:13px!important;-webkit-line-clamp:3}
h2.sec-h .tg{font-size:.82em;font-weight:600;color:#6b7280;letter-spacing:-.02em}
ul.hl-top>li{flex-basis:220px}
ul.hl-top a.tp{background:var(--tc)!important;flex-direction:column-reverse!important;justify-content:flex-end;height:300px}
ul.hl-top a.tp .th{height:auto;flex:1 1 auto;display:flex;align-items:flex-end;margin-top:auto}
ul.hl-top a.tp .th{min-height:0;padding:10px 18px 16px;box-sizing:border-box}
ul.hl-top a.tp .th img{width:100%;height:100%;max-height:150px;object-fit:contain;object-position:center bottom;transform:none}
ul.hl-top a.tp b{order:-1;margin:16px 16px 0;font-size:17px!important;color:#111!important}
ul.hl-top a.tp span{order:0;margin:6px 16px 0!important;color:#333!important}
ul.hl-top a.tp{display:grid!important;grid-template-rows:auto auto 1fr}
ul.hl-top a.tp .th{grid-row:3}
ul.hl-cards li.stk{display:flex;flex-direction:column;gap:12px}
ul.hl-cards a.mn{flex:1 1 0;background:var(--tc)!important;padding:16px!important;justify-content:flex-start}
ul.hl-cards a.mn b{margin:0!important;font-size:15.5px!important}
ul.hl-cards a.mn span{margin:6px 0 0!important}
ul.hl-cards li.stk a.mn:nth-child(2) b,ul.hl-cards li.stk a.mn:nth-child(2) span{color:#fff!important}
ul.hl-cards li.pc a{background:var(--tc)!important}
ul.hl-cards li.pc b,ul.hl-cards li.pt b{margin:16px 16px 0}
ul.hl-cards li.pc span,ul.hl-cards li.pt span{margin:6px 16px 0!important}
ul.hl-cards .pi{display:block;flex:1 1 auto;min-height:150px;background-repeat:no-repeat;background-size:contain;background-position:center bottom;margin-top:10px}
ul.hl-cards li.pt .pi{background-position:center;margin:10px 14px 14px}
ul.hl-cards li.ph:not(.pw) a{background:#fff!important;flex-direction:column-reverse!important;justify-content:flex-end}
ul.hl-cards li.ph:not(.pw) a::after{content:"";display:block;flex:1 1 auto;min-height:160px;background:var(--im) center 20%/cover no-repeat;border-radius:17px 17px 0 0}
ul.hl-cards li.ph:not(.pw) b{order:-1;margin:12px 14px 0!important}
ul.hl-cards li.ph:not(.pw) span{order:-2;margin:4px 14px 14px!important}
ul.hl-cards li.ph b,ul.hl-cards li.ph span{position:relative;z-index:1}
ul.hl-cards li.pw a{background:var(--im) center 30%/cover no-repeat,var(--tc)!important}
ul.hl-cards li.pw a::before{content:"";position:absolute;inset:0 0 auto 0;height:55%;background:linear-gradient(rgba(0,0,0,.55),transparent);border-radius:18px 18px 0 0}
ul.hl-cards li.pw a{position:relative}
ul.hl-cards li.pw b,ul.hl-cards li.pw span{color:#fff!important}
ul.hl-cards li.fp .fi{position:absolute;left:0;right:0;bottom:0;top:96px;height:auto;margin:0;background-size:cover;background-position:center 12%;border-radius:0 0 18px 18px}
ul.hl-cards li.fp .fh{position:relative;z-index:1}
ul.hl-cards li.fp:not(.fd) .fh,ul.hl-cards li.fp:not(.fd) .fh b,ul.hl-cards li.fp:not(.fd) .fh em{color:#111!important}
ul.hl-cards li.fp .go{z-index:2}
ul.hl-cards .th{overflow:hidden}
ul.hl-cards .ft:not(.fp) .fi{position:absolute;left:8px;right:8px;bottom:8px;top:84px;height:auto;margin:0;background-size:contain;background-position:center bottom}
ul.hl-cards .ft:not(.fp) a{overflow:hidden}
ul.hl-cards li.fp .fi{background-position:center 20%!important;background-size:cover!important;background-repeat:no-repeat;border-radius:0 0 18px 18px!important}
ul.hl-cards img.pgb{position:static!important;width:26px!important;height:26px!important;margin:12px 14px 0;box-shadow:none!important;filter:none!important;border-radius:8px}
ul.hl-cards .pg{box-shadow:none!important;filter:none!important}
ul.hl-cards .go,.hl-cw .hl-ar,.hero .search{box-shadow:none!important}
ul.hl-cards a,ul.hl-catrow a.ct{box-shadow:0 8px 20px -12px rgba(16,24,48,.16),0 1px 4px rgba(16,24,48,.04)!important}
ul.hl-cards a:hover{box-shadow:0 12px 26px -12px rgba(16,24,48,.22),0 1px 4px rgba(16,24,48,.05)!important}
ul.hl-cards a:not(.ct){border:1px solid rgba(20,30,60,.08)!important}
.hl-cw .hl-ar{border:1px solid #d9dee7!important}
ul.hl-cards .ft .fi{transition:transform .35s ease}
ul.hl-cards .ft a:hover .fi{transform:scale(1.04)}
ul.hl-cards .ft .fh b{transition:letter-spacing .3s,transform .3s}
ul.hl-cards .ft a:hover .fh b{transform:translateX(3px)}
ul.hl-cards li.ft:not(.fp) a{background:color-mix(in srgb,var(--fc) 70%,#1b2233)!important}
ul.hl-cards a.tx{background:color-mix(in srgb,var(--tc) 82%,#1b2233)!important}
ul.hl-cards li.hl-rv,ul.hl-cards li{opacity:1!important;transform:none!important}
ul.hl-cards b{font-size:15px!important;line-height:1.4;margin:12px 14px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.hl-cards span{font-size:12.5px!important;margin:5px 14px 14px!important;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.hl-cards>li.ft{flex:0 0 300px}
ul.hl-cards .ft a{color:#fff!important;justify-content:space-between;background:var(--fc)!important}
ul.hl-cards .ft .fh{padding:20px 20px 0;margin:0!important;display:block!important;overflow:visible!important;color:#fff!important}
@media (max-width:600px){ul.hl-cards>li.ft{flex-basis:260px}ul.hl-cards>li{flex-basis:190px}}
ul.hl-cards .ft em{color:#fff;font-style:normal;font-size:12px;font-weight:700;opacity:.85;letter-spacing:.02em}
ul.hl-cards .ft b{color:#fff!important;font-size:22px!important;margin:6px 0 0;line-height:1.3;-webkit-line-clamp:3}
ul.hl-cards .ft .fi{display:block;height:200px;background-size:contain;background-repeat:no-repeat;background-position:center bottom;margin:8px 10px 0}
ul.hl-cards .ft .go{position:absolute;right:16px;bottom:14px;width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.92);color:#111;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700}
ul.hl-cards .ft a{position:relative}
.hl-cw{position:relative}
.hl-cw .hl-ar{position:absolute;top:120px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.95);color:#111;font-size:22px;line-height:1;cursor:pointer;box-shadow:0 4px 14px rgba(10,30,60,.18);z-index:2;display:none}
.hl-cw .hl-l{left:-12px}.hl-cw .hl-r{right:-12px}
@media (hover:hover) and (min-width:700px){.hl-cw .hl-ar{display:block}.hl-cw .hl-ar[hidden]{display:none}}
</style>
<script>document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('ul.hl-cards').forEach(function(u){var w=document.createElement('div');w.className='hl-cw';u.parentNode.insertBefore(w,u);w.appendChild(u);var bs=[];[['hl-l','‹',-1],['hl-r','›',1]].forEach(function(a){var b=document.createElement('button');b.type='button';b.className='hl-ar '+a[0];b.textContent=a[1];b.setAttribute('aria-label',a[2]<0?'이전 도구':'다음 도구');b.onclick=function(){u.scrollBy({left:a[2]*u.clientWidth*.8,behavior:'smooth'})};w.appendChild(b);bs.push(b)});function up(){bs[0].hidden=u.scrollLeft<8;bs[1].hidden=u.scrollLeft+u.clientWidth>=u.scrollWidth-8}u.addEventListener('scroll',up,{passive:true});up()})});</script>"""
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = re.sub(r'(<body[^>]*>)', r'\1<div class="hl-flow" aria-hidden="true"><i class="f1"></i><i class="f2"></i><i class="f3"></i></div>', s, count=1)
    a = s.find('<h2 class="sec-h">많이 쓰는 도구'); b = s.find('<section class="card guide"', a)
    if a > 0 and b > a:
        seg = s[a:b]
        cnt = [0, 0, 0]
        TOP = ['#F9C9D9', '#B9D6F2', '#D3C5F3', '#FFE7A3', '#F7C9B5', '#F2763A', '#C1D9F7', '#DCE775', '#6B1E3A', '#F8B4D9', '#9FD8C9', '#FFD6A5']
        def card(m):
            cat = m.group(2); i = cnt[0]; cnt[0] += 1
            sc = f'/assets/art/hl/sc-{cat}.svg'
            if not os.path.exists(os.path.join(root, sc[1:])):
                return m.group(1)
            if i % 5 == 3:
                return m.group(1).replace('<a ', f'<a class="tx" style="--tc:{PAL[(i + 2) % len(PAL)]}" ', 1) + '<img class="pg" src="/assets/art/hl/pgw-' + cat + '.svg" alt="" width="34" height="34" loading="lazy">'
            DK = ['#1E2A4A', '#2B1F3D', '#12352B', '#3A1E24', '#1F3340']
            kind = 'wwvwwdwwvw'[i % 10]
            bgc = '#fff' if kind == 'w' else (PAL[i % len(PAL)] if kind == 'v' else DK[i % len(DK)])
            if cnt[1]:
                return m.group(1).replace('<a ', f'<a class="tp" style="--tc:{TOP[i % len(TOP)]}" ', 1) + f'<i class="th"><img src="{sc.replace("/sc-", "/cs-")}" alt="" width="200" height="140" loading="lazy"></i>'
            return f'{m.group(1)}<i class="th" style="background:{bgc}"><img src="{sc}" alt="" width="200" height="140" loading="lazy"></i><img class="pg pgb" src="/assets/art/hl/pg-{cat}.svg" alt="" width="26" height="26" loading="lazy">'
        def row(m):
            h2, ul = m.group(1), m.group(2)
            mm = re.search(r'id="c-([a-z0-9-]+)"', h2)
            cat = mm.group(1) if mm else 'pop'
            title = re.sub(r'<[^>]+>', '', h2).strip()
            n = ul.count('<li>')
            cnt[1] = 1 if cat == 'pop' else 0
            tag = '가장 많이 찾는 도구부터.' if cat == 'pop' else '바로 만들고, 바로 내려받기.'
            h2 = h2.replace('</h2>', f' <small class="tg">{tag}</small></h2>', 1)
            lis = re.sub(r'(<li><a href="/([a-z0-9-]+)/[^"]*"[^>]*>)', card, ul)
            if cat != 'pop':
                items = re.findall(r'<li>.*?</li>', lis, flags=re.S)
                RAW = re.findall(r'<li><a href="([^"]*)"[^>]*><b>(.*?)</b><span>(.*?)</span></a></li>', ul, flags=re.S)
                if len(items) >= 9 and len(RAW) == len(items):
                    k = sum(map(ord, cat))
                    def mini(r, c):
                        return f'<a class="mn" href="{r[0]}" style="--tc:{c}"><b>{r[1]}</b><span>{r[2]}</span></a>'
                    stack = f'<li class="stk">{mini(RAW[2], ["#FFE066", "#D0BFFF", "#FFD8A8", "#B2F2BB"][k % 4])}{mini(RAW[3], ["#5F3DC4", "#0B7285", "#C2255C", "#1864AB"][k % 4])}</li>'
                    r = RAW[5]
                    ri = cnt[2]; cnt[2] += 1
                    PH = [('p-woman', '#ECB4B9'), ('p-man', '#9DCBDB'), ('p-student', '#EBD793'), ('p-office', '#90C0B1')]
                    if ri % 2 == 0:
                        ph, bc = PH[(ri // 2) % len(PH)]
                        pers = (f'<li class="pc ph"><a href="{r[0]}" style="--tc:{bc};--im:url(/assets/art/ph/{ph}.jpg)"><b>{r[1]}</b><span>{r[2]}</span></a></li>')
                    else:
                        pers = (f'<li class="pc"><a href="{r[0]}" style="--tc:{["#FCC2D7", "#A5D8FF", "#FFEC99", "#C3FAE8"][k % 4]}"><b>{r[1]}</b><span>{r[2]}</span>'
                                f'<i class="pi" style="background-image:url(/assets/art/hl/pp-{k % 4}.svg)"></i></a></li>')
                    r = RAW[7]
                    pic = (f'<li class="pt"><a href="{r[0]}"><b>{r[1]}</b><span>{r[2]}</span>'
                           f'<i class="pi" style="background-image:url(/assets/art/hl/picto.svg)"></i></a></li>')
                    items = items[:2] + [stack] + items[4:5] + [pers] + items[6:7] + [pic] + items[8:]
                    BIG = {'sheet': ('phone-green', '#038E45'), 'calendar': ('phone-dark', '#202425')}
                    if cat in BIG and len(RAW) > 9:
                        r = RAW[9]; ph, bc = BIG[cat]
                        big = f'<li class="pc ph pw"><a href="{r[0]}" style="--tc:{bc};--im:url(/assets/art/ph/{ph}.jpg)"><b>{r[1]}</b><span>{r[2]}</span></a></li>'
                        items = items[:7] + [big] + items[8:]
                    lis = '<ul class="tlist">' + ''.join(items) + '</ul>'
            href = f'/{cat}/' if cat != 'pop' else '/#search'
            img = f'/assets/art/hl/ft-{cat}.svg'
            sub = f'도구 {n}가지' if cat != 'pop' else '자주 찾는 도구'
            FTPH = {'image': ('p-woman', '#ECB4B9'), 'text': ('p-man', '#9DCBDB'), 'study': ('p-student', '#EBD793'),
                    'doc': ('p-office', '#90C0B1'), 'calendar': ('phone-dark', '#202425'), 'sheet': ('phone-green', '#038E45')}
            if cat in FTPH:
                ph, bc = FTPH[cat]
                dark = cat in ('calendar', 'sheet')
                ft = (f'<li class="ft fp{" fd" if dark else ""}"><a href="{href}" style="--fc:{bc}"><span class="fh"><em>{sub}</em><b>{title}</b></span>'
                      f'<i class="fi" style="background-image:url(/assets/art/ph/{ph}.jpg)"></i><span class="go" aria-hidden="true">›</span></a></li>')
            else:
                ft = (f'<li class="ft"><a href="{href}" style="--fc:{FEAT.get(cat, "#2563EB")}"><span class="fh"><em>{sub}</em><b>{title}</b></span>'
                      f'<i class="fi" style="background-image:url({img})"></i><span class="go" aria-hidden="true">›</span></a></li>')
            if cat == 'pop':
                return h2 + lis.replace('<ul class="tlist">', '<ul class="tlist hl-cards hl-top">', 1)
            return h2 + lis.replace('<ul class="tlist">', '<ul class="tlist hl-cards">' + ft, 1)
        seg = re.sub(r'(<h2 class="sec-h"[^>]*>.*?</h2>)(<ul class="tlist">.*?</ul>)', row, seg, flags=re.S)
        s = s[:a] + seg + s[b:]
    open(p, 'w', encoding='utf-8').write(s); print('home: flow hero + tool cards')

# 2026-11-28: 상단/하단 카테고리 12개로 통합(사용자 요청). 접힌 카테고리는 FOLD로 부모에 귀속, URL은 모두 유지. 여행(trip)은 제외.
CATBAR = [('excel', '엑셀'), ('pdf', '한글·PDF'), ('doc', '문서·양식'), ('image', '이미지·디자인'), ('convert', '파일 변환'), ('ai', 'AI'),
          ('life', '생활'), ('gov', '공문서·민원'), ('drive', '자동차·내비'), ('medical', '건강'), ('ipsi', '시험·공부'), ('dev', '개발·인터넷')]
FOLD = {'sheet': 'excel', 'text': 'convert', 'calendar': 'life', 'qr': 'image', 'design': 'image',
        'driver': 'drive', 'legal': 'ipsi', 'study': 'ipsi', 'test': 'life', 'game': 'life', 'shop': 'life', 'net': 'dev'}
CANON_RENAME = {'/excel/': '엑셀', '/pdf/': '한글·PDF', '/doc/': '문서·양식', '/image/': '이미지·디자인',
                '/drive/': '자동차·내비', '/ipsi/': '시험·공부', '/dev/': '개발·인터넷', '/life/': '생활'}

# 홈: '분류별로 찾기'를 면 분할 색 카드(큰 장면 그림) 가로 줄로 — 12개 통합 카테고리로
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
if 'hl-catrow-css' not in s:
    FC = {'excel': '#1F9D55', 'sheet': '#0CA678', 'doc': '#3B5BDB', 'pdf': '#E03131', 'image': '#7048E8', 'convert': '#1098AD',
          'text': '#F08C00', 'ai': '#6741D9', 'calendar': '#F76707', 'qr': '#495057', 'life': '#2F9E44', 'medical': '#E64980',
          'legal': '#5C6BC0', 'study': '#1C7ED6', 'ipsi': '#364FC7', 'dev': '#343A40', 'net': '#1971C2', 'design': '#D6336C', 'shop': '#E8590C', 'trip': '#1C7ED6', 'gov': '#0B7285', 'drive': '#E8590C'}
    def mix(c, t):
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        return '#%02X%02X%02X' % tuple(round(v + (255 - v) * t) for v in (r, g, b))
    m = re.search(r'<div class="cats">(.*?)</div>', s, flags=re.S)
    if m:
        import glob as _glob
        _cnt = {}
        for _mm in re.finditer(r'<a href="/([a-z0-9-]+)/"><img[^>]*><b>.*?</b><em>(.*?)</em></a>', m.group(1)):
            _sl, _em = _mm.groups(); _num = re.search(r'\d+', _em)
            _cnt[_sl] = int(_num.group()) if _num else 0
        for _ex in ('gov', 'drive', 'driver'):  # .cats에 없는 분류는 실제 파일 수로 집계
            if _ex not in _cnt:
                _cnt[_ex] = len(_glob.glob(os.path.join(root, _ex, '*.html')))
        out = []
        for i, (cat, name) in enumerate(CATBAR):
            tot = _cnt.get(cat, 0) + sum(_cnt.get(_k, 0) for _k, _pp in FOLD.items() if _pp == cat)
            n = (str(tot) + '개') if tot else ''
            c = FC.get(cat, '#2563EB')
            a, b, d = mix(c, .80), mix(c, .45), mix(c, .62)
            v = i % 3
            if v == 0:
                bg = f'linear-gradient({a} 0 40%,{b} 40%)'
            elif v == 1:
                bg = f'linear-gradient({a} 0 40%,transparent 40%),linear-gradient(90deg,{d} 0 36%,{b} 36%)'
            else:
                bg = f'linear-gradient({a} 0 40%,transparent 40%),linear-gradient(90deg,{b} 0 58%,{d} 58%)'
            img = f'/assets/art/hl/cs-{cat}.svg'
            out.append(f'<li><a class="ct" href="/{cat}/" style="--bg:{bg}"><span class="ch"><em>{n}</em><b>{name}</b></span>'
                       f'<i class="ci" style="background-image:url({img})"></i><span class="go" aria-hidden="true">›</span></a></li>')
        s = s.replace(m.group(0), '<ul class="tlist hl-cards hl-catrow">' + ''.join(out) + '</ul>', 1)
        CSS = """<style id="hl-catrow-css">
ul.hl-catrow>li{flex:0 0 224px}
ul.hl-catrow a.ct{position:relative;height:300px;background:var(--bg)!important;border-radius:20px!important;box-shadow:0 8px 20px -12px rgba(16,24,48,.16),0 1px 4px rgba(16,24,48,.04)!important}
ul.hl-catrow a.ct .ch{display:block!important;margin:0!important;padding:18px 18px 0;-webkit-line-clamp:unset;overflow:visible!important}
ul.hl-catrow a.ct em{display:block;font-style:normal;font-size:12px;font-weight:700;color:#333}
ul.hl-catrow a.ct b{margin:4px 0 0!important;font-size:19px!important;color:#111!important;line-height:1.3}
ul.hl-catrow a.ct .ci{position:absolute;top:40%;bottom:16px;left:16px;right:16px;height:auto;background-repeat:no-repeat;background-size:contain;background-position:center top;transition:transform .3s}
ul.hl-catrow a.ct:hover .ci{transform:scale(1.04);transform-origin:center top}
ul.hl-catrow a.ct .go{position:absolute;right:12px;bottom:12px;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.95);color:#111;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;margin:0!important}
@media (max-width:600px){ul.hl-catrow>li{flex-basis:200px}ul.hl-catrow a.ct{height:270px}}
</style>"""
        s = s.replace('</head>', CSS + '\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(s); print('home: category row cards')

# 분류 허브 페이지(/excel/ 등): 홈과 같은 느낌 — 흐르는 배경, 가운데 제목, 그림 카드 그리드(흰 카드 70%), 다른 분류 그림 카드 줄
HPAL = ['#FFD6A5', '#C9DCFF', '#D7C8FF', '#BFEBD8', '#FFC9D6', '#FFE89A']
HDK = ['#1E2A4A', '#2B1F3D', '#12352B', '#3A1E24', '#1F3340']
HFC = {'test': '#B14FC5', 'game': '#7FA21B', 'excel': '#1F9D55', 'sheet': '#0CA678', 'doc': '#3B5BDB', 'pdf': '#E03131', 'image': '#7048E8', 'convert': '#1098AD',
       'text': '#F08C00', 'ai': '#6741D9', 'calendar': '#F76707', 'qr': '#495057', 'life': '#2F9E44', 'medical': '#E64980',
       'legal': '#5C6BC0', 'study': '#1C7ED6', 'ipsi': '#364FC7', 'dev': '#343A40', 'net': '#1971C2', 'design': '#D6336C', 'shop': '#E8590C', 'trip': '#1C7ED6', 'gov': '#0B7285', 'drive': '#E8590C'}
KW = [('printer', r'드라이버'), ('bus', r'노선 내비|경유지|셔틀'), ('navup2', r'(기아|쉐보레|KGM).*(업데이트|업그레이드)'), ('navup3', r'(제네시스|르노|아이나비).*(업데이트|업그레이드)'), ('navup', r'내비게이션 업데이트|내비게이션 지도 업데이트|내비 업데이트|지도 업그레이드|업데이트 모음|openR'), ('rest', r'휴게소'), ('park', r'주차장'), ('ev', r'충전소'), ('fuel', r'주유소'), ('mid', r'중간지점'), ('taxi', r'택시비|통행료'), ('pdf', r'PDF'), ('image', r'이미지|사진|PNG|JPG|증명'), ('qr', r'QR|바코드'), ('ai', r'AI|챗GPT|클로드|프롬프트'),
      ('calendar', r'달력|D-day|날짜|공휴일|요일'), ('sheet', r'차트|그래프|가계부|근무표'), ('excel', r'엑셀|수식|CSV'),
      ('dev', r'JSON|코드|정규식|Base64|HTML'), ('doc', r'계약서|견적서|이력서|서식|영수증'), ('text', r'글자|텍스트|맞춤법')]
HUBCSS = """<style id="hl-hub-css">
body{position:relative}
.hl-flow{position:absolute;left:0;right:0;top:0;height:min(900px,130vh);overflow:hidden;z-index:0;pointer-events:none;background:#fff;-webkit-mask-image:linear-gradient(#000 50%,transparent);mask-image:linear-gradient(#000 50%,transparent)}
.hl-flow i{position:absolute;display:block;border-radius:50%}
.hl-flow .f1{width:62vw;height:520px;left:-8vw;top:10px;background:radial-gradient(closest-side,rgba(37,99,235,.5),rgba(37,99,235,0));animation:hlf1 20s ease-in-out infinite}
.hl-flow .f2{width:56vw;height:560px;right:-10vw;top:-40px;background:radial-gradient(closest-side,rgba(56,189,248,.55),rgba(56,189,248,0));animation:hlf2 24s ease-in-out infinite}
.hl-flow .f3{width:58vw;height:480px;left:22vw;top:260px;background:radial-gradient(closest-side,rgba(99,102,241,.4),rgba(99,102,241,0));animation:hlf3 28s ease-in-out infinite}
@keyframes hlf1{0%,100%{transform:translate(0,0) rotate(0) scale(1)}25%{transform:translate(14%,10%) rotate(30deg) scale(1.1)}50%{transform:translate(28%,-4%) rotate(70deg) scale(.95)}75%{transform:translate(10%,-8%) rotate(110deg) scale(1.05)}}
@keyframes hlf2{0%,100%{transform:translate(0,0) rotate(0) scale(1)}25%{transform:translate(-14%,14%) rotate(-40deg) scale(1.08)}50%{transform:translate(-30%,6%) rotate(-80deg) scale(.92)}75%{transform:translate(-16%,-6%) rotate(-120deg) scale(1.04)}}
@keyframes hlf3{0%,100%{transform:translate(0,0) rotate(0) scale(1)}33%{transform:translate(-26%,-14%) rotate(50deg) scale(1.1)}66%{transform:translate(22%,-18%) rotate(100deg) scale(.94)}}
@media (prefers-reduced-motion:reduce){.hl-flow i{animation:none!important}}
.brandbar{position:relative;z-index:2;background:rgba(255,255,255,.55)!important;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
main.wrap{position:relative;z-index:1}
header.top.hub{background:transparent!important;box-shadow:none!important;border:0!important;text-align:center;padding:48px 0 40px!important}
header.top.hub h1{font-size:clamp(30px,5vw,46px)}
header.top.hub .lead{max-width:720px;margin-left:auto;margin-right:auto}
header.top.hub .safe{display:inline-flex;background:rgba(255,255,255,.7)!important}
main section.card{background:transparent!important;box-shadow:none!important;border:0!important;padding:0!important;margin:0 0 40px}
main section.card>h2{font-size:22px;margin:0 0 16px}
ul.hl-grid{display:grid!important;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;padding:0;margin:0;list-style:none}
ul.hl-grid>li{margin:0;min-width:0}
ul.hl-grid>li>a{display:flex!important;flex-direction:column;height:100%;padding:0!important;overflow:hidden;background:#fff!important;border:1px solid rgba(20,30,60,.08)!important;border-radius:18px!important;color:#111;text-decoration:none;box-shadow:0 8px 20px -12px rgba(16,24,48,.16),0 1px 4px rgba(16,24,48,.04)!important;transition:transform .2s,box-shadow .2s}
ul.hl-grid>li>a:hover{transform:translateY(-3px);box-shadow:0 12px 26px -12px rgba(16,24,48,.22),0 1px 4px rgba(16,24,48,.05)!important}
ul.hl-grid .th{display:flex;align-items:center;justify-content:center;height:140px;flex:0 0 auto;padding:18px 22px 0;box-sizing:border-box;background:#F3F5F9}
ul.hl-grid .th img{width:100%;height:100%;object-fit:contain;object-position:center bottom}
ul.hl-grid .pg{width:26px;height:26px;margin:12px 14px 0}
ul.hl-grid b{font-size:15px!important;line-height:1.4;margin:8px 14px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.hl-grid span{font-size:12.5px!important;color:#5b6270;margin:5px 14px 14px!important;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.hl-grid li.v>a{background:var(--tc)!important;border-color:transparent!important}
ul.hl-grid li.v .th{background:transparent}
ul.hl-grid li.d>a{background:var(--tc)!important;border-color:transparent!important;color:#fff}
ul.hl-grid li.d .th{background:rgba(255,255,255,.06)}
ul.hl-grid li.d b{color:#fff!important}ul.hl-grid li.d span{color:rgba(255,255,255,.8)!important}
ul.hl-grid li.ft{grid-column:1/-1}
ul.hl-grid li.ft>a{flex-direction:row!important;align-items:stretch;min-height:220px!important}
ul.hl-grid li.ft .fh2{font-style:normal;flex:1 1 50%;display:flex;flex-direction:column;justify-content:center;padding:10px 0}
ul.hl-grid li.ft .fi{flex:1 1 50%!important;margin:16px 24px!important}
ul.hl-grid li.ft>a{background:color-mix(in srgb,var(--tc) 70%,#1b2233)!important;color:#fff;position:relative;min-height:290px;border-color:transparent!important}
ul.hl-grid li.ft em{display:block;font-style:normal;font-size:12px;font-weight:700;margin:20px 20px 0;opacity:.85}
ul.hl-grid li.ft b{color:#fff!important;font-size:22px!important;margin:6px 20px 0}
ul.hl-grid li.ft span{color:rgba(255,255,255,.85)!important;margin:6px 20px 0!important}
ul.hl-grid li.ft .fi{flex:1 1 auto;min-height:150px;margin:8px 20px 16px;background-repeat:no-repeat;background-size:contain;background-position:center bottom}
@media (max-width:600px){ul.hl-grid li.ft>a{flex-direction:column!important}ul.hl-grid{grid-template-columns:1fr 1fr;gap:10px}ul.hl-grid .th{height:110px;padding:12px 14px 0}ul.hl-grid li.ft{grid-column:1/-1}}
section.rel ul.hl-rel{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px;padding:4px 0 24px;margin:0;list-style:none}
section.rel ul.hl-rel::-webkit-scrollbar{display:none}
ul.hl-rel>li{margin:0;min-width:0}
ul.hl-rel a{display:block!important;position:relative;aspect-ratio:1/1;height:auto;border-radius:18px!important;overflow:hidden;background:var(--bg)!important;color:#111;text-decoration:none;padding:0!important;border:0!important;box-shadow:0 8px 20px -12px rgba(16,24,48,.16),0 1px 4px rgba(16,24,48,.04)!important}
ul.hl-rel a b{display:block;padding:16px 16px 0;font-size:16px!important;line-height:1.3;color:#111!important}
ul.hl-rel a span{display:none!important;padding:4px 16px 0;font-size:12px!important;color:#333!important;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.hl-rel a i{position:absolute;left:14px;right:14px;top:34%;bottom:14px;background-repeat:no-repeat;background-size:contain;background-position:center top}
@media (max-width:900px){section.rel ul.hl-rel{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:10px!important}
ul.hl-rel a{border-radius:14px!important}
ul.hl-rel a b{padding:9px 9px 0!important;font-size:12px!important;line-height:1.25!important;word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
ul.hl-rel a i{left:8px!important;right:8px!important;top:34%!important;bottom:8px!important}}
</style>"""
def _mix(c, t):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    return '#%02X%02X%02X' % tuple(round(v + (255 - v) * t) for v in (r, g, b))
for base, cat in [('', c) for c in sorted(os.listdir(root))] + ([('en', c) for c in sorted(os.listdir(os.path.join(root, 'en')))] if os.path.isdir(os.path.join(root, 'en')) else []):
    p = os.path.join(root, base, cat, 'index.html')
    pre = '/en' if base else ''
    if not os.path.isfile(p) or cat not in HFC:
        continue
    s = open(p, encoding='utf-8').read()
    if 'class="top hub"' not in s or 'hl-hub-css' in s:
        continue
    s = s.replace('</head>', HUBCSS + '\n</head>', 1)
    s = re.sub(r'(<body[^>]*>)', r'\1<div class="hl-flow" aria-hidden="true"><i class="f1"></i><i class="f2"></i><i class="f3"></i></div>', s, count=1)
    first = [True]
    def conv_ul(m):
        items = re.findall(r'<li><a href="([^"]*)"[^>]*><b>(.*?)</b><span>(.*?)</span></a></li>', m.group(1), flags=re.S)
        if not items:
            return m.group(0)
        out = []
        for i, (href, b, sp) in enumerate(items):
            sc = cat
            for k, rx in KW:
                if re.search(rx, b):
                    sc = k
                    break
            if not os.path.exists(os.path.join(root, 'assets/art/hl', f'cs-{sc}.svg')):
                sc = cat
            ALT = {'excel': 'sheet', 'sheet': 'excel', 'doc': 'pdf', 'pdf': 'doc', 'image': 'convert', 'convert': 'doc', 'text': 'doc', 'calendar': 'life'}
            if sc == cat and i % 3 == 1 and ALT.get(cat):
                sc = ALT[cat]
            if False:
                out.append(f'<li class="ft"><a href="{href}" style="--tc:{HFC[cat]}"><i class="fh2"><em>추천 도구</em><b>{b}</b><span>{sp}</span></i>'
                           f'<i class="fi" style="background-image:url(/assets/art/hl/ft-{cat}.svg)"></i></a></li>')
                continue
            kind = 'wwvwwdwwvw'[i % 10]
            if kind == 'w':
                out.append(f'<li><a href="{href}"><i class="th"><img src="/assets/art/hl/cs-{sc}.svg" alt="" width="200" height="140" loading="lazy"></i>'
                           f'<img class="pg" src="/assets/art/hl/pg-{cat}.svg" alt="" width="26" height="26" loading="lazy"><b>{b}</b><span>{sp}</span></a></li>')
            else:
                tc = HPAL[i % len(HPAL)] if kind == 'v' else HDK[i % len(HDK)]
                pg = 'pg' if kind == 'v' else 'pgw'
                out.append(f'<li class="{kind}"><a href="{href}" style="--tc:{tc}"><i class="th"><img src="/assets/art/hl/cs-{sc}.svg" alt="" width="200" height="140" loading="lazy"></i>'
                           f'<img class="pg" src="/assets/art/hl/{pg}-{cat}.svg" alt="" width="26" height="26" loading="lazy"><b>{b}</b><span>{sp}</span></a></li>')
        if first[0] and out and out[0].startswith('<li class="ft"'):
            out = out[1:] + [out[0]]
        first[0] = False
        return '<ul class="tlist hl-grid">' + ''.join(out) + '</ul>'
    s = re.sub(r'<ul class="tlist">(.*?)</ul>', conv_ul, s, flags=re.S)
    def conv_rel2(m):
        items = re.findall(r'<li><a href="/(?:en/)?([a-z0-9-]+)/"><b>(.*?)</b><span>(.*?)</span></a></li>', m.group(2))
        out = []
        for c2, b, sp in items:
            c = HFC.get(c2, '#2563EB'); a, bb = _mix(c, .80), _mix(c, .45)
            img = f'/assets/art/hl/cs-{c2}.svg' if os.path.exists(os.path.join(root, 'assets/art/hl', f'cs-{c2}.svg')) else ''
            out.append(f'<li><a href="{pre}/{c2}/" style="--bg:linear-gradient({a} 0 34%,{bb} 34%)"><b>{b}</b><span>{sp}</span>'
                       + (f'<i style="background-image:url({img})"></i>' if img else '') + '</a></li>')
        return f'<section class="card rel"><h2>{m.group(1)}</h2><ul class="hl-rel">' + ''.join(out) + '</ul></section>'
    s = re.sub(r'<section class="card rel"><h2>(다른 분류|Other categories)</h2><ul>(.*?)</ul></section>', conv_rel2, s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)
print('hub pages styled')


# 영문 홈(/en/)에도 같은 홈 디자인 적용 — 위 한국어 홈 블록을 영문 문구로 바꿔 한 번 더 실행
if os.path.isfile(os.path.join(root, 'en', 'index.html')):
    _src = open(__file__, encoding='utf-8').read()
    _a = _src.index('# 홈: 상단 흰 배경'); _b = _src.index('# 분류 허브 페이지')
    _blk = _src[_a:_b]
    for _x, _y in [("os.path.join(root, 'index.html')", "os.path.join(root, 'en', 'index.html')"),
                   ('<h2 class="sec-h">많이 쓰는 도구', '<h2 class="sec-h">Popular tools'),
                   ('<li><a href="/([a-z0-9-]+)/[^"]*"[^>]*>)', '<li><a href="/en/([a-z0-9-]+)/[^"]*"[^>]*>)'),
                   ("f'/{cat}/' if cat != 'pop' else '/#search'", "f'/en/{cat}/' if cat != 'pop' else '/en/#search'"),
                   ("f'도구 {n}가지'", "f'{n} tools'"), ("'자주 찾는 도구'", "'Most used'"),
                   ("'가장 많이 찾는 도구부터.'", "'Start with the favorites.'"), ("'바로 만들고, 바로 내려받기.'", "'Make it, download it, done.'"),
                   ('<a href="/([a-z0-9-]+)/"><img', '<a href="/en/([a-z0-9-]+)/"><img'),
                   ('href="/{cat}/" style="--bg:{bg}"', 'href="/en/{cat}/" style="--bg:{bg}"'),
                   ("'이전 도구'", "'Previous'"), ("'다음 도구'", "'Next'")]:
        _blk = _blk.replace(_x, _y)
    exec(_blk)

# ── 새 분류: 심리 테스트(/test/) · 게임 계산기(/game/) (overlay, 2026-11-18) ──
import json as _json
_nc_p = os.path.join(root, 'newcats.json')
if os.path.exists(_nc_p):
    NC = _json.load(open(_nc_p, encoding='utf-8')); os.remove(_nc_p)
    A, B = '<a href="/trip/">여행</a>', '<a href="/trip/">여행</a><a href="/test/">테스트</a><a href="/game/">게임</a>'
    k = 0
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith('.html'):
                p = os.path.join(dp, f); s = open(p, encoding='utf-8').read()
                if A in s and '<a href="/test/">테스트</a>' not in s:
                    open(p, 'w', encoding='utf-8').write(s.replace(A, B, 1)); k += 1
    print('menu +test/game:', k)
    p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
    m = re.search(r'<li><a class="ct" href="/ipsi/".*?</a></li>', s, flags=re.S)
    if m and 'href="/test/"' not in s[m.end():m.end() + 2000]:
        def ct(href, n, name, art, c1, c2, c3):
            return (f'<li><a class="ct" href="{href}" style="--bg:linear-gradient({c1} 0 40%,transparent 40%),linear-gradient(90deg,{c2} 0 58%,{c3} 58%)">'
                    f'<span class="ch"><em>{n}개</em><b>{name}</b></span><i class="ci" style="background-image:url(/assets/art/hl/cs-{art}.svg)"></i><span class="go" aria-hidden="true">›</span></a></li>')
        add = ct('/test/', len(NC['test']), '심리 테스트', 'test', '#EFDDF3', '#C98ED6', '#DDB6E6') + ct('/game/', len(NC['game']), '게임 계산기', 'game', '#E9F2CF', '#A8C64A', '#C6DB86')
        s = s[:m.end()] + add + s[m.end():]; print('home: test/game cards')
    entries = [_json.dumps({"t": n, "d": d, "k": kw, "c": "심리 테스트" if c == 'test' else "게임 계산기", "u": u}, ensure_ascii=False, separators=(',', ':')) for c in ('test', 'game') for u, n, d, kw in NC[c]]
    if TRIP in s and '"u":"/test/' not in s:
        s = s.replace(TRIP, TRIP + ',' + ','.join(entries), 1); print('search index +', len(entries))
    open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    if 'honglife.co.kr/test/' not in s:
        urls = ['/test/', '/game/'] + [u for c in ('test', 'game') for u, *_ in NC[c]]
        s = s.replace('</urlset>', ''.join(f'<url><loc>https://honglife.co.kr{u}</loc><lastmod>2026-11-18</lastmod></url>\n' for u in urls) + '</urlset>', 1)
        open(p, 'w', encoding='utf-8').write(s); print('sitemap +', len(urls))

# ── 아티팩트에서 옮긴 페이지: 자격증 시험달력(/calendar/exam-schedule.html), 청약·줍줍+투자계산기(/life/invest.html) ──
MOVED = [('driver', '/driver/', '드라이버 다운로드 모음', '프린터·복합기 드라이버를 회사별로, 설치 순서 그림', '드라이버 다운로드 프린터 드라이버 복합기 드라이버 드라이버 설치 방법 CD 없이 프린터 설치', '드라이버'),
         ('driver', '/driver/hp.html', 'HP 프린터 드라이버 다운로드 (삼성 프린터 포함)', '공식 사이트에서 받기 + 설치 6단계 그림', 'HP 프린터 드라이버 HP 드라이버 다운로드 삼성 프린터 드라이버 HP 복합기 드라이버 HP Smart', '드라이버'),
         ('driver', '/driver/nvidia.html', '엔비디아 그래픽 드라이버 다운로드', 'Game Ready·Studio, NVIDIA App 자동 업데이트', '엔비디아 드라이버 NVIDIA 드라이버 지포스 드라이버 그래픽 드라이버 RTX 드라이버 Game Ready Studio NVIDIA App', '드라이버'),
         ('driver', '/driver/amd.html', 'AMD 라데온·라이젠 칩셋 드라이버 다운로드', 'Auto-Detect 자동 감지 설치, 제품별 바로가기', 'AMD 드라이버 라데온 드라이버 Radeon 드라이버 라이젠 칩셋 드라이버 Adrenalin', '드라이버'),
         ('driver', '/driver/intel.html', '인텔 드라이버 다운로드 (지원 도우미)', '그래픽·칩셋·무선랜 한 번에 업데이트', '인텔 드라이버 인텔 그래픽 드라이버 인텔 드라이버 및 지원 도우미 인텔 무선랜 드라이버', '드라이버'),
         ('driver', '/driver/sindoh.html', '신도리코 드라이버 다운로드 (모델별 바로가기)', 'D452·D472·N502 등 모델별 공식 다운로드', '신도리코 드라이버 신도리코 복합기 드라이버 sindoh Connect D452 D472 D450 N502 빠른 설치 드라이버', '드라이버'),
         ('driver', '/driver/epson.html', '엡손 프린터 드라이버 다운로드 (모델별 바로 받기)', 'L3250·L3210·L6290 등 394개 모델 공식 다운로드', '엡손 드라이버 엡손 프린터 드라이버 Epson 드라이버 L3250 드라이버 L3210 드라이버 L3110 드라이버 정품무한 드라이버 Epson Scan 2', '드라이버'),
         ('driver', '/driver/brother.html', '브라더 프린터 드라이버 다운로드 (모델별 바로 받기)', 'DCP-T720DW·MFC-L2700D 등 모델별 공식 다운로드', '브라더 드라이버 브라더 프린터 드라이버 Brother 드라이버 DCP-T720DW 드라이버 MFC-L2700D 드라이버 HL-L2321D iPrint&Scan', '드라이버'),
         ('driver', '/driver/lg.html', 'LG 그램·모니터 드라이버 다운로드', 'LG Update·OnScreen Control 바로 받기, 모델별 파일', 'LG 드라이버 그램 드라이버 LG Update LG 노트북 드라이버 LG 모니터 드라이버 OnScreen Control 17Z90S 16Z90R', '드라이버'),
         ('driver', '/driver/apple.html', '애플 드라이버·아이폰 PC 연결', 'Apple 기기 앱·iCloud·iTunes·Boot Camp', '아이폰 드라이버 아이폰 PC 연결 아이폰 인식 안됨 Apple 기기 앱 아이튠즈 iCloud for Windows 부트캠프 드라이버 Boot Camp', '드라이버'),
         ('driver', '/driver/surface.html', '서피스 드라이버·펌웨어 다운로드', 'Surface Pro·Laptop·Go 모델별 바로 받기', '서피스 드라이버 Surface 드라이버 서피스 펌웨어 Surface Pro 9 드라이버 Surface Laptop 드라이버 Surface Go 드라이버 마이크로소프트 드라이버', '드라이버'),
         ('driver', '/driver/lenovo.html', '레노버 드라이버 다운로드', 'ThinkPad·IdeaPad·Legion 공식 업데이트 프로그램', '레노버 드라이버 Lenovo 드라이버 씽크패드 드라이버 ThinkPad 드라이버 아이디어패드 드라이버 Lenovo Vantage System Update', '드라이버'),
         ('driver', '/driver/dell.html', '델 드라이버 다운로드', 'Inspiron·XPS·Latitude 공식 업데이트 프로그램', '델 드라이버 Dell 드라이버 델 노트북 드라이버 Inspiron 드라이버 XPS 드라이버 SupportAssist 서비스 태그', '드라이버'),
         ('driver', '/driver/asus.html', '에이수스 드라이버 다운로드', 'Vivobook·Zenbook·ROG·메인보드 공식 업데이트 프로그램', '에이수스 드라이버 ASUS 드라이버 아수스 드라이버 MyASUS 젠북 드라이버 비보북 드라이버 ROG 드라이버 메인보드 드라이버', '드라이버'),
         ('driver', '/driver/acer.html', '에이서 드라이버 다운로드', 'Aspire·Swift·Nitro 공식 업데이트 프로그램', '에이서 드라이버 Acer 드라이버 에이서 노트북 드라이버 Aspire 드라이버 Swift 드라이버 Nitro 드라이버 Predator 드라이버', '드라이버'),
         ('driver', '/driver/roborock.html', '로보락 펌웨어 업데이트 방법', 'Roborock 앱·와이파이 연결·로봇청소기', '로보락 업데이트 로보락 펌웨어 업데이트 로보락 앱 로봇청소기 업데이트 로보락 와이파이 연결 안됨 S8 Qrevo Saros', '드라이버'),
         ('driver', '/driver/samsung.html', '삼성 드라이버 다운로드', '갤럭시 북·모니터·USB·SSD·프린터', '삼성 드라이버 삼성 노트북 드라이버 갤럭시북 드라이버 디바이스 케어 Samsung Update 삼성 모니터 드라이버 갤럭시 USB 드라이버 삼성 SSD 매지션 Magician 삼성 프린터 드라이버', '드라이버'),
         ('driver', '/driver/ecovacs.html', '에코백스 펌웨어 업데이트 방법', 'ECOVACS HOME 앱·로봇청소기', '에코백스 업데이트 에코백스 펌웨어 업데이트 디봇 업데이트 DEEBOT 업데이트 ECOVACS HOME 앱 에코백스 앱 로봇청소기 업데이트 X8 T30 T50', '드라이버'),
         ('driver', '/driver/dreame.html', '드리미 펌웨어 업데이트 방법', 'Dreamehome 앱·로봇청소기', '드리미 업데이트 드리미 펌웨어 업데이트 드리미 로봇청소기 업데이트 Dreamehome 앱 드리미 앱 X50 X40 L20 L10s', '드라이버'),
         ('driver', '/driver/narwal.html', '나르왈 펌웨어 업데이트 방법', 'Narwal Freo 앱·로봇청소기', '나르왈 업데이트 나르왈 펌웨어 업데이트 나르왈 프레오 업데이트 Narwal Freo 앱 나르왈 앱 로봇청소기 업데이트', '드라이버'),
         ('driver', '/driver/wd.html', '웨스턴디지털 SSD·하드디스크 관리 프로그램 다운로드', 'WD·샌디스크 SSD·HDD Dashboard', '웨스턴디지털 드라이버 WD 대시보드 Western Digital Dashboard WD SSD 펌웨어 WD 외장하드 프로그램 샌디스크 SSD 대시보드 WD Black', '드라이버'),
         ('driver', '/driver/seagate.html', '씨게이트 외장하드 백업 프로그램 다운로드', '외장하드 백업 Toolkit', '씨게이트 툴킷 Seagate Toolkit 씨게이트 외장하드 백업 프로그램 씨게이트 펌웨어 씨게이트 드라이버 라씨 LaCie', '드라이버'),
         ('driver', '/driver/crucial.html', '크루셜 SSD 관리 프로그램 다운로드', 'SSD Storage Executive', '크루셜 스토리지 익스큐티브 Crucial Storage Executive 크루셜 SSD 펌웨어 MX500 펌웨어 P3 펌웨어 마이크론 SSD 프로그램', '드라이버'),
         ('driver', '/driver/synology.html', '시놀로지 NAS 설치·PC 동기화 프로그램 다운로드', 'NAS Assistant·Drive Client', '시놀로지 어시스턴트 Synology Assistant 시놀로지 드라이브 클라이언트 Synology Drive Client 시놀로지 다운로드 센터 시놀로지 NAS 설치 DSM 설치', '드라이버'),
         ('driver', '/driver/qnap.html', '큐냅 NAS 설치 프로그램 다운로드', 'NAS Qfinder Pro·Qsync', '큐냅 큐파인더 Qfinder Pro 다운로드 QNAP Qsync 큐냅 NAS 설치 큐냅 프로그램 HDP PC Agent', '드라이버'),
         ('driver', '/driver/benq.html', '벤큐 모니터·프로젝터 드라이버 다운로드', '모니터·프로젝터', '벤큐 모니터 드라이버 BenQ 드라이버 벤큐 프로젝터 드라이버 벤큐 소프트웨어 벤큐 모니터 설치', '드라이버'),
         ('driver', '/driver/viewsonic.html', '뷰소닉 모니터·프로젝터 드라이버 다운로드', '모니터·프로젝터', '뷰소닉 모니터 드라이버 ViewSonic 드라이버 뷰소닉 프로젝터 드라이버 뷰소닉 설치', '드라이버'),
         ('driver', '/driver/huion.html', '휴이온 펜 태블릿 드라이버 다운로드', '펜 태블릿', '휴이온 드라이버 Huion 드라이버 휴이온 태블릿 드라이버 휴이온 카무바스 드라이버 휴이온 펜 안됨', '드라이버'),
         ('driver', '/driver/xppen.html', '엑스피펜 펜 태블릿 드라이버 다운로드', '펜 태블릿', '엑스피펜 드라이버 XPPen 드라이버 XP-PEN 드라이버 엑스피펜 디코 드라이버 아티스트 드라이버', '드라이버'),
         ('driver', '/driver/msi.html', 'MSI 드라이버 다운로드', '노트북·메인보드·그래픽카드·모니터 공식 다운로드·설치 방법', 'MSI 드라이버 엠에스아이 드라이버 MSI 노트북 드라이버 MSI 메인보드 드라이버 MSI Center Live Update 드래곤센터', '드라이버'),
         ('driver', '/driver/gigabyte.html', '기가바이트 드라이버 다운로드', '메인보드·그래픽카드·AORUS 노트북 공식 다운로드·설치 방법', '기가바이트 드라이버 GIGABYTE 드라이버 기가바이트 메인보드 드라이버 GCC GIGABYTE Control Center 어로스 드라이버 AORUS 드라이버', '드라이버'),
         ('driver', '/driver/asrock.html', '애즈락 드라이버 다운로드', '메인보드·그래픽카드 공식 다운로드·설치 방법', '애즈락 드라이버 ASRock 드라이버 애즈락 메인보드 드라이버 Auto Driver Installer ADI 애즈락 랜 드라이버', '드라이버'),
         ('driver', '/driver/hansung.html', '한성컴퓨터 드라이버 다운로드', '노트북·데스크톱·모니터 공식 다운로드·설치 방법', '한성 드라이버 한성컴퓨터 드라이버 한성 노트북 드라이버 TFG 드라이버 보스몬스터 드라이버 한성 고객센터 다운로드', '드라이버'),
         ('driver', '/driver/razer.html', '레이저 드라이버 다운로드', '마우스·키보드·헤드셋·Blade 노트북 공식 다운로드·설치 방법', '레이저 드라이버 Razer 드라이버 레이저 마우스 드라이버 시냅스 Razer Synapse 4 시냅스 3 종료 레이저 키보드 드라이버', '드라이버'),
         ('driver', '/driver/canon.html', '캐논 드라이버 다운로드', 'PIXMA 잉크젯·imageCLASS·LBP 레이저 공식 다운로드·설치 방법', '캐논 드라이버 캐논 프린터 드라이버 Canon 드라이버 G3910 드라이버 G2910 드라이버 MF643Cdw 드라이버 PIXMA 드라이버 LBP 드라이버', '드라이버'),
         ('driver', '/driver/fujifilm.html', '후지필름 드라이버 다운로드', 'Apeos·ApeosPort·DocuPrint 복합기·프린터 공식 다운로드·설치 방법', '후지제록스 드라이버 후지필름 드라이버 후지필름 BI 드라이버 Apeos 드라이버 ApeosPort 드라이버 DocuPrint 드라이버 후지제록스 복합기 드라이버', '드라이버'),
         ('driver', '/driver/kyocera.html', '교세라 드라이버 다운로드', 'TASKalfa 복합기·ECOSYS 프린터 공식 다운로드·설치 방법', '교세라 드라이버 교세라 복합기 드라이버 Kyocera 드라이버 KX Driver TASKalfa 드라이버 ECOSYS 드라이버 M2640idw 드라이버', '드라이버'),
         ('driver', '/driver/ricoh.html', '리코 드라이버 다운로드', 'IM·MP 복합기·SP 프린터 공식 다운로드·설치 방법', '리코 드라이버 리코 복합기 드라이버 Ricoh 드라이버 리코 프린터 드라이버 PCL6 Universal Print IM C3000 드라이버', '드라이버'),
         ('driver', '/driver/logitech.html', '로지텍 드라이버 다운로드', '마우스·키보드·웹캠·Logitech G 공식 다운로드·설치 방법', '로지텍 드라이버 Logitech 드라이버 로지텍 마우스 드라이버 Logi Options+ 옵션플러스 G HUB 지허브 로지텍 키보드 드라이버 Unifying', '드라이버'),
         ('driver', '/driver/wacom.html', '와콤 드라이버 다운로드', 'Intuos·Cintiq·Wacom One 펜 타블렛 공식 다운로드·설치 방법', '와콤 드라이버 Wacom 드라이버 와콤 타블렛 드라이버 인튜어스 드라이버 Intuos 드라이버 신티크 드라이버 Wacom Center CTL-4100 드라이버', '드라이버'),
         ('driver', '/driver/realtek.html', '리얼텍 드라이버 다운로드', '랜카드(이더넷)·오디오·카드리더 칩 공식 다운로드·설치 방법', '리얼텍 드라이버 Realtek 드라이버 리얼텍 랜 드라이버 Realtek PCIe GbE Family Controller 드라이버 리얼텍 오디오 드라이버 랜카드 드라이버', '드라이버'),
         ('driver', '/driver/iptime.html', 'ipTIME 드라이버 다운로드', '공유기·USB 무선랜카드(A3000UA 등) 공식 다운로드·설치 방법', 'ipTIME 드라이버 아이피타임 드라이버 아이피타임 랜카드 드라이버 A3000UA 드라이버 A3000MINI 드라이버 ipTIME 펌웨어 업그레이드 무선랜카드 드라이버', '드라이버'),
         ('driver', '/driver/tplink.html', 'TP-Link 드라이버 다운로드', 'USB 무선랜카드(Archer T·TX)·공유기 공식 다운로드·설치 방법', 'TP-Link 드라이버 티피링크 드라이버 TP-Link 무선랜카드 드라이버 Archer T3U 드라이버 Archer TX20U 드라이버 TP-Link 펌웨어 하드웨어 버전', '드라이버'),
         ('driver', '/driver/steelseries.html', '스틸시리즈 드라이버·프로그램 바로 받기', '게이밍 마우스·키보드·헤드셋(Arctis) 공식 설치 파일 바로 다운로드', '스틸시리즈 드라이버 SteelSeries 드라이버 SteelSeries GG 다운로드 스틸시리즈 엔진 Arctis 드라이버 소나', '드라이버'),
         ('driver', '/driver/corsair.html', '커세어 드라이버·프로그램 바로 받기', '게이밍 키보드·마우스·헤드셋·RGB 팬·쿨러 공식 설치 파일 바로 다운로드', '커세어 드라이버 Corsair 드라이버 iCUE 다운로드 커세어 iCUE 커세어 키보드 드라이버 커세어 헤드셋 드라이버', '드라이버'),
         ('driver', '/driver/hyperx.html', '하이퍼X 드라이버·프로그램 바로 받기', '게이밍 헤드셋·마우스·키보드 공식 설치 파일 바로 다운로드', '하이퍼X 드라이버 HyperX 드라이버 NGENUITY 다운로드 엔제뉴이티 하이퍼엑스 헤드셋 드라이버 클라우드 드라이버', '드라이버'),
         ('driver', '/driver/creative.html', '크리에이티브 드라이버·프로그램 바로 받기', '사운드 블라스터·스피커·헤드셋 공식 설치 파일 바로 다운로드', '크리에이티브 드라이버 Creative 드라이버 사운드블라스터 드라이버 Sound Blaster Command Creative App G6 드라이버', '드라이버'),
         ('driver', '/driver/jabra.html', '자브라 드라이버·프로그램 바로 받기', '업무용 헤드셋·스피커폰·이어버드 공식 설치 파일 바로 다운로드', '자브라 드라이버 Jabra 드라이버 Jabra Direct 다운로드 자브라 헤드셋 펌웨어 Evolve2', '드라이버'),
         ('driver', '/driver/epos.html', '에포스 드라이버·프로그램 바로 받기', '업무용·게이밍 헤드셋(옛 젠하이저 커뮤니케이션) 공식 설치 파일 바로 다운로드', '에포스 드라이버 EPOS Connect 젠하이저 헤드셋 드라이버 젠하이저 게이밍 드라이버 GSP 드라이버', '드라이버'),
         ('driver', '/driver/mskb.html', 'MS 마우스·키보드 드라이버·프로그램 바로 받기', '마이크로소프트 마우스·키보드(Ergonomic·Sculpt 등) 공식 설치 파일 바로 다운로드', '마이크로소프트 마우스 드라이버 마우스 및 키보드 센터 Mouse and Keyboard Center MS 키보드 드라이버 인텔리포인트', '드라이버'),
         ('driver', '/driver/android.html', '안드로이드 USB 드라이버·프로그램 바로 받기', '구글 픽셀·안드로이드 폰 PC 연결·ADB 공식 설치 파일 바로 다운로드', '안드로이드 USB 드라이버 구글 USB 드라이버 픽셀 드라이버 ADB 드라이버 adb 다운로드 platform-tools fastboot 드라이버', '드라이버'),
         ('driver', '/driver/elgato.html', '엘가토 드라이버·프로그램 바로 받기', '스트림덱·웹캠·캡처보드 공식 설치 파일 바로 다운로드', '엘가토 드라이버 Elgato 드라이버 스트림덱 다운로드 Stream Deck Camera Hub 페이스캠 드라이버', '드라이버'),
         ('driver', '/driver/ssd.html', 'SSD 관리 프로그램 드라이버·프로그램 바로 받기', '크루셜·킹스톤·WD·씨게이트 SSD·HDD 펌웨어·상태 검사 공식 설치 파일 바로 다운로드', 'SSD 펌웨어 업데이트 크루셜 Storage Executive 킹스톤 SSD Manager WD Dashboard Kitfox 씨게이트 SeaTools SSD 수명 확인 프로그램', '드라이버'),
         ('driver', '/driver/vcredist.html', 'Visual C++ 재배포 패키지 바로 받기', 'MSVCP140.dll·VCRUNTIME140.dll 오류 해결 — Microsoft 공식 파일 바로 받기', 'Visual C++ 재배포 패키지 다운로드 vcredist MSVCP140.dll 오류 VCRUNTIME140.dll 없음 VCRUNTIME140_1.dll MSVCR100.dll MSVCR120.dll vc_redist.x64 비주얼 C++ 런타임', '드라이버'),
         ('driver', '/driver/directx.html', 'DirectX 최종 사용자 런타임 바로 받기', 'd3dx9_43.dll·XINPUT1_3.dll 오류 해결 — Microsoft 공식 파일 바로 받기', 'DirectX 다운로드 다이렉트X 런타임 d3dx9_43.dll 오류 XINPUT1_3.dll 없음 d3dx11_43.dll dxwebsetup DirectX 설치 xactengine X3DAudio XNA Framework', '드라이버'),
         ('driver', '/driver/dotnet.html', '.NET 데스크톱 런타임 바로 받기', '".NET이 필요합니다" 오류 해결 — Microsoft 공식 파일 바로 받기', '.NET 다운로드 닷넷 런타임 .NET 8 데스크톱 런타임 .NET Desktop Runtime .NET Framework 4.8.1 .NET Framework 3.5 설치 WebView2 런타임 이 애플리케이션을 실행하려면 .NET', '드라이버'),
         ('driver', '/driver/xbox.html', 'Xbox 컨트롤러 PC 드라이버·연결 방법', '엑스박스 패드 PC 연결·무선 어댑터·펌웨어 — Microsoft 공식 파일 바로 받기', '엑스박스 컨트롤러 PC 연결 Xbox 컨트롤러 드라이버 엑박패드 블루투스 연결 Xbox 무선 어댑터 드라이버 Xbox 액세서리 앱 컨트롤러 펌웨어 업데이트', '드라이버'),
         ('drive', '/drive/update/', '차 내비·블랙박스 업데이트 모음', '현대·기아·제네시스 내비 업데이트를 그림으로 쉽게', '내비 업데이트 내비게이션 업데이트 지도 업데이트 순정 내비 업데이트 블랙박스 업데이트 빌트인캠 업데이트 Navigation Updater', '자동차·지도'),
         ('drive', '/drive/update/hyundai.html', '현대 내비게이션 업데이트 방법', 'USB·SD 준비부터 차에서 업데이트까지 그림으로', '현대 내비 업데이트 현대차 네비 업데이트 현대 내비게이션 업데이트 방법 현대 지도 업데이트 블루링크 업데이트 아반떼 쏘나타 그랜저 싼타페 내비 업데이트 빌트인캠 업데이트', '자동차·지도'),
         ('drive', '/drive/update/kia.html', '기아 내비게이션 업데이트 방법', 'USB·SD 준비부터 차에서 업데이트까지 그림으로', '기아 내비 업데이트 기아 네비 업데이트 기아 내비게이션 업데이트 방법 기아 지도 업데이트 쏘렌토 카니발 K5 스포티지 내비 업데이트 빌트인캠 업데이트', '자동차·지도'),
         ('drive', '/drive/update/renault.html', '르노코리아 내비·openR link 업데이트', '무선 업데이트 + 9.3인치 지도 USB 설치', '르노코리아 내비 업데이트 르노 내비 업데이트 openR link 업데이트 오픈알링크 지도 업데이트 그랑콜레오스 아르카나 QM6 SM6 내비 업데이트', '자동차·지도'),
         ('drive', '/drive/update/chevrolet.html', '쉐보레 내비게이션 지도 업데이트', 'SD 카드 + 공식 업데이터, 인증번호 백업', '쉐보레 내비 업데이트 쉐보레 지도 업데이트 말리부 트레일블레이저 트래버스 콜로라도 이쿼녹스 볼트 내비 업데이트 SD카드 인증번호', '자동차·지도'),
         ('drive', '/drive/update/kgm.html', 'KGM(쌍용) 내비게이션 업데이트', '차종별 공식 업데이트 사이트 정리', 'KGM 내비 업데이트 쌍용 내비 업데이트 토레스 내비 업데이트 액티언 무쏘 코란도 렉스턴 티볼리 내비 업데이트 인포콘', '자동차·지도'),
         ('drive', '/drive/update/inavi.html', '아이나비 내비 지도 업그레이드', '아이나비 매니저 원클릭 업그레이드', '아이나비 업데이트 아이나비 지도 업데이트 아이나비 업그레이드 아이나비 매니저 내비 지도 업그레이드', '자동차·지도'),
         ('drive', '/drive/update/genesis.html', '제네시스 내비게이션 업데이트 방법', 'USB·SD 준비부터 차에서 업데이트까지 그림으로', '제네시스 내비 업데이트 제네시스 네비 업데이트 G80 GV80 GV70 G90 내비 업데이트 제네시스 지도 업데이트 빌트인캠 업데이트', '자동차·지도'),
         ('drive', '/drive/update/tesla.html', '테슬라 소프트웨어 업데이트 방법', '와이파이 무선 업데이트·예약·자동 설치', '테슬라 업데이트 테슬라 소프트웨어 업데이트 모델Y 업데이트 모델3 업데이트 테슬라 OTA 우선 업데이트 테슬라 드라이버', '자동차·지도'),
         ('calendar', '/calendar/exam-schedule.html', '자격증 시험일정 달력 (국가기술·국가전문·한국사·토익·JLPT)', '원서접수·시험일·합격발표를 한 달력에, 매달 업데이트', '자격증 시험일정 달력 큐넷 기사 산업기사 기능사 한국사 토익 JLPT 원서접수', '날짜·달력'),
         ('life', '/life/subsidy.html', '조건으로 찾는 정부 지원금 (보조금24 1만여 건)', '지역·대상·나이·분야로 받을 수 있는 지원금만 걸러 보기', '정부 지원금 조회 보조금24 지원금 찾기 청년 지원금 소상공인 지원금 노인 지원금', '생활·행정'),
         ('drive', '/life/route-navi.html', '경유지 많은 노선 내비', '정류장 30곳 넘어도 순서대로 길안내', '경유지 많은 내비 다중 경유지 길찾기 경유지 30개 셔틀버스 노선 통학버스 택배 동선 순서 길안내', '자동차·지도'),
         ('drive', '/life/taxi-fare.html', '택시비·통행료 계산기', '택시비와 내 차 기름값·통행료 비교', '택시비 계산기 택시요금 계산 통행료 계산 고속도로 통행료 기름값 계산 유류비 계산 카카오 길찾기 거리 계산', '자동차·지도'),
         ('study', '/study/meal-ranking.html', '전국 학교 급식 랭킹', '이번 주 전국·시도별 인기 메뉴 TOP 20, 우리 학교 급식', '급식 급식표 오늘 급식 학교 급식 메뉴 급식 순위 급식 랭킹 인기 급식 메뉴 우리학교 급식 식단표 알레르기', '학생·공부'),
         ('drive', '/drive/bus-share.html', '셔틀버스 위치 공유 (기사용)', '링크 하나로 승객에게 실시간 버스 위치·도착 예상', '셔틀버스 위치 공유 통학버스 학원차 실시간 위치 버스 지금 어디 기사 위치 공유 링크 도착 예정 시간', '자동차·지도'),
         ('drive', '/life/midpoint.html', '중간지점 찾기', '친구들과 만날 곳 추천 + 공유 카드', '중간지점 찾기 약속장소 추천 중간 위치 만날 장소 친구 중간 지점 지하철역 중간 카카오 길찾기', '자동차·지도'),
         ('medical', '/medical/pharmacy-open.html', '지금 문 연 약국', '밤·주말·공휴일 영업 약국 지도', '지금 문 연 약국 영업중인 약국 근처 약국 일요일 약국 공휴일 약국 심야약국 야간약국', '병원·건강'),
         ('medical', '/medical/emergency-room.html', '응급실 실시간 병상', '근처 응급실 빈 병상·전화', '응급실 병상 근처 응급실 응급실 실시간 응급실 가용병상 야간 응급실', '병원·건강'),
         ('drive', '/drive/car-inspection.html', '자동차 정기검사 기간 계산기', '신차 5년·이후 2년, 검사 가능 기간·지연 과태료', '자동차 정기검사 기간 정기검사 날짜 정기검사 주기 신차 정기검사 5년 자동차검사 과태료 종합검사 기간 검사 유효기간', '자동차·지도'),
         ('drive', '/drive/tire.html', '타이어 규격·제조일자 읽기', '225/55R17 뜻, DOT 제조 주차, 교체 시기 1.6mm', '타이어 규격 보는법 타이어 숫자 의미 타이어 제조일자 DOT 타이어 교체시기 타이어 편평비 타이어 사이즈 비교 마모한계', '자동차·지도'),
         ('drive', '/drive/cctv.html', '고속도로·국도 CCTV 바로가기', '로드플러스·국가교통정보센터·UTIC·서울·경기·부산·대구·제주', '고속도로 cctv 실시간 고속도로 cctv 국도 cctv 도로 cctv 교통 cctv 실시간 도로상황 로드플러스 utic topis', '자동차·지도'),
         ('image', '/image/film-filter.html', '필름 카메라 필터', 'Y2K 디카·올드폰·흑백 필름, 카메라로 바로 찍기', '필름 카메라 필터 필름 필터 앱 필름 카메라 어플 y2k 디카 감성 올드폰 감성 흑백 필름 사진 빈티지 사진 필터 레트로 카메라 빛샘 그레인 필름 감성 사진', '이미지 도구'),
         ('image', '/image/character-maker.html', '동물 캐릭터 만들기', '귀여운 동물 캐릭터·색칠용 도안 무료 생성', '동물 캐릭터 만들기 캐릭터 생성기 귀여운 캐릭터 만들기 아바타 만들기 캐릭터 메이커 색칠공부 도안 색칠 그림 컬러링 고양이 토끼 곰 캐릭터 프로필 이미지 만들기 저작권 없는 캐릭터', '이미지 도구'),
         ('life', '/life/copyright-register.html', '저작권 등록 도우미', '저작물 등록 수수료 계산·명세서·준비물', '저작권 등록 방법 저작물 등록 수수료 저작권 등록 비용 캐릭터 저작권 등록 그림 저작권 등록 미술저작물 등록 저작권 등록 절차 한국저작권위원회 cros 저작권 등록 신청서 저작물명세서', '생활·행정'),
         ('life', '/life/yearend-tax.html', '연말정산 공제 체크리스트·일정', '2026년 귀속(2027년 진행) 공제 점검 + 놓친 공제 찾기', '연말정산 연말정산 간소화 연말정산 공제 항목 연말정산 체크리스트 연말정산 일정 2026 귀속 연말정산 2027 연말정산 연말정산 미리보기 월세 세액공제 13월의 월급 연말정산 준비물 연말정산 환급 홈택스 간소화', '생활·행정'),
         ('drive', '/life/car-tax-yearly.html', '자동차세 연납 할인 계산기', '1월에 미리 내면 할인 — 연세액으로 할인액 계산 + 신청법', '자동차세 연납 자동차세 할인 자동차세 연납 신청 자동차세 연납 할인율 위택스 자동차세 이택스 자동차세 자동차세 1월 연납 자동차세 계산 자동차세 공제율 자동차세 연납 기간 자동차세 선납', '자동차·지도'),
         ('calendar', '/calendar/seollal-2027.html', '2027 설날 날짜·연휴', '2월 7일 설날, 연휴 2/6~2/9 — D-day·연차·귀성 준비', '2027 설날 설날 2027 구정 2027 2027 설 연휴 설날 연휴 2027 2027 설날 날짜 설날 대체공휴일 2027 설날 며칠 2027 구정 설날 기차표 예매 설 연휴 2027', '날짜·달력'),
         ('life', '/life/min-wage-2027.html', '2027 최저임금·주휴수당 계산기', '시급 10,700원 — 주휴 포함 주급·월급, 최저임금 위반 확인', '2027 최저임금 최저임금 2027 2027 최저시급 2027 최저월급 최저임금 월급 주휴수당 계산 주휴수당 알바 주휴수당 최저임금 계산기 최저시급 월급 2027 최저임금 월급 최저임금 실수령액', '생활·행정'),
         ('medical', '/medical/checkup-2027.html', '2027 국가건강검진 대상 확인', '출생연도(홀짝)로 2027 검진 대상 조회 + 바뀌는 항목', '2027 건강검진 국가건강검진 2027 2027 건강검진 대상자 건강검진 대상자 조회 홀수년생 건강검진 건강검진 출생연도 2027 국가건강검진 일반건강검진 대상 건강검진 홀짝 건강검진 나이', '병원·건강'),
         ('excel', '/excel/practice.html', '엑셀 함수 연습장', '설명 보고 직접 입력, 바로 채점', '엑셀 연습 문제 엑셀 함수 연습 엑셀 수식 예제 SUM AVERAGE IF VLOOKUP 연습 엑셀 공부 엑셀 기초 엑셀 자격증 연습 엑셀 실습 함수 연습장', '엑셀 수식'),
         ('doc', '/doc/hwp-shortcut.html', '한글 단축키 연습', '키보드로 직접 눌러 익히기', '한글 단축키 HWP 단축키 한글 단축키 모음 한글 단축키 연습 한글 저장 단축키 글자 모양 단축키 문단 모양 단축키 한컴 단축키 아래아한글 단축키 연습', '문서'),
         ('drive', '/drive/gas-station.html', '싼 주유소 지도', '동네별 최저가 휘발유·경유', '싼 주유소 최저가 주유소 근처 주유소 기름값 휘발유 가격 경유 가격 오피넷', '자동차·지도'),
         ('drive', '/drive/ev-charger.html', '전기차 충전소 지도', '지금 빈 충전기·급속 충전', '전기차 충전소 근처 충전소 급속충전 빈 충전기 전기차 충전', '자동차·지도'),
         ('drive', '/drive/parking.html', '공영·무료 주차장', '요금·운영시간 지도', '공영주차장 무료주차장 근처 주차장 주차요금 주차장 찾기', '자동차·지도'),
         ('drive', '/drive/rest-area.html', '고속도로 휴게소', '대표 메뉴·기름값 지도', '고속도로 휴게소 휴게소 맛집 휴게소 음식 휴게소 기름값 휴게소 메뉴', '자동차·지도'),
         ('life', '/life/toilet.html', '근처 공중화장실', '개방시간·장애인 화장실 지도', '공중화장실 근처 화장실 화장실 찾기 개방 화장실 24시간 화장실', '생활·행정'),
         ('life', '/life/air-quality.html', '우리 동네 미세먼지', '측정소별 실시간 미세·초미세먼지', '미세먼지 초미세먼지 오늘 미세먼지 실시간 미세먼지 우리동네 미세먼지 대기질', '생활·행정'),
         ('trip', '/trip/festival.html', '이번 주말 축제 지도', '지금 열리는 축제·행사', '이번 주말 축제 축제 지도 지역 축제 행사 일정 가볼만한 축제', '여행'),
         ('trip', '/trip/camping.html', '캠핑장 찾기', '글램핑·카라반·반려견 동반', '캠핑장 글램핑 카라반 오토캠핑장 애견캠핑장 반려견 동반 캠핑장', '여행'),
         ('life', '/life/sms-budget.html', '문자 가계부 (카드 문자 붙여넣기 자동 정리)', '카드·은행 문자를 붙여 넣으면 식비·카페·교통으로 자동 분류, 달 예산·하루 쓸 돈', '가계부 가계부 앱 무료 가계부 웹 가계부 문자 가계부 카드 문자 가계부 자동 가계부 지출 정리 한 달 지출 예산 짜기 하루 예산 소비 분석', '생활·행정'),
         ('life', '/life/fridge-recipe.html', '냉장고 털기 · 있는 재료로 요리 추천', '재료를 누르면 바로 만들 수 있는 집밥과 한 가지만 더 있으면 되는 요리, 단계별 타이머', '냉장고 털기 냉장고 재료 요리 있는 재료로 요리 재료로 요리 찾기 오늘 뭐 해먹지 집밥 레시피 자취 요리 간단 요리 반찬 만들기 레시피 추천', '생활·행정'),
         ('life', '/life/christmas.html', '크리스마스 D-day · 선물 예산 계산기 (2026)', '12월 25일(금)까지 남은 날 카운트다운 + 사람별 선물 예산 나누기', '크리스마스 D-day 크리스마스 디데이 크리스마스까지 며칠 크리스마스 카운트다운 선물 예산 크리스마스 선물 계산기 연말 선물 2026 크리스마스 요일 어드벤트 캘린더', '생활·행정'),
         ('life', '/life/split-bill.html', 'N빵 정산 계산기 (모임·여행 더치페이)', '누가 누구에게 얼마 보낼지 송금 횟수 최소로 정리', 'N빵 계산기 엔빵 더치페이 정산 모임 정산 여행 정산 회비 정산 술값 나누기 정산 앱 누가 누구에게', '생활·행정'),
         ('design', '/design/room-3d.html', '3D 방·사무실 꾸미기 (가구 400여 종 배치·차박 세팅)', '실제 치수 가구를 내 방·사무실 크기에 놓아 보는 3D 인테리어 시뮬레이터', '3D 방 꾸미기 가구 배치 시뮬레이터 원룸 인테리어 시뮬레이션 방 꾸미기 게임 자취방 꾸미기 사무실 배치 사무실 인테리어 사무실 레이아웃 책상 배치 차박 세팅 인테리어 3D', '디자인'),
         ('life', '/life/invest.html', '청약·줍줍 일정 + 투자계산기', '오늘 넣을 수 있는 청약·무순위 줍줍 3일마다 업데이트, 주식 세금·대출·연금 계산', '청약 일정 줍줍 무순위 청약 투자계산기 주식 세금 대출 한도 청약 가점', '생활·행정'),
         ('life', '/life/invest/us-stock-tax.html', '해외주식 양도세 계산·연말 절세 (2026)', '1년 순이익 −250만 원 × 22%, 결제일 기준, 연말 절세 3가지, RIA 계좌', '해외주식 양도세 미국주식 양도소득세 계산 250만원 공제 22% 연말 절세 해외주식 결제일 RIA 계좌 국내시장 복귀계좌 해외주식 세금 신고', '생활·행정'),
         ('life', '/life/invest/pension-tax-credit.html', '연금저축·IRP 세액공제 한도와 환급액 (2026)', '900만 원 채우면 최대 148만 5천 원, 12월 31일 납입 마감, 내 환급액 바로 계산', '연금저축 세액공제 IRP 세액공제 연금저축 한도 900만원 16.5% 13.2% 연말정산 환급 연금저축 연말 납입 마감 ISA 만기 연금 전환 300만원', '생활·행정'),
         ('life', '/life/subsidy/eitc.html', '근로·자녀장려금 자격·금액·신청 기간 (2026)', '단독 165만·홑벌이 285만·맞벌이 330만 원, 기한후 신청 12월 1일 마감, 내 금액 바로 계산', '근로장려금 자녀장려금 기한후 신청 근로장려금 자격 소득 기준 재산 기준 맞벌이 4400만원 근로장려금 지급일 반기신청 홈택스 신청 ARS 1544-9944', '생활·행정')]
for cat, u, n, d, kw, cn in MOVED:
    p = os.path.join(root, cat, 'index.html')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if f'href="{u}"' not in s:
            art = {'/design/room-3d.html': 'room3d', '/life/route-navi.html': 'bus', '/drive/bus-share.html': 'bus', '/life/toilet.html': 'life', '/life/air-quality.html': 'life'}.get(u)
            if not art:
                art = next((k for k, rx in KW if re.search(rx, n) and os.path.exists(os.path.join(root, 'assets/art/hl', f'cs-{k}.svg'))), cat)
            li = (f'<li><a href="{u}"><i class="th"><img src="/assets/art/hl/cs-{art}.svg" alt="" width="200" height="140" loading="lazy"></i>'
                  f'<img class="pg" src="/assets/art/hl/pg-{cat}.svg" alt="" width="26" height="26" loading="lazy"><b>{n}</b><span>{d}</span></a></li>')
            s2 = re.sub(r'(<ul class="tlist[^"]*">)', lambda m: m.group(1) + li, s, count=1)
            if s2 != s:
                open(p, 'w', encoding='utf-8').write(s2); print('hub +', u)
    p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
    if f'"u":"{u}"' not in s and TRIP in s:
        e = _json.dumps({"t": n, "d": d, "k": kw, "c": cn, "u": u}, ensure_ascii=False, separators=(',', ':'))
        open(p, 'w', encoding='utf-8').write(s.replace(TRIP, TRIP + ',' + e, 1)); print('search +', u)
    p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    if f'honglife.co.kr{u}<' not in s:
        open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', f'<url><loc>https://honglife.co.kr{u}</loc><lastmod>2026-11-19</lastmod></url>\n</urlset>', 1)); print('sitemap +', u)


# ── 시도별 급식 랭킹 17쪽: 사이트맵 ──
p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
for _sl in ('seoul', 'busan', 'daegu', 'incheon', 'gwangju', 'daejeon', 'ulsan', 'sejong', 'gyeonggi', 'gangwon', 'chungbuk', 'chungnam', 'jeonbuk', 'jeonnam', 'gyeongbuk', 'gyeongnam', 'jeju'):
    if os.path.exists(os.path.join(root, 'study', 'meal', _sl + '.html')) and f'/study/meal/{_sl}.html<' not in s:
        s = s.replace('</urlset>', f'<url><loc>https://honglife.co.kr/study/meal/{_sl}.html</loc><lastmod>2026-11-21</lastmod></url>\n</urlset>', 1)
open(p, 'w', encoding='utf-8').write(s)

# ── 새 분류: 공문서·민원(/gov/) (overlay, 2026-11-19) ──
_gv_p = os.path.join(root, 'govcats.json')
if os.path.exists(_gv_p):
    GV = _json.load(open(_gv_p, encoding='utf-8')); os.remove(_gv_p)
    p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
    m = re.search(r'<li><a class="ct" href="/life/".*?</a></li>', s, flags=re.S)
    if m and 'href="/gov/"' not in s:
        card = (f'<li><a class="ct" href="/gov/" style="--bg:linear-gradient(#D7EEF2 0 40%,transparent 40%),linear-gradient(90deg,#3BA3B6 0 58%,#8CCBD6 58%)">'
                f'<span class="ch"><em>{len(GV)}개</em><b>공문서·민원</b></span><i class="ci" style="background-image:url(/assets/art/hl/cs-gov.svg)"></i><span class="go" aria-hidden="true">›</span></a></li>')
        s = s[:m.end()] + card + s[m.end():]; print('home: gov card')
    if TRIP in s and '"u":"/gov/' not in s:
        ent = [_json.dumps({"t": n, "d": d, "k": kw, "c": "공문서·민원", "u": u}, ensure_ascii=False, separators=(',', ':')) for u, n, d, kw in GV]
        ent.append(_json.dumps({"t": "공문서·민원 도우미 모음", "d": "위임장 인쇄, 대리 발급 위임장 예시, 주민센터 준비물", "k": "민원 위임장 주민센터 서류 공문서", "c": "공문서·민원", "u": "/gov/"}, ensure_ascii=False, separators=(',', ':')))
        s = s.replace(TRIP, TRIP + ',' + ','.join(ent), 1); print('search index + gov', len(ent))
    open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    if 'honglife.co.kr/gov/' not in s:
        urls = ['/gov/'] + [u for u, *_ in GV]
        s = s.replace('</urlset>', ''.join(f'<url><loc>https://honglife.co.kr{u}</loc><lastmod>2026-11-19</lastmod></url>\n' for u in urls) + '</urlset>', 1)
        open(p, 'w', encoding='utf-8').write(s); print('sitemap + gov', len(urls))

# ── 새 분류: 자동차·지도(/drive/) (overlay, 2026-11-20) — 홈 카드, 허브 검색, 사이트맵 ──
p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
if 'href="/drive/"' not in s:
    m = re.search(r'<li><a class="ct" href="/gov/".*?</a></li>', s, flags=re.S) or re.search(r'<li><a class="ct" href="/life/".*?</a></li>', s, flags=re.S)
    if m:
        nd = sum(1 for e in MOVED if e[0] == 'drive')
        card = (f'<li><a class="ct" href="/drive/" style="--bg:linear-gradient(#FFE8CC 0 40%,transparent 40%),linear-gradient(90deg,#FF922B 0 58%,#FFC078 58%)">'
                f'<span class="ch"><em>{nd}개</em><b>자동차·지도</b></span><i class="ci" style="background-image:url(/assets/art/hl/cs-drive.svg)"></i><span class="go" aria-hidden="true">›</span></a></li>')
        s = s[:m.end()] + card + s[m.end():]; print('home: drive card')
    if TRIP in s and '"u":"/drive/"' not in s:
        s = s.replace(TRIP, TRIP + ',' + _json.dumps({"t": "자동차·지도 도구 모음", "d": "택시비·통행료 계산, 중간지점 찾기, 경유지 많은 노선 내비", "k": "자동차 지도 길찾기 택시비 중간지점 내비", "c": "자동차·지도", "u": "/drive/"}, ensure_ascii=False, separators=(',', ':')), 1)
    open(p, 'w', encoding='utf-8').write(s)
# ── 드라이버 영어판(/en/driver/) 사이트맵 (overlay, 2026-11-22) ──
p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
_en = [u for u in ('/en/driver/', '/en/driver/hp.html', '/en/driver/sindoh.html', '/en/driver/nvidia.html', '/en/driver/amd.html', '/en/driver/intel.html', '/en/driver/epson.html', '/en/driver/brother.html', '/en/driver/lg.html', '/en/driver/apple.html', '/en/driver/surface.html', '/en/driver/lenovo.html', '/en/driver/dell.html', '/en/driver/asus.html', '/en/driver/acer.html', '/en/driver/roborock.html', '/en/driver/samsung.html', '/en/driver/ecovacs.html', '/en/driver/dreame.html', '/en/driver/narwal.html', '/en/driver/wd.html', '/en/driver/seagate.html', '/en/driver/crucial.html', '/en/driver/synology.html', '/en/driver/qnap.html', '/en/driver/benq.html', '/en/driver/viewsonic.html', '/en/driver/huion.html', '/en/driver/xppen.html', '/en/driver/msi.html', '/en/driver/gigabyte.html', '/en/driver/asrock.html', '/en/driver/hansung.html', '/en/driver/razer.html', '/en/driver/canon.html', '/en/driver/fujifilm.html', '/en/driver/kyocera.html', '/en/driver/ricoh.html', '/en/driver/logitech.html', '/en/driver/wacom.html', '/en/driver/realtek.html', '/en/driver/iptime.html', '/en/driver/tplink.html', '/en/driver/steelseries.html', '/en/driver/corsair.html', '/en/driver/hyperx.html', '/en/driver/creative.html', '/en/driver/jabra.html', '/en/driver/epos.html', '/en/driver/mskb.html', '/en/driver/android.html', '/en/driver/elgato.html', '/en/driver/ssd.html', '/en/driver/vcredist.html', '/en/driver/directx.html', '/en/driver/dotnet.html', '/en/driver/xbox.html')
       if os.path.exists(os.path.join(root, u.lstrip('/') + ('index.html' if u.endswith('/') else ''))) and f'honglife.co.kr{u}<' not in s]
if _en:
    open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', ''.join(f'<url><loc>https://honglife.co.kr{u}</loc><lastmod>2026-11-22</lastmod></url>\n' for u in _en) + '</urlset>', 1)); print('sitemap + en driver', len(_en))

# ── 새 분류: 드라이버(/driver/) (overlay, 2026-11-22) — 홈 카드 ──
p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
if 'href="/driver/"' not in s and os.path.exists(os.path.join(root, 'driver', 'index.html')):
    m = re.search(r'<li><a class="ct" href="/drive/".*?</a></li>', s, flags=re.S)
    if m:
        nd = sum(1 for e in MOVED if e[0] == 'driver')
        card = (f'<li><a class="ct" href="/driver/" style="--bg:linear-gradient(#DCE8FF 0 40%,transparent 40%),linear-gradient(90deg,#3B6FE0 0 58%,#8FB1F5 58%)">'
                f'<span class="ch"><em>{nd}개</em><b>드라이버</b></span><i class="ci" style="background-image:url(/assets/art/hl/cs-printer.svg)"></i><span class="go" aria-hidden="true">›</span></a></li>')
        s = s[:m.end()] + card + s[m.end():]; open(p, 'w', encoding='utf-8').write(s); print('home: driver card')
p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
if 'honglife.co.kr/drive/<' not in s:
    open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', '<url><loc>https://honglife.co.kr/drive/</loc><lastmod>2026-11-20</lastmod></url>\n</urlset>', 1)); print('sitemap + drive')

# ── 상단 분류 줄 고정: 모든 한국어 페이지에 같은 분류 전체 목록(가로 스크롤 한 줄) ──
# (CATBAR·FOLD·CANON_RENAME 정의는 파일 앞쪽 '홈 분류별로 찾기' 블록 위로 이동 — 홈 그리드와 상단 바가 같은 정의 사용)
CATCSS = ('<style id="hl-catbar-css">.brandbar .in nav a:not(.srch):not(.lang){display:none!important}'
          '.catbar{border-top:1px solid rgba(0,0,0,.06)}.catbar .in2{max-width:1080px;margin:0 auto;padding:7px 12px;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;'
          '-webkit-mask-image:linear-gradient(90deg,#000 92%,transparent);mask-image:linear-gradient(90deg,#000 92%,transparent)}.catbar .in2::-webkit-scrollbar{display:none}'
          '.brandbar .catbar a{display:inline-block!important;flex:none;padding:6px 12px;border-radius:999px;font-size:14px;font-weight:600;line-height:1.35;color:#4E5968;text-decoration:none;white-space:nowrap}'
          '.catbar a:hover{background:rgba(0,0,0,.05);color:#191F28}.catbar a[aria-current]{background:#191F28;color:#fff}'
          '@media(max-width:600px){.catbar .in2{padding:6px 10px}.catbar a{font-size:13.5px;padding:6px 11px}}'
          '.xp-shot img{border-radius:0!important}</style>')  # 2026-11-28: 설명 스크린샷 모서리에 번호 배지(①②)가 잘리는 것 방지
NAV_RE = re.compile(r'(<div class="brandbar"><div class="in">.*?</div>)(</div>)', re.S)
k = 0
for dp, dn, fn in os.walk(root):
    rel = os.path.relpath(dp, root).split(os.sep)
    if len(rel[0]) == 2 and rel[0] not in ('ai', 'qr'):  # 영어 등 다른 언어 폴더(en, ja ...) 제외
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f); s = open(p, encoding='utf-8').read()
        if 'class="catbar"' in s or '<nav aria-label="주요 분류">' not in s:
            continue
        cur = rel[0] if rel[0] != '.' else ''
        if rel[0] == 'life' and f in ('route-navi.html', 'taxi-fare.html', 'midpoint.html'):
            cur = 'drive'
        cur = FOLD.get(cur, cur)
        links = ''.join(f'<a href="/{c}/"' + (' aria-current="page"' if c == cur else '') + f'>{n}</a>' for c, n in CATBAR)
        s2 = NAV_RE.sub(lambda m: m.group(1) + f'<div class="catbar" role="navigation" aria-label="분류 전체"><div class="in2">{links}</div></div><script>(function(){{var a=document.querySelector(".catbar a[aria-current]");if(a)a.parentNode.scrollLeft=a.offsetLeft-a.parentNode.clientWidth/2+a.offsetWidth/2}})()</script>' + m.group(2), s, count=1)
        if s2 != s:
            s2 = s2.replace('</head>', CATCSS + '</head>', 1)
            open(p, 'w', encoding='utf-8').write(s2); k += 1
print('catbar:', k)

# ── 홈 도구 수·분류 카드 수를 실제 개수로 맞춤 ──
p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
n_tools = len(set(re.findall(r'"u":"(/[^"]*)"', s)))
s = re.sub(r'도구 \d+가지', f'도구 {n_tools}가지', s, count=1)
for cat, add in (('calendar', 1), ('life', 3)):
    s = re.sub(r'(<a class="ct" href="/' + cat + r'/"[^>]*><span class="ch"><em>)(\d+)(개</em>)', lambda m: m.group(1) + str(int(m.group(2)) + add) + m.group(3), s, count=1)
open(p, 'w', encoding='utf-8').write(s); print('home tool count:', n_tools)

# ── 분류 페이지 아래 '다른 분류' 카드 줄을 모든 분류에서 같은 목록·순서로 ──
REL_RE = re.compile(r'(<ul class="hl-rel">)(.*?)(</ul>)', re.S)
LI_RE = re.compile(r'<li><a href="(/[a-z]+/)".*?</li>', re.S)
canon = {}
for c, _ in CATBAR:
    p = os.path.join(root, c, 'index.html')
    if os.path.exists(p):
        m = REL_RE.search(open(p, encoding='utf-8').read())
        if m:
            for lm in LI_RE.finditer(m.group(2)):
                canon.setdefault(lm.group(1), lm.group(0))
if '/gov/' not in canon:
    canon['/gov/'] = ('<li><a href="/gov/" style="--bg:linear-gradient(#D7EEF2 0 34%,#3BA3B6 34%)"><b>공문서·민원</b><span>위임장 인쇄, 주민센터 방문 준비물</span>'
                      '<i style="background-image:url(/assets/art/hl/cs-gov.svg)"></i></a></li>')
if '/drive/' not in canon:
    canon['/drive/'] = ('<li><a href="/drive/" style="--bg:linear-gradient(#FFE8CC 0 34%,#FFA94D 34%)"><b>자동차·지도</b><span>택시비·통행료 계산, 중간지점 찾기, 노선 내비</span>'
                        '<i style="background-image:url(/assets/art/hl/cs-drive.svg)"></i></a></li>')
if '/trip/' not in canon:
    canon['/trip/'] = ('<li><a href="/trip/" style="--bg:linear-gradient(#D6ECF7 0 34%,#7CBDE3 34%)"><b>여행·패키지</b><span>출발확정 해외 패키지 특가, 여행 쇼츠</span>'
                       '<i style="background-image:url(/assets/art/hl/cs-trip.svg)"></i></a></li>')
# 하단 '다른 분류' 타일 라벨을 새 이름으로 교체 (아이콘·그라데이션은 유지)
for _u, _nm in CANON_RENAME.items():
    if _u in canon:
        canon[_u] = re.sub(r'<b>.*?</b>', '<b>' + _nm + '</b>', canon[_u], count=1)
k = 0
for c, _ in CATBAR:
    p = os.path.join(root, c, 'index.html')
    if not os.path.exists(p):
        continue
    s = open(p, encoding='utf-8').read()
    m = REL_RE.search(s)
    if not m:
        continue
    lis = ''.join(canon[f'/{o}/'] for o, _ in CATBAR if o != c and f'/{o}/' in canon)
    s2 = s[:m.start(2)] + lis + s[m.end(2):]
    if s2 != s:
        open(p, 'w', encoding='utf-8').write(s2); k += 1
print('other-category rows unified:', k, 'cards:', len(canon))

# ── 검색 품질: 구글 노출이 거의 없는 대량 자동 생성 하위 페이지는 구글 색인에서만 제외(googlebot noindex,follow)하고
#    사이트맵에서 뺀다. 네이버 등 다른 검색엔진과 사이트 안 이용은 그대로. 허브(index.html)는 유지.
# ── 공휴일·24절기·띠: 페이지마다 다른 유래·풍습 설명 추가 (build/enrich_cal.py), 사진은 assets/photo/cal/<키>.webp 가 있으면 표시
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enrich_cal as _ec
def _photo(key, alt):
    for ext in ('webp', 'jpg'):
        if os.path.exists(os.path.join(root, 'assets', 'photo', 'cal', key + '.' + ext)):
            return (f'<figure class="calph"><img src="/assets/photo/cal/{key}.{ext}" alt="{alt}" width="1344" height="756" '
                    f'loading="lazy" decoding="async"></figure>')
    return ''
_CALPH_CSS = ('<style id="hl-calph">.calph{margin:18px 0;padding:0}.calph img{display:block;width:100%;height:auto;border-radius:14px}</style>')
_SRC_EK = '<li><a href="https://encykorea.aks.ac.kr/" rel="noopener" target="_blank">한국민족문화대백과사전</a> ‘{n}’ 항목</li>'
_SRC_FK = '<li><a href="https://folkency.nfm.go.kr/" rel="noopener" target="_blank">국립민속박물관 한국세시풍속사전</a></li>'
_SRC_LAW = '<li><a href="https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B4%80%EA%B3%B5%EC%84%9C%EC%9D%98%EA%B3%B5%ED%9C%B4%EC%9D%BC%EC%97%90%EA%B4%80%ED%95%9C%EA%B7%9C%EC%A0%95" rel="noopener" target="_blank">국가법령정보센터 「관공서의 공휴일에 관한 규정」</a></li>'
def _ins(rel, sec):
    p = os.path.join(root, rel)
    if not os.path.exists(p): return 0
    s = open(p, encoding='utf-8').read()
    if 'class="card guide more"' in s: return 0
    if 'calph' in sec and 'hl-calph' not in s: s = s.replace('</head>', _CALPH_CSS + '</head>', 1)
    i = s.find('<section class="card guide">')
    if i < 0: return 0
    j = s.find('</section>', i) + len('</section>')
    open(p, 'w', encoding='utf-8').write(s[:j] + sec + s[j:]); return 1
_k = 0
for key, (n, mean, cust, tip) in _ec.J.items():
    lis = ''.join(f'<li>{x}</li>' for x in cust)
    _k += _ins(f'calendar/jeolgi/{key}.html', f'<section class="card guide more"><h2>{n}, 더 알아보기</h2>{_photo("jeolgi-"+key, n+" 무렵 풍경")}<p>{mean}</p><h3>{n} 풍습과 제철 이야기</h3><ul>{lis}</ul>{_photo("jeolgi-"+key+"-2", n+" 무렵 모습")}<p class="note">{tip}</p><h3>참고한 자료</h3><ul class="src">{_SRC_EK.format(n=n)}{_SRC_FK}</ul></section>')
for key, (n, ji, tm, dr, sym) in _ec.T.items():
    _k += _ins(f'calendar/tti/{key}.html', f'<section class="card guide more"><h2>{n}띠 이야기</h2>{_photo("tti-"+key, n+" 그림")}<ul><li><b>12지</b>: {ji}</li><li><b>옛 시각</b>: {tm}</li><li><b>방위</b>: {dr}</li></ul><p>{sym}</p>{_photo("tti-"+key+"-2", n+"띠 민화")}<p class="note">띠별 성격이나 운세는 전해 오는 민속 이야기로, 과학적 근거는 없어요.</p><h3>참고한 자료</h3><ul class="src">{_SRC_EK.format(n="십이지")}</ul></section>')
for key, (n, mean, pts) in _ec.H.items():
    lis = ''.join(f'<li>{x}</li>' for x in pts)
    _k += _ins(f'calendar/holiday/2027-{key}.html', f'<section class="card guide more"><h2>{n}, 어떤 날일까요?</h2>{_photo("holiday-"+key, n+" 풍경")}<p>{mean}</p><ul>{lis}</ul>{_photo("holiday-"+key+"-2", n+" 모습")}<h3>참고한 자료</h3><ul class="src">{_SRC_EK.format(n=n)}{_SRC_LAW}</ul></section>')
print('calendar enrich sections:', _k)
# 내용이 짧아 빌드에서 noindex 됐던 2027년 공휴일 페이지는, 설명을 채운 뒤 색인·사이트맵에 다시 넣는다
_k, _add = 0, []
for key in _ec.H:
    p = os.path.join(root, 'calendar', 'holiday', f'2027-{key}.html')
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    if '<meta name="robots" content="noindex">' in s and 'class="card guide more"' in s:
        open(p, 'w', encoding='utf-8').write(s.replace('<meta name="robots" content="noindex">', '', 1)); _k += 1
    _add.append(f'https://honglife.co.kr/calendar/holiday/2027-{key}.html')
p = os.path.join(root, 'sitemap.xml')
if os.path.exists(p):
    s = open(p, encoding='utf-8').read()
    new = [u for u in _add if f'<loc>{u}</loc>' not in s]
    if new:
        s = s.replace('</urlset>', ''.join(f'<url><loc>{u}</loc><lastmod>2026-11-20</lastmod></url>\n' for u in new) + '</urlset>', 1)
        open(p, 'w', encoding='utf-8').write(s)
    print('holiday 2027 reindexed:', _k, 'sitemap +', len(new))

# ── 허브 제목 '도구 도구 모음' 오타
_k = 0
for d in ('pdf', 'image', 'text', 'dev'):
    p = os.path.join(root, d, 'index.html')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read(); s2 = s.replace('도구 도구 모음', '도구 모음')
        if s2 != s: open(p, 'w', encoding='utf-8').write(s2); _k += 1
print('hub title fix:', _k)

THIN = ['text/emoji', 'text/romanize', 'text/symbol', 'life/length', 'life/weight', 'life/temp', 'life/pyeong',
        'calendar/worldtime', 'dev/color', 'dev/mime', 'dev/http',
        # 숫자만 바뀌는 대량 페이지(AdSense 재심사 대비, 승인 뒤 묶음별로 다시 열 예정)
        'study/grade', 'shop/fee', 'calendar/born', 'calendar/month', 'life/volume', 'calendar/after']
GB = '<meta name="googlebot" content="noindex,follow">'
thin_urls, k = set(), 0
for d in THIN:
    base_d = os.path.join(root, d)
    if not os.path.isdir(base_d):
        continue
    for fn in os.listdir(base_d):
        if not fn.endswith('.html') or fn == 'index.html':
            continue
        p = os.path.join(base_d, fn)
        s = open(p, encoding='utf-8').read()
        if GB not in s and '</head>' in s:
            s = s.replace('</head>', GB + '\n</head>', 1)
            open(p, 'w', encoding='utf-8').write(s); k += 1
        thin_urls.add(f'https://honglife.co.kr/{d}/{fn}')
# 공휴일은 해마다 같은 내용이라 2027년 페이지만 구글 색인, 나머지 연도는 제외
_hd = os.path.join(root, 'calendar', 'holiday')
if os.path.isdir(_hd):
    for fn in os.listdir(_hd):
        if fn.endswith('.html') and fn != 'index.html' and not fn.startswith('2027-'):
            p = os.path.join(_hd, fn); s = open(p, encoding='utf-8').read()
            if GB not in s and '</head>' in s:
                open(p, 'w', encoding='utf-8').write(s.replace('</head>', GB + '\n</head>', 1)); k += 1
            thin_urls.add(f'https://honglife.co.kr/calendar/holiday/{fn}')
p = os.path.join(root, 'sitemap.xml')
s = open(p, encoding='utf-8').read()
lines = s.split('\n')
keep = [l for l in lines if not (l.startswith('<url><loc>') and l[len('<url><loc>'):l.find('</loc>')] in thin_urls)]
open(p, 'w', encoding='utf-8').write('\n'.join(keep))
print('thin pages googlebot-noindex:', k, 'sitemap removed:', len(lines) - len(keep))

# ── 이용약관 페이지 (/terms.html) — 개인정보처리방침 페이지 틀을 그대로 써서 만든다 (2026-11-20)
_pp = os.path.join(root, 'privacy.html')
if os.path.exists(_pp):
    s = open(_pp, encoding='utf-8').read()
    T_TITLE = '이용약관 | 홍라이프 도구'
    T_DESC = '홍라이프 도구(honglife.co.kr) 이용약관 — 무료 서비스 범위, 결과의 이용과 책임, 금지 행위, 광고, 문의 방법.'
    body = ('<main class="wrap"><header class="top"><p class="crumb"><a href="/">홈</a></p><h1>이용<b>약관</b></h1></header><section class="card guide"><h2>이용약관</h2><p>시행일: 2026년 11월 20일</p>'
     '<h3>1. 목적</h3><p>이 약관은 홍라이프 도구(honglife.co.kr, 이하 ‘사이트’)가 제공하는 무료 도구와 안내 글(이하 ‘서비스’)을 이용하는 조건을 정해요.</p>'
     '<h3>2. 서비스</h3><ul><li>사이트의 도구는 회원가입 없이 무료로 쓸 수 있어요.</li><li>도구에 입력한 내용과 올린 파일은 서버로 전송되지 않고 이용자 기기의 브라우저 안에서 처리돼요.</li><li>사이트는 서비스 내용을 바꾸거나 일부 도구를 중단할 수 있어요.</li></ul>'
     '<h3>3. 결과의 이용과 책임</h3><ul><li>계산 결과, 서식, 안내 글은 공식 자료를 바탕으로 정확하게 만들려고 노력하지만 참고용이에요. 중요한 서류 제출, 세금·법률·의료 판단 전에는 해당 기관이나 전문가에게 꼭 확인하세요.</li><li>사이트의 내용은 법률·세무·의료 자문이 아니에요.</li><li>이용자가 입력한 내용과 그 결과를 쓰는 책임은 이용자에게 있어요. 사이트는 고의 또는 중대한 과실이 없는 한 이용 결과로 생긴 손해를 책임지지 않아요.</li></ul>'
     '<h3>4. 권리</h3><ul><li>도구로 만든 결과물(문서, 이미지, 파일)은 만든 이용자의 것이에요.</li><li>사이트의 화면 디자인, 글, 그림의 권리는 사이트에 있어요. 출처를 밝힌 짧은 인용과 링크는 자유롭게 해도 돼요.</li><li>법령의 별지 서식처럼 저작권 보호 대상이 아닌 자료는 원래 출처의 조건을 따라요.</li></ul>'
     '<h3>5. 하지 말아야 할 일</h3><ul><li>자동화된 방법으로 사이트에 과도한 요청을 보내 서비스를 방해하는 행위</li><li>도구로 다른 사람의 서명·도장을 몰래 쓰거나 공문서·사문서를 거짓으로 만드는 행위</li><li>법령이나 다른 사람의 권리를 침해하는 행위</li></ul>'
     '<h3>6. 광고와 외부 링크</h3><p>사이트에는 Google 애드센스 등 제3자 광고가 표시될 수 있어요. 광고와 외부 링크로 연결된 사이트의 내용과 거래는 그 운영자의 책임이에요. 광고에 쓰이는 쿠키는 <a href="/privacy.html">개인정보처리방침</a>에서 안내해요.</p>'
     '<h3>7. 약관 변경과 문의</h3><p>약관을 바꾸면 이 페이지에 시행일과 함께 알려요. 궁금한 점이나 오류 제보는 <a href="/contact.html">문의</a> 페이지로 보내 주세요.</p></section></main>')
    i, j = s.find('<main'), s.find('</main>') + len('</main>')
    t = s[:i] + body + s[j:]
    t = re.sub(r'<title>[^<]*</title>', f'<title>{T_TITLE}</title>', t, count=1)
    t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + T_DESC, t, count=1)
    t = t.replace('https://honglife.co.kr/privacy.html', 'https://honglife.co.kr/terms.html')
    t = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + T_TITLE, t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + T_DESC, t, count=1)
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', '', t, flags=re.S)
    open(os.path.join(root, 'terms.html'), 'w', encoding='utf-8').write(t)
    sp = os.path.join(root, 'sitemap.xml'); s2 = open(sp, encoding='utf-8').read()
    if '/terms.html<' not in s2:
        open(sp, 'w', encoding='utf-8').write(s2.replace('</urlset>', '<url><loc>https://honglife.co.kr/terms.html</loc><lastmod>2026-11-20</lastmod></url>\n</urlset>', 1))
    # 모든 페이지 하단 메뉴에 이용약관 추가
    OLDF = '<a href="/privacy.html">개인정보처리방침</a><a href="/contact.html">문의</a>'
    NEWF = '<a href="/privacy.html">개인정보처리방침</a><a href="/terms.html">이용약관</a><a href="/contact.html">문의</a>'
    _k = 0
    for dp, dn, fn in os.walk(root):
        if '/.git' in dp: continue
        for f in fn:
            if not f.endswith('.html'): continue
            fp = os.path.join(dp, f)
            try: s3 = open(fp, encoding='utf-8').read()
            except Exception: continue
            OLD2 = '<a href="/privacy.html">개인정보처리방침</a><a href="https://honglifecalc.com/ko/">'
            if OLDF in s3 and NEWF not in s3:
                open(fp, 'w', encoding='utf-8').write(s3.replace(OLDF, NEWF)); _k += 1
            elif OLD2 in s3 and '/terms.html">이용약관' not in s3:
                open(fp, 'w', encoding='utf-8').write(s3.replace(OLD2, NEWF + '<a href="https://honglifecalc.com/ko/">')); _k += 1
    print('terms page + footer links:', _k)

# ── 옛 계산기 주소(예전에 이 도메인에서 운영) → honglifecalc.com 이동 페이지. 없는 파일만 만든다 (2026-11-20)
import gzip as _gz
_cp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'com_paths.txt.gz')
if os.path.exists(_cp):
    _k = 0
    for cp in _gz.open(_cp).read().decode().split('\n'):
        if not cp: continue
        local = cp[3:] if cp.startswith('ko/') else cp
        fp = os.path.join(root, local)
        if os.path.exists(fp): continue
        url = 'https://honglifecalc.com/' + cp
        msg = (f'<p>이 계산기는 <a href="{url}">홍라이프 계산기</a>로 옮겼어요.</p>' if cp.startswith('ko/')
               else f'<p>This page moved to <a href="{url}">{url}</a></p>')
        ttl = '홍라이프 계산기로 이동했어요' if cp.startswith('ko/') else 'Moved to honglifecalc.com'
        os.makedirs(os.path.dirname(fp) or root, exist_ok=True)
        open(fp, 'w', encoding='utf-8').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>{ttl}</title><link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={url}"><script>location.replace("{url}"+location.search+location.hash)</script></head><body>{msg}</body></html>')
        _k += 1
    print('old calculator redirect stubs:', _k)
# 404 페이지: 목록에 없던 옛 주소도 계산기 사이트로 보낸다 (칼로리 → 칼로리 계산기, 나라 코드 경로 → 같은 주소)
_p4 = os.path.join(root, '404.html')
if os.path.exists(_p4):
    s = open(_p4, encoding='utf-8').read()
    if 'hl-old-redirect' not in s:
        js = ('<script id="hl-old-redirect">(function(){var p=location.pathname,m=p.match(/^\\/([a-z]{2})\\//);'
              'if(/^\\/kcal\\//.test(p)){location.replace("https://honglifecalc.com/ko/calorie.html");return}'
              'if(m&&m[1]!=="en"){location.replace("https://honglifecalc.com"+p+location.search)}})();</script>')
        open(_p4, 'w', encoding='utf-8').write(s.replace('</head>', js + '</head>', 1)); print('404 old-address redirect added')

# ── 앱 설치(PWA): 모든 페이지에 매니페스트·설치 스크립트 연결 (2026-11-20) ──
PWA = ('<link rel="manifest" href="/manifest.webmanifest">'
       '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
       '<meta name="apple-mobile-web-app-title" content="홍라이프"><meta name="apple-mobile-web-app-status-bar-style" content="default">'
       '<script src="/assets/js/hl-install.js?v=5" defer></script>\n')
k = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        try:
            s = open(p, encoding='utf-8').read()
        except Exception:
            continue
        if 'rel="manifest"' in s or '</head>' not in s:
            continue
        open(p, 'w', encoding='utf-8').write(s.replace('</head>', PWA + '</head>', 1)); k += 1
print('pwa head:', k)

# ── 네이버 대비 정리 (2026-11-20): RSS에 새 페이지 추가, 이미지 사이트맵을 본 사이트맵과 맞춤, 홈에 RSS 링크
import html as _h, email.utils as _eu, time as _tm
_rp = os.path.join(root, 'rss.xml')
if os.path.exists(_rp):
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'newcats'))
        from gov_data3 import F as _F3
        _new = [(f'https://honglife.co.kr/gov/{g["slug"]}.html', g['h1'], g['desc']) for g in _F3]
    except Exception as e:
        print('rss gov load fail', e); _new = []
    _new.append(('https://honglife.co.kr/terms.html', '이용약관', '홍라이프 도구 이용약관 — 무료 서비스 범위, 결과의 이용과 책임, 금지 행위, 광고, 문의 방법.'))
    s = open(_rp, encoding='utf-8').read()
    _pd = 'Fri, 20 Nov 2026 01:00:00 GMT'
    add = ''.join(f'<item><title>{_h.escape(t)}</title><link>{u}</link><guid isPermaLink="true">{u}</guid><description>{_h.escape(d)}</description><pubDate>{_pd}</pubDate></item>\n'
                  for u, t, d in _new if f'<link>{u}</link>' not in s)
    if add:
        i = s.find('<item>')
        s = s[:i] + add + s[i:]
        items = re.findall(r'<item>.*?</item>\n?', s, flags=re.S)
        if len(items) > 50:
            for it in items[50:]: s = s.replace(it, '', 1)
        s = re.sub(r'<lastBuildDate>[^<]*</lastBuildDate>', '<lastBuildDate>' + _eu.formatdate(usegmt=True) + '</lastBuildDate>', s, count=1)
        open(_rp, 'w', encoding='utf-8').write(s)
    print('rss new items:', add.count('<item>'))
_sm = os.path.join(root, 'sitemap.xml'); _si = os.path.join(root, 'sitemap-images.xml')
if os.path.exists(_sm) and os.path.exists(_si):
    keep = set(re.findall(r'<loc>([^<]+)</loc>', open(_sm, encoding='utf-8').read()))
    s = open(_si, encoding='utf-8').read()
    blocks = re.findall(r'<url>.*?</url>\s*', s, flags=re.S); n0 = len(blocks); out = s
    for b in blocks:
        m = re.search(r'<loc>([^<]+)</loc>', b)
        if m and m.group(1) not in keep: out = out.replace(b, '', 1)
    open(_si, 'w', encoding='utf-8').write(out)
    print('image sitemap', n0, '->', len(re.findall(r'<url>', out)))
_ih = os.path.join(root, 'index.html')
if os.path.exists(_ih):
    s = open(_ih, encoding='utf-8').read()
    if 'application/rss+xml' not in s:
        open(_ih, 'w', encoding='utf-8').write(s.replace('</head>', '<link rel="alternate" type="application/rss+xml" title="홍라이프 도구 새 도구" href="https://honglife.co.kr/rss.xml">\n</head>', 1))
        print('home rss link added')

# 한글(HWP) 도구 4종 (overlay/pdf, build/hwp/gen_hwp_tools.py) — PDF 허브 카드, 기존 HWP 페이지 연결, 사이트맵
_hwp_new = [('/pdf/hwp-to-hwpx.html', 'HWP를 HWPX로 변환', '옛 한글 파일을 새 형식으로, 여러 개 ZIP'),
            ('/pdf/hwpx-to-hwp.html', 'HWPX를 HWP로 변환', '옛 버전 한글에서도 열리게'),
            ('/pdf/hwp-to-txt.html', 'HWP 텍스트 추출', '글자만 TXT로, 글자 수·원고지 매수'),
            ('/pdf/text-to-hwp.html', '텍스트·워드를 한글 파일로', 'TXT·DOCX → HWP·HWPX 만들기'),
            ('/pdf/hwp-to-image.html', 'HWP를 그림(PNG·JPG)으로', '쪽마다 한 장, 카톡·블로그용'),
            ('/pdf/hwp-to-docx.html', 'HWP를 워드(DOCX)로', '워드·구글 문서에서 열리게'),
            ('/pdf/excel-to-hwp.html', '엑셀·CSV를 한글 표로', '복사한 표도 HWP 표로'),
            ('/pdf/hwp-table-to-excel.html', 'HWP 표를 엑셀로', '문서 안 표를 XLSX·CSV로'),
            ('/pdf/hwp-image-extract.html', 'HWP 그림 꺼내기', '넣은 사진을 원본 그대로'),
            ('/pdf/hwp-password.html', 'HWP 암호 걸기·풀기', '보내기 전 열기 암호, 아는 암호 풀기'),
            ('/pdf/hwp-compare.html', '한글 문서 비교', '두 파일의 달라진 줄 찾기'),
            ('/pdf/hwp-privacy-check.html', 'HWP 개인정보 찾기', '주민번호·전화번호 확인'),
            ('/pdf/hwp-info.html', '한글 문서 정보·글꼴 확인', '버전·쪽 수·쓴 글꼴'),
            ('/pdf/hwp-shortcuts.html', '한글 단축키 모음', '표·쪽 번호·저장 단축키, 인쇄용')]
_hwp_all = [('/pdf/hwp-viewer.html', 'HWP 뷰어 (한글 파일 열기)', '한컴오피스 없이 HWP·HWPX 보기'),
            ('/pdf/hwp-to-pdf.html', 'HWP를 PDF로 변환', '여러 개 한 번에, 검색되는 PDF')] + _hwp_new
_p = os.path.join(root, 'pdf/index.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read()
    if 'id="hwp-tools"' not in s:
        card = ('<section class="card" id="hwp-tools"><h2>한글(HWP) 문서 도구 ' + str(len(_hwp_all)) + '가지</h2><ul class="tlist hl-grid">'
                + ''.join(f'<li><a href="{u}"><i class="th"><img src="/assets/art/hl/cs-hwp-{u.rsplit("/", 1)[1][:-5]}.svg" alt="" width="200" height="140" loading="lazy"></i><img class="pg" src="/assets/art/hl/pg-doc.svg" alt="" width="26" height="26" loading="lazy"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in _hwp_all) + '</ul></section>\n')
        s = s.replace('<section class="card"><h2>PDF 도구', card + '<section class="card"><h2>PDF 도구', 1)
        open(_p, 'w', encoding='utf-8').write(s); print('pdf hub: hwp card')
for _f in ('pdf/hwp-viewer.html', 'pdf/hwp-to-pdf.html', 'convert/ext/hwp.html', 'convert/ext/hwpx.html', 'doc/gongmun-checker.html'):
    _p = os.path.join(root, _f)
    if not os.path.exists(_p):
        continue
    s = open(_p, encoding='utf-8').read()
    if 'hwp-shortcuts.html' in s or '</main>' not in s:
        continue
    box = ('<section class="card rel"><h2>한글(HWP) 파일 바꾸기·만들기</h2><ul>'
           + ''.join(f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in _hwp_new) + '</ul></section>\n')
    open(_p, 'w', encoding='utf-8').write(s.replace('</main>', box + '</main>', 1)); print('hwp links ->', _f)
_p = os.path.join(root, 'sitemap.xml'); s = open(_p, encoding='utf-8').read()
_add = [u for u, _, _ in _hwp_new if f'https://honglife.co.kr{u}<' not in s]
if _add:
    s = s.replace('</urlset>', ''.join(f'<url><loc>https://honglife.co.kr{u}</loc><lastmod>2026-11-24</lastmod></url>\n' for u in _add) + '</urlset>', 1)
    open(_p, 'w', encoding='utf-8').write(s); print('sitemap + hwp tools', len(_add))

# 한국사능력검정 기출·급수 (/ipsi/hanneung.html, overlay, build/newpages/gen_hanneung.py) — 입시 허브, 사이트맵
_p = os.path.join(root, 'ipsi', 'index.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read()
    _m = re.search(r'<ul class="tlist[^"]*">', s)
    if '/ipsi/hanneung.html' not in s and _m:
        s = s[:_m.end()] + '<li><a href="/ipsi/hanneung.html"><i class="th"><img src="/assets/art/hl/cs-ipsi.svg" alt="" width="200" height="140" loading="lazy"></i><img class="pg" src="/assets/art/hl/pg-ipsi.svg" alt="" width="26" height="26" loading="lazy"><b>한국사능력검정시험 기출·급수 기준</b><span>57~80회 기출 받는 곳, 점수별 1~6급, 2027 시험 일정</span></a></li>' + s[_m.end():]
        s = re.sub(r'입시 도구 (\d+)가지', lambda m: f'입시 도구 {int(m.group(1)) + 1}가지', s, count=1)
        s = s.replace('"hasPart":[', '"hasPart":[{"@type":"WebApplication","name":"한국사능력검정시험 기출·급수 기준","url":"https://honglife.co.kr/ipsi/hanneung.html"},', 1)
        open(_p, 'w', encoding='utf-8').write(s); print('ipsi hub: hanneung added')
_p = os.path.join(root, 'calendar', 'exam-schedule.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read()
    if '/ipsi/hanneung.html' not in s and '</main>' in s:
        open(_p, 'w', encoding='utf-8').write(s.replace('</main>', '<section class="card rel"><h2>한국사능력검정 자세히</h2><ul><li><a href="/ipsi/hanneung.html"><b>한국사능력검정시험 기출·급수 기준</b><span>회차별 기출 받는 곳, 점수별 급수, 2027 일정</span></a></li></ul></section>\n</main>', 1)); print('exam-schedule -> hanneung link')
_p = os.path.join(root, 'sitemap.xml'); s = open(_p, encoding='utf-8').read()
if '/ipsi/hanneung.html<' not in s:
    open(_p, 'w', encoding='utf-8').write(s.replace('</urlset>', '<url><loc>https://honglife.co.kr/ipsi/hanneung.html</loc><lastmod>2026-11-24</lastmod></url>\n</urlset>', 1)); print('sitemap + hanneung')

# 입시·시험 4종 (공무원 9급·검정고시·JLPT·토익 Part5, build/newpages/gen_exam4.py) — 입시 허브, 사이트맵
_EXAM4 = [
  ('/ipsi/gong9.html', '공무원 9급 기출문제', '국가직·지방직 기출 받는 법, 직렬별 전문과목', '공무원 9급 기출문제', '2026-11-27'),
  ('/ipsi/gumjeong.html', '검정고시 기출·합격 계산', '초·중·고졸 기출, 평균 60점 합격 판정기', '검정고시 기출·합격 계산', '2026-11-27'),
  ('/ipsi/jlpt.html', 'JLPT 공식 샘플·합격 판정', 'N1~N5 샘플문제, 영역별 합격점 계산기', 'JLPT 공식 샘플·합격 판정', '2026-11-27'),
  ('/ipsi/toeic-part5.html', '토익 Part 5 연습 10문항', '문법·어휘 오리지널 문제, 해설·채점', '토익 Part 5 연습 10문항', '2026-11-27'),
  ('/ipsi/imyong.html', '교원임용 선발·경쟁률·합격선', '중등·초등 연도별 선발 추이, 지역별 합격선 확인', '교원임용 선발·경쟁률·합격선', '2026-11-27'),
  ('/ipsi/omr.html', 'OMR 모의고사 채점기', '기출 시간 맞춰 풀고 OMR 마킹·자동 채점', 'OMR 모의고사 채점기', '2026-11-28'),
]
_p = os.path.join(root, 'ipsi', 'index.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read()
    for _u, _t, _d, _nm, _lm in _EXAM4:
        _m = re.search(r'<ul class="tlist[^"]*">', s)
        if _u not in s and _m:
            s = s[:_m.end()] + f'<li><a href="{_u}"><i class="th"><img src="/assets/art/hl/cs-ipsi.svg" alt="" width="200" height="140" loading="lazy"></i><img class="pg" src="/assets/art/hl/pg-ipsi.svg" alt="" width="26" height="26" loading="lazy"><b>{_t}</b><span>{_d}</span></a></li>' + s[_m.end():]
            s = re.sub(r'입시 도구 (\d+)가지', lambda m: f'입시 도구 {int(m.group(1)) + 1}가지', s, count=1)
            s = s.replace('"hasPart":[', f'"hasPart":[{{"@type":"WebApplication","name":"{_nm}","url":"https://honglife.co.kr{_u}"}},', 1)
    open(_p, 'w', encoding='utf-8').write(s); print('ipsi hub: exam4 added')
_p = os.path.join(root, 'sitemap.xml'); s = open(_p, encoding='utf-8').read()
for _u, _t, _d, _nm, _lm in _EXAM4:
    if f'{_u}<' not in s:
        s = s.replace('</urlset>', f'<url><loc>https://honglife.co.kr{_u}</loc><lastmod>{_lm}</lastmod></url>\n</urlset>', 1)
open(_p, 'w', encoding='utf-8').write(s); print('sitemap + exam4')

# 홈·분류 첫 화면: 제목·소개 글 작게, 그림 하나, '파일은 서버로…' 문구 빼기 (2026-11-25 사용자 요청)
_SAFE_RE = re.compile(r'\s*<div class="safe">.*?파일은 서버로 전송되지 않고 내 기기에서만 처리돼요</div>', re.S)
_p = os.path.join(root, 'index.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read()
    if 'hl-hero-m' not in s and '<section class="hero" id="search">' in s:
        # 히어로: 정적 일러스트 대신 모션그래픽(궤도 오브) — 2026-11-28 사용자 요청
        HM = ('<div class="hl-hero-m" aria-hidden="true"><svg viewBox="0 0 320 180" xmlns="http://www.w3.org/2000/svg">'
              '<defs><radialGradient id="hmO" cx="50%" cy="42%" r="60%"><stop offset="0" stop-color="#6E9BFF"/>'
              '<stop offset="55%" stop-color="#4F7CFF" stop-opacity=".55"/><stop offset="100%" stop-color="#4F7CFF" stop-opacity="0"/></radialGradient>'
              '<linearGradient id="hmR" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4F7CFF"/><stop offset="1" stop-color="#38BDF8"/></linearGradient></defs>'
              '<g class="hm-orb"><circle cx="160" cy="90" r="50" fill="url(#hmO)"/></g>'
              '<g class="hm-ring r1"><ellipse cx="160" cy="90" rx="86" ry="34" fill="none" stroke="url(#hmR)" stroke-opacity=".5" stroke-width="1.6"/></g>'
              '<g class="hm-ring r2"><ellipse cx="160" cy="90" rx="52" ry="80" fill="none" stroke="#38BDF8" stroke-opacity=".4" stroke-width="1.4"/></g>'
              '<g class="hm-ring r3"><circle cx="160" cy="90" r="30" fill="none" stroke="#A78BFA" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="3 6"/></g>'
              '<g class="hm-orbit o1"><circle cx="246" cy="90" r="5.5" fill="#4F7CFF"/></g>'
              '<g class="hm-orbit o2"><circle cx="160" cy="10" r="4.5" fill="#38BDF8"/></g>'
              '<g class="hm-orbit o3"><circle cx="108" cy="90" r="4" fill="#A78BFA"/></g>'
              '<g class="hm-spark"><circle cx="60" cy="40" r="2" fill="#4F7CFF"/><circle cx="262" cy="150" r="2.4" fill="#38BDF8"/><circle cx="250" cy="34" r="1.8" fill="#A78BFA"/></g>'
              '</svg></div>')
        s = s.replace('<section class="hero" id="search"><h1>', '<section class="hero" id="search">' + HM + '<h1>', 1)
        i = s.find('<section class="hero" id="search">'); j = s.find('</section>', i)
        s = s[:i] + _SAFE_RE.sub('', s[i:j], count=1) + s[j:]
        css = ('<style>.hero .hl-hero-m{display:block;width:min(300px,78%);height:auto;margin:2px auto 8px}'
               '.hero .hl-hero-m svg{width:100%;height:auto;overflow:visible;display:block}'
               '.hero h1{font-size:clamp(26px,5.4vw,36px)!important;line-height:1.2;margin-top:0}'
               '.hero>p{font-size:15px!important;line-height:1.6}@media(min-width:900px){.hero .hl-hero-m{width:320px}}'
               '.hm-orb{transform-box:fill-box;transform-origin:center;animation:hmBr 6s ease-in-out infinite}'
               '.hm-ring,.hm-orbit{transform-box:view-box;transform-origin:160px 90px}'
               '.hm-ring.r1{animation:hmSp 20s linear infinite}.hm-ring.r2{animation:hmSp 26s linear infinite reverse}.hm-ring.r3{animation:hmSp 16s linear infinite}'
               '.hm-orbit.o1{animation:hmSp 9s linear infinite}.hm-orbit.o2{animation:hmSp 13s linear infinite reverse}.hm-orbit.o3{animation:hmSp 11s linear infinite}'
               '.hm-spark circle{animation:hmTw 3s ease-in-out infinite}'
               '@keyframes hmBr{0%,100%{transform:scale(1);opacity:.92}50%{transform:scale(1.09);opacity:1}}'
               '@keyframes hmSp{to{transform:rotate(360deg)}}@keyframes hmTw{0%,100%{opacity:.3}50%{opacity:1}}'
               '@media(prefers-reduced-motion:reduce){.hm-orb,.hm-ring,.hm-orbit,.hm-spark circle{animation:none!important}}</style>')
        s = s.replace('</head>', css + '</head>', 1)
        open(_p, 'w', encoding='utf-8').write(s); print('home: hero motion graphic')
_ART = {k: 'ln-' + k for k in ('ai', 'calendar', 'convert', 'design', 'dev', 'doc', 'excel', 'image', 'ipsi', 'legal', 'life', 'medical', 'net', 'pdf', 'qr', 'sheet', 'shop', 'study', 'text', 'drive')}  # 선 그림
_HUBCSS = ('<style>.top.hub .hub-art{display:block;width:84px;height:63px;padding:16px 20px;box-sizing:content-box;background:#fff;'
           'border:1px solid rgba(20,30,60,.08);border-radius:24px;box-shadow:0 10px 24px -14px rgba(16,24,48,.28);margin:6px auto 12px}'
           '.top.hub h1{font-size:clamp(24px,5vw,32px)!important;line-height:1.25}'
           '.top.hub .lead{font-size:15px!important;line-height:1.65}</style>')
_n = 0
for _d, _a in _ART.items():
    _p = os.path.join(root, _d, 'index.html')
    if not os.path.exists(_p) or not os.path.exists(os.path.join(root, 'assets/art/hl', _a + '.svg')):
        continue
    s = open(_p, encoding='utf-8').read()
    i = s.find('<header class="top hub">')
    if i < 0 or 'class="hub-art"' in s:
        continue
    j = s.find('</header>', i)
    head = _SAFE_RE.sub('', s[i:j], count=1)
    head = head.replace('<header class="top hub">', f'<header class="top hub"><img class="hub-art" src="/assets/art/hl/{_a}.svg" alt="" width="120" height="90">', 1)
    s = s[:i] + head + s[j:]
    s = s.replace('</head>', _HUBCSS + '</head>', 1)
    open(_p, 'w', encoding='utf-8').write(s); _n += 1
print('hub heads: art + smaller title', _n)

# 분류 첫 화면 소개는 2줄로 짧게(긴 원래 소개는 아래 '이 분류 안내'로 옮김), 휴대폰 도구 목록 3칸, English → EN (2026-11-25 사용자 요청)
_LEAD = {
    'ai': 'ChatGPT·Claude를 엑셀 수식, 요약, 보고서, 이미지 만들기에 바로 쓰는 법과 질문 예시예요.',
    'calendar': 'D-day, 나이, 음력 변환, 공휴일, 영업일, 타이머, 달력 인쇄까지 날짜·시간 도구예요.',
    'convert': 'CSV·엑셀·JSON, 깨진 한글, PDF, 동영상·자막·음성까지 파일 형식을 바로 바꿔요.',
    'design': '썸네일, 카드뉴스, 현수막, 초대장, 라벨을 템플릿으로 만들고 PNG·인쇄용 PDF로 받아요.',
    'dev': 'JSON 정리, 정규식, Base64·URL, 색상 코드, 파비콘, 메타 태그 등 웹 만들 때 쓰는 도구예요.',
    'doc': '견적서, 계약서, 차용증, 이력서 같은 문서를 빈칸만 채워 PDF로 바로 만들어요.',
    'excel': '하고 싶은 일을 적으면 엑셀 수식을 만들고, SUMIF·VLOOKUP 뜻도 쉽게 풀어 줘요.',
    'image': '사진 용량·크기·형식 바꾸기, 증명사진, 화질 개선, 모자이크, 글자 넣기를 바로 해요.',
    'ipsi': '수능·내신 합격 가능성, 대학별 반영비율, 수능·공무원·검정고시·한능검 기출을 모았어요.',
    'legal': '상속분, 법정이율·지연손해금, 최우선변제를 법령 기준으로 계산하고 무료 상담 창구를 안내해요.',
    'life': '사업자번호 확인, 단위 변환, 분리배출, 체크리스트, 경조사·안내문까지 생활 도구예요.',
    'medical': '영유아 검진·예방접종, 국가건강검진 대상, 반복 진료 일정을 날짜로 정리해요.',
    'net': '인터넷 속도와 자주 쓰는 사이트·앱 접속 상태를 브라우저에서 바로 확인해요.',
    'pdf': 'PDF 합치기·나누기·편집·변환·OCR과 한글(HWP) 파일 열기·바꾸기를 설치 없이 해요.',
    'qr': '주소·와이파이·명함 QR 코드와 상품 바코드를 만들고, 사진 속 QR을 읽어요.',
    'sheet': '가계부, 근무표, 장부, 급여 대장 엑셀 양식을 수식이 든 채로 바로 내려받아요.',
    'shop': '마감 정산, 배달 수수료, 출퇴근, 발주·예약 관리, 안내문·라벨까지 가게 운영 도구예요.',
    'study': '학점·내신, 시간표, 학습지, 오답 노트, 참고문헌, 면접·자소서까지 공부·취업 도구예요.',
    'text': '글자 수, 맞춤법, 로마자, 줄 정리, 특수문자, 추첨까지 글과 글자 다루는 도구예요.',
    'drive': '택시비·기름값, 중간지점, 노선 내비, 정기검사, 타이어, 도로 CCTV까지 자동차 도구예요.',
}
_n = 0
for _d, _l in _LEAD.items():
    _p = os.path.join(root, _d, 'index.html')
    if not os.path.exists(_p):
        continue
    s = open(_p, encoding='utf-8').read()
    m = re.search(r'(<header class="top hub">.*?<p class="lead">)(.*?)(</p>)', s, re.S)
    if not m or 'id="hub-about"' in s:
        continue
    old = m.group(2)
    s = s[:m.start(2)] + html.escape(_l, quote=False) + s[m.end(2):]
    k = s.rfind('</main>')
    if k > 0:
        s = s[:k] + f'<section class="card" id="hub-about"><h2>이 분류 안내</h2><p>{old}</p></section>\n' + s[k:]
    open(_p, 'w', encoding='utf-8').write(s); _n += 1
print('hub leads shortened', _n)

_GRIDCSS = ('<style>@media(max-width:600px){ul.hl-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:8px!important}'
            'ul.hl-grid>li>a{border-radius:14px!important}ul.hl-grid .th{height:74px!important;padding:8px 8px 0!important}'
            'ul.hl-grid .pg{display:none!important}ul.hl-grid b{font-size:12.5px!important;line-height:1.35!important;margin:7px 8px 9px!important}'
            'ul.hl-grid>li>a>span{display:none!important}ul.hl-grid li.ft{grid-column:1/-1}ul.hl-grid li.ft>a>span,ul.hl-grid li.ft b{display:-webkit-box!important}}</style>')
_LANGRE = re.compile(r'(<a class="lang"[^>]*?)>English</a>')
_g = _e = 0
for _dp, _dn, _fs in os.walk(root):
    if '/assets' in _dp.replace(root, '', 1):
        continue
    for _f in _fs:
        if not _f.endswith('.html'):
            continue
        _p = os.path.join(_dp, _f)
        s = open(_p, encoding='utf-8').read(); o = s
        if 'class="tlist hl-grid"' in s and 'ul.hl-grid{grid-template-columns:repeat(3' not in s:
            s = s.replace('</head>', _GRIDCSS + '</head>', 1); _g += 1
        if '>English</a>' in s:
            s2 = _LANGRE.sub(lambda m: m.group(1) + ' aria-label="English" title="English">EN</a>', s)
            if s2 != s:
                s = s2; _e += 1
        if s != o:
            open(_p, 'w', encoding='utf-8').write(s)
print('mobile 3-col grid pages', _g, '· English→EN pages', _e)

# 홈: 소개 2줄, 휴대폰에서 '분류별로 찾기' 3칸 격자 (2026-11-25)
_p = os.path.join(root, 'index.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read()
    if 'hl-catrow3' not in s:
        s = re.sub(r'(<section class="hero" id="search">.*?</h1>)<p>.*?</p>',
                   lambda m: m.group(1) + '<p>엑셀·PDF·한글·이미지·문서 도구 1050가지를 가입·설치 없이 무료로 바로 써요.</p>', s, count=1, flags=re.S)
        s = s.replace('</head>', '<style id="hl-catrow3">@media(max-width:600px){ul.hl-catrow{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:8px!important;overflow:visible!important;padding:4px 0 8px!important}'
                      'ul.hl-catrow>li{flex:none!important;min-width:0}ul.hl-catrow a.ct{height:148px!important;border-radius:14px!important}'
                      'ul.hl-catrow a.ct .ch{padding:10px 10px 0!important}ul.hl-catrow a.ct em{font-size:10.5px!important}'
                      'ul.hl-catrow a.ct b{font-size:13px!important;line-height:1.3!important;display:-webkit-box!important;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden!important}'
                      'ul.hl-catrow a.ct .ci{top:50%!important;bottom:8px!important;left:8px!important;right:8px!important}ul.hl-catrow a.ct .go{display:none!important}'
                      '.hl-catrow~.rail-btn,.hl-catrow+button{display:none!important}}</style></head>', 1)
        open(_p, 'w', encoding='utf-8').write(s); print('home: 2-line intro, 3-col categories on phone')


# 분류 이름: PDF 도구 → 한글·PDF (한글 도구를 PDF 분류에 함께 둠, 2026-11-25)
_p = os.path.join(root, 'pdf', 'index.html')
if os.path.exists(_p):
    s = open(_p, encoding='utf-8').read(); o = s
    s = s.replace('<h1>PDF 도구</h1>', '<h1>한글·PDF 도구</h1>', 1).replace('› PDF 도구</p>', '› 한글·PDF</p>', 1)
    s = re.sub(r'<title>PDF 도구', '<title>한글(HWP)·PDF 도구', s, count=1)
    if s != o:
        open(_p, 'w', encoding='utf-8').write(s); print('pdf hub renamed 한글·PDF')
_c = 0
for _dp, _dn, _fs in os.walk(root):
    if '/assets' in _dp.replace(root, '', 1):
        continue
    for _f in _fs:
        if not _f.endswith('.html'):
            continue
        _p = os.path.join(_dp, _f); s = open(_p, encoding='utf-8').read(); o = s
        s = s.replace('<a href="/pdf/">PDF</a>', '<a href="/pdf/">한글·PDF</a>').replace('<a href="/pdf/" aria-current="page">PDF</a>', '<a href="/pdf/" aria-current="page">한글·PDF</a>')
        s = s.replace('<em>' , '<em>', 0)
        s = re.sub(r'(<a class="ct" href="/pdf/"[^>]*><span class="ch"><em>[^<]*</em><b>)PDF 도구(</b>)', r'\1한글·PDF\2', s)
        s = s.replace('<a href="/pdf/">PDF 도구</a>', '<a href="/pdf/">한글·PDF</a>')
        if s != o:
            open(_p, 'w', encoding='utf-8').write(s); _c += 1
print('nav/labels PDF → 한글·PDF', _c)
_p = os.path.join(root, 'pdf', 'index.html')
if os.path.exists(_p):
    _hub = open(_p, encoding='utf-8').read()
    _k = _hub.find('id="hwp-tools"'); _main = _hub[:_k] + _hub[_hub.find('</section>', _k):] if _k >= 0 else _hub
    _extra = sum(1 for u, _, _ in _hwp_new if f'href="{u}"' not in _main)
    _h = os.path.join(root, 'index.html'); s = open(_h, encoding='utf-8').read()
    s2 = re.sub(r'(<a class="ct" href="/pdf/"[^>]*><span class="ch"><em>)(\d+)개(</em>)', lambda m: f'{m.group(1)}{int(m.group(2)) + _extra}개{m.group(3)}', s, count=1)
    _cnt = _extra
    if s2 != s:
        open(_h, 'w', encoding='utf-8').write(s2); print('home 한글·PDF count', _cnt)

# 홈 '분류별로 찾기'를 정확히 12개(CATBAR)로 유지 — 다른 블록이 추가한 카드(드라이버·테스트·게임 등) 제거 (2026-11-28)
_KEEP12 = ['/' + _c + '/' for _c, _ in CATBAR]
for _rel in ('index.html', os.path.join('en', 'index.html')):
    _fp = os.path.join(root, _rel)
    if not os.path.exists(_fp):
        continue
    _s = open(_fp, encoding='utf-8').read()
    _m = re.search(r'(<ul class="tlist hl-cards hl-catrow">)(.*?)(</ul>)', _s, re.S)
    if not _m:
        continue
    _lis = re.findall(r'<li>.*?</li>', _m.group(2), re.S)
    def _slug(_li):
        _h = re.search(r'href="(/[a-z0-9-]+/)"', _li)
        return _h.group(1) if _h else None
    _bySlug = {}
    for _li in _lis:
        _sg = _slug(_li)
        if _sg in _KEEP12 and _sg not in _bySlug:
            _bySlug[_sg] = _li
    _kept = [_bySlug[_u] for _u in _KEEP12 if _u in _bySlug]
    if _kept and len(_kept) != len(_lis):
        _s = _s[:_m.start(2)] + ''.join(_kept) + _s[_m.end(2):]
        open(_fp, 'w', encoding='utf-8').write(_s)
        print('home grid pruned ->', len(_kept), 'cards', _rel)

# ── 설명 삽화(인라인 SVG) 안의 <title>/<desc>를 svg의 aria-label로 이전 (2026-11-28) ──
# 네이버 사이트진단이 SVG <title>을 페이지 제목으로 같이 세어 'title 2개 이상'으로 경고하는 문제 해결.
# 접근성은 aria-label로 유지(스크린리더 동일), SVG 렌더링은 변화 없음.
def _svg_aria(_block):
    _mt = re.search(r'<title\b[^>]*>(.*?)</title>', _block, re.S)
    if not _mt:
        return _block
    _md = re.search(r'<desc\b[^>]*>(.*?)</desc>', _block, re.S)
    _lab = re.sub(r'<[^>]+>', '', _mt.group(1)).strip()
    if _md:
        _lab = (_lab + ' ' + re.sub(r'<[^>]+>', '', _md.group(1)).strip()).strip()
    _lab = re.sub(r'\s+', ' ', _lab).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    _block = re.sub(r'<title\b[^>]*>.*?</title>', '', _block, count=1, flags=re.S)
    _block = re.sub(r'<desc\b[^>]*>.*?</desc>', '', _block, count=1, flags=re.S)
    def _open(_m):
        _t = re.sub(r'\s+aria-labelledby="[^"]*"', '', _m.group(0))
        if 'aria-label=' not in _t:
            _t = _t[:-1] + ' aria-label="' + _lab + '">'
        return _t
    return re.sub(r'<svg\b[^>]*>', _open, _block, count=1)
_sc = 0
for _dp, _dn, _fs in os.walk(root):
    if '/assets' in _dp.replace(root, '', 1):
        continue
    for _f in _fs:
        if not _f.endswith('.html'):
            continue
        _p = os.path.join(_dp, _f); s = open(_p, encoding='utf-8').read()
        if '<svg' not in s or '<title' not in s:
            continue
        o = re.sub(r'<svg\b.*?</svg>', lambda m: _svg_aria(m.group(0)), s, flags=re.S)
        if o != s:
            open(_p, 'w', encoding='utf-8').write(o); _sc += 1
print('svg title->aria-label:', _sc)

# ── 기출 페이지: 문제 PDF를 '그 자리에서 바로' 풀고 채점 (2026-11-28) ──
# 바로 풀 수 있는 것(직접 PDF 링크)만 인라인 '풀기' 버튼 → 누르면 페이지 안에서 좌 PDF+우 OMR 펼침(iframe embed).
# 직접 PDF가 없는 시험(포털 링크)엔 아무 버튼도 넣지 않음.
def _suneung_n(_suf):
    # 수능 파일명 접미사 → 문항수. _1 국어45, _2 수학30, _3 영어45, _41 한국사20,
    # _42/_43/_44 사회·과학·직업탐구 각20, _5 제2외국어·한문 각30
    if _suf == '1' or _suf == '3':
        return 45
    if _suf == '2':
        return 30
    if _suf.startswith('5'):
        return 30
    return 20  # 한국사·사회/과학/직업 탐구
def _suneung_t(_suf):
    # 수능 과목별 제한 시간(분)
    if _suf == '1':
        return 80   # 국어
    if _suf == '2':
        return 100  # 수학
    if _suf == '3':
        return 70   # 영어
    if _suf == '41':
        return 30   # 한국사
    if _suf.startswith('5'):
        return 40   # 제2외국어·한문
    return 30       # 사회/과학/직업 탐구 과목당
_DOCK = ('<section class="card omr-dock" id="omr-dock" hidden><style>'
         '.omr-dock{padding:10px 12px}.omr-dock-bar{display:flex;align-items:center;gap:10px;margin-bottom:8px}'
         '.omr-dock-bar b{font-size:16px}.omr-dock-bar .btn{margin-left:auto}'
         '#omr-dock-frame{width:100%;height:88vh;border:1px solid #D9DDE3;border-radius:12px;background:#fff;display:block}'
         '@media(max-width:820px){#omr-dock-frame{height:150vh}}'
         'a.omr-solve{cursor:pointer}</style>'
         '<div class="omr-dock-bar"><b>⏱ 문제 풀고 채점</b><button class="btn" id="omr-dock-x" type="button">닫기 ✕</button></div>'
         '<iframe id="omr-dock-frame" title="OMR 풀기" loading="lazy"></iframe></section>')
_DOCK_JS = ('<script>(function(){var d=document.getElementById("omr-dock");if(!d)return;var fr=document.getElementById("omr-dock-frame");'
            'document.querySelectorAll(".omr-solve").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();'
            'var p=new URLSearchParams();p.set("embed","1");["pdf","n","c","t","name"].forEach(function(k){if(a.dataset[k])p.set(k,a.dataset[k]);});'
            'fr.src="/ipsi/omr.html?"+p.toString();d.hidden=false;d.scrollIntoView({behavior:"smooth",block:"start"});});});'
            'var x=document.getElementById("omr-dock-x");if(x)x.addEventListener("click",function(){d.hidden=true;fr.src="about:blank";});})();</script>')
for _ef in ['suneung-2027.html']:  # 현재 직접 PDF가 있는 시험
    _p = os.path.join(root, 'ipsi', _ef)
    if not os.path.exists(_p) or 'omr-dock' in open(_p, encoding='utf-8').read():
        continue
    s = open(_p, encoding='utf-8').read()
    # 구조: <li><b>과목</b><span class="ql"><a ..>문제</a><a ..>정답</a>...</span></li>
    _pat = re.compile(r'(<b>([가-힣0-9Ⅰ-Ⅻ·\s]{1,14})</b><span class="ql"><a href="https://cdn\.kice\.re\.kr/27dae-suneung/27DaeSuneung_([0-9_]+)\.pdf"[^>]*>문제</a><a href="[^"]*"[^>]*>정답</a>)')
    def _add_solve(_mm):
        _label = re.sub(r'\s+', ' ', _mm.group(2)).strip()
        _suf = _mm.group(3)
        _u = 'https://cdn.kice.re.kr/27dae-suneung/27DaeSuneung_%s.pdf' % _suf
        _n = _suneung_n(_suf)
        _data = 'data-pdf="%s" data-c="5" data-n="%d" data-t="%d"' % (_u, _n, _suneung_t(_suf))
        if _label:
            _data += ' data-name="%s"' % _label
        return _mm.group(0) + '<a class="btn omr-solve" %s title="이 문제지를 바로 풀고 채점">풀기</a>' % _data
    s2 = _pat.sub(_add_solve, s)
    if s2 != s:
        # 다운로드 섹션(또는 lead) 뒤에 도크+스크립트 삽입
        _anchor = re.search(r'(<section class="card" id="exam">)', s2)
        if _anchor:
            s2 = s2[:_anchor.start()] + _DOCK + s2[_anchor.start():]
        else:
            _m = re.search(r'(<p class="lead">.*?</p>)', s2, re.S)
            if _m:
                s2 = s2[:_m.end()] + _DOCK + s2[_m.end():]
        s2 = s2.replace('</main>', _DOCK_JS + '</main>', 1) if '</main>' in s2 else s2 + _DOCK_JS
        open(_p, 'w', encoding='utf-8').write(s2)
        print('suneung: inline 풀기 + dock added')

# ── .co.kr 크롤 예산 정리: 100% 더미 폴더만 크롤 차단 + 사이트맵에서 noindex 더미 URL 제거 (2026-11-28) ──
# honglife.co.kr에는 honglifecalc.com으로 넘기는 noindex 리다이렉트 더미가 폴더째(해외 국가 ae·jp…,
# 한국어 계산기 science·saju·math·mbti…) 또는 실폴더 안에 섞여 있어 크롤 예산을 잡아먹음.
# 실페이지(한국어 전체 + 영어 en/ 162개)는 모두 유지하고, '실페이지가 하나도 없는(100% 더미) 폴더'만 차단.
# 사이트맵에서는 혹시 끼어든 noindex 더미 URL만 제거(실페이지는 그대로).
import glob as _glob2
def _is_stub(_t):
    return ('honglifecalc.com' in _t) and ('noindex' in _t)
_foreign = []
for _d in sorted(os.listdir(root)):
    _dp = os.path.join(root, _d)
    if not os.path.isdir(_dp) or _d == 'assets' or _d.startswith('.'):
        continue
    _hs = _glob2.glob(os.path.join(_dp, '**', '*.html'), recursive=True)
    if not _hs:
        continue
    _real = 0
    for _h in _hs:
        if not _is_stub(open(_h, encoding='utf-8', errors='ignore').read()):
            _real += 1
            break  # 실페이지 1개라도 있으면 폴더 차단 대상 아님
    if _real == 0:  # 폴더 전체가 더미
        _foreign.append(_d)
_rp = os.path.join(root, 'robots.txt')
if _foreign and os.path.exists(_rp):
    _r = open(_rp, encoding='utf-8').read()
    _dis = ''.join('Disallow: /%s/\n' % _d for _d in _foreign if ('Disallow: /%s/' % _d) not in _r)
    if _dis:
        if 'Allow: /\n' in _r:
            _r = _r.replace('Allow: /\n', 'Allow: /\n' + _dis, 1)
        else:
            _r = _r.replace('User-agent: *\n', 'User-agent: *\n' + _dis, 1)
        open(_rp, 'w', encoding='utf-8').write(_r)
    print('robots: blocked 100%-dummy folders', len(_foreign))
# 사이트맵: 각 URL의 대상 파일이 noindex 더미면 제거(실페이지는 유지). 영어 en/ 실페이지는 더미가 아니라 유지됨.
_smpath = os.path.join(root, 'sitemap.xml')
if os.path.exists(_smpath):
    _s = open(_smpath, encoding='utf-8').read()
    _blocks = re.findall(r'<url>.*?</url>', _s, re.S)
    def _loc_stub(_b):
        _m = re.search(r'<loc>https?://honglife\.co\.kr(/[^<]*)</loc>', _b)
        if not _m:
            return False
        _path = _m.group(1)
        _fp = os.path.join(root, _path.lstrip('/'))
        if _path.endswith('/'):
            _fp = os.path.join(root, _path.strip('/'), 'index.html')
        try:
            return _is_stub(open(_fp, encoding='utf-8', errors='ignore').read())
        except Exception:
            return False
    _keep = [_b for _b in _blocks if not _loc_stub(_b)]
    _rm = len(_blocks) - len(_keep)
    if _rm and _blocks:
        _i = _s.find('<url>'); _j = _s.rfind('</url>') + len('</url>')
        _s = _s[:_i] + ''.join(_keep) + _s[_j:]
        open(_smpath, 'w', encoding='utf-8').write(_s)
    print('sitemap: removed noindex-dummy urls', _rm)
