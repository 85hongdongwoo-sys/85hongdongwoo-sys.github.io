"""삼성 드라이버 페이지 보강 — driver_samsung.py가 만든 overlay/driver/samsung.html에 모델명 찾기·갤럭시 북 시리즈표·Windows 업데이트 전용 모델·프린터(HP)·SSD·FAQ를 더해요.
driver_samsung.py 실행 끝에 자동으로 불려요(따로 돌려도 한 번만 적용).
2026-11-23 확인 출처: 삼성전자서비스 시리즈별 SSD·메모리 업그레이드 안내(solution/4229308, 4227987, 4238119, 4227415, 4238104, 4227359, 4238096, 4229421, 4238077, 4229770, 4237970, 4604026, 4604029)의 모델명,
solution/441879 Windows 업데이트 전용 모델, 삼성 멤버스 PC_SW담당 답변(이온·플렉스는 윈도우 11 23H2부터 Windows 업데이트), 삼성 반도체 NVMe 드라이버 3.3 지원 모델(970/960/950만),
samsung.com '삼성 프린터 지원은 HP', HP 커뮤니티(SL-M2020 AirPrint 미지원), HP c05818421(Universal Print Driver 3·Printer Software Installer).
"""
import re,json,os,sys
OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'overlay','driver','samsung.html')
s=open(OUT,encoding='utf-8').read()
if 'id="find"' in s:
    print('already enhanced');sys.exit(0)
D='2026년 11월 23일'
T='삼성 드라이버 다운로드 (2026) — 갤럭시 북 모델명별 설치·프린터·모니터·SSD·USB'
DESC='삼성 드라이버를 모델명으로 찾아요. 갤럭시 북6·5·4·3·2·프로·플렉스·이온(NT940XHA, NT960XGK, NT750XFG 등)은 디바이스 케어·Samsung Update·Windows 업데이트 중 맞는 방법을, 삼성 프린터(SL-M2020 등)는 HP, SSD는 Magician, 갤럭시 USB 드라이버까지 공식 링크로 정리.'
s=re.sub(r'<title>.*?</title>',f'<title>{T} | 홍라이프 도구</title>',s,count=1)
s=re.sub(r'(<meta name="description" content=")[^"]*',lambda m:m.group(1)+DESC,s,count=1)
s=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m.group(1)+T+' | 홍라이프 도구',s)
s=re.sub(r'(<meta property="og:description" content=")[^"]*',lambda m:m.group(1)+DESC,s)

# ---- data ----
BOOK=[ # series, year, prefixes, wu-only prefixes
 ('갤럭시 북6 Ultra',2026,['NT960UJH','NT960UJG']),
 ('갤럭시 북6 Pro',2026,['NT960XJG','NT961XJG','NT940XJG','NT941XJG']),
 ('갤럭시 북6',2026,['NT760VJG','NT760VJT','NT740VJG']),
 ('갤럭시 북5 Pro',2025,['NT940XHA','NT941XHA','NT940XHZ','NT960XHA','NT961XHA','NT960XHZ','NT965XHW']),
 ('갤럭시 북5 Pro 360',2025,['NT960QHA','NT961QHA']),
 ('갤럭시 북5',2025,['NT750XHD','NT751XHD','NT750XHW','NT751XHW']),
 ('갤럭시 북4 Ultra',2024,['NT960XGL','NT961XGL']),
 ('갤럭시 북4 Pro 360',2024,['NT960QGK']),
 ('갤럭시 북4 Pro',2024,['NT960XGQ','NT960XGK','NT961XGK','NT940XGQ','NT940XGK','NT941XGK']),
 ('갤럭시 북4',2024,['NT750XGJ','NT751XGJ','NT750XGK','NT751XGK','NT750XGL','NT751XGL','NT750XGP','NT750XGQ','NT750XGR']),
 ('갤럭시 북3 Ultra',2023,['NT960XFH','NT961XFH']),
 ('갤럭시 북3 Pro 360',2023,['NT960QFG','NT961QFG']),
 ('갤럭시 북3 Pro',2023,['NT960XFG','NT961XFG','NT960XFT','NT940XFG','NT941XFG','NT940XFT']),
 ('갤럭시 북3 360',2023,['NT750QFG','NT751QFG','NT750QFT','NT730QFG','NT730QFT']),
 ('갤럭시 북3 Go 5G',2023,['NT345XPA']),
 ('갤럭시 북3',2023,['NT750XFG','NT751XFG','NT750XFH','NT751XFH','NT750XFS','NT750XFT']),
 ('갤럭시 북2 Pro',2022,['NT930XED','NT950XED','NT950XEE','NT950XGK','NT951XGK']),
 ('갤럭시 북2 Pro 360',2022,['NT930QED','NT950QED']),
 ('갤럭시 북2 Pro 5G',2022,['NT955XED']),
 ('갤럭시 북2',2022,['NT550XED','NT551XED','NT550XEZ','NT750XED','NT750XEW','NT750XEE','NT751XEE','NT750XEV']),
 ('갤럭시 북 Pro',2021,['NT930XDB','NT931XDB','NT930XDY','NT935XDB','NT950XDB','NT951XDB','NT950XDY','NT950XDC','NT950XDX']),
 ('갤럭시 북 Pro 360',2021,['NT930QDB','NT931QDB','NT930QDY','NT935QDB','NT950QDB','NT951QDB','NT950QDY']),
 ('갤럭시 북',2021,['NT750XDA','NT751XDA','NT750XDZ','NT755XDA','NT760XDA','NT761XDA']),
 ('갤럭시 북 이온2',2021,['NT950XDA','NT950XDZ','NT930XDA','NT930XDZ']),
 ('갤럭시 북 이온',2020,['NT950XCJ','NT951XCJ','NT950XCR','NT930XCJ','NT931XCJ','NT930XCR']),
 ('갤럭시 북 플렉스',2020,['NT950QCG','NT951QCG','NT950QCT','NT930QCG','NT931QCG','NT930QCT']),
]
WU=['NT550XDA','NT750XDA','NT755XDA','NT750XED','NT750XEE','NT750XFG','NT750XFH','DM530AFA','DB531AFA']
def method(series,year,pre):
  if any(p.startswith(w) or w.startswith(p) for w in WU for p in pre[:1]): pass
  if year>=2023: return '디바이스 케어 (윈도우 11)'
  if year==2022: return '디바이스 케어 또는 Samsung Update'
  if year==2021: return 'Samsung Update (윈도우 11은 디바이스 케어)'
  return 'Windows 업데이트 + Samsung Update 수동 다운로드'
