/* H1 is a separate, qualitative pilot. It does not replace old level ids. */
const HARBOR_CONTENT={
 version:1,regionId:"harbor",grades:[3,4],
 requiredGoals:["pulley.direction","pulley.compare","pulley.fit"],
 goalTitles:{"pulley.direction":"تغییر جهت کشیدن","pulley.compare":"مقایسهٔ دو آرایش","pulley.fit":"انتخاب برای یک نیاز"},
 routes:[
  {id:"harbor.fishing",title:"اسکلهٔ ماهیگیری",description:"تور و بار قایق را با قرقره بالا ببر.",environmentAssetId:"fishing-dock",
   difficulty:{concept:1,calculation:0,reading:1,controls:1,label:"آغاز آرام"},grades:[3,4],returnAllowed:true,
   activities:[
    {id:"harbor.fishing.direction",title:"بالا کشیدن تور",goals:["pulley.direction"],prerequisiteGoals:[],phase:"observe-apply",
     make:r=>({t:"fixedq",context:"تور کنار اسکله است. حرکت طناب و بار را ببین."})},
    {id:"harbor.fishing.compare",title:"دو راه برای بار قایق",goals:["pulley.compare"],prerequisiteGoals:["pulley.direction"],phase:"try-compare",
     make:r=>({t:"harborCompare",W:60,S:40,h:1,context:"همان بار قایق را تا همان خط بالا می‌بریم.",question:"در کدام آرایش، بار با همین نیروی در دسترس بالا رفت؟"})},
    {id:"harbor.fishing.fit",title:"انتخاب برای تور",goals:["pulley.fit"],prerequisiteGoals:["pulley.direction","pulley.compare"],phase:"try-apply",
     make:r=>({t:"harborNeed",need:"direction",W:30,S:40,h:1,context:"می‌خواهیم از روی اسکله طناب را پایین بکشیم و تور بالا برود.",question:"اگر فقط تغییر جهت کشیدن را بخواهیم، کدام آرایش کافی است؟"})}
   ]},
  {id:"harbor.pirate",title:"اسکلهٔ دزدان دریایی",description:"برای پرچم و صندوق کشتی، آرایش مناسب پیدا کن.",environmentAssetId:"pirate-dock",
   difficulty:{concept:2,calculation:0,reading:1,controls:1,label:"دلیل بیاور"},grades:[3,4],returnAllowed:true,
   activities:[
    {id:"harbor.pirate.direction",title:"پرچم کشتی",goals:["pulley.direction"],prerequisiteGoals:[],phase:"observe-apply",
     make:r=>({t:"fixedq",context:"پرچم کشتی باید بالا برود. حرکت طناب و بار را ببین."})},
    {id:"harbor.pirate.compare",title:"آزمایش صندوق",goals:["pulley.compare"],prerequisiteGoals:["pulley.direction"],phase:"try-compare",
     make:r=>({t:"harborCompare",W:60,S:40,h:1,context:"صندوق و ارتفاع یکسان‌اند؛ فقط آرایش قرقره را عوض می‌کنیم.",question:"چرا فقط آرایش ثابت و متحرک توانست صندوق را بالا ببرد؟",reason:true})},
    {id:"harbor.pirate.fit",title:"صندوق سنگین",goals:["pulley.fit"],prerequisiteGoals:["pulley.direction","pulley.compare"],phase:"try-apply",
     make:r=>({t:"harborNeed",need:"force",W:60,S:40,h:1,context:"با نیروی در دسترس، صندوق را تا خط سبز بالا ببر.",question:"کدام آرایش، با همین نیروی در دسترس صندوق را بالا برد؟"})}
   ]}
 ]
};

/* All observations belong to this attempt, not merely the route's saved goals.
   A successful lift is preparation: only the following answer judges the activity.
   The proxy suppresses the legacy formula/count UI without changing shared settings. */
