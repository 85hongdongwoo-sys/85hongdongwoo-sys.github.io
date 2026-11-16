# 홈 도구 카드용 장면 그림(엑셀 창·핸드폰 화면·문서 등) SVG 생성
import os, sys
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
W, H = 200, 140
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="12 2 176 138" width="{W}" height="{H}">{body}</svg>'
SH = ''
def win(x, y, w, h, bar, inner, dark=False):
    bg = '#1E2433' if dark else '#fff'
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{bg}"/>'
            f'<path d="M{x} {y+9}a9 9 0 0 1 9-9h{w-18}a9 9 0 0 1 9 9v7H{x}z" fill="{bar}"/>'
            f'<circle cx="{x+9}" cy="{y+8}" r="2.2" fill="#fff" opacity=".85"/><circle cx="{x+16}" cy="{y+8}" r="2.2" fill="#fff" opacity=".6"/><circle cx="{x+23}" cy="{y+8}" r="2.2" fill="#fff" opacity=".4"/>'
            f'{inner}</g>')
def phone(x, y, w, h, inner, screen='#fff'):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#1A1D24"/>'
            f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="9" fill="{screen}"/>'
            f'<rect x="{x+w/2-9}" y="{y+7}" width="18" height="4" rx="2" fill="#1A1D24"/>{inner}</g>')
def page(x, y, w, h, inner, fill='#fff'):
    return f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}"/>{inner}</g>'
def lines(x, y, n, w, gap=8, c='#D5DAE3', h=3.5):
    return ''.join(f'<rect x="{x}" y="{y+i*gap}" width="{w*(1 if i%3!=2 else .65)}" height="{h}" rx="1.75" fill="{c}"/>' for i in range(n))
def grid(x, y, cols, rows, cw, ch, head='#1F9D55', hl=None):
    s = ''
    for r in range(rows):
        for c in range(cols):
            f = head if r == 0 else ('#E7F6EC' if hl and (c, r) in hl else '#fff')
            s += f'<rect x="{x+c*cw}" y="{y+r*ch}" width="{cw}" height="{ch}" fill="{f}" stroke="#D9DEE6" stroke-width=".8"/>'
    return s
