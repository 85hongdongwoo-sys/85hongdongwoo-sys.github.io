"""마이크로소프트 런타임·주변기기 페이지 (2026-11-23).
파일 주소: Microsoft 공식 서버(download.microsoft.com, download.visualstudio.microsoft.com, builds.dotnet.microsoft.com).
2026-11-23 응답(200) 확인. .NET 버전은 builds.dotnet.microsoft.com releases.json 최신값.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import driver_brands2 as b

b.KIND_KO.update({'runtime': '런타임', 'periph': '주변기기'})
VS = 'https://download.visualstudio.microsoft.com/download/pr/'
DM = 'https://download.microsoft.com/download/'
DN = 'https://builds.dotnet.microsoft.com/dotnet/WindowsDesktop/'

N = {
    'vcredist': dict(
        name='Visual C++ 재배포 패키지', short='Visual C++ 재배포', en='Microsoft Visual C++ Redistributable', kind='runtime',
        lines='MSVCP140.dll·VCRUNTIME140.dll 오류 해결',
        h1='Visual C++ 재배포 패키지 바로 받기 — MSVCP140.dll·VCRUNTIME140.dll 오류 해결 (2005~2026)',
        lead='게임·프로그램을 켤 때 나오는 dll 없음 오류를 고치는 Microsoft 공식 Visual C++ 런타임을 버전별로 Microsoft 서버에서 바로 받을 수 있게 모았어요.',
        ans='"<b>MSVCP140.dll</b>(또는 VCRUNTIME140.dll, VCRUNTIME140_1.dll)이 없어 코드 실행을 진행할 수 없습니다" 오류는 <b>Visual C++ 2015~2026 재배포 패키지</b>를 설치하면 대부분 해결돼요. 64비트 윈도우라도 <b>x64와 x86을 둘 다</b> 설치하세요(32비트 프로그램도 많아요). 오래된 프로그램이 MSVCR100.dll·MSVCR120.dll 등을 찾으면 아래 표에서 그 버전을 받으세요.',
        tools=[('Visual C++ 2015~2026 (x64) — 64비트 프로그램용', '가장 많이 필요한 최신 통합 런타임이에요. 버전 14.52 · 2026-11-06 배포 · 약 18MB.',
                VS + '78d061c5-9ef3-42ab-98ed-3309d1095dc4/9C02C9ED120F671B900E6B9471D890E3B2414117A7E53F4AE2E855466FA2B7C9/VC_redist.x64.exe', 'x64 바로 받기', 'Microsoft 서버 · VC_redist.x64.exe'),
               ('Visual C++ 2015~2026 (x86) — 32비트 프로그램용', '64비트 윈도우에도 같이 설치하세요. 약 7MB.',
                VS + '78d061c5-9ef3-42ab-98ed-3309d1095dc4/7B0117E6E20E9E349029C000A8A2715A52CF37C15B6BB697B2908E8BC7066CDF/VC_redist.x86.exe', 'x86 바로 받기', 'Microsoft 서버 · VC_redist.x86.exe'),
               ('Visual C++ 2015~2026 (ARM64) — 스냅드래곤 노트북용', 'ARM 프로세서 윈도우용이에요.',
                VS + '78d061c5-9ef3-42ab-98ed-3309d1095dc4/3C81BCF5B06156858362400D7066F65ECE38E8ACCB5E687FC65BEF5735F31FFC/VC_redist.arm64.exe', 'ARM64 바로 받기', 'Microsoft 서버 · VC_redist.arm64.exe')],
        site=('https://learn.microsoft.com/ko-kr/cpp/windows/latest-supported-vc-redist', 'Microsoft Learn — 최신 Visual C++ 재배포 패키지', '공식 안내'),
        site_en='https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist',
        steps=['위에서 <b>x64</b>와 <b>x86</b>을 둘 다 받아요(ARM 노트북은 ARM64도).', '받은 파일을 하나씩 실행해 <b>[동의] → [설치]</b>를 눌러요. 이미 있으면 <b>[복구]</b>를 누르세요.', '다 끝나면 컴퓨터를 다시 시작하고 프로그램을 다시 켜 봐요.', '오류에 <b>MSVCR100·MSVCR110·MSVCR120·MSVCR80·MSVCR90</b>이 나오면 아래 표에서 그 연도 버전을 받아요.'],
        model_h2='오류 메시지로 필요한 버전 찾기', model_toc='오류별 버전',
        serial='오류 창의 dll 이름을 보세요: <b>MSVCP140·VCRUNTIME140·VCRUNTIME140_1 → 2015~2026</b>, MSVCR120·MSVCP120 → 2013, MSVCR110 → 2012, MSVCR100 → 2010, MSVCR90 → 2008, MSVCR80 → 2005.',
        qa=[('64비트 윈도우인데 x86도 깔아야 해요?', '네. 64비트 윈도우에서도 32비트 프로그램이 많아서, 그 프로그램은 x86 런타임을 찾아요. 둘 다 설치해도 충돌하지 않아요.'),
            ('이미 설치돼 있다고 나와요.', '설치 창의 [복구]를 눌러 다시 설치하세요. 파일이 망가진 경우 이걸로 고쳐져요.'),
            ('dll 파일만 따로 받아서 넣으면 안 되나요?', '권하지 않아요. dll 공유 사이트의 파일은 버전이 안 맞거나 악성 코드가 섞일 수 있어요. 공식 재배포 패키지를 설치하세요.')],
        src='Microsoft Learn 최신 Visual C++ 재배포 패키지, Microsoft 다운로드 서버',
        kw='Visual C++ 재배포 패키지 다운로드 vcredist MSVCP140.dll 오류 VCRUNTIME140.dll 없음 VCRUNTIME140_1.dll MSVCR100.dll MSVCR120.dll vc_redist.x64 비주얼 C++ 런타임',
        sub='MSVCP140.dll 오류 해결'),
    'directx': dict(
        name='DirectX 최종 사용자 런타임', short='DirectX 런타임', en='DirectX End-User Runtime', kind='runtime',
        lines='d3dx9_43.dll·XINPUT1_3.dll 오류 해결',
        h1='DirectX 최종 사용자 런타임 바로 받기 — d3dx9_43.dll·XINPUT1_3.dll·xaudio 오류 해결',
        lead='옛날 게임에서 나오는 DirectX dll 없음 오류를 고치는 Microsoft 공식 DirectX 런타임(웹 설치·오프라인 설치)을 Microsoft 서버에서 바로 받을 수 있게 정리했어요.',
        ans='윈도우 10/11에는 DirectX 12가 이미 들어 있지만, 옛날 게임이 쓰는 <b>d3dx9_43.dll·d3dx11_43.dll·XINPUT1_3.dll·xactengine·X3DAudio</b> 같은 파일은 따로 설치해야 해요. 아래 <b>[웹 설치 파일 받기]</b>를 실행하면 빠진 파일만 받아 설치해요. 인터넷이 없는 PC는 <b>오프라인 설치 파일(2010년 6월판)</b>을 쓰세요.',
        tools=[('DirectX 최종 사용자 런타임 웹 설치 관리자', '실행하면 필요한 파일만 인터넷으로 받아 설치해요. 약 290KB. 설치 중 Bing 바 설치 체크는 해제하세요.',
                DM + '1/7/1/1718CCC4-6315-4D8E-9543-8E28A4E18C4C/dxwebsetup.exe', '웹 설치 파일 받기', 'Microsoft 서버 · dxwebsetup.exe'),
               ('DirectX 오프라인 설치 파일 (2010년 6월)', '인터넷 없이 설치할 때 써요. 약 100MB. 실행하면 압축을 풀 폴더를 묻는데, 새 폴더를 만들어 풀고 그 안의 <b>DXSETUP.exe</b>를 실행하세요.',
                DM + '8/4/A/84A35BF1-DAFE-4AE8-82AF-AD2AE20B6B14/directx_Jun2010_redist.exe', '오프라인 설치 파일 받기', 'Microsoft 서버 · 약 100MB'),
               ('XNA Framework 4.0 재배포 (옛 인디 게임용)', '테라리아 옛 버전 등 XNA 게임이 "XNA Framework가 필요" 오류를 낼 때 설치해요.',
                DM + '5/3/A/53A804C8-EC78-43CD-A0F0-2FB4D45603D3/xnafx40_redist.msi', 'XNA 4.0 받기', 'Microsoft 서버 · .msi')],
        site=('https://www.microsoft.com/ko-kr/download/details.aspx?id=35', 'Microsoft 다운로드 센터 — DirectX 런타임', '공식 안내'),
        site_en='https://www.microsoft.com/en-us/download/details.aspx?id=35',
        steps=['위 <b>[웹 설치 파일 받기]</b>로 dxwebsetup.exe를 받아 실행해요.', '<b>[동의함]</b>을 누르고, Bing 바 설치 체크는 해제한 뒤 <b>[다음]</b>을 눌러요.', '필요한 파일을 받아 설치하면 <b>[마침]</b>을 눌러요.', '게임을 다시 켜 봐요. 그래도 안 되면 그래픽 드라이버(엔비디아·AMD·인텔)를 최신으로 바꿔요.'],
        model_h2='오류 메시지로 확인하기', model_toc='오류 확인',
        serial='오류 창에 <b>d3dx9_??.dll, d3dx10_??.dll, d3dx11_??.dll, XINPUT1_3.dll, xactengine, X3DAudio, XAPOFX</b>가 보이면 이 페이지의 DirectX 런타임으로 해결돼요. 내 DirectX 버전은 <b>Win + R → dxdiag</b>로 볼 수 있어요.',
        qa=[('윈도우 11인데 DirectX 12를 따로 받아야 하나요?', '아니요. DirectX 12는 윈도우에 들어 있고 Windows 업데이트로만 갱신돼요. 이 런타임은 옛 게임용 추가 파일이에요.'),
            ('설치했는데 그대로예요.', '게임 폴더 안의 _CommonRedist·DirectX 폴더 설치 파일을 실행하거나, 그래픽 드라이버를 최신으로 바꿔 보세요.')],
        src='Microsoft 다운로드 센터 DirectX End-User Runtime Web Installer·June 2010 Redistributable',
        kw='DirectX 다운로드 다이렉트X 런타임 d3dx9_43.dll 오류 XINPUT1_3.dll 없음 d3dx11_43.dll dxwebsetup DirectX 설치 xactengine X3DAudio XNA Framework',
        sub='d3dx9·XINPUT 오류 해결'),
    'dotnet': dict(
        name='.NET 데스크톱 런타임·.NET Framework', short='.NET 런타임', en='.NET Desktop Runtime', kind='runtime',
        lines='".NET이 필요합니다" 오류 해결',
        h1='.NET 데스크톱 런타임 바로 받기 — ".NET 8/9/10이 필요합니다" 오류 해결·.NET Framework 4.8.1',
        lead='"이 애플리케이션을 실행하려면 .NET을 설치해야 합니다" 창이 뜰 때 필요한 Microsoft 공식 .NET 런타임을 버전별로 Microsoft 서버에서 바로 받을 수 있게 모았어요.',
        ans='프로그램이 "<b>.NET 8(또는 9, 10) 데스크톱 런타임이 필요합니다</b>"라고 하면 그 숫자의 <b>.NET Desktop Runtime</b>을 설치해요. 대부분 PC는 <b>x64</b>를 받으면 돼요. 옛 프로그램이 <b>.NET Framework 4.x</b>를 찾으면 4.8.1을, <b>3.5</b>를 찾으면 윈도우 기능에서 켜요(아래 순서).',
        tools=[('.NET 8 데스크톱 런타임 (x64) — 가장 많이 필요', '장기 지원(LTS) 버전이에요. 8.0.34 · 2026-11-10 배포.',
                DN + '8.0.34/windowsdesktop-runtime-8.0.34-win-x64.exe', '.NET 8 바로 받기', 'Microsoft 서버 · x64 · 8.0.34'),
               ('.NET 10 데스크톱 런타임 (x64)', '최신 장기 지원(LTS) 버전이에요. 10.0.15 · 2026-11-10 배포.',
                DN + '10.0.15/windowsdesktop-runtime-10.0.15-win-x64.exe', '.NET 10 바로 받기', 'Microsoft 서버 · x64 · 10.0.15'),
               ('.NET Framework 4.8.1 (오프라인 설치)', '옛 프로그램이 .NET Framework 4.x를 찾을 때 설치해요. 윈도우 11에는 이미 들어 있어요. 약 74MB.',
                DM + '4/b/2/cd00d4ed-ebdd-49ee-8a33-eabc3d1030e3/NDP481-x86-x64-AllOS-ENU.exe', '.NET Framework 4.8.1 받기', 'Microsoft 서버 · 오프라인 설치'),
               ('Microsoft Edge WebView2 런타임', '"WebView2 런타임이 필요합니다" 오류가 날 때 설치해요. 작은 설치 파일이 최신판을 받아 설치해요.',
                'https://go.microsoft.com/fwlink/p/?LinkId=2124703', 'WebView2 받기', 'Microsoft 공식 · 최신판')],
        site=('https://dotnet.microsoft.com/ko-kr/download/dotnet', 'Microsoft .NET 다운로드', '버전별 전체 목록'),
        site_en='https://dotnet.microsoft.com/en-us/download/dotnet',
        steps=['오류 창에 나온 <b>.NET 숫자</b>(8, 9, 10)와 <b>Desktop</b>(데스크톱) 여부를 확인해요.', '아래 표에서 그 숫자의 <b>x64</b>를 받아 설치해요(ARM 노트북은 ARM64, 32비트 프로그램이면 x86).', '<b>.NET Framework 3.5</b>를 찾으면: <b>Win + R → optionalfeatures</b> → <b>.NET Framework 3.5</b> 체크 → [확인] → <b>Windows 업데이트에서 파일 다운로드</b>.', '설치 후 프로그램을 다시 켜요.'],
        model_h2='오류 창으로 필요한 버전 찾기', model_toc='오류별 버전',
        serial='오류 창의 문구를 보세요: "<b>.NET Desktop Runtime 8</b>" → 아래 표의 .NET 8 데스크톱, "<b>.NET Framework 4.x</b>" → 4.8.1, "<b>.NET Framework 3.5</b>" → 윈도우 기능에서 켜기. 설치된 버전은 명령 프롬프트에서 <b>dotnet --list-runtimes</b>로 볼 수 있어요.',
        qa=[('.NET 8과 10을 둘 다 깔아도 돼요?', '네. 버전마다 따로 설치되고 서로 충돌하지 않아요. 프로그램이 요구하는 숫자를 설치하면 돼요.'),
            ('데스크톱 런타임과 그냥 런타임은 뭐가 달라요?', '창이 있는 윈도우 프로그램은 데스크톱 런타임이 필요해요. 데스크톱 런타임에는 일반 런타임도 들어 있어요.')],
        src='Microsoft .NET 릴리스 정보(releases.json), Microsoft 다운로드 서버',
        kw='.NET 다운로드 닷넷 런타임 .NET 8 데스크톱 런타임 .NET Desktop Runtime .NET Framework 4.8.1 .NET Framework 3.5 설치 WebView2 런타임 이 애플리케이션을 실행하려면 .NET',
        sub='.NET 필요 오류 해결'),
    'xbox': dict(
        name='Xbox 컨트롤러 (PC 연결)', short='Xbox 컨트롤러', en='Xbox Controller', kind='periph',
        lines='엑스박스 패드 PC 연결·무선 어댑터·펌웨어',
        h1='Xbox 컨트롤러 PC 드라이버·연결 방법 — 엑스박스 패드 블루투스·무선 어댑터·펌웨어 업데이트',
        lead='엑스박스 컨트롤러(패드)를 윈도우 PC에 USB·블루투스·무선 어댑터로 연결하는 방법과 펌웨어 업데이트 프로그램을 정리했어요.',
        ans='Xbox 컨트롤러 드라이버는 <b>윈도우 10/11에 이미 들어 있어서</b> USB-C 케이블로 꽂으면 바로 돼요. 블루투스는 <b>Xbox 버튼 + 연결 버튼을 3초</b> 눌러 깜빡일 때 PC에서 추가해요. 버튼 설정·<b>펌웨어 업데이트</b>는 <b>Xbox 액세서리</b> 앱(Microsoft Store)으로 해요.',
        tools=[('Xbox 액세서리 앱 (Microsoft Store)', '컨트롤러 펌웨어 업데이트·버튼 바꾸기·진동 설정 공식 앱이에요.',
                'https://apps.microsoft.com/detail/9NBLGGH30XJ3?hl=ko-kr&gl=KR', 'Xbox 액세서리 받기', 'Microsoft Store · 무료')],
        site=('https://support.xbox.com/ko-KR/help/hardware-network/controller/connect-xbox-wireless-controller-to-pc', 'Xbox 지원 — PC에 컨트롤러 연결', '공식 안내'),
        site_en='https://support.xbox.com/en-US/help/hardware-network/controller/connect-xbox-wireless-controller-to-pc',
        steps=['<b>유선</b>: USB-C(옛 모델은 마이크로 USB) 케이블로 PC에 꽂으면 바로 인식돼요.', '<b>블루투스</b>: 컨트롤러 <b>Xbox 버튼</b>을 켠 뒤 위쪽 <b>연결 버튼</b>을 3초 눌러 빠르게 깜빡이면, PC <b>설정 → Bluetooth 및 장치 → 장치 추가 → Bluetooth</b>에서 Xbox Wireless Controller를 골라요.', '<b>무선 어댑터</b>: 어댑터를 USB에 꽂고 어댑터 버튼 → 컨트롤러 연결 버튼을 차례로 눌러요(드라이버는 Windows 업데이트로 자동 설치).', '<b>펌웨어</b>: 위 Xbox 액세서리 앱에서 컨트롤러를 고르고 <b>…→ 업데이트</b>를 눌러요.'],
        model_h2='내 컨트롤러 종류 확인', model_toc='종류 확인',
        serial='배터리 칸 안쪽 스티커에 모델 번호가 있어요. <b>1914</b>(시리즈 X|S, USB-C), <b>1708</b>(블루투스 지원 Xbox One), <b>1697·1537</b>(블루투스 없음 → 유선이나 무선 어댑터만).',
        qa=[('블루투스 목록에 안 나와요.', '모델 1697·1537은 블루투스가 없어요. 유선이나 Xbox 무선 어댑터를 쓰세요. 블루투스 모델이면 Xbox 액세서리 앱으로 펌웨어를 먼저 업데이트하세요.'),
            ('스팀 게임에서 버튼이 이상해요.', '스팀 → 설정 → 컨트롤러에서 [Xbox 확장 기능 지원]을 켜거나 게임별 컨트롤러 설정을 기본값으로 바꿔 보세요.')],
        src='Xbox 지원 — Windows PC에 Xbox 무선 컨트롤러 연결, Microsoft Store Xbox 액세서리',
        kw='엑스박스 컨트롤러 PC 연결 Xbox 컨트롤러 드라이버 엑박패드 블루투스 연결 Xbox 무선 어댑터 드라이버 Xbox 액세서리 앱 컨트롤러 펌웨어 업데이트',
        sub='엑박 패드 PC 연결'),
}

b.MODELS['vcredist'] = [
    ('2015~2026 (14.x) — MSVCP140, VCRUNTIME140', '64비트 x64', N['vcredist']['tools'][0][2]),
    ('2015~2026 (14.x) — MSVCP140, VCRUNTIME140', '32비트 x86', N['vcredist']['tools'][1][2]),
    ('2013 (12.0) — MSVCR120, MSVCP120', '64비트 x64', VS + '10912041/cee5d6bca2ddbcd039da727bf4acb48a/vcredist_x64.exe'),
    ('2013 (12.0) — MSVCR120, MSVCP120', '32비트 x86', VS + '10912113/5da66ddebb0ad32ebd4b922fd82e8e25/vcredist_x86.exe'),
    ('2012 (11.0) — MSVCR110, MSVCP110', '64비트 x64', DM + '1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x64.exe'),
    ('2012 (11.0) — MSVCR110, MSVCP110', '32비트 x86', DM + '1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe'),
    ('2010 (10.0) — MSVCR100, MSVCP100', '64비트 x64', DM + '1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x64.exe'),
    ('2010 (10.0) — MSVCR100, MSVCP100', '32비트 x86', DM + '1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe'),
    ('2008 (9.0) — MSVCR90', '64비트 x64', DM + '5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x64.exe'),
    ('2008 (9.0) — MSVCR90', '32비트 x86', DM + '5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe'),
    ('2005 (8.0) — MSVCR80', '64비트 x64', DM + '1/1/3/1131962C-70D7-41B8-B093-7B215D192619/vcredist_x64.EXE'),
    ('2005 (8.0) — MSVCR80', '32비트 x86', DM + '8/B/4/8B42259F-5D70-43F4-AC2E-4B208FD8D66A/vcredist_x86.EXE'),
]
b.MH['vcredist'] = ('버전별 바로 받기 (2005~2026)', '버전 · 오류 dll', '윈도우', 'dll 이름', 'MSVCR100', '버튼을 누르면 Microsoft 서버에서 설치 파일이 바로 받아져요. 오류 창의 dll 이름을 아래 칸에 입력하면 맞는 줄만 남아요.')
b.MODELS['dotnet'] = [
    ('.NET 10 데스크톱 런타임 10.0.15', '64비트 x64', DN + '10.0.15/windowsdesktop-runtime-10.0.15-win-x64.exe'),
    ('.NET 10 데스크톱 런타임 10.0.15', '32비트 x86', DN + '10.0.15/windowsdesktop-runtime-10.0.15-win-x86.exe'),
    ('.NET 10 데스크톱 런타임 10.0.15', 'ARM64', DN + '10.0.15/windowsdesktop-runtime-10.0.15-win-arm64.exe'),
    ('.NET 9 데스크톱 런타임 9.0.23', '64비트 x64', DN + '9.0.23/windowsdesktop-runtime-9.0.23-win-x64.exe'),
    ('.NET 9 데스크톱 런타임 9.0.23', '32비트 x86', DN + '9.0.23/windowsdesktop-runtime-9.0.23-win-x86.exe'),
    ('.NET 9 데스크톱 런타임 9.0.23', 'ARM64', DN + '9.0.23/windowsdesktop-runtime-9.0.23-win-arm64.exe'),
    ('.NET 8 데스크톱 런타임 8.0.34', '64비트 x64', DN + '8.0.34/windowsdesktop-runtime-8.0.34-win-x64.exe'),
    ('.NET 8 데스크톱 런타임 8.0.34', '32비트 x86', DN + '8.0.34/windowsdesktop-runtime-8.0.34-win-x86.exe'),
    ('.NET 8 데스크톱 런타임 8.0.34', 'ARM64', DN + '8.0.34/windowsdesktop-runtime-8.0.34-win-arm64.exe'),
    ('.NET Framework 4.8.1 (4.x 전체 대체)', 'x64·x86·ARM64', DM + '4/b/2/cd00d4ed-ebdd-49ee-8a33-eabc3d1030e3/NDP481-x86-x64-AllOS-ENU.exe'),
]
b.MH['dotnet'] = ('버전별 바로 받기', '버전', '윈도우', '버전 숫자', '8', '버튼을 누르면 Microsoft 서버에서 설치 파일이 바로 받아져요. 오류 창의 .NET 숫자를 입력하면 맞는 줄만 남아요.')

ORDER = list(N)
b.C.update(N)

if __name__ == '__main__':
    for k in ORDER:
        print(b.page(k), b.page_en(k))
