"""로봇청소기 앱·펌웨어 업데이트 — 에코백스·드리미·나르왈 (/driver/<key>.html, /en/driver/<key>.html)
2026-11-23 각 회사 공식 지원센터에서 확인:
- 에코백스 help.ecovacs.com 'Upgrade your DEEBOT - firmware upgrade'(us id=448, au id=1103):
  ECOVACS HOME 앱 → 로봇 들어가기 → 오른쪽 위 설정 → About DEEBOT → Update DEEBOT.
  스테이션에서 충전 중, 배터리 50% 이상(약 3시간 충전 권장), 앱 연결·와이파이 신호 강하게. 자동 업그레이드 켜면 자동으로 최신.
  앱: App Store id1329458504 (ECOVACS HOME), Google Play com.eco.global.app
- 드리미 support.dreametech.com 17134694199311 'How to Update Your Dreame Firmware':
  Dreamehome 앱 지도 화면 → 설정 → Firmware Upgrade (검색에서 'Firmware Upgrade' 찾기도 가능). 도크에서 충전, 2.4GHz,
  업데이트 중 사용·중단 금지, 끝나면 자동 재부팅, 순차 배포라 며칠 늦게 올 수 있음, 이전 버전은 고객센터.
  16949804692879: 실패 원인 = 배터리 15% 미만, 와이파이 약함.
  앱: App Store id1564419343, Google Play com.dreame.smartlife
- 나르왈 narwal.com 'Firmware Upgrade Policy': 앱 → 기기 관리 → 펌웨어 업데이트 → 자동 펌웨어 업데이트 켜기 / 새 버전 알림 '지금 업데이트' /
  '업데이트 확인'. 실패 원인 = 배터리 부족, 기기가 작업 중, 충전 이상, 네트워크. 실패하면 기기 재시작 후 다시, 휴대폰 핫스팟으로 시도.
  업데이트 후 이전 버전으로 되돌릴 수 없음.
  support.narwal.com 33680325904141: Narwal Freo 앱 설치 → 이메일 가입 → 블루투스 켜기 → 기기 추가 또는 덮개 안 QR 스캔 → 2.4GHz 와이파이.
  앱: App Store id1636748263 (Narwal Freo), Google Play com.narwal.pita_global
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en
from driver_robot import phone

E = cu.E

C = {
    'ecovacs': dict(
        ko='에코백스', en='ECOVACS', app='ECOVACS HOME', ios='id1329458504', pkg='com.eco.global.app',
        line='DEEBOT 디봇 로봇청소기',
        menu='ECOVACS HOME 앱 → 내 로봇 → 오른쪽 위 설정 → <b>About DEEBOT(디봇 정보)</b> → <b>Update DEEBOT(디봇 업데이트)</b>',
        menu_en='ECOVACS HOME app → your robot → Settings (top right) → <b>About DEEBOT</b> → <b>Update DEEBOT</b>',
        steps=[('로봇을 스테이션에 올려 충전', '로봇을 <b>충전 스테이션</b>에 올려 충전 중인지 확인해요. 에코백스는 배터리 <b>50% 이상</b>, 가능하면 <b>약 3시간</b> 충전한 뒤에 하라고 안내해요.',
                ('ECOVACS HOME', ['충전 중 🔌', '배터리 50% 이상', '와이파이 신호 강함'], '확인')),
               ('앱에서 로봇 들어가기', '<b>ECOVACS HOME</b> 앱에 로그인하고 내 로봇을 눌러 들어가요(가입·로그인은 본인이 직접 해요).',
                ('ECOVACS HOME', ['내 로봇 (DEEBOT)', '+ 로봇 추가', ''], '들어가기')),
               ('설정 → About DEEBOT', '오른쪽 위 <b>설정</b>(톱니바퀴)을 누르고 <b>About DEEBOT</b>(디봇 정보)를 눌러요.',
                ('설정', ['청소 설정', 'About DEEBOT  ›', '자동 업그레이드'], 'About')),
               ('Update DEEBOT 누르기', '<b>Update DEEBOT</b>(디봇 업데이트)를 눌러요. 새 버전이 있으면 화면 안내대로 업데이트하고, 끝날 때까지 로봇을 스테이션에서 빼지 마세요.',
                ('About DEEBOT', ['현재 버전 ****', '새 버전 있음', ''], 'Update'))],
        auto='앱에서 <b>자동 업그레이드</b>를 켜 두면 로봇이 알아서 최신 버전으로 업데이트해요.',
        fail=['로봇이 <b>스테이션에서 충전 중</b>인지 확인해요.', '배터리를 <b>50% 이상</b>으로 충전해요(약 3시간 권장).',
              '로봇이 앱에 <b>연결</b>돼 있고 <b>와이파이 신호가 강한지</b> 확인해요. 공유기 가까이 두면 좋아요.'],
        src='에코백스 지원센터(help.ecovacs.com) \'Upgrade your DEEBOT - firmware upgrade\'',
        src_en='ECOVACS Support (help.ecovacs.com) "Upgrade your DEEBOT - firmware upgrade"',
        models=['DEEBOT X8 PRO OMNI', 'DEEBOT X5 PRO OMNI', 'DEEBOT X2 OMNI', 'DEEBOT X1 OMNI', 'DEEBOT T80 OMNI', 'DEEBOT T50 PRO OMNI', 'DEEBOT T30 OMNI', 'DEEBOT T20 OMNI', 'DEEBOT N30 PRO OMNI', 'DEEBOT N20', 'DEEBOT N10'],
        kw='에코백스 업데이트 에코백스 펌웨어 업데이트 디봇 업데이트 DEEBOT 업데이트 ECOVACS HOME 앱 에코백스 앱 로봇청소기 업데이트 X8 T30 T50'),
    'dreame': dict(
        ko='드리미', en='Dreame', app='Dreamehome', ios='id1564419343', pkg='com.dreame.smartlife',
        line='로봇청소기',
        menu='Dreamehome 앱 → 로봇 지도 화면 → <b>설정</b> → <b>펌웨어 업그레이드(Firmware Upgrade)</b>',
        menu_en='Dreamehome app → robot map page → <b>Settings</b> → <b>Firmware Upgrade</b>',
        steps=[('준비: 도크 충전·2.4GHz·앱 최신', '로봇을 <b>도크에 올려 충전</b>해요. 휴대폰은 집의 <b>2.4GHz 와이파이</b>(5GHz 말고)에 연결하고, <b>Dreamehome 앱</b>을 앱 스토어에서 최신으로 업데이트해요.',
                ('Dreamehome', ['도크에서 충전 중 🔌', '2.4GHz 와이파이', '앱 최신 버전'], '확인')),
               ('지도 화면 → 설정', 'Dreamehome 앱에서 내 로봇의 <b>지도 화면</b>을 열고 <b>설정</b>을 눌러요. 검색 아이콘에서 <b>Firmware Upgrade</b>를 검색해도 돼요.',
                ('지도 화면', ['🗺️ 우리 집 지도', '청소 시작', '설정  ›'], '설정')),
               ('펌웨어 업그레이드', '<b>펌웨어 업그레이드(Firmware Upgrade)</b>를 눌러요. 새 버전이 있으면 <b>버전 번호와 업그레이드 안내</b>가 보여요.',
                ('설정', ['청소 설정', '펌웨어 업그레이드  ›', '기기 정보'], '업그레이드')),
               ('끝날 때까지 기다리기', '업그레이드 버튼을 누르고 기다려요. 받는 중·설치 중에는 <b>로봇을 쓰거나 중단하지 마세요</b>. 끝나면 로봇이 <b>자동으로 다시 켜져요</b>.',
                ('펌웨어 업그레이드', ['다운로드 중…', '설치 중…', '끝나면 자동 재시작'], '확인'))],
        auto='새 펌웨어는 <b>순서대로 나눠서 배포</b>돼서, 다른 사람보다 며칠 늦게 보일 수 있어요. 일주일이 지나도 안 보이면 아래 해결법을 해 보세요.',
        fail=['배터리가 <b>15% 미만</b>이면 업데이트가 안 돼요. 도크에서 충분히 충전한 뒤 다시 해요.',
              '<b>와이파이 신호가 약하면</b> 받는 중에 끊겨요. 로봇을 공유기 가까이 두고, 로봇과 도크 사이를 막는 물건을 치워요.',
              '계속 실패하면 <b>오류 문구를 그대로 적어</b> 드리미 고객센터에 문의해요.',
              '예전 버전으로 되돌리려면 <b>고객센터에 문의</b>해야 해요.'],
        src='드리미 지원센터(support.dreametech.com) \'How to Update Your Dreame Firmware\', \'펌웨어 업데이트 실패 시\'',
        src_en='Dreame Support (support.dreametech.com) "How to Update Your Dreame Firmware"',
        models=['X50 Ultra', 'X40 Ultra', 'X30 Ultra', 'L40 Ultra', 'L20 Ultra', 'L10s Ultra', 'L10s Pro Ultra', 'D10 Plus', 'D9 Max'],
        kw='드리미 업데이트 드리미 펌웨어 업데이트 드리미 로봇청소기 업데이트 Dreamehome 앱 드리미 앱 X50 X40 L20 L10s'),
    'narwal': dict(
        ko='나르왈', en='Narwal', app='Narwal Freo', ios='id1636748263', pkg='com.narwal.pita_global',
        line='Freo 프레오 로봇청소기',
        menu='나르왈 앱 → <b>기기 관리</b> → <b>펌웨어 업데이트</b> → <b>업데이트 확인</b> (자동 펌웨어 업데이트도 여기서 켜요)',
        menu_en='Narwal app → <b>Device management</b> → <b>Firmware updates</b> → <b>Check for updates</b> (turn on Automatic firmware updates here)',
        steps=[('앱 설치·로봇 연결', '<b>Narwal Freo</b> 앱을 설치하고 이메일로 가입해요(본인이 직접). 휴대폰 <b>블루투스</b>를 켜고, 기기 추가에서 모델을 고르거나 로봇 <b>윗덮개 안 QR 코드</b>를 스캔해요. 와이파이는 <b>2.4GHz만</b> 돼요.',
                ('Narwal', ['+ 기기 추가', 'QR 코드 스캔', '2.4GHz 와이파이'], '추가')),
               ('기기 관리 → 펌웨어 업데이트', '앱에서 <b>기기 관리</b> → <b>펌웨어 업데이트</b>로 들어가요.',
                ('기기 관리', ['기기 정보', '펌웨어 업데이트  ›', '자동 펌웨어 업데이트'], '열기')),
               ('업데이트 확인 → 지금 업데이트', '<b>업데이트 확인</b>을 눌러요. 새 버전 알림이 뜨면 <b>지금 업데이트</b>를 눌러요.',
                ('펌웨어 업데이트', ['업데이트 확인', '새 버전 있음', ''], '지금 업데이트')),
               ('자동 업데이트 켜 두기', '<b>자동 펌웨어 업데이트</b>를 켜 두면 다음부터는 알아서 최신 버전을 설치해요.',
                ('펌웨어 업데이트', ['자동 펌웨어 업데이트  ●', '업데이트 확인', ''], '켜기'))],
        auto='나르왈은 업데이트한 뒤에는 <b>예전 버전으로 되돌릴 수 없어요</b>(보안 때문). 그리고 예전 버전에는 보안 업데이트를 주지 않으니 최신 버전을 쓰라고 안내해요.',
        fail=['<b>배터리가 부족</b>하거나, 로봇이 <b>청소 중</b>이거나, <b>충전이 이상</b>하면 실패할 수 있어요. 충전하고 쉬는 상태에서 해요.',
              '로봇·스테이션의 <b>네트워크 문제</b>로도 실패해요.', '실패하면 <b>로봇을 껐다 켜고</b> 다시 수동 업데이트해요.',
              '공유기가 업데이트 파일을 막는 경우가 있어요. 휴대폰 <b>핫스팟</b>에 연결해서 해 보세요.'],
        src='나르왈 공식 \'Firmware Upgrade Policy\', 나르왈 지원센터 \'Download the Narwal Freo App and Create an Account\'',
        src_en='Narwal "Firmware Upgrade Policy" and Narwal Support "Download the Narwal Freo App"',
        models=['Freo Z Ultra', 'Freo X Ultra', 'Freo X Plus', 'Freo Pro', 'Freo', 'Freo Z10'],
        kw='나르왈 업데이트 나르왈 펌웨어 업데이트 나르왈 프레오 업데이트 Narwal Freo 앱 나르왈 앱 로봇청소기 업데이트'),
}


def links(c, lang='ko'):
    i = f'https://apps.apple.com/{"kr" if lang == "ko" else "us"}/app/{c["ios"]}'
    a = f'https://play.google.com/store/apps/details?id={c["pkg"]}&hl={lang}'
    return a, i


def ko(key):
    c = C[key]; path = f'/driver/{key}.html'; a, i = links(c)
    cr, crld = kr.crumb([(f'{c["ko"]} 앱·펌웨어', '')])
    ans = (f'{c["ko"]} 로봇청소기는 PC 드라이버가 없고, 휴대폰 <b>{c["app"]} 앱</b>으로 연결해서 <b>앱 안에서 펌웨어(로봇 소프트웨어)를 업데이트</b>해요. '
           f'{c["ko"]} 공식 안내: {c["menu"]}.')
    steps = ''.join(cu.step(n + 1, t, b, phone(p[0], p[1], p[2], n + 1)) for n, (t, b, p) in enumerate(c['steps']))
    fail = '<ul class="cu-chk">' + ''.join(f'<li>{x}</li>' for x in c['fail']) + f'</ul><p class="cu-src">출처: {E(c["src"])}.</p>'
    qa = [(f'{c["ko"]} 드라이버를 PC에 깔아야 하나요?', f'아니요. {c["ko"]} 로봇청소기는 휴대폰 {c["app"]} 앱으로 연결하고, 로봇 소프트웨어(펌웨어)도 앱 안에서 업데이트해요.'),
          ('펌웨어 업데이트는 어디서 해요?', f'{c["ko"]} 공식 안내: ' + kr.re.sub('<[^>]+>', '', c['menu']) + '.'),
          ('업데이트가 안 돼요.', ' '.join(kr.re.sub('<[^>]+>', '', x) for x in c['fail'][:2])),
          ('앱 화면이 이 페이지 설명과 달라요.', '앱이 업데이트되면 메뉴 이름이나 순서가 조금 달라질 수 있어요. 앱 화면의 안내를 따르세요.'),
          ('앱은 무료인가요?', f'네. {c["app"]} 앱은 구글 플레이와 App Store에서 무료로 받아요.')]
    fq, fqld = cu.faq(qa)
    models = ('<section class="card"><h2>이 방법이 쓰이는 제품 예시</h2><p>' + E(c['app']) + ' 앱으로 연결하는 ' + E(c['ko']) + ' 로봇청소기는 같은 방법으로 펌웨어를 업데이트해요.</p><ul class="nm">'
              + ''.join(f'<li><span style="display:inline-block;padding:6px 10px;border-radius:999px;background:#F1F3F5;font-size:13px">{E(c["ko"])} {E(m)}</span></li>' for m in c['models'])
              + '</ul><p class="cu-src">제품마다 앱 메뉴 이름이 조금 다를 수 있어요.</p></section>')
    apps = (f'<ul class="hpl"><li class="hpm"><h3>{E(c["app"])} 앱 (공식, 무료)</h3><p class="fi">로봇 연결, 청소 지도, 예약 청소, 펌웨어 업데이트를 하는 {E(c["ko"])} 공식 앱이에요.</p>'
            f'<div class="bt">{kr.dl(a, "안드로이드 (구글 플레이)", c["app"] + " 앱 받기")}{kr.dl(i, "아이폰 (App Store)", c["app"] + " 앱 받기", True)}</div></li></ul>')
    main = (kr.HP_CSS + '<style>.nm{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:8px 0 0}</style>'
            + f'<header class="top hub">{cr}<h1>{E(c["ko"])} 로봇청소기 펌웨어 업데이트 방법 — {E(c["app"])} 앱 설치·업데이트</h1>'
            f'<p class="lead">{E(c["ko"])} {E(c["line"])}를 {E(c["app"])} 앱에 연결하고, 앱에서 펌웨어(로봇 소프트웨어)를 최신으로 업데이트하는 방법을 그림으로 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + kr.dl(a, f'{c["app"]} 앱 받기 (안드로이드)', f'구글 플레이 · {c["ko"]} 공식') + kr.dl(i, f'{c["app"]} 앱 받기 (아이폰)', f'App Store · {c["ko"]} 공식', True)
            + '<ul class="dr-toc"><li><a href="#steps">업데이트 순서</a></li><li><a href="#fail">업데이트가 안 될 때</a></li></ul></header>'
            f'<section class="card dr-sec" id="apps"><h2>공식 앱 받기</h2>{apps}</section>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 펌웨어 업데이트 순서</h2>{steps}<p class="cu-ans">{c["auto"]}</p></section>'
            f'<section class="card dr-sec" id="fail"><h2>업데이트가 안 될 때</h2>{fail}</section>'
            + models + fq + kr.src_sec(c['src']) + kr.REL)
    ld = [crld, fqld, kr.howto(f'{c["ko"]} 펌웨어 업데이트 방법', [t for t, _, _ in c['steps']])]
    kr.write(path, f'{c["ko"]} 펌웨어 업데이트 방법 — {c["app"]} 앱 (로봇청소기) | 홍라이프 도구',
             f'{c["ko"]} 로봇청소기 펌웨어는 ' + kr.re.sub('<[^>]+>', '', c['menu']) + f'에서 해요. 앱 받기, 업데이트 순서, 안 될 때 해결법을 {c["ko"]} 공식 안내대로 쉽게 정리했어요.',
             main, ld)
    return path


def en_page(key):
    c = C[key]; path = f'/en/driver/{key}.html'; a, i = links(c, 'en')
    cr, crld = en.crumb([(c['en'], '')])
    body = (f'<ol class="big-n"><li>Install the <b>{E(c["app"])} app</b> (free) and add your robot on <b>2.4GHz</b> Wi-Fi.</li>'
            f'<li>Keep the robot charging on its dock.</li><li>Open {c["menu_en"]}.</li><li>Install the new version and wait until it finishes.</li></ol>'
            '<ul class="cu-chk">' + ''.join(f'<li>{x}</li>' for x in {
                'ecovacs': ['Battery 50% or more (about 3 hours of charging recommended).', 'Strong Wi-Fi signal and robot connected to the app.', 'Turn on automatic upgrades to stay up to date.'],
                'dreame': ['Battery below 15% or weak Wi-Fi makes the update fail.', 'Do not use or interrupt the robot while it updates; it restarts by itself.', 'Updates roll out in batches, so yours may arrive a few days later.'],
                'narwal': ['Low battery, a busy robot, abnormal charging or network problems can make it fail.', 'Restart the robot and retry; a phone hotspot can help if your router blocks the download.', 'You cannot roll back to an older firmware after updating.']}[key]) + '</ul>')
    qa = [('Is there a PC driver?', f'No. {c["en"]} robots are set up and updated in the {c["app"]} app.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>{E(c["en"])} Firmware Update — {E(c["app"])} App</h1>'
            f'<p class="lead">How to update a {E(c["en"])} robot vacuum, following {E(c["en"])}\'s official support.</p>'
            + en.dl(a, f'{c["app"]} app (Android)', 'Google Play') + en.dl(i, f'{c["app"]} app (iPhone)', 'App Store', True) + '</header>'
            f'<section class="card dr-sec"><h2>Steps</h2>{body}</section>' + fq + en.src(c['src_en']) + en.REL)
    en.write(path, f'{c["en"]} Firmware Update — {c["app"]} App | HongLife Tools',
             f'Update {c["en"]} robot vacuum firmware in the {c["app"]} app and fix update problems, based on official {c["en"]} support.', main, [crld, fqld])
    return path


if __name__ == '__main__':
    for k in C:
        print(ko(k), en_page(k))
