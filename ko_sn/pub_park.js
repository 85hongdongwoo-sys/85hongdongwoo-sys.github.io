const row={"title": "수험표 할인 2027 | 에버랜드 2만 원·롯데월드·레고랜드·아쿠아리움 총정리", "description": "https://honglife.co.kr/ipsi/suneung-2027.html\n\n수능 끝났다면 수험표 버리지 마세요! 테마파크·아쿠아리움 수험생 할인 정리.\n· 에버랜드 수험생 이용권 2만 원(동반 최대 3명 1인 3만 원, 12/31까지, 스마트 예약)\n· 롯데월드 어드벤처 서울 2만 7천 원 · 부산 2만 원\n· 서울랜드 본인·동반 2명 각 2만 500원\n· 레고랜드 본인 40%·동반 3명 30%(현장 매표소)\n· 씨라이프 코엑스·부산 본인 50% · 롯데월드 아쿠아리움 1만 8,500원 · 서울스카이 1만 6,500원\n· 아산스파비스 워터파크 종일권 1만 원\n\n수험표 할인 23곳 전체와 내 점수 등급·추정 백분위: https://honglife.co.kr/ipsi/suneung-2027.html\n혜택·기간은 업체 사정으로 바뀌거나 조기 종료될 수 있어요. 방문·예약 전 공식 안내를 꼭 확인하세요.\n더 많은 무료 도구: https://honglife.co.kr/\n\n#Shorts #수험표할인 #수능 #2027수능 #에버랜드 #롯데월드 #수험생할인 #홍라이프", "tags": "수험표 할인,수험표 할인 2027,수능 수험표 할인,수험생 할인,에버랜드 수험생,롯데월드 수험생,레고랜드 수험생,서울랜드 수험표,아쿠아리움 수험생 할인,수능 끝나고,홍라이프", "playlist": "홍라이프 도구 사용법 (한국어)"};
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
d.querySelector('tp-yt-paper-radio-button[name=PUBLIC]').click(); await W(1200);
const pubOk=d.querySelector('tp-yt-paper-radio-button[name=PUBLIC]').hasAttribute('checked')||d.querySelector('tp-yt-paper-radio-button[name=PUBLIC]').getAttribute('aria-checked')==='true';
d.querySelector('#done-button').click(); await W(7000);
const link=(document.querySelector('ytcp-video-info a[href*="youtu"], a.ytcp-video-info[href*="youtu"]')||{}).href||((document.body.innerText.match(/https:\/\/youtube\.com\/shorts\/[\w-]+|https:\/\/youtu\.be\/[\w-]+/)||[''])[0]);
JSON.stringify({tags:nt,thumb:thumbOk,pub:pubOk,link})
