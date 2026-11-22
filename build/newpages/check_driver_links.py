"""드라이버 페이지의 공식 다운로드 주소가 살아 있는지 점검 (매주). 깨진 주소는 목록으로 출력하고 실패 코드로 끝낸다."""
import glob, re, sys, urllib.request
urls = set()
for f in glob.glob('overlay/driver/*.html') + glob.glob('overlay/en/driver/*.html'):
    urls |= set(re.findall(r'href="(https?://[^"]+)"', open(f, encoding='utf-8').read()))
urls = sorted(u.replace('&amp;', '&') for u in urls if 'honglife' not in u)
bad = []
from concurrent.futures import ThreadPoolExecutor
def check(u):
    try:
        req = urllib.request.Request(u, method='HEAD', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'})
        code = urllib.request.urlopen(req, timeout=40).status
    except urllib.error.HTTPError as e:
        code = e.code
        if code in (403, 405):  # HEAD를 막는 사이트는 GET으로 다시
            try:
                code = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-0'}), timeout=40).status
            except urllib.error.HTTPError as e2:
                code = e2.code
            except Exception as e2:
                code = repr(e2)[:60]
    except Exception as e:
        code = repr(e)[:60]
    ok = code in (200, 206) or (code == 403 and any(h in u for h in ('intel.co', 'epson.co.kr', 'ebz.epson.net', 'support.epson.net')))  # 인텔·엡손 사이트는 자동 점검(봇)만 막고 사람은 열림
    return ok, code, u
retry = []
with ThreadPoolExecutor(6) as ex:
    for ok, code, u in ex.map(check, urls):
        if ok:
            print('OK ', code, u)
        else:
            retry.append(u)
import time
for u in retry:  # 너무 많이 동시에 물어 시간 초과된 것은 천천히 한 번 더
    time.sleep(1)
    ok, code, u = check(u)
    print('OK ' if ok else 'BAD', code, u)
    if not ok:
        bad.append(u)
print(f'checked {len(urls)}, broken {len(bad)}')
sys.exit(1 if bad else 0)
