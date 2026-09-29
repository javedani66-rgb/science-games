/* ================= صفحه‌ها و جریان بازی ================= */
const ST={force:ST_force,scale:ST_scale,lever:ST_lever,ramp:ST_ramp,pulley:ST_pulley,wheel:ST_wheel,wedge:ST_wedge,sort:ST_sort};
const ORDER=["force","scale","lever","ramp","pulley","wheel","wedge","sort"];
const TIER=[{n:"آسان",c:"#22965A"},{n:"متوسط",c:"#D99412"},{n:"سخت",c:"#E4553A"},{n:"قهرمان",c:"#7A3FC8"}];
const KIDLAB={force:"هر چه دوست داری امتحان کن: کشش‌ها را روی طناب بکش و «برو!» را بزن.",scale:"روی کفه‌ها چیز بگذار و ببین کدام پایین می‌رود. دکمهٔ «نیروسنج و آب» را هم امتحان کن.",lever:"آجرها را روی الاکلنگ بکش و پایه‌ها را بردار.",ramp:"دایرهٔ زرد را بکش تا سطح درازتر یا کوتاه‌تر شود. بعد «بکش!» را بزن.",pulley:"قرقره انتخاب کن و طناب را پایین بکش.",wheel:"دسته انتخاب کن و آن را بچرخان.",wedge:"گوه را پایین بکش یا پیچ را بچرخان.",sort:"هر کارت را در جعبهٔ درست بینداز."};
const KIDINTRO={force:"هل دادن و کشیدن. ببین کدام طرف قوی‌تر است.",scale:"ترازو نشان می‌دهد کدام چیز سنگین‌تر است. نیروسنج نشان می‌دهد زمین یک چیز را چقدر می‌کشد.",lever:"الاکلنگ را صاف کن. سنگین‌تر نزدیک وسط (تکیه‌گاه) بنشیند.",ramp:"با سطح شیب‌دار، جعبه را راحت‌تر بالا ببر.",pulley:"با قرقره، طناب را پایین بکش و بار را بالا ببر.",wheel:"دستهٔ چاه را بچرخان و سطل را بالا بیاور.",wedge:"با گوه چوب را بشکاف و پیچ را در چوب بچرخان.",sort:"هر وسیله را در جعبهٔ ماشین ساده‌اش بینداز."};
const TRACKS={a:{n:"کاوشگر",g:"دوم و سوم",c:"#22965A",d:"بدون عدد و فرمول. نگاه می‌کند، مقایسه می‌کند و می‌شمارد. دستورها کوتاه‌اند."},b:{n:"سازنده",g:"چهارم",c:"#D97706",d:"عددها را می‌بیند: نیرو به نیوتن، جرم به کیلوگرم و گرم. جمع و تفریق و حساب‌های ساده."},c:{n:"مهندس",g:"پنجم و ششم",c:"#7A3FC8",d:"با فرمول و نمادهای علمی. حساب، طراحی و چالش‌های سخت‌تر."}};
/* عبارت‌های ریاضیِ داخل متن فارسی از چپ به راست نمایش داده شوند */
function ltrMath(h){return h.replace(/(\(?[۰-۹0-9][۰-۹0-9٫/]*(?:\s*(?:[a-zA-Z]+\s*)?[×÷+−=≈<>]\s*[۰-۹0-9][۰-۹0-9٫/]*)+(?:\s*(?:N|J|m|kg|g)\b)?\)?)/g,m=>{let tail="";if(m.endsWith(")")&&!m.startsWith("(")){m=m.slice(0,-1);tail=")";}if(m.startsWith("(")&&!m.endsWith(")")){return "("+`<span dir="ltr" class="eqi">${m.slice(1)}</span>`+tail;}return `<span dir="ltr" class="eqi">${m}</span>`+tail;});}
function mixLevel(k,d0,title,desc){return{title,desc,gen:r=>Array.from({length:6},(_,i)=>ST[k].endless(r,d0+i*.2))};}
function levelsOf(k){const s=ST[k],cur=s.levels;if(S.track==="a")return s.kid;
  const sel=ix=>ix.map(i=>cur[i]);
  if(S.track==="b")return[...(s.bLv?sel(s.bLv):[cur[0],cur[1],cur[2]]),mixLevel(k,2.6,"همه با هم","چالش‌های گوناگون از همهٔ مرحله‌ها، کمی سخت‌تر.")];
  return[...(s.cLv?sel(s.cLv):[cur[1],cur[2],cur[3]]),mixLevel(k,5,"قهرمان","چالش‌های سخت و تصادفی از همهٔ انواع.")];}
