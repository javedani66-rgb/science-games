/* ================= صفحه‌ها و جریان بازی ================= */
const ST={force:ST_force,fric:ST_fric,scale:ST_scale,lever:ST_lever,ramp:ST_ramp,pulley:ST_pulley,wheel:ST_wheel,wedge:ST_wedge,sort:ST_sort};
const ORDER=["force","scale","fric","lever","ramp","pulley","wheel","wedge","sort"];
const TIER=[{n:"آسان",c:"#22965A"},{n:"متوسط",c:"#D99412"},{n:"سخت",c:"#E4553A"},{n:"قهرمان",c:"#7A3FC8"}];
const KIDLAB={fric:"اندازهٔ هل را انتخاب کن و «هل بده!» را بزن. ببین روی کدام سطح جعبه دورتر می‌رود.",force:"کارت‌های نیرو را روی طناب بگذار و «برو!» را بزن. هر چیزی را که دوست داری امتحان کن.",scale:"روی کفه‌ها چیزهای مختلف بگذار و ببین کدام پایین می‌رود. دکمهٔ «نیروسنج و آب» را هم امتحان کن.",lever:"آجرها را روی الاکلنگ بگذار و ببین تخته چطور می‌چرخد.",ramp:"دایرهٔ زرد را جابه‌جا کن تا سطح درازتر یا کوتاه‌تر شود. بعد «بکش!» را بزن.",pulley:"یک قرقره انتخاب کن و طناب را پایین بکش.",wheel:"یک دسته انتخاب کن و آن را بچرخان.",wedge:"گوه را پایین بکش یا پیچ را بچرخان.",sort:"هر کارت را در جعبهٔ درست بینداز."};
const KIDINTRO={fric:"روی یخ لیز می‌خوریم، روی فرش نه. ببین جعبه کجا راحت‌تر سُر می‌خورد.",force:"هل دادن و کشیدن. ببین کدام طرف قوی‌تر است.",scale:"ترازو نشان می‌دهد کدام چیز سنگین‌تر است. نیروسنج نشان می‌دهد زمین یک چیز را چقدر می‌کشد.",lever:"الاکلنگ را صاف کن. چیزِ سنگین‌تر را نزدیک وسط (تکیه‌گاه) بگذار.",ramp:"با سطح شیب‌دار، جعبه را راحت‌تر بالا ببر.",pulley:"با قرقره، طناب را پایین بکش و بار را بالا ببر.",wheel:"دستهٔ چاه را بچرخان و سطل را بالا بیاور.",wedge:"با گوه چوب را بشکاف و پیچ را بچرخان تا در چوب برود.",sort:"هر وسیله را در جعبهٔ ماشین ساده‌اش بینداز."};
const TRACKS={a:{n:"سطح ۱",g:"دوم و سوم",c:"#22965A",d:"بدون عدد و فرمول. نگاه می‌کند، مقایسه می‌کند و می‌شمارد. دستورها کوتاه‌اند."},b:{n:"سطح ۲",g:"چهارم",c:"#D97706",d:"عددها را می‌بیند: نیرو به نیوتن، جرم به کیلوگرم و گرم. جمع، تفریق، ضرب و تقسیم ساده."},c:{n:"سطح ۳",g:"پنجم و ششم",c:"#7A3FC8",d:"مطابق علوم پنجم: عدد و نسبت. فرمول‌ها برای کنجکاوها، با دکمهٔ راهنما."},d:{n:"سطح ۴",g:"هفتم تا نهم",c:"#1B6E8F",d:"با فرمول و نمادهای علمی: گشتاور، مزیت مکانیکی و کار."}};
/* عبارت‌های ریاضیِ داخل متن فارسی از چپ به راست نمایش داده شوند */
function ltrMath(h){return h.replace(/(\(?[۰-۹0-9][۰-۹0-9٫/]*(?:\s*(?:[a-zA-Z]+\s*)?[×÷+−=≈<>]\s*[۰-۹0-9][۰-۹0-9٫/]*)+(?:\s*(?:N|J|m|kg|g)\b)?\)?)/g,m=>{let tail="";if(m.endsWith(")")&&!m.startsWith("(")){m=m.slice(0,-1);tail=")";}if(m.startsWith("(")&&!m.endsWith(")")){return "("+`<span dir="ltr" class="eqi">${m.slice(1)}</span>`+tail;}return `<span dir="ltr" class="eqi">${m}</span>`+tail;});}
function mixLevel(k,d0,id,title,desc){return{id,title,desc,gen:r=>Array.from({length:6},(_,i)=>ST[k].endless(r,d0+i*.2))};}
const CB=(id,tr)=>((S.cb||{})[(tr||S.track||"c")+":"+id])||0;
/* فهرست مرحله‌های هر ایستگاه برای هر سطح؛ هر مرحله شناسهٔ ثابت دارد (ستاره‌ها با شناسه ذخیره می‌شوند، نه با شماره) */
const LVC={};
function levelsFor(k,tr){const key=k+":"+tr;if(LVC[key])return LVC[key];const s=ST[k],cur=s.levels;let out;
  if(tr==="a")out=s.kid;
  else{const sel=ix=>ix.map(i=>cur[i]);
    if(tr==="b")out=[...(s.bLv?sel(s.bLv):[cur[0],cur[1],cur[2]]),mixLevel(k,2.6,k+".xb","همه با هم","چالش‌های گوناگون از همهٔ مرحله‌ها، کمی سخت‌تر.")];
    else out=[...(s.cLv?sel(s.cLv):[cur[1],cur[2],cur[3]]),mixLevel(k,5,k+".xc","قهرمان","چالش‌های سخت و تصادفی از همهٔ انواع.")];}
  out.forEach(chLevel);return LVC[key]=out;}
