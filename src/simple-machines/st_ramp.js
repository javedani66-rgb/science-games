/* ================= ایستگاه سطح شیب‌دار ================= */
/* بالا بردن: نیروی لازم باید از نیروی تو کمتر باشد (در حالت برابر، بار فقط نگه داشته می‌شود) */
function canLift(F,Sv){return F<Sv-1e-9;}
function gBar(F,Sv,x0,y,w){const ok=canLift(F,Sv),fw=Math.min(w,F/(Sv*2)*w);return `<g transform="translate(${x0} ${y})"><rect width="${w}" height="22" rx="11" fill="#fff" stroke="#C7D3DE" stroke-width="2"/>${F>0?`<rect x="${w-fw}" y="3" width="${fw}" height="16" rx="8" fill="${ok?GRN:RED}"/>`:""}<line x1="${w/2}" y1="-5" x2="${w/2}" y2="27" stroke="${INK}" stroke-width="3"/></g>`+T(x0+w/2,y+48,`نیروی تو<tspan class="num">: ${fa(Sv)}</tspan>`,{size:12})+T(x0+w-2,y-10,"نیروی لازم",{size:11,col:MUT,anchor:"start"});}
const r1=v=>Math.round(v*10)/10;
function makeRamp(A,cfg){cfg=machineScene(A,cfg);const svg=A.svg,P=A.P;A.view(404);const PM=70,G=380,DX=470;const H=cfg.H||1;
  const st={L:cfg.L||Math.max(H,2),W:cfg.W,S:cfg.S,t:0,onTop:false,busy:false,edit:cfg.edit!==false,hide:!!cfg.hide};
  const F=()=>MACHINE.ramp(st.W,H,st.L);
  function geo(){const top=G-H*PM,run=Math.sqrt(Math.max(0,st.L*st.L-H*H))*PM,x0=DX-run;return{top,run,x0,ang:Math.atan2(H*PM,Math.max(run,1e-6))};}
  function render(){if(!cfg.current())return;const g=geo(),f=F(),ok=st.hide||canLift(f,st.S),fs=st.hide?"؟":fa(r1(f));let s=bgOut(G);
    s+=`<rect x="${DX}" y="${g.top}" width="${640-DX}" height="${G-g.top}" fill="#B8C1CC"/><rect x="${DX}" y="${g.top}" width="${640-DX}" height="8" fill="#8C97A6"/>`+[0,1,2,3].map(i=>`<rect x="${DX+10+i*40}" y="${g.top+14}" width="18" height="${G-g.top-22}" fill="#A5AFBB"/>`).join("");
    if(NUMS())s+=T(DX+85,(g.top+G)/2+6,`ارتفاع ${fa(H)} متر`,{size:13,col:INK,haloCol:"#DDE3EA"});
    const SZ=40;let bx,by,rot=0;
    if(st.L>H+1e-9){s+=`<polygon points="${g.x0},${G} ${DX},${g.top} ${DX},${g.top+8} ${g.x0+14},${G}" fill="#C98A4B"/><line x1="${g.x0}" y1="${G}" x2="${DX}" y2="${g.top}" stroke="#EAB47C" stroke-width="4"/>`;
      const mx=g.x0+(DX-g.x0)*.62,my=G-(G-g.top)*.62,nx=Math.sin(g.ang)*34,ny=Math.cos(g.ang)*34;if(NUMS())s+=g.run>=260?T(mx+nx,my+ny+6,`طول: ${fa(st.L)} متر`,{size:14,col:"#6B4A2B",rot:-g.ang*180/Math.PI}):T(g.x0-30,G-14,`طول: ${fa(st.L)} متر`,{size:14,col:"#6B4A2B",anchor:"start"});
      const len=Math.hypot(g.run,H*PM),d0=SZ/2+6,d1=len-SZ/2-2,d=d0+(d1-d0)*st.t;bx=g.x0+Math.cos(g.ang)*d;by=G-Math.sin(g.ang)*d;rot=-g.ang*180/Math.PI;}
    else{bx=DX-26;by=G-st.t*H*PM;}
    if(st.onTop){bx=DX+40;by=g.top;rot=0;}
    const th=rot*Math.PI/180;s+=`<g transform="translate(${bx} ${by}) rotate(${rot})">${crateSvg(0,0,SZ,SZ,kn(st.W),null)}</g>`;
    if(S.forces&&!st.onTop){const vert=st.L<=H+1e-9,cx=bx+Math.sin(th)*SZ/2,cy=by-Math.cos(th)*SZ/2,fl=Math.max(22,Math.min(120,f*1.5)),ux=vert?0:Math.cos(th),uy=vert?-1:Math.sin(th);
      s+=arrow(cx+ux*(SZ/2+4),cy+uy*(SZ/2+4),cx+ux*(SZ/2+4+(st.hide?50:fl)),cy+uy*(SZ/2+4+(st.hide?50:fl)),11,st.hide?"#7D8CA3":ok?GRN:RED)+T(cx+ux*(SZ/2+4+(st.hide?50:fl))-12,cy+uy*(SZ/2+4+(st.hide?50:fl))-20,`نیروی لازم<tspan class="num">: ${fs}</tspan>`,{size:13,col:st.hide?INK:ok?GRN:RED,anchor:"start"});
      {const wl=Math.min(90,st.W*.7,G-30-(cy+6));if(wl>=14)s+=arrow(cx,cy+6,cx,cy+6+wl,7,"#7D8CA3",.85);}}
    if(st.edit&&!st.onTop&&!st.busy){s+=`<g data-drag="end" style="cursor:ew-resize"><circle cx="${g.x0}" cy="${G}" r="34" fill="#fff" fill-opacity="0"/><circle cx="${g.x0}" cy="${G}" r="21" fill="#FFC43D" stroke="#fff" stroke-width="3"/>${T(g.x0,G+7,"⟷",{size:20,col:INK,halo:false})}</g>`;}
    s+=gBar(st.hide?0:f,st.S,180,36,260);
    
    machinePaint(A,s);
    machineKeys(A,'[data-drag="end"]',"تغییر طول سطح؛ راست کوتاه‌تر، چپ بلندتر",key=>{if(st.busy||!st.edit||st.onTop)return;st.L=clamp(st.L+(key==="ArrowRight"||key==="ArrowUp"?-.5:.5),H,6);st.t=0;render();if(cfg.onChange)cfg.onChange();});
    A.counter(`<span class="cc">طول سطح: <b>${fa(st.L)} متر</b></span><span class="cc">وزن جعبه: <b class="num">${fa(st.W)} نیوتن</b></span><span class="cc ${ok?"":"r"}">نیروی لازم: <b class="num">${st.hide?fs:fs+" نیوتن"}</b></span><span class="cc">نیروی تو: <b class="num">${fa(st.S)} نیوتن</b></span>`);
    A.formula(FX(`${sy("F")} × ${sy("L")} = ${sy("W")} × ${sy("h")}`,st.hide?"":`${sy("F")} = ${fa(st.W)} × ${fa(H)} ÷ ${fa(st.L)} = ${fa(r1(f))} N`,[[sy("F"),"نیروی لازم (N)"],[sy("L"),"طول سطح شیب‌دار (m)"],[sy("W"),"وزن جعبه (N)"],[sy("h"),"ارتفاع (m)"]]));}
  dragKit(svg,{blocked:()=>A.locked||st.busy||!st.edit,start(d){return d.drag==="end"?{}:null;},begin(){},
    move(g,p){const run=clamp(DX-p.x,0,420)/PM;let L=Math.sqrt(run*run+H*H);L=clamp(Math.round(L*2)/2,H,6);if(L!==st.L){st.L=L;st.t=0;render();if(cfg.onChange)cfg.onChange();}},end(){render();},tap(){}});
  render();
  return{st,render,F,pull(done){const ok=canLift(F(),st.S);st.busy=true;
    if(ok)tween(1800,p=>{st.t=ease(p);render();},()=>{st.onTop=true;render();st.busy=false;done&&done(true);});
    else tween(1300,p=>{st.t=.3*Math.sin(p*Math.PI);render();},()=>{st.t=0;st.busy=false;render();done&&done(false);});},
    reset(){st.t=0;st.onTop=false;render();}};
}
function twoRamps(A,q){A.view(404);const P=A.P,G=380,PM=60,DX=470,top=G-PM;let s=bgOut(G);
  s+=`<rect x="${DX}" y="${top}" width="170" height="${PM}" fill="#B8C1CC"/><rect x="${DX}" y="${top}" width="170" height="7" fill="#8C97A6"/>`;
  const rmp=(L,lab,col)=>{const run=Math.sqrt(L*L-1)*PM,x0=DX-run;return `<polygon points="${x0},${G} ${DX},${top} ${DX},${top+7} ${x0+12},${G}" fill="${col}" opacity=".95"/>`+T(x0+run*.35,G-run*.35*Math.tan(Math.atan2(PM,run))-14,lab,{size:18,col:INK,anchor:"start"});};
  if(q===3){s+=rmp(4,NUMS()?"سطح شیب‌دار ۴ متری":"سطح شیب‌دار","#C98A4B")+`<path d="M${DX-40} ${G} V${top-10}" stroke="${BLUE}" stroke-width="4" stroke-dasharray="6 5"/>`+T(DX-40,top-22,"مستقیم بالا",{size:15,col:BLUE});}
  else s+=rmp(5,"ب","#C98A4B")+rmp(1.6,"الف","#9C6A3A");
  s+=`<g transform="translate(${DX+60} ${top})">${crateSvg(0,0,40,40,kn(60),null)}</g>`;
  P.paint(s);}
