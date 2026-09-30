/* ================= ایستگاه قرقره ================= */
const PUL_NAMES_B={1:"یک قرقرهٔ ثابت",2:"ثابت + متحرک (۲ طناب)",4:"چهار قرقره (۴ طناب)",6:"شش قرقره (۶ طناب)"},PUL_NAMES_K={1:"یک قرقرهٔ ثابت",2:"ثابت + متحرک",4:"چهار قرقره",6:"شش قرقره"};
const pulName=k=>(KID()?PUL_NAMES_K:PUL_NAMES_B)[k];
const pulFrac=n=>n===1?"برابر وزن بار":({2:"نصفِ",3:"یک‌سومِ",4:"یک‌چهارمِ",6:"یک‌ششمِ"}[n]||`یک‌${fa(n)}مِ`)+" وزن بار";
function pulleyIcon(n){let s=`<rect x="4" y="1" width="32" height="3" fill="#8A5427"/>`;if(n===1)return s+`<circle cx="20" cy="9" r="5" fill="none" stroke="${INK}" stroke-width="2"/><path d="M15 9 V22 M25 9 V26" stroke="#7A5634" stroke-width="1.6"/><rect x="11" y="21" width="8" height="6" fill="#E0A45F"/>`;
  const k=n/2;for(let i=0;i<n;i++)s+=`<path d="M${8+i*(24/(n-1||1))} 8 V19" stroke="#7A5634" stroke-width="1.5"/>`;return s+`<rect x="6" y="5" width="28" height="5" rx="2" fill="#8C9BB0"/><rect x="6" y="17" width="28" height="5" rx="2" fill="#8C9BB0"/><rect x="14" y="22" width="12" height="5" fill="#E0A45F"/>`;}