const levelsOf=k=>levelsFor(k,S.track||"c");
if(TESTMODE)migrateS(S);
/* شناسهٔ مرحله → {ایستگاه، مرحله} */
function lvById(id){const k=id.slice(0,id.indexOf("."));if(!ST[k])return null;for(const tr of ["a","b","c"]){const lv=levelsFor(k,tr).find(x=>x.id===id);if(lv)return{k,lv};}return null;}
const starsFor=(p,m)=>p>=m*.9?3:p>=m*.66?2:p>=m*.4?1:0;
function setC(k){document.documentElement.style.setProperty("--c",ST[k]?ST[k].c:"#3B6FD4");}

function home(){epoch++;closeOv();setC("scale");document.body.classList.remove("bdm");setLand(0);
  const tot=ORDER.reduce((a,k)=>a+starsOfSt(k),0);
  app.innerHTML=`<header class="hero"><h1>کارگاه ماشین‌های ساده</h1><p class="lead">از نیرو شروع کن، بعد ترازو، اهرم و بقیهٔ ماشین‌ها. هر ایستگاه یک آزمایشگاه آزاد دارد و چهار مرحله که هر کدام یک چیز تازه یاد می‌دهد.</p>
  <div class="toolbar">${TESTMODE?`<button class="chip-btn trackchip" id="tk" type="button">${S.track?`${TRACKS[S.track].n} (${TRACKS[S.track].g})`:"انتخاب پایه"}</button>`:`<button class="chip-btn trackchip" id="tk" type="button">→ نقشهٔ سفر</button>`}<span class="pill">${starSvg(true,20)}<b>${fa(tot)}</b> ستاره</span><button class="chip-btn" id="fm" type="button">${KID()?"قانون‌ها":"فرمول‌ها"}</button><button class="chip-btn" id="gl" type="button">واژه‌نامه</button></div></header>
  <div class="stations">${ORDER.map((k,i)=>{const s=ST[k],pg=PG(k),lvs=levelsOf(k),next=lvs.findIndex(l=>!LS(l.id));return `<button class="st" data-k="${k}" type="button" style="--c:${s.c}"><svg viewBox="0 20 640 360" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${s.art()}</svg><span class="stb"><span class="k">ایستگاه ${fa(i+1)}</span><span class="n">${s.name}</span><span class="s">${s.sub}</span><span class="m"><span>${next<0?"همهٔ مرحله‌ها تمام شد":next===0?"شروع کن":`مرحلهٔ ${fa(next+1)}`}</span><span class="minis">${starSvg(starsOfSt(k)>0,16)} ${fa(starsOfSt(k))} از ${fa((S.track?levelsOf(k).length:4)*3)}</span></span></span></button>`;}).join("")}</div>
  ${TESTMODE?`<footer class="foot"><span>ستاره‌ها روی همین دستگاه ذخیره می‌شوند.</span><button id="rs" type="button">پاک کردن همهٔ ستاره‌ها</button></footer>`:""}`;
  app.querySelectorAll(".st").forEach(b=>b.onclick=()=>hub(b.dataset.k));$("#tk").onclick=TESTMODE?chooseTrack:()=>jmap({});
  $("#fm").onclick=()=>openFormulas();$("#gl").onclick=openGloss;
  const rs=$("#rs");if(rs){let armed=false;rs.onclick=()=>{if(!armed){armed=true;rs.textContent="مطمئنی؟ دوباره بزن";setTimeout(()=>{armed=false;rs.textContent="پاک کردن همهٔ ستاره‌ها";},3000);return;}S.prog={};save();home();};}
  window.scrollTo(0,0);if(!S.track&&TESTMODE)chooseTrack();}
