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
ul.hl-cards{display:flex;grid-template-columns:none;gap:14px;overflow-x:auto;scroll-snap-type:x proximity;padding:4px 2px 18px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
ul.hl-cards::-webkit-scrollbar{display:none}
ul.hl-cards>li{flex:0 0 210px;scroll-snap-align:start}
ul.hl-cards a{display:flex!important;flex-direction:column;padding:0!important;overflow:hidden;background:#fff!important;border:0!important;border-radius:18px!important;box-shadow:0 2px 10px rgba(20,30,60,.07)!important;height:100%;transition:transform .2s,box-shadow .2s}
ul.hl-cards a:hover{transform:translateY(-3px);box-shadow:0 10px 24px -8px rgba(20,30,60,.22)!important}
ul.hl-cards .th{display:block;height:146px;flex:0 0 auto;position:relative}
ul.hl-cards .th img{width:100%;height:100%;display:block}
ul.hl-cards .th .pg{position:absolute;left:10px;top:10px;width:30px;height:30px;border-radius:9px;box-shadow:0 2px 6px rgba(0,0,0,.18);filter:saturate(1.6)}
ul.hl-cards a.tx{background:var(--tc)!important;padding:18px 16px!important;justify-content:flex-start}
ul.hl-cards a.tx .pg{width:34px;height:34px;border-radius:10px;filter:saturate(1.6);box-shadow:0 2px 6px rgba(0,0,0,.15)}
ul.hl-cards a.tx b{color:#fff!important;font-size:21px!important;line-height:1.3;margin:auto 0 0!important;-webkit-line-clamp:4}
ul.hl-cards a.tx span{color:rgba(255,255,255,.92)!important;margin:8px 0 0!important;font-size:13px!important;-webkit-line-clamp:3}
h2.sec-h .tg{font-size:.82em;font-weight:600;color:#6b7280;letter-spacing:-.02em}
ul.hl-top>li{flex-basis:220px}
ul.hl-top a.tp{background:var(--tc)!important;flex-direction:column-reverse!important;justify-content:flex-end;height:300px}
ul.hl-top a.tp .th{height:auto;flex:1 1 auto;display:flex;align-items:flex-end;margin-top:auto}
ul.hl-top a.tp .th img{height:auto;transform:scale(1.15);transform-origin:bottom center}
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
ul.hl-cards li.ph a{background:var(--im) center bottom/auto 68% no-repeat,var(--tc)!important}
ul.hl-cards li.ph b,ul.hl-cards li.ph span{position:relative;z-index:1}
ul.hl-cards li.pw a{background:var(--im) center/cover no-repeat,var(--tc)!important}
ul.hl-cards li.pw a::before{content:"";position:absolute;inset:0 0 auto 0;height:55%;background:linear-gradient(rgba(0,0,0,.55),transparent);border-radius:18px 18px 0 0}
ul.hl-cards li.pw a{position:relative}
ul.hl-cards li.pw b,ul.hl-cards li.pw span{color:#fff!important}
ul.hl-cards li.fp .fi{position:absolute;left:0;right:0;bottom:0;top:96px;height:auto;margin:0;background-size:cover;background-position:center 12%;border-radius:0 0 18px 18px}
ul.hl-cards li.fp .fh{position:relative;z-index:1}
ul.hl-cards li.fp:not(.fd) .fh,ul.hl-cards li.fp:not(.fd) .fh b,ul.hl-cards li.fp:not(.fd) .fh em{color:#111!important}
ul.hl-cards li.fp .go{z-index:2}
ul.hl-cards .th{overflow:hidden}
ul.hl-cards .th img:not(.pg){transform:scale(1.32);transform-origin:center 40%}
ul.hl-cards .ft:not(.fp) .fi{position:absolute;left:-70px;right:-90px;bottom:-60px;top:40px;height:auto;margin:0;background-size:cover;background-position:center bottom}
ul.hl-cards .ft:not(.fp) a{overflow:hidden}
ul.hl-cards li.fp .fi{background-position:center 8%!important}
ul.hl-cards li.ph:not(.pw) a{background-size:auto 80%!important}
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
                return m.group(1).replace('<a ', f'<a class="tx" style="--tc:{PAL[(i + 2) % len(PAL)]}" ', 1) + '<img class="pg" src="/assets/art/cat2-' + cat + '.svg" alt="" width="34" height="34" loading="lazy">'
            if i % 5 in (0, 1, 4):
                bgc = '#fff'
            else:
                bgc = PAL[i % len(PAL)]
            if cnt[1]:
                return m.group(1).replace('<a ', f'<a class="tp" style="--tc:{TOP[i % len(TOP)]}" ', 1) + f'<i class="th"><img src="{sc}" alt="" width="200" height="140" loading="lazy"></i>'
            return f'{m.group(1)}<i class="th" style="background:{bgc}"><img src="{sc}" alt="" width="200" height="140" loading="lazy"><img class="pg" src="/assets/art/cat2-{cat}.svg" alt="" width="30" height="30" loading="lazy"></i>'
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
                    PH = [('p-woman', '#EBB7BB'), ('p-man', '#9ECDDD'), ('p-student', '#E9DA99'), ('p-office', '#87BCAC')]
                    if ri % 2 == 0:
                        ph, bc = PH[(ri // 2) % 4]
                        pers = (f'<li class="pc ph"><a href="{r[0]}" style="--tc:{bc};--im:url(/assets/art/ph/{ph}.jpg)"><b>{r[1]}</b><span>{r[2]}</span></a></li>')
                    else:
                        pers = (f'<li class="pc"><a href="{r[0]}" style="--tc:{["#FCC2D7", "#A5D8FF", "#FFEC99", "#C3FAE8"][k % 4]}"><b>{r[1]}</b><span>{r[2]}</span>'
                                f'<i class="pi" style="background-image:url(/assets/art/hl/pp-{k % 4}.svg)"></i></a></li>')
                    r = RAW[7]
                    pic = (f'<li class="pt"><a href="{r[0]}"><b>{r[1]}</b><span>{r[2]}</span>'
                           f'<i class="pi" style="background-image:url(/assets/art/hl/picto.svg)"></i></a></li>')
                    items = items[:2] + [stack] + items[4:5] + [pers] + items[6:7] + [pic] + items[8:]
                    BIG = {'study': ('il-kid', '#432115'), 'ai': ('il-monkey', '#4E7D53'), 'calendar': ('phone-dark', '#394144'), 'sheet': ('phone-green', '#028841')}
                    if cat in BIG and len(RAW) > 9:
                        r = RAW[9]; ph, bc = BIG[cat]
                        big = f'<li class="pc ph pw"><a href="{r[0]}" style="--tc:{bc};--im:url(/assets/art/ph/{ph}.jpg)"><b>{r[1]}</b><span>{r[2]}</span></a></li>'
                        items = items[:7] + [big] + items[8:]
                    lis = '<ul class="tlist">' + ''.join(items) + '</ul>'
            href = f'/{cat}/' if cat != 'pop' else '/#search'
            img = f'/assets/art/hl/ft-{cat}.svg'
            sub = f'도구 {n}가지' if cat != 'pop' else '자주 찾는 도구'
            FTPH = {'image': ('p-woman', '#EBB7BB'), 'text': ('p-man', '#9ECDDD'), 'study': ('p-student', '#E9DA99'),
                    'doc': ('p-office', '#87BCAC'), 'calendar': ('phone-dark', '#394144'), 'sheet': ('phone-green', '#028841')}
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
if 'hl-catrow' not in s:
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
                bg = f'linear-gradient(165deg,{a} 0 46%,{b} 46%)'
            else:
                bg = f'linear-gradient({a} 0 40%,transparent 40%),linear-gradient(90deg,{b} 0 58%,{d} 58%)'
            img = f'/assets/art/hl/sc-{cat}.svg'
            out.append(f'<li><a class="ct" href="/{cat}/" style="--bg:{bg}"><span class="ch"><em>{n}</em><b>{name}</b></span>'
                       f'<i class="ci" style="background-image:url({img})"></i><span class="go" aria-hidden="true">›</span></a></li>')
        s = s.replace(m.group(0), '<ul class="tlist hl-cards hl-catrow">' + ''.join(out) + '</ul>', 1)
        CSS = """<style id="hl-catrow-css">
ul.hl-catrow>li{flex:0 0 224px}
ul.hl-catrow a.ct{position:relative;height:300px;background:var(--bg)!important;border-radius:20px!important;box-shadow:none!important}
ul.hl-catrow a.ct .ch{display:block!important;margin:0!important;padding:18px 18px 0;-webkit-line-clamp:unset;overflow:visible!important}
ul.hl-catrow a.ct em{display:block;font-style:normal;font-size:12px;font-weight:700;color:#333}
ul.hl-catrow a.ct b{margin:4px 0 0!important;font-size:19px!important;color:#111!important;line-height:1.3}
ul.hl-catrow a.ct .ci{position:absolute;left:-40px;right:-40px;bottom:-30px;height:270px;background-repeat:no-repeat;background-size:contain;background-position:center bottom;transition:transform .3s}
ul.hl-catrow a.ct:hover .ci{transform:scale(1.05)}
ul.hl-catrow a.ct .go{position:absolute;right:12px;bottom:12px;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.95);color:#111;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;margin:0!important}
@media (max-width:600px){ul.hl-catrow>li{flex-basis:200px}ul.hl-catrow a.ct{height:270px}ul.hl-catrow a.ct .ci{height:180px}}
</style>"""
        s = s.replace('</head>', CSS + '\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(s); print('home: category row cards')