rows=[]
for se,y,pre in BOOK:
  wu=[p for p in pre if p in WU]
  m=method(se,y,pre)
  if wu: m+=f' · <b>{", ".join(wu)}</b>은 Windows 업데이트만'
  dc='○' if y>=2022 else '—'
  rows.append(f'<tr><td data-l="시리즈"><b>{se}</b> <span class="yr">{y}</span></td><td class="yrc" data-l="출시">{y}</td><td class="mn" data-l="모델명">{" · ".join('<span class="nw">'+p+'</span>' for p in pre)}</td><td data-l="받는 곳">{m}</td><td data-l="다운로드 센터">{dc}</td></tr>')
TBL='<div class="sx"><table class="dr-m sg"><thead><tr><th>시리즈</th><th>출시</th><th>모델명이 이렇게 시작해요</th><th>드라이버 받는 곳</th><th>다운로드 센터</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
PRN=[('SL-M2020 · SL-M2020W · SL-M2022 · SL-M2026','Xpress 흑백 레이저','Samsung Xpress SL-M2020'),
 ('SL-M2070 · SL-M2070F · SL-M2070FW','Xpress 흑백 복합기','Samsung Xpress SL-M2070'),
 ('SL-C480 · SL-C480W · SL-C480FW','Xpress 컬러 복합기','Samsung Xpress SL-C480'),
 ('SL-M2620 · SL-M2820 · SL-M2830','흑백 레이저','Samsung Xpress SL-M2830'),
 ('SL-M2670 · SL-M2870 · SL-M2885','흑백 복합기','Samsung Xpress SL-M2870'),
 ('SL-J1660','잉크젯','Samsung SL-J1660'),
 ('ML-2160 · ML-2165 · ML-1660 · ML-1865','흑백 레이저(구형)','Samsung ML-2165'),
 ('SCX-3400 · SCX-3405 · SCX-3405F · SCX-3405FW','흑백 복합기(구형)','Samsung SCX-3405'),
 ('CLP-365 · CLX-3305','컬러 레이저·복합기(구형)','Samsung CLX-3305')]
PT='<div class="sx"><table class="dr-m"><thead><tr><th>모델</th><th>종류</th><th>HP 지원에서 이렇게 검색</th></tr></thead><tbody>'+''.join(f'<tr><td class="mn"><b>{a}</b></td><td>{b}</td><td class="mn">{c}</td></tr>' for a,b,c in PRN)+'</tbody></table></div>'
SSD=[('970 PRO · 970 EVO · 970 EVO Plus · 960 PRO · 960 EVO · 950 PRO','MZ-V7… · MZ-V6… · MZ-V5…','Magician + <b>삼성 NVMe 드라이버 3.3</b> (윈도우 7·8.1·10)'),
 ('980 · 980 PRO · 990 PRO · 990 EVO · 990 EVO Plus · 9100 PRO','MZ-V8… · MZ-V9… · MZ-VAP…','Magician만 · 드라이버는 <b>윈도우 기본 NVMe 드라이버</b>'),
 ('870 EVO · 870 QVO · 860 EVO · 860 PRO · 850 PRO (SATA)','MZ-77… · MZ-76… 등','Magician만 · 별도 드라이버 없음')]
