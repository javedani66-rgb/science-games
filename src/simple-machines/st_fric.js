/* ================= ایستگاه اصطکاک (جدا از نیرو، ۱۴۰۵/۷/۹) =================
   سطح‌ها همان سه سطحِ makeFriction هستند. قانونِ بازی: جعبه راه می‌افتد اگر هل از اصطکاکِ سطح بیشتر باشد؛
   وقتی جعبه ساکن است، اصطکاک دقیقاً برابرِ هل است (فلش‌ها هم‌اندازه). مسافتِ سُر خوردن = (هل − اصطکاک) × ۹ (فقط نمایشی). */
const SURF=[{n:"یخ",f:4,col:"#CFEFFB",edge:"#8CCFEA"},{n:"کف چوبی",f:15,col:"#E3B77F",edge:"#B9834A"},{n:"فرش",f:35,col:"#D9776B",edge:"#A94B41"}];
const slideDist=(F,i)=>Math.min(300,Math.max(0,F-SURF[i].f)*9);
const minPush=i=>Math.floor(SURF[i].f/5)*5+5;
/* نشانگرِ اندازهٔ اصطکاک: برای سطح ۱ سه پلهٔ تصویری، برای بقیه عدد */
function fricMeter(x,y,i){if(!NUMS()){let s="";for(let j=0;j<3;j++)s+=`<rect x="${x-22-j*16}" y="${y-12}" width="12" height="12" rx="3" fill="${j<=i?"#E8590C":"#fff"}" stroke="#E8590C" stroke-width="1.5"/>`;return s+T(x-74,y-1,"اصطکاک",{size:11,col:"#B4460A",anchor:"end",halo:false});}
  return T(x,y,`اصطکاک تا <tspan class="num">${fa(SURF[i].f)}</tspan> نیوتن`,{size:12,col:"#B4460A",anchor:"start",halo:false});}
function surfTex(i,x0,x1,sy){if(i===0){let s="";for(let x=x0+30;x<x1-40;x+=170)s+=`<path d="M${x} ${sy+10} l40 -6" stroke="#fff" stroke-width="3" stroke-linecap="round"/>`;return s;}
  if(i===1){let s="";for(let x=x0+60;x<x1;x+=100)s+=`<line x1="${x}" y1="${sy}" x2="${x}" y2="${sy+26}" stroke="#B9834A" stroke-width="2"/>`;return s;}
  let s="";for(let x=x0+14;x<x1-4;x+=18)s+=`<circle cx="${x}" cy="${sy+8+(x%36?8:0)}" r="2.2" fill="#B85548"/>`;return s;}

/* یک مسیر: جعبه، سطحِ قابل تعویض، پرچمِ هدف (اختیاری) */
function makeSlide(A,cfg){const svg=A.svg,P=A.P;A.view(330);
  const st={surf:cfg.surf==null?null:cfg.surf,F:cfg.F,pos:0,busy:false,flag:cfg.flag==null?null:cfg.flag,moved:null};
  const X0=150,SY=228;
  function render(){const i=st.surf,cx=X0+st.pos;let s=`<rect width="640" height="330" style="fill:var(--sw)"/><rect y="${SY+26}" width="640" height="${330-SY-26}" style="fill:var(--sf)"/>`;
    s+=`<g data-zone="strip" style="cursor:pointer"><rect x="60" y="${SY}" width="560" height="26" rx="6" fill="${i==null?"#fff":SURF[i].col}" stroke="${i==null?"#B8C6D3":SURF[i].edge}" stroke-width="2" ${i==null?'stroke-dasharray="8 6"':""}/>${i==null?"":surfTex(i,60,620,SY)}</g>`;
    if(i!=null){s+=T(612,40,SURF[i].n,{size:15,col:INK,anchor:"start"});if(cfg.labels!==false)s+=fricMeter(612,74,i);}
    else s+=T(612,40,KID()?"سطح را انتخاب کن":"سطحی انتخاب نشده",{size:14,col:MUT,anchor:"start"});
    if(st.flag!=null){const fx=X0+st.flag;s+=`<line x1="${fx}" y1="${SY}" x2="${fx}" y2="${SY-92}" stroke="${INK}" stroke-width="3"/><path d="M${fx} ${SY-92} L${fx+34} ${SY-81} L${fx} ${SY-70}Z" fill="#E4553A"/>`;}
    s+=shadow(cx,SY+1,70)+crateSvg(cx,SY,66,52,"",null);
    if(S.forces&&st.F>0&&!st.busy&&st.pos===0){const AL=v=>Math.max(16,Math.min(90,v*1.6)),pl=AL(st.F);
      s+=arrow(cx-36-pl,SY-36,cx-37,SY-36,10,BLUE)+T(cx-42-pl,SY-58,NUMS()?`هل <tspan class="num">${fa(st.F)}</tspan>`:"هل",{size:13,col:BLUE,anchor:"end"});
      if(i!=null){const f=Math.min(st.F,SURF[i].f),fl=AL(f);s+=arrow(cx+30,SY-8,cx+30-fl,SY-8,7,"#E8590C");}}
    P.paint(s);}
  function run(done){if(st.surf==null){done&&done(null);return;}st.busy=true;const d=slideDist(st.F,st.surf);
    tween(d?1600:500,p=>{const e=1-Math.pow(1-p,3);st.pos=d*e;render();},()=>{st.busy=false;st.moved=d;render();done&&done(d);});}
  render();return{st,render,run,reset(){st.pos=0;st.moved=null;render();}};}

