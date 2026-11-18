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
          'legal': '#5C6BC0', 'study': '#1C7ED6', 'ipsi': '#364FC7', 'dev': '#343A40', 'net': '#1971C2', 'design': '#D6336C', 'shop': '#E8590C'}
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
HFC = {'excel': '#1F9D55', 'sheet': '#0CA678', 'doc': '#3B5BDB', 'pdf': '#E03131', 'image': '#7048E8', 'convert': '#1098AD',
       'text': '#F08C00', 'ai': '#6741D9', 'calendar': '#F76707', 'qr': '#495057', 'life': '#2F9E44', 'medical': '#E64980',
       'legal': '#5C6BC0', 'study': '#1C7ED6', 'ipsi': '#364FC7', 'dev': '#343A40', 'net': '#1971C2', 'design': '#D6336C', 'shop': '#E8590C'}
KW = [('pdf', r'PDF'), ('image', r'이미지|사진|PNG|JPG|증명'), ('qr', r'QR|바코드'), ('ai', r'AI|챗GPT|클로드|프롬프트'),
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
        add = ct('/test/', len(NC['test']), '심리 테스트', 'test', '#F8D7E3', '#E67FA5', '#F1A9C3') + ct('/game/', len(NC['game']), '게임 계산기', 'game', '#D3F0DA', '#6CC58A', '#A3DCB3')
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
