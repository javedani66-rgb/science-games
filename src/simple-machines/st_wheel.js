/* ================= ایستگاه چرخ و محور (چاه) ================= */
const wheelLbl=k=>k===1?"بدون دسته":KID()?({2:"دستهٔ کوتاه",3:"دستهٔ متوسط",4:"دستهٔ بلند",5:"دستهٔ بلندتر",6:"دستهٔ خیلی بلند"}[k]):"دستهٔ "+fa(k);
function makeWell(A,cfg){cfg=machineScene(A,cfg);const svg=A.svg,P=A.P;A.view(404);const G=230,HX=420,HY=137,RP=14,MPX=80;
  const st={R:cfg.R||1,W:cfg.W,S:cfg.S,h:cfg.h||2,ang:0,phi:-Math.PI/2,busy:false,flash:0,edit:cfg.edit!==false,hideF:!!cfg.hideF};
  const F=()=>MACHINE.wheel(st.W,st.R),turns=()=>st.ang/(2*Math.PI),rise=()=>turns()*.5;
  function render(){if(!cfg.current())return;const ok=canLift(F(),st.S),B=342-rise()*MPX;let s=bgOut(G);
    s+=`<rect x="0" y="${G}" width="640" height="${404-G}" fill="#9A6B43"/><rect x="0" y="${G}" width="640" height="8" fill="#6DB35A"/><g fill="#86593A">${[[40,280],[92,330],[300,300],[560,350],[480,270],[120,380]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="4"/>`).join("")}</g>`;
    s+=`<rect x="170" y="${G}" width="60" height="${404-G}" fill="#3F2E22"/>`;
    const th=342-st.h*MPX;s+=`<line x1="150" y1="${th}" x2="250" y2="${th}" stroke="${GRN}" stroke-width="3" stroke-dasharray="8 6"/>`+T(146,th+5,NUMS()?`هدف: ${fa(st.h)} متر`:"هدف",{size:13,col:GRN,anchor:"start"});
    s+=`<line x1="200" y1="144" x2="200" y2="${B-18}" stroke="#7A5634" stroke-width="3"/><path d="M184 ${B-4} Q200 ${B-24} 216 ${B-4}" stroke="#5E6E86" stroke-width="3" fill="none"/><path d="M180 ${B-4} H220 L215 ${B+30} H185Z" fill="#8FA3B5" stroke="#5E6E86" stroke-width="2.5"/><rect x="180" y="${B-6}" width="40" height="6" rx="2" fill="#6F8499"/>`+T(200,B+20,kn(st.W),{size:12,col:"#fff",halo:false});
    s+=`<rect x="170" y="364" width="60" height="40" fill="#4FA3D8" opacity=".85"/>`;
    s+=`<rect x="156" y="202" width="88" height="${G-202}" fill="#A3ACB8"/><path d="M156 216 H244 M178 202 V216 M212 202 V216 M195 216 V230 M228 216 V230" stroke="#7E8894" stroke-width="2"/><rect x="152" y="194" width="96" height="9" rx="3" fill="#7E8894"/>`;
    s+=`<rect x="160" y="96" width="9" height="100" fill="#8A5427"/><rect x="231" y="96" width="9" height="100" fill="#8A5427"/><path d="M136 100 L200 58 L264 100Z" fill="#E4553A"/><path d="M136 100 H264" stroke="#B83E28" stroke-width="5" stroke-linecap="round"/>`;
    const wraps=2+Math.round(Math.min(12,turns()*2.5));let coil="";for(let i=0;i<wraps;i++)coil+=`<line x1="${188+i*2.4}" y1="130" x2="${188+i*2.4}" y2="144" stroke="#6B4A2B" stroke-width="1.8"/>`;
    s+=`<rect x="166" y="130" width="74" height="14" rx="5" fill="#C98A4B"/>${coil}<rect x="240" y="${HY-3}" width="${HX-240}" height="6" fill="#7D8CA3"/>`;
    const rr=st.R*RP,kx=HX+Math.cos(st.phi)*rr,ky=HY+Math.sin(st.phi)*rr,flash=st.flash>0;
    if(st.R>1)s+=`<circle cx="${HX}" cy="${HY}" r="${rr}" fill="none" stroke="#7C4DCC" stroke-width="2.5" stroke-dasharray="6 6" opacity=".8"/>`+T(HX-rr*.72-8,HY-rr*.72-6,"مسیر دست",{size:12,col:"#7C4DCC",anchor:"start"});
    s+=`<line x1="${HX}" y1="${HY}" x2="${kx}" y2="${ky}" stroke="#4A5A78" stroke-width="8" stroke-linecap="round"/><circle cx="${HX}" cy="${HY}" r="8" fill="#4A5A78"/>`;
    if(S.forces){const tx=-Math.sin(st.phi),ty=Math.cos(st.phi),fl=Math.max(22,Math.min(100,F()*1.3));s+=arrow(kx+tx*16,ky+ty*16,kx+tx*(16+fl),ky+ty*(16+fl),9,st.hideF?"#7D8CA3":ok?GRN:RED);}
    s+=`<g data-drag="knob" style="cursor:grab"><circle cx="${kx}" cy="${ky}" r="32" fill="#fff" fill-opacity="0"/><circle cx="${kx}" cy="${ky}" r="20" fill="${flash?RED:"#FFC43D"}" stroke="#fff" stroke-width="3"/><path d="M${kx-6} ${ky} a6 6 0 1 1 6 6" stroke="${INK}" stroke-width="2" fill="none"/></g>`;
    s+=gBar(st.hideF?0:F(),st.S,16,36,112);
    
    machinePaint(A,s);
    machineKeys(A,'[data-drag="knob"]',"چرخاندن دسته؛ کلید راست یا ورود",key=>{if(st.busy||!st.edit||st.done)return;
      if(!canLift(F(),st.S)){if(cfg.onBlocked)cfg.onBlocked();return;}
      const next=clamp(st.ang+(key==="ArrowLeft"?-1:1)*Math.PI/2,0,st.h/.5*2*Math.PI);st.phi+=next-st.ang;st.ang=next;render();
      if(st.ang>=st.h/.5*2*Math.PI-1e-6&&!st.done){st.done=true;if(cfg.onTop)cfg.onTop();}});
    A.counter(`<span class="cc">شعاع دسته (فاصلهٔ دستگیره تا محور): <b>${st.R===1?"بدون دسته":fa(st.R)+" برابر شعاع محور"}</b></span><span class="cc">دور: <b>${fa(r1(turns()))}</b></span><span class="cc">راه دست: <b>${fa(r1(MACHINE.hand(st.R,turns())))} متر</b></span><span class="cc ${ok?"":"r"}">نیروی لازم: <b class="num">${st.hideF?"؟":fa(r1(F()))+" نیوتون"}</b></span>`);
    A.formula(FX(`${sy("F")} × ${sy("R")} = ${sy("W")} × ${sy("r")}`,st.hideF?"":`${sy("F")} = ${fa(st.W)} × ۱ ÷ ${fa(st.R)} = ${fa(r1(F()))} N`,[[sy("F"),"نیروی لازم (N)"],[sy("R"),"شعاع دسته: فاصلهٔ دستگیره تا محور (چند برابر شعاع محور)"],[sy("W"),"وزن سطل (N)"],[sy("r"),"شعاع محور (اینجا ۱ واحد)"]]));}
  let last=0;
  dragKit(svg,{blocked:()=>A.locked||st.busy||!st.edit,start(d,p){if(d.drag!=="knob")return null;last=Math.atan2(p.y-HY,p.x-HX);return{};},begin(){},
    move(g,p){const a=Math.atan2(p.y-HY,p.x-HX);let da=a-last;if(da>Math.PI)da-=2*Math.PI;if(da<-Math.PI)da+=2*Math.PI;last=a;
      if(!canLift(F(),st.S)){st.flash=1;st.phi+=da*.08;if(!g.failed&&cfg.onBlocked){g.failed=true;cfg.onBlocked();}render();return;}
      const maxA=st.h/.5*2*Math.PI;const na=clamp(st.ang+da,0,maxA);st.phi+=na-st.ang;st.ang=na;render();if(st.ang>=maxA-1e-6&&cfg.onTop&&!st.done){st.done=true;cfg.onTop();}},
    end(){st.flash=0;render();},tap(){}});
  render();
  return{st,render,F,reset(){st.ang=0;st.phi=-Math.PI/2;st.done=false;render();},auto(done){const maxA=st.h/.5*2*Math.PI;st.busy=true;tween(1800,p=>{st.ang=maxA*ease(p);st.phi=-Math.PI/2+st.ang;render();},()=>{st.busy=false;if(cfg.current()&&done)done();});}};
}
/* پرسش‌های چرخ و محور؛ همه دربارهٔ همین چاهِ روی صحنه */
const WHEEL_MCQ={1:["چرخ و محور یعنی چرخ یا دستهٔ بزرگی که یک میلهٔ باریک را می‌چرخاند. در این چاه، محور کدام است؟",["میلهٔ باریکی که طناب دورش پیچیده می‌شود","دستهٔ چرخان","سطل"],0,"دستهٔ بزرگ و میلهٔ باریکِ چاه با هم می‌چرخند؛ میلهٔ باریکی که طناب دورش پیچیده می‌شود، محور است."],
 2:["روی صحنه دو دایره می‌بینی: دایرهٔ کوچک مسیر دستِ کوتاه است و دایرهٔ بزرگ مسیر دستِ بلند. با دستهٔ بلندتر، دستت در هر دور راه کوتاه‌تری می‌رود یا بلندتر؟",["کوتاه‌تر","یکسان","بلندتر"],2,"دستهٔ بلندتر یعنی دایرهٔ بزرگ‌تر؛ نیروی کمتری لازم است، ولی دست راه بیشتری می‌رود."],
 3:["چرا دستهٔ این چاه را بلند ساخته‌اند؟",["تا با نیروی کمتری بچرخد","تا زیباتر باشد","تا سطل سبک‌تر شود"],0,"دستهٔ بلندتر یعنی نیروی کمتر برای چرخاندن؛ سطل همان‌قدر سنگین است، ولی دست راه بیشتری می‌رود."]};