T = lambda x, y, t, c='#fff', sz=9, w=700: f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{sz}" font-weight="{w}" fill="{c}">{t}</text>'
S = {}
S['excel'] = win(30, 18, 140, 106, '#1F9D55', '<rect x="36" y="32" width="128" height="12" rx="3" fill="#F1F4F8"/>' + T(41, 41, 'fx  =SUMIFS(C:C,A:A,"서울")', '#1F7A44', 7) + grid(36, 50, 4, 5, 32, 13, hl={(2, 4), (3, 4)}))
S['sheet'] = win(26, 18, 148, 106, '#13A06B', grid(32, 34, 3, 6, 24, 13) + ''.join(f'<rect x="{112+i*14}" y="{112-h}" width="9" height="{h}" rx="2" fill="{c}"/>' for i, (h, c) in enumerate([(30, '#4F8CFF'), (52, '#13A06B'), (40, '#FFB020'), (64, '#FF6B6B')])))
S['doc'] = page(56, 14, 88, 112, '<rect x="66" y="26" width="44" height="7" rx="2" fill="#3D5AFE"/>' + lines(66, 42, 7, 68, 9) + '<circle cx="124" cy="108" r="9" fill="none" stroke="#E5484D" stroke-width="2"/>')
S['pdf'] = page(48, 22, 80, 100, lines(58, 34, 6, 60, 9), '#EEF1F6') + page(70, 14, 84, 104, lines(80, 46, 6, 62, 9) + '<rect x="80" y="26" width="34" height="13" rx="3" fill="#E5484D"/>' + T(85, 36, 'PDF', '#fff', 10))
S['image'] = phone(66, 6, 68, 128, '<rect x="70" y="18" width="60" height="70" fill="#7EC8FF"/><circle cx="117" cy="32" r="7" fill="#FFD43B"/><path d="M70 88l20-30 14 18 9-11 17 23z" fill="#2F9E44"/>' + ''.join(f'<rect x="{72+i*20}" y="96" width="16" height="16" rx="3" fill="{c}"/>' for i, c in enumerate(['#FFA94D', '#B197FC', '#63E6BE'])))
S['convert'] = page(22, 34, 58, 74, '<rect x="30" y="44" width="26" height="11" rx="2" fill="#4F8CFF"/>' + T(33, 52, 'HWP', '#fff', 7) + lines(30, 64, 4, 42, 8)) + '<path d="M90 71h22m-7-7 7 7-7 7" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' + page(122, 34, 58, 74, '<rect x="130" y="44" width="26" height="11" rx="2" fill="#E5484D"/>' + T(134, 52, 'PDF', '#fff', 7) + lines(130, 64, 4, 42, 8))
S['text'] = phone(64, 6, 72, 128, '<rect x="72" y="20" width="44" height="14" rx="7" fill="#E9ECF2"/><rect x="84" y="40" width="44" height="14" rx="7" fill="#4F8CFF"/><rect x="72" y="60" width="52" height="14" rx="7" fill="#E9ECF2"/>' + T(74, 100, '글자 1,248자', '#1A1D24', 9) + '<rect x="72" y="106" width="56" height="5" rx="2.5" fill="#E9ECF2"/><rect x="72" y="106" width="38" height="5" rx="2.5" fill="#7048E8"/>')
S['ai'] = win(28, 18, 144, 106, '#7048E8', '<rect x="36" y="36" width="70" height="16" rx="8" fill="#F1EEFE"/><rect x="88" y="58" width="76" height="30" rx="9" fill="#7048E8"/>' + lines(96, 66, 2, 58, 8, '#CDBFFF') + '<path d="M50 104l3-8 3 8 8 3-8 3-3 8-3-8-8-3z" fill="#FFB020"/><rect x="70" y="100" width="94" height="14" rx="7" fill="#F1F4F8"/>')
S['calendar'] = page(40, 16, 120, 108, '<path d="M40 21a5 5 0 0 1 5-5h110a5 5 0 0 1 5 5v15H40z" fill="#FF6B3D"/>' + T(84, 31, '2027.03', '#fff', 10) + ''.join(f'<rect x="{48+(i%7)*15}" y="{44+(i//7)*15}" width="11" height="11" rx="3" fill="{["#EEF1F6", "#FF6B3D", "#4F8CFF"][1 if i == 10 else 2 if i == 18 else 0]}"/>' for i in range(35)))
S['qr'] = phone(66, 6, 68, 128, '<rect x="76" y="34" width="48" height="48" fill="#fff" stroke="#1A1D24" stroke-width="2"/>' + ''.join(f'<rect x="{80+(i%6)*7}" y="{38+(i//6)*7}" width="6" height="6" fill="#1A1D24"/>' for i in range(36) if (i * 7 + i // 6) % 3 != 1) + '<rect x="76" y="92" width="48" height="10" rx="5" fill="#4F8CFF"/>')
S['life'] = phone(64, 6, 72, 128, '<path d="M84 46l16-14 16 14v20H84z" fill="#FFB020"/><rect x="95" y="52" width="10" height="14" fill="#fff"/>' + ''.join(f'<rect x="74" y="{76+i*13}" width="9" height="9" rx="2" fill="{"#2F9E44" if i < 2 else "#E9ECF2"}"/><rect x="88" y="{78+i*13}" width="36" height="5" rx="2.5" fill="#D5DAE3"/>' for i in range(4)))
S['medical'] = phone(64, 6, 72, 128, '<rect x="72" y="20" width="56" height="36" rx="8" fill="#FFE3E8"/><path d="M96 28h8v8h8v8h-8v8h-8v-8h-8v-8h8z" fill="#E5484D"/>' + ''.join(f'<rect x="72" y="{64+i*14}" width="56" height="10" rx="5" fill="{["#E7F5FF", "#FFF4E6", "#EBFBEE"][i]}"/><circle cx="78" cy="{69+i*14}" r="2.5" fill="{["#4F8CFF", "#FFB020", "#2F9E44"][i]}"/>' for i in range(4 - 1)))
S['legal'] = page(54, 14, 92, 112, '<path d="M100 26v22M86 32h28M86 32l-6 12h12zM114 32l-6 12h12z" fill="none" stroke="#5C6BC0" stroke-width="2.5" stroke-linejoin="round"/>' + lines(64, 60, 5, 72, 9) + '<circle cx="124" cy="110" r="9" fill="#E5484D" opacity=".85"/>')
S['study'] = '<rect x="38" y="24" width="124" height="80" rx="7" fill="#1A1D24"/><rect x="43" y="29" width="114" height="70" rx="3" fill="#fff"/><rect x="50" y="36" width="40" height="7" rx="2" fill="#4F8CFF"/>' + lines(50, 50, 5, 58, 9) + '<rect x="114" y="40" width="36" height="46" rx="4" fill="#FFF3BF"/>' + lines(119, 48, 4, 26, 9, '#FAB005') + '<path d="M28 104h144l-8 10H36z" fill="#868E96"/>'
S['ipsi'] = phone(64, 6, 72, 128, T(74, 32, '합격 가능성', '#1A1D24', 9) + ''.join(f'<rect x="{76+i*13}" y="{96-h}" width="9" height="{h}" rx="2" fill="{c}"/>' for i, (h, c) in enumerate([(26, '#B5C8F5'), (40, '#91A7FF'), (56, '#4F8CFF'), (48, '#5C7CFA')])) + '<rect x="72" y="104" width="56" height="12" rx="6" fill="#2F9E44"/>' + T(89, 113, '안정', '#fff', 8))
S['dev'] = win(28, 18, 144, 106, '#343A46', ''.join(f'<rect x="{38+ind}" y="{36+i*10}" width="{w}" height="4.5" rx="2" fill="{c}"/>' for i, (ind, w, c) in enumerate([(0, 40, '#C792EA'), (10, 64, '#82AAFF'), (20, 48, '#C3E88D'), (20, 70, '#F78C6C'), (10, 30, '#82AAFF'), (0, 20, '#C792EA'), (0, 56, '#89DDFF'), (10, 40, '#C3E88D')])), dark=True)
S['net'] = '<rect x="38" y="30" width="124" height="74" rx="7" fill="#1A1D24"/><rect x="43" y="35" width="114" height="64" rx="3" fill="#E7F5FF"/>' + ''.join(f'<path d="M{100-r} {84-r*.55}a{r} {r} 0 0 1 {2*r} 0" fill="none" stroke="#1C7ED6" stroke-width="2.4" stroke-linecap="round"/>' for r in (12, 22, 32)) + '<circle cx="100" cy="86" r="3" fill="none" stroke="#1C7ED6" stroke-width="2.4"/><path d="M28 104h144l-8 10H36z" fill="#868E96"/>'
S['design'] = page(34, 16, 132, 108, '<circle cx="74" cy="58" r="22" fill="#FF6B6B"/><rect x="96" y="40" width="40" height="40" rx="8" fill="#4F8CFF"/><path d="M80 104l18-28 18 28z" fill="#FFB020"/>' + ''.join(f'<rect x="{46+i*16}" y="26" width="12" height="7" rx="2" fill="{c}"/>' for i, c in enumerate(['#FF6B6B', '#FFB020', '#2F9E44', '#4F8CFF', '#7048E8'])))
S['shop'] = phone(64, 6, 72, 128, '<rect x="72" y="18" width="56" height="10" rx="3" fill="#FF922B"/>' + ''.join(f'<rect x="{72+(i%2)*30}" y="{34+(i//2)*36}" width="26" height="30" rx="5" fill="{c}"/><rect x="{76+(i%2)*30}" y="{56+(i//2)*36}" width="16" height="4" rx="2" fill="#fff"/>' for i, c in enumerate(['#FFD8A8', '#C5F6FA', '#D0BFFF', '#B2F2BB'])) + '<rect x="72" y="108" width="56" height="10" rx="5" fill="#1A1D24"/>')
for k, b in S.items():
    open(os.path.join(out, f'sc-{k}.svg'), 'w').write(svg(SH + b))
print(len(S), 'scenes')

# 큰 색 카드용: 사람 일러스트 + 장면 그림 합성 (300x200)
import re as _re
SK = ['#F2C9A8', '#E8B48C', '#F6D5BC', '#D99E78']
HR = ['#2B2B33', '#5A3825', '#1E1E24', '#7A4A2A']
SH_ = ['#FFFFFF', '#FFE066', '#B2F2BB', '#FFC9C9', '#D0EBFF']
def person(x, y, sk, hr, sh, pants='#2F3A56', pose=0, long_hair=False):
    s = ''
    if long_hair:
        s += f'<path d="M{x-17} {y+6}q0-24 17-24t17 24v20h-34z" fill="{hr}"/>'
    s += f'<rect x="{x-12}" y="{y+62}" width="10" height="44" rx="5" fill="{pants}"/><rect x="{x+2}" y="{y+62}" width="10" height="44" rx="5" fill="{pants}"/>'
    s += f'<ellipse cx="{x-7}" cy="{y+106}" rx="9" ry="4" fill="#1A1D24"/><ellipse cx="{x+7}" cy="{y+106}" rx="9" ry="4" fill="#1A1D24"/>'
    s += f'<path d="M{x-18} {y+28}q0-10 10-10h16q10 0 10 10v38h-36z" fill="{sh}"/>'
    s += f'<rect x="{x-4}" y="{y+12}" width="8" height="8" fill="{sk}"/><circle cx="{x}" cy="{y+2}" r="14" fill="{sk}"/>'
    s += f'<path d="M{x-14} {y}q0-16 14-16t14 16q-6-7-14-7t-14 7z" fill="{hr}"/>'
    s += f'<circle cx="{x-5}" cy="{y+3}" r="1.6" fill="#2B2B33"/><circle cx="{x+5}" cy="{y+3}" r="1.6" fill="#2B2B33"/><path d="M{x-4} {y+9}q4 3 8 0" fill="none" stroke="#B5634B" stroke-width="1.6" stroke-linecap="round"/>'
    if pose == 0:  # 핸드폰 보기
        s += f'<path d="M{x+14} {y+26}l10 18-12 6" fill="none" stroke="{sh}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><rect x="{x+6}" y="{y+40}" width="11" height="18" rx="2.5" fill="#1A1D24"/><circle cx="{x+12}" cy="{y+50}" r="4" fill="{sk}"/>'
        s += f'<path d="M{x-15} {y+26}l-6 26" stroke="{sh}" stroke-width="9" stroke-linecap="round"/><circle cx="{x-21}" cy="{y+54}" r="4" fill="{sk}"/>'
    else:  # 손 들어 가리키기
        s += f'<path d="M{x+14} {y+26}l14-20" stroke="{sh}" stroke-width="9" stroke-linecap="round"/><circle cx="{x+30}" cy="{y+2}" r="4.5" fill="{sk}"/>'
        s += f'<path d="M{x-15} {y+26}l-6 26" stroke="{sh}" stroke-width="9" stroke-linecap="round"/><circle cx="{x-21}" cy="{y+54}" r="4" fill="{sk}"/>'
    return s
def pict(cx, cy, kind, c):
    g = {'star': f'<path d="M{cx} {cy-7}l2.2 4.6 5 .7-3.6 3.5.9 5-4.5-2.4-4.5 2.4.9-5-3.6-3.5 5-.7z" fill="{c}"/>',
         'check': f'<path d="M{cx-5} {cy}l3.5 3.5 6.5-7" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
         'heart': f'<path d="M{cx} {cy+6}l-6.5-6.5a4 4 0 0 1 6.5-4.6 4 4 0 0 1 6.5 4.6z" fill="{c}"/>',
         'bolt': f'<path d="M{cx+1} {cy-8}l-6 9h5l-1 7 6-9h-5z" fill="{c}"/>'}[kind]
    return f'<circle cx="{cx}" cy="{cy}" r="13" fill="#fff"/>{g}'
K = list(S.keys())
for i, k in enumerate(K + ['pop']):
    sc = S.get(k, S['excel'])
    p = person(62, 72, SK[i % 4], HR[i % 4], SH_[i % 5], pose=i % 2, long_hair=i % 3 == 1)
    pc = pict(36, 40, ['star', 'check', 'heart', 'bolt'][i % 4], ['#FFB020', '#2F9E44', '#E64980', '#4F8CFF'][i % 4]) + pict(268, 30, ['check', 'bolt', 'star', 'heart'][i % 4], ['#2F9E44', '#4F8CFF', '#FFB020', '#E64980'][i % 4])
    body = f'<g transform="translate(104 44) scale(.74)">{sc}</g>{p}'
    open(os.path.join(out, f'ft-{k}.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="18 26 248 172" width="300" height="200">{body}</svg>')
print('feature art done')

# 사람(상반신 크게) 카드 그림 + 선 픽토그램 카드 그림
def bust(i):
    sk, hr = SK[i % 4], HR[i % 4]
    sh = ['#E03131', '#1C7ED6', '#2F9E44', '#7048E8'][i % 4]
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" width="220" height="220">'
    if i % 2:
        s += f'<path d="M66 96q0-62 44-62t44 62v60H66z" fill="{hr}"/>'
    s += f'<path d="M30 220q0-62 50-70h60q50 8 50 70z" fill="{sh}"/>'
    s += f'<rect x="96" y="120" width="28" height="34" rx="10" fill="{sk}"/>'
    s += f'<ellipse cx="110" cy="96" rx="40" ry="46" fill="{sk}"/>'
    s += f'<path d="M70 92q-2-50 40-50t40 50q-10-24-40-26t-40 26z" fill="{hr}"/>'
    s += f'<ellipse cx="94" cy="100" rx="4" ry="5" fill="#2B2B33"/><ellipse cx="126" cy="100" rx="4" ry="5" fill="#2B2B33"/>'
    s += f'<path d="M92 118q18 16 36 0" fill="#fff" stroke="#B5634B" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<ellipse cx="82" cy="114" rx="7" ry="4" fill="#F28B82" opacity=".45"/><ellipse cx="138" cy="114" rx="7" ry="4" fill="#F28B82" opacity=".45"/>'
    s += f'<rect x="146" y="150" width="34" height="56" rx="7" fill="#1A1D24" transform="rotate(-12 163 178)"/><rect x="150" y="155" width="26" height="44" rx="4" fill="#7EC8FF" transform="rotate(-12 163 178)"/>'
    s += f'<circle cx="160" cy="200" r="10" fill="{sk}"/>'
    return s + '</svg>'
for i in range(4):
    open(os.path.join(out, f'pp-{i}.svg'), 'w').write(bust(i))
B = '#1C7ED6'
L = f'fill="none" stroke="{B}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
pic = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 160" width="220" height="160">'
       f'<rect x="20" y="20" width="44" height="58" rx="6" {L}/><path d="M30 36h24M30 46h24M30 56h14" {L}/>'
       f'<rect x="86" y="14" width="56" height="44" rx="6" {L}/><path d="M104 70h20M114 58v12" {L}/>'
       f'<rect x="164" y="18" width="32" height="54" rx="6" {L}/><path d="M176 64h8" {L}/>'
       f'<path d="M24 120a14 14 0 0 1 2-27 18 18 0 0 1 34 4 12 12 0 0 1 0 23z" {L}/>'
       f'<path d="M90 98h48v40H90zM90 110h48M106 98v40" {L}/>'
       f'<circle cx="182" cy="118" r="20" {L}/><path d="M172 118l7 7 13-14" {L}/>'
       f'<path d="M70 88l4 4M150 84l-4 4M74 140h4M150 140h4" {L}/></svg>')
open(os.path.join(out, 'picto.svg'), 'w').write(pic)
print('bust+picto')

# 라인 픽토그램 (흰 바탕 + 검은 선) — 원본 분류 아이콘에서 그림 부분만 선으로 바꿔 생성
import glob as _g
src = sys.argv[2] if len(sys.argv) > 2 else None
if src:
    for f in _g.glob(os.path.join(src, 'cat2-*.svg')):
        t = open(f).read()
        k = os.path.basename(f)[5:-4]
        body = _re.split(r'stroke-opacity="\.14"/>', t, 1)[-1].replace('</svg>', '')
        body = body.replace('stroke="#fff"', 'stroke="#1f2430"').replace('stroke-width="4.5"', 'stroke-width="3.2"')
        body = _re.sub(r'fill="#fff"', 'fill="none" stroke="#1f2430" stroke-width="3.2" stroke-linejoin="round"', body)
        body = _re.sub(r'(<text[^>]*?)fill="#[0-9A-Fa-f]{6}"', r'\1fill="#1f2430"', body)
        out_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">'
                   '<rect x="2" y="2" width="60" height="60" rx="14" fill="#fff" stroke="#1f2430" stroke-opacity=".18" stroke-width="2"/>' + body + '</svg>')
        open(os.path.join(out, f'pg-{k}.svg'), 'w').write(out_svg)
        wb = body.replace('#1f2430', '#fff')
        open(os.path.join(out, f'pgw-{k}.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="8 8 48 48" width="48" height="48">' + wb + '</svg>')
    print('line pictos')

# 분류 카드용: 그림 맨 윗선이 정확히 SVG 위쪽 끝에 오도록 잘라낸 버전 (cs-*.svg)
import subprocess, tempfile
try:
    from PIL import Image as _I
    for k in S:
        f = os.path.join(out, f'sc-{k}.svg')
        tmp = tempfile.mktemp(suffix='.png')
        full = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*4}" height="{H*4}">{S[k]}</svg>'
        tf = tempfile.mktemp(suffix='.svg'); open(tf, 'w').write(full)
        subprocess.run(['rsvg-convert', tf, '-o', tmp], check=True)
        im = _I.open(tmp).convert('RGBA'); bb = im.getbbox()
        x0, y0, x1, y1 = [v / 4 for v in bb]
        vb = f'{x0:.1f} {y0:.1f} {x1-x0:.1f} {y1-y0:.1f}'
        open(os.path.join(out, f'cs-{k}.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{x1-x0:.0f}" height="{y1-y0:.0f}">{S[k]}</svg>')
    print('tight scenes')
except Exception as e:
    print('tight scenes failed', e)
