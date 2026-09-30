"use strict";
/* ================= ابزار عمومی ================= */
const FA="۰۱۲۳۴۵۶۷۸۹";
const fa=v=>{const s=typeof v==="number"?String(Math.round(v*100)/100):String(v);return s.replace(/-/g,"−").replace(/\d/g,d=>FA[d]).replace(/\./g,"٫");};
const $=s=>document.querySelector(s);
const app=$("#app");
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const lerp=(a,b,t)=>a+(b-a)*t;
const ease=p=>p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
const hash=s=>{let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619);return h>>>0;};
const ri=(r,a,b)=>a+Math.floor(r()*(b-a+1));
const pick=(r,a)=>a[Math.floor(r()*a.length)];
const shuffle=(r,a)=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const andList=a=>a.length===1?a[0]:a.slice(0,-1).join("، ")+" و "+a[a.length-1];
const reduceMotion=matchMedia("(prefers-reduced-motion: reduce)").matches;
let epoch=0;
function tween(dur,step,done){const my=epoch;if(reduceMotion)dur=1;const t0=performance.now();function f(now){if(my!==epoch)return;const p=Math.min(1,(now-t0)/dur);step(p);if(p<1)requestAnimationFrame(f);else if(done)done();}requestAnimationFrame(f);}
const later=(ms,fn)=>{const my=epoch;setTimeout(()=>{if(my===epoch)fn();},reduceMotion?0:ms);};

/* ================= ذخیره ================= */
const KEY="sm-workshop-v3";
let S={prog:{},nums:true,forces:true,formula:true,track:null};
/* هر بازیکن پیشرفت جدا دارد؛ چند بچه می‌توانند روی یک دستگاه بازی کنند */
const JKEY="sm-journey-v1";let DB={profiles:[],cur:null,week:null};
const TESTMODE=typeof window!=="undefined"&&!!window.__TEST;
if(TESTMODE){try{const d=JSON.parse(localStorage.getItem(KEY)||"null");if(d&&d.prog)S=Object.assign(S,d);}catch(e){}}
else{try{const d=JSON.parse(localStorage.getItem(JKEY)||"null");if(d&&d.profiles)DB=Object.assign(DB,d);}catch(e){}}
const curP=()=>DB.profiles.find(p=>p.id===DB.cur)||null;
function useProfile(p){DB.cur=p?p.id:null;if(p)S=p.S;}
if(!TESTMODE&&curP())S=curP().S;
const save=()=>{try{if(TESTMODE){localStorage.setItem(KEY,JSON.stringify(S));return;}const p=curP();if(p)p.S=S;localStorage.setItem(JKEY,JSON.stringify(DB));}catch(e){}};
const PG=k=>{const key=(S.track||"c")+":"+k;return S.prog[key]||(S.prog[key]={lv:[0,0,0,0,0],best:0});};
const KID=()=>S.track==="a";
const NUMS=()=>S.nums&&!KID();
const kn=v=>KID()?"":fa(v);
const starsOfSt=k=>PG(k).lv.reduce((a,b)=>a+b,0);
const applyNums=()=>{document.body.classList.toggle("nonum",!NUMS());document.body.classList.remove("tr-a","tr-b","tr-c");if(S.track)document.body.classList.add("tr-"+S.track);};
/* فرمول چپ‌به‌راست با نماد */
const sy=(s,sub)=>`<i>${s}</i>${sub?`<sub>${sub}</sub>`:""}`;
function FX(eq,sub,lg){return `<span class="fl">فرمول</span><span class="eqx" dir="ltr">${eq}</span>${sub?`<span class="eqx sub num" dir="ltr">${sub}</span>`:""}${lg?`<span class="lg">${lg.map(([s,m])=>`<span class="lgi"><span dir="ltr">${s}</span>: ${m}</span>`).join("")}</span>`:""}`;}