const starsFor=(p,m)=>p>=m*.9?3:p>=m*.66?2:p>=m*.4?1:0;
function setC(k){document.documentElement.style.setProperty("--c",ST[k]?ST[k].c:"#3B6FD4");}

function home(){epoch++;closeOv();setC("scale");
  const tot=ORDER.reduce((a,k)=>a+starsOfSt(k),0);
  app.innerHTML=`<header class="hero"><h1>کارگاه ماشین‌های ساده</h1><p class="lead">از نیرو شروع کن، بعد ترازو، اهرم و بقیهٔ ماشین‌ها. هر ایستگاه یک آزمایشگاه آزاد دارد و چهار مرحله که هر کدام یک چیز تازه یاد می‌دهد.</p>
  <div class="toolbar">${TESTMODE?`<button class="chip-btn trackchip" id="tk" type="button">${S.track?`مسیر: ${TRACKS[S.track].n} (${TRACKS[S.track].g})`:"انتخاب پایه"}</button>`:`<button class="chip-btn trackchip" id="tk" type="button">→ نقشهٔ سفر</button>`}<span class="pill">${starSvg(true,20)}<b>${fa(tot)}</b> ستاره</span><button class="chip-btn" id="fm" type="button">${KID()?"قانون‌ها":"فرمول‌ها"}</button><button class="chip-btn" id="gl" type="button">واژه‌نامه</button></div></header>
  <div class="stations">${ORDER.map((k,i)=>{const s=ST[k],pg=PG(k),next=pg.lv.findIndex(v=>!v);return `<button class="st" data-k="${k}" type="button" style="--c:${s.c}"><svg viewBox="0 20 640 360" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${s.art()}</svg><span class="stb"><span class="k">ایستگاه ${fa(i+1)}</span><span class="n">${s.name}</span><span class="s">${s.sub}</span><span class="m"><span>${next<0?"همهٔ مرحله‌ها تمام شد":next===0&&!pg.lv[0]?"شروع کن":`مرحلهٔ ${fa(next+1)}`}</span><span class="minis">${starSvg(starsOfSt(k)>0,16)} ${fa(starsOfSt(k))} از ${fa((S.track?levelsOf(k).length:4)*3)}</span></span></span></button>`;}).join("")}</div>
  ${TESTMODE?`<footer class="foot"><span>ستاره‌ها روی همین دستگاه ذخیره می‌شوند.</span><button id="rs" type="button">پاک کردن همهٔ ستاره‌ها</button></footer>`:""}`;
  app.querySelectorAll(".st").forEach(b=>b.onclick=()=>hub(b.dataset.k));$("#tk").onclick=TESTMODE?chooseTrack:()=>jmap({});
  $("#fm").onclick=()=>openFormulas();$("#gl").onclick=openGloss;
  const rs=$("#rs");if(rs){let armed=false;rs.onclick=()=>{if(!armed){armed=true;rs.textContent="مطمئنی؟ دوباره بزن";setTimeout(()=>{armed=false;rs.textContent="پاک کردن همهٔ ستاره‌ها";},3000);return;}S.prog={};save();home();};}
  window.scrollTo(0,0);if(!S.track&&TESTMODE)chooseTrack();}
function chooseTrack(){const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">پایه‌ات را انتخاب کن</h2>${S.track?`<button class="chip-btn" id="cx" type="button">بستن</button>`:""}</div><p class="lead">بازی برای هر گروه سنی مرحله‌ها و متن‌های جدا دارد. ستاره‌های هر مسیر جدا ذخیره می‌شوند و هر وقت خواستی می‌توانی مسیر را عوض کنی.</p><div class="tracks">${Object.entries(TRACKS).map(([id,tr])=>`<button class="trk ${S.track===id?"sel":""}" data-t="${id}" type="button" style="--tc:${tr.c}"><span class="g">${tr.g}</span><span class="t">${tr.n}</span><span class="d">${tr.d}</span></button>`).join("")}</div></div>`,"انتخاب پایه");
  o.querySelectorAll("[data-t]").forEach(b=>b.onclick=()=>{S.track=b.dataset.t;save();applyNums();closeOv();home();});const cx=o.querySelector("#cx");if(cx)cx.onclick=closeOv;(o.querySelector(".trk.sel")||o.querySelector(".trk")).focus();}

