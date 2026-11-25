#!/usr/bin/env python3
"""이미지 웹앱 (/image/…) — 필름 카메라 필터 등. 모두 브라우저 안에서 처리.
로컬에서 돌리고 overlay 결과를 커밋해요: python3 build/newpages/gen_image_apps.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hwp'))
import gen_hwp_tools as G

SEC = ('이미지', '/image/')

REL = ('<section class="card rel"><h2>함께 쓰면 좋은 이미지 도구</h2><ul>'
       '<li><a href="/image/date-stamp.html"><b>사진 날짜 도장</b><span>촬영 날짜를 필름 카메라 주황 숫자로</span></a></li>'
       '<li><a href="/image/frame.html"><b>사진 테두리·폴라로이드 액자</b><span>흰 여백·폴라로이드 틀</span></a></li>'
       '<li><a href="/image/photo-adjust.html"><b>사진 밝기·색 보정</b><span>밝기·대비·채도 직접 조절</span></a></li>'
       '<li><a href="/image/photo-effects.html"><b>사진 효과 모음</b><span>흑백·세피아·흐림 등</span></a></li>'
       '<li><a href="/image/glitch.html"><b>글리치 효과</b><span>화면 깨짐·RGB 어긋남</span></a></li>'
       '<li><a href="/image/collage.html"><b>사진 콜라주</b><span>여러 장을 한 장으로</span></a></li></ul></section>')

FF_CSS = ('<style>#tool h2{margin:22px 0 10px}.ff-view{position:relative;margin-top:12px;background:#F1F3F6;border-radius:14px;min-height:160px;display:flex;align-items:center;justify-content:center;overflow:hidden}'
          '.ff-view canvas{display:block;max-width:100%;max-height:70vh;height:auto}.ff-view video{display:none}'
          '.ff-empty{color:#5B6B82;font-size:15px;padding:30px 16px;text-align:center;margin:0}'
          '.ff-chips{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}@media(max-width:520px){.ff-chips{grid-template-columns:repeat(2,minmax(0,1fr))}}'
          '.ff-chip{border:1.5px solid #D9DDE3;background:#fff;border-radius:12px;padding:6px;cursor:pointer;font:inherit;font-size:14px;font-weight:700;color:#1F2937;display:flex;flex-direction:column;align-items:center;gap:5px;min-width:0}'
          '.ff-chip canvas{width:100%;aspect-ratio:4/3;border-radius:8px;background:#E3E6EB;display:block}.ff-chip span{overflow-wrap:anywhere;text-align:center;line-height:1.3}'
          '.ff-chip[aria-pressed=true]{border-color:#1D4ED8;box-shadow:0 0 0 2px #1D4ED8 inset;color:#1D4ED8}'
          '.ff-th{display:flex;gap:8px;overflow-x:auto;padding:8px 2px 2px}.ff-th button{flex:0 0 auto;border:2px solid transparent;border-radius:10px;padding:0;background:none;cursor:pointer}'
          '.ff-th button[aria-current=true]{border-color:#1D4ED8}.ff-th img{width:64px;height:64px;object-fit:cover;border-radius:8px;display:block}'
          '.ff-cam{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.ff-shot{width:64px;height:64px;border-radius:50%;border:4px solid #fff;background:#E5484D;box-shadow:0 0 0 2px #1F2937;cursor:pointer;font-size:0}'
          '.ff-camrow{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:10px;flex-wrap:wrap}'
          '.ff-chk{display:flex;align-items:center;gap:8px;font-weight:700}.ff-chk input{width:20px;height:20px}'
          '#tool .btns{flex-wrap:wrap}</style>')

FF_TOOL = ("""<section class="card tool" id="tool">""" + FF_CSS + """
<div class="drop" id="drop"><b>사진을 놓거나 눌러서 고르세요 (여러 장)</b><span>JPG · PNG · WEBP · HEIC — 사진은 내 폰·PC 밖으로 나가지 않아요</span></div>
<div class="ff-camrow"><button class="btn ghost" id="camOn" type="button">카메라로 바로 찍기</button></div>
<div class="ff-view" id="view"><p class="ff-empty" id="empty">사진을 고르거나 카메라를 켜면 여기에 필름 느낌으로 보여요.</p><canvas id="cv" aria-label="필름 필터 미리보기" hidden></canvas><video id="vd" playsinline muted></video></div>
<div class="ff-camrow" id="camBar" hidden><button class="btn ghost sm" id="camFlip" type="button">앞·뒤 카메라</button><button class="ff-shot" id="shot" type="button" aria-label="찍기">찍기</button><button class="btn ghost sm" id="camOff" type="button">카메라 끄기</button></div>
<div class="ff-th" id="th" aria-label="고른 사진"></div>
<h2>필름 고르기</h2>
<div class="ff-chips" id="chips"></div>
<h2>세부 조절</h2>
<div class="grid g2">
<div class="f"><label for="k">필름 색 세기 <b id="kv">100</b>%</label><input type="range" id="k" min="0" max="150" value="100"></div>
<div class="f"><label for="g">필름 입자(거친 점) <b id="gv">0</b></label><input type="range" id="g" min="0" max="100" value="0"></div>
<div class="f"><label for="v">가장자리 어둡게 <b id="vv">0</b></label><input type="range" id="v" min="0" max="100" value="0"></div>
<div class="f"><label for="l">빛샘(주황 빛 번짐) <b id="lv">0</b></label><input type="range" id="l" min="0" max="100" value="0"></div>
<div class="f"><label class="ff-chk"><input type="checkbox" id="d"> 날짜 도장 넣기</label><small>’25 11 25처럼 주황 숫자. 사진 파일 날짜를 써요. 바꾸려면 오른쪽에 날짜를 고르세요.</small></div>
<div class="f"><label for="dd">날짜 직접 정하기 (선택)</label><input type="date" id="dd"></div>
</div>
<div class="btns"><button class="btn dl" id="save" type="button" disabled>이 사진 저장 (JPG)</button><button class="btn ghost" id="saveAll" type="button" disabled>모두 저장 (ZIP)</button><button class="btn ghost" id="hold" type="button" disabled>누르고 있으면 원본</button><button class="btn ghost" id="share" type="button">내 필름 설정 링크 복사</button><button class="btn ghost sm" id="clr" type="button" disabled>비우기</button></div>
<p class="note" id="st"></p>
</section>""", """<script src="/assets/js/hlimg.js?v=6b8ffd0b"></script>
<script>
(function(){var $=HL.$;
var N={sat:1,con:1,fade:0,warm:0,tint:0};
var P={
 none:{n:'원본',sat:1,con:1,fade:0,warm:0,tint:0,g:0,v:0,l:0},
 warm:{n:'따뜻한 필름',sat:.92,con:1.08,fade:.07,warm:.55,tint:.12,g:35,v:35,l:0},
 cool:{n:'시원한 필름',sat:.86,con:1.06,fade:.06,warm:-.45,tint:-.18,g:30,v:30,l:0},
 bw:{n:'흑백 필름',sat:0,con:1.22,fade:.05,warm:0,tint:0,g:55,v:40,l:0},
 faded:{n:'빛바랜 사진',sat:.68,con:.86,fade:.17,warm:.35,tint:.22,g:30,v:25,l:35},
 vivid:{n:'선명한 슬라이드',sat:1.32,con:1.16,fade:0,warm:.1,tint:0,g:15,v:30,l:0},
 y2k:{n:'Y2K 디카',sat:1.15,con:1.1,fade:.03,warm:.12,tint:-.06,g:22,v:8,l:0,low:1280,flash:1,date:1},
 phone:{n:'올드폰',sat:.78,con:.93,fade:.09,warm:-.12,tint:-.28,g:18,v:22,l:0,low:400,jpg:.32}
};
var KEYS=Object.keys(P);
var items=[],cur=-1,pre='warm',live=null,facing='environment',holding=false;
var R={p:'warm',k:100,g:35,v:35,l:0,d:0};
/* noise tile */
var NZ=document.createElement('canvas');NZ.width=NZ.height=256;(function(){var c=NZ.getContext('2d'),im=c.createImageData(256,256),a=im.data;for(var i=0;i<a.length;i+=4){var x=128+(Math.random()+Math.random()+Math.random()-1.5)*120;a[i]=a[i+1]=a[i+2]=x;a[i+3]=255}c.putImageData(im,0,0)})();
function eff(){var p=P[R.p],k=R.k/100,o={};for(var key in N)o[key]=N[key]+(p[key]-N[key])*k;return o}
function luts(o){var L=[new Uint8ClampedArray(256),new Uint8ClampedArray(256),new Uint8ClampedArray(256)];
 var gr=1+o.warm*.13+o.tint*.04,gg=1-o.tint*.08,gb=1-o.warm*.15+o.tint*.05;var G=[gr,gg,gb];
 for(var c=0;c<3;c++)for(var i=0;i<256;i++){var x=i/255;x=(x-.5)*o.con+.5;x=x*G[c];x=o.fade*.75+x*(1-o.fade);L[c][i]=Math.round(x*255)}return L}
function rnd(s){return function(){s=(s*9301+49297)%233280;return s/233280}}
function stampTxt(t){var d=new Date(t);return '\\u2019'+String(d.getFullYear()).slice(2)+' '+('0'+(d.getMonth()+1)).slice(-2)+' '+('0'+d.getDate()).slice(-2)}
/* sync pipeline: src(image/video/canvas), sw,sh → canvas cv (w,h) */
function paint(cv,src,sw,sh,maxSide,opt){opt=opt||{};var p=P[R.p];var sc=Math.min(1,maxSide/Math.max(sw,sh));var w=Math.max(1,Math.round(sw*sc)),h=Math.max(1,Math.round(sh*sc));
 cv.width=w;cv.height=h;var c=cv.getContext('2d',{willReadFrequently:true});c.save();
 if(opt.mirror){c.translate(w,0);c.scale(-1,1)}
 if(p.low&&Math.max(w,h)>p.low*(opt.fast?.6:1)){var lw=p.low*(opt.fast?.6:1),s2=lw/Math.max(w,h),t=document.createElement('canvas');t.width=Math.max(1,Math.round(w*s2));t.height=Math.max(1,Math.round(h*s2));var tc=t.getContext('2d');tc.imageSmoothingQuality='low';tc.drawImage(src,0,0,t.width,t.height);c.imageSmoothingEnabled=true;c.drawImage(t,0,0,w,h)}
 else c.drawImage(src,0,0,w,h);
 c.restore();if(R.p==='none'&&!R.g&&!R.v&&!R.l&&!R.d)return cv;
 var o=eff(),L=luts(o),im=c.getImageData(0,0,w,h),a=im.data,s=o.sat,r0=L[0],g0=L[1],b0=L[2];
 for(var i=0;i<a.length;i+=4){var r=a[i],g=a[i+1],b=a[i+2],y=.299*r+.587*g+.114*b;r=y+(r-y)*s;g=y+(g-y)*s;b=y+(b-y)*s;
  a[i]=r0[r<0?0:r>255?255:r|0];a[i+1]=g0[g<0?0:g>255?255:g|0];a[i+2]=b0[b<0?0:b>255?255:b|0]}
 c.putImageData(im,0,0);var m=Math.max(w,h),ms=Math.min(w,h),rn=rnd(opt.seed||7);
 if(p.flash){var fg=c.createRadialGradient(w/2,h*.45,0,w/2,h*.45,m*.55);fg.addColorStop(0,'rgba(255,255,255,.22)');fg.addColorStop(1,'rgba(255,255,255,0)');c.globalCompositeOperation='soft-light';c.fillStyle=fg;c.fillRect(0,0,w,h)}
 if(R.l>0){var lx=rn()<.5?0:w,ly=h*(.15+rn()*.7),lg=c.createRadialGradient(lx,ly,0,lx,ly,m*.6);var la=R.l/100;lg.addColorStop(0,'rgba(255,110,30,'+(.75*la)+')');lg.addColorStop(.45,'rgba(255,60,40,'+(.3*la)+')');lg.addColorStop(1,'rgba(255,60,40,0)');c.globalCompositeOperation='screen';c.fillStyle=lg;c.fillRect(0,0,w,h)}
 if(R.g>0){c.globalCompositeOperation='overlay';c.globalAlpha=R.g/100*.55;var pat=c.createPattern(NZ,'repeat');var zs=Math.max(1,m/1400);c.save();c.scale(zs,zs);c.translate(rn()*256,rn()*256);c.fillStyle=pat;c.fillRect(-256,-256,w/zs+512,h/zs+512);c.restore();c.globalAlpha=1}
 if(R.v>0){var vg=c.createRadialGradient(w/2,h/2,ms*.35,w/2,h/2,Math.sqrt(w*w+h*h)/2);vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,'+(R.v/100*.75)+')');c.globalCompositeOperation='source-over';c.fillStyle=vg;c.fillRect(0,0,w,h)}
 c.globalCompositeOperation='source-over';
 if(R.d&&opt.date){var fs=Math.max(10,Math.round(ms*.045));c.font='700 '+fs+'px "Courier New",monospace';c.textAlign='right';c.textBaseline='alphabetic';c.shadowColor='rgba(255,120,20,.9)';c.shadowBlur=fs*.35;c.fillStyle='#FF8A1E';var tx=stampTxt(opt.date);c.fillText(tx,w-fs*.9,h-fs*.8);c.shadowBlur=0;c.fillText(tx,w-fs*.9,h-fs*.8)}
 return cv}
function jpgRound(cv){var p=P[R.p];if(!p.jpg)return Promise.resolve(cv);return HL.canvasBlob(cv,'image/jpeg',p.jpg).then(function(b){return createImageBitmap(b)}).then(function(bm){cv.getContext('2d').drawImage(bm,0,0);return cv})}
var cv=$('#cv'),busy=0;
function dateOf(it){var v=$('#dd').value;if(v){var q=v.split('-');return new Date(+q[0],+q[1]-1,+q[2]).getTime()}return it.t||Date.now()}
function show(){if(live)return;var it=items[cur];if(!it){cv.hidden=true;$('#empty').hidden=false;return}cv.hidden=false;$('#empty').hidden=true;
 if(holding){var c=cv.getContext('2d');cv.width=Math.round(it.w*Math.min(1,1400/Math.max(it.w,it.h)));cv.height=Math.round(it.h*cv.width/it.w);c.drawImage(it.img,0,0,cv.width,cv.height);return}
 var my=++busy;paint(cv,it.img,it.w,it.h,1400,{seed:cur+3,date:dateOf(it)});jpgRound(cv).then(function(){if(my!==busy)return})}
function chipArt(){var src=items[cur];var keep=R.p;KEYS.forEach(function(k){var cc=document.getElementById('cp-'+k);if(!cc)return;var x=cc.getContext('2d');var old=R.p,ok=R.k,og=R.g,ov=R.v,ol=R.l,od=R.d;R.p=k;R.k=100;R.g=P[k].g;R.v=P[k].v;R.l=P[k].l;R.d=0;
  if(src){var t=document.createElement('canvas');paint(t,src.img,src.w,src.h,180,{seed:5,fast:1});cc.width=160;cc.height=120;var s=Math.max(160/t.width,120/t.height);x.drawImage(t,(160-t.width*s)/2,(120-t.height*s)/2,t.width*s,t.height*s)}
  else{cc.width=160;cc.height=120;var gd=x.createLinearGradient(0,0,160,120);gd.addColorStop(0,'#8FB3E8');gd.addColorStop(.55,'#F3C98B');gd.addColorStop(1,'#5A6B7A');x.fillStyle=gd;x.fillRect(0,0,160,120);x.fillStyle='#F7E3B5';x.beginPath();x.arc(112,38,16,0,7);x.fill();x.fillStyle='#3E5A48';x.beginPath();x.moveTo(0,120);x.lineTo(50,70);x.lineTo(95,110);x.lineTo(130,80);x.lineTo(160,105);x.lineTo(160,120);x.fill();var t2=document.createElement('canvas');paint(t2,cc,160,120,160,{seed:5,fast:1});x.drawImage(t2,0,0)}
  R.p=old;R.k=ok;R.g=og;R.v=ov;R.l=ol;R.d=od})}
function chips(){$('#chips').innerHTML=KEYS.map(function(k){return '<button type="button" class="ff-chip" data-k="'+k+'" aria-pressed="'+(k===R.p)+'"><canvas id="cp-'+k+'" width="160" height="120"></canvas><span>'+P[k].n+'</span></button>'}).join('');
 Array.prototype.forEach.call(document.querySelectorAll('.ff-chip'),function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-k'),true)})});chipArt()}
function sync(){['k','g','v','l'].forEach(function(x){$('#'+x).value=R[x];$('#'+x+'v').textContent=R[x]});$('#d').checked=!!R.d;
 Array.prototype.forEach.call(document.querySelectorAll('.ff-chip'),function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-k')===R.p))});HL.store.set('film-recipe',R)}
function pick(k,reset){if(!P[k])return;R.p=k;if(reset){R.k=100;R.g=P[k].g;R.v=P[k].v;R.l=P[k].l;R.d=P[k].date?1:0}sync();show()}
['k','g','v','l'].forEach(function(x){$('#'+x).addEventListener('input',function(){R[x]=+this.value;sync();show()})});
$('#d').addEventListener('change',function(){R.d=this.checked?1:0;sync();show()});$('#dd').addEventListener('change',show);
function thumbs(){$('#th').innerHTML=items.map(function(it,i){return '<button type="button" data-i="'+i+'" aria-current="'+(i===cur)+'" aria-label="'+HL.esc(it.name)+'"><img src="'+it.url+'" alt=""></button>'}).join('');
 Array.prototype.forEach.call(document.querySelectorAll('#th button'),function(b){b.addEventListener('click',function(){cur=+b.getAttribute('data-i');thumbs();show();chipArt()})});
 var has=items.length>0;['save','hold','clr'].forEach(function(x){$('#'+x).disabled=!has});$('#saveAll').disabled=items.length<2;$('#st').textContent=has?items.length+'장 · 저장할 때 원래 크기(긴 변 최대 4000px)로 만들어요.':''}
async function add(fs){for(var i=0;i<fs.length;i++){try{var it=await HLI.load(fs[i]);items.push({name:fs[i].name||'photo.jpg',img:it.img,w:it.w,h:it.h,t:fs[i].lastModified,url:it.img.src})}catch(e){HL.toast(e.message||'사진을 읽지 못했어요')}}
 if(cur<0&&items.length)cur=0;thumbs();show();chipArt()}
HL.dropzone($('#drop'),{accept:'image/*,.heic,.heif',multiple:true,onFiles:function(fs){stopCam();add(fs)}});
async function full(it,i){var t=document.createElement('canvas');paint(t,it.img,it.w,it.h,P[R.p].low?Math.max(P[R.p].low*2,800):4000,{seed:i+3,date:dateOf(it)});await jpgRound(t);return HLI.blob(t,'image/jpeg',.92)}
function outName(it){return HL.baseName(it.name)+'_'+P[R.p].n.replace(/\\s+/g,'')+'.jpg'}
$('#save').addEventListener('click',async function(){var it=items[cur];if(!it)return;HL.download(await full(it,cur),outName(it))});
$('#saveAll').addEventListener('click',async function(){var out=[];for(var i=0;i<items.length;i++){$('#st').textContent=(i+1)+' / '+items.length+'장 만드는 중…';out.push({name:outName(items[i]),blob:await full(items[i],i)})}await HLI.save(out,'필름사진_'+out.length+'장.zip');$('#st').textContent=out.length+'장을 저장했어요.'});
function hold(on){holding=on;show()}var hb=$('#hold');['pointerdown'].forEach(function(e){hb.addEventListener(e,function(){hold(true)})});['pointerup','pointerleave','pointercancel'].forEach(function(e){hb.addEventListener(e,function(){if(holding)hold(false)})});
$('#clr').addEventListener('click',function(){items=[];cur=-1;thumbs();show();chipArt()});
/* recipe link */
function enc(){return 'f='+[R.p,R.k,R.g,R.v,R.l,R.d].join('.')}
function dec(h){var m=/f=([a-z0-9]+)\\.(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d)/.exec(h||'');if(!m||!P[m[1]])return false;R={p:m[1],k:Math.min(150,+m[2]),g:Math.min(100,+m[3]),v:Math.min(100,+m[4]),l:Math.min(100,+m[5]),d:+m[6]?1:0};return true}
$('#share').addEventListener('click',function(){var u=location.origin+location.pathname+'#'+enc();try{history.replaceState(null,'','#'+enc())}catch(e){}HL.copy(u,'필름 설정 링크를 복사했어요. 친구가 열면 같은 필름이 골라져요.')});
/* camera */
var stream=null,vd=$('#vd'),raf=0,lt=0;
async function startCam(){if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){HL.toast('이 브라우저는 카메라를 쓸 수 없어요. 사진 고르기를 써 주세요.');return}
 try{stopCam();stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing,width:{ideal:1920},height:{ideal:1080}},audio:false});vd.srcObject=stream;await vd.play();live=true;$('#camBar').hidden=false;$('#camOn').hidden=true;cv.hidden=false;$('#empty').hidden=true;loop()}
 catch(e){HL.toast(e&&e.name==='NotAllowedError'?'카메라 권한을 허용해 주세요. 주소창 옆 자물쇠에서 바꿀 수 있어요.':'카메라를 켜지 못했어요.');live=null}}
function stopCam(){cancelAnimationFrame(raf);if(stream){stream.getTracks().forEach(function(t){t.stop()})}stream=null;live=null;$('#camBar').hidden=true;$('#camOn').hidden=false}
function loop(t){raf=requestAnimationFrame(loop);if(!live||!vd.videoWidth)return;if(t-lt<40)return;lt=t;paint(cv,vd,vd.videoWidth,vd.videoHeight,640,{fast:1,mirror:facing==='user',seed:3,date:Date.now()})}
$('#camOn').addEventListener('click',startCam);$('#camOff').addEventListener('click',function(){stopCam();show()});
$('#camFlip').addEventListener('click',function(){facing=facing==='user'?'environment':'user';startCam()});
$('#shot').addEventListener('click',async function(){if(!vd.videoWidth)return;var t=document.createElement('canvas');t.width=vd.videoWidth;t.height=vd.videoHeight;var c=t.getContext('2d');if(facing==='user'){c.translate(t.width,0);c.scale(-1,1)}c.drawImage(vd,0,0);
 var b=await HLI.blob(t,'image/jpeg',.95);var f=new File([b],'camera_'+HL.stamp()+'_'+(items.length+1)+'.jpg',{type:'image/jpeg',lastModified:Date.now()});
 var it=await HLI.load(f);items.push({name:f.name,img:it.img,w:it.w,h:it.h,t:Date.now(),url:it.img.src});cur=items.length-1;thumbs();HL.toast('찍었어요. 아래 사진 목록에 담겼어요.')});
/* init */
if(!dec(location.hash)){var sv=HL.store.get('film-recipe',null);if(sv&&P[sv.p])R=Object.assign(R,sv)}
chips();sync();thumbs();
})();
</script>""")

FF = dict(slug='film-filter', url='/image/film-filter.html', sec=SEC, crumb3='',
  name='필름 카메라 필터 (Y2K 디카·올드폰·흑백 필름, 카메라로 바로 찍기)',
  h1='<b>필름 카메라</b> 필터', lead='사진을 넣거나 카메라로 바로 찍으면 필름 카메라·Y2K 디카·올드폰 느낌으로 바꿔 줘요. 필름 8가지, 입자·빛샘·날짜 도장, 여러 장 한 번에 저장까지 무료예요.',
  desc='사진을 필름 카메라 느낌으로 바꾸는 무료 필터 앱이에요. 따뜻한 필름·시원한 필름·흑백·빛바랜 사진·Y2K 디카·올드폰 8가지, 필름 입자·가장자리 어둡게·빛샘·주황 날짜 도장, 카메라로 바로 찍기, 여러 장 ZIP 저장, 내 필름 설정 링크 공유. 사진은 서버로 보내지 않아요.',
  tool=FF_TOOL, warn='', nosafe=True,
  body=[
    ('사용 방법 (3단계)', '<ol><li><b>사진 고르기</b> — 위 칸을 눌러 사진을 여러 장 고르거나, ‘카메라로 바로 찍기’를 눌러요. 카메라는 화면에 필름 느낌이 바로 보여요.</li>'
      '<li><b>필름 고르기</b> — 8가지 필름 가운데 하나를 눌러요. 작은 그림이 내 사진으로 바뀌어 미리 보여요.</li>'
      '<li><b>저장</b> — ‘이 사진 저장’은 1장, ‘모두 저장’은 여러 장을 ZIP 하나로 받아요. ‘누르고 있으면 원본’으로 전후를 비교할 수 있어요.</li></ol>'),
    ('필름 8가지 차이', '<table class="tbl"><thead><tr><th>필름</th><th>느낌</th><th>잘 어울리는 사진</th></tr></thead><tbody>'
      '<tr><td>따뜻한 필름</td><td>노르스름하고 부드러운 색, 입자 조금</td><td>여행·카페·노을</td></tr>'
      '<tr><td>시원한 필름</td><td>푸르스름하고 차분한 색</td><td>바다·겨울·도시</td></tr>'
      '<tr><td>흑백 필름</td><td>대비가 강한 흑백, 입자 많이</td><td>인물·거리 사진</td></tr>'
      '<tr><td>빛바랜 사진</td><td>색이 빠지고 검은색이 뿌옇게, 빛샘</td><td>옛날 앨범 느낌</td></tr>'
      '<tr><td>선명한 슬라이드</td><td>채도·대비가 높은 쨍한 색</td><td>꽃·음식·하늘</td></tr>'
      '<tr><td>Y2K 디카</td><td>2000년대 디지털카메라: 쨍한 색, 플래시, 주황 날짜</td><td>친구·파티·셀카</td></tr>'
      '<tr><td>올드폰</td><td>예전 폴더폰 카메라: 낮은 화소, 뭉개진 압축, 초록빛</td><td>재미있는 일상 사진</td></tr>'
      '<tr><td>원본</td><td>색은 그대로, 입자·빛샘·날짜만 따로 넣을 때</td><td>—</td></tr></tbody></table>'),
    ('세부 조절은 이렇게', '<ul><li><b>필름 색 세기</b> — 0%면 원본 색, 100%가 기본, 150%까지 더 진하게 할 수 있어요.</li>'
      '<li><b>필름 입자</b> — 필름 사진의 거친 점(그레인)이에요. 흑백은 50 이상, 컬러는 20~40이 자연스러워요.</li>'
      '<li><b>가장자리 어둡게</b> — 렌즈 가장자리가 어두워지는 비네팅이에요. 시선이 가운데로 모여요.</li>'
      '<li><b>빛샘</b> — 필름에 빛이 새서 생기는 주황·빨강 번짐이에요. 사진마다 위치가 조금씩 달라져요.</li>'
      '<li><b>날짜 도장</b> — 사진 파일에 적힌 날짜를 ’25 11 25처럼 주황 숫자로 찍어요. 촬영 날짜를 정확히 쓰고 싶으면 <a href="/image/date-stamp.html">사진 날짜 도장</a> 도구를 쓰세요.</li></ul>'),
    ('내 필름 설정 공유하기', '<p>‘내 필름 설정 링크 복사’를 누르면 지금 고른 필름과 세부 값이 링크 하나에 담겨요. 이 링크를 친구에게 보내면 친구 화면에서도 같은 필름이 골라져요. 사진은 링크에 들어가지 않아요. 마지막에 쓴 설정은 이 브라우저에 저장돼서 다음에 열어도 그대로예요.</p>'),
    ('사진은 어디로 가나요?', '<p>모든 처리는 내 폰·PC의 브라우저 안에서 해요. 사진과 카메라 화면은 홍라이프 서버로 보내지 않아요. 카메라는 ‘카메라로 바로 찍기’를 눌렀을 때만 켜지고, ‘카메라 끄기’를 누르거나 페이지를 닫으면 꺼져요.</p>'
      '<p>저장한 사진은 원래 크기(긴 변 최대 4000px)의 JPG예요. 올드폰은 일부러 작은 화소로, Y2K 디카는 조금 낮은 화소로 저장해서 그 시절 느낌을 살려요.</p>'),
  ],
  faq=[('필름 카메라 필터 앱 없이 무료로 쓸 수 있나요?', '네. 설치나 가입 없이 이 페이지에서 바로 써요. 홈 화면에 추가하면 앱처럼 열 수 있어요.'),
       ('카메라로 찍을 때도 필터가 보이나요?', '네. ‘카메라로 바로 찍기’를 누르면 화면에 고른 필름 느낌이 실시간으로 보이고, 빨간 버튼으로 찍으면 사진 목록에 담겨요. 화면 미리보기는 가볍게 보여 주고, 저장할 때 큰 사진으로 다시 만들어요.'),
       ('카메라가 안 켜져요.', '브라우저가 카메라 권한을 물으면 ‘허용’을 눌러 주세요. 이미 거절했다면 주소창 옆 자물쇠 아이콘에서 카메라를 허용으로 바꾸면 돼요. 카카오톡 같은 앱 안 브라우저에서는 카메라가 안 될 수 있으니 크롬·사파리로 열어 주세요.'),
       ('아이폰 HEIC 사진도 되나요?', '네. HEIC 사진도 넣으면 바꿔서 처리하고 JPG로 저장해요.'),
       ('Y2K 디카 느낌은 어떻게 내나요?', '‘Y2K 디카’를 누르면 쨍한 색, 플래시 빛, 주황 날짜 도장이 함께 들어가요. 화소를 살짝 낮춰 2000년대 디지털카메라처럼 보이게 해요.'),
       ('여러 장을 같은 필름으로 한 번에 바꿀 수 있나요?', '네. 사진을 여러 장 고른 뒤 필름을 정하고 ‘모두 저장 (ZIP)’을 누르면 전부 같은 설정으로 바뀌어 ZIP 파일 하나로 받아져요.')],
  rel=REL,
  src='<li>필름 색·입자·비네팅·빛샘은 홍라이프 도구가 직접 만든 보정 값이에요. 특정 필름 제품이나 앱의 색을 그대로 옮긴 것이 아니에요.</li>'
      '<li><a href="https://developer.mozilla.org/ko/docs/Web/API/MediaDevices/getUserMedia" rel="noopener" target="_blank">MDN — MediaDevices.getUserMedia()</a> — 브라우저 카메라 사용 방식</li>')

import re
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'overlay')

def build(p):
    u = G.page(p)
    f = os.path.join(ROOT, u.lstrip('/'))
    s = open(f, encoding='utf-8').read()
    # 이미지 앱은 PDF·OCR·한글 엔진이 필요 없어요
    s = re.sub(r'<script src="/assets/js/(hlpdf|hlocr|hlhwp|hlhwpkit)\.js[^"]*"></script>\n?', '', s)
    open(f, 'w', encoding='utf-8').write(s)
    return u

if __name__ == '__main__':
    for p in (FF,):
        print('wrote', build(p))
