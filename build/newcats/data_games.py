# 게임 계산기. 각 항목: slug, name, h1, lead, kw, body(도구 HTML), js, xp(설명 섹션 [(제목, 문단)]), faq, src(출처)
GAMES = [
dict(slug='maple-auction-fee', name='메이플 경매장 수수료 계산기', h1='메이플 경매장 수수료 계산기', kw='메이플 경매장 수수료 계산기 메이플옥션 수수료 5% 3% MVP 실수령',
 lead='판매가를 넣으면 경매장 수수료 5%·3%를 뗀 실수령 메소를 바로 보여 주고, 원하는 실수령액을 맞추려면 얼마에 올려야 하는지도 거꾸로 계산해요.',
 body='''<div class="grid g3"><div class="f"><label for="p">판매가 (개당 메소)</label><input id="p" inputmode="numeric" value="100000000"></div><div class="f"><label for="n">수량</label><input id="n" inputmode="numeric" value="1"></div><div class="f"><label for="r">수수료</label><select id="r"><option value="5">기본 5%</option><option value="3">MVP 스페셜 이상·프리미엄 PC방 3%</option></select></div></div>
<div class="gm-out"><div><span>판매 총액</span><b id="o1">-</b></div><div><span>수수료</span><b id="o2">-</b></div><div class="hi"><span>실수령 메소</span><b id="o3">-</b></div></div>
<h3 class="gm-h">거꾸로 계산: 이만큼 받고 싶다면</h3><div class="grid g3"><div class="f"><label for="t">원하는 실수령 (총액)</label><input id="t" inputmode="numeric" value="100000000"></div></div>
<div class="gm-out"><div class="hi"><span>올려야 할 개당 가격</span><b id="o4">-</b></div><div><span>5%와 3% 차이 (이번 판매)</span><b id="o5">-</b></div></div>''',
 js='''function c(){var p=N('p'),n=Math.max(1,N('n')),r=+$('r').value/100,g=p*n,f=Math.floor(g*r);S('o1',M(g));S('o2',M(f));S('o3',M(g-f));var t=N('t');S('o4',M(Math.ceil(t/(1-r)/n)));S('o5',M(Math.floor(g*0.05)-Math.floor(g*0.03)));}''',
 xp=[('계산 방식','경매장에서 물건이 팔리면 판매 대금에서 수수료를 뗀 금액이 들어와요. 이 계산기는 판매 총액(개당 가격 × 수량)에 수수료율을 곱한 값을 수수료로 보고, 1메소 미만은 버림으로 계산해요. 실제 게임 안에서는 표시 방식에 따라 몇 메소 차이가 날 수 있어요.'),
     ('5%와 3%는 언제 적용되나요','넥슨 공식 가이드에 따르면 판매 대금 수령 시 기본 수수료는 5%이고, MVP 스페셜 등급이거나 프리미엄 PC방에서 수령하면 3%가 적용돼요. 두 혜택이 겹치면 MVP 혜택만 적용돼요.'),
     ('거꾸로 계산 활용법','“딱 1억 메소를 손에 쥐고 싶다”처럼 목표 금액이 있으면 거꾸로 계산 칸에 넣어 보세요. 수수료를 감안해 올려야 할 개당 가격을 올림으로 보여 줘요.')],
 faq=[('수수료는 언제 빠지나요?','물건이 팔리고 판매 대금을 수령할 때 빠져요. 등록할 때 따로 내는 비용이 아니에요.'),('다른 월드 아이템을 살 때도 수수료가 있나요?','네. 공식 가이드에 따르면 다른 월드 아이템을 살 때는 가격의 10% 가치에 해당하는 메이플포인트가 추가 수수료로 들어가요. 이 계산기는 판매 수수료만 다뤄요.')],
 src=('메이플스토리 공식 가이드 — 경매장','https://maplestory.nexon.com/guide/n23gameinformation/articles/394','2026년 11월 18일')),

dict(slug='lostark-auction', name='로스트아크 경매 입찰 적정가 계산기', h1='로스트아크 경매 입찰 적정가 계산기', kw='로스트아크 경매 계산기 로아 입찰 적정가 손익분기 분배금',
 lead='레이드 경매에 나온 아이템의 거래소 시세와 파티 인원을 넣으면, 입찰해도 손해 보지 않는 손익분기 금액과 모두가 이득인 추천 입찰가를 계산해요.',
 body='''<div class="grid g3"><div class="f"><label for="p">거래소 시세 (골드)</label><input id="p" inputmode="numeric" value="10000"></div><div class="f"><label for="n">파티 인원</label><select id="n"><option>4</option><option selected>8</option><option>16</option></select></div><div class="f"><label for="r">거래소 수수료 (%)</label><input id="r" inputmode="decimal" value="5"></div></div>
<div class="gm-out"><div><span>판매 시 실수령</span><b id="o1">-</b></div><div><span>손익분기 입찰가</span><b id="o2">-</b></div><div class="hi"><span>추천 입찰가 (선점)</span><b id="o3">-</b></div></div>
<p class="note" id="o4"></p>''',
 js='''function c(){var p=N('p'),n=+$('n').value,r=N('r')/100,net=p*(1-r),be=Math.floor(net*(n-1)/n),rec=Math.floor(be/1.1);S('o1',G(Math.floor(net)));S('o2',G(be));S('o3',G(rec));$('o4').textContent='추천 입찰가로 낙찰받으면 내가 판매해서 얻는 이익과 다른 파티원이 받는 분배금이 비슷해져요. 손익분기보다 비싸게 사면 경매 대신 분배금만 받는 쪽이 이득이에요. 분배금: 입찰가 × 1/'+(n-1)+' 정도씩 나눠 받아요.';}''',
 xp=[('손익분기 입찰가','경매에서 아이템을 낙찰받으면 낸 골드가 나머지 파티원에게 나눠져요. 반대로 입찰하지 않으면 나도 분배금을 받죠. 그래서 “판매 실수령 × (인원−1) ÷ 인원”보다 싸게 사야 이득이에요. 이 값이 손익분기 입찰가예요.'),
     ('추천 입찰가(선점가)','손익분기 가격을 1.1로 나눈 값이에요. 이 가격에 낙찰받으면 내가 아이템을 팔아 얻는 이익과 다른 파티원이 받는 분배금이 거의 같아져서, 서로 공평한 금액으로 널리 쓰여요.'),
     ('수수료 칸','거래소 판매 수수료는 기본 5%로 넣어 뒀어요. 게임 안 판매 창에 표시되는 수수료가 다르면 직접 바꿔 넣으세요.')],
 faq=[('귀속 아이템도 계산되나요?','거래소에 팔 수 없는 귀속 아이템은 시세가 없어서 이 계산이 맞지 않아요. 내가 직접 쓸 가치를 기준으로 판단하세요.'),('16인 레이드는 왜 이득이 적나요?','인원이 많을수록 분배금이 잘게 나뉘어서, 손익분기가 판매가에 더 가까워져요.')],
 src=None),

dict(slug='market-fee', name='게임 거래소 수수료 계산기', h1='게임 거래소 수수료 계산기', kw='게임 거래소 수수료 계산기 실수령 계산 판매 수수료 역산',
 lead='어느 게임이든 판매가와 수수료율만 넣으면 실수령액을 계산하고, 목표 실수령에 맞는 판매가를 거꾸로 알려 줘요. 할인 쿠폰처럼 수수료를 깎는 비율도 넣을 수 있어요.',
 body='''<div class="grid g3"><div class="f"><label for="p">판매가</label><input id="p" inputmode="numeric" value="1000000"></div><div class="f"><label for="r">기본 수수료율 (%)</label><input id="r" inputmode="decimal" value="10"></div><div class="f"><label for="d">수수료 할인 (%)</label><input id="d" inputmode="decimal" value="0"></div></div>
<div class="gm-out"><div><span>실제 수수료율</span><b id="o1">-</b></div><div><span>수수료</span><b id="o2">-</b></div><div class="hi"><span>실수령</span><b id="o3">-</b></div></div>
<div class="grid g3" style="margin-top:12px"><div class="f"><label for="t">원하는 실수령</label><input id="t" inputmode="numeric" value="1000000"></div></div><div class="gm-out"><div class="hi"><span>올려야 할 판매가</span><b id="o4">-</b></div></div>''',
 js='''function c(){var p=N('p'),r=N('r')/100*(1-N('d')/100),f=Math.floor(p*r);S('o1',(r*100).toFixed(2).replace(/\\.?0+$/,'')+'%');S('o2',K(f));S('o3',K(p-f));S('o4',K(Math.ceil(N('t')/(1-r))));}''',
 xp=[('계산 방식','실제 수수료율 = 기본 수수료율 × (1 − 할인율)로 계산해요. 예를 들어 기본 40%에 30% 할인 쿠폰을 쓰면 실제 수수료율은 28%예요. 할인이 “기본율에서 몇 %p를 빼 주는” 방식인 게임이라면, 기본 수수료율 칸에 뺀 값을 바로 넣으세요.'),
     ('어떤 게임에 쓰나요','메이플스토리, 로스트아크, FC 온라인처럼 거래소에서 판매 수수료를 떼는 게임이라면 모두 쓸 수 있어요. 게임마다 수수료율과 할인 방식이 업데이트로 바뀌니, 게임 안 판매 창에 표시되는 수수료율을 넣는 게 가장 정확해요.')],
 faq=[('FC 온라인 수수료도 되나요?','네. 판매 창에 표시되는 수수료율과 PC방·쿠폰 할인율을 넣으면 실수령 BP를 계산할 수 있어요. 수수료 정책은 업데이트로 바뀔 수 있어요.'),('소수점은 어떻게 처리하나요?','수수료는 버림, 거꾸로 계산한 판매가는 올림으로 계산해요.')],
 src=None),

dict(slug='gacha', name='가챠 확률 계산기 (천장 포함)', h1='가챠 확률 계산기', kw='가챠 확률 계산기 뽑기 확률 천장 계산 기댓값 몇 번 뽑아야',
 lead='뽑기 1회 확률과 횟수를 넣으면 적어도 한 번 뽑힐 확률, 천장까지 고려한 평균 뽑기 횟수와 비용을 계산해요. 원하는 확률을 맞추려면 몇 번 뽑아야 하는지도 알려 줘요.',
 body='''<div class="grid g3"><div class="f"><label for="p">1회 확률 (%)</label><input id="p" inputmode="decimal" value="0.6"></div><div class="f"><label for="n">뽑기 횟수</label><input id="n" inputmode="numeric" value="90"></div><div class="f"><label for="c">천장 (없으면 0)</label><input id="c" inputmode="numeric" value="90"></div><div class="f"><label for="w">1회 가격 (원)</label><input id="w" inputmode="numeric" value="2000"></div><div class="f"><label for="g">목표 확률 (%)</label><input id="g" inputmode="decimal" value="90"></div></div>
<div class="gm-out"><div class="hi"><span>적어도 1번 뽑힐 확률</span><b id="o1">-</b></div><div><span>평균 뽑기 횟수</span><b id="o2">-</b></div><div><span>평균 비용</span><b id="o3">-</b></div><div><span>목표 확률까지 필요한 횟수</span><b id="o4">-</b></div></div>
<div class="gm-bar" id="bar"></div>''',
 js='''function c(){var p=N('p')/100,n=N('n'),cl=N('c'),w=N('w'),g=N('g')/100;if(p<=0)return;var pr=(cl>0&&n>=cl)?1:1-Math.pow(1-p,n);S('o1',(pr*100).toFixed(2)+'%');var e=cl>0?(1-Math.pow(1-p,cl))/p:1/p;S('o2',e.toFixed(1)+'회');S('o3',K(Math.round(e*w))+'원');var k=Math.ceil(Math.log(1-Math.min(g,0.999999))/Math.log(1-p));if(cl>0&&k>cl)k=cl;S('o4',k+'회 ('+K(k*w)+'원)');var h='';[10,30,50,70,90].forEach(function(t){var m=Math.ceil(Math.log(1-t/100)/Math.log(1-p));if(cl>0&&m>cl)m=cl;h+='<div><span>'+t+'%</span><i style="width:'+Math.min(100,m/(cl||Math.ceil(Math.log(.01)/Math.log(1-p)))*100)+'%"></i><b>'+m+'회</b></div>'});$('bar').innerHTML='<p class="gm-cap">확률별 필요 횟수</p>'+h;}''',
 xp=[('적어도 한 번 뽑힐 확률','매번 확률이 같은 뽑기를 n번 하면, 한 번도 안 뽑힐 확률은 (1 − p)ⁿ이에요. 그래서 적어도 한 번 뽑힐 확률은 1 − (1 − p)ⁿ이에요. 1% 뽑기를 100번 해도 확률은 약 63%라는 게 이 공식에서 나와요.'),
     ('천장이 있을 때 평균 횟수','천장(c회째에는 확정)이 있으면 평균 뽑기 횟수는 (1 − (1 − p)ᶜ) ÷ p로 계산해요. 천장이 없으면 1 ÷ p예요. 횟수가 천장 이상이면 확률은 100%로 표시해요.'),
     ('주의할 점','게임마다 천장 뒤 픽업 확률(50:50), 확률 상승 구간(소프트 천장) 같은 규칙이 달라요. 이 계산기는 매번 같은 확률과 하드 천장만 반영해요. 정확한 확률은 게임사가 공개한 확률표를 확인하세요.')],
 faq=[('확률 1%면 100번 하면 무조건 나오나요?','아니요. 100번 해도 약 63%예요. 99% 확률을 넘기려면 약 459번이 필요해요.'),('천장 횟수가 0이면?','천장이 없는 뽑기로 보고 계산해요.')],
 src=None),

dict(slug='enhance', name='강화 기댓값 계산기', h1='강화 기댓값 계산기', kw='강화 기댓값 계산기 강화 확률 계산 파괴 확률 평균 비용',
 lead='강화 성공 확률, 1회 비용, 파괴 확률과 파괴 시 복구 비용을 넣으면 성공까지 평균 몇 번, 평균 얼마가 드는지 계산하고 예산 안에 성공할 확률도 보여 줘요.',
 body='''<div class="grid g3"><div class="f"><label for="p">성공 확률 (%)</label><input id="p" inputmode="decimal" value="30"></div><div class="f"><label for="d">파괴 확률 (%)</label><input id="d" inputmode="decimal" value="2"></div><div class="f"><label for="w">1회 강화 비용</label><input id="w" inputmode="numeric" value="10000000"></div><div class="f"><label for="R">파괴 시 복구 비용</label><input id="R" inputmode="numeric" value="500000000"></div><div class="f"><label for="b">내 예산</label><input id="b" inputmode="numeric" value="300000000"></div></div>
<div class="gm-out"><div><span>평균 시도 횟수</span><b id="o1">-</b></div><div><span>평균 파괴 횟수</span><b id="o2">-</b></div><div class="hi"><span>성공까지 평균 비용</span><b id="o3">-</b></div><div><span>예산 안에 성공할 확률 (모의 1만 회)</span><b id="o4">-</b></div></div>''',
 js='''function c(){var p=N('p')/100,d=N('d')/100,w=N('w'),R=N('R'),b=N('b');if(p<=0||p+d>1)return;S('o1',(1/p).toFixed(1)+'회');S('o2',(d/p).toFixed(2)+'회');S('o3',K(Math.round((w+d*R)/p)));var ok=0;for(var i=0;i<10000;i++){var m=0;while(m<=b){m+=w;var x=Math.random();if(x<p){ok++;break}if(x<p+d)m+=R;if(m>b*50)break}}S('o4',(ok/100).toFixed(1)+'%');}''',
 xp=[('계산 방식','한 번 시도할 때 성공 확률이 p, 파괴 확률이 d라면, 성공까지 평균 시도 횟수는 1 ÷ p예요. 그동안 평균 d ÷ p번 파괴되고, 파괴될 때마다 복구 비용이 들어요. 그래서 평균 비용은 (1회 비용 + d × 복구 비용) ÷ p예요. 실패해도 단계가 그대로인 강화를 기준으로 했어요.'),
     ('예산 안에 성공할 확률','평균은 어디까지나 평균이에요. 운이 나쁘면 몇 배가 들기도 해요. 그래서 실제로 1만 번 강화를 모의로 돌려서, 내 예산 안에 성공한 비율을 따로 보여 줘요. 누를 때마다 숫자가 조금씩 다를 수 있어요.'),
     ('주의할 점','스타포스처럼 실패 시 단계가 떨어지거나, 일정 횟수 실패하면 확정 성공하는 규칙이 있는 강화는 결과가 달라요. 단계별 확률은 게임사 공식 확률표를 확인해 넣으세요.')],
 faq=[('성공 30%면 평균 3~4번이면 되나요?','평균은 약 3.3번이지만, 10번 넘게 실패할 확률도 약 2.8%나 돼요. 예산 확률을 함께 보세요.'),('파괴가 없는 강화는?','파괴 확률에 0을 넣으면 돼요.')],
 src=None),

dict(slug='edpi', name='FPS 감도 변환·eDPI 계산기', h1='FPS 감도 변환·eDPI 계산기', kw='eDPI 계산기 감도 변환 발로란트 오버워치 배그 cs2 감도 cm/360',
 lead='마우스 DPI와 게임 감도로 eDPI와 한 바퀴 도는 데 필요한 마우스 거리(cm/360)를 계산하고, 같은 손맛을 다른 게임으로 옮길 때 넣어야 할 감도를 알려 줘요.',
 body='''<div class="grid g3"><div class="f"><label for="g1">지금 게임</label><select id="g1"></select></div><div class="f"><label for="dpi">마우스 DPI</label><input id="dpi" inputmode="numeric" value="800"></div><div class="f"><label for="s">게임 감도</label><input id="s" inputmode="decimal" value="0.4"></div></div>
<div class="gm-out"><div><span>eDPI</span><b id="o1">-</b></div><div class="hi"><span>한 바퀴 (cm/360°)</span><b id="o2">-</b></div></div>
<h3 class="gm-h">다른 게임으로 옮기기</h3><div class="grid g3"><div class="f"><label for="g2">옮길 게임</label><select id="g2"></select></div><div class="f"><label for="dpi2">새 DPI</label><input id="dpi2" inputmode="numeric" value="800"></div></div>
<div class="gm-out"><div class="hi"><span>넣어야 할 감도</span><b id="o3">-</b></div></div>''',
 js='''var Y={"발로란트":0.07,"카운터 스트라이크 2":0.022,"에이펙스 레전드":0.022,"오버워치 2":0.0066};function c(){var a=Y[$('g1').value],dpi=N('dpi'),s=N('s');S('o1',(dpi*s).toFixed(1).replace(/\\.0$/,''));var cm=360/(dpi*s*a)*2.54;S('o2',cm.toFixed(1)+' cm');var b=Y[$('g2').value],d2=N('dpi2');S('o3',(dpi*s*a/(d2*b)).toFixed(3));}
['g1','g2'].forEach(function(i,k){var h='';for(var n in Y)h+='<option'+(k&&n=='카운터 스트라이크 2'?' selected':'')+'>'+n+'</option>';$(i).innerHTML=h;});''',
 xp=[('eDPI란','eDPI는 마우스 DPI × 게임 감도예요. 같은 게임 안에서 사람마다 다른 DPI·감도 조합을 한 숫자로 비교할 수 있어요. 다만 게임마다 감도 단위가 달라서, 서로 다른 게임끼리는 eDPI로 비교하면 안 돼요.'),
     ('cm/360으로 비교해요','게임이 달라도 손맛을 똑같이 맞추려면 “마우스를 몇 cm 움직여야 한 바퀴 도는지”를 맞추면 돼요. 이 값은 360 ÷ (DPI × 감도 × 게임 계수) × 2.54로 계산해요. 게임 계수는 발로란트 0.07, CS2·에이펙스 0.022, 오버워치 2 0.0066처럼 게임마다 정해진 1감도당 회전 각도예요.'),
     ('주의할 점','윈도우 포인터 속도, 마우스 가속, 게임 안의 FOV·배율 감도 설정이 다르면 실제 손맛이 달라질 수 있어요. 원시 입력(raw input)을 켜고 쓰는 걸 기준으로 해요.')],
 faq=[('DPI를 바꾸면 감도도 바꿔야 하나요?','네. DPI를 두 배로 올리면 감도를 절반으로 낮춰야 같은 손맛이 나요. 아래 “새 DPI” 칸에 바꿀 DPI를 넣으면 맞는 감도를 알려 줘요.'),('배틀그라운드는 왜 없나요?','배틀그라운드는 감도 계산식이 배율·FOV마다 달라 단순 계수로 옮기기 어려워서 이번에는 빼 뒀어요.')],
 src=None),

dict(slug='bowling', name='볼링 점수 계산기', h1='볼링 점수 계산기', kw='볼링 점수 계산기 볼링 점수 계산법 스트라이크 스페어',
 lead='투구마다 쓰러뜨린 핀 수를 넣으면 프레임별 점수와 누적 점수를 스트라이크·스페어 보너스까지 넣어 계산해요. 점수 계산법이 헷갈릴 때 연습용으로도 좋아요.',
 body='''<p class="note">한 칸에 핀 수를 넣으세요. 스트라이크는 X, 스페어는 / 로 넣어도 돼요. 10프레임은 최대 3번 던져요.</p><div class="bw" id="bw"></div><div class="btns"><button class="btn ghost" type="button" id="rst">처음부터</button><button class="btn ghost" type="button" id="ex">예시 넣기</button></div>
<div class="gm-out"><div class="hi"><span>총점</span><b id="o1">0</b></div><div><span>스트라이크</span><b id="o2">0</b></div><div><span>스페어</span><b id="o3">0</b></div></div>''',
 js='''var B=$('bw');(function(){var h='';for(var f=1;f<=10;f++){h+='<div class="bf"><em>'+f+'</em><div>';for(var k=0;k<(f==10?3:2);k++)h+='<input maxlength="2" data-f="'+f+'" data-k="'+k+'" aria-label="'+f+'프레임 '+(k+1)+'투">';h+='</div><b id="s'+f+'">&nbsp;</b></div>'}B.innerHTML=h;})();
function rd(i,prev){var v=(i.value||'').trim().toUpperCase();if(v=='')return null;if(v=='X')return 10;if(v=='/')return prev==null?null:10-prev;var n=parseInt(v,10);return isNaN(n)?null:Math.max(0,Math.min(10,n));}
function c(){var R=[],st=0,sp=0;for(var f=1;f<=10;f++){var ins=B.querySelectorAll('input[data-f="'+f+'"]'),a=rd(ins[0]);if(a==null)break;R.push(a);if(f<10){if(a==10){st++;continue}var b=rd(ins[1],a);if(b==null)break;if(a+b>10)b=10-a;R.push(b);if(a+b==10)sp++;}else{if(a==10)st++;var b=rd(ins[1],a==10?null:a);if(b==null)break;R.push(b);if(a<10&&a+b==10)sp++;if(a==10&&b==10)st++;if(a==10||a+b==10){var c3=rd(ins[2],(a==10&&b<10)?b:null);if(c3!=null){R.push(c3);if(c3==10&&(b==10||a+b==10))st++;}}}}
var i=0,t=0;for(var f=1;f<=10;f++){var el=$('s'+f);if(i>=R.length){el.innerHTML='&nbsp;';continue}var sc=null;if(R[i]==10){if(R[i+2]!=null)sc=10+R[i+1]+R[i+2];i+=1}else if(R[i+1]!=null&&R[i]+R[i+1]==10){if(R[i+2]!=null)sc=10+R[i+2];i+=2}else if(R[i+1]!=null){sc=R[i]+R[i+1];i+=2}else{i+=1}if(f==10&&sc==null&&R[i]!=null){}if(sc==null){el.innerHTML='&nbsp;';for(var g=f+1;g<=10;g++)$('s'+g).innerHTML='&nbsp;';break}t+=sc;el.textContent=t;}
S('o1',t);S('o2',st);S('o3',sp);}
$('rst').onclick=function(){B.querySelectorAll('input').forEach(function(i){i.value=''});c()};
$('ex').onclick=function(){var v=['X','','7','/','9','0','X','','0','8','8','/','0','6','X','','X','','X','8','1'];B.querySelectorAll('input').forEach(function(i,k){i.value=v[k]||''});c()};
B.addEventListener('input',c);''',
 xp=[('볼링 점수 계산법','한 게임은 10프레임이고, 프레임마다 두 번 던져요. 스트라이크(첫 투구에 10핀)는 10점에 다음 두 투구 점수를 더하고, 스페어(두 번에 10핀)는 10점에 다음 한 투구 점수를 더해요. 나머지는 쓰러뜨린 핀 수를 그대로 더해요.'),
     ('10프레임 규칙','10프레임에서 스트라이크나 스페어를 치면 보너스 투구를 한 번 더(스트라이크면 최대 두 번 더) 던져서 그 점수까지 더해요. 그래서 10프레임은 최대 3번 던질 수 있어요.'),
     ('300점 퍼펙트 게임','12번 연속 스트라이크를 치면 프레임마다 30점씩, 총 300점이 돼요. 볼링에서 낼 수 있는 가장 높은 점수예요.')],
 faq=[('보너스 점수가 아직 안 나와요','스트라이크나 스페어 뒤의 투구를 넣어야 그 프레임 점수가 정해져서, 그 전까지는 빈칸으로 둬요.'),('X와 /는 어떻게 쓰나요?','스트라이크 칸에 X, 스페어인 두 번째 칸에 /를 넣으면 자동으로 핀 수를 계산해요.')],
 src=None),

dict(slug='winrate', name='승률·KDA 계산기 (목표 승률까지 몇 연승?)', h1='승률·KDA 계산기', kw='승률 계산기 롤 승률 목표 승률 몇 연승 KDA 계산기',
 lead='지금 전적과 목표 승률을 넣으면 몇 연승을 해야 목표에 닿는지 계산하고, 킬·데스·어시스트로 KDA도 바로 계산해요. 롤·발로란트·오버워치 어디든 쓸 수 있어요.',
 body='''<div class="grid g3"><div class="f"><label for="w">승</label><input id="w" inputmode="numeric" value="48"></div><div class="f"><label for="l">패</label><input id="l" inputmode="numeric" value="52"></div><div class="f"><label for="t">목표 승률 (%)</label><input id="t" inputmode="decimal" value="55"></div></div>
<div class="gm-out"><div><span>지금 승률</span><b id="o1">-</b></div><div class="hi"><span>목표까지 필요한 연승</span><b id="o2">-</b></div><div><span>지금 승률로 계속하면</span><b id="o3">-</b></div></div>
<h3 class="gm-h">KDA</h3><div class="grid g3"><div class="f"><label for="k">킬</label><input id="k" inputmode="numeric" value="7"></div><div class="f"><label for="d">데스</label><input id="d" inputmode="numeric" value="4"></div><div class="f"><label for="a">어시스트</label><input id="a" inputmode="numeric" value="9"></div></div>
<div class="gm-out"><div class="hi"><span>KDA</span><b id="o4">-</b></div></div>''',
 js='''function c(){var w=N('w'),l=N('l'),g=w+l,t=N('t')/100;S('o1',g?(w/g*100).toFixed(1)+'%':'-');if(t>=1){S('o2','100%는 불가능')}else{var x=Math.max(0,Math.ceil((t*g-w)/(1-t)));S('o2',x+'연승');}S('o3',g&&w/g>=t?'이미 목표 달성':'승률을 올려야 해요');var k=N('k'),d=N('d'),a=N('a');S('o4',d?((k+a)/d).toFixed(2):'Perfect');}''',
 xp=[('목표 승률까지 연승 계산','지금 승 W, 전체 G판에서 x연승을 하면 승률은 (W + x) ÷ (G + x)가 돼요. 이 값이 목표 승률 t 이상이 되는 가장 작은 x는 (t × G − W) ÷ (1 − t)를 올림한 값이에요. 판수가 많을수록 승률을 올리기 어려운 이유가 이 식에 있어요.'),
     ('KDA 계산','KDA는 (킬 + 어시스트) ÷ 데스로 계산해요. 데스가 0이면 “Perfect”로 표시해요. 게임이나 전적 사이트에 따라 계산식이 조금 다를 수 있어요.')],
 faq=[('승률 50%에서 60%로 가려면?','100판 기준 50승 50패라면 25연승이 필요해요. 판수가 적을 때 올리는 게 훨씬 쉬워요.'),('어떤 게임에 쓸 수 있나요?','승·패만 있으면 롤, 발로란트, 오버워치, 배틀그라운드 등 어떤 게임에도 쓸 수 있어요.')],
 src=None),
]