/* ================= رنگ و نگاره‌های پایه ================= */
const INK="#1B2A41",BLUE="#2F6BD0",RED="#D8452B",PURP="#7A3FC8",GRN="#22965A",MUT="#56677F";
const starSvg=(on,size)=>`<svg width="${size||18}" height="${size||18}" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.6l2.8 5.9 6.4.9-4.6 4.5 1.1 6.4L12 17.3l-5.7 3 1.1-6.4-4.6-4.5 6.4-.9z" fill="${on?"#FFC43D":"none"}" stroke="${on?"#D99A12":"#B8C6D3"}" stroke-width="1.7" stroke-linejoin="round"/></svg>`;
const heart=on=>`<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z" fill="${on?"#E5484D":"none"}" stroke="${on?"#B8323A":"#B8C6D3"}" stroke-width="1.8"/></svg>`;
const LOCK=`<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="3" fill="#9FB0C0"/><path d="M8 11V8a4 4 0 0 1 8 0v3" stroke="#9FB0C0" stroke-width="2.6" fill="none"/></svg>`;
/* متن در SVG؛ halo برای خوانایی روی هر زمینه */
function T(x,y,s,o){o=o||{};const sz=Math.round((o.size||14)*(o.halo===false?1:1.6)),col=o.col||INK,anc=o.anchor||"middle",w=o.weight||700,cls=o.cls?` class="${o.cls}"`:"";
  const halo=o.halo===false?"":`stroke="${o.haloCol||"#fff"}" stroke-width="${o.haloW||4}" stroke-linejoin="round" paint-order="stroke"`;
  const rot=o.rot?` transform="rotate(${o.rot} ${x} ${y})"`:"";
  return `<text x="${x}" y="${y}" text-anchor="${anc}" font-size="${sz}" font-weight="${w}" fill="${col}" ${halo}${cls}${rot} direction="rtl">${s}</text>`;}
/* فلش نیرو */
function arrow(x1,y1,x2,y2,w,col,op){const dx=x2-x1,dy=y2-y1,L=Math.hypot(dx,dy);if(L<2)return "";const ux=dx/L,uy=dy/L,px=-uy,py=ux,hl=Math.min(L,w*2.6),hw=w*1.35,sw=w/2,bx=x2-ux*hl,by=y2-uy*hl;
  const p=[[x1+px*sw,y1+py*sw],[bx+px*sw,by+py*sw],[bx+px*hw,by+py*hw],[x2,y2],[bx-px*hw,by-py*hw],[bx-px*sw,by-py*sw],[x1-px*sw,y1-py*sw]];
  return `<polygon class="farr" points="${p.map(q=>q[0].toFixed(1)+","+q[1].toFixed(1)).join(" ")}" fill="${col}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" opacity="${op||1}"/>`;}
/* پس‌زمینه‌ها */
/* پس‌زمینهٔ تخت با رنگ‌های هر سرزمین (متغیرهای CSS روی body) */
function bgRoom(fy){return `<rect width="640" height="520" style="fill:var(--sw)"/><rect y="${fy}" width="640" height="${520-fy}" style="fill:var(--sf)"/><rect y="${fy}" width="640" height="3" style="fill:var(--sl)"/>`;}
function bgOut(fy){return `<rect width="640" height="520" style="fill:var(--sky)"/><path d="M0 ${fy-26} Q110 ${fy-70} 240 ${fy-34} T470 ${fy-40} T640 ${fy-48} V${fy+2} H0Z" style="fill:var(--hill)"/><rect y="${fy}" width="640" height="${520-fy}" style="fill:var(--gnd)"/><rect y="${fy}" width="640" height="4" style="fill:var(--sl)"/>`;}
function trayPanel(label,y){y=y||404;return `<rect x="8" y="${y}" width="624" height="${512-y}" rx="16" fill="#fff" stroke="#D4E1E9" stroke-width="2"/>`+(label?T(620,y+22,label,{size:13,col:MUT,anchor:"start",halo:false}):"");}
const shadow=(x,y,w)=>`<ellipse cx="${x}" cy="${y}" rx="${w/2}" ry="${Math.max(3,w/12)}" fill="#000" opacity=".12"/>`;
function crateSvg(x,yb,w,h,label,col){col=col||"#E0A45F";return `<g><rect x="${x-w/2}" y="${yb-h}" width="${w}" height="${h}" rx="4" fill="${col}" stroke="#94602D" stroke-width="2.5"/><path d="M${x-w/2+5} ${yb-h+5} L${x+w/2-5} ${yb-5} M${x+w/2-5} ${yb-h+5} L${x-w/2+5} ${yb-5}" stroke="#B97C40" stroke-width="3" opacity=".7"/><rect x="${x-w*.36}" y="${yb-h*.66}" width="${w*.72}" height="${h*.34}" rx="5" fill="#FFF7EA" stroke="#94602D" stroke-width="1.5"/>${T(x,yb-h*.41,label,{size:Math.round(Math.min(w,h)*.24),col:"#5B3A18",halo:false})}</g>`;}

