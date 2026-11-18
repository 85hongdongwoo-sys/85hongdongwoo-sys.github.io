import sys
from playwright.sync_api import sync_playwright
pages=sys.argv[1:]
JS="""()=>{const out=[];const vw=document.documentElement.clientWidth;const main=document.querySelector('main')||document.body;const mr=main.getBoundingClientRect();
for(const el of document.querySelectorAll('main *')){const st=getComputedStyle(el);if(st.display=='none'||st.visibility=='hidden')continue;const r=el.getBoundingClientRect();if(r.width==0||r.height==0)continue;
if(el.closest('.qs-sns,.tp-grid,ul.hl-cards,.chips,.pe-flt,.subtabs,.groups,.tabs'))continue;
if(r.left<mr.left-1||r.right>mr.right+1||r.right>vw+1){out.push(['out',el.tagName+'.'+el.className,Math.round(r.left),Math.round(r.right),(el.textContent||'').trim().slice(0,30)])}
else if(el.scrollWidth>el.clientWidth+2&&['visible','auto','scroll'].indexOf(st.overflowX)<0&&el.children.length==0){out.push(['clip',el.tagName+'.'+el.className,el.scrollWidth,el.clientWidth,(el.textContent||'').trim().slice(0,30)])}}
const docw=document.documentElement.scrollWidth;return {docw,vw,n:out.length,items:out.slice(0,8)}}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (390,1280):
        pg=b.new_page(viewport={'width':w,'height':900})
        for u in pages:
            pg.goto('http://localhost:8791'+u); pg.wait_for_timeout(900)
            r=pg.evaluate(JS)
            if r['n'] or r['docw']>r['vw']: print(w,u,'docw',r['docw'],'vw',r['vw'],r['n']); [print('   ',i) for i in r['items']]
        pg.close()
    b.close()
print('done')
