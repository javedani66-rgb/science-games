const HARBOR_ROUTE_ICONS={"fishing-dock": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 240 128\" aria-hidden=\"true\" focusable=\"false\"><rect width=\"240\" height=\"128\" rx=\"14\" fill=\"#DFF1F2\"/><circle cx=\"204\" cy=\"23\" r=\"12\" fill=\"#FFE5A1\"/><path d=\"M0 89Q35 77 68 89T137 89T205 89T260 89V128H0Z\" fill=\"#86C4CC\"/><path d=\"M10 110q13-6 26 0m18 6q13-6 26 0m78-6q13-6 26 0m16 6q13-6 26 0\" stroke=\"#1F6F7F\" stroke-width=\"2\" fill=\"none\"/><g stroke=\"#3B2417\" stroke-width=\"3\" stroke-linejoin=\"round\" stroke-linecap=\"round\"><path d=\"M124 86h84l-12 17h-60Z\" fill=\"#F5C476\"/><path d=\"M170 86V56\" fill=\"none\"/><path d=\"M171 56l25 26h-25Z\" fill=\"#FFF8E8\"/><path d=\"M24 85V21h76v11\" fill=\"none\"/><circle cx=\"100\" cy=\"38\" r=\"7\" fill=\"#F7DCA5\"/><path d=\"M100 32v30\" fill=\"none\"/><path d=\"M82 62h34l-5 19H87Z\" fill=\"#E8B57E\"/><path d=\"M85 68h28m-22-5v16m9-16v16m9-16v16\" fill=\"none\" stroke-width=\"2\"/><path d=\"M52 76q12-12 26 0-14 12-26 0l-8-6v12Z\" fill=\"#9ED2D9\"/><circle cx=\"71\" cy=\"74\" r=\"2\" fill=\"#3B2417\" stroke=\"none\"/><path d=\"M8 86h99v10H8Z\" fill=\"#D5A26B\"/><path d=\"M24 96v25m62-25v25M8 91h99\" fill=\"none\"/></g></svg>", "pirate-dock": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 240 128\" aria-hidden=\"true\" focusable=\"false\"><rect width=\"240\" height=\"128\" rx=\"14\" fill=\"#DFF1F2\"/><circle cx=\"204\" cy=\"23\" r=\"12\" fill=\"#FFE5A1\"/><path d=\"M0 89Q35 77 68 89T137 89T205 89T260 89V128H0Z\" fill=\"#86C4CC\"/><path d=\"M10 110q13-6 26 0m18 6q13-6 26 0m78-6q13-6 26 0m16 6q13-6 26 0\" stroke=\"#1F6F7F\" stroke-width=\"2\" fill=\"none\"/><g stroke=\"#3B2417\" stroke-width=\"3\" stroke-linejoin=\"round\" stroke-linecap=\"round\"><path d=\"M116 83h110l-15 23h-80Z\" fill=\"#A9754C\"/><path d=\"M171 83V17\" fill=\"none\"/><path d=\"M172 21h34l-7 10 7 10h-34Z\" fill=\"#F2785C\"/><path d=\"m181 26 12 10m0-10-12 10\" stroke=\"#FFF8E8\"/><path d=\"M166 45l-24 33h24Zm11 0 25 33h-25Z\" fill=\"#FFF8E8\"/><path d=\"M34 85V26h61v9\" fill=\"none\"/><circle cx=\"95\" cy=\"41\" r=\"7\" fill=\"#F7DCA5\"/><path d=\"M95 35v23\" fill=\"none\"/><rect x=\"75\" y=\"58\" width=\"38\" height=\"24\" rx=\"3\" fill=\"#D5A26B\"/><path d=\"M75 67h38m-26-9v24m14-24v24\" fill=\"none\" stroke-width=\"2\"/><rect x=\"90\" y=\"66\" width=\"8\" height=\"7\" rx=\"1\" fill=\"#FFE5A1\"/><path d=\"M8 86h99v10H8Z\" fill=\"#D5A26B\"/><path d=\"M24 96v25m62-25v25M8 91h99\" fill=\"none\"/></g></svg>", "dragon-dock": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 240 128\" aria-hidden=\"true\" focusable=\"false\"><rect width=\"240\" height=\"128\" rx=\"14\" fill=\"#DFF1F2\"/><circle cx=\"204\" cy=\"23\" r=\"12\" fill=\"#FFE5A1\"/><path d=\"M0 89Q35 77 68 89T137 89T205 89T260 89V128H0Z\" fill=\"#86C4CC\"/><g stroke=\"#3B2417\" stroke-width=\"3\" stroke-linejoin=\"round\" stroke-linecap=\"round\"><path d=\"M140 90q-6-34 20-40 22-4 30 14l12 4-12 8q-4 14-22 14Z\" fill=\"#7CC48A\"/><path d=\"M150 52l4-12 6 10m8-8 4-11 5 12\" fill=\"none\"/><circle cx=\"177\" cy=\"62\" r=\"3\" fill=\"#3B2417\" stroke=\"none\"/><path d=\"M24 85V21h76v11\" fill=\"none\"/><circle cx=\"100\" cy=\"38\" r=\"7\" fill=\"#F7DCA5\"/><path d=\"M100 32v30\" fill=\"none\"/><rect x=\"78\" y=\"60\" width=\"34\" height=\"22\" rx=\"3\" fill=\"#D5A26B\"/><path d=\"M78 71h34m-23-11v22m12-22v22\" fill=\"none\" stroke-width=\"2\"/><path d=\"M8 86h99v10H8Z\" fill=\"#D5A26B\"/><path d=\"M24 96v25m62-25v25\" fill=\"none\"/></g></svg>"};
/* M07 harbor pilot routes and saved evidence. No Persian text here: ids point into harbor/strings.fa.json (B49/B50).
   Route evidence never fabricates legacy mission stars; the child never sees counts, stars or points of it (B4). */