function chooseTrack(){const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">پایه‌ات را انتخاب کن</h2>${S.track?`<button class="chip-btn" id="cx" type="button">بستن</button>`:""}</div><p class="lead">بازی برای هر گروه سنی مرحله‌ها و متن‌های جدا دارد. ستاره‌های هر مسیر جدا ذخیره می‌شوند و هر وقت خواستی می‌توانی مسیر را عوض کنی.</p><div class="tracks">${Object.entries(TRACKS).map(([id,tr])=>`<button class="trk ${S.track===id?"sel":""}" data-t="${id}" type="button" style="--tc:${tr.c}"><span class="g">${tr.g}</span><span class="t">${tr.n}</span><span class="d">${tr.d}</span></button>`).join("")}</div></div>`,"انتخاب پایه");
  o.querySelectorAll("[data-t]").forEach(b=>b.onclick=()=>{S.track=b.dataset.t;save();applyNums();closeOv();home();});const cx=o.querySelector("#cx");if(cx)cx.onclick=closeOv;(o.querySelector(".trk.sel")||o.querySelector(".trk")).focus();}

function hub(k){epoch++;closeOv();setC(k);document.body.classList.remove("bdm");setLand(ST_LAND[k]);const s=ST[k],pg=PG(k);
  let h=`<div class="bar"><button class="chip-btn" id="bk" type="button">→ همهٔ ایستگاه‌ها</button><button class="chip-btn fill" id="df" type="button">تعریف و فیلم</button></div>
  <div class="hubhead"><h2>${s.name}</h2><p class="lead">${KID()?KIDINTRO[k]:s.intro}</p></div>
  <div class="modes"><button class="mode lab" id="lab" type="button"><span class="t">آزمایشگاه</span><span class="d">آزادانه امتحان کن. امتیاز و مرحله ندارد؛ فقط کشف کردن.</span></button></div>
  <div class="sect">مرحله‌ها · ${TRACKS[S.track||"c"].n} (${TRACKS[S.track||"c"].g}) · برای باز شدن مرحلهٔ بعد، دست‌کم یک ستاره بگیر</div><div class="modes">`;
  const lvs=levelsOf(k);lvs.forEach((lv,i)=>{const open=i===0||LS(lvs[i-1].id)>0,stn=LS(lv.id);h+=`<button class="mode ${open?"":"lock"}" data-l="${i+1}" type="button" ${open?"":"disabled"} style="--tc:${TIER[Math.min(3,i)].c}"><span class="tag">مرحلهٔ ${fa(i+1)}</span><span class="t">${open?"":LOCK+" "}${lv.title}</span><span class="d">${lv.desc}</span><span class="st3">${[1,2,3].map(j=>starSvg(j<=stn,18)).join("")}</span></button>`;});
  const eOpen=LS(lvs[1].id)>0;h+=`<button class="mode ${eOpen?"":"lock"}" id="end" type="button" ${eOpen?"":"disabled"} style="--tc:#1B2A41"><span class="tag">بی‌پایان</span><span class="t">${eOpen?"":LOCK+" "}چالش بی‌پایان</span><span class="d">${eOpen?"سه جان داری. هر جواب درست، چالش بعدی را سخت‌تر می‌کند.":"بعد از گرفتن ستارهٔ مرحلهٔ ۲ باز می‌شود."}</span><span class="st3" style="font-size:14px;font-weight:700">${pg.best?"بهترین رکورد: "+fa(pg.best):""}</span></button></div>
  <div><button class="chip-btn" id="fx" type="button">${KID()?"قانون این ایستگاه":"فرمول‌های این ایستگاه"}</button></div>`;
  app.innerHTML=h;$("#bk").onclick=home;$("#df").onclick=()=>openDef(k);$("#fx").onclick=()=>openFormulas(k);$("#lab").onclick=()=>playLab(k);
  app.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>playLevel(k,+b.dataset.l));if(eOpen)$("#end").onclick=()=>playEndless(k);window.scrollTo(0,0);}

function tgBtn(key,label){return `<button class="tg" type="button" data-tg="${key}" aria-pressed="${S[key]?"true":"false"}"><span class="sw"></span>${label}</button>`;}
/* ---------- سرزمین‌ها، کاراکتر و نمادها ---------- */
const LANDN=["کارگاه نجاری","کارگاه ساختمانی و بندر","کارخانهٔ اختراع"];
const ST_LAND={force:0,fric:0,scale:0,lever:1,ramp:1,wedge:1,wheel:1,pulley:1,sort:2};
function setLand(li){document.body.dataset.land=String((li||0)+1);}
const UIC={map:'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M3 6.5l6-2.5 6 2.5 6-2.5v13.5l-6 2.5-6-2.5-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg>',
 re:'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/><path d="M18.6 3.2v4.4h-4.4"/></svg>',
 q:'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" aria-hidden="true"><g transform="translate(24 0) scale(-1 1)"><path d="M8.6 8.4a3.5 3.5 0 1 1 5 3.2c-1 .5-1.6 1.2-1.6 2.3v.9"/><circle cx="12" cy="19.2" r=".6" fill="currentColor"/></g></svg>'};
