"""드라이버 회사 14곳 추가 (2026-11-23) — 한국어 /driver/<k>.html, 영어 /en/driver/<k>.html
공식 안내에서 확인한 내용만 씀(2026-11-23 확인):
- MSI: MSI Center → Support → Live Update → Scan → 드라이버 선택 → Download (MSI 기술 문서 NB/DT_Driver_Update), kr.msi.com/support/download
- 기가바이트: GIGABYTE Control Center(GCC) 업데이트 센터 — 드라이버·유틸리티 업데이트를 클라우드에서 확인, Windows 10/11 64비트
- 애즈락: Auto Driver Installer(ADI) 2.0.0.9, Windows 10/11 64비트, 5.8MB — 바이오스에 LAN 드라이버가 들어 있어 첫 부팅 때 ADI가 뜸
- 한성컴퓨터: 고객센터 다운로드(superstore.co.kr), 제품명 검색, 인터넷 연결을 끊고 번호 순서대로 설치 권장, 데스크톱 메인보드는 보드 제조사
- 레이저: Razer Synapse 4(Windows 10/11 64비트), Synapse 3은 2026-02-03부터 업데이트·클라우드 서비스 종료
- 캐논: 캐논코리아 고객지원 다운로드(svc.kr.canon)
- 후지필름 BI: 옛 후지제록스(2021-04-01 사명 변경), 모델 검색, 여러 모델용 Multi-Model Print Driver(ARM 윈도우는 Multi-Model Print Driver 2)
- 교세라: KX Driver(여러 모델용, Windows 10/11)
- 리코: PCL6 Driver for Universal Print(support.ricoh.com)
- 로지텍: Logi Options+(일반 마우스·키보드), G HUB(Logitech G), 옛 Unifying·Firmware Update Tool 등은 지원 종료
- 와콤: 드라이버를 설치하면 Wacom Center가 함께 설치됨, 최신 제품은 Wacom Center에서만 설정, 옛 제품용 드라이버 목록 따로 있음
- 리얼텍: 메인보드·노트북 제조사 사이트 드라이버가 우선, 장치 관리자 이름 'Realtek PCIe GbE Family Controller'
- ipTIME: 다운로드 자료실(구분: 펌웨어·드라이버, 모델명 검색), 공유기 관리 화면 → 고급 설정 → 시스템 관리 → 펌웨어 업그레이드
- TP-Link: 다운로드 센터(tp-link.com/kr/support/download) → 모델 → 하드웨어 버전 선택
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en

E = cu.E
CHK = '2026년 11월 23일'
CHK_EN = 'November 23, 2026'

# kind: pc(노트북·PC), board(메인보드), printer, periph(주변기기), chip(칩 회사), net(네트워크)
C = {
    'msi': dict(
        name='MSI', en='MSI', kind='pc', lines='노트북·메인보드·그래픽카드·모니터',
        ans='MSI 노트북·데스크톱·메인보드는 <b>MSI Center</b>(무료)의 <b>Support → Live Update → Scan</b>으로 필요한 드라이버를 한 번에 찾아 받아요. 프로그램 없이 받으려면 아래 <b>[MSI Center 바로 받기]</b>로 설치 파일을 바로 받거나, <b>MSI 다운로드</b> 페이지에서 제품 모델을 골라 드라이버·BIOS·매뉴얼을 받아요.',
        tools=[('MSI Center', 'MSI 노트북·데스크톱용 MSI 공식 앱이에요. 앱을 열고 <b>Support(지원) → Live Update → Scan</b>을 누르면 업데이트할 드라이버 목록이 나와요. 고른 뒤 <b>Download</b>를 누르면 받아서 설치해요.',
                'https://www.msi.com/Landing/MSI-Center', 'MSI Center 받기', 'MSI 공식 페이지 · 무료')],
        site=('https://kr.msi.com/support/download', 'MSI 다운로드 (제품별 드라이버·BIOS)', '제품 종류 → 모델 선택'),
        site_en='https://www.msi.com/support/download',
        steps=['위 <b>[MSI Center 바로 받기]</b>로 파일을 받아 압축을 풀고 설치해요. (노트북에는 이미 깔려 있는 경우가 많아요.)',
               'MSI Center를 열고 <b>Support</b>(지원) → <b>Live Update</b>를 눌러요.',
               '<b>Scan</b>을 누르면 내 PC에 필요한 드라이버·BIOS 업데이트가 목록으로 나와요.',
               '받을 항목에 체크하고 <b>Download</b>를 누르면 받아서 설치해요. 끝나면 다시 시작해요.'],
        serial='제품 뒷면·바닥면 바코드 스티커의 <b>모델명</b>과 <b>S/N</b>을 보세요. 메인보드는 보드 위(보통 PCIe 슬롯 사이)에 모델명이 인쇄돼 있어요.',
        qa=[('MSI Dragon Center를 쓰고 있어요.', 'MSI Center가 이어받은 프로그램이에요. MSI 안내에서도 MSI Center·MSI Center Pro·Dragon Center 모두 Support → Live Update → Scan 순서로 드라이버를 받는다고 해요.')],
        src="MSI 기술 문서 '[Notebook] How to Update Drivers', '[Desktop] How to update the driver?', MSI 한국 지원 다운로드",
        kw='MSI 드라이버 엠에스아이 드라이버 MSI 노트북 드라이버 MSI 메인보드 드라이버 MSI Center Live Update 드래곤센터',
        sub='노트북·메인보드 MSI Center'),
    'gigabyte': dict(
        name='기가바이트', en='GIGABYTE', kind='board', lines='메인보드·그래픽카드·AORUS 노트북',
        ans='기가바이트 메인보드·노트북은 <b>GIGABYTE Control Center(GCC)</b>의 <b>업데이트 센터</b>가 클라우드에서 드라이버·유틸리티 업데이트를 확인해 설치해 줘요(Windows 10/11 64비트). 개별 파일은 <b>기가바이트 지원</b>에서 제품 모델을 찾아 <b>지원(Support)</b> 탭에서 받아요.',
        tools=[('GIGABYTE Control Center (GCC)', '기가바이트 공식 통합 프로그램이에요. <b>업데이트 센터</b>에서 드라이버와 유틸리티 업데이트를 확인하고 설치해요. Windows 10/11 64비트용이고, 전체 설치 파일이 1GB 가까이 돼서 받는 데 시간이 걸려요.',
                'https://www.gigabyte.com/kr/Support', '기가바이트 지원에서 GCC 받기', '기가바이트 공식 · 제품 지원 → 유틸리티')],
        site=('https://www.gigabyte.com/kr/Support', '기가바이트 지원 (제품별 드라이버)', '모델명 검색 → 지원 → 드라이버'),
        site_en='https://www.gigabyte.com/Support',
        steps=['메인보드 모델명과 <b>리비전</b>(예: rev. 1.0)을 확인해요. 같은 이름이라도 리비전마다 파일이 달라요.',
               '기가바이트 지원에서 모델명을 검색하고 제품의 <b>지원(Support)</b> 탭 → <b>드라이버</b>를 열어요.',
               '윈도우 버전을 고르고 <b>칩셋 → LAN → 오디오</b> 순서로 받아 설치해요.',
               '한 번에 하려면 같은 페이지 <b>유틸리티</b>에서 GCC를 받아 <b>업데이트 센터</b>로 설치해요.'],
        serial='메인보드 위에 인쇄된 모델명(예: B760M DS3H)과 <b>rev.</b> 표시를 보세요. 상자 옆면 스티커에도 있어요.',
        qa=[('리비전(rev.)이 뭐예요?', '같은 모델의 기판 판(버전)이에요. 기가바이트는 리비전별로 BIOS·드라이버를 나눠 올리니 꼭 맞춰 고르세요.')],
        src='기가바이트 공식 GIGABYTE Control Center 안내, 기가바이트 한국 지원 다운로드',
        kw='기가바이트 드라이버 GIGABYTE 드라이버 기가바이트 메인보드 드라이버 GCC GIGABYTE Control Center 어로스 드라이버 AORUS 드라이버',
        sub='메인보드·그래픽카드 GCC'),
    'asrock': dict(
        name='애즈락', en='ASRock', kind='board', lines='메인보드·그래픽카드',
        ans='애즈락 최신 메인보드는 <b>BIOS 안에 랜(LAN) 드라이버가 들어 있어서</b>, 윈도우를 처음 켜면 <b>Auto Driver Installer(ADI)</b>가 떠서 필요한 드라이버를 자동으로 받아 깔아 줘요. 창이 안 뜨면 애즈락 지원 → 유틸리티에서 ADI(Windows 10/11 64비트, 약 5.8MB)를 받아 실행하세요.',
        tools=[('Auto Driver Installer (ADI)', '애즈락 메인보드에 맞는 드라이버를 자동으로 찾아 설치해 주는 애즈락 공식 프로그램이에요. 버전 2.0.0.9, Windows 10/11 64비트, 약 5.8MB.',
                'https://www.asrock.com/support/index.asp?cat=Utilities', 'ADI 받기 (애즈락 유틸리티)', '애즈락 공식 · 무료')],
        site=('https://www.asrock.com/support/index.asp', '애즈락 지원 (메인보드별 드라이버)', '모델명 검색 → 다운로드'),
        site_en='https://www.asrock.com/support/index.asp',
        steps=['윈도우 설치가 끝나고 처음 켜면 <b>Auto Driver Installer</b> 창이 떠요. <b>[설치]</b>를 누르면 인터넷으로 드라이버를 받아요.',
               '창이 안 뜨면 위 버튼으로 ADI를 받아 실행해요.',
               '설치할 드라이버 목록이 나오면 전부 체크된 상태로 설치하고, 끝나면 다시 시작해요.',
               '개별로 받고 싶으면 애즈락 지원에서 모델명을 검색해 칩셋·LAN·오디오 드라이버를 받아요.'],
        serial='메인보드 위(보통 램 슬롯 근처나 아래쪽)에 인쇄된 모델명(예: B650M Pro RS)을 보세요.',
        qa=[('처음 켰는데 인터넷이 안 돼서 ADI가 동작하지 않아요.', 'BIOS의 LAN 드라이버 자동 설치 기능이 꺼져 있을 수 있어요. 다른 컴퓨터로 애즈락 지원에서 내 모델 LAN 드라이버를 받아 USB로 옮겨 먼저 설치하세요.')],
        src="애즈락 지원 유틸리티 'Auto Driver Installer', 애즈락 지원 다운로드",
        kw='애즈락 드라이버 ASRock 드라이버 애즈락 메인보드 드라이버 Auto Driver Installer ADI 애즈락 랜 드라이버',
        sub='메인보드 자동 설치(ADI)'),
    'hansung': dict(
        name='한성컴퓨터', en='Hansung Computer', kind='pc', lines='노트북·데스크톱·모니터',
        ans='한성컴퓨터 노트북 드라이버는 <b>한성 고객센터 → 다운로드</b>에서 <b>제품명</b>(노트북 바닥 스티커의 모델명)으로 검색해 받아요. 한성은 <b>인터넷 연결을 끊고, 파일 이름의 번호 순서대로</b> 설치하라고 안내해요. 조립 데스크톱은 <b>메인보드 회사</b> 사이트에서 받아요.',
        tools=[],
        site=('https://www.superstore.co.kr/customer_center/list.html?cc_menu=tbl_cc_download', '한성컴퓨터 다운로드 (고객센터)', '제품명으로 검색'),
        site_en='https://www.superstore.co.kr/customer_center/list.html?cc_menu=tbl_cc_download',
        steps=['노트북 바닥 스티커에서 <b>제품명(모델명)</b>을 확인해요.',
               '한성 고객센터 다운로드에서 제품명을 검색하고 윈도우 버전에 맞는 드라이버를 모두 받아요.',
               '<b>랜선을 뽑고 와이파이를 꺼서</b> 인터넷 연결을 끊어요. (윈도우가 다른 드라이버를 먼저 깔지 않게 하려는 거예요.)',
               '받은 파일을 <b>번호 순서대로</b>(보통 칩셋부터) 하나씩 설치하고, 다시 시작하라고 하면 다시 시작해요.',
               '다 끝나면 인터넷을 다시 연결하고 Windows 업데이트를 해요.'],
        serial='노트북 바닥면 스티커의 <b>제품명</b>과 <b>시리얼 번호</b>를 보세요. 데스크톱은 본체 옆면 스티커나 메인보드 모델명을 보세요.',
        qa=[('조립 PC(데스크톱)인데 한성 사이트에 드라이버가 없어요.', '데스크톱은 메인보드 제조사(에이수스·기가바이트·MSI·애즈락 등) 사이트에서 메인보드 모델로 받아요. 이 페이지 아래 \'다른 회사 드라이버\'에서 고르세요.'),
            ('A/S 문의는 어디로 하나요?', '한성컴퓨터 고객센터 02-3272-1003으로 연락하세요.')],
        src="한성컴퓨터 고객센터 다운로드 안내",
        kw='한성 드라이버 한성컴퓨터 드라이버 한성 노트북 드라이버 TFG 드라이버 보스몬스터 드라이버 한성 고객센터 다운로드',
        sub='노트북 고객센터 다운로드'),
    'razer': dict(
        name='레이저', en='Razer', kind='periph', lines='마우스·키보드·헤드셋·Blade 노트북',
        ans='레이저 마우스·키보드·헤드셋은 <b>Razer Synapse 4</b>(Windows 10/11 64비트, 무료)로 펌웨어 업데이트와 설정을 해요. <b>Synapse 3은 2026년 2월 3일부터 업데이트와 클라우드 서비스가 끝났으니</b> Synapse 4로 옮기세요. Blade 노트북 드라이버는 레이저 지원 사이트에서 받아요.',
        tools=[('Razer Synapse 4', '레이저 주변기기 설정·매크로·조명·펌웨어 업데이트용 레이저 공식 프로그램이에요. Windows 10/11 64비트.',
                'https://www.razer.com/synapse-4', 'Synapse 4 받기', '레이저 공식 · 무료')],
        site=('https://mysupport.razer.com/', '레이저 지원 (Blade 노트북·제품별)', '제품 선택 → 소프트웨어·드라이버'),
        site_en='https://mysupport.razer.com/',
        steps=['위 <b>[Synapse 4 바로 받기]</b>로 설치 파일을 받아 실행해요.',
               '레이저 기기를 <b>USB로 직접</b> 꽂으면 Synapse 4가 자동으로 알아봐요.',
               '업데이트가 있으면 알림이 떠요. 펌웨어 업데이트 중에는 <b>기기를 뽑지 마세요</b>.',
               'Blade 노트북은 레이저 지원에서 모델을 골라 드라이버를 받아요.'],
        serial='기기 바닥면이나 케이블 쪽 스티커의 <b>모델명·S/N</b>을 보세요. Synapse 4에도 연결된 기기 이름이 나와요.',
        qa=[('Synapse 3을 계속 써도 되나요?', '켜지긴 해도 2026년 2월 3일부터 업데이트와 클라우드(설정 동기화 등)가 끝났어요. 새 기기 지원과 보안 수정은 Synapse 4로만 나와요.'),
            ('마우스는 드라이버 없이도 되던데요?', '기본 동작은 윈도우가 알아서 해요. 버튼 매크로·DPI·조명을 바꾸거나 펌웨어를 업데이트할 때 Synapse가 필요해요.')],
        src='레이저 지원 Razer Synapse 4 안내, Razer Synapse 3 서비스 종료 안내',
        kw='레이저 드라이버 Razer 드라이버 레이저 마우스 드라이버 시냅스 Razer Synapse 4 시냅스 3 종료 레이저 키보드 드라이버',
        sub='Synapse 4 마우스·키보드'),
    'canon': dict(
        name='캐논', en='Canon', kind='printer', lines='PIXMA 잉크젯·imageCLASS·LBP 레이저',
        ans='캐논 프린터·복합기 드라이버는 <b>캐논코리아 고객지원 → 다운로드</b>에서 <b>모델명</b>(예: G3910, MF643Cdw)으로 검색해 받아요. 잉크젯(PIXMA·G시리즈)은 드라이버와 스캔 프로그램이 들어 있는 <b>풀 드라이버·소프트웨어 패키지</b>를 받으면 한 번에 깔려요.',
        tools=[],
        site=('https://svc.kr.canon/', '캐논코리아 고객지원 다운로드', '모델명 검색 → 드라이버'),
        site_en='https://www.canon-europe.com/support/',
        steps=['프린터 앞면·윗면의 <b>모델명</b>을 확인해요.',
               '캐논코리아 고객지원 다운로드에서 모델명을 검색하고 <b>드라이버·소프트웨어</b>를 열어요.',
               '내 윈도우 버전을 고르고, 잉크젯은 <b>풀 드라이버 &amp; 소프트웨어 패키지</b>, 레이저는 <b>프린터 드라이버</b>를 받아요.',
               '받은 파일을 실행하고 연결 방법(USB 또는 무선 LAN)을 고르면 프린터를 찾아 설치해요.'],
        serial='프린터 앞면이나 윗면에 모델명이 적혀 있어요. 뒷면 스티커에도 있어요.',
        qa=[('스캔이 안 돼요.', '프린터 드라이버만 깔면 스캔 프로그램이 없을 수 있어요. 잉크젯은 풀 패키지를, 복합기는 스캐너 드라이버(ScanGear 등)를 같이 받으세요.')],
        src='캐논코리아 고객지원 다운로드',
        kw='캐논 드라이버 캐논 프린터 드라이버 Canon 드라이버 G3910 드라이버 G2910 드라이버 MF643Cdw 드라이버 PIXMA 드라이버 LBP 드라이버',
        sub='PIXMA·imageCLASS·LBP'),
    'fujifilm': dict(
        name='후지필름 BI (옛 후지제록스)', short='후지필름', en='FUJIFILM Business Innovation', kind='printer', lines='Apeos·ApeosPort·DocuPrint 복합기·프린터',
        ans='후지제록스는 <b>2021년 4월 1일 후지필름 비즈니스 이노베이션(후지필름 BI)</b>으로 이름이 바뀌었어요. 드라이버는 <b>후지필름 BI 코리아 지원·다운로드</b>에서 모델명으로 찾아요. 여러 모델을 함께 쓰는 사무실은 <b>Multi-Model Print Driver</b> 하나로 여러 기기를 쓸 수 있고, ARM 노트북(스냅드래곤 등)은 <b>Multi-Model Print Driver 2</b>를 써요.',
        tools=[],
        site=('https://www.fujifilm.com/fbkr/ko', '후지필름 BI 코리아 (지원·다운로드)', '지원 → 다운로드 → 모델명 검색'),
        site_en='https://www.fujifilm.com/fb/',
        steps=['복합기 앞면 또는 조작부 위의 <b>모델명</b>(예: Apeos C3060, DocuPrint P285 dw)을 확인해요.',
               '후지필름 BI 코리아에서 <b>지원 → 다운로드</b>로 들어가 모델명을 검색해요.',
               '내 윈도우 버전을 고르고 <b>프린터 드라이버</b>(필요하면 스캐너 드라이버)를 받아요.',
               '받은 파일을 실행하고, 네트워크 복합기는 설치 중에 <b>IP 주소</b>로 기기를 찾아 연결해요.'],
        serial='복합기 앞면이나 조작부 근처에 모델명이 있어요. 회사 복합기는 기기 IP 주소를 전산 담당자에게 물어보면 설치가 빨라요.',
        qa=[('제록스(Xerox) 드라이버를 받으면 되나요?', '한국에서 쓰던 후지제록스 제품은 후지필름 BI 사이트에서 받아요. 미국 Xerox는 다른 회사라 드라이버가 맞지 않을 수 있어요.')],
        src='후지필름 비즈니스 이노베이션 코리아 지원·다운로드, 사명 변경 안내',
        kw='후지제록스 드라이버 후지필름 드라이버 후지필름 BI 드라이버 Apeos 드라이버 ApeosPort 드라이버 DocuPrint 드라이버 후지제록스 복합기 드라이버',
        sub='옛 후지제록스 복합기'),
    'kyocera': dict(
        name='교세라', en='Kyocera', kind='printer', lines='TASKalfa 복합기·ECOSYS 프린터',
        ans='교세라 복합기·프린터는 여러 모델에 쓰는 <b>KX Driver</b>(Windows 10/11)를 많이 써요. <b>교세라 다운로드 센터</b>에서 모델명(예: TASKalfa 2554ci, ECOSYS M2640idw)을 검색해 드라이버를 받아요.',
        tools=[],
        site=('https://www.kyoceradocumentsolutions.co.kr/', '한국교세라 (지원 → 다운로드 센터)', '모델명 검색 → KX Driver'),
        site_en='https://www.kyoceradocumentsolutions.us/en/support/downloads.html',
        steps=['복합기 앞면의 <b>모델명</b>을 확인해요.',
               '교세라 다운로드 센터에서 모델명을 검색하고 <b>Drivers</b>(드라이버) 탭을 열어요.',
               '<b>KX Driver</b>를 받아 압축을 풀고 <b>Setup</b>을 실행해요.',
               '설치 화면에서 <b>빠른 설치</b>를 고르면 네트워크·USB로 연결된 기기를 찾아 설치해요.'],
        serial='복합기 앞면 조작부 위나 원고대 근처에 모델명이 있어요.',
        qa=[('KX Driver와 KX V4 Driver는 뭐가 달라요?', '둘 다 교세라 공식 드라이버예요. 보통은 KX Driver를 쓰고, 회사 전산 지침이 V4를 쓰라고 하면 그걸 고르세요.')],
        src='교세라 다운로드 센터 KX Driver 안내',
        kw='교세라 드라이버 교세라 복합기 드라이버 Kyocera 드라이버 KX Driver TASKalfa 드라이버 ECOSYS 드라이버 M2640idw 드라이버',
        sub='TASKalfa·ECOSYS KX'),
    'ricoh': dict(
        name='리코', en='Ricoh', kind='printer', lines='IM·MP 복합기·SP 프린터',
        ans='리코 복합기·프린터는 <b>리코 공식 지원(support.ricoh.com)</b>에서 모델명으로 드라이버를 받아요. 여러 리코 기기를 함께 쓰면 <b>PCL6 Driver for Universal Print</b> 하나로 여러 모델에 인쇄할 수 있어요.',
        tools=[],
        site=('https://support.ricoh.com/', '리코 공식 지원 (드라이버 다운로드)', '모델명 → 윈도우 버전 → 드라이버'),
        site_en='https://support.ricoh.com/',
        steps=['복합기 앞면의 <b>모델명</b>(예: IM C3000, SP C261DNw)을 확인해요.',
               '리코 공식 지원에서 모델명을 고르고 내 윈도우 버전을 선택해요.',
               '<b>PCL6</b> 드라이버(또는 Universal Print 드라이버)를 받아 압축을 풀어요.',
               '<b>설정 → 프린터 및 스캐너 → 장치 추가</b>에서 기기를 추가하고, 드라이버를 고르라고 하면 받은 폴더를 지정해요.'],
        serial='복합기 앞면 또는 조작 패널 근처에 모델명이 있어요.',
        qa=[('PCL6, PS는 뭘 골라요?', '사무용 문서는 보통 PCL6를 써요. 디자인 작업(PostScript가 필요한 프로그램)을 하면 PS 드라이버를 고르세요.')],
        src="리코 공식 지원 'PCL6 Driver for Universal Print'",
        kw='리코 드라이버 리코 복합기 드라이버 Ricoh 드라이버 리코 프린터 드라이버 PCL6 Universal Print IM C3000 드라이버',
        sub='IM·MP 복합기 PCL6'),
    'logitech': dict(
        name='로지텍', en='Logitech', kind='periph', lines='마우스·키보드·웹캠·Logitech G',
        ans='로지텍 마우스·키보드는 <b>Logi Options+</b>, 게이밍 제품(Logitech G)은 <b>G HUB</b>로 버튼 설정과 펌웨어 업데이트를 해요(둘 다 무료). 예전 <b>Unifying 소프트웨어·Firmware Update Tool</b> 같은 옛 프로그램은 지원이 끝났어요.',
        tools=[('Logi Options+ (일반 마우스·키보드)', 'MX·Pebble·Signature 같은 로지텍 마우스·키보드의 버튼·제스처 설정과 펌웨어 업데이트용 로지텍 공식 프로그램이에요. Windows 10 버전 1903 이상.',
                'https://www.logitech.com/ko-kr/software/logi-options-plus.html', 'Logi Options+ 받기', '로지텍 공식 · 무료'),
               ('Logitech G HUB (게이밍)', 'G 시리즈 마우스·키보드·헤드셋의 DPI·매크로·조명 설정과 펌웨어 업데이트용 프로그램이에요.',
                'https://www.logitechg.com/ko-kr/innovation/g-hub.html', 'G HUB 받기', 'Logitech G 공식 · 무료')],
        site=('https://support.logi.com/', '로지텍 지원 (제품별 다운로드)', '제품 이름 검색 → 다운로드'),
        site_en='https://support.logi.com/',
        steps=['내 제품이 일반(MX·Pebble·Signature 등)이면 <b>Logi Options+</b>, G 로고가 있으면 <b>G HUB</b>를 받아요.',
               '받은 파일을 실행해 설치하고, 마우스·키보드를 연결해요(USB 수신기 또는 블루투스).',
               '프로그램에 기기가 나오면 눌러서 버튼 설정을 바꾸고, 업데이트 알림이 있으면 펌웨어를 업데이트해요.',
               '잘 모르겠으면 로지텍 지원에서 제품 이름을 검색해 맞는 프로그램을 확인해요.'],
        serial='마우스·키보드 바닥 스티커에 모델명(M/N)이 있어요. 수신기 USB에는 주황색 별(Unifying)이나 Logi Bolt 표시가 있어요.',
        qa=[('Logi Options(옛 버전)는요?', 'Logi Options+로 바뀌었어요. 오래된 윈도우를 쓰면 로지텍 지원에서 안내하는 구버전 Options+(1.44)를 쓸 수 있어요.'),
            ('수신기를 잃어버렸어요. 새 수신기 연결은요?', 'Logi Options+의 기기 추가에서 수신기 연결(페어링)을 할 수 있어요. Unifying 수신기와 Logi Bolt 수신기는 서로 호환되지 않아요.')],
        src='로지텍 소프트웨어 다운로드(Logi Options+, G HUB), 로지텍 지원 안내',
        kw='로지텍 드라이버 Logitech 드라이버 로지텍 마우스 드라이버 Logi Options+ 옵션플러스 G HUB 지허브 로지텍 키보드 드라이버 Unifying',
        sub='Options+·G HUB'),
    'wacom': dict(
        name='와콤', en='Wacom', kind='periph', lines='Intuos·Cintiq·Wacom One 펜 타블렛',
        ans='와콤 타블렛은 <b>와콤 공식 드라이버</b>를 설치해야 필압·버튼이 제대로 동작해요. 드라이버를 설치하면 <b>Wacom Center</b>가 함께 깔리고, 최신 제품은 Wacom Center에서만 설정을 바꿀 수 있어요. 오래된 제품은 와콤 드라이버 페이지의 <b>옛 버전(레거시) 드라이버</b>를 받아요.',
        tools=[('와콤 드라이버 (Windows·Mac)', '와콤 펜 타블렛·액정 타블렛 공식 드라이버예요. 설치하면 Wacom Center가 함께 설치돼요.',
                'https://www.wacom.com/ko-kr/support/product-support/drivers', '와콤 드라이버 받기', '와콤 공식 · 무료')],
        site=('https://www.wacom.com/ko-kr/support/product-support/drivers', '와콤 드라이버 페이지 (모델 검색)', '모델명(예: CTL-4100) 검색'),
        site_en='https://www.wacom.com/en-us/support/product-support/drivers',
        steps=['타블렛 뒷면의 <b>모델 번호</b>(예: CTL-4100, DTC133)를 확인해요.',
               '와콤 드라이버 페이지에서 모델 번호를 검색하거나 <b>Windows/Mac 최신 드라이버</b>를 받아요.',
               '타블렛을 <b>뽑은 상태</b>에서 설치하고, 끝나면 컴퓨터를 다시 시작해요.',
               '타블렛을 꽂고 <b>Wacom Center</b>를 열어 펜 버튼·필압·영역을 설정해요.'],
        serial='타블렛 <b>뒷면 스티커</b>에 모델 번호(CTL-, CTH-, PTH-, DTC- 등으로 시작)가 있어요.',
        qa=[('Wacom Center를 지우면 어떻게 돼요?', '드라이버도 함께 지워져요. 와콤 안내에 따르면 드라이버는 항상 Wacom Center와 함께 설치돼요.'),
            ('필압이 안 먹어요.', '드라이버를 지우고 다시 설치해 보세요. 그림 프로그램에서 Windows Ink 설정을 켜거나 꺼야 할 때도 있어요.')],
        src="와콤 지원 드라이버 페이지, 와콤 지원 커뮤니티 답변(드라이버와 Wacom Center)",
        kw='와콤 드라이버 Wacom 드라이버 와콤 타블렛 드라이버 인튜어스 드라이버 Intuos 드라이버 신티크 드라이버 Wacom Center CTL-4100 드라이버',
        sub='펜 타블렛 드라이버'),
    'realtek': dict(
        name='리얼텍', en='Realtek', kind='chip', lines='랜카드(이더넷)·오디오·카드리더 칩',
        ans='리얼텍은 메인보드·노트북 안에 들어가는 <b>칩 회사</b>예요. 그래서 랜·오디오 드라이버는 <b>내 메인보드나 노트북 회사 사이트</b>에서 받는 게 가장 잘 맞아요(오디오는 회사마다 기능을 넣어 둬서 특히 그래요). 유선 랜(<b>Realtek PCIe GbE / 2.5GbE Family Controller</b>)은 리얼텍 공식 사이트에서도 받을 수 있어요.',
        tools=[],
        site=('https://www.realtek.com/', '리얼텍 공식 사이트 (Downloads)', 'Downloads → Communications Network ICs → 랜 드라이버'),
        site_en='https://www.realtek.com/',
        steps=['<b>Win + X → 장치 관리자</b>를 열어요. <b>네트워크 어댑터</b>에 \'Realtek PCIe GbE Family Controller\' 같은 이름이 있는지 봐요.',
               '먼저 <b>메인보드·노트북 회사</b> 사이트에서 내 모델의 LAN·오디오 드라이버를 받아요(아래 다른 회사 드라이버).',
               '랜 드라이버를 최신으로 바꾸고 싶으면 리얼텍 공식 사이트 Downloads에서 윈도우 버전에 맞는 파일을 받아 압축을 풀고 <b>setup.exe</b>를 실행해요.',
               '설치 후 다시 시작하고, 인터넷이 잘 되는지 확인해요.'],
        serial='장치 관리자의 장치 이름(예: Realtek PCIe 2.5GbE Family Controller, Realtek(R) Audio)을 보면 어떤 칩인지 알 수 있어요.',
        qa=[('Realtek HD 오디오 관리자가 없어졌어요.', '요즘은 \'Realtek Audio Console\' 앱으로 바뀌었고, 메인보드·노트북 회사 드라이버와 함께 깔려요. 회사 사이트의 오디오 드라이버를 다시 설치해 보세요.'),
            ('윈도우를 새로 깔았더니 인터넷이 안 돼요.', '랜 드라이버가 없어서 그래요. 다른 컴퓨터로 메인보드 회사 사이트에서 LAN 드라이버를 받아 USB로 옮겨 설치하세요.')],
        src='리얼텍 공식 사이트 Downloads, 각 메인보드 제조사 LAN 드라이버 안내',
        kw='리얼텍 드라이버 Realtek 드라이버 리얼텍 랜 드라이버 Realtek PCIe GbE Family Controller 드라이버 리얼텍 오디오 드라이버 랜카드 드라이버',
        sub='랜·오디오 칩'),
    'iptime': dict(
        name='ipTIME', en='ipTIME', kind='net', lines='공유기·USB 무선랜카드(A3000UA 등)',
        ans='아래 <b>모델별 표</b>에서 내 모델의 <b>[바로 받기]</b>를 누르면 ipTIME 서버에서 드라이버 파일이 바로 받아져요(A3000UA·AX900UA·BE6500UA 등). 표에 없으면 ipTIME USB 무선랜카드 드라이버와 공유기 펌웨어는 <b>ipTIME 홈페이지 → 다운로드 자료실</b>에서 <b>구분(드라이버/펌웨어)</b>을 고르고 <b>모델명</b>을 검색해 받아요. 공유기 펌웨어는 관리 화면(보통 <b>192.168.0.1</b>) → <b>고급 설정 → 시스템 관리 → 펌웨어 업그레이드</b>에서 바로 할 수도 있어요.',
        tools=[],
        site=('https://iptime.com/', 'ipTIME 홈페이지 (다운로드 자료실)', '구분 선택 → 모델명 검색'),
        site_en='https://iptime.com/',
        steps=['제품 뒷면·바닥의 <b>모델명</b>(예: A3000UA, A3000MINI, AX2004M)을 확인해요.',
               'ipTIME 홈페이지 <b>다운로드 자료실</b>에서 구분을 <b>드라이버</b>(랜카드) 또는 <b>펌웨어</b>(공유기)로 고르고 모델명을 검색해요.',
               '랜카드: 받은 파일을 실행해 설치하고, USB에 꽂은 뒤 와이파이를 선택해 연결해요.',
               '공유기: 관리 화면 → 고급 설정 → 시스템 관리 → <b>펌웨어 업그레이드</b>를 눌러요. 진행 중에는 <b>전원을 절대 빼지 마세요</b>.'],
        serial='랜카드는 몸체·포장 상자에, 공유기는 바닥 스티커에 모델명이 있어요.',
        qa=[('윈도우 11에서 꽂기만 하면 되나요?', '최근 모델은 윈도우가 드라이버를 자동으로 잡는 경우가 많아요. 인식이 안 되거나 속도가 느리면 다운로드 자료실의 최신 드라이버를 설치하세요.'),
            ('펌웨어를 꼭 올려야 하나요?', '보안 문제를 고친 펌웨어가 자주 나와요. 공유기는 해킹 대상이 되기 쉬우니 최신 버전으로 유지하는 게 좋아요.')],
        src='ipTIME(이에프엠네트웍스) 다운로드 자료실·펌웨어 배포 안내',
        kw='ipTIME 드라이버 아이피타임 드라이버 아이피타임 랜카드 드라이버 A3000UA 드라이버 A3000MINI 드라이버 ipTIME 펌웨어 업그레이드 무선랜카드 드라이버',
        sub='랜카드 드라이버·공유기 펌웨어'),
    'tplink': dict(
        name='TP-Link', en='TP-Link', kind='net', lines='USB 무선랜카드(Archer T·TX)·공유기',
        ans='아래 <b>모델별 표</b>에서 <b>[바로 받기]</b>를 누르면 TP-Link 서버에서 드라이버가 바로 받아져요(Archer T3U·TX20U·UB500 등). 표에 없는 모델은 <b>TP-Link 다운로드 센터</b>에서 모델명을 검색하고, 제품 스티커의 <b>하드웨어 버전</b>(예: V2)을 골라 드라이버·펌웨어를 받아요. 하드웨어 버전이 다르면 파일이 맞지 않으니 꼭 맞춰 고르세요.',
        tools=[],
        site=('https://www.tp-link.com/kr/support/download/', 'TP-Link 다운로드 센터', '모델 검색 → 하드웨어 버전 선택'),
        site_en='https://www.tp-link.com/us/support/download/',
        steps=['제품 스티커에서 <b>모델명</b>(예: Archer T3U, Archer TX20U)과 <b>Ver</b>(하드웨어 버전)를 확인해요.',
               'TP-Link 다운로드 센터에서 모델을 찾고, 오른쪽 위 <b>하드웨어 버전</b>을 내 버전으로 바꿔요.',
               '<b>드라이버</b>(랜카드) 또는 <b>펌웨어</b>(공유기)에서 내 윈도우 버전 파일을 받아 압축을 풀어요.',
               '랜카드는 <b>Setup.exe</b>를 실행해 설치하고 다시 시작해요. 공유기 펌웨어는 관리 화면의 펌웨어 업그레이드에서 올려요.'],
        serial='제품 뒷면·바닥 스티커에 모델명과 <b>Ver: 1.0</b> 같은 하드웨어 버전이 있어요.',
        qa=[('블루투스 겸용 랜카드인데 블루투스가 안 보여요.', 'TP-Link 다운로드 센터에서 와이파이 드라이버와 블루투스 드라이버를 따로 받아 둘 다 설치하세요.')],
        src='TP-Link 한국 다운로드 센터, TP-Link USB 어댑터 빠른 설치 가이드',
        kw='TP-Link 드라이버 티피링크 드라이버 TP-Link 무선랜카드 드라이버 Archer T3U 드라이버 Archer TX20U 드라이버 TP-Link 펌웨어 하드웨어 버전',
        sub='무선랜카드·공유기'),
}


# ── 바로 받기 파일 (2026-11-23 공식 서버 주소 확인) ──────────────────
# (제목, 설명, 파일 주소, 버튼 글자, 작은 글자)
IP = 'https://iptime.com'
DL = {
    'msi': [('MSI Center 설치 파일', 'MSI 노트북·데스크톱·메인보드용 공식 프로그램이에요. 압축을 풀고 설치 파일을 실행하세요. 설치 후 Support → Live Update → Scan으로 드라이버를 한 번에 받아요.',
             'https://download-2.msi.com/uti_exe/desktop/MSI-Center.zip', 'MSI Center 바로 받기', 'MSI 서버에서 바로 다운로드 · .zip · 최신판 · 약 595MB')],
    'gigabyte': [('GIGABYTE Control Center (GCC) 전체 설치 파일', '기가바이트 메인보드·그래픽카드·노트북 통합 프로그램이에요. 파일이 약 861MB로 커서 받는 데 시간이 걸려요. 압축을 풀고 설치 후 업데이트 센터에서 드라이버를 설치해요.',
                  'https://download.gigabyte.com/FileList/Utility/GCC_26.11.05.01.zip', 'GCC 바로 받기', '기가바이트 서버 · .zip · 26.11.05.01 · Windows 10/11 64비트')],
    'asrock': [('Realtek 랜(LAN) 드라이버 — 윈도우 설치 후 인터넷이 안 될 때', '애즈락 메인보드 공용 Realtek 유선 랜 드라이버예요. 압축을 풀고 setup.exe를 실행하세요.',
                'https://download.asrock.com/Drivers/All/LAN/Realtek_LAN(v10.080.0525.2026).zip', '랜 드라이버 바로 받기', '애즈락 서버 · .zip · v10.080.0525.2026'),
               ('Realtek 오디오 드라이버', '애즈락 메인보드 공용 Realtek 오디오 드라이버예요.',
                'https://download.asrock.com/Drivers/All/Audio/Realtek_Audio(v10007.1_UAD_WHQL).zip', '오디오 드라이버 바로 받기', '애즈락 서버 · .zip · v10007.1')],
    'razer': [('Razer Synapse 4 설치 파일', '레이저 마우스·키보드·헤드셋 공식 프로그램이에요. Windows 10/11 64비트.',
               'https://dl.razerzone.com/drivers/Synapse4/RazerSynapseInstaller.exe', 'Synapse 4 바로 받기', '레이저 서버에서 바로 다운로드 · .exe')],
    'canon': [('캐논 레이저 복합기·프린터 공용 드라이버 (Generic Plus PCL6)', 'imageCLASS·imageRUNNER 등 캐논 레이저 기기 여러 모델에 쓰는 캐논 공용 드라이버예요. 잉크젯(PIXMA·G시리즈)은 아래 다운로드 센터에서 모델명으로 받아요.',
               'https://gdlp01.c-wss.com/gds/0/0100011580/03/GPlus_PCL6_Driver_V272_32_64_00.exe', '레이저 공용 드라이버 받기', '캐논 서버 · .exe · V2.72 · 32/64비트')],
    'fujifilm': [('Easy Setup Installer (기기 자동 감지 설치)', 'USB나 네트워크로 연결된 후지필름 복합기·프린터를 자동으로 찾아 맞는 드라이버를 한 번에 설치해 주는 공식 도구예요. 버전 1.0.19.1.',
                  'https://support-fb.fujifilm.com/tiles/common/hc_drivers_download.jsp?system=%27Windows%2011%2064bit%27&shortdesc=null&xcrealpath=OJ7/3Y0JABCUugXbobj67DOoOaxSrKOz42E2aFJeD2RngMd0NLEQBBTqI6BdeB1jktOAm2qKraFEnGYF9RbrkS3b4UoiDGMtkArucTqazp0=',
                  'Easy Setup 바로 받기', '후지필름 BI 서버 · Windows 11/10'),
                 ('Easy Setup 안내 페이지', '바로 받기가 안 되면 이 공식 페이지에서 [이지 셋업 인스톨러]를 눌러요.',
                  'https://support-fb.fujifilm.com/setupDriverForm.do?pid=EasySI&ctry_code=KR&lang_code=ko&d_lang=ko', 'Easy Setup 공식 페이지', '후지필름 BI 코리아')],
    'kyocera': [('KX Print Driver 8.7.0917 (여러 모델 공용)', 'TASKalfa·ECOSYS 대부분 모델에 쓰는 교세라 공식 드라이버예요. 약 241MB. 실행하면 설치 화면이 나와요.',
                 'https://www.kyoceradocumentsolutions.us/content/dam/download-center-americas-cf/us/drivers/drivers/KX_Print_Driver_exe.download.exe', 'KX Driver 바로 받기', '교세라 서버 · .exe · 8.7.0917 · Windows 10/11')],
    'ricoh': [('PCL6 Driver for Universal Print 4.46 (64비트)', '리코 복합기·프린터 여러 모델에 쓰는 공용 드라이버예요. 실행하면 압축이 풀리고 설치가 시작돼요. 2026-10-06 배포 · 약 34MB.',
               'https://support.ricoh.com/bb/pub_e/dr_ut_e/0001346/0001346104/V44600/z07510L24.exe', 'PCL6 공용 드라이버 받기', '리코 서버 · .exe · Ver.4.46.0.0')],
    'logitech': [('Logi Options+ (일반 마우스·키보드)', 'MX·Pebble·Signature 등 로지텍 마우스·키보드 설정·펌웨어 업데이트 프로그램이에요. Windows 10/11.',
                  'https://download01.logi.com/web/ftp/pub/techsupport/optionsplus/logioptionsplus_installer.exe', 'Options+ 바로 받기', '로지텍 서버 · .exe · 최신판'),
                 ('Logitech G HUB (게이밍)', 'G 시리즈 마우스·키보드·헤드셋 설정 프로그램이에요.',
                  'https://download01.logi.com/web/ftp/pub/techsupport/gaming/lghub_installer.exe', 'G HUB 바로 받기', '로지텍 서버 · .exe · 최신판'),
                 ('Logi Tune (웹캠·헤드셋)', 'Brio·C920 같은 웹캠 화질, Zone 헤드셋 설정 프로그램이에요.',
                  'https://software.vc.logitech.com/downloads/tune/LogiTuneInstall.exe', 'Logi Tune 바로 받기', '로지텍 서버 · .exe')],
    'wacom': [('와콤 드라이버 6.4.15-1 (Windows)', 'Intuos·Cintiq·Wacom One 등 와콤 타블렛 공식 드라이버예요. Wacom Center가 함께 설치돼요. Windows 10/11 64비트.',
               'https://cdn.wacom.com/u/productsupport/drivers/win/professional/WacomTablet_6.4.15-1.exe', '와콤 드라이버 바로 받기', '와콤 서버 · .exe · 6.4.15-1 · 약 320MB')],
    'realtek': [('Realtek 유선 랜 드라이버 Win10/Win11 (NDIS) 10.80.50', 'Realtek PCIe GbE·2.5GbE Family Controller용 자동 설치 프로그램이에요. 2026-10-05 · 약 5MB. 리얼텍 화면이 열리면 [Download file]을 한 번 더 누르세요. 압축을 풀고 setup.exe를 실행해요.',
                 'https://www.realtek.com/Download/ToDownload?mode=first&type=direct&downloadid=3613', '랜 드라이버 바로 받기', '리얼텍 공식 · .zip · Windows 10/11'),
                ('Realtek 유선 랜 드라이버 Win11 (NetAdapterCx) 11.031.50', '윈도우 11 전용 새 방식 드라이버예요. 위 파일로 문제가 있을 때 써 보세요. 2026-10-05 · 약 3MB.',
                 'https://www.realtek.com/Download/ToDownload?mode=first&type=direct&downloadid=4103', 'Win11 전용 받기', '리얼텍 서버 · .zip · Windows 11')],
}

# 모델별 바로 받기 표: (모델들, 운영체제, 파일 주소)
MODELS = {
    'iptime': [
        ('A3000UA, A3000UA-2, A3000U, A3000mini, A3000UA5, A2000UA, A2000U, N400UA, A5000UA', 'Windows 10·11', IP + '/legacy/cdn/link/wlan/RTLWlanU_WindowsDriver_1030.44.0809.2021_Drv_3.00.0037_Win10_Win11.L_54539_.zip'),
        ('NCUBIC, N3U, N300U, N100mini, N500U', 'Windows 11', IP + '/legacy/cdn/link/wlan/RTLWlanU_WindowsDriver_1030.44.0809.2021_Drv_3.00.0037_Win10_Win11.L(54539).zip'),
        ('AX2000U, AX2000UA', 'Windows 10·11', IP + '/legacy/cdn/link/wlan/iptime_AX2000U_AX2000UA_5001.19.128.2.exe'),
        ('AX2000T-UA', 'Windows 10·11', IP + '/legacy/cdn/link/wlan/iptime_AX2000T-UA_5001.19.128.2.exe'),
        ('AX900UA, AX900mini', 'Windows 10·11', IP + '/legacy/cdn/link/wlan/ax900mini/RTWlanUSB_WindowsDriver_5001.19.113.3_Drv_3.00.0045.L.zip'),
        ('AX5400UA-6E', 'Windows 10·11', IP + '/legacy/cdn/link/wlan/ax5400ua6e/RTWlanUSB_WindowsDriver_5001.19.113.3_Drv_3.00.0045.L(184071).zip'),
        ('AX5400PX, AX5400PX-E, AX5400PX-6E, BE9300IPX (인텔 칩)', 'Windows 10·11', 'https://downloadmirror.intel.com/929786/WiFi-24.80.0-Driver64-Win10-Win11.exe'),
        ('BE6500UA', 'Windows 11', IP + '/legacy/cdn/link/wlan/BE6500UA/RTWlanUSB_WindowsDriver_5102.24.126.0_Drv_3.00.0045.L(184002).zip'),
        ('BE6500UA', 'Windows 10', IP + '/legacy/cdn/link/wlan/BE6500UA/RTWlanUSB_WindowsDriver_5002.24.117.1_Drv_3.00.0045_TS.L-1(168678).zip'),
        ('BE6500PX, BE6500PX-E', 'Windows 11', IP + '/legacy/cdn/link/wlan/be6500px/iptime_be6500px_5.4.0.2913_installer.zip'),
        ('A2000PX, A2000PX-MU', 'Windows 11', IP + '/legacy/cdn/link/wlan/RTLWlanE_WindowsDriver_2024.0.10.135_Drv_3.00.0039_Win11.L(55894).zip'),
        ('유선 U2500, U2500C, U1000, U1G, U1G-C, U1003, U1003C, U25G, U25G-C', 'Windows 11', IP + '/upload/admin/downloads/2026/11/mwegck7m3003243df285.zip'),
        ('유선 U2500, U2500C, U1000, U1G, U1G-C, U1003, U1003C, U25G, U25G-C', 'Windows 10', IP + '/upload/admin/downloads/2026/11/mwegckjkb0708a9e3873.zip'),
        ('유선 U2LAN, UC2LAN', 'Windows 11', IP + '/legacy/cdn/link/lan/Install_USB_Win11_11021_20_11102025_01302026.zip'),
        ('유선 U2LAN, UC2LAN', 'Windows 10', IP + '/legacy/cdn/link/lan/Install_USB_Win10_10066_20_11102025_01302026.zip'),
        ('유선 UC306HDMI-1G, UC306HDMI2-1G, U1003CA', 'Windows 11', IP + '/legacy/cdn/link/lan/uc306hdmi/Install_USB_Win11_11019_20_06032025_07212025.zip'),
        ('유선 PX10G, PX10G2', 'Windows 10·11', IP + '/legacy/cdn/link/lan/20221109_Marvell_AQtion_Win10-11_3.1.7.zip'),
    ],
    'tplink': [
        ('Archer T3U (V1)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2024/202411/20241128/Archer_T3U_V1_1030.44.0408.2024_Win10Win11.zip'),
        ('Archer T3U Plus (V1)', 'Windows 10·11', 'https://static.tp-link.com/2019/201912/20191223/Archer%20T3U%20Plus(EUUS)_V1_win10_191204.zip'),
        ('Archer T2U Plus (V1)', 'Windows (10은 자동 인식)', 'https://static.tp-link.com/2019/201905/20190508/Archer%20T2U_Plus_UN_V1_190422_Win.zip'),
        ('Archer TX20U (V1)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2026/202608/20260824/Archer_TX20U_V1.0_V1.6_5001.19.128.2forWin10x86_5001.19.128.3forWin10x64Win11.zip'),
        ('Archer TX20U Plus (V1)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2026/202608/20260807/Archer%20TX20U%20Plus_128.4%20Operating%20System%20win10x86x64_win11x64.zip'),
        ('Archer TX10UB Nano (V1, 와이파이+블루투스)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2025/202510/20251021/Archer_TX10UB_Nano(US)_V1_5001.19.113.1_Win10_Win11.zip'),
        ('Archer T2UB Nano (V1.40)', 'Windows 7~11', 'https://static.tp-link.com/upload/driver/2025/202507/20250704/Archer_T2UB%20Nano(EU)_V1_20250702_Win7_8_8.1_10_11.zip'),
        ('TL-WN725N (V3)', 'Windows 10·11', 'https://static.tp-link.com/upload/software/2021/202108/20210810/TL-WN725N_US_V3_200821_Win10.zip'),
        ('UB500 블루투스 동글 (V3)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2025/202507/20250704/UB500(UN)_V3_20250702_Win10_Win11.zip'),
        ('UB400 블루투스 동글 (V2)', 'Windows 7~11', 'https://static.tp-link.com/upload/driver/2024/202403/20240326/V2_1.9.1051.3012.zip'),
        ('Archer TX3000E (V4, PCIe)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2025/202507/20250704/Archer_TX3000E(UN)_V4_20250702_Win10_11.zip'),
        ('Archer TX50E (V3, PCIe)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2025/202507/20250704/Archer_TX50E(UN)_V3_20250702_Win10_11.zip'),
        ('Archer TX55E (V4, PCIe)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2025/202507/20250704/Archer_TX55E(UN)_V4_20250702_Win10_11.zip'),
        ('Archer TX20E (V1, PCIe)', 'Windows 10·11', 'https://static.tp-link.com/upload/driver/2025/202507/20250704/Archer_TX20E(UN)_V1_20250702_Win10_11.zip'),
        ('Archer TBE550E (V1, PCIe Wi-Fi 7)', 'Windows 11', 'https://static.tp-link.com/upload/driver/2025/202507/20250724/Archer_TBE550E_V1_Aoturun_20250703.zip'),
    ],
}
for _k, _v in DL.items():
    C[_k]['tools'] = _v


MH = {}


def model_table(k):
    rows = MODELS.get(k)
    if not rows:
        return ''
    tr = ''.join(f'<tr><td><b>{E(m)}</b></td><td>{E(o)}</td><td><a class="mdl" href="{E(u)}" rel="noopener nofollow">바로 받기 ↓</a></td></tr>' for m, o, u in rows)
    h = MH.get(k, ('모델별 드라이버 바로 받기', '모델', '윈도우', '모델명'))
    return (f'<section class="card dr-sec" id="models"><h2>{h[0]}</h2>'
            f'<p class="cu-src">{h[5] if len(h) > 5 else "버튼을 누르면 제조사 서버에서 설치 파일이 바로 받아져요. 모델명을 찾을 땐 아래 칸에 입력하세요."}</p>'
            f'<input class="mq" placeholder="{h[3]} 입력 (예: {E(h[4] if len(h) > 4 else rows[0][0].split(",")[0].replace("유선 ", ""))})" oninput="var q=this.value.toUpperCase().replace(/\\s/g,\'\');this.nextElementSibling.querySelectorAll(\'tr\').forEach(function(r){{r.style.display=!q||r.cells[0].textContent.toUpperCase().replace(/\\s/g,\'\').indexOf(q)>=0?\'\':\'none\'}})" aria-label="{h[3]} 검색">'
            f'<div class="mt"><table><thead><tr><th>{h[1]}</th><th>{h[2]}</th><th>받기</th></tr></thead><tbody>{tr}</tbody></table></div></section>')


MT_CSS = ('<style>.mq{width:100%;box-sizing:border-box;padding:12px 14px;border:1.5px solid #CBD5E1;border-radius:12px;font-size:15px;margin:8px 0 10px}'
          '.mt{overflow-x:auto}.mt table{width:100%;border-collapse:collapse;font-size:14px}.mt th,.mt td{padding:10px 8px;border-bottom:1px solid #E9EDF3;text-align:left;vertical-align:middle;word-break:keep-all}'
          '.mt th{font-size:12.5px;color:#5B6B82}.mt td:nth-child(2){white-space:nowrap;color:#333}.mdl{display:inline-block;white-space:nowrap;background:#1D4ED8;color:#fff!important;font-weight:800;padding:8px 12px;border-radius:10px;text-decoration:none}'
          '@media(max-width:480px){.mt td,.mt th{padding:9px 5px;font-size:13px}.mdl{padding:7px 9px}}</style>')

ORDER = list(C)

KIND_KO = {'pc': '노트북·PC', 'board': '메인보드', 'printer': '프린터·복합기', 'periph': '주변기기', 'chip': '칩셋', 'net': '랜카드·공유기'}


def short(c):
    return c.get('short', c['name'])


def win_sec(kind):
    if kind == 'printer':
        return kr.WIN_SEC
    if kind == 'runtime':
        return ('<section class="card dr-sec" id="win"><h2>먼저 해 볼 것: Windows 업데이트</h2><ul class="cu-chk">'
                '<li><b>설정 → Windows 업데이트</b>에서 모든 업데이트를 설치하고 다시 시작해요. 런타임 보안 업데이트가 함께 들어와요.</li>'
                '<li>그래도 같은 오류가 나면 이 페이지의 파일을 받아 설치(또는 [복구])해요.</li></ul></section>')
    if kind in ('pc', 'board'):
        return kr.WIN_PC
    return ('<section class="card dr-sec" id="win"><h2>먼저 해 볼 것: 연결과 Windows 업데이트</h2><ul class="cu-chk">'
            '<li>기기를 <b>USB 허브 말고 컴퓨터 본체에 직접</b> 꽂아요. 기본 드라이버는 윈도우가 알아서 깔아 주는 경우가 많아요.</li>'
            '<li><b>설정 → Windows 업데이트 → 고급 옵션 → 선택적 업데이트</b>에 드라이버가 올라와 있으면 설치해요.</li>'
            '<li>그래도 안 되거나 설정 프로그램이 필요하면 이 페이지의 공식 버튼으로 받아요.</li></ul></section>')


def page(k):
    c = C[k]
    nm = short(c)
    path = f'/driver/{k}.html'
    cr, crld = kr.crumb([(f'{nm} 드라이버', '')])
    su, st, ss = c['site']
    tools = ''.join(
        f'<li class="hpm"><h3>{E(t)}</h3><p class="fi">{d}</p><div class="bt">{kr.dl(u, bt, bs, i > 0)}</div></li>'
        for i, (t, d, u, bt, bs) in enumerate(c['tools']))
    first = c['tools'][0] if c['tools'] else None
    steps = '<ol class="big-n">' + ''.join(f'<li>{s}</li>' for s in c['steps']) + '</ol>'
    qa = list(c['qa']) + [
        (f'{nm} ' + ('설치 파일은' if c['kind'] == 'runtime' else '드라이버는') + ' 어디서 받아야 안전해요?', f'{nm} 공식 사이트·공식 프로그램이나 Windows 업데이트에서 받으세요. 광고에 나오는 \'드라이버 자동 설치\' 프로그램이나 블로그에 올라온 파일은 쓰지 마세요.'),
    ] + ([] if c['kind'] == 'runtime' else [('내 제품 모델을 모르겠어요.', c['serial'].replace('<b>', '').replace('</b>', ''))]) + [

        ('파일은 어디서 받아지나요?', '모든 버튼은 제조사 공식 사이트로 연결돼요. 홍라이프 도구는 파일을 올리지 않아요.')]
    fq, fqld = cu.faq(qa)
    title_lines = c['lines'].replace('·', ', ')
    main = (kr.HP_CSS + MT_CSS + f'<header class="top hub">{cr}<h1>' + (E(c['h1']) if c.get('h1') else f'{E(c["name"])} 드라이버 다운로드·설치 방법 — {E(title_lines)}') + '</h1>'
            '<p class="lead">' + (E(c['lead']) if c.get('lead') else f'{E(nm)} {E(KIND_KO[c["kind"]])} 드라이버를 공식 사이트에서 받는 곳과 설치 순서를 처음 하는 분도 따라 할 수 있게 정리했어요.') + '</p>'
            f'<p class="cu-ans">{c["ans"]}</p>'
            + (kr.dl(first[2], first[3], first[4]) if first else ('<a class="dl3d" href="#models"><span class="tx"><b>내 모델 드라이버 바로 받기 ↓</b><small>모델별 설치 파일 표로 이동</small></span></a>' if k in MODELS else kr.dl(su, st, ss)))
            + '<ul class="dr-toc">' + ('<li><a href="#tools">바로 받기</a></li>' if tools else '') + (f'<li><a href="#models">{MH.get(k, ("모델별 바로 받기",))[0]}</a></li>' if k in MODELS else '') + '<li><a href="#steps">설치 순서</a></li>' + (f'<li><a href="#model">{E(c.get("model_toc", "모델 찾기"))}</a></li>') + '<li><a href="#win">' + ('Windows 업데이트' if c['kind'] == 'runtime' else '윈도우 자동 설치') + '</a></li></ul></header>'
            + (f'<section class="card dr-sec" id="tools"><h2>설치 파일 바로 받기</h2><ul class="hpl">{tools}</ul></section>' if tools else '')
            + model_table(k)
            + f'<section class="card dr-sec" id="steps"><h2>{E(nm)} ' + ('' if c['kind'] == 'runtime' else '드라이버 ') + f'설치 순서 (아주 쉽게)</h2>{steps}' + kr.dl(su, st, ss, bool(first)) + '</section>'
            + f'<section class="card dr-sec" id="model"><h2>' + E(c.get('model_h2', '내 제품 모델명 찾기')) + f'</h2><ul class="cu-chk"><li>{c["serial"]}</li>'
              + ('' if c['kind'] == 'runtime' else '<li>모델명은 영어·숫자를 <b>한 글자도 빼지 말고</b> 그대로 검색하세요. 비슷한 이름의 다른 모델 드라이버는 안 맞을 수 있어요.</li>') + '</ul></section>'
            + win_sec(c['kind'])
            + '<section class="card"><h2>가짜 드라이버 사이트 조심하기</h2><p class="dr-warn">검색 광고의 \'드라이버 자동 설치\' 프로그램이나 블로그에 올라온 설치 파일은 받지 마세요. 원치 않는 프로그램이 함께 깔릴 수 있어요. <b>제조사 공식 사이트</b>나 <b>Windows 업데이트</b>가 가장 안전해요.</p></section>'
            + fq
            + f'<section class="card"><h2>출처와 안내</h2><p class="cu-src">출처: {E(c["src"])} · 확인 {CHK}.<br>'
              '홍라이프 도구는 드라이버 파일을 직접 올리지 않아요. 모든 다운로드는 제조사 공식 사이트에서 이루어져요. 사이트 화면·메뉴 이름은 제조사 사정에 따라 바뀔 수 있어요.</p></section>'
            + kr.REL)
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": f'{nm} 드라이버 설치 방법',
             "step": [{"@type": "HowToStep", "position": i + 1, "text": re.sub('<[^>]+>', '', s).replace('&amp;', '&')} for i, s in enumerate(c['steps'])]}
    ld = [crld, fqld, howto]
    kr.write(path, f'{nm} 드라이버 다운로드 — {c["lines"]} 드라이버 설치 방법 (공식) | 홍라이프 도구',
             f'{c["name"]}({c["en"]}) {c["lines"]} 드라이버를 공식 사이트에서 받는 곳과 설치 순서를 쉽게 정리했어요. 모델명 찾는 법, 윈도우 자동 설치, 자주 묻는 질문까지.',
             main, ld)
    return path


def page_en(k):
    c = C[k]
    path = f'/en/driver/{k}.html'
    cr, crld = en.crumb([(c['en'], '')])
    tools = ''.join(f'<li class="hpm"><h3>{E(t.split(" (")[0])}</h3><div class="bt">{en.dl(u.replace("/ko-kr/", "/en-us/").replace("/kr/", "/"), "Download", "Official", i > 0)}</div></li>'
                    for i, (t, d, u, bt, bs) in enumerate(c['tools']))
    qa = [('Where do files come from?', f'From {c["en"]}\'s official website. HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>{E(c["en"])} Driver Download — Official Sources</h1>'
            f'<p class="lead">Where to download official {E(c["en"])} drivers and software, with easy install steps.</p></header>'
            + (f'<section class="card dr-sec"><h2>Official tools</h2><ul class="hpl">{tools}</ul></section>' if tools else '')
            + f'<section class="card dr-sec"><h2>Drivers by model</h2>{en.dl(c["site_en"], c["en"] + " support", "Search by model name")}</section>'
            + en.easy_pc(c['en']) + en.WIN_PC + fq
            + f'<section class="card"><h2>Sources</h2><p class="cu-src">Sources: {E(c["en"])} official support · checked {CHK_EN}. HongLife Tools does not host driver files.</p></section>'
            + en.REL)
    en.write(path, f'{c["en"]} Driver Download — Official Sources | HongLife Tools',
             f'Where to download official {c["en"]} drivers and software, with easy install steps.', main, [crld, fqld])
    return path


# 등록용 목록 (driver_pages / driver_en / patch_site 에서 가져다 씀)
def rel_ko():
    return ''.join(f'<li><a href="/driver/{k}.html"><b>{E(short(C[k]))}</b><span>{E(C[k]["sub"])}</span></a></li>' for k in ORDER)


def hub_ko():
    return ''.join(f'<li><a href="/driver/{k}.html"><b>{E(short(C[k]))}</b><span>{E(C[k]["lines"])}</span><em>공식 다운로드 ›</em></a></li>' for k in ORDER)


def en_items():
    return [(k, C[k]['en'], 'Official drivers & software') for k in ORDER]


def moved():
    return [('driver', f'/driver/{k}.html', f'{short(C[k])} 드라이버 다운로드', C[k]['lines'] + ' 공식 다운로드·설치 방법', C[k]['kw'], '드라이버') for k in ORDER]


if __name__ == '__main__':
    for k in C:
        print(page(k), page_en(k))
