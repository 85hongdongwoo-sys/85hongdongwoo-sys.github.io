/*! 홍라이프 엑셀 연습장 · 안전한 소형 수식 엔진 + 연습 문제 (브라우저·node 공용) */
(function(root){
  "use strict";

  // ---- 셀 주소 ----
  function colToNum(c){ var n=0; for(var i=0;i<c.length;i++) n=n*26+(c.charCodeAt(i)-64); return n; }
  function parseRef(ref){ var m=/^([A-Z]+)([0-9]+)$/.exec(ref); if(!m) return null; return {c:colToNum(m[1]), r:parseInt(m[2],10), col:m[1]}; }
  function expandRange(a,b){ var A=parseRef(a),B=parseRef(b); if(!A||!B) return []; var out=[];
    var c0=Math.min(A.c,B.c),c1=Math.max(A.c,B.c),r0=Math.min(A.r,B.r),r1=Math.max(A.r,B.r);
    for(var c=c0;c<=c1;c++){ var cl=""; var cc=c; while(cc>0){ cl=String.fromCharCode(65+(cc-1)%26)+cl; cc=Math.floor((cc-1)/26);} for(var r=r0;r<=r1;r++) out.push(cl+r); }
    return out; }

  // ---- 토크나이저 ----
  function tokenize(s){
    var t=[], i=0, re=/\s*(?:(<=|>=|<>|[+\-*/(),<>=:])|([A-Za-z]+[0-9]+)|([A-Za-z]+)|([0-9]*\.?[0-9]+)|"([^"]*)")/g, m;
    re.lastIndex=0;
    while(i<s.length){
      re.lastIndex=i; m=re.exec(s);
      if(!m || m.index!==i){ // skip whitespace
        if(/\s/.test(s[i])){ i++; continue; }
        throw new Error("알 수 없는 문자: "+s[i]);
      }
      if(m[1]!=null) t.push({t:"op",v:m[1]});
      else if(m[2]!=null) t.push({t:"ref",v:m[2].toUpperCase()});
      else if(m[3]!=null) t.push({t:"fn",v:m[3].toUpperCase()});
      else if(m[4]!=null) t.push({t:"num",v:parseFloat(m[4])});
      else if(m[5]!=null) t.push({t:"str",v:m[5]});
      i=re.lastIndex;
    }
    return t;
  }

  var FUNCS={
    SUM:function(a){return a.reduce(function(x,y){return x+(typeof y==="number"?y:0);},0);},
    AVERAGE:function(a){var n=a.filter(function(y){return typeof y==="number";}); return n.length?n.reduce(function(x,y){return x+y;},0)/n.length:0;},
    MAX:function(a){var n=a.filter(function(y){return typeof y==="number";}); return n.length?Math.max.apply(null,n):0;},
    MIN:function(a){var n=a.filter(function(y){return typeof y==="number";}); return n.length?Math.min.apply(null,n):0;},
    COUNT:function(a){return a.filter(function(y){return typeof y==="number";}).length;},
    COUNTA:function(a){return a.filter(function(y){return y!==""&&y!=null;}).length;},
    ROUND:function(a){var x=a[0]||0,n=a[1]||0,p=Math.pow(10,n); return Math.round(x*p)/p;},
    ABS:function(a){return Math.abs(a[0]||0);},
    IF:function(a){return a[0]?a[1]:a[2];}
  };

  // getVal(ref) → number|string ; 재귀 평가 지원
  function evaluate(formula, getRaw){
    var seen={};
    function cellVal(ref){
      var raw=getRaw(ref);
      if(raw==null||raw==="") return "";
      if(typeof raw==="number") return raw;
      var str=String(raw).trim();
      if(str[0]==="="){ if(seen[ref]) throw new Error("순환 참조"); seen[ref]=1; var v=parse(str.slice(1)); delete seen[ref]; return v; }
      var num=parseFloat(str.replace(/,/g,""));
      return (str!==""&&!isNaN(num)&&/^-?[0-9.,]+$/.test(str))?num:str;
    }
    function parse(expr){
      var tk=tokenize(expr), pos=0;
      function peek(){return tk[pos];}
      function next(){return tk[pos++];}
      function eat(v){ var t=next(); if(!t||t.v!==v) throw new Error("'"+v+"' 필요"); }
      function args(){ var out=[]; if(peek()&&peek().v===")"){return out;} out.push(compare()); while(peek()&&peek().v===","){next(); out.push(compare());} return out; }
      function flattenRange(){ /* handled in factor via ref:ref */ }
      function factor(){
        var t=peek();
        if(!t) throw new Error("수식이 끝났어요");
        if(t.t==="num"){ next(); return t.v; }
        if(t.t==="str"){ next(); return t.v; }
        if(t.v==="-"){ next(); return -factor(); }
        if(t.v==="+"){ next(); return factor(); }
        if(t.v==="("){ next(); var e=compare(); eat(")"); return e; }
        if(t.t==="fn"){ var name=t.v; next(); eat("(");
          var raw=args(); eat(")");
          var fn=FUNCS[name]; if(!fn) throw new Error(name+" 함수는 아직 지원 안 해요");
          var AGG={SUM:1,AVERAGE:1,MAX:1,MIN:1,COUNT:1,COUNTA:1};
          var argv = AGG[name] ? raw.reduce(function(acc,x){return acc.concat(Array.isArray(x)?x:[x]);},[]) : raw;
          return fn(argv);
        }
        if(t.t==="ref"){ next();
          if(peek()&&peek().v===":"){ next(); var b=next(); if(!b||b.t!=="ref") throw new Error("범위 오류");
            return expandRange(t.v,b.v).map(cellVal); // 배열 반환(함수 인자용)
          }
          return cellVal(t.v);
        }
        throw new Error("예상치 못한 '"+(t.v)+"'");
      }
      function term(){ var v=factor(); while(peek()&&(peek().v==="*"||peek().v==="/")){ var op=next().v; var r=factor(); v=(op==="*")?num(v)*num(r):num(v)/num(r);} return v; }
      function addsub(){ var v=term(); while(peek()&&(peek().v==="+"||peek().v==="-")){ var op=next().v; var r=term(); v=(op==="+")?num(v)+num(r):num(v)-num(r);} return v; }
      function compare(){ var v=addsub(); var t=peek(); if(t&&(t.v==="<"||t.v===">"||t.v==="<="||t.v===">="||t.v==="="||t.v==="<>")){ var op=next().v; var r=addsub();
          switch(op){case">":return num(v)>num(r);case"<":return num(v)<num(r);case">=":return num(v)>=num(r);case"<=":return num(v)<=num(r);case"=":return v==r;case"<>":return v!=r;} }
        return v; }
      function num(x){ if(Array.isArray(x)) return FUNCS.SUM(x); return (typeof x==="number")?x:(parseFloat(x)||0); }
      var result=compare();
      if(pos<tk.length) throw new Error("수식을 다 읽지 못했어요");
      if(Array.isArray(result)) return FUNCS.SUM(result);
      return result;
    }
    var f=String(formula).trim();
    if(f[0]==="=") f=f.slice(1);
    return parse(f);
  }

  // 결과 비교(숫자 반올림 허용)
  function sameResult(a,b){
    if(typeof a==="number"&&typeof b==="number") return Math.abs(a-b)<1e-6;
    return String(a)===String(b);
  }

  var LESSONS=[
    {id:"sum",title:"합계 — SUM",
     grid:{A1:10,A2:20,A3:30,A4:40,A5:50},rows:6,
     target:"B1",expect:150,
     instruct:"B1 칸을 누르고 <b>=SUM(A1:A5)</b> 를 입력한 뒤 <b>Enter</b>를 눌러 보세요. 다섯 숫자의 합계가 나와요.",
     hint:"= 를 먼저 치고, SUM( 을 쓴 뒤 A1:A5 처럼 범위를 넣어요."},
    {id:"avg",title:"평균 — AVERAGE",
     grid:{A1:80,A2:90,A3:100,A4:70},rows:5,
     target:"B1",expect:85,
     instruct:"B1 칸에 <b>=AVERAGE(A1:A4)</b> 를 입력해 네 점수의 평균을 구하세요.",
     hint:"평균은 AVERAGE 함수예요. 범위는 A1:A4."},
    {id:"max",title:"최댓값 — MAX",
     grid:{A1:15,A2:42,A3:8,A4:33,A5:27},rows:6,
     target:"B1",expect:42,
     instruct:"B1 칸에 <b>=MAX(A1:A5)</b> 를 입력해 가장 큰 값을 찾으세요.",
     hint:"가장 큰 값은 MAX, 가장 작은 값은 MIN 이에요."},
    {id:"mul",title:"곱하기 — 단가 × 수량",
     grid:{A1:"단가",B1:"수량",A2:1200,B2:3},rows:4,
     target:"C2",expect:3600,
     instruct:"C2 칸에 <b>=A2*B2</b> 를 입력해 금액(단가×수량)을 구하세요.",
     hint:"곱하기는 * 기호예요. =A2*B2 처럼 셀 주소를 곱해요."},
    {id:"if",title:"조건 — IF (합격/불합격)",
     grid:{A1:"점수",A2:75},rows:4,
     target:"B2",expect:"합격",
     instruct:"B2 칸에 <b>=IF(A2>=60,\"합격\",\"불합격\")</b> 를 입력하세요. 60점 이상이면 합격이 나와요.",
     hint:"IF(조건, 참일때, 거짓일때) 순서예요. 글자는 \"따옴표\" 안에 넣어요."},
    {id:"round",title:"반올림 — ROUND",
     grid:{A1:3.14159},rows:3,
     target:"B1",expect:3.14,
     instruct:"B1 칸에 <b>=ROUND(A1,2)</b> 를 입력해 소수점 둘째 자리까지 반올림하세요.",
     hint:"ROUND(값, 자릿수) 예요. 2는 소수점 둘째 자리까지라는 뜻."}
  ];

  var api={evaluate:evaluate, sameResult:sameResult, expandRange:expandRange, LESSONS:LESSONS, parseRef:parseRef};
  if(typeof module!=="undefined"&&module.exports) module.exports=api; else root.XLP=api;
})(typeof window!=="undefined"?window:globalThis);
