/* M07 harbor pilot, content version 2 (D250, D251; docs/plans/games/M07_HARBOR_PILOT_SPEC_FA.md).
   Every user-facing Persian string is read by id from HARBOR_STR (harbor/strings.fa.json, built in by build.py).
   Nothing in this file may contain Persian text (B49/B50); tests/harbor_content.js checks that.
   Model data are in "model units": W load, S available force, h height, ropeMax rope supply (same unit as h).
   Display: band 1-2 no numbers; band 3-4 squares (1 square = 10 units) and steps; band 5-6 newtons (units x 10) and metres. */
const HARBOR_BANDS=["1-2","3-4","5-6"];
const hbk=b=>"b"+String(b).replace("-","");
function harborHas(id,band){return HARBOR_STR[id+"."+hbk(band)]!=null||HARBOR_STR[id]!=null;}
/* Text by stable id; band suffix (.b12/.b34/.b56) wins over the plain id; <x/> tokens are filled from vars. */
function hs(id,band,vars){
 const k=band!=null&&HARBOR_STR[id+"."+hbk(band)]!=null?id+"."+hbk(band):id,t=HARBOR_STR[k];
 if(t==null)throw new Error("harbor text missing: "+id);
 return vars?t.replace(/<(\w+)\/>/g,(m,n)=>vars[n]!=null?vars[n]:m):t;
}
const harborUnit=(b,v)=>b==="3-4"?fa(v/10)+" "+hs("harbor.ui.unit.square"):b==="5-6"?fa(v*10)+" "+hs("harbor.ui.unit.newton"):"";
const harborLen=(b,v)=>b==="3-4"?fa(v)+" "+hs("harbor.ui.unit.step"):b==="5-6"?fa(v)+" "+hs("harbor.ui.unit.meter"):"";
/* Model data per mission. alt[band] overrides. best = the single right arrangement (n = supporting rope parts, A15). */
const HARBOR_DATA={
 "green.m1":{t:"harborLift",W:30,S:40,h:2},
 "green.m2":{t:"harborLift",W:10,S:40,h:2},
 "green.m3":{t:"harborLift",W:20,S:40,h:2,q:true},
 "orange.m1":{t:"harborTry",W:60,S:40,h:2},
 "orange.m2":{t:"harborHelpers",W:60,S:40,h:2,helpers:2},
 "orange.m3":{t:"harborLift",W:30,S:40,h:2,q:true},
 "red.m1":{t:"harborPick",opts:[1,2],W:30,S:40,h:2,ropeMax:3,best:1,alt:{"1-2":{W:60,ropeMax:null,best:2},"3-4":{W:40,S:50}}},
 "red.m2":{t:"harborPick",opts:[1,2],W:60,S:40,h:2,ropeMax:5,best:2,alt:{"1-2":{t:"harborCoils",W:30,ropeMax:null,best:null},"3-4":{W:80,S:50}}},
 "red.m3":{t:"harborPlan",opts:[1,2],plan:[30,60],S:40,h:2,ropeMax:7,best:[1,2],q:true,alt:{"1-2":{t:"harborPick",plan:null,W:30,ropeMax:3,best:1},"3-4":{plan:[40,80],S:50}}}
};
/* Scored question: index of the right option and number of options, per challenge and band (positions vary on purpose). */
const HARBOR_Q={green:{"1-2":{answer:1,n:2},"3-4":{answer:0,n:3},"5-6":{answer:1,n:3}},orange:{"1-2":{answer:0,n:3},"3-4":{answer:1,n:3},"5-6":{answer:1,n:3}},red:{"1-2":{answer:1,n:2},"3-4":{answer:1,n:3},"5-6":{answer:0,n:3}}};
function harborSpec(key,band){
 const d=HARBOR_DATA[key],o=Object.assign({},d,d.alt&&d.alt[band]||{});delete o.alt;
 o.band=band;o.key=key;o.sid="harbor."+key;o.color=key.split(".")[0];if(o.q)o.q=HARBOR_Q[o.color][band];return o;
}
/* Routes (challenges). Stable ids; the old v1 activity ids (…direction, …compare, …fit) stay only in saved state under "legacy".
   Missions are steps inside a challenge (B26); the order inside a challenge is guided, never between challenges (B18).
   Goals are per mission so progress in one challenge never unlocks or locks another. */
