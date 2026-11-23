"""정부 지원금(/life/subsidy.html) 항목을 정부24 상세 내용 기준으로 풀어 쓴 검색용 글 — 한 편씩 추가.
1) 근로·자녀장려금 (정부24 105100000001, 2026-11-10 수정본 · 2026-11-24 확인)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr
from invest_guides import CSS

E = cu.E
SITE = kr.SITE
GOV = 'https://www.gov.kr/portal/rcvfvrSvc/dtlEx/'

CSS2 = ('<style>.s-big{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0 4px}'
        '.s-big div{background:#F4F7FB;border-radius:14px;padding:12px 10px;text-align:center;line-height:1.4}'
        '.s-big small{display:block;font-size:13px;color:#5B6B82}.s-big b{display:block;font-size:22px;color:#1D4ED8;margin-top:2px}.s-big span{font-size:12.5px;color:#5B6B82}'
        '.s-dl{display:flex;gap:10px;align-items:center;background:#FFF1F0;border:1.5px solid #FCA5A5;border-radius:14px;padding:12px 14px;margin:12px 0 0;line-height:1.6}'
        '.s-dl b.d{flex:none;background:#DC2626;color:#fff;border-radius:10px;padding:6px 10px;font-size:15px}'
        '.g-calc select{width:100%;box-sizing:border-box;margin-top:5px;padding:12px;border:1.5px solid #CBD5E1;border-radius:12px;font-size:16px;background:#fff}'
        '.s-ok{display:inline-block;border-radius:999px;padding:2px 10px;font-size:13px;font-weight:800;background:#DCFCE7;color:#15803D}.s-no{background:#FEE2E2;color:#B91C1C}'
        '.s-gov{border:1.5px solid #CBD5E1;border-radius:14px;padding:4px 14px 10px;background:#fff}.s-gov h3{font-size:15px;margin:12px 0 4px;color:#1D4ED8}.s-gov p{margin:0;line-height:1.7;font-size:14.5px}'
        '@media(max-width:480px){.s-big{gap:6px}.s-big b{font-size:18px}.s-big div{padding:10px 4px}}</style>')


def crumb(title):
    items = [('홈', '/'), ('생활·행정', '/life/'), ('정부 지원금', '/life/subsidy.html')]
    html = '<p class="crumb">' + ' › '.join(f'<a href="{u}">{E(n)}</a>' for n, u in items) + ' › ' + E(title) + '</p>'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
    return html, ld


def eitc():
    path = '/life/subsidy/eitc.html'
    gid = '105100000001'
    title = '근로장려금·자녀장려금 자격·금액·신청 기간 (2026) — 기한후 신청 12월 1일 마감'
    cr, crld = crumb('근로·자녀장려금')
    rows = [('단독가구', '배우자·부양자녀·70세 이상 부모가 없는 가구', '2,200만 원 미만', '165만 원'),
            ('홑벌이가구', '배우자 총급여 등이 300만 원 미만이거나, 부양자녀·70세 이상 부모가 있는 가구', '3,200만 원 미만', '285만 원'),
            ('맞벌이가구', '본인과 배우자 모두 총급여 등이 300만 원 이상', '4,400만 원 미만', '330만 원')]
    tb = ''.join(f'<tr><td><b>{a}</b><br><span class="cu-src">{b}</span></td><td class="n">{c}</td><td class="n"><b>{d}</b></td></tr>' for a, b, c, d in rows)
    big = ('<div class="s-big"><div><small>단독</small><b>165만</b><span>소득 2,200만 미만</span></div>'
           '<div><small>홑벌이</small><b>285만</b><span>소득 3,200만 미만</span></div>'
           '<div><small>맞벌이</small><b>330만</b><span>소득 4,400만 미만</span></div></div>')
    dl = ('<p class="s-dl"><b class="d">12/1 마감</b><span>5월 정기신청을 놓쳤다면 <b>2026년 12월 1일까지 기한후 신청</b>하면 돼요. 금액의 <b>95%</b>를 받아요. 홈택스·손택스로 바로 신청할 수 있어요.</span></p>')
    calc = ('<section class="card" id="calc"><h2>내 근로·자녀장려금 바로 계산</h2>'
            '<p class="cu-src">2025년 소득(2026년 신청분) 기준이에요. 입력한 숫자는 이 기기에서만 계산돼요.</p>'
            '<div class="g-calc"><label>가구 유형<select id="et"><option value="single">단독가구</option><option value="one" selected>홑벌이가구</option><option value="two">맞벌이가구</option></select></label>'
            '<label>부부 합산 총소득 (연, 원)<input id="ei" inputmode="numeric" value="24,000,000"></label>'
            '<label>가구 재산 합계 (6월 1일, 원)<input id="ep" inputmode="numeric" value="150,000,000"></label>'
            '<label>18세 미만 부양자녀 수<input id="ek" inputmode="numeric" value="2"></label></div>'
            '<div class="g-out" id="eo"></div>'
            '<script>(function(){var g=function(i){return document.getElementById(i)},t=g("et"),i=g("ei"),p=g("ep"),k=g("ek"),o=g("eo");'
            'function n(x){return +String(x.value).replace(/[^0-9]/g,"")||0}function f(x){return Math.round(x/1e3)*1e3}function w(x){return f(x).toLocaleString("ko-KR")+"원"}'
            'function r(){var ty=t.value,inc=n(i),pr=n(p),kd=Math.min(20,n(k));'
            'var P={single:{a:4e6,b:9e6,c:2.2e7,m:1.65e6},one:{a:7e6,b:1.4e7,c:3.2e7,m:2.85e6},two:{a:8e6,b:1.7e7,c:4.4e7,m:3.3e6}}[ty];'
            'var e=inc>=P.c?0:inc<P.a?P.m*inc/P.a:inc<=P.b?P.m:P.m*(P.c-inc)/(P.c-P.b),c=0,cb=ty==="two"?2.5e7:2.1e7,note="";'
            'if(ty!=="single"&&kd>0&&inc<7e7){c=(inc<cb?1e6:1e6-(inc-cb)*(5e5/(7e7-cb)))*kd}'
            'if(pr>=2.4e8){e=0;c=0;note="재산이 2억 4천만 원 이상이라 받을 수 없어요."}else if(pr>=1.7e8){e*=.5;c*=.5;note="재산이 1억 7천만 원 이상이라 50%만 받아요."}'
            'e=f(e);c=f(c);var ok=function(b){return "<span class=\\"s-ok"+(b?"":" s-no")+"\\">"+(b?"통과":"초과")+"</span>"};'
            'o.innerHTML="소득 기준 "+ok(inc<P.c)+" · 재산 기준 "+ok(pr<2.4e8)+"<br>근로장려금 "+w(e)+(ty==="single"?"":" · 자녀장려금 "+w(c))'
            '+"<br>예상 합계 <b>"+w(e+c)+"</b>"+(e+c>0?"<br>지금(기한후 신청) 신청하면 95%인 약 "+w((e+c)*.95)+"을 받아요.":"")+(note?"<br>"+note:"")+(ty==="single"&&kd>0?"<br>부양자녀가 있으면 단독이 아니라 홑벌이가구로 골라 주세요.":"")}'
            '[i,p,k].forEach(function(e){e.addEventListener("input",function(){var v=n(e);e.value=v?v.toLocaleString("ko-KR"):(e===k?"0":"");r()})});t.addEventListener("change",r);r()})();</script>'
            '<p class="cu-src">국세청 산정표를 구간별 직선으로 단순화한 추정치예요. 최종 금액은 홈택스 신청 화면이나 국세청 안내문의 금액이 기준이에요.</p>'
            '<a class="g-cta" href="/life/invest.html#eitc">다른 세금·연금 계산기와 함께 보기 →</a></section>')
    sched = [('정기신청', '2026년 5월 1일 ~ 6월 1일', '2026년 8월 말 (8월 27일 지급)', '100%'),
             ('기한후 신청', '2026년 6월 2일 ~ <b>12월 1일</b>', '신청 후 약 4개월 안', '95%'),
             ('반기신청 (상반기분)', '2026년 9월 1일 ~ 15일', '2026년 12월 (35% 먼저)', '근로소득만'),
             ('반기신청 (하반기분)', '2027년 3월 1일 ~ 15일', '2027년 6월 (정산)', '근로소득만'),
             ('다음 정기신청', '2027년 5월 (2026년 소득분)', '2027년 8월 말', '100%')]
    st = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td class="n">{d}</td></tr>' for a, b, c, d in sched)
    main = (CSS + CSS2 + f'<header class="top hub">{cr}<h1>근로장려금·자녀장려금 자격·금액·신청 기간 (2026년 기준)</h1>'
            '<p class="lead">정부24 보조금24의 국세청 안내를 바탕으로 누가 받는지, 얼마나 받는지, 언제 어디서 신청하는지 표와 계산기로 풀었어요.</p>'
            '<p class="cu-ans">근로장려금은 일은 하지만 소득이 적은 가구에 <b>현금으로 최대 330만 원</b>을 주는 제도예요. 2025년 부부 합산 총소득이 '
            '<b>단독 2,200만·홑벌이 3,200만·맞벌이 4,400만 원 미만</b>이고 6월 1일 가구 재산이 <b>2억 4천만 원 미만</b>이면 받을 수 있어요. '
            '18세 미만 자녀가 있고 총소득이 7,000만 원 미만이면 <b>자녀 1명당 최대 100만 원</b>의 자녀장려금도 함께 받아요.</p>'
            + big + dl +
            '<ul class="dr-toc"><li><a href="#calc">바로 계산</a></li><li><a href="#who">자격 기준표</a></li><li><a href="#child">자녀장려금</a></li><li><a href="#when">신청 기간</a></li><li><a href="#how">신청 방법</a></li><li><a href="#gov">정부24 원문</a></li></ul></header>'
            + calc
            + '<section class="card" id="who"><h2>가구 유형별 근로장려금 소득 기준과 최대 금액</h2><div style="overflow-x:auto"><table class="g-tb"><thead><tr><th>가구 유형</th><th>총소득 기준</th><th>최대 금액</th></tr></thead><tbody>'
            + tb + '</tbody></table></div>'
              '<ul class="cu-chk"><li><b>총소득</b>은 부부의 근로·사업·종교인·이자·배당·연금·기타소득을 모두 합친 금액이에요(비과세 소득은 빼요).</li>'
              '<li><b>재산</b>은 6월 1일 기준 가구원 전체의 주택·토지·건물·자동차·전세보증금·예금·주식 등을 합쳐요. 대출이 있어도 빼지 않아요. <b>1억 7천만 원 이상 2억 4천만 원 미만이면 50%만</b> 받아요.</li>'
              '<li>12월 31일 기준 <b>대한민국 국적</b>이어야 하고(외국인은 한국인 배우자나 부양자녀가 있으면 가능), 다른 사람의 부양자녀이거나 전문직 사업자면 받을 수 없어요.</li>'
              '<li>금액은 소득이 너무 적어도, 기준에 가까워도 줄어들어요. 소득 구간 가운데쯤일 때 최대 금액을 받아요.</li></ul></section>'
            + '<section class="card" id="child"><h2>자녀장려금은 자녀 1명당 50만~100만 원</h2><ul class="cu-chk">'
              '<li><b>대상</b>: 18세 미만 부양자녀가 있는 홑벌이·맞벌이가구(단독가구는 자녀가 없으니 대상이 아니에요).</li>'
              '<li><b>소득 기준</b>: 부부 합산 총소득 <b>7,000만 원 미만</b>. 재산 기준은 근로장려금과 같아요(2억 4천만 원 미만).</li>'
              '<li><b>금액</b>: 자녀 1명당 최소 50만 원, 최대 100만 원. 소득이 낮을수록 100만 원에 가까워요.</li>'
              '<li>근로장려금과 <b>함께 신청</b>하는 구조라 따로 신청할 필요가 없어요. 단, 자녀장려금은 <b>반기신청이 없고</b> 5월 정기신청(또는 기한후 신청)만 돼요.</li></ul></section>'
            + '<section class="card" id="when"><h2>신청 기간과 지급일 (2026~2027)</h2><div style="overflow-x:auto"><table class="g-tb"><thead><tr><th>구분</th><th>신청 기간</th><th>지급</th><th>받는 비율</th></tr></thead><tbody>'
            + st + '</tbody></table></div>'
              '<p class="g-warn">반기신청은 <b>근로소득만 있는 사람</b>의 근로장려금만 돼요. 9월에 상반기분을 신청했다면 3월 하반기분은 따로 신청하지 않아도 신청한 것으로 봐요. 반기 지급액은 나중에 정산되어 많이 받았다면 다음 지급분에서 빠질 수 있어요.</p></section>'
            + '<section class="card" id="how"><h2>신청 방법 (홈택스·손택스·ARS)</h2><ol class="g-st">'
              '<li><b>국세청 안내문을 받았다면</b>: 안내문의 <b>개별인증번호</b>로 ARS <b>1544-9944</b>에 전화하거나, 손택스(모바일 홈택스)에서 몇 번 눌러 신청해요.</li>'
              '<li><b>안내문을 못 받았다면</b>: 홈택스(PC)·손택스에 로그인 → <b>장려금·연말정산·전자기부금</b> → <b>근로·자녀장려금</b> → 신청하기. 소득·재산은 국세청이 대부분 불러와요.</li>'
              '<li><b>계좌를 확인</b>해요. 신청할 때 넣은 본인 계좌로 들어오고, 계좌가 없으면 우편 국세환급금 통지서로 받아요.</li>'
              '<li>서면으로 내려면 가까운 세무서에 신청서를 내요. 진행 상황은 홈택스 <b>심사 진행 상황 조회</b>에서 볼 수 있어요.</li></ol>'
              '<a class="g-cta" href="https://www.hometax.go.kr" target="_blank" rel="noopener">홈택스에서 신청하기 →</a>'
              '<p class="cu-src" style="text-align:center">상담: 장려금 상담센터 1566-3636 · 국세청 126</p></section>'
            + f'<section class="card" id="gov"><h2>정부24(보조금24)에 올라온 내용</h2><div class="s-gov">'
              '<h3>제도 목적</h3><p><b>근로장려세제</b>는 근로·사업·종교인 소득에 따라 계산한 근로장려금을 환급 형태로 지급해 저소득 가구의 근로를 장려하고 실질소득을 지원하는 근로연계형 소득지원 제도예요. '
              '<b>자녀장려세제</b>는 저소득 가구의 소득과 부양자녀 수에 따라 자녀장려금을 세금 환급 형태로 지급해 근로와 출산을 장려하는 제도로 2015년부터 시행했어요.</p>'
              '<h3>신청기간</h3><p>정기신청 5월 1일 ~ 5월 31일 · 반기신청 상반기분 9월 1일 ~ 15일, 하반기분 3월 1일 ~ 15일 (2026년은 5월 31일이 일요일이라 6월 1일까지)</p>'
              '<h3>신청방법</h3><p>개별 신청 안내를 받은 경우 ARS 1544-9944, 홈택스(모바일·PC), 서면 신청. 안내를 받지 않은 경우 홈택스(모바일·PC), 서면 신청</p>'
              '<h3>지원형태 · 소관기관</h3><p>현금 · 국세청 (문의: 관할 세무서)</p>'
              '<h3>근거 법령</h3><p>조세특례제한법 제100조의2 ~ 제100조의13(근로장려세제), 제100조의27 ~ 제100조의31(자녀장려세제)</p></div>'
              f'<p class="cu-src">정부24 최종수정일 2026년 11월 10일 · <a href="{GOV}{gid}" target="_blank" rel="noopener">정부24 원문 보기</a></p></section>')
    qa = [('근로장려금 기한후 신청은 언제까지예요?', '2025년 소득분은 2026년 12월 1일까지예요. 정기신청 금액의 95%를 받고, 신청 후 약 4개월 안에 지급돼요.'),
          ('근로장려금은 최대 얼마예요?', '단독가구 165만 원, 홑벌이가구 285만 원, 맞벌이가구 330만 원이에요.'),
          ('맞벌이 소득 기준이 올랐나요?', '네. 2026년 신청분(2025년 소득)부터 맞벌이가구 총소득 기준이 3,800만 원에서 4,400만 원 미만으로 올랐어요.'),
          ('재산이 2억 원이면 받을 수 있나요?', '받을 수 있어요. 다만 1억 7천만 원 이상 2억 4천만 원 미만이면 계산된 금액의 50%만 받아요.'),
          ('전세보증금도 재산에 들어가요?', '네. 전세보증금(또는 간주 전세금)·주택·자동차·예금·주식 등을 합치고, 대출은 빼지 않아요.'),
          ('자녀장려금도 반기신청이 되나요?', '아니요. 반기신청은 근로소득만 있는 사람의 근로장려금만 돼요. 자녀장려금은 5월 정기신청이나 기한후 신청으로 받아요.'),
          ('2027년부터 바뀌는 게 있나요?', '정부 세제개편안에는 단독가구 소득 기준 2,600만 원, 최대 금액 180만·310만·360만 원으로 올리는 안이 들어 있어요. 국회 통과 여부에 따라 달라질 수 있어요.')]
    fq, fqld = cu.faq(qa)
    main += fq
    main += ('<section class="card"><h2>출처와 안내</h2><p class="cu-src">출처: 정부24 보조금24 「근로·자녀장려금」(국세청, 최종수정 2026년 11월 10일), 국세청 근로·자녀장려금 안내, 조세특례제한법 제100조의2~제100조의31, 2026년 세제개편안 · 확인 2026년 11월 24일.<br>'
             '이 글은 제도를 쉽게 정리한 참고 자료예요. 실제 자격과 금액은 국세청 심사 결과가 기준이니 홈택스나 장려금 상담센터(1566-3636)에 확인하세요.</p></section>'
             '<section class="card"><h2>함께 보면 좋은 글</h2><ul class="cu-chk">'
             '<li><a href="/life/subsidy.html">조건으로 찾는 정부 지원금 (1만여 건)</a></li><li><a href="/life/invest.html#eitc">근로·자녀장려금 계산기</a></li>'
             '<li><a href="/life/invest/pension-tax-credit.html">연금저축·IRP 세액공제 한도와 환급액</a></li><li><a href="/life/invest.html#yet">연말정산 환급 계산기</a></li></ul></section>')
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "근로·자녀장려금 홈택스 신청 방법",
             "step": [{"@type": "HowToStep", "position": 1, "text": "국세청 안내문의 개별인증번호로 ARS 1544-9944나 손택스에서 신청한다."},
                      {"@type": "HowToStep", "position": 2, "text": "안내문이 없으면 홈택스 장려금·연말정산·전자기부금 메뉴에서 근로·자녀장려금을 신청한다."},
                      {"@type": "HowToStep", "position": 3, "text": "지급받을 본인 계좌를 확인하고 심사 진행 상황을 조회한다."}]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "datePublished": "2026-11-24", "dateModified": "2026-11-24",
           "author": {"@type": "Organization", "name": "홍라이프"}, "publisher": {"@type": "Organization", "name": "홍라이프"}, "mainEntityOfPage": SITE + path}
    kr.write(path, title + ' | 홍라이프 도구',
             '근로장려금 단독 2,200만·홑벌이 3,200만·맞벌이 4,400만 원 미만이면 최대 165만·285만·330만 원, 자녀장려금 1명당 최대 100만 원. 재산 2억 4천만 원 미만. 기한후 신청 12월 1일 마감(95%), 내 금액 바로 계산, 홈택스·ARS 신청 방법.',
             main, [crld, fqld, howto, art])
    return path


GUIDES = [('/life/subsidy/eitc.html', '근로·자녀장려금 자격·금액·신청 기간 (2026)', '단독 165만·홑벌이 285만·맞벌이 330만 원, 기한후 신청 12월 1일 마감, 내 금액 바로 계산',
           '근로장려금 자녀장려금 기한후 신청 근로장려금 자격 소득 기준 재산 기준 맞벌이 4400만원 근로장려금 지급일 반기신청 홈택스 신청 ARS 1544-9944', '105100000001')]

if __name__ == '__main__':
    print(eitc())