function mountHarborActivity(sp,A){
 const evidence={activityId:sp.activityId||null,goals:(sp.goals||[]).slice(),observed:[],attempts:0,independent:true,answer:null};
 A.harborEvidence=evidence;
 const Q=new Proxy(A,{get(target,key){
   if(key==="qualitative")return true;
   if(key==="formula")return()=>{};
   if(key==="counter")return()=>A.counter('<span class="cc">همان بار، همان ارتفاع؛ حرکت طناب و بار را ببین.</span>');
   return Reflect.get(target,key);
 }});
 function record(id){if(!evidence.observed.includes(id))evidence.observed.push(id);}
 function assess(question,options,answer,explain,retry){
  A.fb("");A.prompt(question);const c=A.ctrl("");
  const m=mcq(c,options,(i,bt)=>{if(A.locked)return;evidence.attempts++;evidence.answer=i;
   if(i===answer){m.disable();m.mark(i,"right");A.judge(true,{ok:explain,pts:evidence.independent?2:1});}
   else{evidence.independent=false;m.mark(i,"wrong");bt.disabled=true;A.fb(retry,"info");}
  });
 }
 if(sp.t==="fixedq"){
  const pl=makePulley(Q,{n:1,W:60,S:100,h:1,edit:false,qualitative:true});A.refresh=()=>pl.render();
  A.prompt(sp.context+" سر آزاد طناب را پایین می‌کشیم. به جهت حرکت بار نگاه کن.");
  const c=A.ctrl("");const b=btn(c,"آزمایش را ببین","go",()=>{b.disabled=true;pl.auto(()=>{
   record("fixed.direction");
   assess("قرقرهٔ ثابت چه تغییری ایجاد کرد؟",["نیروی لازم را کمتر کرد","جهت کشیدن را عوض کرد","وزن بار را کم کرد"],1,
    "طناب را پایین کشیدیم و بار بالا رفت؛ قرقرهٔ ثابت جهت کشیدن را عوض می‌کند.","جهت حرکت سر آزاد طناب و بار را با هم مقایسه کن.");
  });});return;
 }
 if(sp.t!=="harborCompare"&&sp.t!=="harborNeed")throw new Error("Unknown harbor activity: "+sp.t);
 const compare=sp.t==="harborCompare",seen=new Set();let n=1,pl,ready=false;
 const names={1:"قرقرهٔ ثابت",2:"ثابت و متحرک"};
 function finishTrial(result){
  if(ready||A.locked)return;
  record(names[n]+":"+result);seen.add(n);
  if(!compare||seen.size===2){ready=true;showQuestion();}
  else{
   A.fb("این آرایش را آزمودی. اکنون آرایش دیگر را انتخاب کن و طناب را بکش.","info");
   renderControls();
  }
 }
 function paint(){
  pl=makePulley(Q,{n,W:sp.W,S:sp.S,h:sp.h,qualitative:true,
   onBlocked:()=>finishTrial("blocked"),
   onTop:()=>finishTrial("lifted")});
  A.refresh=()=>{pl.render();summary();};summary();
 }
 function summary(){
  const note=n===1?"قرقرهٔ ثابت بالا می‌ماند.":"قرقرهٔ پایینی همراه بار حرکت می‌کند.";
  A.counter('<span class="cc">'+names[n]+"؛ "+note+"</span>");
 }
 function renderControls(){
  if(ready||A.locked)return;
  const c=A.ctrl("");[1,2].forEach(k=>btn(c,names[k],k===n?"sel":"",()=>{if(A.locked||ready)return;n=k;paint();renderControls();}));
 }
 function showQuestion(){
  if(A.locked)return;
  if(compare){
   assess(sp.question,sp.reason?["با همان بار و ارتفاع، نیروی لازم کمتر شد","چون وزن صندوق کم شد","چون ارتفاع هدف کمتر شد"]:["قرقرهٔ ثابت","ثابت و متحرک","هر دو نیروی برابر می‌خواستند"],sp.reason?0:1,
    "با بار و ارتفاع یکسان، آرایش ثابت و متحرک نیروی کمتری می‌خواهد. قرقرهٔ پایینی همراه بار حرکت می‌کند.",
    sp.reason?"در این آزمایش، بار و ارتفاع چه تغییری کردند؟":"نیروی لازم در دو آرایش را مقایسه کن. قرقرهٔ پایینی با بار حرکت می‌کند.");
  }else{
   /* A blocked fixed trial alone does not provide the successful comparison. */
   if((sp.need==="force"&&seen.size<2)||(sp.need==="direction"&&!seen.has(1))){
    ready=false;A.fb(sp.need==="force"?"آرایش دیگر را هم با همین نیرو بیازما.":"قرقرهٔ ثابت را هم بیازما و جهت حرکت را ببین.","info");renderControls();return;
   }
   assess(sp.question,["قرقرهٔ ثابت","ثابت و متحرک"],sp.need==="force"?1:0,
    sp.need==="force"?"آرایش ثابت و متحرک نیروی لازم را کمتر کرد و صندوق بالا رفت؛ وزن صندوق تغییر نکرد.":"قرقرهٔ ثابت برای تغییر جهت کافی است؛ سر طناب پایین می‌رود و بار بالا می‌رود.",
    sp.need==="force"?"نتیجهٔ کشیدن صندوق را در دو آرایش به یاد بیاور.":"برای این کار، فقط می‌خواهیم جهت کشیدن عوض شود.");
  }
 }
 A.prompt(sp.context+" "+(compare?"هر دو آرایش را انتخاب کن و دستگیرهٔ زرد را پایین بکش. ببین بار با کدام آرایش به خط سبز می‌رسد.":"آرایش را انتخاب کن و دستگیرهٔ زرد را پایین بکش تا بار به خط سبز برسد."));
 paint();renderControls();
}
