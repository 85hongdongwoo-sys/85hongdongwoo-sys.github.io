"""홍라이프 여행픽(/trip/)을 다른 분류 허브와 같은 틀(제목 영역·흰 카드·폰 그림 카드·다른 분류·공통 하단)로 다시 만든다.
패키지 데이터와 동작 스크립트는 trip_src.html 원본 그대로 쓴다."""
import os, re, sys, html, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
OUT = sys.argv[1]
E = lambda x: html.escape(str(x), quote=True)
HEAD = open(f'{D}/tpl_head.html').read(); MID = open(f'{D}/tpl_mid.html').read()
BRAND = open(f'{D}/tpl_brand.html').read(); TAIL = open(f'{D}/tpl_tail.html').read()
OTHER = open(f'{D}/tpl_other.html').read()
SITE = 'https://honglife.co.kr'
src = open(f'{D}/trip_src.html', encoding='utf-8').read()
script = re.findall(r'<script>(?:(?!</script>).)*?</script>', src[src.index('<body'):], re.S)
script = max(script, key=len)
import thumbs
TOOLS = [
 ('travel-budget', '여행경비 계산기', '항공·숙박·식비까지 1인 1일 경비를 한 번에 계산해요.', 'https://honglifecalc.com/ko/travel.html', '#1B64DA', '#E8F3FF',
  '<rect x="6" y="12" width="32" height="22" rx="4"/><path d="M6 19h32"/><circle cx="29" cy="27" r="2.4" fill="#fff"/>'),
 ('yen', '엔화 환율 계산기', '일본 여행 환전 금액을 바로 확인해요.', 'https://honglifecalc.com/ko/yen.html', '#2F9E44', '#EBFBEE',
  '<path d="M13 9l9 12 9-12"/><path d="M22 21v14"/><path d="M15 23h14M15 29h14"/>'),
 ('japan-tax-free', '일본 면세 계산기', '면세 기준 금액과 환급액을 확인해요.', 'https://honglifecalc.com/ko/japan-tax-free.html', '#E8590C', '#FFF4E6',
  '<path d="M8 22L22 8h12v12L20 34z"/><circle cx="28" cy="14" r="2.4" fill="#fff"/>'),
 ('visa-free', '무비자 국가 확인', '한국 여권으로 무비자 입국 가능한 나라를 찾아요.', 'https://honglifecalc.com/ko/visa-free.html', '#0C8599', '#E3FAFC',
  '<rect x="11" y="6" width="22" height="32" rx="3"/><circle cx="22" cy="19" r="5"/><path d="M16 31h12"/>'),
]
os.makedirs(OUT + '/assets/art/hl/t', exist_ok=True)
for slug, name, d, u, c, bg, ic in TOOLS:
    thumbs.ICON[slug] = ic; thumbs.COL[slug] = (c, bg); thumbs.GAME_SLUGS.add(slug)
    open(f'{OUT}/assets/art/hl/t/trip-{slug}.svg', 'w').write(thumbs.thumb(slug, name.replace(' 확인', '')))
lis = ''.join(f'<li><a href="{u}"><i class="th"><img src="/assets/art/hl/t/trip-{s}.svg" alt="" width="200" height="140" loading="lazy"></i><img class="pg" src="/assets/art/hl/pg-trip.svg" alt="" width="26" height="26" loading="lazy"><b>{E(n)}</b><span>{E(d)}</span></a></li>' for s, n, d, u, *_ in TOOLS)
CSS = '''<style id="hl-trip">
#tp{--label:#191F28;--label2:#6B7684;--sep:#E5E8EB;--blue:#1B64DA}
#tp .chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px}
#tp .chip{border:1px solid var(--sep);background:#fff;border-radius:999px;padding:8px 15px;font-size:14px;font-weight:700;cursor:pointer;color:var(--label2)}
#tp .chip.on{background:var(--label);border-color:var(--label);color:#fff}
#tp .pkgs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
#tp .pkg{position:relative;aspect-ratio:9/16;border-radius:20px;overflow:hidden;background:#000;box-shadow:0 8px 24px rgba(0,0,0,.14);transition:transform .25s}
#tp .pkg:hover{transform:translateY(-3px)}#tp .pkg.has-video{cursor:pointer}
#tp .pkg.sound-on{box-shadow:0 0 0 3px var(--blue),0 8px 24px rgba(0,0,0,.2)}
#tp .pkg video,#tp .pkg img{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;display:block}
#tp .pkg img{animation:tpkb 16s ease-in-out infinite alternate}@keyframes tpkb{from{transform:scale(1)}to{transform:scale(1.12)}}
#tp .pkg .dd{position:absolute;left:12px;top:12px;background:rgba(255,255,255,.92);color:var(--label);font-size:12px;font-weight:700;padding:4px 9px;border-radius:999px}
#tp .pkg .nt{position:absolute;right:12px;top:12px;background:rgba(0,0,0,.45);color:#fff;font-size:12px;font-weight:700;padding:5px 10px;border-radius:999px;backdrop-filter:blur(8px)}
#tp .pkg .rb{position:absolute;left:0;right:0;bottom:0;padding:70px 14px 14px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.78));color:#fff;display:flex;flex-direction:column;gap:5px}
#tp .pkg .rag{font-size:12px;font-weight:600;opacity:.85}
#tp .pkg .rt{font-weight:800;font-size:20px;line-height:1.25;letter-spacing:-.03em;word-break:keep-all}
#tp .pkg .rs{font-size:13px;opacity:.9;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
#tp .pkg .rp{display:flex;align-items:baseline;gap:6px;font-size:13px;margin-top:2px;flex-wrap:wrap}
#tp .pkg .rp del{opacity:.6}#tp .pkg .rp .off{color:#ffb84d;font-weight:800}#tp .pkg .rp b{font-size:19px}
#tp .pkg .rbtn{margin-top:8px;background:#fff;color:var(--label);border-radius:999px;padding:10px;text-align:center;font-weight:800;font-size:14px}
.tp-sub{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:14px}.tp-sub a{display:inline-block;padding:8px 14px;border-radius:999px;background:#fff;border:1px solid #E5E8EB;font-size:14px;font-weight:700;color:#333D4B;text-decoration:none}
.tp-note{margin:0 0 14px;color:#6B7684;font-size:14.5px;line-height:1.6}
@media(max-width:480px){#tp .pkgs{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}#tp .pkg .rt{font-size:16px}#tp .pkg .rs{display:none}#tp .pkg .rb{padding:50px 10px 10px}#tp .pkg .rp b{font-size:16px}#tp .pkg .rbtn{padding:8px;font-size:13px}}
</style>'''
title = '홍라이프 여행픽 | 출발확정 해외 패키지 특가·여행 쇼츠·여행경비 계산기'
desc = '대마도·후쿠오카·오사카·스페인 등 출발확정 해외여행 패키지를 쇼츠 영상으로 먼저 보고 바로 예약하세요. 여행경비 계산기, 엔화 환율, 일본 면세, 무비자 국가까지 한국인 여행 도구를 한곳에 모았어요.'
ld = {"@context": "https://schema.org", "@graph": [{"@type": "CollectionPage", "name": "홍라이프 여행픽", "url": SITE + "/trip/", "description": desc},
      {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "홈", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "여행", "item": SITE + "/trip/"}]}]}
