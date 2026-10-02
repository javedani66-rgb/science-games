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
// Route evidence is local and isolated from all old save/code slots.
const content=fs.readFileSync(path.join(dir,'harbor-content.js'),'utf8');
const routes=fs.readFileSync(path.join(dir,'harbor-routes.js'),'utf8');
const pure=vm.createContext({trk:p=>p.lvl|| (p.g<=1?'a':p.g===2?'b':p.g<=4?'c':'d')});
vm.runInContext(content.slice(0,content.indexOf('function mountHarborActivity('))+routes.slice(0,routes.indexOf('function harborEntry(')),pure);
const pilot=vm.runInContext('HARBOR_CONTENT',pure);
const record=pure.harborRecord,eligible=vm.runInContext('harborEligible',pure),done=vm.runInContext('harborRouteDone',pure);
const canPlay=pure.harborCanPlay,prereq={g:3};
assert.equal(canPlay(prereq,pilot.routes[0].activities[0]),true);
assert.equal(canPlay(prereq,pilot.routes[0].activities[1]),false);
assert.equal(canPlay(prereq,pilot.routes[0].activities[2]),false);
record(prereq,pilot.routes[0].id,pilot.routes[0].activities[0].id,{correct:true},false);
assert.equal(canPlay(prereq,pilot.routes[1].activities[1]),true,'shared observed goal follows route switching');
assert.equal(canPlay(prereq,pilot.routes[1].activities[2]),false,'fit still needs comparison');
record(prereq,pilot.routes[1].id,pilot.routes[1].activities[1].id,{correct:true},false);
assert.equal(canPlay(prereq,pilot.routes[0].activities[2]),true);
prereq.routeProgress.regions.harbor.contentVersion=0;
assert.equal(canPlay(prereq,pilot.routes[0].activities[1]),false,'stale evidence cannot open prerequisites');
const p={g:3,lvl:null,S:{ls:{'c:pulley.2':2},cb:{kept:1}},at:{i:9,j:1,r:{i:2}},stash:{b:{quiz:[1]}},quiz:[1],words:[1],home:[1],side:[1],opt:[1],done:'ab'};
const legacy=JSON.stringify(p),r=pilot.routes[0],a=r.activities[0],ok={correct:true,independent:true,assisted:false,observed:['fixed']};
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
for(const g of [0,1,2,5,6,7]){const q={g};assert.equal(eligible(q),false);assert.equal(record(q,r.id,a.id,ok,false),false);assert.equal(q.routeProgress,undefined);}
assert.equal(eligible({g:4}),true);assert.equal(eligible({g:3,lvl:'b'}),false);
assert.equal(done({g:3},r),false,'another player has no route completion');
const restored=JSON.parse(JSON.stringify(p));assert.equal(done(restored,r),true);assert.equal(JSON.stringify(restored.routeProgress),JSON.stringify(p.routeProgress));
restored.routeProgress.regions.harbor.contentVersion=0;assert.equal(done(restored,r),false);assert.deepEqual(Object.keys(pure.harborState(restored).activities),[]);
for(const corrupt of [null,[],{version:99,regions:{}},{version:1,regions:[]},{version:1,regions:{harbor:{contentVersion:1,activities:[]}}}]){
 const q={g:3,routeProgress:corrupt};record(q,r.id,a.id,ok,false);assert.equal(q.routeProgress.regions.harbor.activities[a.id].runs,1);
}
for(const corrupt of ['broken',{},[]]){
 const q={g:3};pure.harborState(q).activities[a.id]=corrupt;record(q,r.id,a.id,ok,false);assert.equal(q.routeProgress.regions.harbor.activities[a.id].runs,1);
}
// Drive real content transitions: lifting is evidence, answering is the assessment.
function activity(spec){
 let controls=[],question,physics,judged=[];
 const A={locked:false,ctrl:()=>{controls=[];return controls;},counter(){},prompt(){},fb(){},judge:(ok,m)=>{judged.push(m.pts);}};
 const c=vm.createContext({
  rng:()=>()=>0,makePulley:(Q,p)=>{physics=p;return {render(){},auto:done=>done()};},
  btn:(parent,label,cls,click)=>{const b={label,click};parent.push(b);return b;},
  mcq:(parent,options,callback)=>{question={options,callback};return {disable(){},mark(){}};}
 });vm.runInContext(content.slice(content.indexOf('function mountHarborActivity(')),c);
 c.mountHarborActivity(spec,A);
 return {A,click:label=>{const b=controls.find(b=>b.label===label);assert.ok(b,label);b.click();},
  observe:result=>physics[result==='blocked'?'onBlocked':'onTop'](),answer:i=>question.callback(i,{disabled:false}),
  hasQuestion:()=>!!question,judged};
}
for(const route of pilot.routes){
 const fixed=activity(route.activities[0].make());assert.equal(fixed.hasQuestion(),false);
 fixed.click('آزمایش را ببین');assert.equal(fixed.hasQuestion(),true);assert.equal(fixed.judged.length,0);
 fixed.answer(1);assert.equal(fixed.judged[0],2);assert.ok(fixed.A.harborEvidence.observed.includes('fixed.direction'));
 const compare=activity(route.activities[1].make());compare.observe('blocked');assert.equal(compare.hasQuestion(),false);
 compare.click('ثابت و متحرک');compare.observe('lifted');assert.equal(compare.hasQuestion(),true);assert.equal(compare.judged.length,0);
 compare.answer(route.id==='harbor.pirate'?0:1);assert.equal(compare.judged[0],2);assert.equal(compare.A.harborEvidence.observed.length,2);
 const fit=activity(route.activities[2].make());
 if(route.id==='harbor.pirate'){fit.observe('blocked');assert.equal(fit.hasQuestion(),false);fit.click('ثابت و متحرک');fit.observe('lifted');}
 else fit.observe('lifted');
 assert.equal(fit.hasQuestion(),true);fit.answer(route.id==='harbor.pirate'?1:0);assert.equal(fit.judged[0],2);
}
// Data extension: a third route has its own stable activity IDs and state.
const third={...r,id:'harbor.third',activities:r.activities.map((a,i)=>({...a,id:'harbor.third.'+i}))};
pilot.routes.push(third);const thirdProfile={g:4};
for(const act of third.activities)record(thirdProfile,third.id,act.id,ok,false);
assert.equal(done(thirdProfile,third),true);assert.equal(done(thirdProfile,r),false);
assert.equal(Object.keys(thirdProfile.routeProgress.regions.harbor.activities).length,3);
console.log('harbor_routes: original score/resume, assistance, isolated evidence, corrupt saves and observed route goals passed');