const HARBOR_CONTENT={
 version:2,regionId:"harbor",bands:HARBOR_BANDS,
 routes:[["fishing","green","fishing-dock","core",{concept:1,calculation:0,reading:1,controls:1}],["pirate","orange","pirate-dock","challenge",{concept:2,calculation:0,reading:1,controls:1}],["dragon","red","dragon-dock","very-hard",{concept:3,calculation:0,reading:1,controls:2}]].map(([name,color,env,tier,d])=>({
  id:"harbor."+name,color,environmentAssetId:env,difficulty:Object.assign({tier},d),returnAllowed:true,
  activities:[1,2,3].map(k=>({id:"harbor."+name+".m"+k,key:color+".m"+k,goals:["harbor."+name+".m"+k],prerequisiteGoals:k>1?["harbor."+name+".m"+(k-1)]:[],phase:k<3?"try-observe":"try-apply",make:band=>harborSpec(color+".m"+k,band)}))}))
};
const harborRouteText=(r,k,band)=>hs("harbor."+r.color+"."+k,band);
const harborActTitle=(a,band)=>hs("harbor."+a.key+".title",band);
function harborOutcome(W,n,S,h,ropeMax,used){const F=W/n,need=n*h,force=F<S-1e-9,rope=ropeMax==null||used+need<=ropeMax+1e-9;return{F,need,force,rope,lifts:force&&rope};}
/* All arrangements that succeed (pure; used by the tests: a pick or plan question must have exactly one). */
function harborSolutions(sp){
 const S=sp.t==="harborTry"?sp.S:sp.S*(sp.helpers||1),out=[];
 if(sp.plan){for(const a of sp.opts)for(const b of sp.opts){const o1=harborOutcome(sp.plan[0],a,S,sp.h,sp.ropeMax,0),o2=harborOutcome(sp.plan[1],b,S,sp.h,sp.ropeMax,a*sp.h);if(o1.lifts&&o2.lifts)out.push([a,b]);}return out;}
 for(const n of sp.opts||[1])if(harborOutcome(sp.W,n,S,sp.h,sp.ropeMax,0).lifts)out.push([n]);
 return out;
}
/* Distances from every limit; none may be 0 (A15: never tune a mission onto the equality border). */
function harborMargins(sp){
 const m=[],Ss=[sp.S*(sp.helpers||1)];if(sp.helpers>1)Ss.push(sp.S);const loads=sp.plan||[sp.W];
 for(const W of loads)for(const n of sp.opts||[1]){for(const S of Ss)m.push(W/n-S);if(sp.ropeMax!=null)m.push(n*sp.h-sp.ropeMax);}
 if(sp.plan&&sp.ropeMax!=null)for(const a of sp.opts)for(const b of sp.opts)m.push((a+b)*sp.h-sp.ropeMax);
 return m;
}
function harborVars(sp){
 const b=sp.band,u=v=>harborUnit(b,v),l=v=>harborLen(b,v),W=sp.plan?sp.plan[1]:sp.W;
 return{w:sp.W!=null?u(sp.W):"",s:u(sp.S),s2:u(sp.S*2),h:l(sp.h),r:sp.ropeMax!=null?l(sp.ropeMax):"",w1:sp.plan?u(sp.plan[0]):"",w2:sp.plan?u(sp.plan[1]):"",f:W!=null?u(W):"",f2:W!=null?u(W/2):"",rn1:l(sp.h),rn2:l(2*sp.h)};
}
const harborArrIcon=k=>`<svg viewBox="0 0 40 28" width="40" height="28" aria-hidden="true">${pulleyIcon(k)}</svg>`;
function harborCoil(len){let e="";for(let i=0;i<len*2;i++)e+=`<ellipse cx="30" cy="${50-i*5}" rx="${24-i*.3}" ry="6" fill="none" stroke="#7A5634" stroke-width="3"/>`;return `<svg viewBox="0 0 60 56" width="60" height="56" aria-hidden="true">${e}</svg>`;}

/* One mission = guess (unscored) -> experiment -> seen. Only the question after mission 3 is scored (two chances, then the cause).
   A failed physical try costs nothing (A8). Evidence is for the teacher page only; nothing here shows stars or points (B4). */
