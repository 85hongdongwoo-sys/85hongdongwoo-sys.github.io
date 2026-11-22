"""애플 드라이버·프로그램 페이지 (한국어 /driver/apple.html, 영어 /en/driver/apple.html)
2026-11-22 공식 안내로 확인:
- Apple 지원 'Windows용 Apple 기기 앱 설치'(Microsoft Store에서 Apple 기기 검색 → 받기, Apple Music·Apple TV 앱 있어야 음악·영상 동기화)
- Apple 지원 103232 'Windows용 iCloud 다운로드'(Microsoft Store 9PKTQ5699M62, Windows 11 이상 권장)
- Apple 지원 102465 'Mac에 Windows 지원 소프트웨어 다운로드 및 설치'(Boot Camp, 16GB USB, Boot Camp 지원 앱 → 동작 메뉴)
- Apple 지원 '컴퓨터가 iPhone 또는 iPad를 인식하지 못하는 경우'
- Microsoft Store 앱 페이지: Apple 기기 9NP83LWLPZ9K, iCloud 9PKTQ5699M62, iTunes 9PB2MZ1ZMB1S, Apple Music 9PFHDD62MXS1, Apple TV 9NM4T8B9JQZ1
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en

E = cu.E
MS = 'https://apps.microsoft.com/detail/{}?hl=ko-kr&gl=KR'
DEV, ICL, ITU, MUS, ATV = (MS.format(x) for x in ('9NP83LWLPZ9K', '9PKTQ5699M62', '9PB2MZ1ZMB1S', '9PFHDD62MXS1', '9NM4T8B9JQZ1'))
G_DEV = 'https://support.apple.com/ko-kr/guide/devices-windows/mchl5ded2763/windows'
G_ICL = 'https://support.apple.com/ko-kr/103232'
G_BC = 'https://support.apple.com/ko-kr/102465'
G_BCREQ = 'https://support.apple.com/ko-kr/102622'
G_REC = 'https://support.apple.com/ko-kr/TS1538'


def apple():
    path = '/driver/apple.html'
    cr, crld = kr.crumb([('애플 드라이버·프로그램', '')])
    ans = ('윈도우 PC에서 <b>아이폰·아이패드</b>를 연결하려면 <b>Apple 기기</b> 앱(Microsoft Store, 무료)을 설치하면 돼요. 아이폰을 연결하는 드라이버도 이 앱과 함께 들어가요. '
           '사진·파일을 PC와 맞추려면 <b>Windows용 iCloud</b>, <b>인텔 맥에 윈도우를 깔았다면</b> Boot Camp 지원 소프트웨어(Windows 지원 소프트웨어)를 받아요.')
    apps = ('<ul class="hpl">'
            f'<li class="hpm" id="devices"><h3>Apple 기기 (Apple Devices)</h3><p class="fi">윈도우 PC에서 아이폰·아이패드를 <b>백업·업데이트·복원</b>하고 음악·영상을 동기화하는 Apple 공식 앱이에요.</p>'
            f'<div class="bt">{kr.dl(DEV, "Apple 기기 앱 받기", "Microsoft Store (Apple 공식, 무료)")}</div>'
            f'<p class="ex"><a class="sm" href="{MUS}" target="_blank" rel="noopener nofollow">Apple Music 앱</a><a class="sm" href="{ATV}" target="_blank" rel="noopener nofollow">Apple TV 앱</a>'
            f'<a class="sm" href="{G_DEV}" target="_blank" rel="noopener nofollow">Apple 설치 안내 ↗</a></p></li>'
            f'<li class="hpm" id="icloud"><h3>Windows용 iCloud</h3><p class="fi">아이폰 사진·파일·암호·캘린더를 윈도우 PC와 맞춰 줘요. Apple은 <b>윈도우 11 이상</b>(메일·캘린더는 Outlook 2021 이상)을 안내해요.</p>'
            f'<div class="bt">{kr.dl(ICL, "iCloud 받기", "Microsoft Store (Apple 공식, 무료)")}</div><p class="ex"><a class="sm" href="{G_ICL}" target="_blank" rel="noopener nofollow">Apple 안내 ↗</a></p></li>'
            f'<li class="hpm" id="itunes"><h3>iTunes (윈도우)</h3><p class="fi">예전 방식이 필요할 때 쓰는 앱이에요. 새로 시작한다면 위 Apple 기기 앱을 쓰세요.</p>'
            f'<div class="bt">{kr.dl(ITU, "iTunes 받기", "Microsoft Store (Apple, 무료)", True)}</div></li>'
            f'<li class="hpm" id="bootcamp"><h3>Boot Camp 지원 소프트웨어 (인텔 맥에 윈도우를 깐 경우)</h3><p class="fi">맥에 윈도우를 설치한 뒤 <b>와이파이·블루투스가 안 되거나, 스피커 소리가 안 나거나, 검은·파란 화면</b>이 뜨면 필요해요. 파일은 웹 버튼이 아니라 맥의 <b>Boot Camp 지원 앱</b>에서 받아요(아래 순서).</p>'
            f'<div class="bt">{kr.dl(G_BC, "Boot Camp 지원 소프트웨어 안내", "Apple 공식 (받는 방법)", True)}</div><p class="ex"><a class="sm" href="{G_BCREQ}" target="_blank" rel="noopener nofollow">지원되는 맥·윈도우 확인 ↗</a></p></li>'
            '</ul>')
    steps_dev = (cu.step(1, 'Microsoft Store에서 받기', '위 <b>[Apple 기기 앱 받기]</b>를 누르면 Microsoft Store 페이지가 열려요. <b>[받기]</b>(또는 [Store 앱에서 받기])를 눌러 설치해요.',
                         kr.W_list('apps.microsoft.com', 'Apple 기기 · Apple Inc.', [('무료', ''), ('', ''), ('받기', '받기')], 2, 1))
                 + cu.step(2, '아이폰을 USB로 연결', 'Apple 기기 앱을 열고 아이폰을 USB 케이블로 PC에 연결해요.',
                           kr.W_installer('Apple 기기', ['아이폰을 연결하세요', '(USB 케이블)', ''], '확인', 2))
                 + cu.step(3, '아이폰에서 \'신뢰\' 누르기', '아이폰 화면에 <b>\'이 컴퓨터를 신뢰하겠습니까?\'</b>가 뜨면 <b>[신뢰]</b>를 누르고 암호를 넣어요. 그러면 앱 왼쪽 목록에 내 아이폰이 나타나요.',
                           kr.W_list('iPhone', '이 컴퓨터를 신뢰하겠습니까?', [('설정과 데이터에 접근할 수 있어요', ''), ('', ''), ('신뢰', '신뢰')], 2, 3)))
    bc = ('<ol class="big-n"><li><b>16GB 이상 USB 메모리</b>를 맥에 꽂고, <b>디스크 유틸리티</b>로 <b>MS-DOS(FAT)</b>, <b>마스터 부트 레코드</b> 방식으로 포맷해요.</li>'
          '<li>인터넷에 연결하고 <b>응용 프로그램 → 유틸리티 → Boot Camp 지원</b> 앱을 열어요.</li>'
          '<li>메뉴 막대의 <b>동작 → Windows 지원 소프트웨어 다운로드</b>를 고르고, 저장 위치로 그 USB를 골라요. 다 받으면 Boot Camp 지원 앱을 닫아요.</li>'
          '<li>USB를 꽂은 채로 맥을 <b>윈도우로 시작</b>해요.</li>'
          '<li>파일 탐색기에서 USB → <b>WindowsSupport</b> 또는 <b>BootCamp</b> 폴더의 <b>Setup(setup.exe)</b>을 열고, 변경 허용 창에서 <b>[예]</b>를 눌러요.</li>'
          '<li><b>[복구]</b>를 눌러 설치를 시작해요. \'Windows 로고 테스트를 통과하지 않았다\'는 경고가 나오면 <b>[계속]</b>을 눌러요.</li>'
          '<li><b>[완료]</b>를 누르고, 다시 시작하라고 하면 맥을 다시 시작해요.</li></ol>'
          '<p class="cu-src">출처: Apple 지원 \'Mac에 Windows 지원 소프트웨어 다운로드 및 설치\'. 지원되는 맥 모델과 윈도우 버전은 Apple의 시스템 요구 사항 문서에서 확인하세요.</p>')
    rec = ('<ul class="cu-chk"><li>먼저 <b>Apple 기기 앱</b>을 연 다음 아이폰을 연결하고, 아이폰의 <b>\'신뢰\'</b>를 눌렀는지 확인해요.</li>'
           '<li>충전만 되는 케이블일 수 있어요. <b>데이터 전송이 되는 다른 케이블</b>로 바꿔 보세요. 아이폰 충전 단자에 먼지가 없는지도 봐요.</li>'
           '<li><b>다른 USB 포트</b>나 다른 PC에 꽂아 봐요.</li>'
           '<li><b>윈도우 업데이트</b>와 <b>아이폰 iOS 업데이트</b>를 최신으로 해요.</li>'
           '<li>그래도 안 되면 Apple 지원에 문의하세요.</li></ul>'
           f'<p class="cu-src">출처: Apple 지원 \'컴퓨터가 iPhone 또는 iPad를 인식하지 못하는 경우\'.</p>' + kr.dl(G_REC, 'Apple 안내 원문 보기', 'support.apple.com', True))
    qa = [('아이폰 드라이버는 따로 받아야 하나요?', '아니요. 윈도우 PC는 Apple 기기 앱을 설치하면 아이폰 연결에 필요한 것이 함께 설치돼요. 따로 \'아이폰 드라이버\'를 주는 사이트는 조심하세요.'),
          ('iTunes와 Apple 기기 앱 중 뭘 써요?', '새로 시작한다면 Apple 기기 앱을 쓰세요. 음악·영상 동기화에는 Apple Music, Apple TV 앱도 설치돼 있어야 해요(Apple 안내).'),
          ('맥(Mac)은 드라이버를 어디서 받아요?', '맥은 macOS 업데이트(시스템 설정 → 일반 → 소프트웨어 업데이트)로 드라이버가 함께 업데이트돼요. 프린터 등 다른 회사 기기는 이 사이트의 각 회사 페이지를 보세요.'),
          ('Apple 실리콘(M1·M2…) 맥에서도 Boot Camp를 쓸 수 있나요?', 'Boot Camp 지원은 인텔 프로세서 맥용이에요. 지원 여부는 Apple의 Boot Camp 시스템 요구 사항 문서에서 내 맥 모델을 확인하세요.'),
          ('모두 무료인가요?', '네. Apple 기기, iCloud, iTunes, Boot Camp 지원 소프트웨어 모두 무료예요.')]
    fq, fqld = cu.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>애플 드라이버·프로그램 다운로드 — 윈도우에서 아이폰 연결(Apple 기기 앱)·iCloud·Boot Camp</h1>'
            '<p class="lead">윈도우 PC에 아이폰·아이패드를 연결하는 Apple 기기 앱, Windows용 iCloud, iTunes, 인텔 맥의 Boot Camp 지원 소프트웨어를 Apple 공식 경로로 받고 쉽게 설치하는 방법이에요.</p>'
            f'<p class="cu-ans">{ans}</p>' + kr.dl(DEV, 'Apple 기기 앱 바로 받기', 'Microsoft Store · Apple 공식 · 무료')
            + '<ul class="dr-toc"><li><a href="#apps">프로그램 받기</a></li><li><a href="#steps">아이폰 연결 순서</a></li><li><a href="#bc">Boot Camp</a></li><li><a href="#rec">인식이 안 될 때</a></li></ul></header>'
            f'<section class="card dr-sec" id="apps"><h2>프로그램 바로 받기</h2>{apps}</section>'
            f'<section class="card dr-sec" id="steps"><h2>그림으로 보는 아이폰 연결 순서 (윈도우)</h2>{steps_dev}</section>'
            f'<section class="card dr-sec" id="bc"><h2>Boot Camp 지원 소프트웨어 받고 설치하기 (인텔 맥)</h2>{bc}</section>'
            f'<section class="card dr-sec" id="rec"><h2>PC가 아이폰을 못 알아볼 때</h2>{rec}</section>'
            + kr.WIN_SEC.replace('id="win"', 'id="win2"') + fq
            + kr.src_sec('Apple 지원(support.apple.com/ko-kr) \'Windows용 Apple 기기 앱 설치\', \'Windows용 iCloud 다운로드\', \'Mac에 Windows 지원 소프트웨어 다운로드 및 설치\', \'컴퓨터가 iPhone을 인식하지 못하는 경우\', Microsoft Store 앱 페이지')
            + kr.REL)
    ld = [crld, fqld, kr.howto('윈도우 PC에 아이폰 연결하는 방법 (Apple 기기 앱)', ['Microsoft Store에서 Apple 기기 앱 받기', 'Apple 기기 앱을 열고 아이폰을 USB로 연결', '아이폰에서 신뢰 누르기'])]
    kr.write(path, '애플 드라이버 다운로드 — 아이폰 PC 연결(Apple 기기 앱)·iCloud·iTunes·Boot Camp 설치 방법 | 홍라이프 도구',
             '윈도우 PC가 아이폰을 인식하지 못할 때, Apple 기기 앱·Windows용 iCloud·iTunes를 Apple 공식 경로로 받고, 인텔 맥의 Boot Camp 지원 소프트웨어(Windows 지원 소프트웨어)를 설치하는 방법을 쉽게 정리했어요.',
             main, ld)
    return path


def apple_en():
    path = '/en/driver/apple.html'
    cr, crld = en.crumb([('Apple', '')])
    msE = lambda x: x.replace('hl=ko-kr&gl=KR', 'hl=en-us&gl=US')
    body = ('<ul class="hpl">'
            f'<li class="hpm"><h3>Apple Devices (Windows)</h3><p class="fi">Back up, update, restore and sync iPhone/iPad on a Windows PC.</p><div class="bt">{en.dl(msE(DEV), "Get Apple Devices", "Microsoft Store · free")}</div></li>'
            f'<li class="hpm"><h3>iCloud for Windows</h3><p class="fi">Apple recommends Windows 11 or later.</p><div class="bt">{en.dl(msE(ICL), "Get iCloud", "Microsoft Store · free")}</div></li>'
            f'<li class="hpm"><h3>iTunes for Windows</h3><div class="bt">{en.dl(msE(ITU), "Get iTunes", "Microsoft Store · free", True)}</div></li>'
            f'<li class="hpm"><h3>Boot Camp support software (Intel Mac)</h3><p class="fi">Download it inside Boot Camp Assistant: Action → Download Windows Support Software, to a 16GB+ USB drive (MS-DOS FAT, Master Boot Record). In Windows, run Setup in the WindowsSupport/BootCamp folder and click Repair.</p>'
            f'<div class="bt">{en.dl(G_BC.replace("ko-kr", "en-us"), "Apple guide", "support.apple.com", True)}</div></li></ul>')
    qa = [('Do I need a separate iPhone driver?', 'No. Installing Apple Devices from the Microsoft Store sets up what Windows needs to connect your iPhone.'),
          ('PC does not recognise my iPhone?', 'Open Apple Devices first, connect, tap Trust on the iPhone, try another data cable or USB port, and update Windows and iOS (Apple guidance).')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>Apple Drivers &amp; Apps — Apple Devices, iCloud, iTunes, Boot Camp</h1>'
            '<p class="lead">Connect iPhone/iPad to Windows and get Boot Camp support software, using Apple\'s official channels.</p></header>'
            f'<section class="card dr-sec"><h2>Downloads</h2>{body}</section>' + en.WIN + fq
            + en.src('Apple Support (support.apple.com), Microsoft Store app pages') + en.REL)
    en.write(path, 'Apple Drivers for Windows — Apple Devices, iCloud, iTunes, Boot Camp | HongLife Tools',
             'Get Apple Devices, iCloud for Windows and iTunes from the Microsoft Store, and Boot Camp support software for Intel Macs, with easy steps.', main, [crld, fqld])
    return path


if __name__ == '__main__':
    print(apple(), apple_en())
