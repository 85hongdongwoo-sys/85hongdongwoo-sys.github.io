"""페이지마다 다른 본문 넣기 (2026-11-25) — 페이지 유사도 검사에서 서로 많이 겹친 페이지에
그 회사·그 프로그램에만 해당하는 글(소개, 제품별 표, 자주 생기는 문제, 자주 묻는 질문)을 2,000자 안팎으로 넣는다.
데이터: build/unique/data_*.py 의 PAGES = {'/driver/acer.html': {...}, ...}
넣는 자리: 페이지의 첫 '처음 하는 분' 안내(id="easy") 바로 앞, 없으면 '자주 묻는 질문' 카드 앞.
Usage: python3 build/unique/inject.py _site"""
import glob, html, importlib.util, json, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else '_site'
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
CSS = ('<style id="uq-css">.uq p{line-height:1.8;margin:0 0 10px;word-break:keep-all}'
       '.uq h3{font-size:16.5px;margin:18px 0 8px}.uq .tw{max-width:100%;overflow-x:auto}'
       '.uq table{width:100%;border-collapse:collapse;font-size:14.5px}.uq th,.uq td{border-bottom:1px solid var(--line-s,#E3E7EE);'
       'padding:8px 6px;text-align:left;vertical-align:top;word-break:keep-all}.uq thead th{font-size:13px;color:var(--muted,#5B6B82)}'
       '.uq dl{margin:0}.uq dt{font-weight:700;margin:12px 0 4px;word-break:keep-all}.uq dd{margin:0;line-height:1.75;word-break:keep-all}'
       '.uq ol.uq-steps{margin:0 0 6px;padding-left:22px;line-height:1.75}.uq ol.uq-steps li{margin:4px 0;word-break:keep-all}'
       '.uq .uq-src{font-size:13px;color:var(--muted,#5B6B82);margin-top:12px}</style>')


def load():
    pages = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'data_*.py'))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, v in getattr(m, 'PAGES', {}).items():
            pages.setdefault(k, {}).update(v)
        for k, v in getattr(m, 'EXTRA', {}).items():
            pages.setdefault(k, {})['extra'] = v
        for k, v in getattr(m, 'MORE', {}).items():
            for key in ('trouble', 'faq'):
                pages.setdefault(k, {}).setdefault(key, []).extend(v.get(key, []))
        for k, v in getattr(m, 'TIPS', {}).items():
            pages.setdefault(k, {})['tips'] = v
    return {k: v for k, v in pages.items() if 'h2' in v}


def render(d, lang):
    ko = lang == 'ko'
    h = '<section class="%s" id="uq"><h2>%s</h2>' % (d.get('sec_cls', 'card dr-sec uq'), E(d['h2']))
    h += ''.join('<p>%s</p>' % x for x in d['about'])
    if d.get('rows'):
        hd = d.get('head') or (['제품', '필요한 것', '알아 둘 점'] if ko else ['Product', 'What you need', 'Note'])
        h += '<h3>%s</h3><div class="tw"><table><thead><tr>%s</tr></thead><tbody>' % (
            E(d.get('rows_h') or ('제품별로 받을 것' if ko else 'What to get for each product')), ''.join('<th>%s</th>' % E(x) for x in hd))
        h += ''.join('<tr><th scope="row">%s</th>%s</tr>' % (r[0], ''.join('<td>%s</td>' % c for c in r[1:])) for r in d['rows'])
        h += '</tbody></table></div>'
    if d.get('steps'):
        h += '<h3>%s</h3><ol class="uq-steps">%s</ol>' % (E(d.get('steps_h') or '변환할 때 파일 안에서 일어나는 일'), ''.join('<li>%s</li>' % x for x in d['steps']))
    if d.get('extra'):
        h += '<h3>%s</h3>' % E(d['extra'][0]) + ''.join('<p>%s</p>' % x for x in d['extra'][1:])
    if d.get('tips'):
        h += '<h3>%s</h3><ul class="cu-chk">%s</ul>' % (E(d.get('tips_h') or ('알아 두면 좋은 점' if ko else 'Good to know')), ''.join('<li>%s</li>' % x for x in d['tips']))
    if d.get('trouble'):
        h += '<h3>%s</h3><dl>' % E(d.get('trouble_h') or ('자주 생기는 문제와 해결' if ko else 'Common problems and fixes'))
        h += ''.join('<dt>%s</dt><dd>%s</dd>' % (q, a) for q, a in d['trouble']) + '</dl>'
    if d.get('note'):
        h += '<p class="uq-src">%s</p>' % d['note']
    return h + '</section>'


def strip(s):
    return re.sub(r'<[^>]+>', '', s)


def main():
    pages = load(); n = 0
    for url, d in pages.items():
        rel = url.lstrip('/')
        p = os.path.join(root, rel + ('index.html' if rel.endswith('/') or rel == '' else ''))
        if not os.path.isfile(p):
            print('uq: missing', url); continue
        s = open(p, encoding='utf-8').read()
        if 'id="uq"' in s: continue
        for rx in d.get('strip', []):   # 형제 페이지끼리 똑같이 반복되는 블록 빼기(새 본문이 같은 역할을 함)
            s = re.sub(rx, '', s, count=1, flags=re.S)
        lang = d.get('lang', 'ko')
        sec = render(d, lang)
        anchors = ['<section class="card dr-sec" id="easy">', '<section class="card dr-sec" id="win">', '<section class="card faq', '<section class="card"><h2>자주 묻는 질문', '<section class="card"><h2>FAQ', '<section class="card"><h2>Frequently']
        at = next((a for a in anchors if a in s), None)
        if not at:
            print('uq: no anchor', url); continue
        s = s.replace(at, sec + at, 1)
        if 'id="uq-css"' not in s:
            s = s.replace('</head>', CSS + '</head>', 1)
        # 자주 묻는 질문: 화면(dl.pe-faq 또는 details) + JSON-LD
        faqs = d.get('faq', [])
        if faqs:
            m = re.search(r'<dl class="pe-faq">', s)
            if m:
                s = s[:m.end()] + ''.join('<dt>%s</dt><dd>%s</dd>' % (q, a) for q, a in faqs) + s[m.end():]
            else:
                i = s.find('<section class="card faq'); j = s.find('</section>', i) if i >= 0 else -1
                if j > 0:
                    s = s[:j] + ''.join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in faqs) + s[j:]
            mm = re.search(r'<script type="application/ld\+json">(\{[^<]*?"@type":\s*"FAQPage".*?)</script>', s, re.S)
            if mm:
                try:
                    j = json.loads(mm.group(1))
                    j['mainEntity'] = [{'@type': 'Question', 'name': strip(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}} for q, a in faqs] + j.get('mainEntity', [])
                    s = s[:mm.start(1)] + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + s[mm.end(1):]
                except Exception as e:
                    print('uq: ld skip', url, e)
        open(p, 'w', encoding='utf-8').write(s); n += 1
    print('uq: pages', n, '/', len(pages))


if __name__ == '__main__':
    main()
