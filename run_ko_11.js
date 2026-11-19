const row={"title": "평수 계산기 | 84㎡ 몇 평? 제곱미터 평 변환", "description": "https://honglife.co.kr/life/pyeong.html\n\n제곱미터(㎡)와 평을 양쪽으로 바꾸고, 전용면적과 전용률로 흔히 부르는 평형도 계산해요.\n1평 = 3.3058㎡, ㎡ × 0.3025 = 평. 계산식과 변환표, 엑셀 받기도 있어요.\n① ㎡ 넣기 → ② 평 확인 → ③ 전용률로 평형 보기\n회원가입 없이 무료.\n\n더 많은 무료 도구: https://honglife.co.kr/\n\n#Shorts #평수계산 #평수 #아파트 #이사 #홍라이프", "tags": "평수 계산기,평 제곱미터 변환,84제곱미터 몇평,평형 계산,전용면적 평수,아파트 평수,홍라이프,생활 도구", "playlist": "홍라이프 도구 사용법 (한국어)", "date": "2026. 11. 29.", "month": 11, "day": 29, "time": "오후 7:00", "year": 2026};
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
const thumbOk=!!d.querySelector('ytcp-thumbnail-uploader img[src^="blob:"], ytcp-thumbnail-uploader img[src^="data:"]');
if(tt!==row.title||!pl.includes(row.playlist.slice(0,12))) throw new Error('fields not set: '+tt+' / '+pl);
for(let k=0;k<3;k++){d.querySelector('#next-button').click(); await W(2000);}
d.querySelector('#second-container-expand-button').click(); await W(1500);
if(d.querySelector('#datepicker-trigger').innerText.trim()!==row.date){
 d.querySelector('#datepicker-trigger').click(); await W(1500);
 const T=e=>(e.textContent||'').trim(); let cal; for(let k=0;k<20;k++){cal=document.querySelector('ytcp-scrollable-calendar'); if(cal&&cal.querySelector('.calendar-month-label'))break; await W(500);} await W(500);
 const leaves=[...cal.querySelectorAll('*')].filter(e=>e.children.length===0);
 const hdr=leaves.find(e=>T(e)===row.year+'년 '+row.month+'월');
 const nxt=leaves.filter(e=>/^\d{4}년 \d+월$/.test(T(e))&&e.getBoundingClientRect().top>hdr.getBoundingClientRect().top)[0];
 const y0=hdr.getBoundingClientRect().top, y1=nxt?nxt.getBoundingClientRect().top:1e9;
 const cell=leaves.find(e=>T(e)===String(row.day)&&e.getBoundingClientRect().top>y0&&e.getBoundingClientRect().top<y1);
 cell.click(); await W(1200);
}
const tin=d.querySelector('#time-of-day-container input'); tin.click(); await W(800);
const it=[...document.querySelectorAll('tp-yt-paper-item')].find(e=>e.innerText.trim()===row.time); it.scrollIntoView({block:'center'}); it.click(); await W(800);
const got=[d.querySelector('#datepicker-trigger').innerText.trim(), tin.value];
if(got[0]!==row.date||got[1]!==row.time) throw new Error('date/time mismatch '+got.join(' ')+' want '+row.date+' '+row.time);
d.querySelector('#done-button').click(); await W(6000);
JSON.stringify({tags:nt,thumb:thumbOk,sched:(document.body.innerText.match(/\d{4}년 \d+월 \d+일 [^\n]{0,20}에 동영상이 공개/)||['?'])[0]})