/* Band comes from the grade only (B1, B14, D250): indexes of GRADES are دوم..ششم = 0..4. Grade 1 is not in GRADES, see docs/STATE.md. */
const harborBand=p=>{const g=p&&p.g;return g===0?"1-2":g===1||g===2?"3-4":g===3||g===4?"5-6":null;};
const harborEligible=p=>!!p&&harborBand(p)!==null;
/* A content-version change keeps the old activities under "legacy" (read only) and starts the new ones empty; nothing is wiped (B5, T8). */
function harborState(p){
 if(!p.routeProgress||p.routeProgress.version!==1||!p.routeProgress.regions||typeof p.routeProgress.regions!=='object'||Array.isArray(p.routeProgress.regions))p.routeProgress={version:1,regions:{}};
 const all=p.routeProgress.regions,h=all.harbor,shape=h&&typeof h==='object'&&!Array.isArray(h)&&h.activities&&typeof h.activities==='object'&&!Array.isArray(h.activities);
 if(!shape)all.harbor={contentVersion:HARBOR_CONTENT.version,routeId:null,activities:{}};
 else if(h.contentVersion!==HARBOR_CONTENT.version){
  const legacy=h.legacy&&typeof h.legacy==='object'&&!Array.isArray(h.legacy)?h.legacy:{};
  legacy['v'+(Number.isSafeInteger(h.contentVersion)?h.contentVersion:0)]=h.activities;
  all.harbor={contentVersion:HARBOR_CONTENT.version,routeId:typeof h.routeId==='string'?h.routeId:null,activities:{},legacy};
 }
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
 const result={correct:!!answer.correct,independent:!!answer.independent,assisted:!!answer.assisted,observed:Array.isArray(answer.observed)?answer.observed.filter(x=>typeof x==='string').slice(0,12):[],at:Date.now()};
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
function harborGoalTitle(goal,band){for(const r of HARBOR_CONTENT.routes)for(const a of r.activities)if(a.goals.includes(goal))return harborActTitle(a,band);return goal;}
function harborEntry(p){return harborEligible(p)?`<div class="harbor-entry"><span aria-hidden="true">⚓</span><div><b>${hs('harbor.ui.entry.title')}</b><p>${hs('harbor.ui.entry.text')}</p><button class="btn" type="button" data-harbor>${hs('harbor.ui.entry.btn')}</button></div></div>`:'';}
/* Difficulty follows content, never card position. Future data may name a tier. */
function harborDifficulty(route){
 const tiers={core:{id:'core',title:hs('harbor.ui.tier.core'),symbol:'●'},challenge:{id:'challenge',title:hs('harbor.ui.tier.challenge'),symbol:'◆ ◆'},'very-hard':{id:'very-hard',title:hs('harbor.ui.tier.very-hard'),symbol:'◆ ◆ ◆'}};
 const key=route.difficulty.tier||(route.difficulty.concept>=3?'very-hard':route.difficulty.concept>=2?'challenge':'core');
 return tiers[key]||{id:'unknown',title:hs('harbor.ui.tier.unknown'),symbol:'\u061F'};
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
  const marks=route.activities.map(a=>state.activities[a.id]?.latest?.correct?'✓':'○').join(' ');
  return `<button class="harbor-route tier-${tier.id} ${sel?'selected':''}" type="button" data-route="${esc(route.id)}" aria-pressed="${sel}"><span class="harbor-scene">${HARBOR_ROUTE_ICONS[route.environmentAssetId]||''}</span><b class="harbor-title">${esc(harborRouteText(route,'title'))}</b><span class="harbor-difficulty"><span aria-hidden="true">${tier.symbol}</span> ${tier.title} · ${esc(harborRouteText(route,'label'))}</span><span class="harbor-summary">${esc(harborRouteText(route,'desc'))}</span><span class="harbor-selection ${sel?'is-selected':''}">${sel?hs('harbor.ui.sel.chosen'):hs('harbor.ui.sel.open')}</span><span class="harbor-completion">${done?hs('harbor.ui.sel.done'):hs('harbor.ui.sel.missions')+' '+marks}</span><span class="harbor-card-action">${done?hs('harbor.ui.sel.again'):hs('harbor.ui.sel.go')} <span aria-hidden="true">←</span></span></button>`;
 }).join('');
 const o=jsheet(`<div class="harbor-selector" dir="rtl"><div class="shead"><h2>${hs('harbor.ui.sel.title')}</h2><button class="chip-btn" id="hclose" type="button">${hs('harbor.ui.sel.close')}</button></div><p class="harbor-intro">${hs('harbor.ui.sel.intro')}</p><div class="harbor-choice-map"><svg class="harbor-branches" aria-hidden="true" focusable="false"></svg><div class="harbor-routes">${cards}</div></div><p class="j-note">${hs('harbor.ui.sel.note')}</p></div>`,hs('harbor.ui.sel.label'),"#1F6F7F");
 o.querySelector('#hclose').onclick=()=>jmap({scroll:false});o.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{state.routeId=b.dataset.route;save();harborRouteSheet(b.dataset.route);});harborDrawBranches(o);o.querySelector('[data-route]')?.focus();
}
function harborRouteSheet(id){
 const p=JP(),route=harborRoute(id),band=harborBand(p);if(!harborEligible(p)||!route)return;
 const state=harborState(p);
 const rows=route.activities.map((a,i)=>{const e=state.activities[a.id],done=!!(e&&e.latest&&e.latest.correct),available=harborCanPlay(p,a);const reason=harborMissingGoals(p,a).map(g=>harborGoalTitle(g,band)).join(' + ');return `<div class="j-part ${done?'done':''}"><span class="ic">${fa(i+1)}</span><span class="tx"><span class="n">${esc(harborActTitle(a,band))}</span><span>${done?hs('harbor.ui.sheet.done'):available?hs('harbor.ui.sheet.ready'):hs('harbor.ui.sheet.locked',null,{t:esc(reason)})}</span></span><button class="btn" type="button" data-activity="${i}" ${available?'':'disabled'}>${done?hs('harbor.ui.sheet.btnAgain'):hs('harbor.ui.sheet.btnStart')}</button></div>`;}).join('');
 const o=jsheet(`<div class="shead"><h2>${esc(harborRouteText(route,'title'))}</h2><button class="chip-btn" id="hchange" type="button">${hs('harbor.ui.sheet.change')}</button></div><p class="j-note">${esc(harborRouteText(route,'story',band))}</p>${rows}<p class="j-note">${hs('harbor.ui.model')}</p>`,harborRouteText(route,'title'),"#1F6F7F");
 o.querySelector('#hchange').onclick=harborSelector;o.querySelectorAll('[data-activity]').forEach(b=>b.onclick=()=>harborPlay(id,+b.dataset.activity));(o.querySelector('[data-activity]:not([disabled])')||o.querySelector('[data-activity]')).focus();
}
function harborPlay(id,index,sameSpec,practice){
 const p=JP(),route=harborRoute(id),a=route&&route.activities[index],band=harborBand(p);if(!harborEligible(p)||!a||!harborCanPlay(p,a))return;
 const previous=harborState(p).activities[a.id];practice=!!practice||!!(previous&&previous.latest&&previous.latest.correct);
 const spec=sameSpec||Object.assign(a.make(band),{activityId:a.id,goals:a.goals});
 const A=board('pulley',{mode:'level',backLabel:hs('harbor.ui.backLabel'),unscored:true,help:()=>harborHelp(route,band),title:harborActTitle(a,band),sub:harborRouteText(route,'title')+(practice?hs('harbor.ui.practiceSuffix'):''),land:1,stop:9,allowReplay:true,back:()=>harborRouteSheet(id),restart:()=>harborPlay(id,index,spec,!!(A.locked||practice))});
 $('#dots').innerHTML=dotsHtml(route.activities.length,index,route.activities.map(x=>harborState(p).activities[x.id]?.latest?.correct?2:null));$('#scr').textContent=practice?hs('harbor.ui.scr.practice'):hs('harbor.ui.scr.normal');
 A.done=pts=>{
  const ev=A.harborEvidence||{};harborRecord(p,id,a.id,{correct:pts>0&&!A.answerShown,independent:pts>0&&!A.assisted&&!A.answerShown&&ev.independent!==false&&A.tries===0&&A.trials===0,assisted:A.assisted||A.answerShown||ev.independent===false||A.tries>0||A.trials>0,observed:ev.observed||[]},practice);save();
  const n=A.nav('');btn(n,hs('harbor.ui.btn.again'),'',()=>harborPlay(id,index,spec,true));
  if(index+1<route.activities.length)btn(n,hs('harbor.ui.btn.next'),'go next',()=>harborPlay(id,index+1));else btn(n,hs('harbor.ui.btn.result'),'go next',()=>harborResult(id));
  btn(n,hs('harbor.ui.btn.changeRoute'),'',harborSelector);
 };
 if(window.__TEST||window.__JT)window.__T={spec,k:'pulley',i:index,harbor:true};mountHarborActivity(spec,A);window.scrollTo(0,0);
}
/* The child sees no counts, stars or points here (B4); per-mission evidence stays in the saved state for the teacher page. */
/* Lesson card after the green challenge (B15, B16): only the direction of pull; nothing about force or moving wheels (those are the orange and red answers). Same backpack list as word cards (p.cards). */
const HARBOR_CARDS={"harbor.card.pull":{route:"green"}};
function harborCardIcon(){const L='stroke="#7A5634" stroke-width="3" stroke-linecap="round"';return `<svg viewBox="0 0 160 110" width="160" height="110" role="img" aria-hidden="true" style="display:block;margin:0 auto"><rect x="30" y="4" width="100" height="8" rx="3" fill="#8A5427"/><line x1="80" y1="12" x2="80" y2="18" ${L}/><circle cx="80" cy="34" r="16" fill="#F4F7FA" stroke="#34425E" stroke-width="4"/><line x1="64" y1="34" x2="64" y2="76" ${L}/><line x1="96" y1="34" x2="96" y2="64" ${L}/><rect x="48" y="76" width="32" height="26" rx="3" fill="#E0A45F" stroke="#94602D" stroke-width="2"/><path d="M96 66 V96 M88 88 L96 98 L104 88" fill="none" stroke="#D8452B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M40 92 V62 M32 70 L40 60 L48 70" fill="none" stroke="#22965A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>`;}
const harborCardTitle=w=>HARBOR_CARDS[w]?hs(w+".title"):w;
const harborCardText=(w,band)=>hs(w+".text",band);
function harborLessonCard(cardId,then,force){
 const p=JP();p.cards=p.cards||[];if(!force&&p.cards.includes(cardId)){then();return;}
 const band=harborBand(p),o=jsheet(`<span class="j-step" style="text-align:center">${hs(cardId+'.tag')}</span><div class="j-word"><span class="w">${hs(cardId+'.title')}</span>${harborCardIcon()}<p>${harborCardText(cardId,band)}</p></div><p class="j-note" style="text-align:center">${hs(cardId+'.note')}</p><button class="btn go j-wide" id="hcardgo" type="button">${hs(cardId+'.btn')}</button>`,hs(cardId+'.tag'),'#2F6BD0');
 o.querySelector('#hcardgo').onclick=()=>{if(!p.cards.includes(cardId)){p.cards.push(cardId);save();}closeOv();then();};o.querySelector('#hcardgo').focus();
}
function harborResult(id){
 const p=JP(),route=harborRoute(id);if(!harborEligible(p)||!route)return;
 const done=harborRouteDone(p,route);
 if(route.color==='green'&&done&&!(p.cards||[]).includes('harbor.card.pull')){harborLessonCard('harbor.card.pull',()=>harborResult(id));return;}
 const o=jsheet(`<h2>${done?hs('harbor.ui.res.done'):hs('harbor.ui.res.more')}</h2><p class="j-note">${hs('harbor.ui.res.note')}</p><div class="nav"><button class="btn" id="hag" type="button">${hs('harbor.ui.res.again')}</button><button class="btn" id="hother" type="button">${hs('harbor.ui.res.other')}</button><button class="btn go" id="hmap" type="button">${hs('harbor.ui.sel.close')}</button></div>`,hs('harbor.ui.res.label'),"#1F6F7F");
 o.querySelector('#hag').onclick=()=>harborRouteSheet(id);o.querySelector('#hother').onclick=harborSelector;o.querySelector('#hmap').onclick=()=>jmap({scroll:false});o.querySelector('#hmap').focus();
}
function harborHelp(route,band){
 const o=jsheet(`<h2>${hs('harbor.ui.help.title')}</h2><p>${hs('harbor.'+route.color+'.help',band)}</p><p>${hs('harbor.ui.model')}</p><button class="btn" id="hhelpclose" type="button">${hs('harbor.ui.help.close')}</button>`,hs('harbor.ui.help.title'),'#1F6F7F');o.querySelector('#hhelpclose').onclick=closeOv;o.querySelector('#hhelpclose').focus();
}
