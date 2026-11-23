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


def man(n):
    v = round(n) / 10000
    return (f'{v:,.1f}'.rstrip('0').rstrip('.')) + '만 원'


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


def pension():
    path = '/life/invest/pension-tax-credit.html'
    title = '연금저축·IRP 세액공제 한도와 환급액 (2026) — 900만 원·16.5%·12월 31일 납입 마감'
    cr, crld = crumb('연금저축·IRP 세액공제')
    rows = [(3_000_000, '연금저축'), (6_000_000, '연금저축'), (9_000_000, '연금저축 600 + IRP 300')]
    tb = ''.join(f'<tr><td class="n" style="text-align:left">{a // 10000:,}만 원<br><small style="color:#64748B">{E(k)}</small></td><td class="n"><b>{man(a * .165)}</b></td><td class="n">{man(a * .132)}</td></tr>' for a, k in rows)
    calc = ('<section class="card" id="calc"><h2>내 연금저축·IRP 환급액 바로 계산</h2>'
            '<p class="cu-src">올해(1월 1일~12월 31일) 넣은 금액과 앞으로 넣을 금액을 합쳐서 넣으세요. 입력한 숫자는 이 기기에서만 계산돼요.</p>'
            '<div class="g-calc"><label>올해 총급여 (원)<input id="ps" inputmode="numeric" value="50,000,000"></label>'
            '<label>연금저축 납입 (원)<input id="pa" inputmode="numeric" value="4,000,000"></label>'
            '<label>IRP 납입 (원)<input id="pi" inputmode="numeric" value="0"></label>'
            '<label>올해 ISA 만기 자금 연금계좌로 옮긴 금액 (원)<input id="pz" inputmode="numeric" value="0"></label></div>'
            '<div class="g-out" id="po"></div>'
            '<script>(function(){var ids=["ps","pa","pi","pz"],el={};ids.forEach(function(i){el[i]=document.getElementById(i)});var o=document.getElementById("po");'
            'function n(x){return +String(x.value).replace(/[^0-9]/g,"")||0}function f(x){return Math.round(x).toLocaleString("ko-KR")+"원"}'
            'function r(){var sal=n(el.ps),a=n(el.pa),i=n(el.pi),z=n(el.pz),rate=sal<=55000000?.165:.132;'
            'var ps=Math.min(a,6000000),base=Math.min(ps+i,9000000),extra=Math.min(z*.1,3000000),tot=base+extra,ref=tot*rate,room=Math.max(0,9000000-(ps+i));'
            'var xa=Math.max(0,6000000-a),xi=Math.max(0,room-xa);var tip=room<=0?"기본 한도 900만 원을 다 채웠어요.":(xa?"연금저축에 "+f(Math.min(xa,room))+(xi?", IRP에 "+f(xi):""):"IRP에 "+f(xi))+" 더 넣으면 900만 원 한도를 다 채워요.";'
            'o.innerHTML="공제율 "+(rate*100).toFixed(1)+"% (총급여 5,500만 원 "+(rate>.15?"이하":"초과")+") · 공제 대상 "+f(tot)+(extra?" (ISA 전환 추가 "+f(extra)+" 포함)":"")+"<br>예상 환급 <b>"+f(ref)+"</b><br>"+tip+(room>0?" 그러면 환급이 "+f(room*rate)+" 늘어요.":"")+(a>6000000?"<br><small>연금저축에서 600만 원을 넘긴 "+f(a-6000000)+"은 공제 대상이 아니에요. 그만큼은 IRP에 넣어야 해요.</small>":"")}'
            'ids.forEach(function(k){el[k].addEventListener("input",function(){var v=n(el[k]);el[k].value=v?v.toLocaleString("ko-KR"):"";r()})});r()})();</script>'
            '<a class="g-cta" href="/life/invest.html#pen">투자계산기에서 연금 세액공제 자세히 계산하기 →</a></section>')
    main = (CSS + f'<header class="top hub">{cr}<h1>연금저축·IRP 세액공제 한도와 환급액 (2026년 기준)</h1>'
            '<p class="lead">연말정산에서 가장 확실하게 돌려받는 방법인 연금저축·IRP를 한도, 내 연봉별 환급액, 12월 납입 마감까지 숫자로 정리했어요.</p>'
            '<p class="cu-ans">연금저축은 <b>연 600만 원</b>, IRP를 합치면 <b>연 900만 원</b>까지 세액공제를 받아요. 공제율은 <b>총급여 5,500만 원 이하 16.5%, 초과 13.2%</b>(지방소득세 포함)예요. '
            '900만 원을 채우면 <b>최대 148만 5천 원</b>(13.2%면 118만 8천 원)을 돌려받고, 올해 공제를 받으려면 <b>12월 31일 금융사 마감 시간 전까지</b> 입금이 끝나야 해요.</p>'
            '<ul class="dr-toc"><li><a href="#calc">바로 계산</a></li><li><a href="#table">환급액 표</a></li><li><a href="#how">채우는 순서</a></li><li><a href="#deadline">12월 마감</a></li><li><a href="#warn">주의할 점</a></li></ul></header>'
            + calc
            + '<section class="card" id="table"><h2>납입액별 환급액 한눈에 보기</h2><div style="overflow-x:auto"><table class="g-tb"><thead><tr><th>1년 납입액</th><th>총급여 5,500만 이하<br>16.5%</th><th>5,500만 초과<br>13.2%</th></tr></thead><tbody>'
            + tb + '</tbody></table></div><p class="cu-src">종합소득만 있는 사람은 종합소득금액 4,500만 원이 기준이에요. 환급액은 내가 낸 세금(결정세액)보다 클 수 없어서, 낸 세금이 적으면 표보다 적게 돌려받아요.</p></section>'
            + '<section class="card" id="how"><h2>900만 원 채우는 순서</h2><ol class="g-st">'
              '<li><b>연금저축에 600만 원</b> — 연금저축만으로는 600만 원까지만 공제돼요. 그 이상 넣어도 공제는 600만 원에서 멈춰요.</li>'
              '<li><b>IRP에 300만 원</b> — 나머지 300만 원은 IRP(개인형 퇴직연금)에 넣어야 900만 원 한도가 열려요. IRP만으로 900만 원을 채워도 돼요.</li>'
              '<li><b>ISA 만기 자금이 있다면 +300만 원</b> — ISA 만기 후 60일 안에 연금계좌로 옮기면 옮긴 금액의 10%(최대 300만 원)가 그해 공제 한도에 더해져요. 이러면 최대 1,200만 원까지 공제돼요.</li>'
              '<li><b>남은 돈은 그냥 넣어도 돼요</b> — 연금계좌에는 공제와 상관없이 연 1,800만 원까지 넣을 수 있어요. 공제는 없지만 운용 수익에 대한 세금이 연금 받을 때로 미뤄져요.</li></ol></section>'
            + '<section class="card" id="deadline"><h2>12월 31일 밤 이체는 늦을 수 있어요</h2><ul class="cu-chk">'
              '<li>올해 공제를 받으려면 <b>12월 31일 금융사 영업 마감 전에 입금</b>이 끝나야 해요. 마감 시각은 금융사마다 달라요.</li>'
              '<li>예를 들어 지난해 한 증권사는 <b>연금저축 12월 31일 밤 11시, IRP 오후 4시</b>까지였어요. IRP는 영업일·영업시간 기준이라 연금저축보다 일찍 마감돼요.</li>'
              '<li>마지막 날 밤에 IRP 이체를 했다가 다음 해 납입으로 넘어간 사례도 있어요. <b>12월 중순에 가입한 금융사 앱의 "연말 납입 마감 안내"를 확인하고, 며칠 여유를 두고</b> 넣으세요.</li>'
              '<li>증권사 연금저축은 현금으로 입금만 해도 납입으로 인정돼요. 펀드·ETF는 나중에 사도 돼요.</li></ul></section>'
            + '<section class="card" id="warn"><h2>넣기 전에 꼭 알아둘 점</h2><ul class="cu-chk">'
              '<li><b>55세 전에 빼면 16.5%를 다시 내요.</b> 공제받은 원금과 수익을 중도에 찾으면 기타소득세 16.5%가 붙어요. 13.2%로 공제받은 사람은 받은 것보다 더 내게 돼요.</li>'
              '<li><b>IRP는 중도 인출이 거의 안 돼요.</b> 주택 구입·장기 요양 같은 법에서 정한 사유가 아니면 일부만 빼기 어렵고 해지해야 해요. 연금저축은 일부 인출이 가능해요.</li>'
              '<li><b>연금으로 받을 땐 3.3~5.5%</b>를 내요(나이에 따라 다름). 55세 이후, 가입 5년 이상이면 연금으로 받을 수 있어요.</li>'
              '<li>생활비가 빠듯하면 무리해서 채우지 마세요. 여유 자금으로만 넣는 게 안전해요.</li></ul></section>')
    qa = [('연금저축 세액공제 한도는 얼마예요?', '연금저축만 넣으면 연 600만 원, IRP와 합치면 연 900만 원이에요. ISA 만기 자금을 옮기면 최대 300만 원이 더해져요.'),
          ('연봉 6천만 원이면 얼마 돌려받아요?', '총급여가 5,500만 원을 넘으면 13.2%라서 900만 원을 채우면 118만 8천 원이에요. 600만 원만 넣으면 79만 2천 원이에요.'),
          ('연금저축에 900만 원을 다 넣으면요?', '연금저축 단독 한도가 600만 원이라 300만 원은 공제를 못 받아요. 300만 원은 IRP에 넣어야 해요.'),
          ('12월 31일에 넣어도 올해 공제되나요?', '금융사 마감 시간 전에 입금이 끝나면 돼요. 연금저축은 밤까지 받는 곳이 많지만 IRP는 오후에 마감되는 곳이 많아요. 미리 넣는 게 안전해요.'),
          ('세금을 거의 안 냈는데도 148만 원을 받나요?', '아니요. 세액공제는 내가 낸 세금에서 빼 주는 거라, 결정세액보다 많이 돌려받을 수 없어요.'),
          ('연말정산 때 따로 서류를 내야 하나요?', '보통 홈택스 연말정산 간소화 서비스에 납입 내역이 자동으로 올라와요. 안 보이면 금융사에서 연금납입확인서를 받아 회사에 내요.')]
    fq, fqld = cu.faq(qa)
    main += fq
    main += ('<section class="card"><h2>출처와 안내</h2><p class="cu-src">출처: 소득세법 제59조의3(연금계좌세액공제), 국세청 연말정산 안내, 금융감독원 통합연금포털, 증권사 연말 납입 마감 안내(2025년), 2026년 세제개편안 · 확인 2026년 11월 23일.<br>'
             '이 글은 일반적인 계산 방법을 정리한 참고 자료예요. 실제 환급액은 결정세액과 개인 상황에 따라 달라요. 국세청(126)이나 가입 금융사에 확인하세요.</p></section>'
             '<section class="card"><h2>함께 쓰면 좋은 계산기</h2><ul class="cu-chk">'
             '<li><a href="/life/invest.html#pen">연금저축·IRP로 얼마 돌려받을까</a></li><li><a href="/life/invest.html#yet">연말정산 환급, 얼마나 받을까</a></li>'
             '<li><a href="/life/invest.html#fire">은퇴하려면 얼마 있어야 할까</a></li><li><a href="/life/invest/us-stock-tax.html">해외주식 양도세 연말 절세</a></li></ul></section>')
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "연금저축·IRP 세액공제 900만 원 채우는 방법",
             "step": [{"@type": "HowToStep", "position": 1, "text": "연금저축에 연 600만 원까지 넣는다."},
                      {"@type": "HowToStep", "position": 2, "text": "IRP에 300만 원을 더 넣어 합계 900만 원을 채운다."},
                      {"@type": "HowToStep", "position": 3, "text": "12월 31일 금융사 마감 시간 전에 입금을 끝낸다."}]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "datePublished": "2026-11-23", "dateModified": "2026-11-23",
           "author": {"@type": "Organization", "name": "홍라이프"}, "publisher": {"@type": "Organization", "name": "홍라이프"}, "mainEntityOfPage": SITE + path}
    kr.write(path, title + ' | 홍라이프 도구',
             '연금저축 600만 원, IRP 합산 900만 원 세액공제. 총급여 5,500만 원 이하 16.5%(최대 148만 5천 원), 초과 13.2%. 내 환급액 바로 계산, 12월 31일 납입 마감, ISA 전환 300만 원 추가, 중도인출 주의점까지.',
             main, [crld, fqld, howto, art])
    return path


GUIDES = [('/life/invest/us-stock-tax.html', '해외주식 양도세 계산·연말 절세 (2026)', '1년 순이익 −250만 원 × 22%, 결제일 기준, 연말 절세 3가지, RIA 계좌',
           '해외주식 양도세 미국주식 양도소득세 계산 250만원 공제 22% 연말 절세 해외주식 결제일 RIA 계좌 국내시장 복귀계좌 해외주식 세금 신고'),
          ('/life/invest/pension-tax-credit.html', '연금저축·IRP 세액공제 한도와 환급액 (2026)', '900만 원 채우면 최대 148만 5천 원, 12월 31일 납입 마감, 내 환급액 바로 계산',
           '연금저축 세액공제 IRP 세액공제 연금저축 한도 900만원 16.5% 13.2% 연말정산 환급 연금저축 연말 납입 마감 ISA 만기 연금 전환 300만원')]

if __name__ == '__main__':
    print(us_tax())
    print(pension())
