/* Ideal-machine model. Distances use the units stated in each scene.
   Reference: OpenStax Physics 9.3 (no friction; massless rope/pulleys).
   Wedge resistance is the effective lateral load in this simplified model. */
const MACHINE={
 ramp:(W,h,L)=>W*h/L,
 wheel:(W,R)=>W/R,
 pulley:(W,n)=>W/n,
 wedge:(R,L,w=2)=>R*w/L,
 screw:(R,p,C=120)=>R*p/C,
 rope:(n,h)=>n*h,
 hand:(R,n,c=.5)=>R*n*c,
 turns:(depth,p)=>depth/p,
 minimum:(options,force,Sv)=>options.find(v=>force(v)<Sv-1e-9)
};
const MACHINE_ASSUMPTIONS="در این مدل اصطکاک و اتلاف انرژی را حساب نمی‌کنیم. برای آغاز حرکت از حالت سکون، نیروی تو باید از نیروی لازم بیشتر باشد.";
function machineRule(text,kid){return KID()?(kid||text):text+" "+MACHINE_ASSUMPTIONS;}
/* Exploration never costs points. Showing a solution still earns one point. */
function machineSuccess(A,text,kid){return A.judge(true,{ok:KID()?(kid||text):text,pts:2,act:true});}
function machineGuide(A,text,more,final,show){return A.trial(false,{retry:text,more,final,show});}
/* Capture focus before replacing the SVG descendants. */
function machinePaint(A,html){const active=document.activeElement;
 A.machineFocus=active&&A.svg.contains(active)&&active.dataset.drag?'[data-drag="'+active.dataset.drag+'"]':null;
 A.P.paint(html);
}
/* A replaced configuration cannot redraw or finish the newer scene. */
function machineScene(A,cfg){const id=(A.machineSceneId||0)+1;A.machineSceneId=id;
 const current=()=>A.machineSceneId===id,out=Object.assign({},cfg,{current});
 ["onTop","onDone","onBlocked","onChange"].forEach(k=>{if(cfg[k])out[k]=(...args)=>{if(current())return cfg[k](...args);};});return out;
}
/* Repainted SVG controls retain focus; listeners are replaced, never stacked. */
function machineKeys(A,selector,label,act){
 const keep=A.machineFocus===selector;A.machineFocus=null;
 A.svg.setAttribute("role","group");
 A.svg.querySelectorAll(selector).forEach(el=>{el.setAttribute("tabindex","0");el.setAttribute("role","button");el.setAttribute("aria-label",label);});
 A.svg.onkeydown=e=>{if(!e.target.closest(selector)||!["Enter"," ","ArrowRight","ArrowLeft","ArrowDown","ArrowUp"].includes(e.key))return;
   e.preventDefault();if(A.locked)return;act(e.key);};
 if(keep){const el=A.svg.querySelector(selector);if(el)el.focus({preventScroll:true});}
}
/* An observation is completed before the assessed comparison appears. */
function machineObserve(A,prompt,run,question,options,answer,explain,retry){
 A.prompt(prompt+" آزمایش امتیاز ندارد.");const c=A.ctrl("");
 const b=btn(c,"آزمایش را ببین","go",()=>{b.disabled=true;run(()=>{
   A.prompt(question);A.fb("آزمایش انجام شد. حالا از روی نتیجه پاسخ بده.","info");const c2=A.ctrl("");
   const m=mcq(c2,options,(i,bt)=>{if(A.locked)return;
     if(i===answer){m.disable();m.mark(i,"right");A.judge(true,{ok:explain});}
     else{m.mark(i,"wrong");bt.disabled=true;A.judge(false,{retry,final:explain});if(A.locked){m.disable();m.mark(answer,"right");}}
   });
 });});
}
/* Stable challenge ids preserve the existing mission/level topology.
   Pack metadata names the taught idea and prerequisite observation. */
function machinePacks(st,levels){levels.forEach(lv=>{
 const generate=lv.gen,first=generate(()=>.42),ids=first.map((_,i)=>lv.id+".p"+(i+1));
 defCh(st,ids.map((id,i)=>({id,d:/\.([34])$/.test(lv.id)?1:0,
   phase:["cmp","mcq","fixedq","fixedk","ropeq"].includes(first[i].t)?"observe-apply":["fit","choose","wc","sc","crank","lift"].includes(first[i].t)?"try":"apply",
   terms:st==="ramp"?["سطح شیب‌دار"]:st==="wheel"?["چرخ و محور"]:st==="pulley"?["قرقره"]:["wc","wF"].includes(first[i].t)||(first[i].t==="mcq"&&[1,3].includes(first[i].q))?["گوه"]:["پیچ"],teach:lv.desc,
   mk:r=>Object.assign({},generate(r)[i])})));
 lv.ch=ids;delete lv.gen;chLevel(lv);
});}
