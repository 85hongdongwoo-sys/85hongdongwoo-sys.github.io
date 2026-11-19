const row={"title": "로또 번호 생성기 무료 | 넣을 번호·뺄 번호 정해서 뽑기", "description": "https://honglife.co.kr/text/lotto.html\n\n1~45 중 6개 번호를 1·5·10게임 무작위로 뽑아 줘요.\n꼭 넣을 번호(최대 5개)와 뺄 번호를 정할 수 있고 번호 복사도 한 번에 돼요.\n① 게임 수 고르기 → ② 넣을/뺄 번호 적기 → ③ 번호 뽑기\n무작위로 뽑을 뿐 당첨 확률을 높여 주지는 않아요. 무료.\n\n더 많은 무료 도구: https://honglife.co.kr/\n\n#Shorts #로또 #로또번호 #로또번호생성기 #로또1등 #홍라이프", "tags": "로또 번호 생성기,로또 번호 추천,로또 자동,로또 번호 뽑기,로또 랜덤,홍라이프,생활 도구", "playlist": "홍라이프 도구 사용법 (한국어)", "date": "2026. 12. 2.", "month": 12, "day": 2, "time": "오후 7:00", "year": 2026};
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
