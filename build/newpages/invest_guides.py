"""투자계산기(/life/invest.html) 탭 내용을 검색용 글 페이지로 꺼냄 — 한 편씩 추가.
1) 해외주식 양도세 (2026-11-23 확인: 250만 원 공제·22%·결제일 기준·RIA 2026 한시)
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_update as cu
import driver_pages as kr

E = cu.E
SITE = kr.SITE


def crumb(title):
    items = [('홈', '/'), ('생활·행정', '/life/'), ('투자계산기', '/life/invest.html')]
    html = '<p class="crumb">' + ' › '.join(f'<a href="{u}">{E(n)}</a>' for n, u in items) + ' › ' + E(title) + '</p>'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
    return html, ld


CSS = ('<style>.g-cta{display:block;text-align:center;background:#1D4ED8;color:#fff!important;font-weight:800;font-size:17px;padding:15px 16px;border-radius:14px;text-decoration:none;margin:14px 0 4px}'
       '.g-tb{width:100%;border-collapse:collapse;font-size:15px}.g-tb th,.g-tb td{border-bottom:1px solid #E9EDF3;padding:10px 8px;text-align:left;word-break:keep-all}.g-tb th{font-size:13px;color:#5B6B82}.g-tb td.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}'
       '.g-calc{display:grid;grid-template-columns:1fr 1fr;gap:10px}.g-calc label{font-size:13.5px;color:#4A5568;display:block}.g-calc input{width:100%;box-sizing:border-box;margin-top:5px;padding:12px;border:1.5px solid #CBD5E1;border-radius:12px;font-size:17px;font-variant-numeric:tabular-nums}'
       '.g-out{margin-top:12px;background:#EEF4FF;border-radius:14px;padding:14px 16px;font-size:15px;line-height:1.7}.g-out b{font-size:22px;color:#1D4ED8}'
       '.g-st{counter-reset:s;list-style:none;padding:0;margin:0}.g-st li{position:relative;padding:0 0 12px 40px;line-height:1.7}.g-st li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;background:#1D4ED8;color:#fff;font-weight:800;text-align:center;line-height:28px}'
       '.g-warn{background:#FFF7E6;border-radius:12px;padding:12px 14px;line-height:1.7;font-size:14.5px}'
       '@media(max-width:480px){.g-calc{grid-template-columns:1fr}.g-tb{font-size:14px}.g-tb th,.g-tb td{padding:9px 5px}}</style>')


def won(n):
    return f'{n:,}원'


def us_tax():
    path = '/life/invest/us-stock-tax.html'
    title = '해외주식 양도세 계산·연말 절세 (2026) — 250만 원 공제, 22%, 결제일 기준, RIA 계좌'
    cr, crld = crumb('해외주식 양도세')
    rows = [(2_000_000,), (5_000_000,), (8_000_000,), (10_000_000,), (20_000_000,), (50_000_000,)]
    tb = ''.join(f'<tr><td class="n" style="text-align:left">{p // 10000:,}만 원</td><td class="n">{won(max(0, p - 2_500_000))}</td><td class="n"><b>{won(round(max(0, p - 2_500_000) * .22))}</b></td></tr>' for (p,) in rows)
    calc = ('<section class="card" id="calc"><h2>내 해외주식 양도세 바로 계산</h2>'
            '<p class="cu-src">올해(결제일 기준) 판 해외주식의 이익과 손실을 원화로 넣으세요. 입력한 숫자는 이 기기에서만 계산돼요.</p>'
            '<div class="g-calc"><label>이익 본 종목 합계 (원)<input id="gp" inputmode="numeric" value="8,000,000"></label>'
            '<label>손해 본 종목 합계 (원, 양수로)<input id="gl" inputmode="numeric" value="0"></label></div>'
            '<div class="g-out" id="go"></div>'
            '<script>(function(){var p=document.getElementById("gp"),l=document.getElementById("gl"),o=document.getElementById("go");'
            'function n(x){return +String(x.value).replace(/[^0-9]/g,"")||0}function f(x){return x.toLocaleString("ko-KR")+"원"}'
            'function r(){var net=n(p)-n(l),base=Math.max(0,net-2500000),tax=Math.round(base*.22),room=Math.max(0,2500000-Math.max(0,net));'
            'o.innerHTML="순이익 "+f(net)+" − 기본공제 250만 원 = 과세표준 "+f(base)+"<br>예상 세금 <b>"+f(tax)+"</b> (양도소득세 "+f(Math.round(base*.2))+" + 지방소득세 "+f(tax-Math.round(base*.2))+")"'
            '+(room>0?"<br>올해 공제가 <b style=\\"font-size:16px\\">"+f(room)+"</b> 남았어요. 연말 전에 이익을 더 실현해도 이만큼은 세금이 없어요.":"")}'
            '[p,l].forEach(function(e){e.addEventListener("input",function(){var v=n(e);e.value=v?v.toLocaleString("ko-KR"):"";r()})});r()})();</script>'
            '<a class="g-cta" href="/life/invest.html#us">환율·수수료까지 넣어 정확히 계산하기 →</a></section>')
    main = (CSS + f'<header class="top hub">{cr}<h1>해외주식 양도세 계산과 연말 절세 방법 (2026년 기준)</h1>'
            '<p class="lead">미국주식·해외 ETF를 팔았을 때 세금이 얼마인지, 12월에 무엇을 하면 세금이 줄어드는지 숫자로 정리했어요.</p>'
            '<p class="cu-ans">해외주식 양도세는 <b>1년 동안 판 해외주식의 이익과 손실을 모두 합친 순이익에서 250만 원을 빼고, 남은 금액의 22%</b>(양도소득세 20% + 지방소득세 2%)예요. '
            '연도는 매도한 날이 아니라 <b>결제일</b>로 나뉘고, 2026년에 판 몫은 <b>2027년 5월</b>에 신고·납부해요. 국내 소액주주와 달리 금액이 적어도 과세 대상이에요.</p>'
            '<ul class="dr-toc"><li><a href="#calc">바로 계산</a></li><li><a href="#table">금액별 세금표</a></li><li><a href="#tips">연말 절세 3가지</a></li><li><a href="#ria">RIA 계좌</a></li><li><a href="#report">신고 방법</a></li></ul></header>'
            + calc
            + '<section class="card" id="table"><h2>순이익별 해외주식 양도세 한눈에 보기</h2><div style="overflow-x:auto"><table class="g-tb"><thead><tr><th>1년 순이익</th><th>과세표준 (−250만)</th><th>세금 (22%)</th></tr></thead><tbody>'
            + tb + '</tbody></table></div><p class="cu-src">순이익 = 이익 본 종목 합계 − 손해 본 종목 합계. 매매 수수료는 필요경비로 빼고, 매수·매도 금액은 각각의 결제일 환율로 원화로 바꿔요.</p></section>'
            + '<section class="card" id="tips"><h2>12월에 하는 해외주식 절세 3가지</h2><ol class="g-st">'
              '<li><b>250만 원 공제를 꽉 채우기</b> — 공제는 사람마다 1년에 한 번이고 다음 해로 넘어가지 않아요. 올해 순이익이 250만 원보다 적다면, 이익 난 종목을 일부 팔아 250만 원까지 실현하고 다시 사면 그만큼의 이익에는 앞으로도 세금이 붙지 않아요(취득가가 올라가요).</li>'
              '<li><b>손실 종목으로 이익 상쇄하기</b> — 같은 해에 판 종목끼리는 이익과 손실을 합쳐요(손익통산). 이익이 250만 원을 넘었다면, 손해 중인 종목을 연내에 팔아 순이익을 줄일 수 있어요. 올해 손실은 내년으로 넘어가지 않아요.</li>'
              '<li><b>결제일 마감을 지키기</b> — 연도는 결제일로 갈려요. 12월 마지막 주에 팔면 결제가 다음 해로 넘어가 내년 소득이 될 수 있어요. 증권사가 12월에 공지하는 "올해 귀속 마지막 매도일"을 확인하고 며칠 여유를 두세요. (참고: 2025년 귀속분 미국주식 마지막 거래일은 한 증권사 공지 기준 12월 29일이었어요.)</li></ol>'
              '<p class="g-warn">다시 살 때는 매매 수수료와 환전 비용이 들고, 밤사이 가격이 바뀔 수 있어요. 같은 종목을 팔고 바로 사는 경우 취득가 계산 방식(증권사별 이동평균·선입선출 등)에 따라 결과가 달라질 수 있으니 증권사에 확인하세요.</p></section>'
            + '<section class="card" id="ria"><h2>2026년 한정: 국내시장 복귀계좌(RIA)로 세금 줄이기</h2><ul class="cu-chk">'
              '<li><b>대상</b>: 2025년 12월 23일 이전부터 갖고 있던 해외주식이에요. 그 뒤에 산 주식은 해당되지 않아요.</li>'
              '<li><b>방법</b>: 현금이 아니라 <b>해외주식 자체를 RIA 계좌로 옮긴 뒤 그 안에서 팔아야</b> 해요. 매도 대금은 1년 동안 국내 상장주식·국내주식형 펀드 등에 투자해 유지해요.</li>'
              '<li><b>한도·공제율</b>: 1인당 매도금액 5천만 원까지. 매도 시기에 따라 5월 말까지 100%, 6~7월 80%, <b>8월~12월 31일 50%</b> 공제예요. 지금(11~12월) 팔면 50%가 적용돼요.</li>'
              '<li><b>주의</b>: 2026년에 RIA가 아닌 다른 계좌(일반·ISA·연금 포함)에서 해외주식·해외 ETF를 순매수하면 감면이 그만큼 줄어요. 2026년 12월 31일까지 한시 제도예요.</li></ul>'
              '<p class="cu-src">세부 요건과 공제 계산은 이용하는 증권사 RIA 안내에서 꼭 확인하세요.</p></section>'
            + '<section class="card" id="report"><h2>신고·납부는 이렇게 해요</h2><ol class="g-st">'
              '<li>2026년에 판 해외주식은 <b>2027년 5월</b>(종합소득세 신고 기간)에 양도소득세 확정신고를 해요. 예정신고는 없어요.</li>'
              '<li>국내 증권사 대부분이 <b>양도세 신고대행</b>(무료·유료)을 받아요. 보통 연초~4월에 신청을 받으니 공지를 확인하세요.</li>'
              '<li>직접 하려면 증권사에서 <b>해외주식 양도소득 계산 내역</b>을 내려받아 홈택스 양도소득세 신고 화면에 넣어요. 여러 증권사를 썼다면 모두 합쳐서 신고해요.</li>'
              '<li>신고하지 않거나 늦으면 가산세가 붙을 수 있어요.</li></ol></section>')
    qa = [('해외주식 양도세 세율은 몇 %인가요?', '22%예요. 양도소득세 20%와 지방소득세 2%를 합친 값이에요. 1년 순이익에서 250만 원을 뺀 금액에 곱해요.'),
          ('250만 원 공제는 종목마다 받나요?', '아니요. 사람 기준으로 1년에 한 번이에요. 여러 증권사·여러 종목의 손익을 모두 합친 뒤 한 번만 빼요.'),
          ('올해 손실을 내년으로 넘길 수 있나요?', '안 돼요. 같은 해(결제일 기준)에 판 종목끼리만 손익을 합쳐요. 그래서 연말 전에 손익을 점검하는 게 중요해요.'),
          ('12월 31일에 팔면 올해 소득인가요?', '결제일이 다음 해로 넘어가면 내년 소득이 돼요. 증권사가 공지하는 올해 귀속 마지막 매도일을 확인하고 며칠 여유를 두세요.'),
          ('국내에 상장된 미국 ETF도 같은 세금인가요?', '아니요. 국내 상장 해외 ETF는 매매차익이 배당소득으로 분류돼 15.4%가 원천징수되고, 금융소득 2천만 원 합산 대상이에요. ISA·연금계좌에서 사면 세금이 줄어요. 투자계산기의 미국주식 탭에서 계좌별로 비교할 수 있어요.'),
          ('손해만 봤어도 신고해야 하나요?', '납부할 세금이 없으면 보통 신고 의무는 없지만, 증권사·세무서 안내가 다를 수 있으니 판 기록이 있다면 증권사 신고대행 안내를 확인하세요.')]
    fq, fqld = cu.faq(qa)
    main += fq
    main += ('<section class="card"><h2>출처와 안내</h2><p class="cu-src">출처: 소득세법 제103조(양도소득 기본공제)·제104조(세율), 국세청 홈택스 양도소득세 신고 안내, '
             '재정경제부 국내시장 복귀계좌(RIA) 세제지원 발표(2026년 1월)와 증권사 RIA 안내(2026년 3월) · 확인 2026년 11월 23일.<br>'
             '이 글은 일반적인 계산 방법을 정리한 참고 자료예요. 실제 세액은 개인 상황에 따라 다를 수 있으니 국세청(126)이나 세무사에게 확인하세요.</p></section>'
             '<section class="card"><h2>함께 쓰면 좋은 계산기</h2><ul class="cu-chk">'
             '<li><a href="/life/invest.html#us">미국주식·ETF 팔면 얼마 남을까 (환율·수수료·계좌별 비교)</a></li>'
             '<li><a href="/life/invest.html#sell">국내주식 팔면 얼마 남을까 (거래세·대주주 양도세)</a></li>'
             '<li><a href="/life/invest.html#div">배당금 세후 계산</a></li><li><a href="/life/invest.html#fin">금융소득 2천만 원 종합과세 점검</a></li></ul></section>')
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "해외주식 양도세 계산 방법",
             "step": [{"@type": "HowToStep", "position": 1, "text": "1년(결제일 기준) 동안 판 해외주식의 이익과 손실을 원화로 모두 합쳐 순이익을 구한다."},
                      {"@type": "HowToStep", "position": 2, "text": "순이익에서 기본공제 250만 원을 뺀다."},
                      {"@type": "HowToStep", "position": 3, "text": "남은 금액에 22%(양도소득세 20% + 지방소득세 2%)를 곱한다."}]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "datePublished": "2026-11-23", "dateModified": "2026-11-23",
           "author": {"@type": "Organization", "name": "홍라이프"}, "publisher": {"@type": "Organization", "name": "홍라이프"}, "mainEntityOfPage": SITE + path}
    kr.write(path, title + ' | 홍라이프 도구',
             '해외주식 양도세는 1년 순이익에서 250만 원을 빼고 22%. 금액별 세금표, 바로 계산기, 12월 연말 절세 3가지(공제 채우기·손익통산·결제일), 2026년 RIA 계좌 50% 공제, 2027년 5월 신고 방법까지.',
             main, [crld, fqld, howto, art])
    return path


GUIDES = [('/life/invest/us-stock-tax.html', '해외주식 양도세 계산·연말 절세 (2026)', '1년 순이익 −250만 원 × 22%, 결제일 기준, 연말 절세 3가지, RIA 계좌',
           '해외주식 양도세 미국주식 양도소득세 계산 250만원 공제 22% 연말 절세 해외주식 결제일 RIA 계좌 국내시장 복귀계좌 해외주식 세금 신고')]

if __name__ == '__main__':
    print(us_tax())
