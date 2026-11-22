"""마이크로소프트 서피스(Surface) 드라이버·펌웨어 페이지 — /driver/surface.html, /en/driver/surface.html
출처(2026-11-22 확인): Microsoft 지원 'Surface용 드라이버 및 펌웨어 다운로드'와 제품군별 하위 페이지(모델 → 다운로드 센터 id),
Microsoft 다운로드 센터 각 모델 페이지의 .msi 파일 (data/surface_models.json)
파일 이름의 윈도우 빌드 번호(예: Win11_22631)는 '그 빌드 이상'에서 설치하는 파일이다(MS 안내).
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
import driver_en as en
import driver_more as dm

E = cu.E
SF = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'surface_models.json'), encoding='utf-8'))
DLB = 'https://download.microsoft.com/download/'
DET = 'https://www.microsoft.com/download/details.aspx?id='
GUIDE = 'https://support.microsoft.com/ko-kr/surface/drivers-firmware/download-drivers-and-firmware-for-surface'
FAM = {'pro': 'Surface Pro', 'laptop': 'Surface Laptop', 'go': 'Surface Go', 'laptop-go': 'Surface Laptop Go', 'laptop-studio': 'Surface Laptop Studio',
       'book': 'Surface Book', 'studio': 'Surface Studio', '3': 'Surface 3', 'dock': 'Surface 도크'}
FAM_EN = {**FAM, 'dock': 'Surface Dock'}
WIN11 = {'22000': '21H2', '22621': '22H2', '22631': '23H2', '26100': '24H2', '26200': '25H2'}


def label(fn, lang='ko'):
    m = re.search(r'_(Win1[01])_(?:x64_)?(\d{5})', fn)
    if not m:
        return ('설치 파일', 'Install file') if lang == 'ko' else ('Install file', 'Install file')
    w, b = m.group(1), m.group(2)
    ver = WIN11.get(b) if w == 'Win11' else {'19045': '22H2', '19044': '21H2', '19042': '20H2', '19041': '2004', '18362': '1903', '17763': '1809'}.get(b)
    if lang == 'ko':
        return (f'윈도우 {w[3:]}용', f'빌드 {b}' + (f'({ver})' if ver else '') + ' 이상 · .msi')
    return (f'Windows {w[3:]}', f'build {b}' + (f' ({ver})' if ver else '') + '+ · .msi')


def mid(i):
    return 'sf-' + i


def cards(lang='ko'):
    groups = {}
    for fam, name, i in SF['models']:
        groups.setdefault(fam, []).append((name, i))
    out = []
    for gi, (fam, ms) in enumerate((f, groups[f]) for f in FAM if f in groups):
        rows = []
        for name, i in ms:
            files = [] if i == '101317' else SF['msi'].get(i, [])
            btns = ''
            for k, f in enumerate(files):
                t, s = label(f.split('/')[-1], lang)
                btns += (f'<a class="mb{" s" if k else ""}" href="{E(DLB + f)}" rel="nofollow"><b>{E(t)}</b>'
                         f'<small>{E(s)} · {"누르면 바로 다운로드" if lang == "ko" else "direct download"}</small></a>')
            off = (f'<a class="of" href="{DET + i}" target="_blank" rel="noopener nofollow">'
                   + ('Microsoft 다운로드 센터 (다른 윈도우 버전 파일) ↗' if lang == 'ko' else 'Microsoft Download Center (other files) ↗') + '</a>')
            if not btns:
                btns = ''
            nm = name if lang == 'ko' else name
            rows.append(f'<li class="mr" id="{mid(i)}"><h3>{E(nm)}</h3>' + (f'<div class="bt">{btns}</div>' if btns else '') + off + '</li>')
        title = (FAM if lang == 'ko' else FAM_EN)[fam]
        cnt = f'{len(rows)}개 모델' if lang == 'ko' else f'{len(rows)} models'
        out.append(f'<details class="mg"{" open" if gi == 0 else ""}><summary>{E(title)} <span>{cnt}</span></summary><ul class="ml">{"".join(rows)}</ul></details>')
    return ''.join(out)


def surface():
    path = '/driver/surface.html'
    cr, crld = kr.crumb([('서피스 드라이버', '')])
    n = len(SF['models'])
    search = dm.search_js('sfQ', [[nm, '#' + mid(i)] for _, nm, i in SF['models']], '모델명 입력 (예: Pro 9, Laptop 5, Go 3)', '목록에 없는 모델이에요. Microsoft 지원에서 Surface 모델을 고르세요.', '찾기')
    ans = ('서피스는 <b>Windows 업데이트</b>로 드라이버·펌웨어가 자동으로 설치되는 게 기본이에요(Microsoft 권장). '
           '직접 받아야 하면 아래에서 <b>내 서피스 모델</b>을 찾아 <b>내 윈도우 버전에 맞는 .msi 파일</b>을 받아 실행하면 돼요. 파일은 Microsoft 서버에서 바로 내려와요.')
    prep = ('<ol class="big-n"><li><b>키보드(타입 커버)·서피스 펜·도크</b>가 있으면 연결해 두세요. 함께 업데이트돼요.</li>'
            '<li>서피스를 <b>전원에 연결</b>하고 배터리를 <b>40% 이상</b> 충전해 두세요. 업데이트 중에는 전원을 꽂은 채 켜 두세요.</li>'
            '<li><b>인터넷이 안정적인</b> 곳에서 하세요.</li></ol>'
            '<p class="cu-src">Microsoft 지원 \'Surface용 드라이버 및 펌웨어 다운로드\'의 \'Surface 업데이트 전 준비\'.</p>')
    auto = ('<ol class="big-n"><li><b>설정 → Windows 업데이트</b>에서 <b>[업데이트 확인]</b>을 누르고 나온 업데이트를 설치해요.</li>'
            '<li>작업 표시줄 검색창에 <b>선택적 업데이트 보기</b>를 입력해 열고, <b>드라이버 업데이트</b>에 이름이 <b>Surface</b>로 시작하는 항목이 있으면 모두 설치해요.</li>'
            '<li><b>Surface 앱</b> → <b>도움말 및 지원</b>을 펼치면 업데이트 상태를 볼 수 있어요. Surface 앱이 없으면 Microsoft Store에서 받을 수 있어요.</li></ol>')
    manual = ('<ol class="big-n"><li><b>내 윈도우 빌드 확인:</b> 키보드 <b>윈도우 키 + R</b> → <b>winver</b> 입력 → 엔터. \'OS 빌드 22631.xxxx\'처럼 나와요.</li>'
              '<li>아래 내 모델에서 <b>윈도우 11용</b> 또는 <b>윈도우 10용</b> 버튼을 눌러요. 버튼에 적힌 <b>빌드 번호 이상</b>이면 설치할 수 있어요(예: 빌드 22631 이상 → 내 빌드가 22631·26100이면 OK).</li>'
              '<li>받은 <b>.msi 파일</b>을 두 번 눌러 실행하고, 안내대로 설치한 뒤 <b>다시 시작</b>해요.</li>'
              '<li>내 빌드보다 높은 파일만 있으면 먼저 Windows 업데이트로 윈도우를 최신으로 올리거나, \'Microsoft 다운로드 센터\'에서 다른 파일을 고르세요.</li></ol>')
    qa = [('서피스 드라이버는 꼭 따로 받아야 하나요?', '아니요. Microsoft는 대부분의 사용자에게 Windows 업데이트로 자동 설치하는 방법을 권장해요. 직접 받는 .msi 파일은 윈도우를 새로 깔았거나 업데이트가 잘 안 될 때 쓰는 고급 방법이에요.'),
          ('파일이 여러 개예요. 뭘 받아요?', '파일 이름의 Win11/Win10과 빌드 번호를 보고 내 윈도우에 맞는 것을 받아요. winver로 내 빌드를 확인하고, 그 빌드 이하 번호가 붙은 파일 중 가장 높은 것을 고르면 돼요.'),
          ('내 서피스 모델을 모르겠어요.', 'Surface 앱을 열면 모델 이름이 나와요. 또는 설정 → 시스템 → 정보에서 장치 이름을 확인하세요.'),
          ('오래된 서피스도 계속 업데이트되나요?', 'Microsoft 안내에 따르면 각 Surface는 \'드라이버 및 펌웨어 수명 주기\'에 적힌 서비스 종료 날짜까지 새 업데이트를 받아요.'),
          ('파일은 어디서 받아지나요?', 'Microsoft 공식 다운로드 서버(download.microsoft.com)에서 바로 받아져요. 홍라이프 도구는 파일을 올리지 않아요.')]
    fq, fqld = cu.faq(qa)
    main = (kr.HP_CSS + dm.CSS + f'<header class="top hub">{cr}<h1>마이크로소프트 서피스(Surface) 드라이버·펌웨어 바로 다운로드 — 모델별 {n}개</h1>'
            f'<p class="lead">Surface Pro·Laptop·Go·Book·Studio·Laptop Studio·도크까지 {n}개 모델의 드라이버·펌웨어 설치 파일을 Microsoft 서버에서 바로 받고, 쉬운 설치 순서를 확인하세요.</p>'
            f'<p class="cu-ans">{ans}</p>'
            '<ul class="dr-toc"><li><a href="#models">모델별 바로 받기</a></li><li><a href="#prep">업데이트 전 준비</a></li><li><a href="#auto">자동 업데이트</a></li><li><a href="#manual">직접 설치</a></li></ul></header>'
            f'<section class="card dr-sec" id="models"><h2>모델별 바로 받기 ({n}개)</h2><p>모델명을 입력하거나 제품군을 눌러 내 모델을 찾으세요.</p>{search}{cards()}'
            f'<p class="cu-src" style="margin-top:10px">Microsoft 지원의 제품군별 \'드라이버 및 펌웨어 다운로드\' 표와 Microsoft 다운로드 센터 파일을 {kr.CHECKED}에 확인했어요. 가장 최신 빌드용 파일을 버튼으로 걸었고, 다른 빌드용 파일은 다운로드 센터에 있어요.</p>'
            + kr.dl(GUIDE, 'Microsoft Surface 드라이버 안내 원문', 'support.microsoft.com', True) + '</section>'
            f'<section class="card dr-sec" id="prep"><h2>업데이트 전 준비</h2>{prep}</section>'
            f'<section class="card dr-sec" id="auto"><h2>가장 쉬운 방법: Windows 업데이트 (Microsoft 권장)</h2>{auto}</section>'
            f'<section class="card dr-sec" id="manual"><h2>직접 설치하기 (.msi 파일)</h2>{manual}</section>'
            + kr.guide_sec('서피스') + fq
            + kr.src_sec('Microsoft 지원 \'Surface용 드라이버 및 펌웨어 다운로드\'(support.microsoft.com/ko-kr), Microsoft 다운로드 센터 모델별 페이지')
            + kr.REL)
    ld = [crld, fqld, kr.howto('서피스 드라이버·펌웨어 설치 방법', ['액세서리 연결·전원 연결·배터리 40% 이상', '설정 → Windows 업데이트 → 업데이트 확인', '선택적 업데이트에서 Surface 드라이버 설치', '직접 설치 시 winver로 빌드 확인 후 맞는 .msi 실행'])]
    kr.write(path, f'서피스 드라이버 다운로드 — Surface Pro·Laptop·Go 모델별 {n}개 펌웨어 바로 받기, 설치 방법 | 홍라이프 도구',
             f'마이크로소프트 서피스 Surface Pro 9·8·7, Laptop 5·4, Go 3·4, Book 3, Laptop Studio 등 {n}개 모델의 드라이버·펌웨어(.msi)를 Microsoft 서버에서 바로 받고, 윈도우 빌드에 맞는 파일 고르는 법과 설치 순서를 쉽게 확인하세요.',
             main, ld)
    return path


def surface_en():
    path = '/en/driver/surface.html'
    cr, crld = en.crumb([('Surface', '')])
    n = len(SF['models'])
    search = dm.search_js('sfE', [[nm, '#' + mid(i)] for _, nm, i in SF['models']], 'Model (e.g. Pro 9, Laptop 5)', 'Not in this list.', 'Find')
    steps = ('<ol class="big-n"><li>Microsoft recommends Windows Update: Settings → Windows Update → Check for updates, then install optional driver updates named Surface.</li>'
             '<li>To install manually, run <b>winver</b> to see your build, then download the .msi whose build number is equal to or lower than yours.</li>'
             '<li>Before updating: connect accessories, plug in power, charge to 40%+, use a stable connection.</li></ol>')
    qa = [('Where do files come from?', 'Directly from Microsoft (download.microsoft.com). HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + dm.CSS + f'<header class="top hub">{cr}<h1>Microsoft Surface Drivers &amp; Firmware — Direct Download for {n} Models</h1>'
            '<p class="lead">Surface Pro, Laptop, Go, Book, Studio, Laptop Studio and Dock driver/firmware packages straight from Microsoft.</p></header>'
            f'<section class="card dr-sec" id="models"><h2>Models ({n})</h2>{search}{cards("en")}</section>'
            f'<section class="card dr-sec"><h2>How to install</h2>{steps}</section>' + fq
            + en.src('Microsoft Support "Download drivers and firmware for Surface", Microsoft Download Center') + en.REL)
    en.write(path, f'Surface Driver & Firmware Download — {n} Models (Pro, Laptop, Go) | HongLife Tools',
             f'Download Microsoft Surface driver and firmware .msi packages for {n} models directly from Microsoft, and pick the right file for your Windows build.', main, [crld, fqld])
    return path


if __name__ == '__main__':
    print(surface(), surface_en())
