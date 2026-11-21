"""큐넷 국가전문자격 문제지 ZIP → 교시별 PDF를 풀어 GitHub Releases에 올리고, 버튼용 주소표(data/qnet_pdf.json)를 만든다.
공공누리 제1유형(출처표시: 한국산업인력공단) 자료라 재배포가 허용된다. 자격마다 릴리스 하나(qnet-<gId>), 파일 이름은 <fileSeq>_<n>.pdf.
GitHub Actions(qnet-pdf.yml)에서 실행. 이미 올린 파일은 건너뛴다."""
import json, os, re, subprocess, sys, tempfile, time, urllib.parse, urllib.request, zipfile
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'data')
REPO = os.environ['GITHUB_REPOSITORY']; QN = 'https://www.q-net.or.kr'
Q = json.load(open(os.path.join(D, 'qnet.json'), encoding='utf-8'))
OUT = os.path.join(D, 'qnet_pdf.json')
M = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
def gh(*a, check=True): return subprocess.run(['gh', *a], capture_output=True, text=True, check=check)
def label(n):
    b = n.rsplit('.', 1)[0]
    m = re.findall(r'(\d\s*차)|(\d\s*교시)|([A-Z]형)', b)
    parts = [x for t in m for x in t if x]
    return ' '.join(re.sub(r'\s', '', p) for p in parts) or re.sub(r'^(19|20)\d\d\s*년?\s*(제?\s*\d+\s*회)?\s*', '', b)[:20]
def fix(n):
    try: return n.encode('cp437').decode('cp949')
    except Exception: return n
done_rel = set()
budget = float(os.environ.get('MAX_MIN', '300')) * 60; t0 = time.time()
for r in Q['rows']:
    g = r['g']; tag = f'qnet-{g}'
    for name, path, seq in r['files']:
        if seq in M or time.time() - t0 > budget or not name.lower().endswith('.zip'): continue
        if tag not in done_rel:
            if gh('release', 'view', tag, '-R', REPO, check=False).returncode != 0:
                gh('release', 'create', tag, '-R', REPO, '-t', f'{r["q"]} 기출 문제지 (큐넷, 공공누리 제1유형)', '-n', '출처: 한국산업인력공단 큐넷(Q-Net). 공공누리 제1유형.', '--latest=false')
            done_rel.add(tag)
        url = f'{QN}/cst003.do?id=cst00302s01&gSite=L&gId={g}&fileCode=R001&filePath={urllib.parse.quote(path)}&fileName={urllib.parse.quote(name)}&fileSeq={seq}'
        try:
            with tempfile.TemporaryDirectory() as td:
                fp = os.path.join(td, 'f.bin')
                with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'HongLifeTools/1.0 (+https://honglife.co.kr)'}), timeout=300) as resp, open(fp, 'wb') as o:
                    o.write(resp.read())
                pdfs = []
                if zipfile.is_zipfile(fp):
                    with zipfile.ZipFile(fp) as z:
                        for i, zi in enumerate(sorted((x for x in z.infolist() if x.filename.lower().endswith('.pdf')), key=lambda x: fix(x.filename))):
                            out = os.path.join(td, f'{seq}_{i + 1}.pdf'); open(out, 'wb').write(z.read(zi)); pdfs.append((out, fix(os.path.basename(zi.filename))))
                elif name.lower().endswith('.pdf'):
                    out = os.path.join(td, f'{seq}_1.pdf'); os.rename(fp, out); pdfs.append((out, name))
                if not pdfs: M[seq] = []; continue
                big = [p for p, _ in pdfs if os.path.getsize(p) > 1900 * 1024 * 1024]
                ok = [p for p, _ in pdfs if p not in big]
                if ok: gh('release', 'upload', tag, *ok, '-R', REPO, '--clobber')
                M[seq] = [[label(n), f'https://github.com/{REPO}/releases/download/{tag}/{os.path.basename(p)}'] for p, n in pdfs if p in ok]
                print(r['q'], r['title'], len(ok), 'PDF', flush=True)
        except Exception as e:
            print('FAIL', r['q'], r['title'], e, flush=True)
        json.dump(M, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        time.sleep(1)
print('mapped', len(M))
