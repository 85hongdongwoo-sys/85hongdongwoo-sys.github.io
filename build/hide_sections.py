"""잠시 숨기기 (되돌릴 수 있게): 여행 카테고리(/trip/)와 유료 미대 컨설팅(midae-review).

빌드 맨 끝에 돌아요. 페이지 파일은 그대로 두고
  - 메뉴·카드·목록·검색·사이트맵·RSS에서 링크를 빼고
  - 숨긴 페이지에는 noindex 를 넣어 검색에서 빠지게 하고
  - 미대 정시 판독기 안의 유료 안내(광고 상자·버튼·FAQ 문장)를 지워요.
다시 보이게 하려면 아래 HIDE 를 비우면 돼요 (예: HIDE = []).
"""
import os, re, sys

HIDE = ['trip', 'midae']          # 'trip' = 여행 카테고리, 'midae' = 유료 미대 컨설팅

root = sys.argv[1] if len(sys.argv) > 1 else '_site'
pats = []
if 'trip' in HIDE:
    pats.append(r'/trip/[^"\'<>\s]*')
if 'midae' in HIDE:
    pats.append(r'/ipsi/midae-review\.html[^"\'<>\s]*')
if not pats:
    print('hide: nothing to hide'); sys.exit(0)
U = r'(?:https?://honglife\.co\.kr)?(?:' + '|'.join(pats) + ')'
HREF = r'href=["\']' + U + r'["\']'

LI = re.compile(r'<li\b[^>]*>(?:(?!</?li\b).)*?' + HREF + r'(?:(?!</?li\b).)*?</li>', re.S)
A = re.compile(r'<a\b[^>]*' + HREF + r'[^>]*>.*?</a>', re.S)
OBJ = r'\{[^{}]*?"(?:u|url)":"' + U + r'"[^{}]*\}'
JS1, JS2 = re.compile(',' + OBJ), re.compile(OBJ + ',?')
SM = re.compile(r'<url>(?:(?!</url>).)*?<loc>' + U + r'</loc>.*?</url>\s*', re.S)
RSS = re.compile(r'<item>(?:(?!</item>).)*?<link>' + U + r'</link>.*?</item>\s*', re.S)
NOIDX = '<meta name="robots" content="noindex">'


def hidden_page(rel):
    rel = '/' + rel.replace(os.sep, '/')
    return ('trip' in HIDE and rel.startswith('/trip/')) or \
           ('midae' in HIDE and rel == '/ipsi/midae-review.html')


def midae_tool(s):
    """미대 정시 판독기에서 유료 안내만 지우고 무료 판독은 그대로 둬요."""
    s = re.sub(r'\s*<aside class="mj-pro".*?</aside>', '', s, flags=re.S)
    s = re.sub(r' 그림 10장을 보내 4년제 미대(?:(?!</p>|"\}).)*?\(베타, 유료\)도 있어요\.', '', s, flags=re.S)
    s = re.sub(r'<b>🔒 이 학과는 강사가 직접 판독해요</b><p>[^<]*</p><a class="lkbtn"[^>]*>[^<]*</a>',
               '<b>🔒 합격 컷 비공개 학과예요</b><p>대학이 비교할 합격 컷을 공개하지 않아 자동 판독을 하지 않아요. 각 대학 모집요강을 확인해 주세요.</p>', s)
    s = s.replace('‘🔒 강사 판독’으로', '‘🔒 합격 컷 비공개’로')
    s = s.replace('🔒 강사 판독', '🔒 합격 컷 비공개').replace("'강사 판독'", "'합격 컷 비공개'")
    s = s.replace('자동 판독 대신 강사가 그림을 보고 직접 봐 드리는 유료 진단으로 안내해요.',
                  '자동 판독을 하지 않고 비워 둬요. 각 대학 모집요강을 확인해 주세요.')
    return s


n = 0
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith(('.html', '.xml', '.json', '.js', '.webmanifest')):
            continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, root)
        try:
            s = open(p, encoding='utf-8').read()
        except Exception:
            continue
        o = s
        if f.endswith('.xml'):
            s = SM.sub('', s); s = RSS.sub('', s)
        else:
            if f.endswith('.html'):
                if hidden_page(rel):
                    if NOIDX not in s and 'name="robots"' not in s:
                        s = s.replace('<head>', '<head>' + NOIDX, 1)
                    if hidden_page(rel):  # 숨긴 페이지 안 링크는 그대로 둬요
                        if s != o:
                            open(p, 'w', encoding='utf-8').write(s); n += 1
                        continue
                s = LI.sub('', s); s = A.sub('', s)
                if rel == 'index.html':
                    s = s.replace('입시·여행까지 무료 도구', '입시까지 무료 도구')
                    s = s.replace('정시 입시 계산과 출발확정 여행 패키지까지', '정시 입시 계산까지')
                if 'midae' in HIDE and rel.replace(os.sep, '/') == 'ipsi/midae-jeongsi-2027.html':
                    s = midae_tool(s)
            s = JS1.sub('', s); s = JS2.sub('', s)
        if s != o:
            open(p, 'w', encoding='utf-8').write(s); n += 1
print('hide:', HIDE, 'files changed', n)
