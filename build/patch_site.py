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

# 홈: 상단 흰 배경 + 블루 계열 흐르는 애니메이션(가운데 정렬) / 하단 도구 목록을 그림 카드 가로 줄로
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
if 'hl-flow' not in s:
    TINT = {'excel':'#E3F0E8','sheet':'#E4F3EC','doc':'#E7EEFB','pdf':'#FBE9E7','image':'#F3E8FA','convert':'#E5F4F7',
            'text':'#F6F0E2','ai':'#ECEAFD','calendar':'#FDEEE6','qr':'#EAEEF3','life':'#E9F5E9','medical':'#FCE9EF',
            'legal':'#F1EDE6','study':'#E8F1FC','ipsi':'#E6EEFF','dev':'#E9ECF2','net':'#E4F2FA','design':'#FCEBF3','shop':'#FFF1E0'}
    CSS = '''<style id="hl-flow-css">
.hero{position:relative;overflow:hidden;background:#fff!important;background-image:none!important;text-align:center}
.hero>.hl-flow{position:absolute;inset:0;z-index:0;pointer-events:none;animation:none!important}
.hl-flow i{position:absolute;display:block;filter:blur(48px);will-change:transform,border-radius}
.hl-flow .f1{width:42%;height:62%;left:2%;top:4%;background:#2563eb;opacity:.42;animation:hlf1 20s ease-in-out infinite}
.hl-flow .f2{width:36%;height:64%;right:4%;top:0;background:#38bdf8;opacity:.45;animation:hlf2 24s ease-in-out infinite}
.hl-flow .f3{width:40%;height:52%;left:34%;bottom:-6%;background:#6366f1;opacity:.32;animation:hlf3 28s ease-in-out infinite}
@keyframes hlf1{0%,100%{transform:translate(0,0) rotate(0);border-radius:60% 40% 55% 45%/50% 60% 40% 50%}25%{transform:translate(18%,12%) rotate(40deg);border-radius:40% 60% 45% 55%/60% 40% 60% 40%}50%{transform:translate(34%,-4%) rotate(90deg);border-radius:55% 45% 60% 40%/45% 55% 45% 55%}75%{transform:translate(14%,-10%) rotate(140deg);border-radius:45% 55% 40% 60%/55% 45% 55% 45%}}
@keyframes hlf2{0%,100%{transform:translate(0,0) rotate(0);border-radius:50% 50% 40% 60%/60% 40% 60% 40%}25%{transform:translate(-18%,16%) rotate(-50deg);border-radius:60% 40% 55% 45%/45% 55% 45% 55%}50%{transform:translate(-38%,6%) rotate(-100deg);border-radius:40% 60% 50% 50%/55% 45% 55% 45%}75%{transform:translate(-20%,-8%) rotate(-150deg);border-radius:55% 45% 60% 40%/40% 60% 40% 60%}}
@keyframes hlf3{0%,100%{transform:translate(0,0) rotate(0);border-radius:45% 55% 60% 40%/55% 45% 55% 45%}33%{transform:translate(-32%,-18%) rotate(70deg);border-radius:60% 40% 45% 55%/40% 60% 40% 60%}66%{transform:translate(28%,-22%) rotate(140deg);border-radius:50% 50% 55% 45%/60% 40% 60% 40%}}
.hero>:not(.hl-flow){position:relative;z-index:1}
.hero h1,.hero h1 b{color:#111!important}
.hero p{color:#2b2f36!important;margin-left:auto;margin-right:auto}
.hero .safe{display:inline-flex;background:rgba(255,255,255,.7)!important;color:#1d3f7a!important;backdrop-filter:blur(4px)}
.hero .search{max-width:640px;margin-left:auto;margin-right:auto}
.hero .sres,.hero .note{text-align:left;max-width:640px;margin-left:auto;margin-right:auto}
@media (prefers-reduced-motion:reduce){.hl-flow i{animation:none!important}}
ul.hl-cards{display:flex;grid-template-columns:none;gap:12px;overflow-x:auto;scroll-snap-type:x proximity;padding:4px 2px 14px;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
ul.hl-cards>li{flex:0 0 176px;scroll-snap-align:start}
ul.hl-cards a{display:flex!important;flex-direction:column;padding:0!important;overflow:hidden;background:#fff!important;border:1px solid #e3e7ee!important;border-radius:14px!important;box-shadow:none!important;height:100%}
ul.hl-cards a:hover{border-color:#9ec0f5!important;transform:translateY(-2px)}
ul.hl-cards .th{display:flex;align-items:center;justify-content:center;height:112px;flex:0 0 auto}
ul.hl-cards .th img{width:56px;height:56px}
ul.hl-cards b{font-size:14.5px!important;line-height:1.4;margin:10px 12px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.hl-cards span{font-size:12.5px!important;margin:4px 12px 12px!important;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.hl-cw{position:relative}
.hl-cw .hl-ar{position:absolute;top:44px;width:38px;height:38px;border-radius:50%;border:1px solid #d9dee7;background:#fff;color:#111;font-size:20px;line-height:1;cursor:pointer;box-shadow:0 4px 12px rgba(10,30,60,.12);z-index:2;display:none}
.hl-cw .hl-l{left:-14px}.hl-cw .hl-r{right:-14px}
@media (hover:hover) and (min-width:700px){.hl-cw .hl-ar{display:block}}
</style>
<script>document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('ul.hl-cards').forEach(function(u){var w=document.createElement('div');w.className='hl-cw';u.parentNode.insertBefore(w,u);w.appendChild(u);[['hl-l','\u2039',-1],['hl-r','\u203A',1]].forEach(function(a){var b=document.createElement('button');b.type='button';b.className='hl-ar '+a[0];b.textContent=a[1];b.setAttribute('aria-label',a[2]<0?'이전 도구':'다음 도구');b.onclick=function(){u.scrollBy({left:a[2]*u.clientWidth*.8,behavior:'smooth'})};w.appendChild(b)})})});</script>'''
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = s.replace('<section class="hero" id="search">', '<section class="hero" id="search"><div class="hl-flow" aria-hidden="true"><i class="f1"></i><i class="f2"></i><i class="f3"></i></div>', 1)
    a = s.find('<h2 class="sec-h">많이 쓰는 도구'); b = s.find('<section class="card guide"', a)
    if a > 0 and b > a:
        def card(m):
            cat = m.group(2)
            t = TINT.get(cat, '#EEF2F8')
            img = f'<img src="/assets/art/cat2-{cat}.svg" alt="" width="56" height="56" loading="lazy">' if os.path.exists(os.path.join(root, 'assets/art', f'cat2-{cat}.svg')) else ''
            return f'{m.group(1)}<i class="th" style="background:{t}">{img}</i>'
        seg = s[a:b].replace('<ul class="tlist">', '<ul class="tlist hl-cards">')
        seg = re.sub(r'(<li><a href="/([a-z0-9-]+)/[^"]*"[^>]*>)', card, seg)
        s = s[:a] + seg + s[b:]
    open(p, 'w', encoding='utf-8').write(s); print('home: flow hero + tool cards')