const curPlayer=()=>(typeof JP==="function"&&JP())||null;
const charOf=p=>p&&p.t!=null?(p.t%8)+1:1;
function titleName(p,land){return (land===2?"مهندس":"اوستا")+(p?" "+esc2(p.name):"");}
const esc2=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function bustImg(p,mood,cls){const c=charOf(p),B=IMG.bust[c],m=B[mood]?mood:"happy",sh=p&&p.shirt||"";return `<img class="${cls||"bi"}" src="${B[m]}" data-c="${c}" data-m="${m}" data-sh="${sh}" alt="">`;}
function fullImg(p,c,sh){c=c||charOf(p);sh=sh!=null?sh:(p&&p.shirt||"");return `<img class="fi" src="${IMG.full[c]}" data-c="${c}" data-full="1" data-sh="${sh}" alt="">`;}
function tintAll(root){(root||document).querySelectorAll("img[data-sh]").forEach(im=>{const sh=im.dataset.sh;if(!sh)return;const c=im.dataset.c;const src=im.dataset.full?IMG.full[c]:IMG.bust[c][im.dataset.m],mask=im.dataset.full?IMG.mfull[c]:IMG.mbust[c][im.dataset.m];tintShirt(src,mask,sh).then(u=>{if(im.dataset.sh===sh)im.src=u;}).catch(()=>{});});}
function setMood(mood){const im=document.querySelector(".bd .who img");if(!im)return;const p=curPlayer(),c=charOf(p),B=IMG.bust[c];const m=B[mood]?mood:"happy";im.dataset.m=m;im.src=B[m];tintAll(im.parentNode);}
/* واژه‌های علمیِ متن، قابل لمس می‌شوند و کارت تعریف را باز می‌کنند */
const TERMLIST=(typeof QDEF!=="undefined"?Object.keys(QDEF):[]).sort((a,b)=>b.length-a.length);
function lvKey(){return S.track||"c";}
function qdef(t,lv){const d=QDEF[t];if(!d)return "";const order="abcd",i=order.indexOf(lv||lvKey());for(let j=i;j<4;j++)if(d[order[j]])return d[order[j]];for(let j=i;j>=0;j--)if(d[order[j]])return d[order[j]];return "";}
function linkTerms(el){if(!TERMLIST.length||!el)return;const seen=new Set();const walk=n=>{if(n.nodeType===3){let t=n.nodeValue;for(const w of TERMLIST){if(seen.has(w))continue;const i=t.indexOf(w);if(i<0)continue;const before=i>0?t[i-1]:" ",after=t[i+w.length]||" ";const nx=t[i+w.length+1]||" ";if(/[\u0600-\u06FF]/.test(before)&&before!=="\u200c")continue;if(/[\u0600-\u06FF]/.test(after)&&after!=="\u200c"&&!(after==="ی"&&!/[\u0600-\u06FF]/.test(nx)))continue;seen.add(w);const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+w.length);const sp=document.createElement("button");sp.type="button";sp.className="term";sp.dataset.term=w;r.surroundContents(sp);walk(n);return;}}else if(n.nodeType===1&&!n.classList.contains("term")&&n.tagName!=="BUTTON"&&n.tagName!=="svg"){[...n.childNodes].forEach(walk);}};[...el.childNodes].forEach(walk);
  el.querySelectorAll(".term").forEach(b=>b.onclick=e=>{e.stopPropagation();termCard(b.dataset.term);});}
function termCard(t){const o=overlay(`<div class="sheet tcard"><span class="tk">کارت واژه</span><h2>${t}</h2><p>${ltrMath(qdef(t))}</p><p class="j-note">این کارت در دفترچهٔ کوله‌پشتی‌ات هست.</p><button class="btn go" id="tcx" type="button">فهمیدم</button></div>`,"کارت واژه");const p=curPlayer();if(p){p.cards=p.cards||[];if(!p.cards.includes(t)){p.cards.push(t);save();}}o.querySelector("#tcx").onclick=closeOv;o.querySelector("#tcx").focus();}
/* ---------- حدس بزن ← ببین ← توضیح بده (POE) ----------
   وقتی هنوز قاعده‌ای یاد نداده‌ایم، پیش‌بینی فقط حدس است و امتیاز ندارد؛ امتیاز برای سؤالی است که دربارهٔ دیده‌هاست.
   g={prompt,opts,reveal(guessIndex,next),right}  s={prompt,opts,ans,ok,retry} */
