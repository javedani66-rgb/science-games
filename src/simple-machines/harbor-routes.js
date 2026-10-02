const HARBOR_ROUTE_ICONS={"fishing-dock": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 240 128\" aria-hidden=\"true\" focusable=\"false\"><rect width=\"240\" height=\"128\" rx=\"14\" fill=\"#DFF1F2\"/><circle cx=\"204\" cy=\"23\" r=\"12\" fill=\"#FFE5A1\"/><path d=\"M0 89Q35 77 68 89T137 89T205 89T260 89V128H0Z\" fill=\"#86C4CC\"/><path d=\"M10 110q13-6 26 0m18 6q13-6 26 0m78-6q13-6 26 0m16 6q13-6 26 0\" stroke=\"#1F6F7F\" stroke-width=\"2\" fill=\"none\"/><g stroke=\"#3B2417\" stroke-width=\"3\" stroke-linejoin=\"round\" stroke-linecap=\"round\"><path d=\"M124 86h84l-12 17h-60Z\" fill=\"#F5C476\"/><path d=\"M170 86V56\" fill=\"none\"/><path d=\"M171 56l25 26h-25Z\" fill=\"#FFF8E8\"/><path d=\"M24 85V21h76v11\" fill=\"none\"/><circle cx=\"100\" cy=\"38\" r=\"7\" fill=\"#F7DCA5\"/><path d=\"M100 32v30\" fill=\"none\"/><path d=\"M82 62h34l-5 19H87Z\" fill=\"#E8B57E\"/><path d=\"M85 68h28m-22-5v16m9-16v16m9-16v16\" fill=\"none\" stroke-width=\"2\"/><path d=\"M52 76q12-12 26 0-14 12-26 0l-8-6v12Z\" fill=\"#9ED2D9\"/><circle cx=\"71\" cy=\"74\" r=\"2\" fill=\"#3B2417\" stroke=\"none\"/><path d=\"M8 86h99v10H8Z\" fill=\"#D5A26B\"/><path d=\"M24 96v25m62-25v25M8 91h99\" fill=\"none\"/></g></svg>", "pirate-dock": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 240 128\" aria-hidden=\"true\" focusable=\"false\"><rect width=\"240\" height=\"128\" rx=\"14\" fill=\"#DFF1F2\"/><circle cx=\"204\" cy=\"23\" r=\"12\" fill=\"#FFE5A1\"/><path d=\"M0 89Q35 77 68 89T137 89T205 89T260 89V128H0Z\" fill=\"#86C4CC\"/><path d=\"M10 110q13-6 26 0m18 6q13-6 26 0m78-6q13-6 26 0m16 6q13-6 26 0\" stroke=\"#1F6F7F\" stroke-width=\"2\" fill=\"none\"/><g stroke=\"#3B2417\" stroke-width=\"3\" stroke-linejoin=\"round\" stroke-linecap=\"round\"><path d=\"M116 83h110l-15 23h-80Z\" fill=\"#A9754C\"/><path d=\"M171 83V17\" fill=\"none\"/><path d=\"M172 21h34l-7 10 7 10h-34Z\" fill=\"#F2785C\"/><path d=\"m181 26 12 10m0-10-12 10\" stroke=\"#FFF8E8\"/><path d=\"M166 45l-24 33h24Zm11 0 25 33h-25Z\" fill=\"#FFF8E8\"/><path d=\"M34 85V26h61v9\" fill=\"none\"/><circle cx=\"95\" cy=\"41\" r=\"7\" fill=\"#F7DCA5\"/><path d=\"M95 35v23\" fill=\"none\"/><rect x=\"75\" y=\"58\" width=\"38\" height=\"24\" rx=\"3\" fill=\"#D5A26B\"/><path d=\"M75 67h38m-26-9v24m14-24v24\" fill=\"none\" stroke-width=\"2\"/><rect x=\"90\" y=\"66\" width=\"8\" height=\"7\" rx=\"1\" fill=\"#FFE5A1\"/><path d=\"M8 86h99v10H8Z\" fill=\"#D5A26B\"/><path d=\"M24 96v25m62-25v25M8 91h99\" fill=\"none\"/></g></svg>"};
/* H1 local prototype. Route evidence never fabricates legacy mission stars.
   Stable IDs and versioned profile storage allow more routes without new slots. */
