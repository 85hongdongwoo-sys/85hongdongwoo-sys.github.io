# 큐넷 국가전문자격 '자격상세정보 > 시험정보'(시험일정·응시자격·시험과목·합격기준·수수료)를 자격별로 읽어
# 허용 태그만 남긴 HTML로 build/exams/data/qnet_info.json 에 저장 (출처: 한국산업인력공단 큐넷)
import json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from scrape_more import QGIDS
UA = {'User-Agent': 'Mozilla/5.0 (honglife.co.kr exam index)'}
QN = 'https://www.q-net.or.kr'
OUT = os.path.join(os.path.dirname(__file__), 'data', 'qnet_info.json')
KEEP = {'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption', 'p', 'br', 'ul', 'ol', 'li', 'strong', 'b', 'h3', 'h4', 'h5', 'dl', 'dt', 'dd'}


def get(u):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf-8', 'replace')
        except Exception:
            time.sleep(3)
    return ''


def clean(h):
    h = re.sub(r'(?s)<!--.*?-->', '', h)
    h = re.sub(r'(?is)<(script|style|button|select|form|input|img|a)\b[^>]*>(.*?</\1>)?', lambda m: re.sub(r'<[^>]+>', '', m.group(2) or '') if m.group(1).lower() == 'a' else '', h)

    def tag(m):
        close, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if name not in KEEP:
            return ' ' if name in ('div', 'span') else ''
        if close:
            return f'</{name}>'
        keep = ' '.join(f'{k}="{v}"' for k, v in re.findall(r'\b(colspan|rowspan)\s*=\s*["\']?(\d+)', attrs, re.I))
        return f'<{name}{" " + keep if keep else ""}>'
    h = re.sub(r'<(/?)([a-zA-Z0-9]+)([^>]*)>', tag, h)
    h = re.sub(r'[ \t\r\f\v]+', ' ', h)
    h = re.sub(r'\s*\n\s*', '\n', h)
    h = re.sub(r'(<p>\s*</p>|<li>\s*</li>)', '', h)
    return h.strip()


def main():
    res = {}
    for g, name in QGIDS:
        h = get(f'{QN}/crf005.do?id=crf00503&gSite=L&gId={g}')
        jm = re.search(r'id="jmCd"[^>]*value="([^"]*)"', h) or re.search(r'name="jmCd"[^>]*value="([^"]*)"', h)
        nm = re.search(r'id="jmNm"[^>]*value="([^"]*)"', h) or re.search(r'name="jmNm"[^>]*value="([^"]*)"', h)
        if not jm:
            print('no jmCd', g, name); continue
        jm, nm = jm.group(1), (nm.group(1) if nm else name)
        u = f'{QN}/crf005.do?id=crf00503s02&gSite=L&gId={g}&jmCd={jm}&jmInfoDivCcd=B0&jmNm={urllib.parse.quote(nm)}&seriesCd={g}'
        c = clean(get(u))
        if len(c) < 200:
            print('short', g, name, len(c)); continue
        res[g] = {'name': nm, 'jmCd': jm, 'html': c, 'src': f'{QN}/crf005.do?id=crf00503&gSite=L&gId={g}'}
        print(g, nm, len(c))
        time.sleep(1)
    res['_checked'] = time.strftime('%Y-%m-%d')
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    if len(sys.argv) > 1:
        print(res.get(sys.argv[1], {}).get('html', '')[:6000])


if __name__ == '__main__':
    main()
