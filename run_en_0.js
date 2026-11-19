const row={"title": "Paycheck Calculator 2026 — $75,000 Salary After Taxes", "description": "https://honglifecalc.com/us/paycheck-calculator.html\n\nWhat's $75,000 a year after taxes? About $2,169.00 every two weeks.\n\nHow to use it: 1) Enter a salary of $75,000, single. 2) Put 6% into your 401(k). Result: That's $56,394 per year, total tax 15.6% of gross.\n\nFree, no sign-up, works on your phone. Estimates only — not tax, legal or financial advice.\nMore calculators: https://honglifecalc.com/\n\n#Shorts #paycheck #takehomepay #taxes #salary #personalfinance", "tags": "paycheck calculator,take home pay calculator,75000 salary after taxes,salary after tax,paycheck calculator 2026,federal income tax,FICA,401k,net pay,free calculator,honglife calculators", "playlist": "HongLife Calculators — How-to Shorts (English)", "date": "2026. 11. 18.", "month": 11, "day": 18, "time": "오후 10:00"};
const W=ms=>new Promise(r=>setTimeout(r,ms));
const setText=(el,txt)=>{el.focus();document.execCommand('selectAll',false,null);document.execCommand('insertText',false,txt);el.dispatchEvent(new Event('input',{bubbles:true}))};
let d; for(let k=0;k<60;k++){d=document.querySelector('ytcp-uploads-dialog'); if(d&&d.querySelector('#title-textarea #textbox'))break; await W(500);}
await W(2500);
let pd; for(let k=0;k<6&&!pd;k++){d.querySelector('ytcp-video-metadata-playlists ytcp-dropdown-trigger').click(); await W(2500);
 pd=[...document.querySelectorAll('ytcp-playlist-dialog, tp-yt-paper-dialog')].find(x=>x.offsetParent&&x.innerText.includes(row.playlist.slice(0,12)));
 if(!pd){const p2=[...document.querySelectorAll('ytcp-playlist-dialog, tp-yt-paper-dialog')].find(x=>x.offsetParent&&x.innerText.includes('완료')); [...(p2?.querySelectorAll('ytcp-button,button')||[])].find(b=>b.innerText.trim()==='완료')?.click(); await W(2500);}}
const cb=[...pd.querySelectorAll('ytcp-checkbox-lit')].find(c=>(c.closest('li,label,ytcp-ve,div')?.innerText||'').includes(row.playlist.slice(0,12))); cb.click(); await W(500);
[...pd.querySelectorAll('ytcp-button,button')].find(b=>b.innerText.trim()==='완료').click(); await W(1200);
setText(d.querySelector('#title-textarea #textbox'),row.title); setText(d.querySelector('#description-textarea #textbox'),row.description);
d.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]').click(); await W(2000);
if(!d.querySelector('#tags-container')?.offsetParent){d.querySelector('#toggle-button').click(); await W(1500);}
const tg=[...d.querySelectorAll('input')].find(i=>/태그/.test(i.getAttribute('aria-label')||'')); tg.focus(); tg.value=row.tags+','; tg.dispatchEvent(new Event('input',{bubbles:true})); tg.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); tg.blur(); await W(800);
const nt=d.querySelectorAll('#tags-container ytcp-chip').length, tt=d.querySelector('#title-textarea #textbox').innerText, pl=d.querySelector('ytcp-video-metadata-playlists').innerText;
const thumbOk=!!d.querySelector('ytcp-thumbnail-uploader img[src^="blob:"], ytcp-thumbnail-uploader img[src^="data:"], #still-picker img.selected, ytcp-thumbnail-uploader .uploaded');
if(tt!==row.title||!pl.includes(row.playlist.slice(0,12))) throw new Error('fields not set: '+tt+' / '+pl);
for(let k=0;k<3;k++){d.querySelector('#next-button').click(); await W(2000);}
d.querySelector('#second-container-expand-button').click(); await W(1500);
if(d.querySelector('#datepicker-trigger').innerText.trim()!==row.date){
  d.querySelector('#datepicker-trigger').click(); await W(1500);
  const inp=[...document.querySelectorAll('ytcp-date-picker input, tp-yt-paper-dialog input')].find(i=>i.offsetParent);
  if(inp){inp.focus(); inp.select(); document.execCommand('insertText',false,row.date); inp.dispatchEvent(new Event('input',{bubbles:true})); inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); await W(1200);}
  if(d.querySelector('#datepicker-trigger').innerText.trim()!==row.date){
    const cal=document.querySelector('ytcp-scrollable-calendar, ytcp-date-picker');
    const months=[...cal.querySelectorAll('.calendar-month, [class*=month]')].filter(m=>m.innerText.includes(row.month+'월'));
    const scope=months.length?months[0]:cal;
    const cell=[...scope.querySelectorAll('[class*=day]')].filter(e=>e.children.length===0&&e.innerText.trim()===String(row.day))[0]; cell.click(); await W(1200);
  }
}
const tin=d.querySelector('#time-of-day-container input'); tin.click(); await W(800);
const it=[...document.querySelectorAll('tp-yt-paper-item')].find(e=>e.innerText.trim()===row.time); it.scrollIntoView({block:'center'}); it.click(); await W(800);
const got=[d.querySelector('#datepicker-trigger').innerText.trim(), tin.value];
if(got[0]!==row.date||got[1]!==row.time) throw new Error('date/time mismatch '+got.join(' ')+' want '+row.date+' '+row.time);
d.querySelector('#done-button').click(); await W(6000);
JSON.stringify({tags:nt,thumb:thumbOk,sched:(document.body.innerText.match(/\d{4}년 \d+월 \d+일 [^\n]{0,20}에 동영상이 공개/)||['?'])[0]})
