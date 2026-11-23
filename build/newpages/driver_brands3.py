"""드라이버 회사 추가 2차 (2026-11-23) — 설치 파일 바로 받기 위주.
파일 주소는 각 회사 공식 서버 주소(Windows 패키지 관리자 winget 공식 목록에 등록된 설치 주소)로 확인함.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import driver_brands2 as b

b.KIND_KO.update({'storage': 'SSD·저장장치', 'audio': '헤드셋·오디오', 'phone': '휴대폰 PC 연결'})

N = {
    'steelseries': dict(
        name='스틸시리즈', en='SteelSeries', kind='periph', lines='게이밍 마우스·키보드·헤드셋(Arctis)',
        ans='스틸시리즈 마우스·키보드·Arctis 헤드셋은 <b>SteelSeries GG</b>(무료) 하나로 설정·펌웨어 업데이트를 해요. 아래 <b>[SteelSeries GG 바로 받기]</b>를 누르면 스틸시리즈 서버에서 설치 파일이 바로 받아져요.',
        tools=[('SteelSeries GG 124.0.0', '스틸시리즈 기기 설정(Engine)·헤드셋 음향(Sonar)·펌웨어 업데이트를 하는 공식 프로그램이에요. Windows 10/11 64비트. 2026-11-17 배포.',
                'https://engine.steelseriescdn.com/SteelSeriesGG124.0.0Setup.exe', 'SteelSeries GG 바로 받기', '스틸시리즈 서버 · .exe · 124.0.0')],
        site=('https://steelseries.com/gg', 'SteelSeries GG 공식 페이지', '최신판 안내'),
        site_en='https://steelseries.com/gg',
        steps=['위 버튼으로 설치 파일을 받아 실행해요.', '기기를 USB로 연결하면 GG의 <b>Engine</b> 탭에 나타나요.', '업데이트 알림이 있으면 펌웨어를 업데이트해요(중간에 뽑지 마세요).'],
        serial='기기 바닥·케이블 쪽 스티커에 모델명이 있어요. GG의 Engine 화면에도 기기 이름이 나와요.',
        qa=[('SteelSeries Engine은요?', '지금은 SteelSeries GG 안의 Engine 탭으로 들어갔어요. GG를 설치하면 돼요.')],
        src='SteelSeries GG 공식 배포 파일', kw='스틸시리즈 드라이버 SteelSeries 드라이버 SteelSeries GG 다운로드 스틸시리즈 엔진 Arctis 드라이버 소나',
        sub='GG 마우스·헤드셋'),
    'corsair': dict(
        name='커세어', en='Corsair', kind='periph', lines='게이밍 키보드·마우스·헤드셋·RGB 팬·쿨러',
        ans='커세어 키보드·마우스·헤드셋·RGB 팬·수랭 쿨러는 <b>iCUE 5</b>(무료)로 조명·속도·펌웨어를 관리해요. 아래 버튼을 누르면 커세어 서버에서 설치 파일이 바로 받아져요.',
        tools=[('Corsair iCUE 5', '커세어 기기 조명·매크로·팬 속도·펌웨어 관리 공식 프로그램이에요. Windows 10/11 64비트.',
                'https://www3.corsair.com/software/CUE_V5/public/modules/windows/installer/Install%20iCUE.exe', 'iCUE 바로 받기', '커세어 서버 · .exe · 최신판')],
        site=('https://www.corsair.com/kr/ko/s/downloads', '커세어 다운로드 페이지', '제품별 소프트웨어'),
        site_en='https://www.corsair.com/us/en/s/downloads',
        steps=['위 버튼으로 iCUE 설치 파일을 받아 실행해요(설치 중 필요한 파일을 추가로 받아요).', '설치 후 다시 시작하고 iCUE를 열면 연결된 기기가 보여요.', '기기를 누르고 설정 → <b>업데이트</b>로 펌웨어를 올려요.'],
        serial='기기 바닥·박스의 모델명(예: K70, M65, HS80)을 보세요.',
        qa=[('iCUE 4와 5가 같이 깔려도 되나요?', 'iCUE 5를 설치하면 이전 버전은 바뀌어요. 한 가지만 쓰세요.')],
        src='Corsair iCUE 공식 배포 파일', kw='커세어 드라이버 Corsair 드라이버 iCUE 다운로드 커세어 iCUE 커세어 키보드 드라이버 커세어 헤드셋 드라이버',
        sub='iCUE RGB·키보드'),
    'hyperx': dict(
        name='하이퍼X', en='HyperX', kind='periph', lines='게이밍 헤드셋·마우스·키보드',
        ans='하이퍼X 헤드셋·마우스·키보드 설정 프로그램 <b>NGENUITY</b>는 <b>Microsoft Store</b>에서만 배포돼요. 아래 버튼을 누르면 스토어의 NGENUITY 페이지가 열리고 <b>[받기]</b>만 누르면 돼요. 대부분의 하이퍼X 헤드셋은 프로그램 없이도 꽂기만 하면 소리가 나요.',
        tools=[('HyperX NGENUITY (Microsoft Store)', '하이퍼X 기기의 조명·매크로·DPI·펌웨어 업데이트 공식 프로그램이에요.',
                b.MS.format('9P1TBXR6QDCX') if hasattr(b, 'MS') else 'https://apps.microsoft.com/detail/9P1TBXR6QDCX?hl=ko-kr&gl=KR', 'NGENUITY 받기', 'Microsoft Store · 무료')],
        site=('https://hyperx.com/pages/ngenuity', 'HyperX NGENUITY 공식 페이지', '지원 기기 확인'),
        site_en='https://hyperx.com/pages/ngenuity',
        steps=['위 버튼을 누르면 Microsoft Store가 열려요. <b>[받기]</b>를 눌러 설치해요.', '하이퍼X 기기를 연결하고 NGENUITY를 열어요.', '기기를 누르면 조명·버튼·펌웨어 업데이트 메뉴가 나와요.'],
        serial='헤드셋 케이블·동글이나 마우스 바닥에 모델명(예: Cloud III, Pulsefire Haste)이 있어요.',
        qa=[('스토어 없이 받을 수 있나요?', '하이퍼X는 새 NGENUITY를 Microsoft Store로만 배포해요. 회사 PC에서 스토어가 막혀 있으면 전산 담당자에게 문의하세요.')],
        src='Microsoft Store HyperX NGENUITY, HyperX 공식 NGENUITY 안내', kw='하이퍼X 드라이버 HyperX 드라이버 NGENUITY 다운로드 엔제뉴이티 하이퍼엑스 헤드셋 드라이버 클라우드 드라이버',
        sub='NGENUITY 헤드셋'),
    'creative': dict(
        name='크리에이티브', en='Creative', kind='audio', lines='사운드 블라스터·스피커·헤드셋',
        ans='크리에이티브 사운드 블라스터(USB 사운드카드)·스피커·헤드셋은 <b>Creative App</b>으로, 일부 사운드 블라스터 모델은 <b>Sound Blaster Command</b>로 설정해요. 두 프로그램 모두 아래 버튼을 누르면 크리에이티브 서버에서 바로 받아져요.',
        tools=[('Creative App', '최신 크리에이티브 제품(사운드 블라스터 G·X 시리즈, Pebble, Zen 등)의 음향 설정·펌웨어 업데이트 프로그램이에요.',
                'https://files.creative.com/creative/bin/apps/swureleases/win/creativeapp/release/CreativeAppSetup_1.24.05.01.exe', 'Creative App 바로 받기', '크리에이티브 서버 · .exe · 1.24.05'),
               ('Sound Blaster Command', 'Sound BlasterX G6·AE-5 같은 사운드 블라스터 제품용 프로그램이에요.',
                'https://files.creative.com/creative/bin/apps/swureleases/win/sbcommand/release/CreativeSBCommandSetup_3.5.10.00.exe', 'SB Command 바로 받기', '크리에이티브 서버 · .exe · 3.5.10')],
        site=('https://support.creative.com/Downloads/', '크리에이티브 지원 다운로드', '제품별 드라이버'),
        site_en='https://support.creative.com/Downloads/',
        steps=['내 제품이 어떤 프로그램을 쓰는지 상자나 설명서를 확인해요(모르면 Creative App부터).', '위 버튼으로 받아 실행해 설치해요.', '제품을 연결하고 프로그램에서 음향·펌웨어를 설정해요.'],
        serial='제품 바닥·뒷면 스티커의 모델명(예: SB1770)을 보세요.',
        qa=[('PCIe 사운드카드 드라이버는요?', '크리에이티브 지원 다운로드에서 모델명으로 드라이버를 받아요.')],
        src='Creative 공식 배포 파일', kw='크리에이티브 드라이버 Creative 드라이버 사운드블라스터 드라이버 Sound Blaster Command Creative App G6 드라이버',
        sub='사운드 블라스터'),
    'jabra': dict(
        name='자브라', en='Jabra', kind='audio', lines='업무용 헤드셋·스피커폰·이어버드',
        ans='자브라 헤드셋·스피커폰은 <b>Jabra Direct</b>(무료)로 펌웨어 업데이트와 설정을 해요. 아래 버튼을 누르면 자브라 서버에서 설치 파일이 바로 받아져요.',
        tools=[('Jabra Direct 8.4', '자브라 기기 펌웨어 업데이트·통화 설정 공식 프로그램이에요. Windows 10/11 64비트. 2026-11-04 배포.',
                'https://jabraxpressonlineprdstor.blob.core.windows.net/jdo/JabraDirectSetup.exe', 'Jabra Direct 바로 받기', '자브라 서버 · .exe · 8.4')],
        site=('https://www.jabra.com/software-and-services/jabra-direct', 'Jabra Direct 공식 페이지', '지원 기기'),
        site_en='https://www.jabra.com/software-and-services/jabra-direct',
        steps=['위 버튼으로 받아 실행해요.', '헤드셋(또는 USB 동글)을 연결해요.', 'Jabra Direct에 업데이트 표시가 있으면 눌러서 펌웨어를 올려요.'],
        serial='헤드셋 안쪽이나 동글에 모델명(예: Evolve2 65)이 있어요.',
        qa=[('줌·팀즈에서 버튼이 안 먹어요.', 'Jabra Direct 설정에서 사용하는 통화 프로그램(소프트폰)을 지정하세요.')],
        src='Jabra Direct 공식 배포 파일', kw='자브라 드라이버 Jabra 드라이버 Jabra Direct 다운로드 자브라 헤드셋 펌웨어 Evolve2',
        sub='Jabra Direct 헤드셋'),
    'epos': dict(
        name='에포스 (젠하이저 게이밍·업무용)', short='에포스', h1='에포스(옛 젠하이저 업무용·게이밍) 헤드셋 프로그램 바로 받기 — EPOS Connect', en='EPOS', kind='audio', lines='업무용·게이밍 헤드셋(옛 젠하이저 커뮤니케이션)',
        ans='에포스(옛 젠하이저 업무용·게이밍 헤드셋) 제품은 <b>EPOS Connect</b>로 펌웨어 업데이트와 설정을 해요. 아래 버튼을 누르면 에포스 서버에서 바로 받아져요.',
        tools=[('EPOS Connect 8.7', '에포스 헤드셋 펌웨어 업데이트·설정 공식 프로그램이에요. 2026-10-02 배포.',
                'https://www.eposaudio.com/globalassets/abc---master-blocks-uk-fallback/epos-build/epos/files/software/epos-connect/epos-connect-8.7.0/eposconnect_8.7.0.52713.exe', 'EPOS Connect 바로 받기', '에포스 서버 · .exe · 8.7.0')],
        site=('https://www.eposaudio.com/', '에포스 공식 사이트', '지원 → 소프트웨어'),
        site_en='https://www.eposaudio.com/',
        steps=['위 버튼으로 받아 실행해요.', '헤드셋을 연결하고 EPOS Connect를 열어요.', '업데이트가 있으면 눌러 펌웨어를 올려요.'],
        serial='헤드셋 밴드 안쪽이나 동글의 모델명을 보세요.',
        qa=[('젠하이저 게이밍 헤드셋(GSP 시리즈)도 되나요?', '젠하이저 게이밍·업무용 라인은 에포스로 옮겨 갔어요. EPOS 프로그램을 쓰세요.')],
        src='EPOS Connect 공식 배포 파일', kw='에포스 드라이버 EPOS Connect 젠하이저 헤드셋 드라이버 젠하이저 게이밍 드라이버 GSP 드라이버',
        sub='EPOS Connect 헤드셋'),
    'mskb': dict(
        name='마이크로소프트 마우스·키보드', short='MS 마우스·키보드', h1='마이크로소프트 마우스 및 키보드 센터 바로 받기 — MS 마우스·키보드 버튼 설정', en='Microsoft Mouse and Keyboard', kind='periph', lines='마이크로소프트 마우스·키보드(Ergonomic·Sculpt 등)',
        ans='마이크로소프트 마우스·키보드의 버튼 설정은 <b>마우스 및 키보드 센터</b>(Mouse and Keyboard Center)로 해요. 아래 버튼을 누르면 Microsoft 서버에서 64비트 설치 파일이 바로 받아져요.',
        tools=[('마우스 및 키보드 센터 14.41 (64비트)', '마이크로소프트 마우스·키보드 버튼 기능 바꾸기 공식 프로그램이에요.',
                'https://download.microsoft.com/download/c/3/5/c35ae8d6-d607-4095-8eb8-ca1860dc2175/MouseKeyboardCenter_64bit_ENG_14.41.exe', '64비트 바로 받기', 'Microsoft 서버 · .exe · 14.41'),
               ('ARM 노트북용 (스냅드래곤 등)', 'ARM 프로세서 윈도우용 설치 파일이에요.',
                'https://download.microsoft.com/download/c/3/5/c35ae8d6-d607-4095-8eb8-ca1860dc2175/MouseKeyboardCenter_ARM64_ENG_14.41.exe', 'ARM64 바로 받기', 'Microsoft 서버 · .exe')],
        site=('https://www.microsoft.com/ko-kr/download/details.aspx?id=103453', 'Microsoft 다운로드 센터', '마우스 및 키보드 센터'),
        site_en='https://www.microsoft.com/en-us/download/details.aspx?id=103453',
        steps=['위 버튼으로 받아 실행해요(설치 중 한국어로 표시돼요).', '마우스·키보드를 연결하고 프로그램을 열어요.', '버튼을 눌러 원하는 기능을 지정해요.'],
        serial='마우스·키보드 바닥 스티커의 모델명을 보세요.',
        qa=[('프로그램이 내 마우스를 못 찾아요.', '마이크로소프트 제품만 지원해요. 다른 회사 마우스는 그 회사 프로그램을 쓰세요.')],
        src='Microsoft 다운로드 센터 Mouse and Keyboard Center', kw='마이크로소프트 마우스 드라이버 마우스 및 키보드 센터 Mouse and Keyboard Center MS 키보드 드라이버 인텔리포인트',
        sub='마우스 및 키보드 센터'),
    'android': dict(
        name='안드로이드 USB 드라이버 (구글·픽셀·ADB)', short='안드로이드 USB', h1='안드로이드 USB 드라이버·ADB 바로 받기 — 구글 픽셀·안드로이드 폰 PC 연결', lead='구글 공식 안드로이드 USB 드라이버와 ADB(Platform-Tools)를 구글 서버에서 바로 받고, 장치 관리자로 설치하는 순서를 정리했어요.', en='Android USB Driver', kind='phone', lines='구글 픽셀·안드로이드 폰 PC 연결·ADB',
        ans='구글 픽셀 등 안드로이드 폰을 PC에 연결해 <b>ADB</b>(개발자 모드)를 쓰려면 <b>Google USB 드라이버</b>가 필요해요. 사진만 옮길 때는 대부분 드라이버 없이 돼요. <b>삼성 갤럭시</b>는 삼성 USB 드라이버를 쓰세요(삼성 드라이버 페이지).',
        tools=[('Google USB 드라이버 (최신판)', '구글 공식 안드로이드 USB 드라이버예요. 압축을 풀고 장치 관리자에서 드라이버 업데이트 → 내 컴퓨터에서 찾기로 이 폴더를 지정해요.',
                'https://dl.google.com/android/repository/latest_usb_driver_windows.zip', 'USB 드라이버 바로 받기', '구글 서버 · .zip · 최신판'),
               ('Android SDK Platform-Tools (adb·fastboot)', 'ADB·fastboot 명령 도구예요. 압축을 풀면 바로 쓸 수 있어요. 2026-11-19 배포 r37.0.3.',
                'https://dl.google.com/android/repository/platform-tools_r37.0.3-win.zip', 'Platform-Tools 바로 받기', '구글 서버 · .zip · 37.0.3')],
        site=('https://developer.android.com/studio/run/win-usb', '안드로이드 개발자 — Google USB 드라이버', '설치 방법'),
        site_en='https://developer.android.com/studio/run/win-usb',
        steps=['위 버튼으로 USB 드라이버를 받아 압축을 풀어요.', '폰을 USB로 연결하고 <b>Win + X → 장치 관리자</b>를 열어요.', '느낌표가 붙은 Android 기기를 오른쪽 클릭 → <b>드라이버 업데이트 → 내 컴퓨터에서 찾기</b> → 압축 푼 폴더를 지정해요.', 'ADB를 쓰려면 Platform-Tools도 받아 압축을 풀어요.'],
        serial='폰 설정 → 휴대전화 정보에서 모델명을 확인해요.',
        qa=[('갤럭시 폰도 이걸로 되나요?', '삼성 갤럭시는 삼성 USB 드라이버를 쓰는 게 맞아요. 아래 다른 회사 드라이버에서 삼성을 고르세요.'),
            ('사진 옮기는데도 필요해요?', '보통은 필요 없어요. 폰 알림에서 USB 용도를 [파일 전송]으로 바꾸면 돼요.')],
        src='Android Developers Google USB Driver, SDK Platform-Tools', kw='안드로이드 USB 드라이버 구글 USB 드라이버 픽셀 드라이버 ADB 드라이버 adb 다운로드 platform-tools fastboot 드라이버',
        sub='구글 USB·ADB'),
    'elgato': dict(
        name='엘가토', en='Elgato', kind='periph', lines='스트림덱·웹캠·캡처보드',
        ans='엘가토 <b>Stream Deck</b>은 Stream Deck 프로그램, <b>Facecam</b> 웹캠은 <b>Camera Hub</b>로 설정해요. 아래 버튼을 누르면 엘가토 서버에서 설치 파일이 바로 받아져요.',
        tools=[('Stream Deck 7.6.1', '스트림덱 버튼 설정 공식 프로그램이에요. 2026-11-03 배포.',
                'https://edge.elgato.com/egc/windows/sd/Stream_Deck_7.6.1.23033.msi', 'Stream Deck 바로 받기', '엘가토 서버 · .msi · 7.6.1'),
               ('Camera Hub 2.3', 'Facecam 웹캠 화질 설정 프로그램이에요.',
                'https://edge.elgato.com/egc/windows/echw/2.3.0/CameraHub_2.3.0.7295_x64.msi', 'Camera Hub 바로 받기', '엘가토 서버 · .msi · 2.3.0')],
        site=('https://www.elgato.com/kr/ko/s/downloads', '엘가토 다운로드', '제품별 소프트웨어'),
        site_en='https://www.elgato.com/us/en/s/downloads',
        steps=['내 제품에 맞는 프로그램을 위에서 받아요.', '받은 .msi 파일을 실행해 설치해요.', '기기를 연결하고 프로그램을 열어 설정해요.'],
        serial='기기 바닥 스티커의 모델명을 보세요.',
        qa=[('캡처보드 프로그램은요?', '엘가토 다운로드 페이지에서 4K Capture Utility 등 모델에 맞는 프로그램을 받아요.')],
        src='Elgato 공식 배포 파일', kw='엘가토 드라이버 Elgato 드라이버 스트림덱 다운로드 Stream Deck Camera Hub 페이스캠 드라이버',
        sub='스트림덱·웹캠'),
    'ssd': dict(
        name='SSD·하드디스크 관리 프로그램 (크루셜·킹스톤·WD·씨게이트)', short='SSD 관리 프로그램', h1='SSD 관리 프로그램 바로 받기 — 크루셜·킹스톤·WD·씨게이트 펌웨어·수명 확인', lead='SSD·하드디스크 회사별 공식 관리 프로그램(펌웨어 업데이트·상태 검사)을 제조사 서버에서 바로 받을 수 있게 모았어요.', en='SSD Tools', kind='storage', lines='크루셜·킹스톤·WD·씨게이트 SSD·HDD 펌웨어·상태 검사',
        ans='SSD는 드라이버가 따로 필요 없지만 <b>펌웨어 업데이트·수명(상태) 확인</b>은 제조사 프로그램으로 해요. 아래에서 내 SSD 회사를 골라 <b>바로 받기</b>를 누르세요. 삼성 SSD는 <b>삼성 매지션</b>(삼성 드라이버 페이지)을 쓰세요.',
        tools=[('크루셜 Storage Executive 11.11 (Crucial·Micron)', '크루셜 SSD 펌웨어 업데이트·상태 확인·Momentum Cache 프로그램이에요. 64비트.',
                'https://assets.micron.com/adobe/assets/urn:aaid:aem:4f8683ee-4679-4a2e-8f94-522fa19126d2/renditions/original/as/storage-executive-win-64-11-11.zip', 'Storage Executive 받기', '마이크론 서버 · .zip · 11.11'),
               ('킹스톤 SSD Manager 1.5.6.5', '킹스톤 SSD 펌웨어 업데이트·상태 확인 프로그램이에요. 2026-04-08 배포.',
                'https://media.kingston.com/support/downloads/KSM_setup_1.5.6.5.exe', 'SSD Manager 받기', '킹스톤 서버 · .exe · 1.5.6.5'),
               ('WD Kitfox (WD·샌디스크 SSD)', 'WD Dashboard를 잇는 WD SSD 펌웨어·상태 관리 프로그램이에요.',
                'https://downloads.wdc.com/wdapp/wd_kitfox.zip', 'WD Kitfox 받기', 'WD 서버 · .zip · 1.1'),
               ('씨게이트 SeaTools (하드디스크·SSD 검사)', '씨게이트·다른 회사 HDD/SSD 상태를 검사하는 프로그램이에요.',
                'https://www.seagate.com/files/old-support-files/seatools/SeaToolsforWindowsSetup.exe', 'SeaTools 받기', '씨게이트 서버 · .exe')],
        site=('https://www.crucial.kr/support/storage-executive', '크루셜 Storage Executive 안내', '지원 SSD 확인'),
        site_en='https://www.crucial.com/support/storage-executive',
        steps=['내 SSD 회사를 확인해요. <b>Win + X → 디스크 관리</b>나 <b>장치 관리자 → 디스크 드라이브</b>에 모델명이 나와요.', '위에서 그 회사 프로그램을 받아 설치해요.', '프로그램에서 상태(수명)를 보고, 펌웨어 업데이트가 있으면 <b>중요한 파일을 백업한 뒤</b> 진행해요.'],
        serial='장치 관리자 → 디스크 드라이브에서 SSD 모델명(예: CT1000P3PSSD8, SNV2S1000G, WDS100T3X0E)을 확인해요.',
        qa=[('SSD 드라이버를 꼭 깔아야 하나요?', '아니요. 윈도우 기본 드라이버로 충분해요. 펌웨어 업데이트·상태 확인용으로 회사 프로그램을 써요.'),
            ('펌웨어 업데이트 중 꺼지면요?', 'SSD가 고장 날 수 있어요. 노트북은 충전기를 꽂고, 중요한 자료는 미리 백업하세요.')],
        src='Crucial·Kingston·Western Digital·Seagate 공식 배포 파일', kw='SSD 펌웨어 업데이트 크루셜 Storage Executive 킹스톤 SSD Manager WD Dashboard Kitfox 씨게이트 SeaTools SSD 수명 확인 프로그램',
        sub='크루셜·킹스톤·WD'),
}

ORDER = list(N)
b.C.update(N)


def rel_items():
    E = b.E
    return [(k, b.short(N[k]), N[k]['sub'], N[k]['lines'], N[k]['en'], N[k]['kw']) for k in ORDER]


if __name__ == '__main__':
    for k in ORDER:
        print(b.page(k), b.page_en(k))
