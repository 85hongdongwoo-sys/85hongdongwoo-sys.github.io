"""로봇청소기 앱·펌웨어 업데이트 페이지 — 로보락 (/driver/roborock.html, /en/driver/roborock.html)
2026-11-22 로보락 공식 지원센터(support.roborock.com)에서 확인:
- 'Download links and QR code of Roborock App'(10752008947609): App Store id1462875428, Google Play com.roborock.smart
- 'How do I upgrade the firmware of S6 MaxV?'(900002175343): Roborock 앱 설정 → 펌웨어 업데이트 / Mi Home 앱 설정 → 펌웨어 업데이트
- 'Wi-Fi connection fails or robot shows as offline'(360035369812): 5GHz 미지원, 비밀번호 확인, 위치 권한, iOS 로컬 네트워크, 로봇 Wi-Fi 아닌 집 Wi-Fi 선택, 특수문자, WEP 미지원, 재부팅
- 'Connecting Roborock robots to Roborock App (Android)'(4405898659865): 앱 업데이트에 따라 과정이 달라질 수 있으니 앱 안내를 따를 것
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en

E = cu.E
IOS = 'https://apps.apple.com/kr/app/roborock/id1462875428'
AND = 'https://play.google.com/store/apps/details?id=com.roborock.smart&hl=ko'
SUP = 'https://support.roborock.com/hc/en-us'
FW = 'https://support.roborock.com/hc/en-us/articles/900002175343'
WIFI = 'https://support.roborock.com/hc/en-us/articles/360035369812'
MODELS = ['Saros 10R', 'Saros 10', 'Qrevo Curv', 'Qrevo Master', 'Qrevo MaxV', 'Qrevo S', 'Qrevo', 'S8 MaxV Ultra', 'S8 Pro Ultra', 'S8+', 'S8',
          'S7 MaxV Ultra', 'S7 Max Ultra', 'S7+', 'S7', 'S6 MaxV', 'S6 Pure', 'S6', 'S5 Max', 'S5', 'Q8 Max', 'Q7 Max', 'Q5', 'E5', 'E4']


def phone(title, lines, button, n):
    """휴대폰 앱 화면을 단순하게 그린 그림"""
    t = (f'<rect x="120" y="14" width="120" height="186" rx="16" fill="#0F172A"/><rect x="128" y="30" width="104" height="156" rx="6" fill="#fff"/>'
         f'<text x="180" y="50" text-anchor="middle" font-size="10" font-weight="800" fill="#111">{E(title)}</text>')
    y = 70
    for ln in lines:
        t += f'<rect x="134" y="{y - 11}" width="92" height="18" rx="4" fill="#F1F3F5"/><text x="140" y="{y + 2}" font-size="8.5" fill="#333">{E(ln)}</text>'
        y += 24
    t += cu.btn(140, 158, 80, 22, button) + cu.ring(140, 158, 80, 22, n)
    return f'<svg viewBox="0 0 360 214" role="img" {cu.FONT}>{t}</svg>'


def roborock():
    path = '/driver/roborock.html'
    cr, crld = kr.crumb([('로보락 앱·펌웨어', '')])
    ans = ('로보락 로봇청소기는 PC 드라이버가 없고, 휴대폰 <b>Roborock 앱</b>으로 연결해서 <b>앱 안에서 펌웨어(로봇 소프트웨어)를 업데이트</b>해요. '
           '로보락 공식 안내: <b>Roborock 앱 → 로봇 선택 → 설정 → 펌웨어 업데이트</b>. 샤오미 <b>Mi Home</b> 앱에 연결했다면 <b>설정 → 펌웨어 업데이트</b>예요.')
    apps = ('<ul class="hpl"><li class="hpm"><h3>Roborock 앱 (공식, 무료)</h3><p class="fi">로봇 연결, 청소 지도, 예약 청소, 펌웨어 업데이트를 하는 로보락 공식 앱이에요.</p>'
            f'<div class="bt">{kr.dl(AND, "안드로이드 (구글 플레이)", "Roborock 앱 받기")}{kr.dl(IOS, "아이폰 (App Store)", "Roborock 앱 받기", True)}</div></li></ul>')
    steps = (cu.step(1, '앱 설치하고 로그인', '위 버튼으로 <b>Roborock 앱</b>을 설치하고 회원가입·로그인해요(가입은 본인이 직접 해요).',
                     phone('Roborock', ['내 기기', '+ 기기 추가', ''], '기기 추가', 1))
             + cu.step(2, '로봇을 집 와이파이에 연결', '앱의 <b>기기 추가</b>를 눌러 화면 안내대로 연결해요. 로봇 와이파이가 아니라 <b>우리 집 와이파이</b>를 고르고 비밀번호를 넣어요. 로보락 로봇은 <b>5GHz 와이파이를 지원하지 않으니 2.4GHz</b>를 고르세요.',
                       phone('Wi-Fi 선택', ['우리집_2.4G  ✓', '우리집_5G (안 됨)', '비밀번호 ****'], '다음', 2))
             + cu.step(3, '설정 → 펌웨어 업데이트', '앱에서 내 로봇을 누르고 <b>설정</b>(톱니바퀴)으로 들어가 <b>펌웨어 업데이트</b>를 눌러요. 새 버전이 있으면 <b>업데이트</b>를 눌러요.',
                       phone('설정', ['청소 설정', '펌웨어 업데이트  ›', '기기 정보'], '업데이트', 3))
             + cu.step(4, '끝날 때까지 기다리기', '업데이트하는 동안 앱 화면 안내를 따르고, 끝날 때까지 로봇을 움직이거나 전원을 끄지 마세요. 끝나면 앱에서 새 버전 번호를 확인할 수 있어요.',
                       phone('펌웨어 업데이트', ['업데이트 중…', '잠시 기다려 주세요', ''], '확인', 4)))
    wifi = ('<ul class="cu-chk"><li>로보락 로봇은 <b>5GHz 와이파이를 지원하지 않아요.</b> 공유기의 2.4GHz 이름으로 연결하세요.</li>'
            '<li>와이파이 <b>비밀번호</b>를 정확히 넣었는지 확인해요.</li>'
            '<li>휴대폰에서 Roborock 앱에 <b>위치 권한</b>을 켜 주세요. 아이폰(iOS 14 이상)은 <b>로컬 네트워크</b> 권한도 켜야 해요.</li>'
            '<li>와이파이 목록에서 로봇 이름이 아니라 <b>우리 집 와이파이</b>를 골라요.</li>'
            '<li>와이파이 이름·비밀번호에 <b>!@#$ 같은 특수문자</b>가 있으면 공유기 설정에서 빼는 게 좋아요.</li>'
            '<li>공유기 보안 방식이 <b>WEP</b>이면 지원하지 않아요. WPA 또는 WPA2로 바꿔요.</li>'
            '<li>로봇과 공유기를 <b>껐다 켜고</b> 다시 해 봐요.</li></ul>'
            '<p class="cu-src">출처: 로보락 지원센터 \'Wi-Fi 연결이 안 되거나 앱에서 오프라인으로 보일 때\'.</p>')
    qa = [('로보락 드라이버를 PC에 깔아야 하나요?', '아니요. 로보락 로봇청소기는 휴대폰 Roborock 앱으로 연결하고, 로봇 소프트웨어(펌웨어)도 앱 안에서 업데이트해요.'),
          ('펌웨어 업데이트는 어디서 해요?', '로보락 공식 안내: Roborock 앱 → 설정 → 펌웨어 업데이트. Mi Home 앱에 연결한 경우 설정 → 펌웨어 업데이트예요.'),
          ('로봇이 와이파이에 연결이 안 돼요.', '5GHz가 아닌 2.4GHz 와이파이를 고르고, 앱 위치 권한(아이폰은 로컬 네트워크 권한도)을 켜고, 비밀번호와 특수문자·WEP 보안 방식을 확인하세요.'),
          ('앱 화면이 이 페이지 설명과 달라요.', '로보락 안내대로 앱 업데이트에 따라 순서가 조금 달라질 수 있어요. 앱 화면의 안내를 따르세요.'),
          ('앱은 무료인가요?', '네. Roborock 앱은 구글 플레이와 App Store에서 무료로 받아요.')]
    fq, fqld = cu.faq(qa)
    models = ('<section class="card"><h2>이 방법이 쓰이는 로보락 제품 예시</h2><p>Roborock 앱으로 연결하는 로보락 로봇청소기는 같은 방법으로 펌웨어를 업데이트해요.</p><ul class="nm">'
              + ''.join(f'<li><span style="display:inline-block;padding:6px 10px;border-radius:999px;background:#F1F3F5;font-size:13px">로보락 {E(m)}</span></li>' for m in MODELS)
              + '</ul><p class="cu-src">제품마다 앱 메뉴 이름이 조금 다를 수 있어요.</p></section>')
    main = (kr.HP_CSS + '<style>.nm{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:8px 0 0}</style>'
            + f'<header class="top hub">{cr}<h1>로보락 로봇청소기 앱·펌웨어 업데이트 방법 — Roborock 앱 설치·와이파이 연결</h1>'
            '<p class="lead">로보락 로봇청소기를 Roborock 앱에 연결하고, 앱에서 펌웨어(로봇 소프트웨어)를 최신으로 업데이트하는 방법을 그림으로 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ans}</p>' + kr.dl(AND, 'Roborock 앱 받기 (안드로이드)', '구글 플레이 · 로보락 공식') + kr.dl(IOS, 'Roborock 앱 받기 (아이폰)', 'App Store · 로보락 공식', True)
            + '<ul class="dr-toc"><li><a href="#steps">업데이트 순서</a></li><li><a href="#wifi">와이파이 연결이 안 될 때</a></li></ul></header>'
            f'<section class="card dr-sec" id="apps"><h2>공식 앱 받기</h2>{apps}</section>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 펌웨어 업데이트 순서</h2>{steps}</section>'
            f'<section class="card dr-sec" id="wifi"><h2>와이파이 연결이 안 될 때</h2>{wifi}</section>'
            + models + fq
            + kr.src_sec('로보락 지원센터(support.roborock.com) \'Roborock 앱 다운로드 링크\', \'펌웨어 업그레이드 방법\', \'Wi-Fi 연결 실패 시\'')
            + kr.REL)
    ld = [crld, fqld, kr.howto('로보락 펌웨어 업데이트 방법', ['Roborock 앱 설치·로그인', '로봇을 2.4GHz 집 와이파이에 연결', '설정 → 펌웨어 업데이트', '끝날 때까지 기다리기'])]
    kr.write(path, '로보락 펌웨어 업데이트 방법 — Roborock 앱 설치·와이파이 연결 (로봇청소기) | 홍라이프 도구',
             '로보락 로봇청소기 펌웨어는 Roborock 앱 → 설정 → 펌웨어 업데이트에서 해요. 앱 받기, 2.4GHz 와이파이 연결, 연결이 안 될 때 해결법을 로보락 공식 안내대로 쉽게 정리했어요.',
             main, ld)
    return path


def roborock_en():
    path = '/en/driver/roborock.html'
    cr, crld = en.crumb([('Roborock', '')])
    body = ('<ol class="big-n"><li>Install the <b>Roborock app</b> (free).</li><li>Add your robot and connect it to your <b>2.4GHz</b> home Wi-Fi (5GHz and WEP are not supported).</li>'
            '<li>Open the robot → <b>Settings → Firmware Updates</b> (Mi Home app: Settings → Update Firmware).</li><li>Wait until the update finishes.</li></ol>')
    qa = [('Is there a PC driver?', 'No. Roborock robots are set up and updated in the Roborock app.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>Roborock Firmware Update — Roborock App &amp; Wi-Fi Setup</h1>'
            '<p class="lead">How to update a Roborock robot vacuum, following Roborock\'s official support center.</p>'
            + en.dl(AND.replace('hl=ko', 'hl=en'), 'Roborock app (Android)', 'Google Play') + en.dl(IOS.replace('/kr/', '/us/'), 'Roborock app (iPhone)', 'App Store', True) + '</header>'
            f'<section class="card dr-sec"><h2>Steps</h2>{body}</section>' + fq + en.src('Roborock Support Center (support.roborock.com)') + en.REL)
    en.write(path, 'Roborock Firmware Update — Roborock App, Wi-Fi Setup | HongLife Tools',
             'Update Roborock robot vacuum firmware in the Roborock app (Settings → Firmware Updates) and fix Wi-Fi setup problems.', main, [crld, fqld])
    return path


if __name__ == '__main__':
    print(roborock(), roborock_en())