const harborEligible=p=>!!p&&HARBOR_CONTENT.grades.includes(p.g)&&trk(p)==='c';
function harborState(p){
 if(!p.routeProgress||p.routeProgress.version!==1||!p.routeProgress.regions||typeof p.routeProgress.regions!=='object'||Array.isArray(p.routeProgress.regions))p.routeProgress={version:1,regions:{}};
 const all=p.routeProgress.regions;
 if(!all.harbor||all.harbor.contentVersion!==HARBOR_CONTENT.version||!all.harbor.activities||typeof all.harbor.activities!=='object'||Array.isArray(all.harbor.activities))all.harbor={contentVersion:HARBOR_CONTENT.version,routeId:null,activities:{}};
 return all.harbor;
}
const harborRoute=id=>HARBOR_CONTENT.routes.find(r=>r.id===id);
function harborRecord(p,routeId,activityId,answer,practice){
 const route=harborRoute(routeId),activity=route&&route.activities.find(a=>a.id===activityId);
 if(!harborEligible(p)||!activity)return false;
 const state=harborState(p),raw=state.activities[activityId],valid=raw&&typeof raw==='object'&&!Array.isArray(raw);
 const old=valid?raw:{runs:0,practices:0,first:null,latest:null};
 for(const key of ['runs','practices'])if(!Number.isSafeInteger(old[key])||old[key]<0)old[key]=0;
 for(const key of ['first','latest'])if(!old[key]||typeof old[key]!=='object'||Array.isArray(old[key]))old[key]=null;
 answer=answer&&typeof answer==='object'?answer:{};
 const result={correct:!!answer.correct,independent:!!answer.independent,assisted:!!answer.assisted,observed:Array.isArray(answer.observed)?answer.observed.filter(x=>typeof x==='string').slice(0,8):[],at:Date.now()};
 if(practice){old.practices++;old.practice=result;}else{old.runs++;if(!old.first)old.first=result;old.latest=result;}
 state.activities[activityId]=old;return true;
}
const harborRouteDone=(p,route)=>route.activities.every(a=>{const state=p.routeProgress&&p.routeProgress.version===1&&p.routeProgress.regions&&p.routeProgress.regions.harbor;return !!(state&&state.contentVersion===HARBOR_CONTENT.version&&state.activities&&state.activities[a.id]&&state.activities[a.id].latest&&state.activities[a.id].latest.correct);});
function harborMissingGoals(p,activity){
 const state=p.routeProgress?.version===1?p.routeProgress.regions?.harbor:null;
 const goals=new Set();if(state?.contentVersion===HARBOR_CONTENT.version)for(const r of HARBOR_CONTENT.routes)for(const a of r.activities)if(state.activities?.[a.id]?.latest?.correct)for(const g of a.goals)goals.add(g);
 return (activity.prerequisiteGoals||[]).filter(g=>!goals.has(g));
}
function harborCanPlay(p,activity){return harborEligible(p)&&harborMissingGoals(p,activity).length===0;}
function harborEntry(p){return harborEligible(p)?`<div class="harbor-entry"><span aria-hidden="true">⚓</span><div><b>بندر: راهت را انتخاب کن</b><p>اسکلهٔ ماهیگیری یا اسکلهٔ دزدان دریایی؟</p><button class="btn" type="button" data-harbor>دیدن راه‌های بندر</button></div></div>`:'';}
/* Difficulty follows content, never card position. Future data may name a tier. */
function harborDifficulty(route){
 const tiers={core:{id:'core',title:'آسان‌تر',symbol:'●'},challenge:{id:'challenge',title:'چالشی',symbol:'◆ ◆'},'very-hard':{id:'very-hard',title:'خیلی سخت',symbol:'◆ ◆ ◆'}};
 const key=route.difficulty.tier||(route.difficulty.concept>=3?'very-hard':route.difficulty.concept>=2?'challenge':'core');
 return tiers[key]||{id:'unknown',title:'سختی مشخص نشده',symbol:'؟'};
}
function harborDrawBranches(o){
 const map=o.querySelector('.harbor-choice-map'),svg=map.querySelector('.harbor-branches');
 const draw=()=>{
  if(!o.isConnected){observer.disconnect();return;}
  const box=map.getBoundingClientRect(),cards=[...map.querySelectorAll('[data-route]')].map(b=>b.getBoundingClientRect());
  const rows=[];for(const r of cards){let row=rows.find(x=>Math.abs(x.top-(r.top-box.top))<2);if(!row){row={top:r.top-box.top,cards:[]};rows.push(row);}row.cards.push(r);}
  const cx=box.width/2;let paths='',dots='';
  rows.forEach((row,i)=>{
   const rail=row.top-18;
   const stem=i===0?`M${cx} 9V${rail}`:`M${cx} 9H4V${rail}H${cx}`;
   paths+=`<path d="${stem}"/>`;
   for(const r of row.cards){const x=(r.left+r.right)/2-box.left;paths+=`<path d="M${cx} ${rail}H${x}V${row.top-3}"/>`;dots+=`<circle cx="${x}" cy="${row.top-3}" r="4"/>`;}
  });
  svg.setAttribute('viewBox',`0 0 ${box.width} ${box.height}`);svg.innerHTML=`<circle cx="${cx}" cy="9" r="6"/>${paths}${dots}`;
 };
 const observer=new ResizeObserver(draw);observer.observe(map);map.querySelectorAll('[data-route]').forEach(b=>observer.observe(b));requestAnimationFrame(draw);
}
function harborSelector(){
 const p=JP();if(!harborEligible(p))return;closeOv();
 const state=harborState(p);
 const cards=HARBOR_CONTENT.routes.map(route=>{
  const done=harborRouteDone(p,route),sel=state.routeId===route.id,tier=harborDifficulty(route);
  const count=route.activities.filter(a=>state.activities[a.id]?.latest?.correct).length;
  return `<button class="harbor-route tier-${tier.id} ${sel?'selected':''}" type="button" data-route="${esc(route.id)}" aria-pressed="${sel}"><span class="harbor-scene">${HARBOR_ROUTE_ICONS[route.environmentAssetId]||''}</span><b class="harbor-title">${esc(route.title)}</b><span class="harbor-difficulty"><span aria-hidden="true">${tier.symbol}</span> ${tier.title} · ${esc(route.difficulty.label)}</span><span class="harbor-summary">${esc(route.description)}</span><span class="harbor-selection ${sel?'is-selected':''}">${sel?'● راه انتخاب‌شده':'○ راه باز است'}</span><span class="harbor-completion">${done?'✓ فعالیت‌ها انجام شده‌اند':`${fa(count)} از ${fa(route.activities.length)} فعالیت انجام شده`}</span><span class="harbor-card-action">${done?'دوباره تمرین کن':'از این راه برو'} <span aria-hidden="true">←</span></span></button>`;
 }).join('');
 const o=jsheet(`<div class="harbor-selector" dir="rtl"><div class="shead"><h2>از کدام اسکله می‌روی؟</h2><button class="chip-btn" id="hclose" type="button">نقشه</button></div><p class="harbor-intro">راهت را انتخاب کن. هر وقت خواستی می‌توانی آن را عوض کنی.</p><div class="harbor-choice-map"><svg class="harbor-branches" aria-hidden="true" focusable="false"></svg><div class="harbor-routes">${cards}</div></div><p class="j-note">این راه‌ها برای تمرین قرقره‌اند. برای ادامهٔ سفر به نقشه برگرد.</p></div>`,"راه‌های بندر","#1F6F7F");
 o.querySelector('#hclose').onclick=()=>jmap({scroll:false});o.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{state.routeId=b.dataset.route;save();harborRouteSheet(b.dataset.route);});harborDrawBranches(o);o.querySelector('[data-route]')?.focus();
}
function harborRouteSheet(id){
 const p=JP(),route=harborRoute(id);if(!harborEligible(p)||!route)return;
 const state=harborState(p);
 const rows=route.activities.map((a,i)=>{const e=state.activities[a.id],done=!!(e&&e.latest&&e.latest.correct),available=harborCanPlay(p,a);const reason=harborMissingGoals(p,a).map(g=>HARBOR_CONTENT.goalTitles[g]).join(' و ');return `<div class="j-part ${done?'done':''}"><span class="ic">${fa(i+1)}</span><span class="tx"><span class="n">${esc(a.title)}</span><span>${done?'انجام شد؛ دوباره هم می‌توانی تمرین کنی':available?'ببین، امتحان کن، پاسخ بده':'🔒 اول '+esc(reason)+' را انجام بده'}</span></span><button class="btn" type="button" data-activity="${i}" ${available?'':'disabled'}>${done?'دوباره':'شروع'}</button></div>`;}).join('');
 const o=jsheet(`<div class="shead"><h2>${esc(route.title)}</h2><button class="chip-btn" id="hchange" type="button">تغییر راه</button></div>${rows}<p class="j-note">در این مدل، اصطکاک و وزن طناب و قرقره را در نظر نمی‌گیریم. این راه برای تمرین است.</p>`,route.title,"#1F6F7F");
 o.querySelector('#hchange').onclick=harborSelector;o.querySelectorAll('[data-activity]').forEach(b=>b.onclick=()=>harborPlay(id,+b.dataset.activity));o.querySelector('[data-activity]').focus();
}
function harborPlay(id,index,sameSpec,practice){
 const p=JP(),route=harborRoute(id),a=route&&route.activities[index];if(!harborEligible(p)||!a||!harborCanPlay(p,a))return;
 const previous=harborState(p).activities[a.id];practice=!!practice||!!(previous&&previous.latest&&previous.latest.correct);
 const spec=sameSpec||Object.assign(a.make(rng((Date.now()^hash(a.id))>>>0)),{activityId:a.id,goals:a.goals});
 const A=board('pulley',{mode:'level',backLabel:'بندر',unscored:true,help:harborHelp,title:a.title,sub:route.title+(practice?' · تمرین دوباره':''),land:1,stop:9,allowReplay:true,back:()=>harborRouteSheet(id),restart:()=>harborPlay(id,index,spec,!!(A.locked||practice))});
 $('#dots').innerHTML=dotsHtml(route.activities.length,index,route.activities.map(x=>harborState(p).activities[x.id]?.latest?.correct?2:null));$('#scr').textContent=practice?'تمرین؛ نتیجهٔ قبلی محفوظ است.':'بار و طناب را آزمایش کن.';
 A.done=pts=>{
  const ev=A.harborEvidence||{};harborRecord(p,id,a.id,{correct:pts>0&&!A.answerShown,independent:pts>0&&!A.assisted&&!A.answerShown&&ev.independent!==false&&A.tries===0&&A.trials===0,assisted:A.assisted||A.answerShown||ev.independent===false||A.tries>0||A.trials>0,observed:ev.observed||[]},practice);save();
  const n=A.nav('');btn(n,'بیا یک بار دیگر انجامش بدهیم','',()=>harborPlay(id,index,spec,true));
  if(index+1<route.activities.length)btn(n,'فعالیت بعد','go next',()=>harborPlay(id,index+1));else btn(n,'دیدن نتیجهٔ راه','go next',()=>harborResult(id));
  btn(n,'تغییر راه','',harborSelector);
 };
 if(window.__TEST||window.__JT)window.__T={spec,k:'pulley',i:index,harbor:true};mountHarborActivity(spec,A);window.scrollTo(0,0);
}
function harborResult(id){
 const p=JP(),route=harborRoute(id);if(!harborEligible(p)||!route)return;
 const done=harborRouteDone(p,route),state=harborState(p),first=route.activities.filter(a=>state.activities[a.id]?.first?.independent).length;
 const o=jsheet(`<h2>${done?'فعالیت‌های این راه انجام شد':'یک بار دیگر تمرین کنیم'}</h2><p>پاسخ مستقل در نخستین اجرا: ${fa(first)} از ${fa(route.activities.length)} فعالیت. تمرین پس از پاسخ جدا ثبت می‌شود.</p><p class="j-note">هر وقت خواستی دوباره تمرین کن. برای ادامهٔ سفر به نقشه برگرد.</p><div class="nav"><button class="btn" id="hag" type="button">تمرین دوباره</button><button class="btn" id="hother" type="button">راه دیگر</button><button class="btn go" id="hmap" type="button">نقشه</button></div>`,"نتیجهٔ بندر","#1F6F7F");
 o.querySelector('#hag').onclick=()=>harborRouteSheet(id);o.querySelector('#hother').onclick=harborSelector;o.querySelector('#hmap').onclick=()=>jmap({scroll:false});o.querySelector('#hmap').focus();
}

function harborHelp(){
 const o=jsheet('<h2>راهنمای قرقره</h2><p>قرقرهٔ ثابت بالا می‌ماند. سر آزاد طناب را پایین می‌کشی و بار بالا می‌رود.</p><p>در آرایش ثابت و متحرک، قرقرهٔ پایینی با بار حرکت می‌کند. با همان بار و ارتفاع، نیروی کمتری لازم است؛ طناب بیشتری می‌کشیم.</p><p>در این مدل، اصطکاک و وزن طناب و قرقره را در نظر نمی‌گیریم.</p><button class="btn" id="hhelpclose" type="button">برگشت به آزمایش</button>','راهنمای قرقره','#1F6F7F');o.querySelector('#hhelpclose').onclick=closeOv;o.querySelector('#hhelpclose').focus();
}