/* دکمه‌های انتخاب سطح (مثل انتخاب جهت در نیروی خالص) */
function surfPicker(c,st,onPick){c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="surfs">${SURF.map((L,i)=>`<button class="opt ${st.surf===i?"sel":""}" data-s="${i}" type="button">${L.n}</button>`).join("")}</div>`);
  const box=c.querySelector("#surfs");box.onclick=e=>{const b=e.target.closest("[data-s]");if(!b||b.disabled)return;st.surf=+b.dataset.s;box.querySelectorAll(".opt").forEach(x=>x.classList.toggle("sel",x===b));onPick&&onPick(st.surf);};
  return{lock(){box.querySelectorAll(".opt").forEach(x=>x.disabled=true);}};}

const ST_fric={key:"fric",name:"اصطکاک",c:"#C2410C",sub:"یخ، چوب و فرش؛ کمترین هل",
 intro:"اصطکاک نیرویی است که جلوی سُر خوردن را می‌گیرد. جعبه را روی یخ، چوب و فرش هل بده و ببین کجا راحت‌تر حرکت می‌کند.",
 art(){let h=`<rect width="640" height="520" style="fill:var(--sw)"/>`;SURF.forEach((L,i)=>{const sy=150+i*90;h+=`<rect x="70" y="${sy}" width="520" height="24" rx="6" fill="${L.col}" stroke="${L.edge}" stroke-width="2"/>`+surfTex(i,70,590,sy)+crateSvg(180+(2-i)*110,sy,58,46,"",null);});
   return h+arrow(110,330,180,330,10,BLUE);},
 lab(A){A.prompt("آزمایشگاه اصطکاک: اندازهٔ هل را انتخاب کن و «هل بده!» را بزن. ببین روی هر سطح جعبه چقدر جلو می‌رود.");A.counter("");
   let F=20,fr=makeFriction(A,F);A.formula(`<span class="fl">قانون</span><span>اصطکاک تا یک اندازه جلوی هل را می‌گیرد. اگر هل از آن اندازه بیشتر شود، جعبه راه می‌افتد.</span>`);A.refresh=()=>fr.render();
   const c=A.ctrl("");if(!KID())stepper(c,{init:F,min:5,max:60,steps:[5],unit:"نیوتن هل",onChange:v=>{F=v;fr=makeFriction(A,F);A.refresh=()=>fr.render();}});
   else{c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="kf"><button class="opt" data-f="10" type="button">هل کم</button><button class="opt sel" data-f="20" type="button">هل متوسط</button><button class="opt" data-f="40" type="button">هل زیاد</button></div>`);
     const kf=c.querySelector("#kf");kf.onclick=e=>{const b=e.target.closest("[data-f]");if(!b)return;F=+b.dataset.f;kf.querySelectorAll(".opt").forEach(x=>x.classList.toggle("sel",x===b));fr=makeFriction(A,F);A.refresh=()=>fr.render();};}
   btn(c,"هل بده!","go",b=>{b.disabled=true;fr.reset();fr.run(()=>{b.disabled=false;const moved=fr.lanes.filter(L=>F>L.f).map(L=>L.n);
     A.fb(moved.length?`${NUMS()?`با ${fa(F)} نیوتن، `:""}جعبه روی ${andList(moved)} حرکت کرد.${moved.length<3?" روی بقیه، اصطکاک جلوی حرکت را گرفت.":""}`:"روی هیچ سطحی حرکت نکرد؛ هل آن‌قدر نبود که بر اصطکاک غلبه کند.","info");});});},
 /* مرحله‌ها: هر سه چالش یک ایده (ببین ← امتحان کن ← به کار ببر) */
 kid:[
  {id:"fric.a1",title:"لیز یا زبر؟",desc:"جعبه روی یخ، چوب و فرش. کجا راحت‌تر سُر می‌خورد؟",ch:["fr.far","fr.rough","fr.move20","fr.stuck20","fr.flagW","fr.stop10"]},
  {id:"fric.a2",title:"جعبه را برسان",desc:"سطح را عوض کن تا جعبه درست روی پرچم بایستد.",ch:["fr.flagI","fr.rough","fr.move20","fr.flagW","fr.stuck20","fr.stop10"]}],
 levels:[
  {id:"fric.1",title:"اصطکاک چیست؟",desc:"سطحِ زبرتر اصطکاکِ بیشتری دارد. جعبه را با عوض کردن سطح راه بینداز یا نگه دار.",ch:["fr.far","fr.rough","fr.move20","fr.stuck20","fr.flagW","fr.min.w"]},
  {id:"fric.2",title:"کمترین هل",desc:"جعبه وقتی راه می‌افتد که هل از اصطکاک بیشتر شود. کمترین هل را پیدا کن.",ch:["fr.min.i","fr.only10","fr.min.w","fr.flagI30","fr.min.c","fr.stop30"]},
  {id:"fric.3",title:"قهرمان اصطکاک",desc:"عددهای بزرگ‌تر و پیش‌بینی بدون امتحان.",ch:["fr.stuck40","fr.min.c","fr.flagW40","fr.only10","fr.min.w","fr.flagI30"]}],
 bLv:[0,1],cLv:[1,2],
 endless(r,d){const tp=pick(r,d<2?["far","rough","stuck","move","flag"]:KID()?["stuck","move","flag","stop"]:["stuck","only","flag","stop","min","min"]);
   if(tp==="far")return{t:"fq",q:1,F:20};if(tp==="rough")return{t:"fq",q:3,F:20};if(tp==="stuck")return{t:"fq",q:2,F:pick(r,[20,30])};if(tp==="only")return{t:"fq",q:4,F:10};
   if(tp==="move")return{t:"surf",goal:"move",F:20,start:2};if(tp==="stop")return{t:"surf",goal:"stop",F:pick(r,KID()?[10]:[10,30]),start:0};
   if(tp==="min")return{t:"min",s:pick(r,[0,1,2])};return{t:"surf",goal:"flag",F:pick(r,[20,30,40]),ans:pick(r,[0,1])};},
 mount(sp,A){
  if(sp.t==="fq")return fricChallenge(sp,A);
  if(sp.t==="surf"){const sl=makeSlide(A,{F:sp.F,surf:sp.start==null?null:sp.start,flag:sp.goal==="flag"?slideDist(sp.F,sp.ans):null});A.refresh=()=>sl.render();A.counter("");
    A.formula(`<span class="fl">قانون</span><span>جعبه حرکت می‌کند اگر هل از اصطکاک بیشتر باشد</span>`);
    const K=KID(),Fs=NUMS()?` با ${fa(sp.F)} نیوتن`:"";
    if(sp.goal==="move")A.prompt(K?"جعبه روی فرش تکان نمی‌خورد. سطح را عوض کن تا راه بیفتد.":`جعبه روی فرش${Fs} هل داده می‌شود ولی تکان نمی‌خورد. سطح را عوض کن تا راه بیفتد. هر چند بار خواستی امتحان کن.<small>یک سطح انتخاب کن و «هل بده!» را بزن.</small>`);
    else if(sp.goal==="stop")A.prompt(K?"جعبه روی یخ سُر می‌خورد. سطحی انتخاب کن که جعبه تکان نخورد.":`جعبه روی یخ${Fs} هل داده می‌شود و سُر می‌خورد. سطحی انتخاب کن که جعبه تکان نخورد. هر چند بار خواستی امتحان کن.<small>یک سطح انتخاب کن و «هل بده!» را بزن.</small>`);
    else A.prompt(K?"سطحی انتخاب کن که جعبه درست کنار پرچم بایستد.":`جعبه را${Fs} هل می‌دهیم. سطحی انتخاب کن که جعبه درست کنار پرچم بایستد. هر چند بار خواستی امتحان کن.<small>یک سطح انتخاب کن و «هل بده!» را بزن.</small>`);
    const c=A.ctrl("");const pk=surfPicker(c,sl.st,()=>{sl.reset();A.fb("");});
    const go=btn(c,"هل بده!","go",()=>{if(sl.st.surf==null){A.fb("اول یک سطح انتخاب کن.","info");return;}go.disabled=true;sl.reset();
      sl.run(d=>{const i=sl.st.surf,ok=sp.goal==="move"?d>0:sp.goal==="stop"?d===0:i===sp.ans;
        const nm=SURF[i].n;
        const res=A.trial(ok,{ok:sp.goal==="move"?`روی ${nm} اصطکاک کمتر است؛ هل بر اصطکاک غلبه کرد و جعبه راه افتاد.`:sp.goal==="stop"?`اصطکاکِ ${nm} همهٔ هل را خنثی کرد؛ جعبه تکان نخورد.`:`آفرین! روی ${nm} جعبه درست کنار پرچم ایستاد.`,
          retry:sp.goal==="move"?`روی ${nm} هم اصطکاک جلوی حرکت را گرفت. سطحی لیزتر انتخاب کن.`:sp.goal==="stop"?`روی ${nm} جعبه هنوز سُر خورد. سطحی زبرتر انتخاب کن.`:d===0?"جعبه اصلاً حرکت نکرد. سطحی لیزتر انتخاب کن.":d>slideDist(sp.F,sp.ans)?"جعبه از پرچم رد شد. سطحی زبرتر انتخاب کن.":"جعبه به پرچم نرسید. سطحی لیزتر انتخاب کن.",
          more:"هرچه سطح زبرتر باشد، اصطکاک بیشتر است و جعبه زودتر می‌ایستد.",
          final:`جواب: ${SURF[sp.goal==="flag"?sp.ans:sp.goal==="move"?0:2].n}.`,
          show:()=>{sl.st.surf=sp.goal==="flag"?sp.ans:sp.goal==="move"?0:2;sl.reset();sl.run();}});
        if(res||A.locked)pk.lock();else later(700,()=>{sl.reset();go.disabled=false;});});});
    return;}
  if(sp.t==="min"){const sl=makeSlide(A,{F:5,surf:sp.s});A.refresh=()=>sl.render();A.counter("");const nm=SURF[sp.s].n,ans=minPush(sp.s);
    A.prompt(`کمترین هلی را پیدا کن که جعبه را روی ${nm} راه می‌اندازد. هر چند بار خواستی امتحان کن.<small>اندازهٔ هل را با + و − تنظیم کن و «هل بده!» را بزن. اصطکاکِ این سطح بالای صحنه نوشته شده است.</small>`);
    A.formula(`<span class="fl">قانون</span><span>جعبه راه می‌افتد اگر هل از اصطکاک بیشتر باشد</span>`);
    const c=A.ctrl("");const stp=stepper(c,{init:5,min:5,max:60,steps:[5],unit:"نیوتن هل",label:"اندازهٔ هل",onChange:v=>{sl.st.F=v;sl.reset();A.fb("");}});
    const go=btn(c,"هل بده!","go",()=>{go.disabled=true;sl.reset();sl.run(d=>{const F=sl.st.F,ok=F===ans;
      const res=A.trial(ok,{ok:`${fa(F)} نیوتن از اصطکاکِ ${nm} (${fa(SURF[sp.s].f)} نیوتن) بیشتر است، ولی ${fa(F-5)} نیوتن نبود. پس کمترین هل ${fa(F)} نیوتن است.`,
        retry:d===0?`با ${fa(F)} نیوتن جعبه راه نیفتاد؛ هل هنوز از اصطکاک بیشتر نیست.`:`جعبه راه افتاد، ولی با هل کمتری هم راه می‌افتاد. کمی کمتر امتحان کن.`,
        more:`هل باید فقط کمی از ${fa(SURF[sp.s].f)} نیوتن بیشتر باشد.`,final:`جواب: ${fa(ans)} نیوتن؛ اولین عددی که از ${fa(SURF[sp.s].f)} بیشتر است.`,
        show:()=>{stp.set(ans);sl.st.F=ans;sl.reset();sl.run();}});
      if(res||A.locked)stp.disable();else later(600,()=>{sl.reset();go.disabled=false;});});});
    return;}
 }};