/* ================= موتور کشیدن و رها کردن ================= */
function svgPoint(svg,e){const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;const m=svg.getScreenCTM();return m?p.matrixTransform(m.inverse()):{x:0,y:0};}
function dragKit(svg,cfg){
  let d=null;
  svg.onpointerdown=e=>{if(e.button>0)return;if(cfg.blocked&&cfg.blocked())return;const p=svgPoint(svg,e),t=e.target.closest("[data-drag]");
    if(!t){const z=e.target.closest("[data-zone]");if(z&&cfg.zoneTap)cfg.zoneTap(z.dataset,p);return;}
    const g=cfg.start(t.dataset,p);if(!g)return;d={g,id:e.pointerId,x0:p.x,y0:p.y,moved:false};
    try{svg.setPointerCapture(e.pointerId);}catch(_){}e.preventDefault();};
  svg.onpointermove=e=>{if(!d||e.pointerId!==d.id)return;const p=svgPoint(svg,e);if(!d.moved&&Math.hypot(p.x-d.x0,p.y-d.y0)>6){d.moved=true;if(cfg.begin)cfg.begin(d.g,p);}if(d.moved&&cfg.move)cfg.move(d.g,p);e.preventDefault();};
  const up=e=>{if(!d||e.pointerId!==d.id)return;const p=svgPoint(svg,e),dd=d;d=null;if(dd.moved){if(cfg.end)cfg.end(dd.g,p);}else if(cfg.tap)cfg.tap(dd.g,p);};
  svg.onpointerup=up;svg.onpointercancel=e=>{if(!d)return;const dd=d;d=null;if(cfg.cancel)cfg.cancel(dd.g);else if(cfg.end)cfg.end(dd.g,{x:-9999,y:-9999});};
}
/* شبحِ در حال کشیدن */
function makePainter(svg){let gh="",gx=0,gy=0,hint="";svg.addEventListener("pointerdown",()=>{if(hint){hint="";const e=svg.querySelector("#hint");if(e)e.remove();}});
  const P={view(h){svg.setAttribute("viewBox",`0 0 640 ${h}`);svg.style.aspectRatio=`640/${h}`;},paint(html){svg.innerHTML=html+`<g id="ghost" pointer-events="none" transform="translate(${gx} ${gy})" opacity=".92">${gh}</g>`+hint;},
    hint(d){if(reduceMotion)return;hint=`<g id="hint" pointer-events="none"><path d="${d}" fill="none" stroke="#FF8A3D" stroke-width="4" stroke-dasharray="3 9" stroke-linecap="round" opacity=".7"/><g><animateMotion dur="2.6s" repeatCount="indefinite" path="${d}" keyPoints="0;1;1" keyTimes="0;.75;1" calcMode="linear"/><circle r="20" fill="#FF8A3D" opacity=".25"/><g transform="translate(-6 -2) scale(1.5)"><rect x="-5" y="0" width="10" height="24" rx="5" fill="#FFE0C4" stroke="#B9855A" stroke-width="1.6"/><rect x="-11" y="15" width="30" height="24" rx="10" fill="#FFE0C4" stroke="#B9855A" stroke-width="1.6"/></g></g></g>`;const e=svg.querySelector("#hint");if(e)e.remove();svg.insertAdjacentHTML("beforeend",hint);},
    ghost(html,x,y){gh=html;gx=x;gy=y;const g=svg.querySelector("#ghost");if(g){g.innerHTML=html;g.setAttribute("transform",`translate(${x} ${y})`);}},
    move(x,y){gx=x;gy=y;const g=svg.querySelector("#ghost");if(g)g.setAttribute("transform",`translate(${x} ${y})`);},
    clear(){gh="";const g=svg.querySelector("#ghost");if(g)g.innerHTML="";}};
  return P;}

