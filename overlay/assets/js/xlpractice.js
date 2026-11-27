/*! 홍라이프 엑셀 연습장 · 안전한 소형 수식 엔진 + 연습 문제 (브라우저·node 공용) */
(function(root){
  "use strict";

  function colToNum(c){ var n=0; for(var i=0;i<c.length;i++) n=n*26+(c.charCodeAt(i)-64); return n; }
  function numToCol(n){ var s=""; while(n>0){ s=String.fromCharCode(65+(n-1)%26)+s; n=Math.floor((n-1)/26);} return s; }
  function parseRef(ref){ var m=/^([A-Z]+)([0-9]+)$/.exec(ref); if(!m) return null; return {c:colToNum(m[1]), r:parseInt(m[2],10), col:m[1]}; }
  function expandRange(a,b){ var A=parseRef(a),B=parseRef(b); if(!A||!B) return []; var out=[];
    var c0=Math.min(A.c,B.c),c1=Math.max(A.c,B.c),r0=Math.min(A.r,B.r),r1=Math.max(A.r,B.r);
    for(var c=c0;c<=c1;c++){ for(var r=r0;r<=r1;r++) out.push(numToCol(c)+r); } return out; }

  function tokenize(s){
    var t=[], i=0, re=/\s*(?:(<=|>=|<>|[+\-*/(),<>=:&])|([A-Za-z]+[0-9]+)|([A-Za-z]+)|([0-9]*\.?[0-9]+)|"([^"]*)")/g, m;
    while(i<s.length){
      re.lastIndex=i; m=re.exec(s);
      if(!m || m.index!==i){ if(/\s/.test(s[i])){ i++; continue; } throw new Error("알 수 없는 문자: "+s[i]); }
      if(m[1]!=null) t.push({t:"op",v:m[1]});
      else if(m[2]!=null) t.push({t:"ref",v:m[2].toUpperCase()});
      else if(m[3]!=null) t.push({t:"fn",v:m[3].toUpperCase()});
      else if(m[4]!=null) t.push({t:"num",v:parseFloat(m[4])});
      else if(m[5]!=null) t.push({t:"str",v:m[5]});
      i=re.lastIndex;
    }
    return t;
  }

  function toNum(x){ if(x&&x.__r) return FUNCS.SUM(x.flat); if(Array.isArray(x)) return FUNCS.SUM(x); return (typeof x==="number")?x:(parseFloat(x)||0); }
  function flatten(x){ if(x&&x.__r) return x.flat.slice(); if(Array.isArray(x)) return x.slice(); return [x]; }
  function matchCrit(v, crit){
    if(typeof crit==="number") return toNum(v)===crit;
    var s=String(crit), m=/^(>=|<=|<>|>|<|=)(.*)$/.exec(s);
    if(m){ var op=m[1], rhs=m[2]; var rn=parseFloat(rhs);
      if(!isNaN(rn) && /^-?[0-9.]+$/.test(rhs)){ var vn=toNum(v);
        switch(op){case">":return vn>rn;case"<":return vn<rn;case">=":return vn>=rn;case"<=":return vn<=rn;case"=":return vn===rn;case"<>":return vn!==rn;} }
      if(op==="=") return String(v)===rhs; if(op==="<>") return String(v)!==rhs;
    }
    return String(v)===s;
  }

  var FUNCS={
    SUM:function(a){return a.reduce(function(x,y){return x+(typeof y==="number"?y:0);},0);},
    AVERAGE:function(a){var n=a.filter(function(y){return typeof y==="number";}); return n.length?n.reduce(function(x,y){return x+y;},0)/n.length:0;},
    MAX:function(a){var n=a.filter(function(y){return typeof y==="number";}); return n.length?Math.max.apply(null,n):0;},
    MIN:function(a){var n=a.filter(function(y){return typeof y==="number";}); return n.length?Math.min.apply(null,n):0;},
    COUNT:function(a){return a.filter(function(y){return typeof y==="number";}).length;},
    COUNTA:function(a){return a.filter(function(y){return y!==""&&y!=null;}).length;},
    ROUND:function(a){var x=toNum(a[0]),n=toNum(a[1]||0),p=Math.pow(10,n); return Math.round(x*p)/p;},
    ROUNDUP:function(a){var x=toNum(a[0]),n=toNum(a[1]||0),p=Math.pow(10,n); return (x<0?-1:1)*Math.ceil(Math.abs(x)*p)/p;},
    ROUNDDOWN:function(a){var x=toNum(a[0]),n=toNum(a[1]||0),p=Math.pow(10,n); return (x<0?-1:1)*Math.floor(Math.abs(x)*p)/p;},
    ABS:function(a){return Math.abs(toNum(a[0]));},
    IF:function(a){return a[0]?a[1]:a[2];},
    COUNTIF:function(a){ var f=flatten(a[0]); var crit=a[1]; return f.filter(function(v){return matchCrit(v,crit);}).length; },
    SUMIF:function(a){ var f=flatten(a[0]); var crit=a[1]; var s=a[2]?flatten(a[2]):f; var t=0;
      for(var i=0;i<f.length;i++){ if(matchCrit(f[i],crit)) t+=(typeof s[i]==="number"?s[i]:(parseFloat(s[i])||0)); } return t; },
    VLOOKUP:function(a){ var key=a[0], rng=a[1], col=toNum(a[2]); if(!rng||!rng.__r) throw new Error("VLOOKUP 두 번째 인자는 표(범위)여야 해요");
      for(var i=0;i<rng.rows.length;i++){ if(String(rng.rows[i][0])===String(key)) return rng.rows[i][col-1]; } return "#N/A"; },
    AVERAGEIF:function(a){ var f=flatten(a[0]); var crit=a[1]; var s=a[2]?flatten(a[2]):f; var sum=0,n=0;
      for(var i=0;i<f.length;i++){ if(matchCrit(f[i],crit)){ var val=(typeof s[i]==="number"?s[i]:parseFloat(s[i])); if(!isNaN(val)){sum+=val;n++;} } } return n?sum/n:0; },
    RANK:function(a){ var num=toNum(a[0]); var arr=flatten(a[1]).filter(function(y){return typeof y==="number";}); var asc=a[2]&&toNum(a[2])!==0; var r=1;
      for(var i=0;i<arr.length;i++){ if(asc?arr[i]<num:arr[i]>num) r++; } return r; },
    IFERROR:function(a){ var v=a[0]; var err=(typeof v==="number"&&!isFinite(v))||(typeof v==="string"&&v.charAt(0)==="#"); return err?a[1]:v; }
  };
  var AGG={SUM:1,AVERAGE:1,MAX:1,MIN:1,COUNT:1,COUNTA:1};

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
    function range2D(a,b){ var A=parseRef(a),B=parseRef(b);
      var c0=Math.min(A.c,B.c),c1=Math.max(A.c,B.c),r0=Math.min(A.r,B.r),r1=Math.max(A.r,B.r);
      var rows=[],flat=[];
      for(var r=r0;r<=r1;r++){ var row=[]; for(var c=c0;c<=c1;c++){ var v=cellVal(numToCol(c)+r); row.push(v); flat.push(v);} rows.push(row);}
      return {__r:true, rows:rows, flat:flat};
    }
    function parse(expr){
      var tk=tokenize(expr), pos=0;
      function peek(){return tk[pos];}
      function next(){return tk[pos++];}
      function eat(v){ var t=next(); if(!t||t.v!==v) throw new Error("'"+v+"' 필요"); }
      function args(){ var out=[]; if(peek()&&peek().v===")"){return out;} out.push(compare()); while(peek()&&peek().v===","){next(); out.push(compare());} return out; }
      function factor(){
        var t=peek(); if(!t) throw new Error("수식이 끝났어요");
        if(t.t==="num"){ next(); return t.v; }
        if(t.t==="str"){ next(); return t.v; }
        if(t.v==="-"){ next(); return -toNum(factor()); }
        if(t.v==="+"){ next(); return factor(); }
        if(t.v==="("){ next(); var e=compare(); eat(")"); return e; }
        if(t.t==="fn"){ var name=t.v; next(); eat("("); var raw=args(); eat(")");
          var fn=FUNCS[name]; if(!fn) throw new Error(name+" 함수는 아직 지원 안 해요");
          var argv = AGG[name] ? raw.reduce(function(acc,x){return acc.concat(flatten(x));},[]) : raw;
          return fn(argv);
        }
        if(t.t==="ref"){ next();
          if(peek()&&peek().v===":"){ next(); var b=next(); if(!b||b.t!=="ref") throw new Error("범위 오류"); return range2D(t.v,b.v); }
          return cellVal(t.v);
        }
        throw new Error("예상치 못한 '"+(t.v)+"'");
      }
      function term(){ var v=factor(); while(peek()&&(peek().v==="*"||peek().v==="/")){ var op=next().v; var r=factor(); v=(op==="*")?toNum(v)*toNum(r):toNum(v)/toNum(r);} return v; }
      function addsub(){ var v=term(); while(peek()&&(peek().v==="+"||peek().v==="-")){ var op=next().v; var r=term(); v=(op==="+")?toNum(v)+toNum(r):toNum(v)-toNum(r);} return v; }
      function cstr(x){ if(typeof x==="number") return (Math.round(x*1e6)/1e6).toString(); if(x&&x.__r) return cstr(FUNCS.SUM(x.flat)); return String(x); }
      function concat(){ var v=addsub(); while(peek()&&peek().v==="&"){ next(); var r=addsub(); v=cstr(v)+cstr(r); } return v; }
      function compare(){ var v=concat(); var t=peek(); if(t&&(t.v==="<"||t.v===">"||t.v==="<="||t.v===">="||t.v==="="||t.v==="<>")){ var op=next().v; var r=concat();
          switch(op){case">":return toNum(v)>toNum(r);case"<":return toNum(v)<toNum(r);case">=":return toNum(v)>=toNum(r);case"<=":return toNum(v)<=toNum(r);case"=":return v==r;case"<>":return v!=r;} }
        return v; }
      var result=compare();
      if(pos<tk.length) throw new Error("수식을 다 읽지 못했어요");
      if(result&&result.__r) return FUNCS.SUM(result.flat);
      if(Array.isArray(result)) return FUNCS.SUM(result);
      return result;
    }
    var f=String(formula).trim(); if(f[0]==="=") f=f.slice(1); return parse(f);
  }

  function sameResult(a,b){ if(typeof a==="number"&&typeof b==="number") return Math.abs(a-b)<1e-6; return String(a)===String(b); }

  var LESSONS=[
    {id:"sum",title:"합계 — SUM",grid:{A1:10,A2:20,A3:30,A4:40,A5:50},rows:6,target:"B1",expect:150,
     instruct:"B1 칸을 누르고 <b>=SUM(A1:A5)</b> 를 입력한 뒤 <b>Enter</b>를 눌러 보세요. 다섯 숫자의 합계가 나와요.",hint:"= 를 먼저 치고, SUM( 뒤에 A1:A5 처럼 범위를 넣어요."},
    {id:"avg",title:"평균 — AVERAGE",grid:{A1:80,A2:90,A3:100,A4:70},rows:5,target:"B1",expect:85,
     instruct:"B1 칸에 <b>=AVERAGE(A1:A4)</b> 를 입력해 네 점수의 평균을 구하세요.",hint:"평균은 AVERAGE 함수예요. 범위는 A1:A4."},
    {id:"max",title:"최댓값 — MAX",grid:{A1:15,A2:42,A3:8,A4:33,A5:27},rows:6,target:"B1",expect:42,
     instruct:"B1 칸에 <b>=MAX(A1:A5)</b> 를 입력해 가장 큰 값을 찾으세요.",hint:"가장 큰 값은 MAX, 가장 작은 값은 MIN 이에요."},
    {id:"mul",title:"곱하기 — 단가 × 수량",grid:{A1:"단가",B1:"수량",A2:1200,B2:3},rows:4,target:"C2",expect:3600,
     instruct:"C2 칸에 <b>=A2*B2</b> 를 입력해 금액(단가×수량)을 구하세요.",hint:"곱하기는 * 기호예요. =A2*B2 처럼 셀 주소를 곱해요."},
    {id:"if",title:"조건 — IF (합격/불합격)",grid:{A1:"점수",A2:75},rows:4,target:"B2",expect:"합격",
     instruct:"B2 칸에 <b>=IF(A2>=60,\"합격\",\"불합격\")</b> 를 입력하세요. 60점 이상이면 합격이 나와요.",hint:"IF(조건, 참일때, 거짓일때) 순서예요. 글자는 \"따옴표\" 안에 넣어요."},
    {id:"round",title:"반올림 — ROUND",grid:{A1:3.14159},rows:3,target:"B1",expect:3.14,
     instruct:"B1 칸에 <b>=ROUND(A1,2)</b> 를 입력해 소수점 둘째 자리까지 반올림하세요.",hint:"ROUND(값, 자릿수) 예요. 2는 소수점 둘째 자리까지."},
    {id:"countif",title:"조건 개수 — COUNTIF",grid:{A1:"사과",A2:"배",A3:"사과",A4:"포도",A5:"사과"},rows:6,target:"C1",expect:3,
     instruct:"C1 칸에 <b>=COUNTIF(A1:A5,\"사과\")</b> 를 입력해 ‘사과’가 몇 개인지 세어 보세요.",hint:"COUNTIF(범위, 조건) 이에요. 조건 글자는 \"따옴표\" 안에."},
    {id:"sumif",title:"조건 합계 — SUMIF",grid:{A1:"식비",B1:10000,A2:"교통",B2:5000,A3:"식비",B3:8000,A4:"교통",B4:3000},rows:5,target:"D1",expect:18000,
     instruct:"D1 칸에 <b>=SUMIF(A1:A4,\"식비\",B1:B4)</b> 를 입력해 ‘식비’ 금액만 더해 보세요.",hint:"SUMIF(조건범위, 조건, 더할범위) 순서예요."},
    {id:"vlookup",title:"표에서 찾기 — VLOOKUP",grid:{A1:"A01",B1:"사과",A2:"A02",B2:"배",A3:"A03",B3:"포도",C1:"찾을 코드",D1:"A02"},rows:4,target:"E1",expect:"배",
     instruct:"E1 칸에 <b>=VLOOKUP(D1,A1:B3,2,0)</b> 를 입력해 코드 ‘A02’의 이름을 찾으세요.",hint:"VLOOKUP(찾을값, 표범위, 가져올열번호, 0) 이에요. 0은 정확히 일치."},
    {id:"min",title:"최솟값 — MIN",grid:{A1:15,A2:42,A3:8,A4:33,A5:27},rows:6,target:"B1",expect:8,
     instruct:"B1 칸에 <b>=MIN(A1:A5)</b> 를 입력해 가장 작은 값을 찾으세요.",hint:"가장 작은 값은 MIN 이에요."},
    {id:"sub",title:"빼기 — 수입 − 지출",grid:{A1:"수입",B1:"지출",A2:50000,B2:32000},rows:4,target:"C2",expect:18000,
     instruct:"C2 칸에 <b>=A2-B2</b> 를 입력해 남은 돈(수입−지출)을 구하세요.",hint:"빼기는 - 기호예요. =A2-B2."},
    {id:"count",title:"숫자 개수 — COUNT",grid:{A1:10,A2:20,A3:"없음",A4:40,A5:50},rows:6,target:"B1",expect:4,
     instruct:"B1 칸에 <b>=COUNT(A1:A5)</b> 를 입력하세요. 글자(‘없음’)는 빼고 숫자만 세요.",hint:"COUNT는 숫자가 든 칸만 세요. 글자는 빼요."},
    {id:"range",title:"범위 폭 — MAX−MIN",grid:{A1:15,A2:42,A3:8,A4:33,A5:27},rows:6,target:"B1",expect:34,
     instruct:"B1 칸에 <b>=MAX(A1:A5)-MIN(A1:A5)</b> 를 입력해 가장 큰 값과 작은 값의 차이를 구하세요.",hint:"함수끼리도 빼기(-)로 이을 수 있어요."},
    {id:"countif2",title:"합격자 수 — COUNTIF 조건",grid:{A1:55,A2:80,A3:40,A4:90,A5:70},rows:6,target:"B1",expect:3,
     instruct:"B1 칸에 <b>=COUNTIF(A1:A5,\">=60\")</b> 를 입력해 60점 이상이 몇 명인지 세요.",hint:"조건에 부등호를 쓸 땐 \">=60\" 처럼 따옴표 안에 넣어요."},
    {id:"concat",title:"문자 합치기 — &",grid:{A1:"홍길",B1:"동"},rows:3,target:"C1",expect:"홍길동",
     instruct:"C1 칸에 <b>=A1&B1</b> 를 입력해 두 글자를 하나로 합치세요.",hint:"& 기호는 글자를 이어 붙여요. =A1&B1."},
    {id:"roundup",title:"올림 — ROUNDUP",grid:{A1:2.1},rows:3,target:"B1",expect:3,
     instruct:"B1 칸에 <b>=ROUNDUP(A1,0)</b> 를 입력해 올림하세요. 2.1이 3이 돼요.",hint:"ROUNDUP은 무조건 올려요. 0은 정수 자리까지."},
    {id:"nestedif",title:"중첩 IF — 학점 매기기",grid:{A1:"점수",A2:85},rows:4,target:"B2",expect:"B",
     instruct:"B2 칸에 <b>=IF(A2>=90,\"A\",IF(A2>=80,\"B\",\"C\"))</b> 를 입력하세요. 90↑은 A, 80↑은 B, 나머지는 C.",hint:"IF 안에 IF를 또 넣어요. 85점이면 B가 나와요."},
    {id:"averageif",title:"조건 평균 — AVERAGEIF",grid:{A1:"국어",B1:80,A2:"수학",B2:90,A3:"국어",B3:70},rows:5,target:"C1",expect:75,
     instruct:"C1 칸에 <b>=AVERAGEIF(A1:A3,\"국어\",B1:B3)</b> 를 입력해 국어 점수만 평균 내세요.",hint:"AVERAGEIF(조건범위, 조건, 평균낼범위) 순서예요. (80+70)÷2=75."},
    {id:"percent",title:"백분율 — 달성률(%)",grid:{A1:"실적",B1:"목표",A2:80,B2:100},rows:4,target:"C2",expect:80,
     instruct:"C2 칸에 <b>=ROUND(A2/B2*100,0)</b> 를 입력해 달성률(%)을 구하세요.",hint:"실적÷목표×100 이에요. 80/100×100=80."},
    {id:"abs",title:"절댓값 — 차이 ABS",grid:{A1:30,A2:50},rows:3,target:"B1",expect:20,
     instruct:"B1 칸에 <b>=ABS(A1-A2)</b> 를 입력해 두 값의 차이(부호 없이)를 구하세요.",hint:"ABS는 음수도 양수로 만들어요. 30−50=−20 → 20."},
    {id:"rank",title:"순위 — RANK",grid:{A1:70,A2:90,A3:85,A4:60,A5:100},rows:6,target:"B2",expect:2,
     instruct:"B2 칸에 <b>=RANK(A2,A1:A5)</b> 를 입력해 90점(A2)이 몇 등인지 구하세요.",hint:"RANK(값, 전체범위) 예요. 100 다음이라 2등."},
    {id:"iferror",title:"오류 처리 — IFERROR",grid:{A1:10,B1:0},rows:3,target:"C1",expect:"오류",
     instruct:"C1 칸에 <b>=IFERROR(A1/B1,\"오류\")</b> 를 입력하세요. 0으로 나눠 오류가 나면 ‘오류’로 보여줘요.",hint:"IFERROR(계산, 오류일때값) 이에요. 10/0은 오류라서 ‘오류’가 나와요."}
  ];

  var api={evaluate:evaluate, sameResult:sameResult, expandRange:expandRange, LESSONS:LESSONS, parseRef:parseRef};
  if(typeof module!=="undefined"&&module.exports) module.exports=api; else root.XLP=api;
})(typeof window!=="undefined"?window:globalThis);
