/*! 홍라이프 캐릭터 메이커 · 부품 조합 드로잉 (브라우저·node 공용) · 100% 오리지널 */
(function(root){
  "use strict";
  var ANIMALS = {
    cat:   {name:"고양이", ear:"triangle", nose:"small", whisker:true,  body:"#F7C98B", feat:"#D98A3C"},
    bunny: {name:"토끼",   ear:"long",     nose:"small", whisker:false, body:"#F6DCE4", feat:"#E79BB4"},
    bear:  {name:"곰",     ear:"round",    nose:"snout", whisker:false, body:"#C9A27A", feat:"#8A5A34"},
    dog:   {name:"강아지", ear:"floppy",   nose:"snout", whisker:false, body:"#EAD9C2", feat:"#9A6B3F"},
    fox:   {name:"여우",   ear:"pointy",   nose:"snout", whisker:true,  body:"#F4A15E", feat:"#C85A28"},
    pig:   {name:"돼지",   ear:"round",    nose:"pig",   whisker:false, body:"#F7C2CE", feat:"#E07A94"},
    panda: {name:"판다",   ear:"blackround",nose:"snout",whisker:false, body:"#FFFFFF", feat:"#2B2B2B"},
    frog:  {name:"개구리", ear:"none",     nose:"dots",  whisker:false, body:"#A7D98B", feat:"#5F9B45", eyesTop:true, wideMouth:true},
    chick: {name:"병아리", ear:"tuft",     nose:"beak",  whisker:false, body:"#FBE28A", feat:"#E9A52C"},
    sheep: {name:"양",     ear:"small",    nose:"small", whisker:false, body:"#F3F1EC", feat:"#B8B2A6", fluffy:true}
  };
  var ANIMAL_KEYS = Object.keys(ANIMALS);
  var EYES=["dot","shine","happy","sparkle"], MOUTHS=["smile","cat","o","wave"], ACCS=["none","bow","flower","star","heart","hat"];

  function mk(list, rng){ return list[Math.floor((rng?rng():Math.random())*list.length)]; }
  function randomParts(rng){
    return { animal: mk(ANIMAL_KEYS,rng), eye: mk(EYES,rng), mouth: mk(MOUTHS,rng), acc: mk(ACCS,rng) };
  }

  function draw(ctx, cx, cy, r, parts, opts){
    opts = opts || {};
    var colored = !!opts.color;
    var A = ANIMALS[parts.animal] || ANIMALS.cat;
    var LW = Math.max(3, r*0.05);
    ctx.lineJoin="round"; ctx.lineCap="round";
    ctx.strokeStyle="#1b1b1b"; ctx.lineWidth=LW;
    var bodyFill = colored ? A.body : "#ffffff";
    var featFill = colored ? A.feat : "#ffffff";

    function circle(x,y,rr,fill){ ctx.beginPath(); ctx.arc(x,y,rr,0,Math.PI*2); if(fill){ctx.fillStyle=fill;ctx.fill();} ctx.stroke(); }
    function ellipse(x,y,rx,ry,fill,rot){ ctx.beginPath(); ctx.ellipse(x,y,rx,ry,rot||0,0,Math.PI*2); if(fill){ctx.fillStyle=fill;ctx.fill();} ctx.stroke(); }
    function tri(ax,ay,bx,by,dx,dy,fill){ ctx.beginPath(); ctx.moveTo(ax,ay); ctx.lineTo(bx,by); ctx.lineTo(dx,dy); ctx.closePath(); if(fill){ctx.fillStyle=fill;ctx.fill();} ctx.stroke(); }
    function arc(x,y,rr,a0,a1){ ctx.beginPath(); ctx.arc(x,y,rr,a0,a1); ctx.stroke(); }

    // limbs (behind)
    for(var s=-1;s<=1;s+=2){ ellipse(cx+s*r*0.96, cy+r*0.12, r*0.16, r*0.22, bodyFill); }
    for(var s2=-1;s2<=1;s2+=2){ ellipse(cx+s2*r*0.42, cy+r*1.02, r*0.24, r*0.15, bodyFill); }

    // ears (behind head, drawn then head covers base)
    var ey = cy - r*0.78;
    function earsDraw(){
      switch(A.ear){
        case "triangle": for(var s=-1;s<=1;s+=2){ var bx=cx+s*r*0.55; tri(bx-r*0.2, ey+r*0.3, bx, ey-r*0.35, bx+r*0.2, ey+r*0.3, bodyFill);} break;
        case "long": for(var s=-1;s<=1;s+=2){ ctx.save(); ctx.translate(cx+s*r*0.34, cy-r*0.6); ctx.rotate(s*0.18); ellipse(0,-r*0.5,r*0.14,r*0.52, bodyFill); ctx.restore(); } break;
        case "round": for(var s=-1;s<=1;s+=2){ circle(cx+s*r*0.62, cy-r*0.62, r*0.26, bodyFill);} break;
        case "blackround": for(var s=-1;s<=1;s+=2){ circle(cx+s*r*0.64, cy-r*0.64, r*0.26, featFill);} break;
        case "floppy": for(var s=-1;s<=1;s+=2){ ellipse(cx+s*r*0.78, cy-r*0.25, r*0.17, r*0.34, bodyFill, s*0.5);} break;
        case "pointy": for(var s=-1;s<=1;s+=2){ var bx=cx+s*r*0.58; tri(bx-r*0.16, ey+r*0.3, bx+s*r*0.05, ey-r*0.45, bx+r*0.18, ey+r*0.3, bodyFill);} break;
        case "small": for(var s=-1;s<=1;s+=2){ ellipse(cx+s*r*0.58, cy-r*0.5, r*0.1, r*0.14, bodyFill);} break;
        case "tuft": ctx.beginPath(); ctx.moveTo(cx-r*0.06, cy-r*0.9); ctx.quadraticCurveTo(cx, cy-r*1.2, cx+r*0.06, cy-r*0.9); ctx.stroke(); break;
      }
    }
    earsDraw();

    // sheep fluffy halo
    if(A.fluffy){ for(var i=0;i<10;i++){ var a=i/10*Math.PI*2; circle(cx+Math.cos(a)*r*0.95, cy+Math.sin(a)*r*0.95, r*0.2, bodyFill);} }

    // head
    circle(cx, cy, r, bodyFill);

    // panda eye patches
    if(parts.animal==="panda"){ for(var s=-1;s<=1;s+=2){ ellipse(cx+s*r*0.34, cy-r*0.02, r*0.2, r*0.26, featFill, s*0.3);} }

    // accessory (top)
    (function(){ var ox,oy;
      if(parts.acc==="bow"){ ox=cx+r*0.6; oy=cy-r*0.72; for(var s=-1;s<=1;s+=2){ tri(ox,oy, ox+s*r*0.22,oy-r*0.13, ox+s*r*0.22,oy+r*0.13, featFill);} circle(ox,oy,r*0.07, featFill); }
      else if(parts.acc==="flower"){ ox=cx-r*0.62; oy=cy-r*0.7; for(var i=0;i<5;i++){ var a=i/5*Math.PI*2; circle(ox+Math.cos(a)*r*0.12, oy+Math.sin(a)*r*0.12, r*0.09, colored?"#F7B5C4":"#fff");} ctx.fillStyle=colored?"#E9A52C":"#1b1b1b"; circle(ox,oy,r*0.05,colored?"#F6D97A":"#fff"); }
      else if(parts.acc==="star"){ ox=cx+r*0.62; oy=cy-r*0.78; star(ox,oy,r*0.16,colored?"#F6D97A":"#fff"); }
      else if(parts.acc==="heart"){ ox=cx+r*0.6; oy=cy-r*0.74; heart(ox,oy,r*0.16,colored?"#F2889E":"#fff"); }
      else if(parts.acc==="hat"){ ctx.fillStyle=colored?"#7FA8D6":"#fff"; ctx.beginPath(); ctx.ellipse(cx,cy-r*0.86,r*0.42,r*0.1,0,0,Math.PI*2); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.rect(cx-r*0.24,cy-r*1.2,r*0.48,r*0.36); ctx.fill(); ctx.stroke(); }
    })();
    function star(ox,oy,rr,fill){ ctx.beginPath(); for(var i=0;i<10;i++){ var a=-Math.PI/2+i*Math.PI/5; var R=i%2?rr*0.45:rr; var fn=i?'lineTo':'moveTo'; ctx[fn](ox+Math.cos(a)*R, oy+Math.sin(a)*R);} ctx.closePath(); ctx.fillStyle=fill; ctx.fill(); ctx.stroke(); }
    function heart(ox,oy,rr,fill){ ctx.beginPath(); ctx.moveTo(ox,oy+rr*0.6); ctx.bezierCurveTo(ox-rr*1.3,oy-rr*0.5, ox-rr*0.4,oy-rr*1.1, ox,oy-rr*0.35); ctx.bezierCurveTo(ox+rr*0.4,oy-rr*1.1, ox+rr*1.3,oy-rr*0.5, ox,oy+rr*0.6); ctx.closePath(); ctx.fillStyle=fill; ctx.fill(); ctx.stroke(); }

    // eyes
    var eyY = (A.eyesTop? cy-r*0.45 : cy-r*0.05), sp=r*0.3;
    for(var s3=-1;s3<=1;s3+=2){ var ex=cx+s3*sp;
      if(A.eyesTop){ circle(ex, eyY, r*0.2, "#fff"); ctx.fillStyle="#1b1b1b"; circle(ex, eyY, r*0.09, "#1b1b1b"); }
      else if(parts.eye==="dot"){ ctx.fillStyle="#1b1b1b"; circle(ex,eyY,r*0.07,"#1b1b1b"); }
      else if(parts.eye==="shine"){ ctx.fillStyle="#1b1b1b"; circle(ex,eyY,r*0.1,"#1b1b1b"); ctx.fillStyle="#fff"; ctx.beginPath(); ctx.arc(ex+r*0.035,eyY-r*0.035,r*0.03,0,7); ctx.fill(); }
      else if(parts.eye==="happy"){ arc(ex,eyY+r*0.04,r*0.11, Math.PI*1.15, Math.PI*1.85); }
      else if(parts.eye==="sparkle"){ star(ex,eyY,r*0.1,"#1b1b1b"); }
    }

    // cheeks
    for(var s4=-1;s4<=1;s4+=2){ ctx.strokeStyle=colored?"#EF9BB0":"#c98"; ellipse(cx+s4*r*0.62, cy+r*0.12, r*0.1, r*0.06, colored?"#F7C3D2":null); }
    ctx.strokeStyle="#1b1b1b";

    // nose / snout / beak
    var ny=cy+r*0.18;
    if(A.nose==="snout"){ ellipse(cx,ny+r*0.06,r*0.26,r*0.18, colored?"#F3E7D8":"#fff"); ctx.fillStyle="#1b1b1b"; ellipse(cx,ny-r*0.02,r*0.08,r*0.06,"#1b1b1b"); }
    else if(A.nose==="pig"){ ellipse(cx,ny+r*0.04,r*0.2,r*0.14, colored?"#F0A7B8":"#fff"); ctx.fillStyle="#1b1b1b"; for(var s5=-1;s5<=1;s5+=2){ ellipse(cx+s5*r*0.07,ny+r*0.04,r*0.03,r*0.05,"#1b1b1b"); } }
    else if(A.nose==="beak"){ tri(cx-r*0.1,ny, cx+r*0.1,ny, cx,ny+r*0.16, colored?"#E9A52C":"#fff"); }
    else if(A.nose==="small"){ ctx.fillStyle="#1b1b1b"; tri(cx-r*0.05,ny-r*0.02, cx+r*0.05,ny-r*0.02, cx,ny+r*0.05, "#1b1b1b"); }
    // frog nose = dots (skip)

    // mouth
    var my=cy+r*0.4;
    if(A.wideMouth){ arc(cx,my-r*0.15,r*0.4, Math.PI*0.15, Math.PI*0.85); }
    else if(A.nose==="snout"||A.nose==="pig"){ ctx.beginPath(); ctx.moveTo(cx,ny+r*0.1); ctx.lineTo(cx,my-r*0.02); ctx.moveTo(cx-r*0.12,my); ctx.quadraticCurveTo(cx,my+r*0.08,cx,my); ctx.moveTo(cx+r*0.12,my); ctx.quadraticCurveTo(cx,my+r*0.08,cx,my); ctx.stroke(); }
    else if(parts.mouth==="smile"){ arc(cx,my-r*0.16,r*0.22, Math.PI*0.2, Math.PI*0.8); }
    else if(parts.mouth==="cat"){ arc(cx-r*0.1,my-r*0.1,r*0.12,Math.PI*0.15,Math.PI*0.85); arc(cx+r*0.1,my-r*0.1,r*0.12,Math.PI*0.15,Math.PI*0.85); }
    else if(parts.mouth==="o"){ ellipse(cx,my-r*0.04,r*0.07,r*0.1, colored?"#E07A94":"#fff"); }
    else if(parts.mouth==="wave"){ ctx.beginPath(); ctx.moveTo(cx-r*0.16,my-r*0.04); ctx.quadraticCurveTo(cx-r*0.05,my-r*0.14,cx,my-r*0.04); ctx.quadraticCurveTo(cx+r*0.05,my+r*0.06,cx+r*0.16,my-r*0.04); ctx.stroke(); }

    // whiskers
    if(A.whisker){ for(var s6=-1;s6<=1;s6+=2){ for(var k=-1;k<=1;k++){ ctx.beginPath(); ctx.moveTo(cx+s6*r*0.28, ny+k*r*0.06); ctx.lineTo(cx+s6*r*0.66, ny+k*r*0.12); ctx.stroke(); } } }
  }

  var api = { ANIMALS:ANIMALS, ANIMAL_KEYS:ANIMAL_KEYS, EYES:EYES, MOUTHS:MOUTHS, ACCS:ACCS, randomParts:randomParts, draw:draw };
  if(typeof module!=="undefined"&&module.exports) module.exports=api; else root.CHAR=api;
})(typeof window!=="undefined"?window:globalThis);
