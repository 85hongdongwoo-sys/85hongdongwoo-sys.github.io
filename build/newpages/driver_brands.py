"""여러 회사 드라이버·공식 프로그램 안내 (한 회사 = 한 페이지) — /driver/<key>.html, /en/driver/<key>.html
데이터는 build/newpages/data/brands.py 의 B 사전 (회사마다 공식 페이지에서 확인한 내용과 출처).
버튼은 모두 제조사 공식 사이트·서버·앱 스토어로 연결해요. 파일은 올리지 않아요.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
import car_update as cu
import driver_pages as kr
import driver_en as en
from brands import B, CATS

E = cu.E


def page(k):
    c = B[k]
    path = f'/driver/{k}.html'
    cat = CATS[c['cat']]
    cr, crld = kr.crumb([(f'{c["name"]} {cat["short"]}', '')])
    tools = ''.join(
        f'<li class="hpm"><h3>{E(t["h"])}</h3><p class="fi">{t["d"]}</p><div class="bt">'
        + ''.join(kr.dl(u, bt, bs, i > 0 or j > 0) for j, (u, bt, bs) in enumerate(t['b'])) + '</div></li>'
        for i, t in enumerate(c['tools']))
    steps = '<ol class="big-n">' + ''.join(f'<li>{s}</li>' for s in c['steps']) + '</ol>'
    notes = ('<section class="card dr-sec" id="tips"><h2>꼭 알아 둘 것</h2><ul class="cu-chk">' + ''.join(f'<li>{x}</li>' for x in c['notes']) + '</ul></section>') if c.get('notes') else ''
    model = '<section class="card dr-sec" id="model"><h2>내 제품 모델명 찾기</h2><ul class="cu-chk">' + ''.join(f'<li>{x}</li>' for x in c['model']) + '</ul></section>'
    qa = [(f'{c["name"]} {cat["q"]}는 어디서 받아야 안전해요?', f'{c["name"]} 공식 사이트·공식 앱 스토어에서 받으세요. 이 페이지의 버튼은 모두 {c["name"]} 공식 주소로 연결돼요. 광고에 나오는 \'드라이버 자동 설치\' 프로그램은 쓰지 마세요.')] + c.get('qa', []) + \
         [('파일은 어디서 받아지나요?', f'{c["name"]} 공식 서버나 공식 앱 스토어에서 받아져요. 홍라이프 도구는 파일을 올리지 않아요.')]
    fq, fqld = cu.faq(qa)
    first = c['tools'][0]['b'][0]
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>{E(c["name"])}({E(c["en"])}) {E(c["title"])}</h1>'
            f'<p class="lead">{E(c["name"])} {E(c["lead"])}</p>'
            f'<p class="cu-ans">{c["ans"]}</p>' + kr.dl(*first)
            + '<ul class="dr-toc"><li><a href="#tools">공식 프로그램</a></li><li><a href="#steps">설치 순서</a></li><li><a href="#model">모델명 찾기</a></li>'
            + ('<li><a href="#tips">꼭 알아 둘 것</a></li>' if notes else '') + '</ul></header>'
            f'<section class="card dr-sec" id="tools"><h2>공식 프로그램·드라이버 받기</h2><ul class="hpl">{tools}</ul></section>'
            f'<section class="card dr-sec" id="steps"><h2>설치 순서 (아주 쉽게)</h2>{steps}</section>'
            + notes + model + (kr.guide_pc(c['name']) if cat['pc'] else '') + fq + kr.src_sec(c['src']) + kr.REL)
    kr.write(path, f'{c["name"]} {c["title"]} (공식) | 홍라이프 도구', c['desc'], main, [crld, fqld])
    return path


def page_en(k):
    c = B[k]
    path = f'/en/driver/{k}.html'
    cr, crld = en.crumb([(c['en'], '')])
    tools = ''.join(f'<li class="hpm"><h3>{E(t["en"])}</h3><div class="bt">'
                    + ''.join(en.dl(u, t['en'] if j == 0 else 'More', 'Official', i > 0 or j > 0) for j, (u, _, _) in enumerate(t['b'][:2])) + '</div></li>'
                    for i, t in enumerate(c['tools']))
    qa = [('Where do files come from?', f'From {c["en"]}\'s official sites, servers or app stores. HongLife Tools does not host files.')]
    fq, fqld = en.faq(qa)
    main = (kr.HP_CSS + f'<header class="top hub">{cr}<h1>{E(c["en"])} {E(c["title_en"])}</h1>'
            f'<p class="lead">{E(c["lead_en"])}</p></header>'
            f'<section class="card dr-sec"><h2>Official software</h2><ul class="hpl">{tools}</ul></section>'
            + (en.easy_pc(c['en']) if CATS[c['cat']]['pc'] else '') + fq + en.src(c['src_en']) + en.REL)
    en.write(path, f'{c["en"]} {c["title_en"]} | HongLife Tools', c['lead_en'], main, [crld, fqld])
    return path


if __name__ == '__main__':
    for k in B:
        print(page(k), page_en(k))
