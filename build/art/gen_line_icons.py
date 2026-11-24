#!/usr/bin/env python3
"""분류 첫 화면(머리) 그림 — 채우기 없이 선만, 한 가지 색 (ln-*.svg).
python3 build/art/gen_line_icons.py  → overlay/assets/art/hl/ln-*.svg"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'overlay/assets/art/hl')
C = '#1E2A44'
HEAD = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 90" width="120" height="90" fill="none" stroke="{C}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">'
PAGE = '<path d="M34 10h38l16 16v54a4 4 0 0 1-4 4H34a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4z"/><path d="M72 10v16h16"/>'
I = {
 'excel': '<rect x="22" y="14" width="76" height="62" rx="6"/><path d="M22 30h76M22 46h76M22 62h76M46 30v46M72 30v46"/><path d="M30 22h8M44 20l4 4M48 20l-4 4"/>',
 'sheet': '<rect x="16" y="16" width="56" height="58" rx="5"/><path d="M16 32h56M16 48h56M36 32v42M54 32v42"/><path d="M82 74V52M92 74V40M102 74V58"/><path d="M78 74h28"/>',
 'doc': PAGE + '<path d="M40 36h30M40 46h38M40 56h38M40 66h22"/>',
 'pdf': PAGE + '<rect x="38" y="36" width="34" height="16" rx="3"/><path d="M40 62h38M40 70h26"/>',
 'image': '<rect x="18" y="14" width="84" height="62" rx="7"/><circle cx="80" cy="32" r="7"/><path d="M18 66l24-24 18 18 12-10 30 22"/>',
 'convert': '<rect x="10" y="20" width="34" height="46" rx="4"/><rect x="76" y="20" width="34" height="46" rx="4"/><path d="M18 34h18M18 44h18M84 34h18M84 44h18"/><path d="M52 43h18M62 35l8 8-8 8"/>',
 'text': '<path d="M26 18h40M46 18v52"/><path d="M76 40h22M76 52h22M76 64h14"/>',
 'ai': '<path d="M20 18h62a6 6 0 0 1 6 6v30a6 6 0 0 1-6 6H44l-14 12V60H20a6 6 0 0 1-6-6V24a6 6 0 0 1 6-6z"/><path d="M98 8l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/><path d="M30 34h40M30 44h26"/>',
 'calendar': '<rect x="18" y="18" width="84" height="60" rx="7"/><path d="M18 34h84M40 10v14M80 10v14"/><path d="M34 48h4M50 48h4M66 48h4M82 48h4M34 62h4M50 62h4M66 62h4"/>',
 'qr': '<rect x="22" y="12" width="22" height="22" rx="3"/><rect x="76" y="12" width="22" height="22" rx="3"/><rect x="22" y="56" width="22" height="22" rx="3"/><path d="M58 14v10M58 34v12h12M80 46h18M58 58h10v18M80 60v18h18M90 60v6"/>',
 'life': '<path d="M18 44L60 10l42 34"/><path d="M28 38v40h64V38"/><path d="M52 78V56h16v22"/>',
 'gov': '<path d="M14 32L60 10l46 22z"/><path d="M22 38v32M42 38v32M60 38v32M78 38v32M98 38v32"/><path d="M12 78h96"/>',
 'drive': '<path d="M16 58V46l10-20h68l10 20v12a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4z"/><path d="M16 46h88"/><circle cx="34" cy="64" r="8"/><circle cx="86" cy="64" r="8"/>',
 'driver': '<rect x="16" y="32" width="88" height="34" rx="6"/><path d="M32 32V12h56v20"/><path d="M32 54h56v24H32z"/><path d="M40 64h40M40 72h26"/><circle cx="92" cy="44" r="2"/>',
 'medical': '<path d="M60 78C30 60 16 46 16 30a18 18 0 0 1 32-11 15 15 0 0 1 12 6 15 15 0 0 1 12-6 18 18 0 0 1 32 11c0 16-14 30-44 48z"/><path d="M26 42h18l6-10 10 20 6-10h28"/>',
 'legal': '<path d="M60 12v62M38 78h44M28 24h64"/><path d="M28 24l-14 30h28z"/><path d="M92 24L78 54h28z"/>',
 'study': '<path d="M60 22c-12-8-28-10-44-8v56c16-2 32 0 44 8 12-8 28-10 44-8V14c-16-2-32 0-44 8z"/><path d="M60 22v56"/>',
 'ipsi': '<path d="M60 14L10 36l50 22 50-22z"/><path d="M30 46v18c8 8 22 12 30 12s22-4 30-12V46"/><path d="M104 38v24"/>',
 'test': '<circle cx="60" cy="45" r="32"/><path d="M48 36a12 12 0 1 1 18 10c-4 3-6 5-6 10"/><path d="M60 66v1"/>',
 'game': '<path d="M36 26h48a22 22 0 0 1 22 22v4a14 14 0 0 1-26 7l-4-6H44l-4 6a14 14 0 0 1-26-7v-4a22 22 0 0 1 22-22z"/><path d="M34 40v12M28 46h12"/><path d="M82 42h1M90 50h1"/>',
 'dev': '<rect x="14" y="14" width="92" height="62" rx="7"/><path d="M14 28h92"/><path d="M46 40l-12 10 12 10M74 40l12 10-12 10M64 36l-8 30"/>',
 'net': '<path d="M14 36a66 66 0 0 1 92 0"/><path d="M28 50a46 46 0 0 1 64 0"/><path d="M42 64a26 26 0 0 1 36 0"/><path d="M60 78h1"/>',
 'design': '<path d="M60 10c-28 0-46 18-46 38 0 14 10 24 24 24 8 0 10-6 10-10 0-6 6-8 10-8h10c16 0 24-10 24-20 0-14-14-24-32-24z"/><path d="M38 40h1M52 26h1M72 26h1M86 40h1"/>',
 'shop': '<path d="M14 30l8-18h76l8 18"/><path d="M14 30c0 8 6 12 12 12s12-4 12-12c0 8 6 12 11 12s11-4 11-12c0 8 6 12 11 12s11-4 11-12c0 8 6 12 12 12s12-4 12-12"/><path d="M22 42v36h76V42"/><path d="M50 78V58h20v20"/>',
 'hwp': PAGE + '<path d="M53 33h14M46 41h28"/><circle cx="60" cy="56" r="8"/><path d="M40 72h40"/>',
}
if __name__ == '__main__':
    for k, v in I.items():
        open(os.path.join(OUT, f'ln-{k}.svg'), 'w', encoding='utf-8').write(HEAD + v + '</svg>\n')
    print('line icons', len(I))