function hub(k){epoch++;closeOv();setC(k);const s=ST[k],pg=PG(k);
  let h=`<div class="bar"><button class="chip-btn" id="bk" type="button">→ همهٔ ایستگاه‌ها</button><button class="chip-btn fill" id="df" type="button">تعریف و فیلم</button></div>
  <div class="hubhead"><h2>${s.name}</h2><p class="lead">${KID()?KIDINTRO[k]:s.intro}</p></div>
  <div class="modes"><button class="mode lab" id="lab" type="button"><span class="t">آزمایشگاه</span><span class="d">آزادانه امتحان کن. امتیاز و مرحله ندارد؛ فقط کشف کردن.</span></button></div>
  <div class="sect">مرحله‌ها · مسیر ${TRACKS[S.track||"c"].n} (${TRACKS[S.track||"c"].g}) · برای باز شدن مرحلهٔ بعد، دست‌کم یک ستاره بگیر</div><div class="modes">`;
  levelsOf(k).forEach((lv,i)=>{const open=i===0||pg.lv[i-1]>0,stn=pg.lv[i];h+=`<button class="mode ${open?"":"lock"}" data-l="${i+1}" type="button" ${open?"":"disabled"} style="--tc:${TIER[Math.min(3,i)].c}"><span class="tag">مرحلهٔ ${fa(i+1)}</span><span class="t">${open?"":LOCK+" "}${lv.title}</span><span class="d">${lv.desc}</span><span class="st3">${[1,2,3].map(j=>starSvg(j<=stn,18)).join("")}</span></button>`;});
  const eOpen=pg.lv[1]>0;h+=`<button class="mode ${eOpen?"":"lock"}" id="end" type="button" ${eOpen?"":"disabled"} style="--tc:#1B2A41"><span class="tag">بی‌پایان</span><span class="t">${eOpen?"":LOCK+" "}چالش بی‌پایان</span><span class="d">${eOpen?"سه جان داری. هر جواب درست، چالش بعدی را سخت‌تر می‌کند.":"بعد از گرفتن ستارهٔ مرحلهٔ ۲ باز می‌شود."}</span><span class="st3" style="font-size:14px;font-weight:700">${pg.best?"بهترین رکورد: "+fa(pg.best):""}</span></button></div>
  <div><button class="chip-btn" id="fx" type="button">${KID()?"قانون این ایستگاه":"فرمول‌های این ایستگاه"}</button></div>`;
  app.innerHTML=h;$("#bk").onclick=home;$("#df").onclick=()=>openDef(k);$("#fx").onclick=()=>openFormulas(k);$("#lab").onclick=()=>playLab(k);
  app.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>playLevel(k,+b.dataset.l));if(eOpen)$("#end").onclick=()=>playEndless(k);window.scrollTo(0,0);}

