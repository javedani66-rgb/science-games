/* Replay/persistence contract: execute real level controller with a tiny UI adapter. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const dir=path.join(__dirname,'..'),app=fs.readFileSync(path.join(dir,'app.js'),'utf8');
const levelSource=app.slice(app.indexOf('function playLevel('),app.indexOf('function playEndless('));
function session(points){
  const original=[{cid:'first',n:7},{cid:'second',n:11}],mounted=[],snapshots=[],saved=[],stars=[],elements={};
  let board,lastHead,buttons=[],finished;
  const S={track:'c',cb:{'c:first':1},ls:{'c:pulley.2':2}};
  const ctx=vm.createContext({S,window:{__JT:1,scrollTo(){}},MASS:[],LV_MASS:[],fa:String,hash:()=>1,rng:()=>()=>0,
    levelsOf:()=>[{id:'pulley.2',title:'level',gen:()=>original}],
    ST:{pulley:{mount:(spec,A)=>{mounted.push(spec);board=A;},c:'#123'}},
    board:(k,head)=>{lastHead=head;buttons=[];return {nav:()=>buttons,fb(){}};},
    $:s=>elements[s]||(elements[s]={}),dotsHtml:()=>'',
    btn:(nav,label,cls,click)=>{const b={label,click,focus(){}};nav.push(b);return b;},
    later:(ms,f)=>f(),revealFb(){},save:()=>saved.push(JSON.stringify(S)),
    starsFor:(pts,max)=>pts>=max*.9?3:pts>=max*.66?2:pts>=max*.4?1:0,
    setLS:(id,v)=>{stars.push(v);S.ls['c:'+id]=Math.max(S.ls['c:'+id]||0,v);}
  });
  vm.runInContext(levelSource,ctx);
  ctx.playLevel('pulley',1,{land:2,keep:st=>snapshots.push(JSON.parse(JSON.stringify(st))),back(){},finish:(...args)=>{finished=args;}});
  const answer=p=>board.done(p),click=label=>{const b=buttons.find(b=>b.label===label);assert.ok(b,label);b.click();};
  assert.equal(lastHead.land,2);
  answer(points);
  const afterAnswer=JSON.stringify(S),calls=snapshots.length,saves=saved.length;
  click('بیا یک بار دیگر انجامش بدهیم');
  assert.equal(mounted.at(-1),original[0],'practice reuses the identical challenge spec');
  answer(2);
  assert.equal(JSON.stringify(S),afterAnswer,'practice cannot improve original stars/challenge best');
  assert.equal(snapshots.length,calls,'practice answer cannot overwrite resume snapshot');
  assert.equal(saved.length,saves,'practice answer does not save scored progress');
  click('دوباره تمرین کن');answer(0);
  assert.equal(JSON.stringify(S),afterAnswer,'failed practice cannot reduce progress');
  lastHead.back();
  assert.equal(snapshots.at(-1).i,1,'back after disclosed answer resumes next unanswered challenge');
  assert.equal(snapshots.at(-1).res[0],points);
  click('ادامهٔ مرحله');assert.equal(mounted.at(-1),original[1]);
  answer(2);click('بیا یک بار دیگر انجامش بدهیم');answer(2);
  lastHead.back();assert.equal(snapshots.at(-1).done,true,'back after final replay keeps mission complete');
  click('دیدن نتیجه');
  assert.deepEqual(finished,[points===2?3:points===1?2:1,points+2,4]);
  assert.equal(S.cb['c:first'],Math.max(1,points));
  assert.equal(stars.length,1,'only the original stage result commits stars');
}
// Success, show-me (1 point), and disclosed wrong-answer (0 point) replay equally safely.
for(const points of [2,1,0])session(points);
// Execute the real board's free-try/show-me and question-disclosure branches.
const aStart=app.indexOf('const A={',app.indexOf('function board('));
const aEnd=app.indexOf('  $("#bk").onclick',aStart);
function challenge(){
  const els={'#nv':{insertAdjacentHTML(){els['#showme']={};}}};
  const ui=vm.createContext({svg:{},P0:{},head:{mode:'level'},S:{formula:false},
    KID:()=>false,fa:String,voice:()=>'',ltrMath:x=>x,later(){},setMood(){},revealFb(){},
    $:id=>els[id]||(['#fb','#hlpb'].includes(id)?els[id]={classList:{add(){}}}:null)});
  vm.runInContext(app.slice(aStart,aEnd).replace('const A=','globalThis.A='),ui);
  let result,shown=false;ui.A.done=pts=>{result=pts;};
  const m={retry:'retry',more:'more',final:'disclosed',show:()=>{shown=true;}};
  for(let n=0;n<3;n++)ui.A.trial(false,m);
  assert.equal(ui.A.locked,false);assert.equal(result,undefined);
  els['#showme'].onclick();
  assert.equal(result,1);assert.equal(ui.A.assisted,true);assert.equal(ui.A.answerShown,true);assert.equal(shown,true);
  // A disclosed answer is committed once even if the button is pressed again.
  result=undefined;els['#showme'].onclick();assert.equal(result,undefined);
  return ui.A;
}
challenge();
// Route evidence is local and isolated from all old save/code slots (content version 2: bands, per-mission goals, migration).
const strings=JSON.parse(fs.readFileSync(path.join(dir,'harbor','strings.fa.json'),'utf8'));
const HARBOR_STR=Object.fromEntries(Object.entries(strings).map(([k,v])=>[k,v.text]));
const FA='۰۱۲۳۴۵۶۷۸۹';
const content=fs.readFileSync(path.join(dir,'harbor-content.js'),'utf8');
const routes=fs.readFileSync(path.join(dir,'harbor-routes.js'),'utf8');
const pure=vm.createContext({HARBOR_STR,fa:v=>String(v).replace(/\d/g,d=>FA[d]),pulleyIcon:()=>''});
vm.runInContext(content.slice(0,content.indexOf('function mountHarborActivity('))+routes.slice(routes.indexOf('const harborBand='),routes.indexOf('function harborEntry(')),pure);
const pilot=vm.runInContext('HARBOR_CONTENT',pure);
const record=pure.harborRecord,eligible=vm.runInContext('harborEligible',pure),done=vm.runInContext('harborRouteDone',pure),band=vm.runInContext('harborBand',pure);
const canPlay=pure.harborCanPlay,prereq={g:3};
assert.equal(pilot.version,2);assert.deepEqual(Array.from(pilot.routes.map(r=>r.id)),['harbor.fishing','harbor.pirate','harbor.dragon']);
assert.equal(pilot.routes[2].difficulty.tier,'very-hard');
const [green,orange,red]=pilot.routes;
assert.equal(canPlay(prereq,green.activities[0]),true);
assert.equal(canPlay(prereq,green.activities[1]),false);
assert.equal(canPlay(prereq,green.activities[2]),false);
for(const r of pilot.routes)assert.equal(canPlay(prereq,r.activities[0]),true,'no lock between challenges (B18)');
record(prereq,green.id,green.activities[0].id,{correct:true},false);
assert.equal(canPlay(prereq,green.activities[1]),true);
assert.equal(canPlay(prereq,orange.activities[1]),false,'progress in one challenge does not open another');
record(prereq,orange.id,orange.activities[0].id,{correct:true},false);
assert.equal(canPlay(prereq,orange.activities[1]),true);
prereq.routeProgress.regions.harbor.contentVersion=0;
assert.equal(canPlay(prereq,green.activities[1]),false,'stale evidence cannot open prerequisites');
const p={g:3,lvl:null,S:{ls:{'c:pulley.2':2},cb:{kept:1}},at:{i:9,j:1,r:{i:2}},stash:{b:{quiz:[1]}},quiz:[1],words:[1],home:[1],side:[1],opt:[1],done:'ab'};
const legacy=JSON.stringify(p),r=green,a=r.activities[0],ok={correct:true,independent:true,assisted:false,observed:['guess:0']};
assert.equal(record(p,'bad',a.id,ok,false),false);assert.equal(record(p,r.id,'bad',ok,false),false);
assert.equal(JSON.stringify(p),legacy,'invalid IDs do not create any state');
assert.equal(record(p,r.id,a.id,{...ok,correct:false,independent:false},false),true);
const first=JSON.stringify(p.routeProgress.regions.harbor.activities[a.id].first);
record(p,r.id,a.id,ok,false);
const e=p.routeProgress.regions.harbor.activities[a.id],latest=JSON.stringify(e.latest);
record(p,r.id,a.id,{...ok,correct:false},true);
assert.equal(JSON.stringify(e.first),first);assert.equal(JSON.stringify(e.latest),latest);assert.equal(e.runs,2);assert.equal(e.practices,1);
assert.equal(done(p,r),false);for(const act of r.activities.slice(1))record(p,r.id,act.id,ok,false);assert.equal(done(p,r),true);
const copied={...p};delete copied.routeProgress;assert.equal(JSON.stringify(copied),legacy);
// Bands from the grade only (B1, D250): 0 = second grade ... 4 = sixth grade.
assert.deepEqual([0,1,2,3,4].map(g=>band({g})),['1-2','3-4','3-4','5-6','5-6']);
for(const g of [0,1,2,3,4])assert.equal(eligible({g}),true,'harbor open for grade index '+g);
for(const g of [-1,5,6,7,undefined,null,'3'])assert.equal(eligible({g}),false);
assert.equal(eligible({g:3,lvl:'b'}),true,'band follows the grade, not the old track');
assert.equal(eligible(null),false);
assert.equal(done({g:3},r),false,'another player has no route completion');
const restored=JSON.parse(JSON.stringify(p));assert.equal(done(restored,r),true);assert.equal(JSON.stringify(restored.routeProgress),JSON.stringify(p.routeProgress));
// A content-version change migrates (keeps the old activities as legacy) and never wipes saved progress (B5, T8).
const oldKeys=Object.keys(restored.routeProgress.regions.harbor.activities);
restored.routeProgress.regions.harbor.contentVersion=1;restored.routeProgress.regions.harbor.routeId='harbor.pirate';
assert.equal(done(restored,r),false);
const st=pure.harborState(restored);
assert.deepEqual(Object.keys(st.activities),[]);assert.equal(st.contentVersion,2);assert.equal(st.routeId,'harbor.pirate');
assert.deepEqual(Object.keys(st.legacy.v1),oldKeys,'old activities are kept read-only');
pure.harborState(restored);assert.deepEqual(Object.keys(restored.routeProgress.regions.harbor.legacy),['v1'],'migration runs once');
for(const corrupt of [null,[],{version:99,regions:{}},{version:1,regions:[]},{version:1,regions:{harbor:{contentVersion:2,activities:[]}}}]){
 const q={g:3,routeProgress:corrupt};record(q,r.id,a.id,ok,false);assert.equal(q.routeProgress.regions.harbor.activities[a.id].runs,1);
}
for(const corrupt of ['broken',{},[]]){
 const q={g:3};pure.harborState(q).activities[a.id]=corrupt;record(q,r.id,a.id,ok,false);assert.equal(q.routeProgress.regions.harbor.activities[a.id].runs,1);
}
// Data extension: a fourth route has its own stable activity IDs and state.
const extra={...r,id:'harbor.extra',activities:r.activities.map((x,i)=>({...x,id:'harbor.extra.'+i,goals:['harbor.extra.'+i],prerequisiteGoals:i?['harbor.extra.'+(i-1)]:[]}))};
pilot.routes.push(extra);const extraProfile={g:4};
for(const act of extra.activities)record(extraProfile,extra.id,act.id,ok,false);
assert.equal(done(extraProfile,extra),true);assert.equal(done(extraProfile,r),false);
assert.equal(Object.keys(extraProfile.routeProgress.regions.harbor.activities).length,3);
console.log('harbor_routes: original score/resume, assistance, per-mission goals, bands for all grades, migration without wipe, corrupt saves passed');