ST='<div class="sx"><table class="dr-m"><thead><tr><th>SSD</th><th>모델명 예</th><th>필요한 것</th></tr></thead><tbody>'+''.join(f'<tr><td><b>{a}</b></td><td class="mn">{b}</td><td>{c}</td></tr>' for a,b,c in SSD)+'</tbody></table></div>'

js_book=json.dumps([[se,y,pre] for se,y,pre in BOOK],ensure_ascii=False)
FINDER=f'''<section class="card dr-sec" id="find"><h2>모델명으로 삼성 드라이버 찾기</h2><p>노트북 바닥면이나 모니터 뒷면의 모델명을 넣으면 맞는 방법을 알려 줘요. 앞 8자리만 넣어도 돼요. 예: <b class="nw">NT940XHA</b>, <b class="nw">NT750XFG</b>, <b class="nw">SL-M2020W</b>, <b class="nw">MZ-V9P1T0</b>, <b class="nw">SM-S928</b></p>
<div class="sf"><input id="sgq" type="text" inputmode="text" autocomplete="off" spellcheck="false" placeholder="모델명 입력 (예: NT940XHA-KC71G)" aria-label="삼성 모델명"><button id="sgb" type="button">찾기</button></div>
<div id="sgr" class="sgr" aria-live="polite"><p class="mut">모델명을 넣으면 여기에 결과가 나와요.</p></div></section>'''
SER=f'''<section class="card dr-sec" id="series"><h2>갤럭시 북 시리즈별 모델명과 드라이버 받는 곳</h2><p>삼성 노트북은 모델명 앞부분(예: <b>NT940XHA</b>)으로 시리즈를 알 수 있어요. 아래 표는 삼성전자서비스가 시리즈별로 안내하는 모델명을 모은 거예요. 모델명 뒤의 <b>-KC71G</b> 같은 글자는 색상·CPU·저장 용량 차이라서 드라이버는 앞부분이 같으면 같아요.</p>{TBL}
<p class="cu-src">다운로드 센터 ○: 갤럭시 북2 시리즈부터 <a href="https://www.samsung.com/global/galaxybooks-downloadcenter/?siteCode=sec" target="_blank" rel="noopener nofollow">갤럭시 북 다운로드 센터</a>에서 윈도우 11 드라이버를 파일로 받을 수 있어요. 갤럭시 북 이온·플렉스(2020년)는 윈도우 11 23H2부터 필수 드라이버를 Windows 업데이트로 받고, 더 필요한 파일은 Samsung Update의 [설정 → 다운로드 → 모델 선택 → OS 선택]으로 받아요.</p></section>
<section class="card dr-sec" id="wu"><h2>Samsung Update를 지원하지 않는 모델 (Windows 업데이트로 설치)</h2><p>아래 모델은 Samsung Update로 드라이버를 받을 수 없어요. <b>설정 → Windows 업데이트 → [업데이트 확인]</b>, 그리고 <b>고급 옵션 → 선택적 업데이트</b>에서 드라이버를 받아요.</p><ul class="cu-chk"><li class="mn"><b>{" · ".join(WU)}</b> 로 시작하는 모델 (갤럭시 북·북2·북3 일반 모델, 데스크톱 일부)</li><li class="mn"><b>SM-W737 · SM-W767 · DM530ABE</b> 등</li></ul><p class="cu-src">삼성전자서비스 ‘노트북 장치 드라이버 설치 및 업데이트 방법’의 Windows 업데이트 전용 모델 안내 기준이에요. 목록은 바뀔 수 있으니 모델이 안 보이면 디바이스 케어부터 열어 보세요.</p></section>'''
PRINTER=f'''<section class="card dr-sec" id="printer"><h2>삼성 프린터 드라이버 (SL-M2020·M2070·C480 등) — HP에서 받아요</h2><p>삼성 프린터 사업은 <b>HP가 인수</b>해서, 지금은 삼성 프린터의 드라이버·지원·보증을 <b>HP</b>가 맡고 있어요. 삼성전자 고객지원도 M2070 같은 삼성 프린터는 HP 사이트에서 지원받으라고 안내해요.</p>
<ol class="big-n"><li><a href="https://support.hp.com/kr-ko/drivers" target="_blank" rel="noopener nofollow"><b>HP 고객지원 드라이버 페이지</b></a>를 열어요.</li><li>[프린터]를 고르고, 프린터 앞면 라벨의 모델명을 <b>Samsung Xpress SL-M2020</b>처럼 넣어요.</li><li>내 운영체제(윈도우 11 등)를 확인하고 <b>전체 소프트웨어(설치 프로그램)</b> 또는 <b>프린트 드라이버</b>를 받아요.</li><li>설치 프로그램을 실행해 USB나 Wi-Fi로 연결해요.</li></ol>
{PT}
<ul class="cu-chk"><li>모델 페이지에 드라이버가 안 보이면 HP가 배포하는 <b>Samsung Universal Print Driver 3</b>(여러 삼성 레이저 모델 공용)이나 <b>Samsung Printer Software Installer</b>(웹 설치 프로그램)를 써요.</li><li><b>맥(macOS)</b>: SL-M2020·M2020W는 AirPrint를 지원하지 않아서, 최신 macOS에서는 드라이버 지원이 제한될 수 있어요. HP 모델 페이지에서 macOS용 파일이 있는지 먼저 확인하세요.</li><li>삼성전자서비스 다운로드 자료실의 [PC/프린터 → 프린터 S/W 설치 프로그램]도 여전히 쓸 수 있어요.</li></ul>
<div class="bt"><a class="dl3d" href="https://support.hp.com/kr-ko/drivers" target="_blank" rel="noopener nofollow"><span class="ic">↓</span><span class="tx"><b>HP에서 삼성 프린터 드라이버 찾기</b><small>support.hp.com · 공식</small></span></a><a class="dl3d s" href="/driver/hp.html"><span class="ic">›</span><span class="tx"><b>홍라이프 HP 드라이버 안내</b><small>설치 순서 자세히</small></span></a></div></section>'''
SSDSEC=f'''<section class="card dr-sec" id="ssd"><h2>삼성 SSD 드라이버 — Magician과 NVMe 드라이버 3.3</h2><p>삼성 SSD는 대부분 <b>따로 드라이버를 깔 필요가 없어요</b>. 펌웨어 업데이트와 상태 확인은 <b>Samsung Magician</b>으로 해요. 삼성 NVMe 드라이버 3.3은 <b>970 PRO·970 EVO·970 EVO Plus·960 PRO·960 EVO·950 PRO</b>만 지원하고, 윈도우 7·8.1·10용이에요. 980·990 시리즈는 윈도우 기본 NVMe 드라이버를 쓰면 돼요.</p>{ST}</section>'''
FAQ=[('삼성 노트북 드라이버는 어디서 받아요?','윈도우 11 갤럭시 북은 디바이스 케어 앱의 [업데이트] → [업데이트 확인] → [모두 업데이트]로 받아요. 2017년 8월 이후 윈도우 10 노트북은 Microsoft Store의 Samsung Update 앱, 그 이전 윈도우 7·8 노트북은 삼성전자서비스 다운로드 자료실의 Samsung Update 프로그램을 써요.'),
('내 노트북이 갤럭시 북 몇인지 모르겠어요.','노트북 바닥의 모델명 앞 8자리를 이 페이지의 ‘모델명으로 찾기’에 넣으세요. 예를 들어 NT940XHA는 갤럭시 북5 Pro, NT960XGK는 갤럭시 북4 Pro, NT750XFG는 갤럭시 북3예요.'),
('Samsung Update에 드라이버가 안 나와요.','NT750XDA, NT750XED, NT750XEE, NT750XFG, NT750XFH처럼 Samsung Update를 지원하지 않는 모델은 Windows 업데이트(선택적 업데이트 포함)로 드라이버를 받아요. 윈도우 11 25H2 이상에서는 디바이스 케어를 쓰세요.'),
('윈도우를 새로 깔았는데 와이파이가 안 돼요.','인터넷이 되는 다른 PC에서 갤럭시 북 다운로드 센터(북2 이후)나 Samsung Update의 [다운로드] 메뉴로 무선랜 드라이버를 받아 USB에 옮겨 설치해요.'),
('갤럭시 북 다운로드 센터는 어떤 모델이 되나요?','갤럭시 북2 시리즈 이후 모델의 윈도우 11 드라이버를 제공해요. 그 이전 모델은 Samsung Update나 다운로드 자료실을 쓰세요.'),
('삼성 프린터 SL-M2020 드라이버는 어디 있어요?','삼성 프린터 지원은 HP가 맡고 있어요. HP 고객지원(support.hp.com)에서 ‘Samsung Xpress SL-M2020’을 검색해 받으세요. 모델 페이지에 없으면 Samsung Universal Print Driver 3를 써요.'),
('삼성 SSD 드라이버를 꼭 깔아야 하나요?','아니요. 970 EVO Plus 이하 일부 모델만 삼성 NVMe 드라이버 3.3을 쓸 수 있고, 980·990 시리즈는 윈도우 기본 드라이버로 충분해요. 펌웨어 업데이트는 Samsung Magician으로 해요.'),
('삼성 모니터 드라이버와 Easy Setting Box는요?','모니터는 연결하면 대부분 윈도우가 자동으로 인식해요. 화면 분할 프로그램 Easy Setting Box는 삼성전자서비스 다운로드 자료실에서 모델명을 검색해 [응용프로그램]에서 받아요(윈도우 7~11, macOS 12 이상).'),
('갤럭시 휴대폰을 PC에 연결하려면 드라이버가 필요해요?','사진·파일 옮기기는 보통 필요 없어요. 안드로이드 개발(ADB)을 할 때만 삼성 Android USB 드라이버를 깔아요.'),
('업데이트가 진행되지 않아요.','충전기를 꽂았는지, 배터리가 30%보다 많은지 확인하세요. BIOS 업데이트 중에는 전원을 끄거나 덮개를 닫지 마세요.')]
FAQH='<section class="card" id="faq"><h2>자주 묻는 질문</h2><dl class="pe-faq">'+''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q,a in FAQ)+'</dl></section>'
SRC=f'''<section class="card"><h2>출처와 안내</h2><p class="cu-src">작성: 홍라이프 도구 편집팀 · 마지막 확인: {D}<br>출처: 삼성전자서비스 ‘디바이스 케어에서 장치 드라이버 업데이트하기’, ‘윈도우 버전별 Samsung Update 설치 방법’, ‘Samsung Update로 드라이버, 소프트웨어 설치방법(Win10, 11)’, ‘노트북 장치 드라이버 설치 및 업데이트 방법’, 갤럭시 북·북2·북3·북4·북5·북6 ‘SSD·메모리 업그레이드 문의’(시리즈별 모델명), ‘Easy Setting Box가 뭔가요’, 삼성 멤버스 PC_SW담당 답변(이온·플렉스 윈도우 11 23H2), 삼성 반도체 ‘Tools & Software’·‘NVMe Driver 설치 가이드’, Samsung Magician 지원 모델, 삼성전자 ‘삼성 프린터 지원은 HP’, HP 고객지원 ‘Samsung 프린터 드라이버’ 안내, 삼성 개발자 ‘Android USB Driver’.<br>홍라이프 도구는 드라이버 파일을 직접 올리지 않아요. 모든 다운로드는 제조사 공식 사이트에서 이루어져요. 모델 목록은 삼성 안내를 옮긴 것으로, 새 모델은 빠져 있을 수 있어요.</p></section>'''