function tgBtn(key,label){return `<button class="tg" type="button" data-tg="${key}" aria-pressed="${S[key]?"true":"false"}"><span class="sw"></span>${label}</button>`;}
function board(k,head){epoch++;closeOv();setC(k);const s=ST[k];
  app.innerHTML=`<div class="bar"><button class="chip-btn" id="bk" type="button">→ ${head.backLabel}</button><div class="mid"><b>${s.name}</b><small>${head.sub}</small></div><button class="chip-btn fill" id="df" type="button">تعریف و فیلم</button></div>
  <section class="board">${head.mode!=="lab"?`<div class="phead"><div class="dots" id="dots"></div><div class="score" id="scr"></div></div>`:""}
  <p class="prompt" id="pr"></p><div class="scw"><svg id="sc" viewBox="0 0 640 520" role="img" aria-label="صحنهٔ آزمایش"></svg></div>
  <div class="counter" id="ct" aria-live="polite"></div><div class="ctrl" id="cl"></div><p class="fb" id="fb" aria-live="polite"></p><div class="nav" id="nv"></div><div class="formula" id="fm"></div>
  <div class="toggles">${tgBtn("forces","نمایش نیروها")}${tgBtn("nums","نمایش عددها")}${tgBtn("formula","نمایش فرمول")}</div></section>`;
  const svg=$("#sc");let fmHtml="";
  const P0=makePainter(svg);const A={svg,P:P0,hint:d=>P0.hint(d),view:h=>{svg.setAttribute("viewBox",`0 0 640 ${h}`);svg.style.aspectRatio=`640/${h}`;},tries:0,locked:false,lab:head.mode==="lab",refresh:null,done:null,onLane:null,
    prompt:h=>{if(KID()&&head.mode==="lab")h=KIDLAB[k];const i=h.indexOf("<small>");let main=h,sub="";if(i>=0){main=h.slice(0,i);sub=h.slice(i+7).replace("</small>","");}const pr=$("#pr");main=ltrMath(main);sub=ltrMath(sub);pr.innerHTML=main+(sub&&!KID()?`<button class="helpb" type="button" aria-expanded="false">راهنما</button><small class="help" hidden>${sub}</small>`:"");const hb=pr.querySelector(".helpb");if(hb)hb.onclick=()=>{const s2=pr.querySelector(".help");s2.hidden=!s2.hidden;hb.setAttribute("aria-expanded",String(!s2.hidden));};},counter:h=>{const e=$("#ct");if(e)e.innerHTML=h||"";},
    formula:h=>{fmHtml=h||"";const e=$("#fm");if(e)e.innerHTML=S.formula?fmHtml:"";},
    ctrl:h=>{const c=$("#cl");c.innerHTML=h||"";return c;},fb:(m,c)=>{const e=$("#fb");if(!e)return;e.innerHTML=ltrMath(m||"");e.className="fb "+(c||"");},
    nav:h=>{const n=$("#nv");n.innerHTML=h||"";return n;},
    judge(ok,m){if(A.locked||A.lab)return ok;if(KID()&&m.k)m=Object.assign({},m,m.k);
      if(ok){const pts=m.pts!=null?m.pts:(A.tries===0?2:1);A.locked=true;A.fb(`${pts===2?"آفرین!":"درست شد."} ${m.ok||""} <span style="white-space:nowrap">(+${fa(pts)} امتیاز)</span>`,"ok");if(A.done)A.done(pts);return true;}
      A.tries++;if(A.tries<2){A.fb(KID()?`دوباره امتحان کن. ${m.retry||""}`:`نه هنوز. ${m.retry||""} یک فرصت دیگر داری.`,"no");return false;}
      A.locked=true;A.fb(`${m.final||""}`,"no");if(A.done)A.done(0);return false;}};
  app.querySelectorAll("[data-tg]").forEach(b=>b.onclick=()=>{const key=b.dataset.tg;S[key]=!S[key];save();applyNums();b.setAttribute("aria-pressed",S[key]?"true":"false");A.formula(fmHtml);if(A.refresh)A.refresh();});
  $("#bk").onclick=head.back;$("#df").onclick=()=>openDef(k);
  return A;}