/* فهرست چالش‌ها (سختی: ۰ آسان، ۱ سخت) */
defCh("fric",[
 {id:"fr.far",d:0,teach:"روی سطح لیز، اصطکاک کم است و جعبه دورتر می‌رود.",terms:["اصطکاک"],mk:()=>({t:"fq",q:1,F:20,poe:1})},
 {id:"fr.rough",d:0,teach:"سطحِ زبرتر اصطکاکِ بیشتری دارد.",terms:["اصطکاک"],mk:()=>({t:"fq",q:3,F:20})},
 {id:"fr.move20",d:0,teach:"با کم کردنِ اصطکاک، همان هل جعبه را راه می‌اندازد.",mk:()=>({t:"surf",goal:"move",F:20,start:2})},
 {id:"fr.stuck20",d:0,teach:"اگر اصطکاک به اندازهٔ هل باشد، جعبه تکان نمی‌خورد.",mk:()=>({t:"fq",q:2,F:20})},
 {id:"fr.flagW",d:1,teach:"اصطکاکِ بیشتر یعنی جعبه زودتر می‌ایستد.",mk:()=>({t:"surf",goal:"flag",F:30,ans:1})},
 {id:"fr.flagI",d:0,teach:"روی یخ، جعبه دورتر سُر می‌خورد.",mk:()=>({t:"surf",goal:"flag",F:20,ans:0})},
 {id:"fr.stop10",d:1,teach:"اصطکاک می‌تواند جلوی حرکت را بگیرد؛ اصطکاک همیشه بد نیست.",mk:()=>({t:"surf",goal:"stop",F:10,start:0})},
 {id:"fr.stop30",d:1,teach:"برای نگه داشتنِ جعبه، سطحی لازم است که اصطکاکش از هل بیشتر باشد.",mk:()=>({t:"surf",goal:"stop",F:30,start:0})},
 {id:"fr.only10",d:1,teach:"هل کم فقط روی سطح لیز جعبه را راه می‌اندازد.",mk:()=>({t:"fq",q:4,F:10})},
 {id:"fr.stuck40",d:1,teach:"هل بیشتر بر اصطکاکِ بیشتری غلبه می‌کند.",mk:()=>({t:"fq",q:5,F:40})},
 {id:"fr.flagI30",d:1,teach:"هل بیشتر روی سطح لیز یعنی سُر خوردنِ بیشتر.",mk:()=>({t:"surf",goal:"flag",F:30,ans:0})},
 {id:"fr.flagW40",d:1,teach:"با هل بیشتر، روی سطح زبرتر هم جعبه جلو می‌رود.",mk:()=>({t:"surf",goal:"flag",F:40,ans:1})},
 {id:"fr.min.i",d:1,teach:"هل باید از اصطکاک بیشتر شود تا جعبه راه بیفتد.",mk:()=>({t:"min",s:0})},
 {id:"fr.min.w",d:1,teach:"هل باید از اصطکاک بیشتر شود تا جعبه راه بیفتد.",mk:()=>({t:"min",s:1})},
 {id:"fr.min.c",d:1,teach:"سطح زبرتر هل بیشتری لازم دارد.",mk:()=>({t:"min",s:2})}]);