h = HEAD + f'<title>{E(title)}</title>\n<meta name="description" content="{E(desc)}">\n<meta name="keywords" content="여행 패키지 특가, 출발확정 패키지, 대마도 여행, 후쿠오카 여행, 오사카 패키지, 스페인 포르투갈 패키지, 여행경비 계산기, 홍라이프 여행픽">\n<link rel="canonical" href="{SITE}/trip/">\n'
h += f'<meta property="og:type" content="website"><meta property="og:url" content="{SITE}/trip/"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="홍라이프 도구">\n<meta property="og:title" content="홍라이프 여행픽 | 출발확정 해외 패키지 특가"><meta property="og:description" content="쇼츠로 먼저 보고, 마음에 들면 바로 예약. 출발확정 해외 패키지와 여행 도구 모음."><meta property="og:image" content="{SITE}/assets/og/site.png">\n'
h += MID + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '\n</head>\n<body>\n\n' + BRAND
h += ('<main class="wrap wide"><header class="top hub"><p class="crumb"><a href="/">홈</a> › 여행</p><h1>홍라이프 여행픽</h1>'
      '<p class="lead">출발확정 여행만 골라요. 쇼츠로 먼저 보고 마음에 들면 바로 예약해요. 한국인 기준으로 고른 해외 패키지와 여행 준비 도구를 모았어요.</p>'
      '<div class="safe"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>출발확정 상품만 담고, 가격은 예약 페이지와 같아요</div>'
      '<div class="tp-sub"><a href="#pkgs">출발확정 패키지</a><a href="#tools">여행 준비 도구</a><a href="https://www.youtube.com/channel/UCD5LjkSsI4yMD0PlSfLyBTA/shorts" target="_blank" rel="noopener">유튜브 쇼츠</a></div></header>'
      '<section class="card" id="pkgs"><h2>출발확정 특가 패키지</h2><p class="tp-note">네이버 여행 패키지 중 골라 담았어요. 영상 카드에 마우스를 올리면 재생되고, 누르면 소리가 나와요. 가격은 표시된 출발일 기준이에요.</p>'
      '<div id="tp"><div class="chips" id="pchips"><button class="chip on" data-g="all">전체</button><button class="chip" data-g="일본">일본</button><button class="chip" data-g="중국·대만">중국·대만</button><button class="chip" data-g="유럽">유럽</button></div><div class="pkgs" id="pkglist"></div></div></section>'
      f'<section class="card" id="tools"><h2>여행 준비 도구 {len(TOOLS)}가지</h2><ul class="tlist hl-grid">{lis}</ul></section>'
      + OTHER +
      '<p class="upd">이 페이지의 예약 링크는 제휴 링크로, 이를 통해 예약하시면 운영자가 수수료를 받을 수 있어요. 이용자가 내는 가격은 같아요. 영상은 여행사 제공 사진을 바탕으로 AI로 만든 장면이 포함되어 있어요. 가격과 일정은 예약 페이지에서 꼭 다시 확인하세요.</p>'
      '</main>' + script + TAIL)
os.makedirs(OUT + '/trip', exist_ok=True)
open(OUT + '/trip/index.html', 'w', encoding='utf-8').write(h)
print('ok /trip/', len(h))
