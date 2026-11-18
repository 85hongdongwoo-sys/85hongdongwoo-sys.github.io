# 분류 목록 카드용 항목별 썸네일 (200x140). 항목마다 다른 색·그림.
# 그림은 48x48 좌표의 선 아이콘(흰색) + 아래 작은 장식
ICON = {
 'burnout': '<rect x="6" y="14" width="32" height="20" rx="4"/><path d="M38 20v8"/><rect x="10" y="18" width="6" height="12" rx="1.5" fill="#fff"/>',
 'attachment': '<path d="M17 36s-11-7-11-15a6 6 0 0 1 11-3 6 6 0 0 1 11 3"/><path d="M31 40s-11-7-11-15a6 6 0 0 1 11-3 6 6 0 0 1 11 3c0 8-11 15-11 15z"/>',
 'spending': '<rect x="6" y="14" width="36" height="24" rx="4"/><path d="M6 20h36"/><circle cx="34" cy="29" r="2.5" fill="#fff"/>',
 'hsp': '<path d="M24 8c-8 6-12 14-12 22a12 12 0 0 0 24 0c0-8-4-16-12-22z"/><path d="M24 22v16"/>',
 'happiness': '<circle cx="24" cy="24" r="9"/><path d="M24 6v4M24 38v4M6 24h4M38 24h4M11 11l3 3M34 34l3 3M11 37l3-3M34 14l3-3"/>',
 'smartphone': '<rect x="14" y="6" width="20" height="36" rx="4"/><path d="M21 36h6"/><path d="M19 15h10M19 21h7"/>',
 'career': '<rect x="7" y="16" width="34" height="24" rx="4"/><path d="M18 16v-4a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v4M7 26h34"/>',
 'temperament': '<circle cx="16" cy="16" r="7"/><circle cx="32" cy="16" r="7"/><circle cx="16" cy="32" r="7"/><circle cx="32" cy="32" r="7" fill="#fff"/>',
 'brain': '<path d="M24 9v30M24 12c-3-4-11-3-12 3-5 1-6 8-2 11-3 4 0 10 5 10 2 3 7 4 9 0"/><path d="M28 18h6M28 25h8M28 32h5"/>',
 'mental-age': '<rect x="10" y="24" width="28" height="14" rx="3"/><path d="M10 31h28M18 24v-6M24 24v-6M30 24v-6"/><path d="M18 14c0-2 1-3 0-5M24 14c0-2 1-3 0-5M30 14c0-2 1-3 0-5"/>',
 'love-style': '<path d="M24 40S8 30 8 19a8 8 0 0 1 16-3 8 8 0 0 1 16 3c0 11-16 21-16 21z"/><path d="M18 21l4 4 8-8"/>',
 'conflict': '<path d="M6 10h20v13H14l-6 5v-5H6z"/><path d="M42 20H24v13h10l6 5v-5h2z"/>',
 'depression': '<path d="M14 30a8 8 0 0 1 1-16 11 11 0 0 1 21 3 7 7 0 0 1-1 13z"/><path d="M17 36l-2 5M25 36l-2 5M33 36l-2 5"/>',
 'maple-auction-fee': '<ellipse cx="24" cy="16" rx="14" ry="6"/><path d="M10 16v8c0 3 6 6 14 6s14-3 14-6v-8M10 24v8c0 3 6 6 14 6s14-3 14-6v-8"/>',
 'lostark-auction': '<path d="M10 38h20"/><path d="M15 20l10-10 8 8-10 10z"/><path d="M28 23l12 12"/>',
 'market-fee': '<path d="M12 6h24v36l-4-3-4 3-4-3-4 3-4-3-4 3z"/><path d="M19 30l10-12"/><circle cx="19" cy="19" r="2"/><circle cx="29" cy="29" r="2"/>',
 'gacha': '<circle cx="24" cy="24" r="16"/><path d="M8 24h32"/><circle cx="24" cy="24" r="4" fill="#fff"/>',
 'enhance': '<path d="M24 6l5 11 12 1-9 8 3 12-11-6-11 6 3-12-9-8 12-1z"/>',
 'edpi': '<circle cx="24" cy="24" r="13"/><circle cx="24" cy="24" r="3" fill="#fff"/><path d="M24 4v10M24 34v10M4 24h10M34 24h10"/>',
 'bowling': '<path d="M24 6c-4 0-5 4-4 8 1 3-6 9-6 17 0 6 4 11 10 11s10-5 10-11c0-8-7-14-6-17 1-4 0-8-4-8z"/><path d="M19 16h10"/>',
 'winrate': '<path d="M15 8h18v8a9 9 0 0 1-18 0z"/><path d="M15 11H9a6 6 0 0 0 6 7M33 11h6a6 6 0 0 1-6 7M24 25v8M17 40h14M19 33h10v7H19z"/>',
}
COL = {
 'burnout': ('#FF8A65', '#FFE3D9'), 'attachment': ('#EC6A9C', '#FDE0EB'), 'spending': ('#F2A93B', '#FDEFD6'), 'hsp': ('#7BB662', '#E4F2DC'),
 'happiness': ('#F5B700', '#FFF3C4'), 'smartphone': ('#4C8DF6', '#DDE9FE'), 'career': ('#2E9C8F', '#D6F0EC'), 'temperament': ('#9A6DD7', '#ECE2F8'),
 'brain': ('#E2785A', '#FBE3DB'), 'mental-age': ('#36A3D9', '#DBEFF9'), 'love-style': ('#E5546E', '#FCDDE2'), 'conflict': ('#5C7CFA', '#E0E6FE'),
 'depression': ('#6C8EAD', '#E2EAF1'),
 'maple-auction-fee': ('#F08C00', '#FFE9C7'), 'lostark-auction': ('#8E6C3A', '#F1E6D4'), 'market-fee': ('#1098AD', '#D3F0F4'), 'gacha': ('#D6336C', '#FBDDE8'),
 'enhance': ('#F59F00', '#FFF0C2'), 'edpi': ('#2F9E44', '#D9F2DE'), 'bowling': ('#5F3DC4', '#E5DEFA'), 'winrate': ('#C08A00', '#FBEFC9'),
}

