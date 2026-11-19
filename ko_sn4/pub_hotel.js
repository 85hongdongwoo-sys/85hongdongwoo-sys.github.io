const row={"title": "수험생 할인 3탄 | 호텔 뷔페 반값·뮤지컬 30%·대학로 연극 50%", "description": "https://honglife.co.kr/ipsi/suneung-2027.html\n\n수험생 이벤트 3탄! 호텔 뷔페·공연 할인 정리.\n· 켄싱턴호텔 여의도 브로드웨이 점심·저녁 뷔페 50%(11/30까지, 테이블당 수험생 1명)\n· 제주신라호텔 더 파크뷰 디너 뷔페 30%(11/19~11/30)\n· JW 메리어트 서울 플레이버즈 성인 3명 이상 동반 시 수험생 1명 무료(11/30까지 평일, 전화 예약)\n· 반얀트리 서울 평일 30%·주말 20%(11/30까지, 본인 포함 최대 4명)\n· 뮤지컬 스위니토드 R·S·A석 30%(공연 12/4~1/17)\n· 아르코·대학로예술극장 지정 연극 50%(11/20~22, 27~29)\n· 수험생 쉼표콘서트 10CM·소수빈 1인 1만 원(11/21 용인포은아트홀)\n\n수험표 할인 40곳 전체와 내 점수 등급·추정 백분위: https://honglife.co.kr/ipsi/suneung-2027.html\n혜택·기간은 업체 사정으로 바뀌거나 조기 종료될 수 있어요. 방문·예약 전 공식 안내를 꼭 확인하세요.\n수능 보느라 정말 수고 많았어요! 🎉\n더 많은 무료 도구: https://honglife.co.kr/\n\n#Shorts #수험생할인 #수능할인 #수험표할인 #수능 #2027수능 #호텔뷔페 #뮤지컬 #홍라이프", "tags": "수험표 할인,2027 수능,수험생 이벤트,수험생 할인,수능 할인,수험표 할인 2027,호텔 뷔페 수험생,켄싱턴호텔 수험생,JW메리어트 수험생,수험생 공연 할인,스위니토드 수험생,수험생 콘서트,수능 끝나고,홍라이프", "playlist": "홍라이프 도구 사용법 (한국어)"};
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