function mountHarborActivity(sp,A){
 const evidence={activityId:sp.activityId||null,goals:(sp.goals||[]).slice(),observed:[],attempts:0,independent:true,answer:null};
 A.harborEvidence=evidence;
 const band=sp.band,V=harborVars(sp),T_=(k,x)=>hs(sp.sid+"."+k,band,x?Object.assign({},V,x):V),U_=(k,x)=>hs("harbor.ui."+k,band,x?Object.assign({},V,x):V);
 const has=k=>harborHas(sp.sid+"."+k,band),tx=(k,x)=>has(k)?T_(k,x):U_(k,x),u=v=>harborUnit(band,v),l=v=>harborLen(band,v);
 let pl=null,cur=null,strip="",fails=0;
 const Q=new Proxy(A,{get(target,key){
   if(key==="qualitative")return true;
   if(key==="formula")return()=>{};
   if(key==="counter")return()=>readout();
   return Reflect.get(target,key);
 }});
 const arr=k=>U_("arr."+k);
 function readout(){
  if(strip){A.counter(strip);return;}
  if(!cur){A.counter("");return;}
  const st=cur.pl.st;let h="";
  if(band==="1-2"){if(sp.opts&&sp.opts.length>1)h=`<span class="cc">${arr(cur.n)}</span>`;}
  else h=`<span class="cc">${U_("counter.rope",{v:l(r1(st.pulled))})}</span><span class="cc">${U_("counter.rise",{v:l(r1(st.pulled/st.n))})}</span>`;
  A.counter(h);
 }
 function record(id){if(!evidence.observed.includes(id))evidence.observed.push(id);}
 function scene(n,over){
  over=over||{};cur=null;
  const orange=sp.color==="orange",helpers=over.helpers||1,S0=over.S!=null?over.S:sp.S*helpers;
  const avail=U_(orange?(helpers>1?"label.avail.pirates2":"label.avail.pirate"):"label.avail.sailor");
  pl=makePulley(Q,Object.assign({n,W:sp.W,S:S0,h:sp.h,qualitative:true,band,ropeMax:sp.ropeMax,helpers,fmt:v=>harborUnit(band,v),targetText:band==="1-2"?U_("label.target"):U_("label.target.n",{h:l(sp.h)}),
   ropeText:sp.ropeMax==null?"":band==="1-2"?U_("label.rope"):U_("label.rope.n",{r:l(sp.ropeMax)}),
   labels:{weight:U_("label.weight"),need:U_("label.need"),avail,crate:U_("label.crate")}},over));
  cur={pl,n};A.refresh=()=>{pl.render();readout();};readout();return pl;
 }
 function complete(msg){if(A.locked)return;A.judge(true,{ok:msg,pts:evidence.independent?2:1,act:true});}
 function seen(){
  record("lifted");
  if(sp.q){if(sp.color==="red"){strip=stripHtml();readout();}assess();A.fb(T_("seen"),"info");}else complete(T_("done"));
 }
 function assess(){
  const q=sp.q,Q_=(k,x)=>hs("harbor."+sp.color+".q."+k,band,x?Object.assign({},V,x):V);A.fb("");A.prompt(Q_("prompt"));const c=A.ctrl("");
  const opts=[];for(let i=1;i<=q.n;i++)opts.push(Q_("opt"+i));
  const m=mcq(c,opts,(i,bt)=>{if(A.locked)return;evidence.attempts++;evidence.answer=i;
   if(i===q.answer){m.disable();m.mark(i,"right");A.judge(true,{ok:Q_("explain"),pts:evidence.independent?2:1});}
   else{evidence.independent=false;m.mark(i,"wrong");bt.disabled=true;A.judge(false,{retry:Q_("retry"),final:Q_("explain")});if(A.locked){m.disable();m.mark(q.answer,"right");}}
  });
 }
 /* Cause of a blocked try, always visible in the scene as well (A9). */
 function failMsg(kind,n,W,S,left){
  return kind==="rope"?tx("fail.rope",{rn:l(n*sp.h),r:l(left)}):tx("fail.force",{f:u(W/n),s:u(S)});
 }
 function guess(next){
  scene(sp.opts?sp.opts[0]:1,{edit:false,W:sp.plan?sp.plan[0]:sp.W,helpers:1});/* the scene is visible while the child guesses; it cannot be pulled yet */
  A.prompt(T_("prompt")+" "+T_("guess.q"));
  const c=A.ctrl(""),opts=[],strict=HARBOR_STR[sp.sid+".guess.opt1."+hbk(band)]!=null;
  for(let i=1;i<=4&&(strict?HARBOR_STR[sp.sid+".guess.opt"+i+"."+hbk(band)]!=null:has("guess.opt"+i));i++)opts.push(T_("guess.opt"+i));
  const m=mcq(c,opts,i=>{record("guess:"+i);A.ctrl("");A.prompt(T_("prompt")+" "+U_("tryNow"));A.fb(U_("guessSaved"),"info");next();});
 }
 function arrangementControls(select,extra){
  const c=A.ctrl("");
  for(const k of sp.opts)btn(c,harborArrIcon(k)+" "+arr(k),k===cur.n?"sel":"",()=>{if(A.locked)return;select(k);});
  if(extra)extra(c);
 }
 function showMe(c,done){
  const b=btn(c,U_("btn.showMe"),"",()=>{if(A.locked)return;A.assisted=true;A.answerShown=true;A.locked=true;done();A.fb(T_("showed"),"info");A.done(1);});b.setAttribute("data-show","1");
 }
 /* mission types */
 function expLift(){scene(1,{onTop:seen,onBlocked:()=>A.fb(failMsg("force",1,sp.W,sp.S,0),"info")});}
 function expTry(){
  scene(1,{onBlocked:()=>{if(A.locked)return;record("blocked");complete(T_("done"));}});
 }
 function expHelpers(){
  let helpers=1;
  const paint=()=>scene(1,{helpers,onTop:seen,onBlocked:()=>{record("blocked:"+helpers);A.fb(failMsg("force",1,sp.W,sp.S*helpers),"info");}});
  paint();const c=A.ctrl("");
  const b=btn(c,T_("btn.helper"),"go",()=>{if(A.locked||helpers>1)return;helpers=2;b.disabled=true;record("helper");paint();A.fb(T_("helperIn"),"info");});
 }
 function expPick(){
  let n=sp.opts[0];
  const best=sp.best;
  const reveal=()=>{n=best;paint();pl.st.pulled=best*sp.h;pl.st.done=true;pl.render();readout();};
  const bad=kind=>{fails++;A.fb(failMsg(kind,n,sp.W,sp.S,pl.ropeLeft()),"info");record("fail:"+kind+":"+n);if(fails===3)controls();};
  const paint=()=>scene(n,{onTop:()=>{record("lifted:"+n);seen();},onBlocked:()=>bad("force"),onRopeOut:()=>bad("rope")});
  const select=k=>{n=k;paint();controls();};
  const controls=()=>arrangementControls(select,c=>{if(fails>=3)showMe(c,reveal);});
  paint();controls();
 }
 function expCoils(){
  const done=new Set();let n=1;
  const paint=()=>scene(n,{onTop:()=>{if(A.locked)return;done.add(n);record("lifted:"+n);
    if(done.size===sp.opts.length){strip=stripHtml();readout();complete(T_("done"));}else A.fb(T_("other"),"info");}});
  const select=k=>{n=k;paint();controls();};
  const controls=()=>arrangementControls(select);
  paint();controls();
 }
 function expPlan(){
  let step=0,used=0,n=sp.opts[0];
  const paint=()=>scene(n,{W:sp.plan[step],ropeUsed0:used,
   onTop:()=>{record("lifted:"+step+":"+n);used+=n*sp.h;if(step===0){step=1;n=sp.opts[0];paint();controls();A.fb(T_("plan.next"),"info");}else seen();},
   onBlocked:()=>{fails++;A.fb(failMsg("force",n,sp.plan[step],sp.S,0),"info");record("fail:force:"+step+":"+n);},
   onRopeOut:()=>{fails++;record("fail:rope:"+step+":"+n);A.fb(T_("plan.fail.rope",{rn:l(n*sp.h),r:l(sp.ropeMax-used)}),"info");}});
  const select=k=>{n=k;paint();controls();};
  const controls=()=>arrangementControls(select,c=>btn(c,U_("btn.restartPlan"),"",()=>{if(A.locked)return;step=0;used=0;n=sp.opts[0];paint();controls();A.fb(T_("plan.restarted"),"info");}));
  A.fb(T_("plan.first"),"info");paint();controls();
 }
 /* Evidence shown with the final question of the red challenge: both arrangements side by side (A2). */
 function stripHtml(){
  const W=sp.plan?sp.plan[1]:sp.W;
  if(band==="1-2")return sp.opts.map(n=>`<span class="cc">${harborArrIcon(n)} ${arr(n)} ${harborCoil(n*sp.h)}</span>`).join("");
  return sp.opts.map(n=>`<span class="cc">${U_("strip.row",{a:arr(n),f:u(W/n),rn:l(n*sp.h)})}</span>`).join("");
 }
 const kinds={harborLift:expLift,harborTry:expTry,harborHelpers:expHelpers,harborPick:expPick,harborCoils:expCoils,harborPlan:expPlan};
 if(!kinds[sp.t])throw new Error("Unknown harbor activity: "+sp.t);
 guess(kinds[sp.t]);
}