/* ================= اجزای رابط ================= */
function stepper(host,o){let v=o.init||0;const steps=o.steps||[1,10];
  host.insertAdjacentHTML("beforeend",`<div class="stp" role="group" aria-label="${o.label||"عدد"}">${steps.slice().reverse().map(s=>`<button type="button" data-d="${-s}" aria-label="کم کردن ${fa(s)}">−${fa(s)}</button>`).join("")}<output aria-live="polite">${fa(v)}</output>${o.unit?`<span class="u">${o.unit}</span>`:""}${steps.map(s=>`<button type="button" data-d="${s}" aria-label="اضافه کردن ${fa(s)}">+${fa(s)}</button>`).join("")}</div>`);
  const box=host.lastElementChild,out=box.querySelector("output");
  box.onclick=e=>{const b=e.target.closest("[data-d]");if(!b||b.disabled)return;v=clamp(Math.round((v+(+b.dataset.d))*100)/100,o.min==null?0:o.min,o.max==null?9999:o.max);out.textContent=fa(v);if(o.onChange)o.onChange(v);};
  return{get:()=>v,set:x=>{v=x;out.textContent=fa(v);},disable:()=>box.querySelectorAll("button").forEach(b=>b.disabled=true)};}
function mcq(host,labels,onPick){host.insertAdjacentHTML("beforeend",`<div class="mcq">${labels.map((l,i)=>`<button class="btn" type="button" data-i="${i}">${l}</button>`).join("")}</div>`);
  const box=host.lastElementChild;box.onclick=e=>{const b=e.target.closest("[data-i]");if(!b||b.disabled)return;onPick(+b.dataset.i,b);};
  return{mark(i,c){const b=box.querySelector(`[data-i="${i}"]`);if(b)b.classList.add(c);},clearMarks(){box.querySelectorAll(".btn").forEach(b=>b.classList.remove("right","wrong"));},disable(){box.querySelectorAll(".btn").forEach(b=>b.disabled=true);},enable(){box.querySelectorAll(".btn").forEach(b=>b.disabled=false);}};}
function btn(host,label,cls,fn){host.insertAdjacentHTML("beforeend",`<button class="btn ${cls||""}" type="button">${label}</button>`);const b=host.lastElementChild;b.onclick=()=>{if(!b.disabled)fn(b);};return b;}

/* ================= پنجره‌ها ================= */
function closeOv(){document.querySelectorAll(".ovl,.conf").forEach(e=>e.remove());}
function overlay(html,label,col){closeOv();const o=document.createElement("div");o.className="ovl";o.setAttribute("role","dialog");o.setAttribute("aria-modal","true");o.setAttribute("aria-label",label);if(col)o.style.setProperty("--c",col);o.innerHTML=html;o.addEventListener("click",e=>{if(e.target===o)closeOv();});document.body.appendChild(o);return o;}
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeOv();});
function confetti(){if(reduceMotion)return;const cols=["#FFC43D","#E8590C","#22965A","#2F6BD0","#7A3FC8"];for(let i=0;i<28;i++){const c=document.createElement("div");c.className="conf";c.style.left=Math.random()*100+"vw";c.style.background=cols[i%5];c.style.animationDuration=(1.4+Math.random()*1.4)+"s";c.style.animationDelay=Math.random()*.4+"s";document.body.appendChild(c);setTimeout(()=>c.remove(),3200);}}