const ST_wheel={key:"wheel",name:"چرخ و محور",c:"#7C4DCC",sub:"دستهٔ بلندتر، نیروی کمتر",
 intro:"دستگیرهٔ زرد را دور دایره بچرخان تا سطل از چاه بالا بیاید. طول دسته را عوض کن و ببین نیروی لازم و راه دستت چطور تغییر می‌کند.",
 art(){let h=bgOut(230).replace(/id="go"/,'id="aw"').replace(/url\(#go\)/,"url(#aw)");h+=`<rect x="0" y="230" width="640" height="300" fill="#9A6B43"/><rect x="170" y="230" width="60" height="300" fill="#3F2E22"/><rect x="156" y="202" width="88" height="28" fill="#A3ACB8"/><rect x="160" y="96" width="9" height="100" fill="#8A5427"/><rect x="231" y="96" width="9" height="100" fill="#8A5427"/><path d="M136 100 L200 58 L264 100Z" fill="#E4553A"/><rect x="166" y="130" width="74" height="14" rx="5" fill="#C98A4B"/><rect x="240" y="134" width="180" height="6" fill="#7D8CA3"/><circle cx="420" cy="137" r="56" fill="none" stroke="#7C4DCC" stroke-width="2.5" stroke-dasharray="6 6"/><line x1="420" y1="137" x2="460" y2="97" stroke="#4A5A78" stroke-width="8" stroke-linecap="round"/><circle cx="460" cy="97" r="14" fill="#FFC43D" stroke="#fff" stroke-width="3"/><line x1="200" y1="144" x2="200" y2="250" stroke="#7A5634" stroke-width="3"/><path d="M180 262 H220 L215 296 H185Z" fill="#8FA3B5" stroke="#5E6E86" stroke-width="2.5"/>`;return h;},
 lab(A){A.prompt("آزمایشگاه چرخ و محور: طول دسته را انتخاب کن و دستگیره را بچرخان. به راه دست و نیروی لازم دقت کن.");
   let R=3,W=60,Sv=30,wl;const mk=()=>{wl=makeWell(A,{R,W,S:Sv,h:2,onTop:()=>A.fb("سطل بالا آمد!","ok"),onBlocked:()=>A.fb("نیرویت کافی نیست؛ دستهٔ بلندتری انتخاب کن.","no")});A.refresh=()=>wl.render();};mk();
   const c=A.ctrl("");c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="rs">${[1,2,3,4,5,6].map(k=>`<button class="opt ${k===R?"sel":""}" data-r="${k}" type="button">${wheelLbl(k)}</button>`).join("")}</div>`);
   c.querySelector("#rs").onclick=e=>{const b=e.target.closest("[data-r]");if(!b)return;R=+b.dataset.r;c.querySelectorAll("#rs .opt").forEach(x=>x.classList.toggle("sel",x===b));A.fb("");mk();};
   stepper(c,{init:W,min:10,max:200,steps:[10],unit:"وزن سطل",onChange:v=>{W=v;mk();}});stepper(c,{init:Sv,min:5,max:100,steps:[5],unit:"نیروی تو",onChange:v=>{Sv=v;mk();}});btn(c,"از اول","",()=>{wl.reset();A.fb("");});},
 kid:[
  {id:"wheel.a1",title:"چرخاندن دسته",desc:"دسته را بچرخان و سطل را بالا بیاور.",gen(){return[{t:"crank",R:4,W:40,S:20,h:1},{t:"mcq",q:1},{t:"crank",R:3,W:30,S:20,h:1}];}},
  {id:"wheel.a2",title:"دستهٔ بلندتر",desc:"دسته‌ای انتخاب کن که با آن بتوانی سطل را بالا بکشی.",gen(){return[{t:"choose",W:60,S:25,opts:[1,2,3,4]},{t:"mcq",q:2},{t:"choose",W:80,S:30,opts:[1,2,3,4]},{t:"mcq",q:3}];}}],
 levels:[
  {id:"wheel.1",title:"چرخاندن دسته",desc:"دسته را بچرخان تا سطل بالا بیاید. بعد دسته‌ای انتخاب کن که با آن بتوانی سطل را بالا بکشی.",gen(){return[{t:"crank",R:4,W:40,S:20,h:1},{t:"mcq",q:1},{t:"choose",W:60,S:25,opts:[1,2,3,4]},{t:"crank",R:2,W:30,S:20,h:1.5},{t:"mcq",q:2},{t:"choose",W:80,S:30,opts:[1,2,3,4]}];}},
  {id:"wheel.2",title:"نیرو و راه دست",desc:"نیروی لازم و راه دست را حساب کن.",gen(){return[{t:"choose",W:100,S:30,opts:[1,2,3,4,5,6]},{t:"calcF",W:90,R:3},{t:"calcPath",R:3,n:4},{t:"choose",W:120,S:25,opts:[1,2,3,4,5,6]},{t:"calcF",W:150,R:6},{t:"mcq",q:3}];}},
  {id:"wheel.3",title:"طراحی دسته",desc:"کوتاه‌ترین دسته‌ای را که با آن سطل بالا می‌آید حساب کن.",gen(){return[{t:"mcq",q:2},{t:"choose",W:110,S:20,opts:[1,2,3,4,5,6]},{t:"calcR",W:110,S:20},{t:"choose",W:140,S:30,opts:[1,2,3,4,5,6]},{t:"calcPath",R:5,n:6},{t:"calcF",W:75,R:5},{t:"calcR",W:90,S:20},{t:"choose",W:50,S:12,opts:[1,2,3,4,5,6]}];}},
  {id:"wheel.4",title:"قهرمان چرخ و محور",desc:"عددهای بزرگ‌تر و همه‌چیز با هم.",gen(r){return[{t:"mcq",q:2},{t:"choose",W:170,S:35,opts:[1,2,3,4,5,6]},{t:"calcR",W:130,S:30},{t:"calcPath",R:6,n:5},{t:"calcF",W:120,R:4},{t:"mcq",q:pick(r,[2,3])},{t:"choose",W:200,S:45,opts:[1,2,3,4,5,6]}];}}],
 endless(r,d){const tp=pick(r,d<2?["crank","choose","mcq"]:["choose","calcF","calcR","calcPath"]);
   if(tp==="mcq")return{t:"mcq",q:pick(r,[1,2,3])};if(tp==="crank"){const R=ri(r,2,5),W=ri(r,2,8)*10;return{t:"crank",R,W,S:Math.ceil(W/R)+5,h:pick(r,[1,1.5])};}
   if(tp==="calcF"){const R=ri(r,2,6);return{t:"calcF",W:R*ri(r,3,12)*5,R};}if(tp==="calcPath")return{t:"calcPath",R:ri(r,2,6),n:ri(r,2,8)};
   for(let k=0;k<60;k++){const W=ri(r,4,20)*10,Sv=ri(r,2,10)*5;const R=Math.ceil(W/Sv);if(R>1&&R<=6&&W%Sv!==0)return tp==="calcR"?{t:"calcR",W,S:Sv}:{t:"choose",W,S:Sv,opts:[1,2,3,4,5,6]};}return{t:"choose",W:60,S:25,opts:[1,2,3,4]};},
 mount(sp,A){
  if(sp.t==="mcq"){const Q=WHEEL_MCQ[sp.q];
    if(sp.q===1){const wl=makeWell(A,{R:4,W:40,S:100,h:1,edit:false});A.refresh=()=>wl.render();
      machineObserve(A,"دسته و میلهٔ دور طناب را ببین. با چرخاندن دسته، میله هم می‌چرخد.",done=>wl.auto(done),Q[0],Q[1],Q[2],Q[3],"طناب دور کدام بخش پیچیده می‌شود؟");return;}
    let wl,busy=false;const seen=new Set(),draw=R=>{wl=makeWell(A,{R,W:40,S:100,h:1,edit:false});A.refresh=()=>wl.render();};draw(2);
    A.prompt(machineRule("همان سطل را با دستهٔ کوتاه و بلند تا همان ارتفاع بالا می‌بریم. هر دو آزمایش را ببین. شعاع محور ثابت است.","همان سطل را با دستهٔ کوتاه و بلند بالا می‌بریم. هر دو را آزمایش کن."));const c=A.ctrl("");
    [2,4].forEach(R=>btn(c,R===2?"دستهٔ کوتاه را آزمایش کن":"دستهٔ بلند را آزمایش کن","",()=>{if(busy||A.locked)return;busy=true;draw(R);wl.auto(()=>{busy=false;seen.add(R);
      A.fb(KID()?(R===2?"دستهٔ کوتاه: دست راه کمتری رفت؛ نیروی بیشتری لازم بود.":"دستهٔ بلند: دست راه بیشتری رفت؛ نیروی کمتری لازم بود."):`شعاع ${fa(R)} برابر محور؛ ۲ دور؛ راه دست ${fa(R)} متر؛ نیروی لازم ${fa(40/R)} نیوتون.`,"info");if(seen.size===2)ask();});}));
    function ask(){A.prompt(sp.q===2?"با دستهٔ بلندتر، دست در همان تعداد دور چه راهی رفت؟":"با دستهٔ بلندتر، نیروی لازم چه تغییری کرد؟");const c2=A.ctrl("");const m=mcq(c2,sp.q===2?["کوتاه‌تر","یکسان","بلندتر"]:["کمتر شد","یکسان ماند","بیشتر شد"],(i,bt)=>{if(A.locked)return;const ans=sp.q===2?2:0,ex="با سطل، محور و ارتفاع یکسان، دستهٔ بلندتر نیروی کمتری خواست و دست راه بیشتری رفت. تعداد دورها یکسان بود.";
      if(i===ans){m.disable();m.mark(i,"right");A.judge(true,{ok:ex});}else{bt.disabled=true;A.judge(false,{retry:"در هر دو آزمایش ۲ دور چرخاندیم؛ دستهٔ بلند راه دست را بیشتر کرد و نیرو را کمتر.",final:ex});if(A.locked){m.disable();m.mark(ans,"right");}}});}
    return;}
  if(sp.t==="crank"||sp.t==="choose"){const R0=sp.t==="crank"?sp.R:sp.opts[0],rr=Math.max(1,R0)*14;A.hint(`M420 ${137-rr} A${rr} ${rr} 0 1 1 419.9 ${137-rr}`);}
  if(sp.t==="crank"){A.prompt(KID()?"دستگیره را بچرخان تا سطل بالا بیاید.":`سطل آب را تا خط سبز بالا بکش.<small>دستگیرهٔ زرد را دور دایره بچرخان.</small>`);const wl=makeWell(A,{R:sp.R,W:sp.W,S:sp.S,h:sp.h,onTop:()=>A.judge(true,{k:{ok:"سطل بالا آمد!"},ok:`سطل بالا آمد. ${fa(sp.h/.5)} دور چرخاندی و دستت ${fa(sp.h/.5*sp.R*.5)} متر راه رفت.`})});A.refresh=()=>wl.render();A.ctrl("");return;}
  if(sp.t==="choose"){const best=MACHINE.minimum(sp.opts,R=>MACHINE.wheel(sp.W,R),sp.S);
    A.prompt(machineRule(`همان سطل ${fa(sp.W)} نیوتونی را ۱ متر بالا ببر. نیروی تو ${fa(sp.S)} نیوتون است. شعاع دسته را انتخاب کن و دستگیره را بچرخان. شعاع محور ثابت است.`,"دسته‌ای انتخاب کن و بچرخان تا سطل بالا بیاید. آزمایش‌های ناموفق امتیاز کم نمی‌کنند."));
    let R=sp.opts[0],wl,bl=false;const mk=()=>{wl=makeWell(A,{R,W:sp.W,S:sp.S,h:1,onBlocked:()=>{
      machineGuide(A,"دسته نچرخید؛ نیرویت کافی نیست. دستهٔ بلندتری انتخاب کن.","سطل، محور و ارتفاع ثابت‌اند. دستهٔ بلندتر نیروی کمتری می‌خواهد و دست راه بیشتری می‌رود.",KID()?"با دستهٔ بلندتر، سطل بالا می‌آید.":`با شعاع ${fa(best)} برابر محور، نیروی لازم ${fa(r1(MACHINE.wheel(sp.W,best)))} نیوتون است.`,()=>{R=best;mk();wl.st.ang=4*Math.PI;wl.st.phi=-Math.PI/2+wl.st.ang;wl.st.done=true;wl.render();select();});},
      onTop:()=>machineSuccess(A,`سطل ۱ متر بالا آمد. دسته ${fa(2)} دور چرخید و دست ${fa(R)} متر راه رفت. با هر دستهٔ موفق، تعداد دور برای همین ارتفاع یکسان است؛ راه دست با شعاع تغییر می‌کند.`,"سطل بالا آمد! دستهٔ بلندتر نیروی کمتری می‌خواهد، اما دست راه بیشتری می‌رود.")});A.refresh=()=>wl.render();};mk();
    const c=A.ctrl("");c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="rs">${sp.opts.map(k=>`<button class="opt ${k===R?"sel":""}" data-r="${k}" type="button">${wheelLbl(k)}</button>`).join("")}</div>`);
    function select(){c.querySelectorAll("#rs .opt").forEach(x=>x.classList.toggle("sel",+x.dataset.r===R));}
    c.querySelector("#rs").onclick=e=>{if(A.locked)return;const b=e.target.closest("[data-r]");if(!b)return;R=+b.dataset.r;bl=false;select();mk();};return;}
  let q,ans,unit,steps,expl,retry,cfg;
  if(sp.t==="calcF"){cfg={R:sp.R,W:sp.W,S:Math.floor(sp.W/sp.R/5)*5+5,hideF:true};q=`سطل ${fa(sp.W)} نیوتون است و شعاع دسته ${fa(sp.R)} برابر شعاع محور است. نیروی لازم چقدر است؟ (نیرو = وزن سطل ÷ چند برابر بودنِ شعاع دسته)`;ans=sp.W/sp.R;unit="نیوتون";steps=[1,10];expl=`${fa(sp.W)} ÷ ${fa(sp.R)} = ${fa(r1(ans))} نیوتون.`;retry="وزن را بر عدد «چند برابر» تقسیم کن.";}
  else if(sp.t==="calcR"){ans=Math.floor(sp.W/sp.S)+1;cfg={R:1,W:sp.W,S:sp.S,hideF:false};q=`سطل ${fa(sp.W)} نیوتون است و نیروی تو ${fa(sp.S)} نیوتون. برای شروع بالا رفتن سطل، شعاع دسته چند برابر شعاع محور باشد؟ کوچک‌ترین عدد صحیح را پیدا کن. (وزن سطل ÷ شعاعِ چندبرابری باید کمتر از نیروی تو باشد)`;unit="برابر";steps=[1];expl=`${fa(sp.W)} ÷ ${fa(sp.S)} = ${fa(r1(sp.W/sp.S))}؛ برای شروع حرکت، شعاع دسته باید دست‌کم ${fa(ans)} برابر شعاع محور باشد.`;retry="وزن را بر نیروی خودت تقسیم کن و عدد صحیح بزرگ‌تر از حاصل را انتخاب کن. در حالت برابر، سطل از سکون بالا نمی‌رود.";}
  else{cfg={R:sp.R,W:40,S:100};q=`شعاع دسته ${fa(sp.R)} برابر شعاع محور است و در هر دور، محور نیم متر طناب می‌پیچد. اگر ${fa(sp.n)} دور بچرخانی، دستت چند متر راه می‌رود؟ (در هر دور، دست چند برابرِ طنابِ محور راه می‌رود؛ همان چند برابرِ شعاع)`;ans=sp.n*sp.R*.5;unit="متر";steps=[.5,1];expl=`هر دور دست ${fa(sp.R)} × ۰٫۵ = ${fa(sp.R*.5)} متر؛ ${fa(sp.n)} دور = ${fa(ans)} متر.`;retry="در هر دور، دست به اندازهٔ (چند برابرِ شعاع × نیم متر) راه می‌رود. این را در تعداد دورها ضرب کن.";}
  const wl=makeWell(A,Object.assign({h:2,edit:false},cfg));A.refresh=()=>wl.render();A.prompt(machineRule(q));const c=A.ctrl("");const stp=stepper(c,{init:0,max:300,steps,unit});
  const chk=btn(c,"بررسی","go",()=>{const ok=Math.abs(stp.get()-ans)<.051;A.judge(ok,{ok:expl,retry,final:expl});if(A.locked){chk.disabled=true;stp.disable();if(sp.t==="calcR"){wl.st.R=ans;}wl.st.hideF=false;wl.render();wl.auto();}});
 }};

machinePacks("wheel",[...ST_wheel.kid,...ST_wheel.levels]);
