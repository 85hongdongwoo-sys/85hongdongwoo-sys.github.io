"""Overlay patch for honglife.co.kr: adds 입시·여행 to the top menu and the home page.
Runs in the deploy workflow after the tools bundle is unpacked into _site/."""
import os, sys, re
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

# 홈: '분류별로 찾기'를 면 분할 색 카드(큰 장면 그림) 가로 줄로
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
        out = []
        for i, mm in enumerate(re.finditer(r'<a href="/([a-z0-9-]+)/"><img[^>]*><b>(.*?)</b><em>(.*?)</em></a>', m.group(1))):
            cat, name, n = mm.groups()
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
KW = [('bus', r'노선 내비|경유지'), ('pdf', r'PDF'), ('image', r'이미지|사진|PNG|JPG|증명'), ('qr', r'QR|바코드'), ('ai', r'AI|챗GPT|클로드|프롬프트'),
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
MOVED = [('calendar', '/calendar/exam-schedule.html', '자격증 시험일정 달력 (국가기술·국가전문·한국사·토익·JLPT)', '원서접수·시험일·합격발표를 한 달력에, 매달 업데이트', '자격증 시험일정 달력 큐넷 기사 산업기사 기능사 한국사 토익 JLPT 원서접수', '날짜·달력'),
         ('life', '/life/subsidy.html', '조건으로 찾는 정부 지원금 (보조금24 1만여 건)', '지역·대상·나이·분야로 받을 수 있는 지원금만 걸러 보기', '정부 지원금 조회 보조금24 지원금 찾기 청년 지원금 소상공인 지원금 노인 지원금', '생활·행정'),
         ('drive', '/life/route-navi.html', '경유지 많은 노선 내비', '정류장 30곳 넘어도 순서대로 길안내', '경유지 많은 내비 다중 경유지 길찾기 경유지 30개 셔틀버스 노선 통학버스 택배 동선 순서 길안내', '자동차·지도'),
         ('drive', '/life/taxi-fare.html', '택시비·통행료 계산기', '택시비와 내 차 기름값·통행료 비교', '택시비 계산기 택시요금 계산 통행료 계산 고속도로 통행료 기름값 계산 유류비 계산 카카오 길찾기 거리 계산', '자동차·지도'),
         ('drive', '/life/midpoint.html', '중간지점 찾기', '친구들과 만날 곳 추천 + 공유 카드', '중간지점 찾기 약속장소 추천 중간 위치 만날 장소 친구 중간 지점 지하철역 중간 카카오 길찾기', '자동차·지도'),
         ('life', '/life/invest.html', '청약·줍줍 일정 + 투자계산기', '오늘 넣을 수 있는 청약·무순위 줍줍 3일마다 업데이트, 주식 세금·대출·연금 계산', '청약 일정 줍줍 무순위 청약 투자계산기 주식 세금 대출 한도 청약 가점', '생활·행정')]
for cat, u, n, d, kw, cn in MOVED:
    p = os.path.join(root, cat, 'index.html')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if f'href="{u}"' not in s:
            art = {'/life/route-navi.html': 'bus', '/life/taxi-fare.html': 'drive', '/life/midpoint.html': 'drive'}.get(u, cat)
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
p = os.path.join(root, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
if 'honglife.co.kr/drive/<' not in s:
    open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', '<url><loc>https://honglife.co.kr/drive/</loc><lastmod>2026-11-20</lastmod></url>\n</urlset>', 1)); print('sitemap + drive')

# ── 상단 분류 줄 고정: 모든 한국어 페이지에 같은 분류 전체 목록(가로 스크롤 한 줄) ──
CATBAR = [('excel', '엑셀 수식'), ('sheet', '엑셀 양식'), ('doc', '문서'), ('pdf', 'PDF'), ('image', '이미지'), ('convert', '파일 변환'),
          ('text', '텍스트'), ('ai', 'AI'), ('calendar', '날짜·달력'), ('qr', 'QR'), ('life', '생활·행정'), ('gov', '공문서·민원'), ('drive', '자동차·지도'), ('medical', '병원·건강'),
          ('legal', '법률'), ('study', '학생·공부'), ('ipsi', '입시'), ('trip', '여행'), ('test', '심리 테스트'), ('game', '게임 계산기'),
          ('design', '디자인'), ('shop', '소상공인'), ('dev', '개발'), ('net', '인터넷')]
CATCSS = ('<style id="hl-catbar-css">.brandbar .in nav a:not(.srch):not(.lang){display:none!important}'
          '.catbar{border-top:1px solid rgba(0,0,0,.06)}.catbar .in2{max-width:1080px;margin:0 auto;padding:7px 12px;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;'
          '-webkit-mask-image:linear-gradient(90deg,#000 92%,transparent);mask-image:linear-gradient(90deg,#000 92%,transparent)}.catbar .in2::-webkit-scrollbar{display:none}'
          '.brandbar .catbar a{display:inline-block!important;flex:none;padding:6px 12px;border-radius:999px;font-size:14px;font-weight:600;line-height:1.35;color:#4E5968;text-decoration:none;white-space:nowrap}'
          '.catbar a:hover{background:rgba(0,0,0,.05);color:#191F28}.catbar a[aria-current]{background:#191F28;color:#fff}'
          '@media(max-width:600px){.catbar .in2{padding:6px 10px}.catbar a{font-size:13.5px;padding:6px 11px}}</style>')
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
            return (f'<figure class="calph"><img src="/assets/photo/cal/{key}.{ext}" alt="{alt}" width="1200" height="675" '
                    f'loading="lazy" decoding="async" style="width:100%;height:auto;border-radius:14px"><figcaption>{alt} (AI로 만든 이미지)</figcaption></figure>')
    return ''
_SRC_EK = '<li><a href="https://encykorea.aks.ac.kr/" rel="noopener" target="_blank">한국민족문화대백과사전</a> ‘{n}’ 항목</li>'
_SRC_FK = '<li><a href="https://folkency.nfm.go.kr/" rel="noopener" target="_blank">국립민속박물관 한국세시풍속사전</a></li>'
_SRC_LAW = '<li><a href="https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B4%80%EA%B3%B5%EC%84%9C%EC%9D%98%EA%B3%B5%ED%9C%B4%EC%9D%BC%EC%97%90%EA%B4%80%ED%95%9C%EA%B7%9C%EC%A0%95" rel="noopener" target="_blank">국가법령정보센터 「관공서의 공휴일에 관한 규정」</a></li>'
def _ins(rel, sec):
    p = os.path.join(root, rel)
    if not os.path.exists(p): return 0
    s = open(p, encoding='utf-8').read()
    if 'class="card guide more"' in s: return 0
    i = s.find('<section class="card guide">')
    if i < 0: return 0
    j = s.find('</section>', i) + len('</section>')
    open(p, 'w', encoding='utf-8').write(s[:j] + sec + s[j:]); return 1
_k = 0
for key, (n, mean, cust, tip) in _ec.J.items():
    lis = ''.join(f'<li>{x}</li>' for x in cust)
    _k += _ins(f'calendar/jeolgi/{key}.html', f'<section class="card guide more"><h2>{n}, 더 알아보기</h2>{_photo("jeolgi-"+key, n+" 무렵 풍경")}<p>{mean}</p><h3>{n} 풍습과 제철 이야기</h3><ul>{lis}</ul><p class="note">{tip}</p><h3>참고한 자료</h3><ul class="src">{_SRC_EK.format(n=n)}{_SRC_FK}</ul></section>')
for key, (n, ji, tm, dr, sym) in _ec.T.items():
    _k += _ins(f'calendar/tti/{key}.html', f'<section class="card guide more"><h2>{n}띠 이야기</h2>{_photo("tti-"+key, n+" 그림")}<ul><li><b>12지</b>: {ji}</li><li><b>옛 시각</b>: {tm}</li><li><b>방위</b>: {dr}</li></ul><p>{sym}</p><p class="note">띠별 성격이나 운세는 전해 오는 민속 이야기로, 과학적 근거는 없어요.</p><h3>참고한 자료</h3><ul class="src">{_SRC_EK.format(n="십이지")}</ul></section>')
for key, (n, mean, pts) in _ec.H.items():
    lis = ''.join(f'<li>{x}</li>' for x in pts)
    _k += _ins(f'calendar/holiday/2027-{key}.html', f'<section class="card guide more"><h2>{n}, 어떤 날일까요?</h2>{_photo("holiday-"+key, n+" 풍경")}<p>{mean}</p><ul>{lis}</ul><h3>참고한 자료</h3><ul class="src">{_SRC_EK.format(n=n)}{_SRC_LAW}</ul></section>')
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
       '<script src="/assets/js/hl-install.js?v=4" defer></script>\n')
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