const ST_ramp={key:"ramp",name:"سطح شیب‌دار",c:"#0F9488",sub:"نیروی کمتر، راه بیشتر",
 intro:"سر پایین سطح شیب‌دار را روی زمین بکش تا درازتر یا کوتاه‌تر شود. نوار نیرو بالای صحنه نشان می‌دهد نیرویت کافی است یا نه. سطحی پیدا کن که جعبه با آن بالا برود. در این بازی اصطکاک را حساب نمی‌کنیم.",
 art(){let h=bgOut(380).replace(/id="go"/,'id="ar"').replace(/url\(#go\)/,"url(#ar)");h+=`<rect x="470" y="310" width="170" height="70" fill="#B8C1CC"/><polygon points="120,380 470,310 470,318 134,380" fill="#C98A4B"/>`;const a=-Math.atan2(70,350)*180/Math.PI;h+=`<g transform="translate(300 346) rotate(${a})">${crateSvg(0,0,40,40,"۶۰",null)}</g>`+arrow(330,322,410,306,11,GRN);return h;},
 lab(A){A.prompt("آزمایشگاه سطح شیب‌دار: طول سطح را با کشیدن دایرهٔ زرد عوض کن و «بکش!» را بزن. وزن جعبه و نیروی خودت را هم می‌توانی عوض کنی.");
   let W=60,Sv=30,rp=makeRamp(A,{W,S:Sv,L:2.5});A.refresh=()=>rp.render();const c=A.ctrl("");
   stepper(c,{init:W,min:10,max:200,steps:[10],unit:"وزن جعبه",onChange:v=>{if(!rp.st.busy){rp.st.W=v;rp.reset();}}});stepper(c,{init:Sv,min:10,max:100,steps:[5],unit:"نیروی تو",onChange:v=>{if(!rp.st.busy){rp.st.S=v;rp.reset();}}});
   const b=btn(c,"بکش!","go",()=>{b.disabled=true;c.querySelectorAll(".stp button").forEach(x=>x.disabled=true);rp.pull(ok=>{A.fb(ok?`جعبه بالا رفت. نیروی لازم ${fa(r1(rp.F()))} بود و جعبه ${fa(rp.st.L)} متر راه رفت.`:"نیرویت کافی نبود و جعبه سُر خورد پایین. سطح را درازتر کن.",ok?"ok":"no");later(1200,()=>{rp.reset();b.disabled=false;c.querySelectorAll(".stp button").forEach(x=>x.disabled=false);});});});},
 kid:[
  {id:"ramp.a1",title:"راه طولانی‌تر، نیروی کمتر",desc:"سطح شیب‌دار بساز و ببین کدام راحت‌تر است.",gen(){return[{t:"fit",W:60,S:35},{t:"cmp",q:1},{t:"fit",W:80,S:50},{t:"cmp",q:3},{t:"cmp",q:2}];}},
  {id:"ramp.a2",title:"سطح شیب‌دار بساز",desc:"سطح را آن‌قدر دراز کن که جعبه بالا برود.",gen(){return[{t:"fit",W:90,S:35},{t:"fit",W:100,S:45},{t:"cmp",q:1},{t:"fit",W:70,S:25},{t:"fit",W:120,S:25}];}}],
 levels:[
  {id:"ramp.1",title:"راه طولانی‌تر، نیروی کمتر",desc:"دو سطح شیب‌دار را مقایسه کن و سطحی بساز که با آن بتوانی جعبه را بالا ببری.",gen(){return[{t:"fit",W:60,S:35},{t:"cmp",q:1},{t:"fit",W:80,S:30},{t:"cmp",q:2},{t:"fit",W:100,S:45},{t:"cmp",q:3}];}},
  {id:"ramp.2",title:"طول درست",desc:"طول سطح را تغییر بده، نتیجه را مقایسه کن و نیروی لازم را حساب کن.",gen(){return[{t:"fit",W:90,S:25},{t:"calcF",W:60,L:3},{t:"fit",W:120,S:35},{t:"calcF",W:100,L:4},{t:"cmp",q:2},{t:"fit",W:70,S:25}];}},
  {id:"ramp.3",title:"فرمول سطح شیب‌دار",desc:"نیرو × طول سطح = وزن × ارتفاع. طول لازم را حساب کن و بساز.",gen(){return[{t:"cmp",q:1},{t:"fit",W:90,S:30},{t:"calcL",W:90,S:30},S.track==="b"?{t:"calcF",W:90,L:6}:{t:"work"},{t:"fit",W:150,S:35},{t:"calcF",W:120,L:6},{t:"calcL",W:80,S:20},{t:"fit",W:110,S:25}];}},
  {id:"ramp.4",title:"قهرمان سطح شیب‌دار",desc:"سکوی بلندتر (۲ متر) و عددهای بزرگ‌تر.",gen(){return[{t:"cmp",q:1},{t:"fit",W:60,S:25,H:2},{t:"calcF",W:90,L:6,H:2},{t:"fit",W:100,S:45,H:2},{t:"calcL",W:120,S:40,H:2},{t:"work"},{t:"fit",W:80,S:30,H:2}];}}],
 endless(r,d){const tp=pick(r,d<2?["cmp","fit"]:["fit","calcF","calcL","fit"]);const H=d>3.5&&r()<.5?2:1;
   if(tp==="cmp")return{t:"cmp",q:pick(r,[1,2,3])};const Ls=[];for(let L=H;L<=6;L+=.5)Ls.push(L);
   for(let k=0;k<100;k++){const W=ri(r,4,15)*10,L=pick(r,Ls.filter(x=>x>H));const f=W*H/L;if(tp==="calcF"&&Number.isInteger(f))return{t:"calcF",W,L,H};if(tp==="calcL"){const S=pick(r,[10,15,20,25,30,40]);const Lm=W*H/S;if(Number.isInteger(Lm*2)&&Lm>H&&Lm<=6)return{t:"calcL",W,S,H};}if(tp==="fit"){const S=ri(r,2,10)*5,mL=minL(W,S,H);if(mL&&mL>H&&!Number.isInteger(W*H/S*2))return{t:"fit",W,S,H};}}
   return{t:"fit",W:60,S:30};},
 mount(sp,A){const H=sp.H||1;
  if(sp.t==="cmp"){
    const lengths=sp.q===3?[1,4]:[1.5,5],seen=new Set();let busy=false,rp;
    const draw=j=>{rp=makeRamp(A,{W:60,S:100,L:lengths[j],H:1,edit:false});A.refresh=()=>rp.render();};draw(0);
    A.prompt(machineRule("همان جعبه را تا همان ارتفاع با دو راه بالا می‌بریم. هر دو آزمایش را ببین؛ فقط طول راه تغییر می‌کند.","همان جعبه را تا همان سکو بالا می‌بریم. هر دو راه را آزمایش کن."));
    const c=A.ctrl("");[0,1].forEach(j=>btn(c,j===0?"آزمایش الف":"آزمایش ب","",()=>{if(busy||A.locked)return;busy=true;draw(j);rp.pull(()=>{busy=false;seen.add(j);A.fb(KID()?(j===0?"راه الف کوتاه‌تر است و نیروی بیشتری می‌خواهد.":"راه ب بلندتر است و نیروی کمتری می‌خواهد."):`راه ${j===0?"الف":"ب"}: طول ${fa(lengths[j])} متر؛ نیروی لازم ${fa(r1(60/lengths[j]))} نیوتن. ارتفاع هر دو ۱ متر است.`,"info");if(seen.size===2)ask();});}));
    function ask(){const Q=sp.q===2?["در کدام آزمایش، جعبه راه بیشتری رفت؟",2]:sp.q===3?["کدام راه نیروی بیشتری خواست؟",0]:["در کدام آزمایش، نیروی کمتری لازم بود؟",2];
      A.prompt(Q[0]);const c2=A.ctrl("");const m=mcq(c2,["الف","هر دو یکسان","ب"],(i,bt)=>{if(A.locked)return;const ex="همان جعبه تا همان ارتفاع بالا رفت؛ راه ب بلندتر بود و نیروی کمتری خواست.";if(i===Q[1]){m.disable();m.mark(i,"right");A.judge(true,{ok:ex});}else{bt.disabled=true;A.judge(false,{retry:"نتیجهٔ دو آزمایش را مقایسه کن: ب بلندتر بود و نیروی کمتری خواست.",final:ex});if(A.locked){m.disable();m.mark(Q[1],"right");}}});}
    return;}
  if(sp.t==="work"){twoRamps(A,3);A.counter("");A.formula(FX(`${sy("W")}<sub>کار</sub> = ${sy("F")} × ${sy("d")}`,"",[[sy("F"),"نیرو (N)"],[sy("d"),"جابه‌جایی (m)"],["یکای کار","ژول (J)"]]));A.prompt("جعبهٔ ۶۰ نیوتنی را یک بار مستقیم ۱ متر بالا می‌بریم (نیرو ۶۰) و یک بار روی سطح ۴ متری هل می‌دهیم (نیرو ۱۵). در کدام حالت «کار» بیشتری انجام داده‌ایم؟ (کار = نیرو × جابه‌جایی؛ اصطکاک را حساب نکن.)");
    const c=A.ctrl("");const m=mcq(c,["مستقیم بالا","هر دو یکسان","سطح شیب‌دار"],(i,b)=>{if(A.locked)return;const ex="مستقیم: ۶۰ × ۱ = ۶۰. سطح شیب‌دار: ۱۵ × ۴ = ۶۰. کار یکسان است؛ ماشین ساده کار را کم نمی‌کند، نیرو را کم می‌کند. در واقعیت اصطکاک کار روی سطح شیب‌دار را کمی بیشتر هم می‌کند.";if(i===1){m.disable();m.mark(i,"right");A.judge(true,{ok:ex});}else{m.mark(i,"wrong");b.disabled=true;A.judge(false,{retry:"برای هر کدام نیرو را در جابه‌جایی ضرب کن.",final:ex});if(A.locked){m.disable();m.mark(1,"right");}}});return;}
  if(sp.t==="fit"){const mL=minL(sp.W,sp.S,H);const L0=Math.min(6,H+1),x0=470-Math.sqrt(L0*L0-H*H)*70;A.hint(`M${x0} 380 L${x0-160} 380`);
    A.prompt(machineRule(`جعبهٔ ${fa(sp.W)} نیوتنی را تا سکوی ${fa(H)} متری بالا ببر. نیروی تو ${fa(sp.S)} نیوتن است. طول سطح را تغییر بده و «بکش!» را بزن. هدف، بالا رفتن جعبه است.`,"سطح را دراز کن و «بکش!» را بزن تا جعبه بالا برود. آزمایش‌های ناموفق امتیاز کم نمی‌کنند."));
    const rp=makeRamp(A,{W:sp.W,S:sp.S,L:L0,H});A.refresh=()=>rp.render();const c=A.ctrl("");
    const go=btn(c,"بکش!","go",()=>{go.disabled=true;const L=rp.st.L;rp.pull(ok=>{
      if(ok){machineSuccess(A,`جعبه تا ارتفاع ${fa(H)} متر بالا رفت. نیروی لازم ${fa(r1(rp.F()))} نیوتن و راه جعبه ${fa(L)} متر بود.`,"جعبه بالا رفت! راه بلندتر کمک کرد با نیروی کمتری آن را بالا ببری.");return;}
      machineGuide(A,"جعبه بالا نرفت؛ نیروی تو کافی نبود. سطح را درازتر کن.","ارتفاع و جعبه ثابت‌اند. با طول بیشتر، نیروی لازم کمتر می‌شود.",KID()?"با راه بلندتر جعبه بالا می‌رود.":`با طول ${fa(mL)} متر، نیروی لازم ${fa(r1(MACHINE.ramp(sp.W,H,mL)))} نیوتن است.`,()=>{rp.st.L=mL;rp.st.t=1;rp.st.onTop=true;rp.render();});
      if(!A.locked)later(700,()=>{if(!A.locked){rp.reset();go.disabled=false;}});
    });});return;}
  if(sp.t==="calcF"||sp.t==="calcL"){const cf=sp.t==="calcF",ans=cf?MACHINE.ramp(sp.W,H,sp.L):sp.W*H/sp.S;
    const rp=makeRamp(A,{W:sp.W,S:cf?Math.floor(ans/5)*5+5:sp.S,L:cf?sp.L:H,H,edit:false,hide:true});A.refresh=()=>rp.render();
    A.prompt(machineRule(cf?`جعبهٔ ${fa(sp.W)} نیوتنی، سطح شیب‌دار ${fa(sp.L)} متری و ارتفاع ${fa(H)} متر. برای هل دادن جعبه چه مقدار نیرو لازم است؟ (نیرو × طول سطح = وزن × ارتفاع)`:`نیروی تو ${fa(sp.S)} نیوتن است، جعبه ${fa(sp.W)} نیوتن و ارتفاع ${fa(H)} متر. با سطح شیب‌دار چند متری، نیروی لازم درست برابر نیروی تو می‌شود؟ (نیرو × طول سطح = وزن × ارتفاع) با سطحی کمی درازتر از این، جعبه بالا می‌رود.`));
    const c=A.ctrl("");const stp=stepper(c,{init:0,max:cf?300:10,steps:cf?[.1,1,10]:[.1,.5,1],unit:cf?"نیوتن":"متر"});
    const chk=btn(c,"بررسی","go",()=>{const ok=Math.abs(stp.get()-ans)<.051;A.judge(ok,{ok:cf?`${fa(sp.W)} × ${fa(H)} ÷ ${fa(sp.L)} = ${fa(r1(ans))} نیوتن.`:`${fa(sp.W)} × ${fa(H)} ÷ ${fa(sp.S)} = ${fa(ans)} متر؛ با سطحی کمی درازتر از این، جعبه بالا می‌رود.`,retry:cf?"وزن را در ارتفاع ضرب کن و بر طول سطح تقسیم کن.":"وزن را در ارتفاع ضرب کن و بر نیروی خودت تقسیم کن.",final:cf?`نیرو = ${fa(sp.W)} × ${fa(H)} ÷ ${fa(sp.L)} = ${fa(r1(ans))} نیوتن.`:`طول = ${fa(sp.W)} × ${fa(H)} ÷ ${fa(sp.S)} = ${fa(ans)} متر.`});
      if(A.locked){chk.disabled=true;stp.disable();rp.st.hide=false;if(!cf)rp.st.L=Math.min(6,ans+.5);rp.render();if(canLift(rp.F(),rp.st.S))rp.pull();}});return;}
 }};
function minL(W,Sv,H){for(let L=H;L<=6+1e-9;L+=.5)if(canLift(W*H/L,Sv))return L;return null;}

machinePacks("ramp",[...ST_ramp.kid,...ST_ramp.levels]);
