const R='https://raw.githubusercontent.com/85hongdongwoo-sys/85hongdongwoo-sys.github.io/__SHA__/__LANG__/';
const IDX=__IDX__;
const csv=t=>{const rows=[];let row=[],f='',q=false;for(let i=0;i<t.length;i++){const c=t[i];if(q){if(c=='"'){if(t[i+1]=='"'){f+='"';i++}else q=false}else f+=c}else{if(c=='"')q=true;else if(c==','){row.push(f);f=''}else if(c=='\n'){row.push(f);rows.push(row);row=[];f=''}else if(c!='\r')f+=c}}if(f||row.length){row.push(f);rows.push(row)}const h=rows.shift();return rows.filter(r=>r.length>1).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]])))};
const W=ms=>new Promise(r=>setTimeout(r,ms));
const setText=(el,txt)=>{el.focus();document.execCommand('selectAll',false,null);document.execCommand('insertText',false,txt);el.dispatchEvent(new Event('input',{bubbles:true}))};
await W(2500);
const rows=csv(await (await fetch(R+'schedule.csv')).text()); const row=rows[IDX];
const vb=await (await fetch(R+row.file)).blob();
const fp=document.querySelector('ytcp-uploads-file-picker input[type=file]'); let dt=new DataTransfer(); dt.items.add(new File([vb],row.file,{type:'video/mp4'})); fp.files=dt.files; fp.dispatchEvent(new Event('change',{bubbles:true}));
let d; for(let k=0;k<40;k++){await W(500); d=document.querySelector('ytcp-uploads-dialog'); if(d&&d.querySelector('#title-textarea #textbox'))break;}
await W(4000);
let pd; for(let k=0;k<6&&!pd;k++){d.querySelector('ytcp-video-metadata-playlists ytcp-dropdown-trigger').click(); await W(2500);
 pd=[...document.querySelectorAll('ytcp-playlist-dialog, tp-yt-paper-dialog')].find(x=>x.offsetParent&&x.innerText.includes(row.playlist.slice(0,12)));
 if(!pd){const p2=[...document.querySelectorAll('ytcp-playlist-dialog, tp-yt-paper-dialog')].find(x=>x.offsetParent&&x.innerText.includes('완료')); [...(p2?.querySelectorAll('ytcp-button,button')||[])].find(b=>b.innerText.trim()==='완료')?.click(); await W(2500);}}
const cb=[...pd.querySelectorAll('ytcp-checkbox-lit')].find(c=>(c.closest('li,label,ytcp-ve,div')?.innerText||'').includes(row.playlist.slice(0,12))); cb.click(); await W(500);
[...pd.querySelectorAll('ytcp-button,button')].find(b=>b.innerText.trim()==='완료').click(); await W(1200);
setText(d.querySelector('#title-textarea #textbox'),row.title); setText(d.querySelector('#description-textarea #textbox'),row.description);
const tb=await (await fetch(R+row.thumb_v)).blob(); const ti=d.querySelector('ytcp-thumbnail-uploader input[type=file]'); dt=new DataTransfer(); dt.items.add(new File([tb],row.thumb_v,{type:'image/png'})); ti.files=dt.files; ti.dispatchEvent(new Event('change',{bubbles:true}));
d.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]').click(); await W(2500);
if(!d.querySelector('#tags-container')?.offsetParent){d.querySelector('#toggle-button').click(); await W(1500);}
const tg=[...d.querySelectorAll('input')].find(i=>/태그/.test(i.getAttribute('aria-label')||'')); tg.focus(); tg.value=row.tags+','; tg.dispatchEvent(new Event('input',{bubbles:true})); tg.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); tg.blur(); await W(800);
const nt=d.querySelectorAll('#tags-container ytcp-chip').length, tt=d.querySelector('#title-textarea #textbox').innerText, pl=d.querySelector('ytcp-video-metadata-playlists').innerText;
if(tt!==row.title||!pl.includes(row.playlist.slice(0,12))) throw new Error('fields not set: '+tt+' / '+pl);
for(let k=0;k<3;k++){d.querySelector('#next-button').click(); await W(2000);}
d.querySelector('#second-container-expand-button').click(); await W(1500);
const hh=+row.time_kst.split(':')[0], mm=row.time_kst.split(':')[1];
const day=__BASE__+(+row.day)+(hh<__CUT__?1:0); const dateTxt=`2026. 11. ${day}.`;
const ampm=hh<12?'오전':'오후'; const h12=hh%12===0?12:hh%12; const timeTxt=`${ampm} ${h12}:${mm}`;
if(d.querySelector('#datepicker-trigger').innerText.trim()!==dateTxt){
  d.querySelector('#datepicker-trigger').click(); await W(1500);
  const cal=document.querySelector('ytcp-scrollable-calendar, ytcp-date-picker');
  const cell=[...cal.querySelectorAll('[class*=day]')].filter(e=>e.children.length===0&&e.innerText.trim()===String(day))[0]; cell.click(); await W(1200);
}
const tin=d.querySelector('#time-of-day-container input'); tin.click(); await W(800);
const it=[...document.querySelectorAll('tp-yt-paper-item')].find(e=>e.innerText.trim()===timeTxt); it.scrollIntoView({block:'center'}); it.click(); await W(800);
const got=[d.querySelector('#datepicker-trigger').innerText.trim(), tin.value];
if(got[0]!==dateTxt||got[1]!==timeTxt) throw new Error('date/time mismatch '+got.join(' ')+' want '+dateTxt+' '+timeTxt);
d.querySelector('#done-button').click(); await W(6000);
[row.file, nt, (document.body.innerText.match(/\d{4}년 \d+월 \d+일 [\d:]+에 동영상이 공개/)||['?'])[0]]
