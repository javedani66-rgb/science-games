const HARBOR_ROUTE_ICONS={"fishing-dock": "<svg aria-hidden=\"true\" xmlns=\"http://www.w3.org/2000/svg\" width=\"64\" height=\"64\" viewBox=\"0 0 64 64\" role=\"img\" aria-labelledby=\"title\"><title id=\"title\">Fishing dock</title><g stroke=\"#3B2417\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 44h48v7H8z\" fill=\"#C78E56\"/><path d=\"M15 51v7m34-7v7M10 38q7 5 14 0t14 0t16 0\" fill=\"none\" stroke=\"#1F6F7F\"/><path d=\"M15 43V13q24 0 30 13v5\" fill=\"none\"/><path d=\"M38 32q-8-8-15 0 7 8 15 0l6-5v10Z\" fill=\"#9ED2D9\"/><circle cx=\"29\" cy=\"31\" r=\"1\" fill=\"#3B2417\" stroke=\"none\"/></g></svg>\n", "pirate-dock": "<svg aria-hidden=\"true\" xmlns=\"http://www.w3.org/2000/svg\" width=\"64\" height=\"64\" viewBox=\"0 0 64 64\" role=\"img\" aria-labelledby=\"title\"><title id=\"title\">Pirate dock</title><g stroke=\"#3B2417\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 44h48v7H8z\" fill=\"#C78E56\"/><path d=\"M15 51v7m34-7v7M10 38q7 5 14 0t14 0t16 0\" fill=\"none\" stroke=\"#1F6F7F\"/><path d=\"M20 43V8\" fill=\"none\"/><path d=\"M20 11h31l-7 10 7 10H20Z\" fill=\"#F2785C\"/><path d=\"m30 16 9 10m0-10-9 10\" fill=\"none\"/><circle cx=\"34.5\" cy=\"21\" r=\"3.5\" fill=\"#FFF8E8\"/></g></svg>\n"};
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
function harborCanPlay(p,activity){
 const state=p.routeProgress?.version===1?p.routeProgress.regions?.harbor:null;
 const goals=new Set();if(state?.contentVersion===HARBOR_CONTENT.version)for(const r of HARBOR_CONTENT.routes)for(const a of r.activities)if(state.activities?.[a.id]?.latest?.correct)for(const g of a.goals)goals.add(g);
 return harborEligible(p)&&(activity.prerequisiteGoals||[]).every(g=>goals.has(g));
}
function harborEntry(p){return harborEligible(p)?`<div class="harbor-entry"><span aria-hidden="true">⚓</span><div><b>بندر: راهت را انتخاب کن</b><p>اسکلهٔ ماهیگیری یا اسکلهٔ دزدان دریایی؟</p><button class="btn" type="button" data-harbor>دیدن راه‌های بندر</button></div></div>`:'';}
function harborSelector(){
 const p=JP();if(!harborEligible(p))return;closeOv();
 const state=harborState(p);
 const cards=HARBOR_CONTENT.routes.map(route=>{const done=harborRouteDone(p,route),sel=state.routeId===route.id;return `<button class="harbor-route ${sel?'selected':''}" type="button" data-route="${esc(route.id)}" aria-pressed="${sel}">${HARBOR_ROUTE_ICONS[route.environmentAssetId]||''}<b>${esc(route.title)}</b><span class="harbor-difficulty ${route.difficulty.concept>1?'hard':''}">${route.difficulty.concept>1?'⚑ ':''}${esc(route.difficulty.label)}</span><span>${esc(route.description)}</span><span>${done?'✓ فعالیت‌ها انجام شده‌اند':sel?'این راه را انتخاب کرده‌ای':'این راه را انتخاب کن'}</span></button>`;}).join('');
 const o=jsheet(`<div class="shead"><h2>کدام راهِ بندر را می‌روی؟</h2><button class="chip-btn" id="hclose" type="button">نقشه</button></div><p>در هر دو راه، حرکت طناب و بار را می‌بینی و آرایش مناسب را پیدا می‌کنی. هر وقت خواستی می‌توانی راهت را عوض کنی.</p><div class="harbor-fork" aria-hidden="true">⚓<span>↓</span></div><div class="harbor-routes">${cards}</div><p class="j-note">این راه‌ها برای تمرین قرقره‌اند. می‌توانی هر دو را امتحان کنی و به نقشه برگردی.</p>`,"راه‌های بندر","#1F6F7F");
 o.querySelector('#hclose').onclick=()=>jmap({scroll:false});o.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{state.routeId=b.dataset.route;save();harborRouteSheet(b.dataset.route);});o.querySelector('[data-route]').focus();
}
function harborRouteSheet(id){
 const p=JP(),route=harborRoute(id);if(!harborEligible(p)||!route)return;
 const state=harborState(p);
 const rows=route.activities.map((a,i)=>{const e=state.activities[a.id],done=!!(e&&e.latest&&e.latest.correct);return `<div class="j-part ${done?'done':''}"><span class="ic">${fa(i+1)}</span><span class="tx"><span class="n">${esc(a.title)}</span><span>${done?'انجام شد؛ دوباره هم می‌توانی تمرین کنی':'ببین، امتحان کن، پاسخ بده'}</span></span><button class="btn" type="button" data-activity="${i}" ${harborCanPlay(p,a)?'':'disabled'}>${done?'دوباره':'شروع'}</button></div>`;}).join('');
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