SHORT={}
def thumb_old(slug, title):
    c, bg = COL[slug]
    ic = ICON[slug].replace('fill="#fff"', f'fill="#fff"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 140" width="200" height="140">'
            f'<rect width="200" height="140" fill="{bg}"/>'
            f'<circle cx="168" cy="20" r="46" fill="{c}" fill-opacity=".13"/><circle cx="22" cy="128" r="34" fill="{c}" fill-opacity=".12"/>'
            f'<rect x="64" y="30" width="72" height="72" rx="22" fill="{c}"/>'
            f'<g transform="translate(76 42)" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{ic}</g>'
            f'<rect x="54" y="112" width="92" height="7" rx="3.5" fill="{c}" fill-opacity=".28"/><rect x="54" y="112" width="{30 + (sum(map(ord, slug)) % 55)}" height="7" rx="3.5" fill="{c}"/>'
            f'</svg>')

def thumb(slug, title):
    c, bg = COL[slug]
    lab = title.split(' (')[0].replace(' 테스트','').replace(' 계산기','')[:9]
    btn = '결과 보기' if slug in ICON and slug not in GAME_SLUGS else '계산하기'
    ic = ICON[slug]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="64.0 6.0 72.0 128.0" width="72" height="128"><g>'
            '<rect x="64" y="6" width="72" height="128" rx="12" fill="#1A1D24"/><rect x="68" y="10" width="64" height="120" rx="9" fill="#fff"/><rect x="91.0" y="13" width="18" height="4" rx="2" fill="#1A1D24"/>'
            f'<text x="74" y="32" font-family="Arial,Helvetica,sans-serif" font-size="8.5" font-weight="700" fill="#1A1D24">{lab}</text>'
            f'<rect x="76" y="40" width="48" height="48" rx="13" fill="{c}"/>'
            f'<g transform="translate(78 42) scale(.917)" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">{ic}</g>'
            f'<rect x="74" y="94" width="52" height="5" rx="2.5" fill="{bg}"/><rect x="74" y="94" width="{20 + (sum(map(ord, slug)) % 30)}" height="5" rx="2.5" fill="{c}"/>'
            f'<rect x="72" y="106" width="56" height="12" rx="6" fill="{c}"/><text x="{100 - len(btn)*4.2}" y="114.6" font-family="Arial,Helvetica,sans-serif" font-size="8" font-weight="700" fill="#fff">{btn}</text>'
            '</g></svg>')
GAME_SLUGS = {'maple-auction-fee','lostark-auction','market-fee','gacha','enhance','edpi','bowling','winrate'}
