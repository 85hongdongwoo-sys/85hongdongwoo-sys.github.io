// node build/pwa/make_icons.js  → overlay/assets/app/<key>-{180,192,512,m512}.png
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const R=path.join(__dirname,'..','..');
const apps=JSON.parse(require('child_process').execSync(`python3 -c "import sys,json;sys.path.insert(0,'${__dirname}');from apps import APPS,key;print(json.dumps([[key(p),e,bg] for p,n,e,bg in APPS]))"`).toString());
const logo='data:image/svg+xml;base64,'+fs.readFileSync(path.join(R,'..','..','..','tmp/claude-0/br/assets/brand/symbol-small.svg')).toString('base64');
function html(e,bg,mask){const em=mask?44:56, b=mask?13:19, bx=mask?57:74;
return `<html><body style="margin:0"><div style="width:512px;height:512px;position:relative;background:linear-gradient(160deg,#fff 0%,${bg} 100%);overflow:hidden">
<div style="position:absolute;left:0;right:0;top:${mask?47:45}%;transform:translateY(-50%);text-align:center;font-size:${em*5.12}px;line-height:1;font-family:'Noto Color Emoji','Apple Color Emoji',sans-serif">${e}</div>
<img src="${logo}" style="position:absolute;left:${bx}%;top:${bx}%;width:${b}%;height:${b}%;border-radius:22%;box-shadow:0 0 0 6px #fff"></div></body></html>`}
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:512,height:512}});
for(const [k,e,bg] of apps){for(const mask of [0,1]){await p.setContent(html(e,bg,mask));await p.waitForTimeout(60);
 const buf=await p.screenshot({type:'png'});const out=path.join(R,'overlay/assets/app',k+(mask?'-m512':'-512')+'.png');fs.writeFileSync(out,buf);}}
await b.close();console.log('icons',apps.length);})();