function playLab(k){const A=board(k,{mode:"lab",backLabel:"ایستگاه",sub:"آزمایشگاه",back:()=>hub(k)});ST[k].lab(A);window.scrollTo(0,0);}
function dotsHtml(n,i,res){return Array.from({length:n},(_,j)=>`<i class="${res[j]!=null?"p"+res[j]:j===i?"cur":""}" title="چالش ${fa(j+1)}"></i>`).join("");}
function playLevel(k,L,ctx){const s=ST[k],LV=levelsOf(k),lv=LV[L-1];const r=rng((Date.now()^hash(k+L))>>>0);const specs=ctx&&ctx.resume?ctx.resume.specs:lv.gen(r);const res=ctx&&ctx.resume?ctx.resume.res.slice():[];let i=ctx&&ctx.resume?ctx.resume.i:0;
  const keep=()=>{if(ctx&&ctx.keep)ctx.keep({specs,res,i});};keep();
  function show(){const A=board(k,{mode:"level",backLabel:ctx?"نقشه":"ایستگاه",sub:ctx?ctx.sub:`مرحلهٔ ${fa(L)}: ${lv.title}`,back:ctx?()=>{keep();ctx.back();}:()=>hub(k)});
    const upd=()=>{$("#dots").innerHTML=dotsHtml(specs.length,i,res);$("#scr").innerHTML=`چالش ${fa(i+1)} از ${fa(specs.length)} · امتیاز: ${fa(res.reduce((a,b)=>a+(b||0),0))} از ${fa(specs.length*2)}`;};upd();
    A.done=pts=>{res[i]=pts;upd();if(ctx&&ctx.keep)ctx.keep({specs,res,i:i+1<specs.length?i+1:i,done:i+1>=specs.length});const n=A.nav("");const b=btn(n,i+1<specs.length?"چالش بعدی ←":"دیدن نتیجه","go",()=>{i++;if(i<specs.length){show();$("#pr").scrollIntoView({block:"start",behavior:reduceMotion?"auto":"smooth"});}else finish();});later(50,()=>b.focus({preventScroll:true}));};
    if(window.__TEST||window.__JT)window.__T={spec:specs[i],MASS,LV_MASS,k,i};s.mount(specs[i],A);}
  function finish(){const pts=res.reduce((a,b)=>a+b,0),max=specs.length*2,stars=starsFor(pts,max),pg=PG(k);if(stars>pg.lv[L-1])pg.lv[L-1]=stars;save();
    if(ctx){ctx.finish(stars,pts,max);return;}
    const nextOpen=L<LV.length&&PG(k).lv[L-1]>0;
    const o=overlay(`<div class="sheet res"><h2>${stars===3?"عالی بود!":stars===2?"آفرین!":stars===1?"خوب بود!":"دوباره امتحان کن"}</h2><div class="bigst">${[1,2,3].map(j=>`<span style="--d:${j*.18}s">${starSvg(j<=stars,52)}</span>`).join("")}</div><p><b>${fa(pts)}</b> امتیاز از ${fa(max)}</p><p class="lead">${stars===0?"برای باز شدن مرحلهٔ بعد، دست‌کم یک ستاره لازم است. تعریف‌ها را بخوان و دوباره بازی کن.":stars<3?"برای سه ستاره، بیشتر چالش‌ها را در بار اول درست جواب بده.":"همهٔ چالش‌ها را عالی حل کردی."}</p><div class="nav" style="justify-content:center">${nextOpen?`<button class="btn go" id="rn" type="button">مرحلهٔ بعد</button>`:""}<button class="btn" id="rr" type="button">دوباره</button><button class="btn" id="rh" type="button">ایستگاه</button></div></div>`,"نتیجهٔ مرحله",s.c);
    if(nextOpen)o.querySelector("#rn").onclick=()=>playLevel(k,L+1);o.querySelector("#rr").onclick=()=>playLevel(k,L);o.querySelector("#rh").onclick=()=>hub(k);(o.querySelector("#rn")||o.querySelector("#rr")).focus();if(stars>=2)confetti();}
  show();window.scrollTo(0,0);}
function playEndless(k,ctx){const s=ST[k];const r=rng((Date.now()^hash(k+"e"))>>>0);let lives=3,d=1,score=0,count=0,right=0;
  function show(){const A=board(k,{mode:"endless",backLabel:ctx?"نقشه":"ایستگاه",sub:ctx?ctx.sub:"چالش بی‌پایان",back:ctx?ctx.back:()=>hub(k)});
    const upd=()=>{$("#dots").innerHTML=`<span class="hearts">${[0,1,2].map(j=>heart(j<lives)).join("")}</span>`;$("#scr").innerHTML=ctx?`جواب درست: ${fa(right)} از ${fa(ctx.goal)}`:`چالش ${fa(count+1)} · امتیاز: ${fa(score)} · سختی: ${fa(Math.floor(d))}`;};upd();
    A.done=pts=>{count++;if(pts===0)lives--;else{score+=pts;d+=.4;right++;}upd();if(ctx&&right>=ctx.goal){later(700,()=>ctx.win());return;}const n=A.nav("");const b=btn(n,lives>0?"چالش بعدی ←":"پایان بازی","go",()=>{if(lives>0){show();$("#pr").scrollIntoView({block:"start",behavior:reduceMotion?"auto":"smooth"});}else finish();});later(50,()=>b.focus({preventScroll:true}));};
    const sp=s.endless(r,KID()?Math.min(d,1.9):d);if(window.__TEST||window.__JT)window.__T={spec:sp,MASS,LV_MASS,k,d};s.mount(sp,A);}
  function finish(){const pg=PG(k),rec=score>pg.best;if(rec)pg.best=score;save();if(ctx){ctx.lose(right);return;}
    const o=overlay(`<div class="sheet res"><h2>${rec?"رکورد تازه!":"بازی تمام شد"}</h2><p><b>${fa(score)}</b> امتیاز در ${fa(count)} چالش</p><p class="lead">بهترین رکورد تو: ${fa(pg.best)}</p><div class="nav" style="justify-content:center"><button class="btn go" id="ra" type="button">دوباره</button><button class="btn" id="rh" type="button">ایستگاه</button></div></div>`,"پایان چالش بی‌پایان",s.c);
    o.querySelector("#ra").onclick=()=>playEndless(k);o.querySelector("#rh").onclick=()=>hub(k);o.querySelector("#ra").focus();if(rec)confetti();}
  show();window.scrollTo(0,0);}