function makePulley(A,cfg){const svg=A.svg,P=A.P;A.view(404);const G=380,PXM=60,REST=250,MAXD=150;
  const st={n:cfg.n||1,W:cfg.W,S:cfg.S,h:cfg.h||2,pulled:0,stroke:0,busy:false,blocked:false,flash:0,edit:cfg.edit!==false,hideF:!!cfg.hideF};
  const F=()=>st.W/st.n;const rise=()=>st.pulled/st.n;
  const R=(a,b,c,d)=>`<line x1="${a}" y1="${b}" x2="${c}" y2="${d}" stroke="#7A5634" stroke-width="4" stroke-linecap="round"/>`;
  const Wh=(x,y,r)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="#F4F7FA" stroke="#34425E" stroke-width="5"/><circle cx="${x}" cy="${y}" r="4" fill="#34425E"/>`;
  function render(){const ok=canLift(F(),st.S),y0=G-56-rise()*PXM,hy=REST+st.stroke;let s=bgRoom(G);
    s+=`<rect x="100" y="16" width="440" height="22" rx="6" fill="#8A5427"/><rect x="100" y="16" width="440" height="6" rx="3" fill="#A86A36"/>`;
    const th=G-st.h*PXM;s+=`<line x1="70" y1="${G}" x2="70" y2="${th-26}" stroke="#7D8CA3" stroke-width="4"/><path d="M70 ${th-26} l34 10 -34 10Z" fill="${GRN}"/><line x1="60" y1="${th}" x2="560" y2="${th}" stroke="${GRN}" stroke-width="2" stroke-dasharray="8 6" opacity=".7"/>`+T(82,th+22,NUMS()?`هدف: ${fa(st.h)} متر`:"هدف",{size:13,col:GRN,anchor:"end"});
    let lx,hx,body="";const yp=y0-34;
    if(st.n===1){lx=272;hx=328;body=R(300,38,300,50)+R(272,70,272,y0)+R(328,70,328,hy)+`<path d="M272 70 A28 28 0 0 1 328 70" stroke="#7A5634" stroke-width="4" fill="none"/>`+Wh(300,70,28);}
    else if(st.n===2){lx=304;hx=376;body=R(352,38,352,48)+R(280,38,280,yp)+R(328,yp,328,70)+R(376,70,376,hy)+`<path d="M328 70 A24 24 0 0 1 376 70" stroke="#7A5634" stroke-width="4" fill="none"/><path d="M280 ${yp} A24 24 0 0 0 328 ${yp}" stroke="#7A5634" stroke-width="4" fill="none"/>`+Wh(352,70,24)+Wh(304,yp,24)+R(304,yp,304,y0);}
    else{const k=st.n/2,cs=k===2?[280,336]:[264,308,352],xa=cs[0]-26,wd=cs[k-1]-cs[0]+52;lx=308;hx=cs[k-1]+40;
      body=R(308,38,308,50);cs.forEach(c=>{body+=R(c-16,70,c-16,yp)+R(c+16,70,c+16,yp);});
      body+=`<path d="M${cs[k-1]} 52 Q${hx} 50 ${hx} 74" stroke="#7A5634" stroke-width="4" fill="none"/>`+R(hx,74,hx,hy);
      body+=`<rect x="${xa}" y="50" width="${wd}" height="40" rx="14" fill="#8C9BB0"/><rect x="${xa}" y="${yp-20}" width="${wd}" height="40" rx="14" fill="#8C9BB0"/>`;cs.forEach(c=>{body+=Wh(c,70,16)+Wh(c,yp,16);});body+=R(308,yp+20,308,y0);}
    s+=body;
    const coil=Math.min(60,st.pulled*6);if(coil>0){s+=`<g>`;for(let i=0;i<Math.ceil(coil/6);i++)s+=`<ellipse cx="${hx+74}" cy="${G-4-i*3}" rx="${22-i*.4}" ry="6" fill="none" stroke="#7A5634" stroke-width="3"/>`;s+=`</g>`;}
    s+=R(hx,hy,hx+10,G-6);
    s+=crateSvg(lx,y0+56,64,56,kn(st.W),null);
    if(S.forces){s+=arrow(lx,y0+62,lx,y0+62+Math.min(80,st.W*.5),9,"#7D8CA3",.9);
      const fl=Math.max(24,Math.min(120,F()*1.6));s+=arrow(hx+34,hy+8,hx+34,hy+8+fl,11,st.hideF?"#7D8CA3":ok?GRN:RED)+T(hx+56,hy+30+fl/2,`نیروی لازم<tspan class="num">: ${st.hideF?"؟":fa(r1(F()))}</tspan>`,{size:13,col:st.hideF?INK:ok?GRN:RED,anchor:"end"});}
    const flash=st.flash>0;s+=`<g data-drag="grip" style="cursor:ns-resize"><rect x="${hx-40}" y="${hy-14}" width="80" height="70" fill="#fff" fill-opacity="0"/><rect x="${hx-26}" y="${hy}" width="52" height="40" rx="12" fill="${flash?RED:"#FFC43D"}" stroke="#fff" stroke-width="3"/>${T(hx,hy+28,"⇩",{size:22,col:INK,halo:false})}</g>`;
    s+=gBar(st.hideF?0:F(),st.S,400,70,170);
    
    P.paint(s);
    A.counter(`<span class="cc">طناب‌هایی که بار را نگه می‌دارند: <b>${fa(st.n)}</b></span><span class="cc">طناب کشیدی: <b>${fa(r1(st.pulled))} متر</b></span><span class="cc">بار بالا رفت: <b>${fa(r1(rise()))} متر</b></span><span class="cc ${ok?"":"r"}">نیروی لازم: <b class="num">${st.hideF?"؟":fa(r1(F()))+" نیوتن"}</b></span>`);
    A.formula(FX(`${sy("F")} = ${sy("W")} ÷ ${sy("n")}`,st.hideF?"":`${sy("F")} = ${fa(st.W)} ÷ ${fa(st.n)} = ${fa(r1(F()))} N`,[[sy("F"),"نیروی لازم (N)"],[sy("W"),"وزن بار (N)"],[sy("n"),"تعداد طناب‌های نگه‌دارنده"]])+FX(`${sy("s")} = ${sy("n")} × ${sy("h")}`,`${sy("s")} = ${fa(st.n)} × ${fa(r1(rise()))} = ${fa(r1(st.pulled))} m`,[[sy("s"),"طول طناب کشیده (m)"],[sy("h"),"بالا رفتن بار (m)"]]));}
  let y0drag=0;
  dragKit(svg,{blocked:()=>A.locked||st.busy||!st.edit,start(d){return d.drag==="grip"?{}:null;},begin(g,p){y0drag=p.y;g.base=st.pulled;},
    move(g,p){const dy=clamp(p.y-y0drag,0,MAXD);if(!canLift(F(),st.S)){st.stroke=Math.min(dy,12);st.flash=1;if(cfg.onBlocked)cfg.onBlocked();render();return;}
      const maxPull=st.h*st.n;const want=g.base+dy/PXM;st.pulled=Math.min(maxPull,want);st.stroke=Math.min(dy,(st.pulled-g.base)*PXM);render();},
    end(){st.flash=0;const from=st.stroke;tween(200,p=>{st.stroke=from*(1-p);render();},()=>{st.stroke=0;render();if(rise()>=st.h-1e-6&&cfg.onTop)cfg.onTop();});},tap(){}});
  render();
  return{st,render,F,rise,reset(){st.pulled=0;st.stroke=0;render();}};
}
function pulleyStatic(A,n){const pl=makePulley(A,{n,W:80,S:100,h:2,edit:false});return pl;}
const ST_pulley={key:"pulley",name:"قرقره",c:"#B7791F",sub:"قرقرهٔ ثابت، متحرک و طناب‌های بیشتر",
 intro:"دستگیرهٔ زرد طناب را پایین بکش تا بار بالا برود. هرچه طناب‌های بیشتری بار را نگه دارند، نیروی کمتری لازم است؛ ولی باید طناب بیشتری بکشی.",
 art(){let h=bgRoom(380).replace(/id="g/g,'id="ap').replace(/url\(#g/g,"url(#ap");h+=`<rect x="100" y="16" width="440" height="22" rx="6" fill="#8A5427"/><line x1="352" y1="38" x2="352" y2="48" stroke="#7A5634" stroke-width="4"/><line x1="280" y1="38" x2="280" y2="230" stroke="#7A5634" stroke-width="4"/><line x1="328" y1="230" x2="328" y2="70" stroke="#7A5634" stroke-width="4"/><line x1="376" y1="70" x2="376" y2="300" stroke="#7A5634" stroke-width="4"/><circle cx="352" cy="70" r="24" fill="#F4F7FA" stroke="#34425E" stroke-width="5"/><circle cx="304" cy="230" r="24" fill="#F4F7FA" stroke="#34425E" stroke-width="5"/>`+crateSvg(304,320,64,56,"۸۰",null)+`<rect x="358" y="300" width="36" height="28" rx="10" fill="#FFC43D"/>`+arrow(410,300,410,360,11,GRN);return h;},
 lab(A){A.prompt("آزمایشگاه قرقره: یک سیستم انتخاب کن و دستگیره را پایین بکش. ببین چقدر طناب می‌کشی تا بار ۲ متر بالا برود.");
   let n=2,W=80,Sv=50,pl;const mk=()=>{pl=makePulley(A,{n,W,S:Sv,h:2,onTop:()=>A.fb(`بار ۲ متر بالا رفت و تو ${fa(2*n)} متر طناب کشیدی.`,"ok"),onBlocked:()=>A.fb("نیرویت کافی نیست! سیستمی با طناب‌های بیشتر انتخاب کن.","no")});A.refresh=()=>pl.render();};mk();
   const c=A.ctrl("");c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="sys">${[1,2,4,6].map(k=>`<button class="opt ${k===n?"sel":""}" data-n="${k}" type="button"><svg viewBox="0 0 40 28" aria-hidden="true">${pulleyIcon(k)}</svg>${pulName(k)}</button>`).join("")}</div>`);
   c.querySelector("#sys").onclick=e=>{const b=e.target.closest("[data-n]");if(!b)return;n=+b.dataset.n;c.querySelectorAll("#sys .opt").forEach(x=>x.classList.toggle("sel",x===b));A.fb("");mk();};
   stepper(c,{init:W,min:10,max:200,steps:[10],unit:"وزن بار",onChange:v=>{W=v;mk();}});stepper(c,{init:Sv,min:10,max:100,steps:[5],unit:"نیروی تو",onChange:v=>{Sv=v;mk();}});btn(c,"از اول","",()=>{pl.reset();A.fb("");});},
 kid:[
  {title:"بالا بردن بار",desc:"طناب را بکش و بار را بالا ببر.",gen(){return[{t:"lift",n:1,W:30,S:40,h:2},{t:"fixedk"},{t:"lift",n:2,W:60,S:40,h:1},{t:"count",n:2}];}},
  {title:"قرقرهٔ کمکی",desc:"قرقره‌ای انتخاب کن که بار سنگین را بالا ببرد.",gen(){return[{t:"choose",W:50,S:30,h:1,opts:[1,2]},{t:"lift",n:4,W:120,S:40,h:1},{t:"choose",W:80,S:30,h:1,opts:[1,2,4]},{t:"count",n:4}];}}],
 levels:[
  {title:"قرقرهٔ ثابت و متحرک",desc:"طناب را بکش و بار را بالا ببر. ببین قرقرهٔ ثابت چه می‌کند و قرقرهٔ متحرک چه.",gen(){return[{t:"lift",n:1,W:30,S:40,h:2},{t:"fixedq"},{t:"lift",n:2,W:60,S:40,h:1},{t:"count",n:2},{t:"choose",W:50,S:30,h:1,opts:[1,2]},{t:"calcRope",n:2,h:2}];}},
  {title:"طناب‌های بیشتر",desc:"بار سنگین‌تر، نیروی کم. ساده‌ترین قرقره‌ای را انتخاب کن که با آن بتوانی بار را بالا ببری.",gen(){return[{t:"choose",W:80,S:45,h:1,opts:[1,2,4]},{t:"count",n:4},{t:"calcF",W:80,n:4},{t:"choose",W:100,S:30,h:1,opts:[1,2,4]},{t:"calcRope",n:4,h:1.5},{t:"lift",n:4,W:120,S:35,h:1}];}},
  {title:"سیستم قرقره",desc:"شش طناب، حساب نیرو و طول طناب.",gen(){return[{t:"count",n:6},{t:"choose",W:150,S:30,h:1,opts:[1,2,4,6]},{t:"calcF",W:150,n:6},{t:"calcRope",n:6,h:2},{t:"choose",W:90,S:50,h:1,opts:[1,2,4,6]},{t:"ropeq"}];}},
  {title:"قهرمان قرقره",desc:"همه‌چیز با هم: انتخاب، شمردن و حساب.",gen(r){return[{t:"choose",W:210,S:40,h:1,opts:[1,2,4,6]},{t:"calcF",W:100,n:4},{t:"calcRope",n:4,h:2.5},{t:"count",n:pick(r,[4,6])},{t:"choose",W:130,S:70,h:1,opts:[1,2,4,6]},{t:"calcW",F:25,n:6}];}}],
 endless(r,d){const tp=pick(r,d<2?["lift","choose","count","fixedq"]:["choose","calcF","calcRope","count","calcW"]);const ns=d<2?[1,2]:d<3.5?[1,2,4]:[1,2,4,6];
   if(tp==="lift"){const n=pick(r,ns);const W=ri(r,2,8)*10;return{t:"lift",n,W,S:Math.floor(W/n)+ri(r,1,10),h:pick(r,[1,1.5,2])};}
   if(tp==="count")return{t:"count",n:pick(r,[1,2,4,6])};if(tp==="fixedq")return{t:KID()?"fixedk":"fixedq"};
   if(tp==="calcF"){const n=pick(r,ns.filter(x=>x>1));return{t:"calcF",W:n*ri(r,2,12)*5,n};}
   if(tp==="calcRope")return{t:"calcRope",n:pick(r,ns),h:pick(r,[1,1.5,2,2.5,3])};
   if(tp==="calcW")return{t:"calcW",F:ri(r,2,6)*5,n:pick(r,[2,4,6])};
   for(let k=0;k<50;k++){const W=ri(r,4,20)*10,Sv=ri(r,3,10)*5;const best=ns.find(n=>canLift(W/n,Sv));if(best&&best>1&&!ns.some(n=>W/n===Sv))return{t:"choose",W,S:Sv,h:1,opts:ns};}return{t:"choose",W:80,S:45,h:1,opts:[1,2,4]};},
 mount(sp,A){
  if(sp.t==="fixedk"){const pl=makePulley(A,{n:1,W:30,S:100,h:2,edit:false});A.refresh=()=>pl.render();A.prompt("با این قرقره، طناب را به کدام طرف بکشیم تا بار بالا برود؟");const c=A.ctrl("");const m=mcq(c,["رو به پایین ↓","رو به بالا ↑"],(i,b)=>{if(A.locked)return;if(i===0){m.disable();m.mark(0,"right");A.judge(true,{ok:"طناب را پایین می‌کشیم و بار بالا می‌رود. قرقره جهت را عوض می‌کند."});}else{m.mark(1,"wrong");b.disabled=true;A.judge(false,{retry:"به طنابی که از روی چرخ رد می‌شود نگاه کن.",final:"طناب را پایین می‌کشیم و بار بالا می‌رود."});if(A.locked){m.disable();m.mark(0,"right");}}});return;}
  if(sp.t==="fixedq"||sp.t==="ropeq"){const pl=makePulley(A,{n:sp.t==="fixedq"?1:4,W:60,S:100,h:2,edit:false});A.refresh=()=>pl.render();
    const Q=sp.t==="fixedq"?["قرقرهٔ ثابت چه کمکی به ما می‌کند؟",["نیروی لازم را نصف می‌کند","جهت کشیدن را عوض می‌کند","بار را سبک‌تر می‌کند"],1,"با قرقرهٔ ثابت نیرو همان وزن بار است؛ فقط به‌جای بالا کشیدن، طناب را پایین می‌کشیم که راحت‌تر است."]:["اگر بار را با ۴ طناب ۱ متر بالا ببریم، دست ما چقدر طناب می‌کشد؟",["۱ متر","۴ متر","یک‌چهارم متر"],1,"هر ۴ طناب باید ۱ متر کوتاه شوند؛ پس ۴ متر طناب می‌کشیم. نیروی کمتر، طناب بیشتر."];
    A.prompt(Q[0]);const c=A.ctrl("");const m=mcq(c,Q[1],(i,b)=>{if(A.locked)return;if(i===Q[2]){m.disable();m.mark(i,"right");A.judge(true,{ok:Q[3]});}else{m.mark(i,"wrong");b.disabled=true;A.judge(false,{retry:"به طنابی که از روی قرقره رد می‌شود و جهت کشیدن دستت فکر کن.",final:Q[3]});if(A.locked){m.disable();m.mark(Q[2],"right");}}});return;}
  if(sp.t==="lift"||sp.t==="choose"){const HX={1:328,2:376,4:376,6:392};const nn=sp.t==="lift"?sp.n:sp.opts[0];A.hint(`M${HX[nn]} 264 L${HX[nn]} 400`);}
  if(sp.t==="lift"){A.prompt(KID()?"طناب را پایین بکش تا بار به خط سبز برسد.":`بار را تا خط سبز بالا ببر (${fa(sp.h)} متر).<small>دستگیرهٔ زرد را پایین بکش؛ هر بار رها کنی، دوباره بالا می‌آید.</small>`);
    const pl=makePulley(A,{n:sp.n,W:sp.W,S:sp.S,h:sp.h,onTop:()=>{A.judge(true,{k:{ok:"بار به خط سبز رسید!"},ok:`بار ${fa(sp.h)} متر بالا رفت و تو ${fa(sp.h*sp.n)} متر طناب کشیدی (${fa(sp.h)} × ${fa(sp.n)}).`});}});A.refresh=()=>pl.render();A.ctrl("");return;}
  if(sp.t==="choose"){const best=sp.opts.find(n=>canLift(sp.W/n,sp.S));A.prompt(KID()?"قرقره‌ای انتخاب کن که نیرویت کافی باشد. بعد طناب را بکش. هر چند بار خواستی امتحان کن.":`بار ${fa(sp.W)} نیوتنی را تا خط سبز ببر. نیروی تو <b>${fa(sp.S)} نیوتن</b> است.<small>ساده‌ترین قرقره‌ای را انتخاب کن که نیرویت کافی باشد، بعد طناب را بکش.</small>`);
    let pl,n=sp.opts[0],blockedOnce=false;const mk=()=>{pl=makePulley(A,{n,W:sp.W,S:sp.S,h:sp.h,onBlocked:()=>{if(!blockedOnce){blockedOnce=true;const r=(KID()?A.trial:A.judge)(false,{k:{ok:"بار بالا رفت!",retry:"نیرویت کافی نیست. یکی دیگر را انتخاب کن.",final:"باید قرقره‌ای با طناب‌های بیشتر انتخاب می‌کردی."},retry:"نیرویت کافی نیست! قرقره‌ای با طناب‌های بیشتر انتخاب کن.",final:`باید «${pulName(best)}» را انتخاب می‌کردی: ${fa(sp.W)} ÷ ${fa(best)} = ${fa(r1(sp.W/best))} نیوتن.`});}},
      onTop:()=>{const b=KID()||n===best;(KID()?A.trial:A.judge)(true,{k:{ok:"بار بالا رفت!",retry:"نیرویت کافی نیست. یکی دیگر را انتخاب کن.",final:"باید قرقره‌ای با طناب‌های بیشتر انتخاب می‌کردی."},ok:b?`ساده‌ترین قرقرهٔ لازم را انتخاب کردی. نیروی لازم ${fa(r1(sp.W/n))} نیوتن بود.`:`بالا رفت، ولی «${pulName(best)}» هم کافی بود و طناب کمتری می‌کشیدی.`,pts:b?undefined:1});}});A.refresh=()=>pl.render();};mk();
    const c=A.ctrl("");c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="sys">${sp.opts.map(k=>`<button class="opt ${k===n?"sel":""}" data-n="${k}" type="button"><svg viewBox="0 0 40 28" aria-hidden="true">${pulleyIcon(k)}</svg>${pulName(k)}</button>`).join("")}</div>`);
    c.querySelector("#sys").onclick=e=>{if(A.locked)return;const b=e.target.closest("[data-n]");if(!b)return;n=+b.dataset.n;blockedOnce=false;c.querySelectorAll("#sys .opt").forEach(x=>x.classList.toggle("sel",x===b));mk();};return;}
  if(sp.t==="count"){const pl=makePulley(A,{n:sp.n,W:60,S:100,h:2,edit:false,hideF:true});const hideN=()=>A.counter(`<span class="cc">طناب‌هایی که بار را نگه می‌دارند: <b>؟</b></span>`);A.refresh=()=>{pl.render();hideN();};hideN();
    A.prompt(KID()?"چند طناب بار را نگه داشته‌اند؟ بشمار.":"چند تکه طناب بار را نگه داشته‌اند؟<small>طناب‌هایی را بشمار که به قرقرهٔ پایینی (یا خود بار) وصل‌اند. طنابی که دست می‌کشد را نشمار.</small>");
    const c=A.ctrl("");const stp=stepper(c,{init:0,max:10,steps:[1],unit:"طناب"});const chk=btn(c,"بررسی","go",()=>{const ok=stp.get()===sp.n;A.judge(ok,{k:{ok:"درست شمردی! هرچه طناب بیشتر، کشیدن آسان‌تر."},ok:`${fa(sp.n)} طناب؛ پس نیروی لازم ${pulFrac(sp.n)} است.`,retry:"فقط طناب‌های بین قرقره‌های بالا و پایین را بشمار.",final:`${fa(sp.n)} طناب بار را نگه داشته‌اند.`});if(A.locked){chk.disabled=true;stp.disable();pl.st.hideF=false;A.refresh=()=>pl.render();pl.render();}});return;}
  const pl=makePulley(A,{n:sp.n,W:sp.W||(sp.F?sp.F*sp.n:60),S:100,h:sp.h||2,edit:false,hideF:true});A.refresh=()=>pl.render();
  let q,ans,unit,steps,expl,retry;
  if(sp.t==="calcF"){q=`بار ${fa(sp.W)} نیوتن است و ${fa(sp.n)} طناب آن را نگه داشته‌اند. نیروی لازم چقدر است؟`;ans=sp.W/sp.n;unit="نیوتن";steps=[1,10];expl=`${fa(sp.W)} ÷ ${fa(sp.n)} = ${fa(r1(ans))} نیوتن.`;retry="وزن بار را بر تعداد طناب‌ها تقسیم کن.";}
  else if(sp.t==="calcRope"){q=`با ${fa(sp.n)} طناب، برای اینکه بار ${fa(sp.h)} متر بالا برود، چند متر طناب باید بکشیم؟`;ans=sp.n*sp.h;unit="متر";steps=[.5,1];expl=`${fa(sp.h)} × ${fa(sp.n)} = ${fa(ans)} متر.`;retry="بالا رفتن بار را در تعداد طناب‌ها ضرب کن.";}
  else{q=`با ${fa(sp.n)} طناب و نیروی ${fa(sp.F)} نیوتن، سنگین‌ترین باری که می‌توانی نگه داری چند نیوتن است؟<small>برای بالا بردنش، کمی نیروی بیشتر لازم است.</small>`;ans=sp.F*sp.n;unit="نیوتن";steps=[5,10];expl=`${fa(sp.F)} × ${fa(sp.n)} = ${fa(ans)} نیوتن.`;retry="نیرو را در تعداد طناب‌ها ضرب کن.";}
  A.prompt(q);const c=A.ctrl("");const stp=stepper(c,{init:0,max:500,steps,unit});
  const chk=btn(c,"بررسی","go",()=>{const ok=Math.abs(stp.get()-ans)<.051;A.judge(ok,{ok:expl,retry,final:expl});if(A.locked){chk.disabled=true;stp.disable();pl.st.hideF=false;pl.render();}});
 }};
