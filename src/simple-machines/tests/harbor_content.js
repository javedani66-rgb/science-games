/* Pure checks of the harbor model data and text layer (no browser).
   - every question has exactly one right arrangement/answer (A2, A15)
   - nothing sits exactly on a limit: force equal to available force, rope equal to the rope supply (A15)
   - model numbers match the spec (load 60, available force 40, light net 30, h 2; the 3-4 red variant without decimals)
   - no Persian text in the code: every string comes from harbor/strings.fa.json by id (B49/B50)
   - every referenced text id exists, every mission has its texts for every band, no em dash, ZWNJ/digit rules
   - the text bank (docs/texts/TEXT_BANK_FA.json) contains each harbor id. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const dir=path.join(__dirname,'..'),root=path.join(dir,'..','..');
const strings=JSON.parse(fs.readFileSync(path.join(dir,'harbor','strings.fa.json'),'utf8'));
const HARBOR_STR=Object.fromEntries(Object.entries(strings).map(([k,v])=>[k,v.text]));
const FA='۰۱۲۳۴۵۶۷۸۹';
const src=fs.readFileSync(path.join(dir,'harbor-content.js'),'utf8'),routesSrc=fs.readFileSync(path.join(dir,'harbor-routes.js'),'utf8');
const ctx=vm.createContext({HARBOR_STR,fa:v=>String(v).replace(/\d/g,d=>FA[d]),pulleyIcon:()=>''});
vm.runInContext(src.slice(0,src.indexOf('function mountHarborActivity(')),ctx);
const C=vm.runInContext('({HARBOR_CONTENT,HARBOR_BANDS,harborSpec,harborSolutions,harborMargins,harborVars,hs,harborHas,harborUnit,harborLen})',ctx);
const bands=Array.from(C.HARBOR_BANDS);
assert.deepEqual(bands,['1-2','3-4','5-6']);

// 1. model data
let missions=0;
for(const r of C.HARBOR_CONTENT.routes)for(const a of r.activities)for(const b of bands){
 const sp=C.harborSpec(a.key,b),tag=`${a.key} ${b}`;missions++;
 for(const m of C.harborMargins(sp))assert.ok(Math.abs(m)>1e-9,tag+': a value sits exactly on a limit');
 const sol=C.harborSolutions(sp).map(x=>Array.from(x));
 if(sp.t==='harborTry')assert.equal(sol.length,0,tag+': the observation mission must not lift');
 else if(sp.t==='harborCoils')assert.equal(sol.length,2,tag+': the coil-viewing mission shows both arrangements lifting');
 else assert.equal(sol.length,1,tag+': exactly one arrangement succeeds, got '+JSON.stringify(sol));
 if(sp.best!=null&&sp.t!=="harborCoils")assert.deepEqual(sol[0],[].concat(sp.best),tag+': declared best arrangement is the only success');
 assert.equal(sp.h,2,tag+': height');
 if(sp.q){assert.ok(sp.q.answer>=0&&sp.q.answer<sp.q.n,tag+': answer index');assert.ok(sp.q.n===2||sp.q.n===3);}
 // allowed arrangements are only 1 or 2 supporting parts (M07 does not teach counting parts, B51)
 for(const n of sp.opts||[1])assert.ok(n===1||n===2);
 // the fixed-versus-movable comparison lives only in the red challenge (D239)
 if(r.id!=='harbor.dragon')assert.deepEqual(Array.from(sp.opts||[1]),[1],tag+': green/orange have no movable pulley');
}
assert.equal(missions,27);
const spec=(k,b)=>C.harborSpec(k,b);
// spec table (sections 3 and 7)
for(const b of bands){
 assert.deepEqual([spec('green.m1',b).W,spec('green.m2',b).W,spec('green.m3',b).W],[30,10,20]);
 assert.deepEqual([spec('orange.m1',b).W,spec('orange.m2',b).W,spec('orange.m3',b).W],[60,60,30]);
 assert.equal(spec('orange.m2',b).helpers,2);
}
for(const b of ['5-6']){
 assert.deepEqual([spec('red.m1',b).W,spec('red.m1',b).ropeMax,spec('red.m2',b).W,spec('red.m2',b).ropeMax,spec('red.m3',b).ropeMax],[30,3,60,5,7]);
 assert.deepEqual(Array.from(spec('red.m3',b).plan),[30,60]);assert.equal(spec('red.m3',b).S,40);
}
assert.deepEqual(Array.from(spec('red.m3','3-4').plan),[40,80]);assert.equal(spec('red.m3','3-4').S,50);   // decimal-free variant of the spec (net 40, cage 80, S 50)
assert.deepEqual([spec('red.m1','1-2').W,spec('red.m1','1-2').ropeMax,spec('red.m2','1-2').t,spec('red.m3','1-2').W,spec('red.m3','1-2').ropeMax],[60,null,'harborCoils',30,3]);
// 3-4 shows only whole squares and steps
for(const r of C.HARBOR_CONTENT.routes)for(const a of r.activities){const sp=spec(a.key,'3-4');for(const v of [sp.W,sp.S,sp.S*(sp.helpers||1)].concat(Array.from(sp.plan||[])))if(v!=null)assert.equal(v%10,0,a.key+': whole squares');}
assert.equal(C.harborUnit('3-4',40),'۴ خانه');assert.equal(C.harborUnit('5-6',40),'۴۰۰ نیوتون');assert.equal(C.harborUnit('1-2',40),'');assert.equal(C.harborLen('5-6',2),'۲ متر');

// 2. text layer
const stripped=f=>f.replace(/\/\*[\s\S]*?\*\//g,'').replace(/"(fishing-dock|pirate-dock|dragon-dock)": "<svg[\s\S]*?<\/svg>"/g,'');
for(const [name,code] of [['harbor-content.js',src],['harbor-routes.js',routesSrc]]){
 const left=stripped(code).match(/[؀-ۿ]+/g);
 assert.equal(left,null,name+' must not contain Persian text; use harbor/strings.fa.json ids: '+left);
}
for(const code of [src,routesSrc])for(const m of code.matchAll(/\bhs\(\s*['"]([^'"]+)['"]\s*[,)]/g))assert.ok(C.harborHas(m[1],'5-6')||Object.keys(HARBOR_STR).some(k=>k.startsWith(m[1]+'.')),'unknown text id in code: '+m[1]);
const need=(id,b)=>assert.ok(C.harborHas(id,b),`missing text ${id} for band ${b}`);
for(const r of C.HARBOR_CONTENT.routes){
 for(const k of ['title','label','desc','story','help'])for(const b of bands)need(`harbor.${r.color}.${k}`,b);
 for(const a of r.activities)for(const b of bands){
  const sp=spec(a.key,b),id='harbor.'+a.key;
  need(id+'.title',b);need(id+'.prompt',b);need(id+'.guess.q',b);need(id+'.guess.opt1',b);need(id+'.guess.opt2',b);
  if(sp.q){need(id+'.seen',b);for(let i=1;i<=sp.q.n;i++)need(`harbor.${r.color}.q.opt${i}`,b);for(const k of ['prompt','explain','retry'])need(`harbor.${r.color}.q.${k}`,b);
   const opts=[];for(let i=1;i<=sp.q.n;i++)opts.push(C.hs(`harbor.${r.color}.q.opt${i}`,b));assert.equal(new Set(opts).size,opts.length,`${a.key} ${b}: options must differ`);}
  else need(id+'.done',b);
  if(sp.t==='harborPick')need(id+'.showed',b);
  if(sp.t==='harborHelpers'){need(id+'.btn.helper',b);need(id+'.helperIn',b);}
  if(sp.t==='harborCoils')need(id+'.other',b);
  if(sp.t==='harborPlan')for(const k of ['plan.first','plan.next','plan.restarted','plan.fail.rope'])need(id+'.'+k,b);
  // guess options of a band must not borrow a third option from another band's wording
  const n12=Object.keys(HARBOR_STR).filter(k=>k.startsWith(id+'.guess.opt')&&k.endsWith('.b12')).length;
  if(b==='1-2'&&n12)assert.ok(n12>=2);
 }
}
for(const k of ['unit.square','unit.newton','unit.step','unit.meter','label.weight','label.need','label.avail.sailor','label.avail.pirate','label.avail.pirates2','label.crate','label.target','label.target.n','label.rope','label.rope.n','counter.rope','counter.rise','tryNow','guessSaved','btn.showMe','btn.restartPlan','fail.force','fail.rope','strip.row','model','tier.core','tier.challenge','tier.very-hard','tier.unknown'])for(const b of bands)need('harbor.ui.'+k,b);
assert.equal(C.hs('harbor.red.title'),'شکار اژدر!','the red card title is the owner\'s and never changes');
// token filling
assert.equal(C.hs('harbor.green.m1.prompt','5-6',C.harborVars(spec('green.m1','5-6'))),'تور پر از ماهی ۳۰۰ نیوتون وزن دارد. ملوان ۴۰۰ نیوتون نیرو دارد. تور را ۲ متر بالا بیاور.');
for(const [id,e] of Object.entries(strings)){
 assert.ok(!/[—–]/.test(e.text),id+': no dash characters in Persian text');
 assert.ok(['draft'].includes(e.status||'draft'),id+': Claude texts are draft only');
 assert.ok(!/\d/.test(e.text.replace(/<[^>]*>/g,'')),id+': Persian digits only');
 assert.ok(!/(^|\s)(می|نمی)(?=[آ-ی])/.test(e.text),id+': می/نمی must be joined with a ZWNJ');
}
// every id is in the text bank
const bank=JSON.parse(fs.readFileSync(path.join(root,'docs','texts','TEXT_BANK_FA.json'),'utf8')).entries;
for(const id of Object.keys(strings))assert.ok(bank[id]&&bank[id].text===strings[id].text,id+': run python3 tools/text_bank.py collect');
console.log(`harbor_content: ${missions} mission-band specs have one answer and no limit ties; no Persian text in code; ${Object.keys(strings).length} texts in the bank`);
