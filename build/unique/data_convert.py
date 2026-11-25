"""변환(/convert/pair/)·확장자(/convert/ext/) 페이지 고유 본문 — 사실 재료(_conv_*.py)로 페이지마다 다르게 조립.
가장 중요한 것: '바꾸면 내용이 어떻게 되나'(그대로인 것·달라지는 것) 표를 변환마다 따로 쓴다."""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))


def _load(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(HERE, n + '.py'))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


FMT = _load('_conv_fmt').FMT
EXT = _load('_conv_ext').EXT
STEPS = _load('_conv_steps').STEPS
PAIR = {}
for n in ('_conv_pairs_img', '_conv_pairs_av', '_conv_pairs_doc'):
    PAIR.update(_load(n).PAIR)


def josa(word, a, b):
    """받침 있으면 a, 없으면 b. 영문 약어는 끝 글자 읽는 소리 기준(엘·엠·엔·알만 받침), 괄호 뒤는 무시."""
    w = word.split('(')[0].strip()
    last = w[-1]
    if '가' <= last <= '힣':
        jong = (ord(last) - 0xAC00) % 28
        if b == '로' and jong == 8: return b   # ㄹ 받침은 '로'
        return a if jong else b
    if last.upper() == 'L' and b == '로': return b
    return a if last.upper() in 'LMNR' else b


PAGES = {}
for key, p in PAIR.items():
    a, b = key.split('-to-')
    A, B = FMT[a], FMT[b]
    an, bn = A['name'], B['name']
    about = [A['hist'] + ' ' + A['src']]
    if B.get('dst'):
        about.append(B['dst'])
    PAGES['/convert/pair/%s.html' % key] = dict(
        h2='%s%s %s%s 바꾸면 내용은 어떻게 되나' % (an, josa(an, '을', '를'), bn, josa(bn, '으로', '로')),
        about=about,
        rows_h='바꾸기 전과 후 — 그대로인 것·달라지는 것', head=['항목', an, bn], rows=p['rows'],
        extra=('이럴 때 %s%s 바꿔요' % (bn, josa(bn, '으로', '로')), p['why']),
        steps=STEPS.get(key, []),
        tips=p['tips'], tips_h='바꿀 때 이렇게 하세요', trouble=p['trouble'], faq=p['faq'],
        sec_cls='card uq')

for f, e in EXT.items():
    F = FMT[f]
    about = [F['hist'], (F.get('src') or '') + ' ' + (F.get('dst') or '')]
    PAGES['/convert/ext/%s.html' % f] = dict(
        h2='.%s 파일, 기기마다 여는 법과 주의할 점' % f,
        about=[x.strip() for x in about if x.strip()],
        rows_h='기기·프로그램별로 열기', head=['기기·프로그램', '여는 방법'], rows=e['open'],
        extra=e['extra'], trouble=e['trouble'], faq=e['faq'], sec_cls='card uq')