function openDef(k){const s=ST[k],D=DEFS[k];
  const o=overlay(`<div class="sheet"><div class="shead"><h2>${s.name}</h2><button class="chip-btn" id="cx" type="button">بستن</button></div><svg viewBox="0 20 640 360" preserveAspectRatio="xMidYMid slice" style="width:100%;height:auto;border-radius:16px;display:block;aspect-ratio:16/9" aria-hidden="true">${s.art()}</svg>${D.paras.map(p=>`<p>${p}</p>`).join("")}<div class="rem">یادت باشد: ${D.rule}</div><div class="sect">نمونه‌ها در زندگی</div><div class="ex">${D.ex.map(e=>`<span>${e}</span>`).join("")}</div><div class="sect">${KID()?"قانون":"فرمول‌ها"}</div><div class="fcards">${FORMULAS.filter(f=>f.k===k).map(fcard).join("")||"<p class='lead'>این ایستگاه فرمول ندارد.</p>"}</div><div class="sect">فیلم‌ها و شبیه‌سازها</div><div class="vids">${D.vids.map(id=>{const v=V[id];return `<a href="${v[1]}" target="_blank" rel="noopener"><svg class="play-ic" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="16" fill="${s.c}"/><path d="M14 11 L24 17 L14 23Z" fill="#fff"/></svg><span>${v[0]}<small>${v[2]}</small></span></a>`;}).join("")}</div><p class="lead">فیلم‌های آپارات بدون فیلترشکن باز می‌شوند.</p></div>`,"تعریف "+s.name,s.c);
  o.querySelector("#cx").onclick=closeOv;o.querySelector("#cx").focus();}
function fcard(f){if(KID())return f.rule?`<div class="fcard" style="--c:${ST[f.k].c}"><span class="gr">${ST[f.k].name}</span><h3>${f.t}</h3><div class="exm" style="font-size:18px;font-weight:700">${f.rule}</div></div>`:"";return `<div class="fcard" style="--c:${ST[f.k].c}"><span class="gr">${ST[f.k].name} · ${f.g==="b"?"از پایهٔ چهارم":"پایهٔ پنجم و ششم"}</span><h3>${f.t}</h3><div class="eq"><span class="eqx" dir="ltr">${f.eq()}</span></div><div class="lg" style="justify-content:center">${f.lg().map(([s,m])=>`<span class="lgi"><span dir="ltr">${s}</span>: ${m}</span>`).join("")}</div><div class="exm">مثال: ${f.ex} <span class="eqx" dir="ltr" style="font-size:16px">${f.exq()}</span></div></div>`;}
function openFormulas(k){const list=k?FORMULAS.filter(f=>f.k===k).concat(FORMULAS.filter(f=>f.k!==k)):FORMULAS;
  const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">${KID()?"قانون‌ها":"فرمول‌ها"}</h2><button class="chip-btn" id="cx" type="button">بستن</button></div><p class="lead">${KID()?"قانون هر ماشین ساده در یک جمله.":"هر فرمول با نمادهای علمی و یک مثال حل‌شده. فرمول‌ها از چپ به راست خوانده می‌شوند."}</p><div class="fcards">${list.map(fcard).join("")}</div></div>`,"فرمول‌ها",k?ST[k].c:null);
  o.querySelector("#cx").onclick=closeOv;o.querySelector("#cx").focus();}
function openGloss(){const o=overlay(`<div class="sheet"><div class="shead"><h2 style="color:var(--ink)">واژه‌نامه</h2><button class="chip-btn" id="cx" type="button">بستن</button></div><dl class="gl">${GLOSS.map(([t,d])=>`<div><dt>${t}</dt><dd>${d}</dd></div>`).join("")}</dl></div>`,"واژه‌نامه");o.querySelector("#cx").onclick=closeOv;o.querySelector("#cx").focus();}