function poe(A,g,s){A.prompt(g.prompt);const c=A.ctrl("");
  const m=mcq(c,g.opts,i=>{if(A.locked)return;m.disable();m.mark(i,"sel");A.fb(KID()?"حالا ببین چه می‌شود.":"حدس زدی. حالا ببین چه می‌شود.","info");later(350,()=>g.reveal(i,()=>ask(i)));});
  function ask(gi){A.prompt(s.prompt);const note=g.right==null?"":gi===g.right?(KID()?" حدست درست بود!":" حدست هم درست بود."):(KID()?" حدست چیز دیگری بود؛ حالا دیدی چه شد.":" حدست چیز دیگری بود؛ آزمایش جواب را نشان داد.");
    const c2=A.ctrl("");const m2=mcq(c2,s.opts,(j,bt)=>{if(A.locked)return;
      if(j===s.ans){m2.disable();m2.mark(j,"right");A.judge(true,{ok:s.ok+note});}
      else{m2.mark(j,"wrong");bt.disabled=true;A.judge(false,{retry:s.retry,final:s.ok});if(A.locked){m2.disable();m2.mark(s.ans,"right");}}});}}
/* ---------- صحنهٔ بازی: سربرگ، صحنه، قاب متن و یک دکمهٔ اصلی ---------- */
function board(k,head){epoch++;closeOv();if(typeof clearToasts==="function")clearToasts();setC(k);const s=ST[k],p=curPlayer();
  const land=head.land!=null?head.land:ST_LAND[k];setLand(land);document.body.classList.add("bdm");
  const chip=head.stop!=null?`<span class="sn" aria-label="منزل ${fa(head.stop+1)}">${fa(head.stop+1)}</span>`:"";
  app.innerHTML=`<section class="bd">
  <header class="bh"><button class="nb" id="bk" type="button" aria-label="${head.backLabel}">${head.backLabel==="نقشه"?UIC.map:""}<span>${head.backLabel}</span></button>
   <div class="tt"><small>${chip}${LANDN[land]}</small><b>${head.title||s.name}</b>${head.mode!=="lab"?`<div class="dots" id="dots"></div>`:`<div class="dots"><span class="lbl">آزمایشگاه</span></div>`}<span class="vh" id="scr"></span></div>
   <button class="hb" id="rst" type="button" aria-label="از نو">${UIC.re}</button><button class="hb" id="hlpb" type="button" aria-label="راهنما">${UIC.q}</button></header>
  <div class="bsc"><svg id="sc" viewBox="0 0 640 520" role="img" aria-label="صحنهٔ آزمایش"></svg></div>
  <div class="bp"><div class="who">${bustImg(p,"thinking")}<span class="nm">${titleName(p,land)}</span></div>
   <p class="prompt" id="pr"></p><div class="counter" id="ct" aria-live="polite"></div><div class="ctrl" id="cl"></div><div class="formula" id="fm"></div><p class="fb" id="fb" aria-live="polite"></p><div class="nav" id="nv"></div></div></section>`;
  tintAll(app);
  const svg=$("#sc");let fmHtml="",helpHtml="";
  const P0=makePainter(svg);const A={svg,P:P0,hint:d=>P0.hint(d),view:h=>{svg.setAttribute("viewBox",`0 0 640 ${h}`);},tries:0,locked:false,lab:head.mode==="lab",refresh:null,done:null,onLane:null,
    prompt:h=>{if(KID()&&head.mode==="lab")h=KIDLAB[k];const i=h.indexOf("<small>");let main=h,sub="";if(i>=0){main=h.slice(0,i);sub=h.slice(i+7).replace("</small>","");}const pr=$("#pr");pr.innerHTML=ltrMath(main);helpHtml=sub&&!KID()?ltrMath(sub):"";linkTerms(pr);$("#hlpb").classList.toggle("has",!!helpHtml);},
    counter:h=>{const e=$("#ct");if(e)e.innerHTML=h||"";},
    formula:h=>{fmHtml=h||"";const e=$("#fm");if(e)e.innerHTML=S.formula?fmHtml:"";},
    ctrl:h=>{const c=$("#cl");c.innerHTML=h||"";return c;},fb:(m,c)=>{const e=$("#fb");if(!e)return;e.innerHTML=ltrMath(m||"");e.className="fb "+(c||"");if(m)later(80,revealFb);if(c==="ok")setMood("happy");else if(c==="no")setMood("oops");},
    nav:h=>{const n=$("#nv");n.innerHTML=h||"";return n;},
    /* آزمایش آزاد: وقتی بچه با امتحان کردن جواب را پیدا می‌کند (مثلاً جرمِ نامعلوم)، امتحانِ ناموفق فرصت را کم نمی‌کند */
    trials:0,trial(ok,m){if(A.locked||A.lab)return ok;if(KID()&&m.k)m=Object.assign({},m,m.k);if(ok)return A.judge(true,Object.assign({},m,{pts:A.trials<3?2:1,k:null,act:true}));
      A.trials++;A.fb(`${m.retry||""}${A.trials>=2&&m.more?" "+m.more:""} <b>${voice("retry")}</b>`,"info");
      /* نردبان راهنما: بعد از سه امتحانِ ناموفق، «نشانم بده» (جواب نشان داده می‌شود، ۱ امتیاز) تا بچه گیر نکند */
      if(A.trials>=3&&m.final&&!$("#showme")){const n=$("#nv");n.insertAdjacentHTML("beforeend",`<button class="btn" id="showme" type="button">نشانم بده</button>`);
        $("#showme").onclick=()=>{if(A.locked)return;A.locked=true;if(m.show)m.show();A.fb(m.final,"info");if(A.done)A.done(1);};}
      return false;},
    judge(ok,m){if(A.locked||A.lab)return ok;if(KID()&&m.k)m=Object.assign({},m,m.k);
      if(ok){const pts=m.pts!=null?m.pts:(A.tries===0?2:1);A.locked=true;A.fb(`${voice(pts===2?(A.trials?"okTries":m.act?"okDo":"okSay"):"okLate")} ${m.ok||""} <span style="white-space:nowrap">(+${fa(pts)} امتیاز)</span>`,"ok");if(A.done)A.done(pts);return true;}
      A.tries++;if(A.tries<2){A.fb(KID()?`${voice("wrong")} ${m.retry||""}`:`نه هنوز. ${m.retry||""} یک فرصت دیگر داری.`,"no");$("#hlpb").classList.add("nudge");return false;}
      A.locked=true;A.fb(`${m.final||""}`,"no");if(A.done)A.done(0);return false;}};
  $("#bk").onclick=head.back;
  $("#rst").onclick=()=>{if(A.locked&&!A.lab){jtoast2("این چالش تمام شده؛ دکمهٔ پایین را بزن.");return;}if(head.restart)head.restart();};
  $("#hlpb").onclick=()=>helpSheet(k,helpHtml,()=>{A.formula(fmHtml);if(A.refresh)A.refresh();});
  return A;}
