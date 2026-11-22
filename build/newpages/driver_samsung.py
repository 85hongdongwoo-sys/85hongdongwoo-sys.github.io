"""삼성 드라이버 페이지 — /driver/samsung.html, /en/driver/samsung.html
2026-11-23 공식 페이지에서 확인한 내용만 씀:
- 삼성전자서비스 solution/3470373 '디바이스 케어에서 장치 드라이버 업데이트': 윈도우 11·윈도우 10 22H2 갤럭시 북은 디바이스 케어,
  작업표시줄 검색 '디바이스 케어' → 없으면 Microsoft Store 설치 → 왼쪽 [업데이트] → 오른쪽 위 [업데이트 확인] → [모두 업데이트] → 재시작 [네].
  갤럭시 북2 이후는 갤럭시 북 다운로드 센터(samsung.com/global/galaxybooks-downloadcenter/?siteCode=sec)에서 윈도우 11 드라이버·매뉴얼 수동 다운로드.
- solution/441879 '노트북 장치 드라이버 설치 및 업데이트': 그 전 윈도우 10은 Samsung Update → [드라이버] → [설치]/[모두 업데이트], 소프트웨어는 [삼성 앱스].
  전원 어댑터 연결, 배터리 30% 이하면 진행 안 됨, BIOS 업데이트 중 전원 강제 종료 금지. 일부 모델(SM-W737, SM-W767, DM530ABE 등)은 Windows 업데이트로만.
  모델명: 노트북 바닥 레이저 각인, 또는 켤 때 삼성 로고 전 F6 약 5번 → Model Name(2016년 이후 제품). 윈도우 7은 다운로드 자료실에서 모델명 검색.
- Microsoft Store 9NQ3HDB99VBF 'Samsung Update': 윈도우 11 25H2 이상은 지원 안 함 → 디바이스 케어.
- solution/24689: 삼성 모니터 응용프로그램(Easy Setting Box)은 다운로드 자료실 → 모델명 → [응용프로그램]. 윈도우 7~11, macOS 12 이상.
- developer.samsung.com/android-usb-driver: Samsung Android USB Driver 1.9.5.0, 2026-05-06, 35.5MB, 윈도우용(개발용).
- semiconductor.samsung.com Magician: 최신 9.0, 윈도우 10(32·64비트)·macOS 10.15·안드로이드 7.0 이상, 윈도우 8.1 이하는 7.3, 다운로드는 지원 도구 페이지.
- solution/25294: 삼성 레이저 프린터·복합기는 다운로드 자료실 → PC/프린터 → '프린터 S/W 설치 프로그램'. samsung.com: 삼성 프린터 지원은 HP가 맡음.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en

E = cu.E
SVC = 'https://www.samsungsvc.co.kr/download'
GB = 'https://www.samsung.com/global/galaxybooks-downloadcenter/?siteCode=sec'
SU = 'https://apps.microsoft.com/detail/9nq3hdb99vbf?hl=ko-kr&gl=KR'
DC = 'https://apps.microsoft.com/search?query=Samsung%20Device%20Care&hl=ko-kr&gl=KR'
USB_PAGE = 'https://developer.samsung.com/android-usb-driver'
USB_FILE = 'https://developer.samsung.com/SDP/file/a2fcaf64-7aa3-49f7-b06f-9e646590d528'
MAG = 'https://semiconductor.samsung.com/consumer-storage/support/tools/'

ANS = ('삼성 노트북(갤럭시 북)은 윈도우 11이면 <b>디바이스 케어(Device Care)</b> 앱의 <b>[업데이트] → [업데이트 확인] → [모두 업데이트]</b>로 드라이버를 한 번에 설치해요. '
       '예전 윈도우 10 노트북은 <b>Samsung Update</b> 앱을 써요. 모니터·프린터·옛날 모델은 <b>삼성전자서비스 다운로드 자료실</b>에서 모델명으로 찾아 받아요.')


def page():
    path = '/driver/samsung.html'
    cr, crld = kr.crumb([('삼성 드라이버', '')])

    def item(h, d, btns):
        return f'<li class="hpm"><h3>{h}</h3><p class="fi">{d}</p><div class="bt">{"".join(btns)}</div></li>'

    pc = ('<ul class="hpl">'
          + item('윈도우 11 갤럭시 북 → 디바이스 케어 (추천)',
                 '윈도우 11이나 윈도우 10 22H2 갤럭시 북은 <b>디바이스 케어</b>로 드라이버를 업데이트해요. 작업표시줄 검색에 <b>디바이스 케어</b>를 쳐서 열고, 없으면 Microsoft Store에서 설치해요.',
                 [kr.dl(DC, 'Microsoft Store에서 디바이스 케어 찾기', '삼성 공식 앱 · 무료')])
          + item('예전 윈도우 10 노트북 → Samsung Update',
                 '디바이스 케어 이전 노트북은 <b>Samsung Update</b> 앱으로 드라이버·BIOS·삼성 앱을 받아요. 윈도우 11 25H2 이상에서는 Samsung Update가 지원되지 않아요(디바이스 케어를 쓰세요).',
                 [kr.dl(SU, 'Samsung Update 받기', 'Microsoft Store · 삼성 공식', True)])
          + item('갤럭시 북2 이후 → 갤럭시 북 다운로드 센터',
                 '앱 없이 파일로 받고 싶으면 갤럭시 북 다운로드 센터에서 모델 번호를 검색해 <b>윈도우 11 드라이버·매뉴얼</b>을 직접 받아요(갤럭시 북2 시리즈부터).',
                 [kr.dl(GB, '갤럭시 북 다운로드 센터', 'samsung.com · 모델 번호로 찾기', True)])
          + item('윈도우 7·8 옛날 노트북 → 다운로드 자료실',
                 '삼성전자서비스 <b>다운로드 자료실</b>에서 모델명을 검색해 드라이버를 하나씩 받아요. 윈도우 8·8.1용 Samsung Update 프로그램도 [유용한 소프트웨어 → PC/프린터]에 있어요.',
                 [kr.dl(SVC, '삼성전자서비스 다운로드 자료실', '모델명으로 찾기', True)])
          + '</ul>')

    steps = ('<ol class="big-n"><li>노트북에 <b>충전기를 꽂아요</b>. 배터리가 <b>30% 이하</b>면 업데이트가 진행되지 않아요.</li>'
             '<li>작업표시줄 검색에 <b>디바이스 케어</b>를 쳐서 열어요(없으면 위 버튼으로 Microsoft Store에서 설치).</li>'
             '<li>왼쪽 메뉴에서 <b>[업데이트]</b>를 누르고, 오른쪽 위 <b>[업데이트 확인]</b>을 눌러요.</li>'
             '<li>설치할 수 있는 드라이버 목록이 나오면 오른쪽 위 <b>[모두 업데이트]</b>를 눌러요.</li>'
             '<li>"PC를 다시 시작할까요?"가 나오면 <b>[네]</b>를 눌러 다시 시작해요. BIOS 업데이트 중에는 <b>절대 전원을 끄지 마세요</b>.</li></ol>'
             '<p class="cu-src">Samsung Update를 쓰는 노트북: 앱을 열고 <b>[드라이버]</b> → 설치 가능 항목의 <b>[설치]</b> 또는 오른쪽 위 <b>[모두 업데이트]</b>. 삼성 소프트웨어는 왼쪽 위 <b>[삼성 앱스]</b>에서 받아요.</p>')

    other = ('<ul class="hpl">'
             + item('삼성 모니터',
                    '모니터는 연결하면 윈도우가 대부분 알아서 인식해요. 화면 나누기 프로그램 <b>Easy Setting Box</b> 같은 모니터 프로그램은 다운로드 자료실에서 <b>모델명 검색 → [응용프로그램]</b>에서 내 운영체제용을 받아요(윈도우 7~11, macOS 12 이상). 지원하지 않는 모델은 목록에 안 나와요.',
                    [kr.dl(SVC, '다운로드 자료실에서 모니터 모델 찾기', '삼성전자서비스 공식')])
             + item('갤럭시 휴대폰 USB 드라이버 (윈도우)',
                    '갤럭시 휴대폰·태블릿을 윈도우 PC에 USB로 연결해 개발(안드로이드 스튜디오 등)할 때 필요한 삼성 공식 드라이버예요. 버전 1.9.5.0 · 35.5MB · 2026-05-06. 사진 옮기기만 할 때는 보통 필요 없어요.',
                    [kr.dl(USB_FILE, 'USB 드라이버 바로 받기', '삼성 개발자 사이트 서버 · 윈도우'), kr.dl(USB_PAGE, '삼성 개발자 안내 페이지', 'developer.samsung.com', True)])
             + item('삼성 SSD → Samsung Magician',
                    '삼성 SSD의 <b>펌웨어 업데이트</b>, 상태 확인, 정품 인증을 하는 공식 프로그램이에요. 최신 Magician 9.0은 윈도우 10(32·64비트), macOS 10.15, 안드로이드 7.0 이상을 지원하고, 윈도우 8.1 이하는 Magician 7.3을 써요. 맥·안드로이드에서는 내장 SSD를 지원하지 않아요.',
                    [kr.dl(MAG, 'Samsung Magician 받기 (공식 지원 도구)', 'semiconductor.samsung.com', True)])
             + item('삼성 프린터·복합기',
                    '삼성 레이저 프린터·복합기는 다운로드 자료실 <b>[PC/프린터] → 프린터 S/W 설치 프로그램</b>으로 드라이버를 깔아요. 삼성은 이제 프린터를 만들지 않고, <b>삼성 프린터 지원은 HP</b>가 맡고 있어요.',
                    [kr.dl(SVC, '다운로드 자료실 (프린터 S/W 설치 프로그램)', '삼성전자서비스 공식'), kr.dl('/driver/hp.html', 'HP에서 삼성 프린터 드라이버 받기', '홍라이프 HP 드라이버 안내', True)])
             + '</ul>')

    qa = [('삼성 노트북 드라이버는 어디서 받아요?', '윈도우 11 갤럭시 북은 디바이스 케어 앱의 [업데이트] → [업데이트 확인] → [모두 업데이트]로 받아요. 예전 윈도우 10 노트북은 Samsung Update, 옛날 모델은 삼성전자서비스 다운로드 자료실에서 모델명으로 찾아요.'),
          ('Samsung Update가 안 돼요.', '윈도우 11 25H2 이상에서는 Samsung Update가 지원되지 않아요. 디바이스 케어를 쓰세요. 일부 모델(SM-W737, SM-W767, DM530ABE 등)은 Windows 업데이트로만 드라이버를 받아요.'),
          ('내 노트북 모델명을 모르겠어요.', '노트북 바닥에 새겨진 모델명을 보세요. 2016년 이후 제품은 켜자마자 삼성 로고가 나오기 전에 F6 키를 5번쯤 누르면 Model Name이 보여요.'),
          ('업데이트가 진행되지 않아요.', '충전기를 꽂았는지, 배터리가 30%보다 많은지 확인하세요. 배터리 30% 이하에서는 진행되지 않아요.'),
          ('삼성 프린터 드라이버는요?', '삼성전자서비스 다운로드 자료실의 프린터 S/W 설치 프로그램으로 설치하거나, 지원을 맡은 HP 사이트에서 모델명(SL-로 시작)으로 찾으세요.'),
          ('파일은 어디서 받아지나요?', '모든 버튼은 삼성 공식 사이트·서버나 Microsoft Store로 연결돼요. 홍라이프 도구는 파일을 올리지 않아요.')]
    fq, fqld = cu.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>삼성 드라이버 다운로드·설치 방법 — 갤럭시 북 노트북, 모니터, 갤럭시 USB, SSD, 프린터</h1>'
            '<p class="lead">삼성 노트북(갤럭시 북)·모니터·갤럭시 휴대폰 USB·SSD·프린터 드라이버를 삼성 공식 앱과 공식 사이트에서 받는 방법을 아주 쉽게 정리했어요.</p>'
            f'<p class="cu-ans">{ANS}</p>' + kr.dl(DC, '디바이스 케어 찾기 (윈도우 11 갤럭시 북)', 'Microsoft Store · 삼성 공식 · 무료')
            + '<ul class="dr-toc"><li><a href="#pc">노트북</a></li><li><a href="#steps">업데이트 순서</a></li><li><a href="#other">모니터·USB·SSD·프린터</a></li><li><a href="#model">모델명 찾기</a></li></ul></header>'
            f'<section class="card dr-sec" id="pc"><h2>삼성 노트북(갤럭시 북) — 내 윈도우에 맞는 방법 고르기</h2>{pc}</section>'
            f'<section class="card dr-sec" id="steps"><h2>디바이스 케어로 드라이버 업데이트 (아주 쉽게)</h2>{steps}</section>'
            f'<section class="card dr-sec" id="other"><h2>모니터·갤럭시 USB·SSD·프린터</h2>{other}</section>'
            '<section class="card dr-sec" id="model"><h2>내 제품 모델명 찾기</h2><ul class="cu-chk">'
            '<li>노트북 <b>바닥면</b>에 새겨진(레이저 각인) 모델명을 봐요.</li>'
            '<li>2016년 이후 노트북은 전원을 켜고 <b>삼성 로고가 나오기 전에 F6 키를 5번쯤</b> 누르면 제품 정보의 <b>Model Name</b>이 보여요.</li>'
            '<li>모니터는 <b>뒷면 스티커</b>에서 모델명을 봐요.</li></ul></section>'
            + kr.guide_pc('삼성') + kr.WIN_PC + fq
            + kr.src_sec('삼성전자서비스 \'디바이스 케어에서 장치 드라이버 업데이트하기\', \'노트북 장치 드라이버 설치 및 업데이트 방법\', \'Easy Settings Box 사용\', \'삼성 SW 설치 프로그램 설치하는 방법\', Microsoft Store \'Samsung Update\', 삼성 개발자 \'Android USB Driver\', 삼성 반도체 \'Samsung Magician\', 삼성전자 \'삼성 프린터 지원은 HP\' 안내') + kr.REL)
    kr.write(path, '삼성 드라이버 다운로드 — 갤럭시 북 노트북·모니터·USB·SSD·프린터 설치 방법 (디바이스 케어·Samsung Update) | 홍라이프 도구',
             '삼성 노트북(갤럭시 북) 드라이버는 디바이스 케어나 Samsung Update로, 모니터·프린터는 삼성전자서비스 다운로드 자료실에서 받아요. 갤럭시 USB 드라이버, SSD Magician까지 공식 링크와 쉬운 설치 순서.',
             main, [crld, fqld, kr.howto('삼성 노트북 드라이버 업데이트 (디바이스 케어)', ['충전기 연결', '디바이스 케어 열기', '업데이트 → 업데이트 확인', '모두 업데이트', '다시 시작'])])
    return path


def page_en():
    path = '/en/driver/samsung.html'
    cr, crld = en.crumb([('Samsung', '')])
    li = lambda h, d, b: f'<li class="hpm"><h3>{h}</h3><p class="fi">{d}</p><div class="bt">{b}</div></li>'
    body = ('<ul class="hpl">'
            + li('Galaxy Book (Windows 11) — Samsung Device Care', 'Open Device Care → Update → Check for updates → Update all, then restart. Plug in the charger; updates stop at 30% battery or less.',
                 en.dl(DC.replace('hl=ko-kr&gl=KR', 'hl=en-us&gl=US'), 'Find Device Care', 'Microsoft Store'))
            + li('Older Windows 10 laptops — Samsung Update', 'Drivers → Install or Update all. Not supported on Windows 11 25H2 or later.', en.dl(SU.replace('hl=ko-kr&gl=KR', 'hl=en-us&gl=US'), 'Samsung Update', 'Microsoft Store', True))
            + li('Galaxy Book2 and later — Download Center', 'Search your model number for Windows 11 drivers and manuals.', en.dl(GB.replace('siteCode=sec', 'siteCode=us'), 'Galaxy Book Download Center', 'samsung.com', True))
            + li('Galaxy phone USB driver (Windows)', 'Version 1.9.5.0, 35.5 MB, for development over USB.', en.dl(USB_PAGE, 'Samsung Android USB Driver', 'developer.samsung.com', True))
            + li('Samsung SSD — Magician', 'Firmware updates and drive health. Magician 9.0 supports Windows 10, macOS 10.15 and Android 7.0+.', en.dl(MAG, 'Samsung Magician', 'semiconductor.samsung.com', True))
            + li('Samsung printers', 'Samsung printer support is now handled by HP.', en.dl('/en/driver/hp.html', 'HP / Samsung printer drivers', 'HongLife guide', True))
            + '</ul>')
    qa = [('Where do files come from?', 'From Samsung\'s official sites and servers or the Microsoft Store. HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>Samsung Driver Download — Galaxy Book, USB, SSD, Printer</h1>'
            '<p class="lead">Official ways to update Samsung laptop drivers and get Samsung USB, SSD and printer software.</p></header>'
            f'<section class="card dr-sec"><h2>Pick your product</h2>{body}</section>' + en.easy_pc('Samsung') + en.WIN_PC + fq
            + en.src('Samsung Electronics Service, Microsoft Store "Samsung Update", Samsung Developer "Android USB Driver", Samsung Semiconductor "Magician", Samsung "printer support by HP"') + en.REL)
    en.write(path, 'Samsung Driver Download — Galaxy Book, USB, SSD, Printer | HongLife Tools',
             'Update Samsung Galaxy Book drivers with Device Care or Samsung Update, and get Samsung USB driver, Magician and printer support from official sources.', main, [crld, fqld])
    return path


if __name__ == '__main__':
    print(page(), page_en())