# header
a=s.index('<header class="top hub">');b=s.index('</header>',a)+9
head=f'''<header class="top hub"><p class="crumb"><a href="/">홈</a> › <a href="/driver/">드라이버</a> › 삼성 드라이버</p><h1>삼성 드라이버 다운로드 — 갤럭시 북 모델명별 설치, 프린터·모니터·SSD·USB</h1><p class="byl">홍라이프 도구 편집팀 · 마지막 확인 {D} · 삼성전자서비스·HP·삼성 반도체 공식 안내 기준</p><p class="lead">삼성 노트북(갤럭시 북6·5·4·3·2·프로·플렉스·이온), 삼성 프린터, 모니터, SSD, 갤럭시 휴대폰 USB 드라이버를 <b>모델명으로 찾아서</b> 공식 앱과 공식 사이트에서 받는 방법을 정리했어요.</p><p class="cu-ans"><b>한 줄 답:</b> 갤럭시 북은 윈도우 11이면 <b>디바이스 케어 → [업데이트] → [업데이트 확인] → [모두 업데이트]</b>, 예전 윈도우 10이면 <b>Samsung Update</b>, NT750XFG 같은 일부 모델은 <b>Windows 업데이트</b>로 받아요. 삼성 프린터는 <b>HP 고객지원</b>, SSD는 <b>Samsung Magician</b>이에요.</p>'''+s[s.index('<a class="dl3d"',a):s.index('<ul class="dr-toc">',a)]+'<ul class="dr-toc"><li><a href="#find">모델명으로 찾기</a></li><li><a href="#series">갤럭시 북 시리즈표</a></li><li><a href="#pc">설치 방법</a></li><li><a href="#steps">업데이트 순서</a></li><li><a href="#wu">Windows 업데이트 모델</a></li><li><a href="#printer">프린터</a></li><li><a href="#ssd">SSD</a></li><li><a href="#other">모니터·USB</a></li><li><a href="#faq">자주 묻는 질문</a></li></ul></header>'
s=s[:a]+head+FINDER+SER+s[b:]
# printer/ssd: remove old printer & SSD li from #other, insert new sections after #other
o=s.index('<section class="card dr-sec" id="other">');oe=s.index('</section>',o)+10
other=s[o:oe]
other=re.sub(r'<li class="hpm"><h3>삼성 SSD → Samsung Magician</h3>.*?</li>(?=<li class="hpm"><h3>삼성 프린터)','',other,flags=re.S)
other=re.sub(r'<li class="hpm"><h3>삼성 프린터·복합기</h3>.*?</li></ul>','</ul>',other,flags=re.S)
other=other.replace('<h2>모니터·갤럭시 USB·SSD·프린터</h2>','<h2>삼성 모니터·갤럭시 USB 드라이버</h2>')
other=other.replace('(윈도우 7~11, macOS 12 이상). 지원하지 않는 모델은 목록에 안 나와요.','(윈도우 7~11, macOS 12 이상). 지원하지 않는 모델은 목록에 안 나와요. 오디세이·스마트 모니터처럼 모델명이 <b>LS27</b>, <b>LS32</b>, <b>LC27</b> 등으로 시작하는 제품도 같은 방법이에요.')
s=s[:o]+PRINTER+SSDSEC+other+s[oe:]
# FAQ + sources replace
f0=s.index('<section class="card"><h2>자주 묻는 질문</h2>');f1=s.index('</section>',f0)+10
s=s[:f0]+FAQH+s[f1:]
c0=s.index('<section class="card"><h2>출처와 안내</h2>');c1=s.index('</section>',c0)+10
s=s[:c0]+SRC+s[c1:]
# ld+json
lds=re.findall(r'<script type="application/ld\+json">.*?</script>',s,flags=re.S)
bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"홈","item":"https://honglife.co.kr/"},{"@type":"ListItem","position":2,"name":"드라이버","item":"https://honglife.co.kr/driver/"},{"@type":"ListItem","position":3,"name":"삼성 드라이버","item":"https://honglife.co.kr/driver/samsung.html"}]}
fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a_}} for q,a_ in FAQ]}
art={"@context":"https://schema.org","@type":"TechArticle","headline":T,"description":DESC,"inLanguage":"ko","dateModified":"2026-11-23","author":{"@type":"Organization","name":"홍라이프 도구"},"publisher":{"@type":"Organization","name":"홍라이프 도구","url":"https://honglife.co.kr/"},"mainEntityOfPage":"https://honglife.co.kr/driver/samsung.html","about":[{"@type":"Brand","name":"Samsung"}]}
s=s.replace(lds[0],'<script type="application/ld+json">'+json.dumps(bc,ensure_ascii=False)+'</script>',1)
s=s.replace(lds[1],'<script type="application/ld+json">'+json.dumps(fq,ensure_ascii=False)+'</script><script type="application/ld+json">'+json.dumps(art,ensure_ascii=False)+'</script>',1)
# CSS + JS
CSS='<style id="sg-css">.byl{font-size:13px;color:var(--muted,#5B6B82);margin:2px 0 8px}.sx{overflow-x:auto;margin:10px 0;-webkit-overflow-scrolling:touch}.dr-m.sg{min-width:640px}.dr-m .mn{font-variant-numeric:tabular-nums;font-size:13.5px}.sf{display:flex;gap:8px;margin:12px 0}.sf input{flex:1;min-width:0;height:48px;border:1.5px solid var(--line-s,#E3E7EE);border-radius:12px;padding:0 14px;font:inherit;font-size:17px;text-transform:uppercase}.sf input:focus{outline:none;border-color:#1D4ED8;box-shadow:0 0 0 3px #DCE8FF}.sf button{height:48px;padding:0 20px;border:0;border-radius:12px;background:#1B64DA;color:#fff;font:inherit;font-weight:700;font-size:16px;cursor:pointer;flex:none}.sgr{border:1px dashed var(--line-s,#E3E7EE);border-radius:14px;padding:14px;background:#FAFBFD}.sgr .mut{margin:0;color:var(--muted,#5B6B82);font-size:14px}.sgr h3{margin:0 0 6px;font-size:18px}.sgr .tg{display:inline-block;font-size:12.5px;font-weight:700;background:#E8F0FE;color:#1D4ED8;border-radius:8px;padding:2px 8px;margin-left:6px;vertical-align:2px}.sgr ol{margin:8px 0 0;padding-left:20px;line-height:1.75}.sgr .bt{display:flex;flex-wrap:wrap;gap:0 8px;margin-top:6px}.nw{white-space:nowrap}.dr-m .yr{display:none}.dr-m .yrc{white-space:nowrap}@media(max-width:640px){.dr-m.sg{min-width:0}.dr-m.sg thead{display:none}.dr-m.sg tr{display:block;padding:10px 0;border-bottom:1px solid var(--line-s,#E3E7EE)}.dr-m.sg td{display:block;border:0;padding:3px 0}.dr-m.sg .yrc{display:none}.dr-m.sg .yr{display:inline-block;font-size:12px;font-weight:700;color:#1D4ED8;background:#E8F0FE;border-radius:6px;padding:0 6px;margin-left:4px}.dr-m.sg td[data-l]:not(:first-child)::before{content:attr(data-l)" · ";color:var(--muted,#5B6B82);font-size:12.5px;font-weight:600}}</style>'
s=s.replace('</head>',CSS+'</head>',1)
JS='''<script>(function(){var B=__BOOK__,WU=__WU__,$=function(i){return document.getElementById(i)};
var DC='https://apps.microsoft.com/search?query=Samsung%20Device%20Care&hl=ko-kr&gl=KR',SU='https://apps.microsoft.com/detail/9nq3hdb99vbf?hl=ko-kr&gl=KR',DL='https://www.samsung.com/global/galaxybooks-downloadcenter/?siteCode=sec',SV='https://www.samsungsvc.co.kr/download';
function bt(h,t,s,p){return '<a class="dl3d'+(p?'':' s')+'" href="'+h+'" target="_blank" rel="noopener nofollow"><span class="ic">↓</span><span class="tx"><b>'+t+'</b><small>'+s+'</small></span></a>'}
function esc(x){return x.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function run(){var raw=$('sgq').value.trim().toUpperCase(),q=raw.replace(/[\\s]/g,''),r=$('sgr');if(!q){r.innerHTML='<p class="mut">모델명을 넣으면 여기에 결과가 나와요.</p>';return}
 var n=q.replace(/^NP/,'NT').replace(/-/g,'');var h='';
 if(/^NT|^DM|^DB/.test(n)){var hit=null;B.forEach(function(b){b[2].forEach(function(p){if(n.indexOf(p)===0||(n.length>=6&&p.indexOf(n)===0&&!hit))hit=[b,p]})});
  var wu=WU.some(function(w){return n.indexOf(w)===0});
  if(hit){var b=hit[0],y=b[1];h='<h3>'+b[0]+'<span class="tg">'+y+'년 출시</span></h3><p>모델명 <b>'+esc(raw)+'</b>은 <b>'+b[0]+'</b> 계열('+hit[1]+'…)이에요.</p>';
   if(wu)h+='<ol><li>이 모델은 <b>Samsung Update를 지원하지 않아요</b>.</li><li><b>설정 → Windows 업데이트 → [업데이트 확인]</b>을 눌러요.</li><li><b>고급 옵션 → 선택적 업데이트</b>의 드라이버도 설치해요.</li></ol><div class="bt">'+(y>=2022?bt(DL,'갤럭시 북 다운로드 센터','윈도우 11 드라이버 파일',1):'')+bt(DC,'디바이스 케어 (윈도우 11)','Microsoft Store')+'</div>';
   else if(y>=2023)h+='<ol><li>충전기를 꽂고 <b>디바이스 케어</b>를 열어요.</li><li><b>[업데이트] → [업데이트 확인] → [모두 업데이트]</b>를 눌러요.</li><li>앱 없이 파일로 받으려면 다운로드 센터에서 모델 번호를 검색해요.</li></ol><div class="bt">'+bt(DC,'디바이스 케어 열기','Microsoft Store · 삼성 공식',1)+bt(DL,'갤럭시 북 다운로드 센터','모델 번호로 파일 받기')+'</div>';
   else if(y>=2021)h+='<ol><li>윈도우 11이면 <b>디바이스 케어</b>, 윈도우 10이면 <b>Samsung Update</b>를 열어요.</li><li><b>[드라이버] → [모두 업데이트]</b>를 눌러요.</li>'+(y>=2022?'<li>파일로 받으려면 다운로드 센터를 써요.</li>':'')+'</ol><div class="bt">'+bt(DC,'디바이스 케어','윈도우 11',1)+bt(SU,'Samsung Update','윈도우 10·11')+(y>=2022?bt(DL,'갤럭시 북 다운로드 센터','윈도우 11 파일'):'')+'</div>';
   else h+='<ol><li>윈도우 11 23H2부터는 필수 드라이버를 <b>Windows 업데이트</b>로 받아요.</li><li>더 필요한 드라이버는 <b>Samsung Update → 설정 → 다운로드 → 모델 선택 → OS 선택</b>으로 받아요.</li></ol><div class="bt">'+bt(SU,'Samsung Update','Microsoft Store',1)+bt(SV,'다운로드 자료실','삼성전자서비스')+'</div>';}
  else h='<h3>삼성 PC 모델 <span class="tg">목록 밖 모델</span></h3><p><b>'+esc(raw)+'</b>은 이 페이지 표에 없는 모델이에요(2020년 이전 노트북이거나 새 모델일 수 있어요).</p><ol><li>윈도우 11이면 먼저 <b>디바이스 케어</b>를 열어 보세요.</li><li>안 되면 <b>Samsung Update</b>, 윈도우 7·8 제품은 <b>다운로드 자료실</b>에서 모델명을 검색해요.</li></ol><div class="bt">'+bt(DC,'디바이스 케어','Microsoft Store',1)+bt(SU,'Samsung Update','Microsoft Store')+bt(SV,'다운로드 자료실','모델명 검색')+'</div>';}
 else if(/^(SL|ML|SCX|CLP|CLX|SF)/.test(n)){h='<h3>삼성 프린터·복합기 <span class="tg">HP 지원</span></h3><p><b>'+esc(raw)+'</b>은 삼성 프린터 모델이에요. 지금은 <b>HP</b>가 드라이버를 제공해요.</p><ol><li>HP 고객지원 드라이버 페이지를 열어요.</li><li>[프린터]에서 <b>Samsung '+esc(raw)+'</b>을 검색해요.</li><li>내 윈도우에 맞는 설치 프로그램을 받아요. 없으면 Samsung Universal Print Driver 3를 써요.</li></ol><div class="bt">'+bt('https://support.hp.com/kr-ko/drivers','HP에서 드라이버 찾기','support.hp.com',1)+bt(SV,'삼성 다운로드 자료실','프린터 S/W 설치 프로그램')+'</div>';}
 else if(/^MZ/.test(n)){var old=/^MZV[567]/.test(n);h='<h3>삼성 SSD <span class="tg">Magician</span></h3><p><b>'+esc(raw)+'</b>은 삼성 SSD예요. 펌웨어 업데이트·상태 확인은 <b>Samsung Magician</b>으로 해요.</p><p>'+(old?'이 모델(950·960·970 계열)은 <b>삼성 NVMe 드라이버 3.3</b>을 쓸 수 있어요(윈도우 7·8.1·10).':'따로 드라이버를 깔 필요 없이 <b>윈도우 기본 NVMe 드라이버</b>를 써요.')+'</p><div class="bt">'+bt('https://semiconductor.samsung.com/consumer-storage/support/tools/','Samsung Magician·NVMe 드라이버','삼성 반도체 공식',1)+'</div>';}
 else if(/^SM/.test(n)){h='<h3>갤럭시 휴대폰·태블릿 <span class="tg">USB 드라이버</span></h3><p>사진·파일 옮기기는 보통 드라이버 없이 돼요. 안드로이드 개발(ADB)을 할 때만 <b>삼성 Android USB 드라이버</b>를 깔아요.</p><div class="bt">'+bt('https://developer.samsung.com/android-usb-driver','삼성 Android USB 드라이버','developer.samsung.com',1)+'</div>';}
 else if(/^(LS|LC|LF|LU|S\\d{2}|C\\d{2}|F\\d{2}|U\\d{2})/.test(n)){h='<h3>삼성 모니터 <span class="tg">다운로드 자료실</span></h3><p>모니터는 연결하면 대부분 자동으로 인식돼요. 드라이버(.inf)나 <b>Easy Setting Box</b>는 다운로드 자료실에서 모델명 <b>'+esc(raw)+'</b>을 검색해 [드라이버]·[응용프로그램]에서 받아요.</p><div class="bt">'+bt(SV,'삼성전자서비스 다운로드 자료실','모델명 검색',1)+'</div>';}
 else h='<h3>모델을 알아보지 못했어요</h3><p>모델명 앞부분을 확인해 주세요. 노트북은 <b>NT</b>(해외 제품은 <b>NP</b>), 프린터는 <b>SL·ML·SCX</b>, SSD는 <b>MZ</b>, 휴대폰은 <b>SM</b>, 모니터는 <b>LS·LC</b> 등으로 시작해요.</p>';
 r.innerHTML=h}
$('sgb').addEventListener('click',run);$('sgq').addEventListener('keydown',function(e){if(e.key==='Enter')run()});var t;$('sgq').addEventListener('input',function(){clearTimeout(t);t=setTimeout(run,250)});
var m=location.hash.match(/^#m-([A-Za-z0-9-]+)$/);if(m){$('sgq').value=m[1];run()}})();</script>'''
JS=JS.replace('__BOOK__',js_book).replace('__WU__',json.dumps(WU))
s=s.replace('</main>',JS+'</main>',1)
open(OUT,'w',encoding='utf-8').write(s)
print(len(s))
