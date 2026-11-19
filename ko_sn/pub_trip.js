const row={"title": "수험표 할인 2027 | 제주항공·이스타항공·트리니티 항공권 25%, 숙박 반값 이벤트", "description": "https://honglife.co.kr/ipsi/suneung-2027.html\n\n수능 끝나고 여행 간다면 수험표 꼭 챙기세요! 항공·숙박 수험생 이벤트 정리.\n· 제주항공 국내선 플렉스 운임 20%(예매 12/16까지, 본인+동반 1명)\n· 이스타항공 국내선 25%·국제선 최대 10%(구매 12/31까지)\n· 트리니티항공 국내선 25%·국제선 최대 20%(예매 1/31까지)\n· 국립 산림복지시설 10곳 숙박 주중 30%·주말 10%(숲e랑 예약)\n· 하이서울유스호스텔 객실 50%(11/30까지, 만 24세 이하)\n\n수험표 할인 23곳 전체와 내 점수 등급·추정 백분위: https://honglife.co.kr/ipsi/suneung-2027.html\n혜택·기간은 업체 사정으로 바뀌거나 조기 종료될 수 있어요. 방문·예약 전 공식 안내를 꼭 확인하세요.\n더 많은 무료 도구: https://honglife.co.kr/\n\n#Shorts #수험표할인 #수능할인 #수험생할인 #수능 #2027수능 #제주항공 #이스타항공 #홍라이프", "tags": "수험표 할인,2027 수능,수험생 이벤트,수험생 할인,수능 할인,수험표 할인 2027,수험생 항공권 할인,제주항공 수험생,이스타항공 수험생,트리니티항공 수험생,수험생 여행,수능 백분위,수능 등급컷,홍라이프", "playlist": "홍라이프 도구 사용법 (한국어)"};
const W=ms=>new Promise(r=>setTimeout(r,ms));
const setText=(el,txt)=>{el.focus();document.execCommand('selectAll',false,null);document.execCommand('insertText',false,txt);el.dispatchEvent(new Event('input',{bubbles:true}))};
let d; for(let k=0;k<60;k++){d=document.querySelector('ytcp-uploads-dialog'); if(d&&d.querySelector('#title-textarea #textbox'))break; await W(500);}
await W(2500);
let pd; for(let k=0;k<6&&!pd;k++){d.querySelector('ytcp-video-metadata-playlists ytcp-dropdown-trigger').click(); await W(2500);
 pd=[...document.querySelectorAll('ytcp-playlist-dialog, tp-yt-paper-dialog')].find(x=>x.offsetParent&&x.innerText.includes(row.playlist));
 if(!pd){const p2=[...document.querySelectorAll('ytcp-playlist-dialog, tp-yt-paper-dialog')].find(x=>x.offsetParent&&x.innerText.includes('완료')); [...(p2?.querySelectorAll('ytcp-button,button')||[])].find(b=>b.innerText.trim()==='완료')?.click(); await W(2500);}}
const lt=c=>{let e=c;while(e&&!(e.innerText||'').trim())e=e.parentElement;return (e?.innerText||'').trim()};const cb=[...pd.querySelectorAll('ytcp-checkbox-lit')].find(c=>lt(c)===row.playlist); if(cb.getAttribute('aria-checked')!=='true'&&!cb.hasAttribute('checked')) cb.click(); await W(500);
[...pd.querySelectorAll('ytcp-button,button')].find(b=>b.innerText.trim()==='완료').click(); await W(1200);
setText(d.querySelector('#title-textarea #textbox'),row.title); setText(d.querySelector('#description-textarea #textbox'),row.description);
d.querySelector('tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]').click(); await W(2000);
if(!d.querySelector('#tags-container')?.offsetParent){d.querySelector('#toggle-button').click(); await W(1500);}
const tg=[...d.querySelectorAll('input')].find(i=>/태그/.test(i.getAttribute('aria-label')||'')); tg.focus(); tg.value=row.tags+','; tg.dispatchEvent(new Event('input',{bubbles:true})); tg.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); tg.blur(); await W(800);
const nt=d.querySelectorAll('#tags-container ytcp-chip').length, tt=d.querySelector('#title-textarea #textbox').innerText, pl=d.querySelector('ytcp-video-metadata-playlists').innerText;
const thumbOk=!!d.querySelector('ytcp-thumbnail-uploader img[src^="blob:"], ytcp-thumbnail-uploader img[src^="data:"]');
if(tt!==row.title||!pl.includes(row.playlist)) throw new Error('fields not set: '+tt+' / '+pl);
for(let k=0;k<3;k++){d.querySelector('#next-button').click(); await W(2000);}
d.querySelector('tp-yt-paper-radio-button[name=PUBLIC]').click(); await W(1200);
const pubOk=d.querySelector('tp-yt-paper-radio-button[name=PUBLIC]').hasAttribute('checked')||d.querySelector('tp-yt-paper-radio-button[name=PUBLIC]').getAttribute('aria-checked')==='true';
d.querySelector('#done-button').click(); await W(7000);
const link=(document.querySelector('ytcp-video-info a[href*="youtu"], a.ytcp-video-info[href*="youtu"]')||{}).href||((document.body.innerText.match(/https:\/\/youtube\.com\/shorts\/[\w-]+|https:\/\/youtu\.be\/[\w-]+/)||[''])[0]);
JSON.stringify({tags:nt,thumb:thumbOk,pub:pubOk,link})