function revealFb(){const e=$("#fb"),bp=document.querySelector(".bp");if(!e||!bp||!e.textContent.trim())return;bp.scrollTop=bp.scrollHeight;}
function jtoast2(t){if(typeof jtoast==="function")jtoast(t);}
function helpSheet(k,helpHtml,onToggle){const s=ST[k],D=DEFS[k],terms=(typeof QTERMS!=="undefined"?[...new Set(Object.values(QTERMS[lvKey()]||{}).flat())]:[]).filter(t=>D&&D.paras.join(" ").includes(t)).slice(0,6);
  const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">راهنما</h2><button class="chip-btn" id="cx" type="button">بستن</button></div>
   ${helpHtml?`<p class="hlp">${helpHtml}</p>`:""}
   ${terms.length?`<div class="sect">واژه‌های این ایستگاه</div><div class="tchips">${terms.map(t=>`<button type="button" class="term" data-term="${t}">${t}</button>`).join("")}</div>`:""}
   <button class="btn" id="hdf" type="button">تعریف‌ها و فیلم‌های «${s.name}»</button>
   ${KID()?"":`<div class="sect">نمایش</div><div class="toggles">${tgBtn("forces","فلش‌های نیرو")}${tgBtn("nums","عددها")}${tgBtn("formula",S.track==="c"?"فرمول‌ها (برای کنجکاوها)":"فرمول‌ها")}</div>`}</div>`,"راهنما");
  o.querySelector("#cx").onclick=closeOv;o.querySelector("#hdf").onclick=()=>openDef(k);o.querySelectorAll(".term").forEach(b=>b.onclick=()=>termCard(b.dataset.term));
  o.querySelectorAll("[data-tg]").forEach(b=>b.onclick=()=>{const key=b.dataset.tg;S[key]=!S[key];save();applyNums();b.setAttribute("aria-pressed",S[key]?"true":"false");onToggle();});o.querySelector("#cx").focus();}

function playLab(k,ctx){const go=()=>{const A=board(k,Object.assign({mode:"lab",backLabel:"ایستگاه",sub:"آزمایشگاه",back:()=>hub(k),restart:go},ctx||{}));ST[k].lab(A);};go();window.scrollTo(0,0);}
function dotsHtml(n,i,res){return Array.from({length:n},(_,j)=>`<i class="${res[j]!=null?"p"+res[j]:j===i?"cur":""}" title="چالش ${fa(j+1)}"></i>`).join("");}
function playLevel(k,L,ctx){const s=ST[k],LV=levelsOf(k),lv=LV[L-1];const r=rng((Date.now()^hash(k+L))>>>0);const specs=ctx&&ctx.resume?ctx.resume.specs:lv.gen(r);const res=ctx&&ctx.resume?ctx.resume.res.slice():[];let i=ctx&&ctx.resume?ctx.resume.i:0;
  const keep=()=>{if(ctx&&ctx.keep)ctx.keep({specs,res,i});};keep();
  function show(){const A=board(k,{mode:"level",backLabel:ctx?"نقشه":"ایستگاه",sub:ctx?ctx.sub:`مرحلهٔ ${fa(L)}: ${lv.title}`,title:ctx&&ctx.title,stop:ctx?ctx.stop:null,back:ctx?()=>{keep();ctx.back();}:()=>hub(k),restart:()=>show()});
    const upd=()=>{$("#dots").innerHTML=dotsHtml(specs.length,i,res);$("#scr").innerHTML=`چالش ${fa(i+1)} از ${fa(specs.length)} · امتیاز: ${fa(res.reduce((a,b)=>a+(b||0),0))} از ${fa(specs.length*2)}`;};upd();
    A.done=pts=>{res[i]=pts;upd();const cid=specs[i]&&specs[i].cid;if(cid){if(!S.cb)S.cb={};const kk=(S.track||"c")+":"+cid;if(pts>(S.cb[kk]||0))S.cb[kk]=pts;save();}if(ctx&&ctx.keep)ctx.keep({specs,res,i:i+1<specs.length?i+1:i,done:i+1>=specs.length});const n=A.nav("");const b=btn(n,i+1<specs.length?"چالشِ بعد":"دیدن نتیجه","go next",()=>{i++;if(i<specs.length){show();}else finish();});later(60,()=>{revealFb();b.focus({preventScroll:true});});};
    if(window.__TEST||window.__JT)window.__T={spec:specs[i],MASS,LV_MASS,k,i};s.mount(specs[i],A);}
  function finish(){const pts=res.reduce((a,b)=>a+b,0),max=specs.length*2,stars=starsFor(pts,max);setLS(lv.id,stars);save();
    if(ctx){ctx.finish(stars,pts,max);return;}
    const nextOpen=L<LV.length&&LS(lv.id)>0;
    const o=overlay(`<div class="sheet res"><h2>${stars===3?"عالی بود!":stars===2?"آفرین!":stars===1?"خوب بود!":"دوباره امتحان کن"}</h2><div class="bigst">${[1,2,3].map(j=>`<span style="--d:${j*.18}s">${starSvg(j<=stars,52)}</span>`).join("")}</div><p><b>${fa(pts)}</b> امتیاز از ${fa(max)}</p><p class="lead">${stars===0?"برای باز شدن مرحلهٔ بعد، دست‌کم یک ستاره لازم است. تعریف‌ها را بخوان و دوباره بازی کن.":stars<3?"برای سه ستاره، بیشتر چالش‌ها را در بار اول درست جواب بده.":"همهٔ چالش‌ها را عالی حل کردی."}</p><div class="nav" style="justify-content:center">${nextOpen?`<button class="btn go" id="rn" type="button">مرحلهٔ بعد</button>`:""}<button class="btn" id="rr" type="button">دوباره</button><button class="btn" id="rh" type="button">ایستگاه</button></div></div>`,"نتیجهٔ مرحله",s.c);
    if(nextOpen)o.querySelector("#rn").onclick=()=>playLevel(k,L+1);o.querySelector("#rr").onclick=()=>playLevel(k,L);o.querySelector("#rh").onclick=()=>hub(k);(o.querySelector("#rn")||o.querySelector("#rr")).focus();if(stars>=2)confetti();}
  show();window.scrollTo(0,0);}
function playEndless(k,ctx){const s=ST[k];const r=rng((Date.now()^hash(k+"e"))>>>0);let lives=3,d=1,score=0,count=0,right=0;
  let sp=null;function show(same){const A=board(k,{mode:"endless",backLabel:ctx?"نقشه":"ایستگاه",sub:ctx?ctx.sub:"چالش بی‌پایان",title:ctx&&ctx.title,stop:ctx?ctx.stop:null,back:ctx?ctx.back:()=>hub(k),restart:()=>show(true)});
    const upd=()=>{$("#dots").innerHTML=`<span class="hearts">${[0,1,2].map(j=>heart(j<lives)).join("")}</span>`;$("#scr").innerHTML=ctx?`جواب درست: ${fa(right)} از ${fa(ctx.goal)}`:`چالش ${fa(count+1)} · امتیاز: ${fa(score)} · سختی: ${fa(Math.floor(d))}`;};upd();
    A.done=pts=>{count++;if(pts===0)lives--;else{score+=pts;d+=.4;right++;}upd();if(ctx&&right>=ctx.goal){later(700,()=>ctx.win());return;}const n=A.nav("");const b=btn(n,lives>0?"چالشِ بعد":"پایان بازی","go next",()=>{if(lives>0){show();}else finish();});later(60,()=>{revealFb();b.focus({preventScroll:true});});};
    if(!same||!sp)sp=s.endless(r,KID()?Math.min(d,1.9):d);if(window.__TEST||window.__JT)window.__T={spec:sp,MASS,LV_MASS,k,d};s.mount(sp,A);}
  function finish(){const pg=PG(k),rec=score>pg.best;if(rec)pg.best=score;save();if(ctx){ctx.lose(right);return;}
    const o=overlay(`<div class="sheet res"><h2>${rec?"رکورد تازه!":"بازی تمام شد"}</h2><p><b>${fa(score)}</b> امتیاز در ${fa(count)} چالش</p><p class="lead">بهترین رکورد تو: ${fa(pg.best)}</p><div class="nav" style="justify-content:center"><button class="btn go" id="ra" type="button">دوباره</button><button class="btn" id="rh" type="button">ایستگاه</button></div></div>`,"پایان چالش بی‌پایان",s.c);
    o.querySelector("#ra").onclick=()=>playEndless(k);o.querySelector("#rh").onclick=()=>hub(k);o.querySelector("#ra").focus();if(rec)confetti();}
  show();window.scrollTo(0,0);}

function openDef(k){const s=ST[k],D=DEFS[k];
  const o=overlay(`<div class="sheet"><div class="shead"><h2>${s.name}</h2><button class="chip-btn" id="cx" type="button">بستن</button></div><svg viewBox="0 20 640 360" preserveAspectRatio="xMidYMid slice" style="width:100%;height:auto;border-radius:16px;display:block;aspect-ratio:16/9" aria-hidden="true">${s.art()}</svg>${D.paras.map(p=>`<p>${p}</p>`).join("")}<div class="rem">یادت باشد: ${D.rule}</div><div class="sect">نمونه‌ها در زندگی</div><div class="ex">${D.ex.map(e=>`<span>${e}</span>`).join("")}</div><div class="sect">${KID()?"قانون":"فرمول‌ها"}</div><div class="fcards">${FORMULAS.filter(f=>f.k===k).map(fcard).join("")||"<p class='lead'>این ایستگاه فرمول ندارد.</p>"}</div><div class="sect">فیلم‌ها و شبیه‌سازها</div><div class="vids">${D.vids.map(id=>{const v=V[id];return `<a href="${v[1]}" target="_blank" rel="noopener"><svg class="play-ic" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="${s.c}"/><path d="M14 11 L24 17 L14 23Z" fill="#fff"/></svg><span>${v[0]}<small>${v[2]}</small></span></a>`;}).join("")}</div><p class="lead">فیلم‌های آپارات بدون فیلترشکن باز می‌شوند.</p></div>`,"تعریف "+s.name,s.c);
  o.querySelector("#cx").onclick=closeOv;o.querySelector("#cx").focus();}
function fcard(f){if(KID())return f.rule?`<div class="fcard" style="--c:${ST[f.k].c}"><span class="gr">${ST[f.k].name}</span><h3>${f.t}</h3><div class="exm" style="font-size:18px;font-weight:700">${f.rule}</div></div>`:"";return `<div class="fcard" style="--c:${ST[f.k].c}"><span class="gr">${ST[f.k].name} · ${f.g==="b"?"از پایهٔ چهارم":"هفتم تا نهم، و پنجم و ششمِ کنجکاو"}</span><h3>${f.t}</h3><div class="eq"><span class="eqx" dir="ltr">${f.eq()}</span></div><div class="lg" style="justify-content:center">${f.lg().map(([s,m])=>`<span class="lgi"><span dir="ltr">${s}</span>: ${m}</span>`).join("")}</div><div class="exm">مثال: ${f.ex} <span class="eqx" dir="ltr" style="font-size:16px">${f.exq()}</span></div></div>`;}
function openFormulas(k){const list=k?FORMULAS.filter(f=>f.k===k).concat(FORMULAS.filter(f=>f.k!==k)):FORMULAS;
  const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">${KID()?"قانون‌ها":"فرمول‌ها"}</h2><button class="chip-btn" id="cx" type="button">بستن</button></div><p class="lead">${KID()?"قانون هر ماشین ساده در یک جمله.":"هر فرمول با نمادهای علمی و یک مثال حل‌شده. فرمول‌ها از چپ به راست خوانده می‌شوند."}</p><div class="fcards">${list.map(fcard).join("")}</div></div>`,"فرمول‌ها",k?ST[k].c:null);
  o.querySelector("#cx").onclick=closeOv;o.querySelector("#cx").focus();}
function openGloss(){const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">واژه‌نامه</h2><button class="chip-btn" id="cx" type="button">بستن</button></div><dl class="gl">${GLOSS.map(([t,d])=>`<div><dt>${t}</dt><dd>${d}</dd></div>`).join("")}</dl></div>`,"واژه‌نامه");o.querySelector("#cx").onclick=closeOv;o.querySelector("#cx").focus();}

