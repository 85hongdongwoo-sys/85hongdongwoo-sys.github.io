"""노트북·PC 회사 드라이버 페이지 (레노버·델·에이수스·에이서) — 한국어 /driver/<k>.html, 영어 /en/driver/<k>.html
2026-11-22 공식 페이지에서 확인한 내용만 씀:
- 레노버: 'Lenovo 시스템 업데이트'(DS012808, system_update_5.08.01.exe, 8.28MB, 2023-02-06 배포, ThinkPad·ThinkCentre·ThinkStation·V/B/K/E 시리즈),
         'Lenovo Vantage'(HT505081, 윈도우 11·10, Microsoft Store 9WZDNCRFJ4MV — 드라이버 업데이트·진단·기술 지원)
- 델: '홈 PC용 SupportAssist'(dell.com/support ko-kr, 설치 파일 downloads.dell.com/serviceability/catalog/SupportAssistInstaller.exe — 자동 스캔·업데이트 설치)
- 에이수스: MyASUS(Microsoft Store 9N7R5S6B0ZZH), ASUS 다운로드 센터(모델명·시리얼번호로 드라이버·펌웨어·소프트웨어)
- 에이서: Acer 지원 '드라이버 및 매뉴얼 다운로드'(acer.com/kr-ko)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en

E = cu.E
MS = 'https://apps.microsoft.com/detail/{}?hl=ko-kr&gl=KR'

C = {
    'lenovo': {
        'name': '레노버', 'en': 'Lenovo',
        'lines': 'ThinkPad·IdeaPad·Legion·Yoga·ThinkCentre',
        'ans': '레노버 노트북·PC는 <b>Lenovo Vantage</b>(Microsoft Store, 무료)로 드라이버를 업데이트하는 게 가장 쉬워요. <b>ThinkPad·ThinkCentre·ThinkStation</b>은 <b>Lenovo 시스템 업데이트</b>(System Update) 프로그램으로 드라이버·BIOS·앱을 한 번에 받을 수도 있어요. 개별 파일은 레노버 지원 사이트에서 제품명이나 시리얼 번호로 찾아요.',
        'tools': [
            ('Lenovo Vantage (일반 사용자 추천)', '드라이버 업데이트, 진단 검사, 기술 지원 요청을 할 수 있는 레노버 공식 앱이에요. 윈도우 11·10용이에요(윈도우 10 IoT는 지원 안 함).',
             MS.format('9WZDNCRFJ4MV'), 'Lenovo Vantage 받기', 'Microsoft Store · 레노버 공식 · 무료', False),
            ('Lenovo 시스템 업데이트 (System Update)', '소프트웨어·드라이버·BIOS 업데이트를 내려받아 설치해 주는 레노버 프로그램이에요. 지원 제품: 모든 ThinkPad·ThinkCentre·ThinkStation, Lenovo V/B/K/E 시리즈 등. 버전 5.08.01 · 8.28MB.',
             'https://download.lenovo.com/pccbbs/thinkvantage_en/system_update_5.08.01.exe', 'System Update 바로 받기', '레노버 서버에서 바로 다운로드 · .exe', True),
        ],
        'site': ('https://pcsupport.lenovo.com/kr/ko/', '레노버 지원 사이트 (제품별 드라이버)', '제품명·시리얼 번호로 찾기'),
        'serial': '노트북 바닥면 스티커의 <b>S/N</b>(시리얼 번호)이나 Lenovo Vantage 첫 화면에서 볼 수 있어요.',
        'src': '레노버 지원 \'Lenovo 시스템 업데이트\'(DS012808), \'Lenovo Vantage: PC 사용이 더욱 쉬워졌습니다\'(HT505081)',
        'kw': '레노버 드라이버 Lenovo 드라이버 씽크패드 드라이버 ThinkPad 드라이버 아이디어패드 드라이버 Lenovo Vantage System Update',
    },
    'dell': {
        'name': '델', 'en': 'Dell',
        'lines': 'Inspiron·XPS·Vostro·Latitude·Alienware',
        'ans': '델 노트북·PC는 <b>SupportAssist</b>(홈 PC용, 무료)를 설치하면 PC를 자동으로 검사해 <b>필요한 드라이버·소프트웨어 업데이트를 찾아 설치</b>해 줘요. 개별 파일은 델 지원 사이트에서 <b>서비스 태그</b>(제품 고유 번호)로 내 PC를 찾아 받아요.',
        'tools': [
            ('SupportAssist (홈 PC용)', 'PC 상태를 검사하고, 사용 가능한 업데이트를 자동으로 찾아 설치해 주는 델 공식 프로그램이에요. 업데이트가 있으면 알림이 오고, 알림을 누르거나 SupportAssist에서 [소프트웨어 업데이트]를 누르면 돼요.',
             'https://downloads.dell.com/serviceability/catalog/SupportAssistInstaller.exe', 'SupportAssist 바로 받기', '델 서버에서 바로 다운로드 · .exe', False),
        ],
        'site': ('https://www.dell.com/support/home/ko-kr', '델 지원 사이트 (제품별 드라이버)', '서비스 태그로 찾기'),
        'serial': '노트북 바닥면이나 본체 옆 스티커의 <b>Service Tag</b>(7자리 영문·숫자)를 보세요.',
        'src': '델 대한민국 \'홈 PC용 SupportAssist\'',
        'kw': '델 드라이버 Dell 드라이버 델 노트북 드라이버 Inspiron 드라이버 XPS 드라이버 SupportAssist 서비스 태그',
    },
    'asus': {
        'name': '에이수스', 'en': 'ASUS',
        'lines': 'Vivobook·Zenbook·ROG·TUF·메인보드',
        'ans': '에이수스 노트북은 <b>MyASUS</b> 앱(Microsoft Store, 무료)으로 드라이버를 업데이트하는 게 쉬워요. 메인보드·그래픽카드·모니터 같은 부품은 <b>ASUS 다운로드 센터</b>에서 모델명이나 시리얼 번호를 넣으면 드라이버·펌웨어·소프트웨어가 나와요.',
        'tools': [
            ('MyASUS', '에이수스 노트북 사용자를 위한 에이수스 공식 앱이에요. Microsoft Store에서 무료로 받아요.',
             MS.format('9N7R5S6B0ZZH'), 'MyASUS 받기', 'Microsoft Store · 에이수스 공식 · 무료', False),
        ],
        'site': ('https://www.asus.com/kr/support/download-center/', 'ASUS 다운로드 센터', '모델명·시리얼번호로 드라이버·펌웨어 찾기'),
        'serial': '제품 바닥면이나 상자의 <b>S/N</b>을 보세요. ASUS 다운로드 센터는 이 컴퓨터의 시리얼 번호를 자동으로 감지하는 기능도 있어요.',
        'src': 'ASUS 한국 \'다운로드 센터\', Microsoft Store MyASUS',
        'kw': '에이수스 드라이버 ASUS 드라이버 아수스 드라이버 MyASUS 젠북 드라이버 비보북 드라이버 ROG 드라이버 메인보드 드라이버',
    },
    'acer': {
        'name': '에이서', 'en': 'Acer',
        'lines': 'Aspire·Swift·Nitro·Predator·TravelMate',
        'ans': '에이서 노트북·PC·모니터 드라이버는 <b>Acer 지원 → 드라이버 및 매뉴얼</b>에서 <b>시리얼 번호(S/N)·SNID</b>나 제품 모델로 찾아 받아요. 윈도우 업데이트로 기본 드라이버가 자동으로 깔리는 경우도 많아요.',
        'tools': [],
        'site': ('https://www.acer.com/kr-ko/support/drivers-and-manuals', 'Acer 드라이버 및 매뉴얼 다운로드', '시리얼 번호·모델로 찾기'),
        'serial': '노트북 바닥면 스티커의 <b>S/N</b>이나 <b>SNID</b>를 보세요.',
        'src': 'Acer 한국 \'Acer 지원 드라이버 및 매뉴얼 다운로드\'',
        'kw': '에이서 드라이버 Acer 드라이버 에이서 노트북 드라이버 Aspire 드라이버 Swift 드라이버 Nitro 드라이버 Predator 드라이버',
    },
}


def page(k):
    c = C[k]
    path = f'/driver/{k}.html'
    cr, crld = kr.crumb([(f'{c["name"]} 드라이버', '')])
    tools = ''.join(
        f'<li class="hpm"><h3>{E(t)}</h3><p class="fi">{d}</p><div class="bt">{kr.dl(u, bt, bs, i > 0)}</div></li>'
        for i, (t, d, u, bt, bs, _) in enumerate(c['tools']))
    su, st, ss = c['site']
    first = c['tools'][0] if c['tools'] else None
    steps = '<ol class="big-n">'
    if first:
        steps += (f'<li>위 <b>[{E(first[3])}]</b>를 눌러 받아요. ' + ('Microsoft Store 페이지가 열리면 <b>[받기]</b>를 눌러 설치해요.' if 'microsoft' in first[2] else '받은 파일을 <b>Ctrl + J</b>로 열고, 윈도우 확인 창에서 <b>[예]</b>를 눌러 설치해요.') + '</li>'
                  f'<li>설치한 프로그램을 열고 <b>업데이트 확인</b>(검사)을 눌러요. 내 PC에 맞는 드라이버·BIOS 업데이트가 목록으로 나와요.</li>'
                  '<li>목록의 업데이트를 설치하고, 다시 시작하라고 하면 <b>컴퓨터를 다시 시작</b>해요. 노트북은 <b>전원을 꽂은 상태</b>에서 하세요(BIOS 업데이트 중 꺼지면 위험해요).</li>')
    steps += (f'<li>프로그램 없이 받고 싶으면 <b>{E(st)}</b>에서 {E(ss)} → 내 윈도우 버전 → 필요한 드라이버(그래픽·오디오·무선랜 등)를 받아 실행해요.</li></ol>')
    qa = [(f'{c["name"]} 드라이버는 어디서 받아야 안전해요?', f'{c["name"]} 공식 사이트나 공식 앱, 또는 Windows 업데이트에서 받으세요. 광고에 나오는 \'드라이버 자동 설치\' 프로그램은 쓰지 마세요.'),
          ('내 제품 모델을 모르겠어요.', c['serial'].replace('<b>', '').replace('</b>', '')),
          ('BIOS 업데이트도 해야 하나요?', '문제가 있거나 제조사가 권할 때만 하세요. 하는 동안 전원이 꺼지면 위험하니 노트북은 반드시 충전기를 꽂고 하세요.'),
          ('윈도우를 새로 깔았더니 와이파이가 안 돼요.', '무선랜 드라이버가 아직 없어서 그래요. 다른 컴퓨터로 공식 사이트에서 내 모델의 무선랜(WLAN) 드라이버를 받아 USB로 옮겨 먼저 설치하세요.'),
          ('파일은 어디서 받아지나요?', '모든 버튼은 제조사 공식 서버나 Microsoft Store로 연결돼요. 홍라이프 도구는 파일을 올리지 않아요.')]
    fq, fqld = cu.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>{E(c["name"])}({E(c["en"])}) 드라이버 다운로드·설치 방법 — {E(c["lines"].replace("·", ", "))}</h1>'
            f'<p class="lead">{E(c["name"])} 노트북·PC 드라이버를 공식 프로그램으로 한 번에 업데이트하거나, 공식 사이트에서 모델별로 받는 방법을 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{c["ans"]}</p>'
            + (kr.dl(first[2], first[3], first[4]) if first else kr.dl(su, st, ss))
            + '<ul class="dr-toc"><li><a href="#tools">공식 프로그램</a></li><li><a href="#steps">설치 순서</a></li><li><a href="#model">모델 찾기</a></li><li><a href="#easy">처음이세요?</a></li></ul></header>'
            + (f'<section class="card dr-sec" id="tools"><h2>공식 업데이트 프로그램 바로 받기</h2><ul class="hpl">{tools}</ul></section>' if tools else '')
            + f'<section class="card dr-sec" id="steps"><h2>설치 순서 (아주 쉽게)</h2>{steps}' + kr.dl(su, st, ss, True) + '</section>'
            + f'<section class="card dr-sec" id="model"><h2>내 제품 모델·시리얼 번호 찾기</h2><ul class="cu-chk"><li>{c["serial"]}</li>'
              '<li>윈도우에서는 <b>설정 → 시스템 → 정보</b>에서 장치 이름을 볼 수 있어요.</li>'
              '<li>공식 사이트에 <b>시리얼 번호</b>를 넣으면 내 제품에 맞는 드라이버만 나와서 가장 정확해요.</li></ul></section>'
            + kr.guide_sec(c['name'], True) + kr.WIN_SEC + fq
            + kr.src_sec(c['src'] + ', Microsoft 지원 \'최신 프린터 드라이버 다운로드 및 설치\'') + kr.REL)
    ld = [crld, fqld]
    kr.write(path, f'{c["name"]} 드라이버 다운로드 — {c["lines"]} 드라이버 설치 방법 (공식 프로그램) | 홍라이프 도구',
             f'{c["name"]}({c["en"]}) 노트북·PC 드라이버를 공식 프로그램으로 한 번에 업데이트하거나 공식 사이트에서 시리얼 번호로 받는 방법. {c["lines"]} 드라이버 설치 순서를 쉽게 정리했어요.',
             main, ld)
    return path


def page_en(k):
    c = C[k]
    path = f'/en/driver/{k}.html'
    cr, crld = en.crumb([(c['en'], '')])
    su, st, ss = c['site']
    tools = ''.join(f'<li class="hpm"><h3>{E(t.split(" (")[0])}</h3><div class="bt">{en.dl(u.replace("hl=ko-kr&gl=KR", "hl=en-us&gl=US"), "Download", "Official", i > 0)}</div></li>'
                    for i, (t, d, u, bt, bs, _) in enumerate(c['tools']))
    qa = [('Where do files come from?', f'From {c["en"]}\'s official servers or the Microsoft Store. HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>{E(c["en"])} Driver Download — Official Update Tools</h1>'
            f'<p class="lead">Update {E(c["en"])} laptop and PC drivers with the official tool, or find drivers by serial number on the official support site.</p></header>'
            + (f'<section class="card dr-sec"><h2>Official tools</h2><ul class="hpl">{tools}</ul></section>' if tools else '')
            + f'<section class="card dr-sec"><h2>Drivers by model</h2>{en.dl(su.replace("/kr-ko", "/en-us").replace("/ko-kr", "/en-us").replace("/kr/ko/", "/us/en/").replace("/kr/support", "/us/support"), c["en"] + " support", "Search by serial number or model")}</section>'
            + en.easy(c['en'], True) + en.WIN + fq + en.src(c['src']) + en.REL)
    en.write(path, f'{c["en"]} Driver Download — Official Update Tools | HongLife Tools',
             f'Update {c["en"]} drivers with the official tool or download by serial number from the official support site, with easy steps.', main, [crld, fqld])
    return path


if __name__ == '__main__':
    for k in C:
        print(page(k), page_en(k))
