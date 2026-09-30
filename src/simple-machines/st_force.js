/* ================= ایستگاه نیرو: طناب‌کشی و اصطکاک ================= */
const TOKH={10:44,20:54,50:66};
function tokenSvg(x,y,v,side,hl){const h=TOKH[v]||50,w=50,col=side==="L"?BLUE:RED,dir=side==="L"?-1:1,ay=KID()?y+h/2:y+14;
  return `<g><rect x="${x-w/2}" y="${y}" width="${w}" height="${h}" rx="12" fill="${col}" stroke="${hl?"#FFC43D":"#fff"}" stroke-width="${hl?4:2}"/>${arrow(x-dir*14,ay,x+dir*16,ay,7,"#fff")}${KID()?"":T(x,y+h-6,fa(v),{size:15,col:"#fff",halo:false})}</g>`;}
function reach(sum,vals,maxN){if(sum===0)return true;if(maxN===0||sum<0)return false;return vals.some(v=>reach(sum-v,vals,maxN-1));}
const sumA=a=>a.reduce((x,y)=>x+(y||0),0);

function makeTug(A,cfg){
  const svg=A.svg,P=A.P;A.view(cfg.edit?520:404);
  const st={L:(cfg.L||[]).slice(),R:(cfg.R||[]).slice(),edit:cfg.edit||"",tray:cfg.tray||[10],cx:320,sel:null,hover:null,busy:false,show:cfg.show||"all"};
  while(st.L.length<4)st.L.push(null);while(st.R.length<4)st.R.push(null);
  const slotX=(side,i)=>side==="L"?st.cx-95-i*56:st.cx+95+i*56;
  const editable=side=>!A.locked&&!st.busy&&(st.edit==="both"||st.edit===side);
  function render(){
    const cx=st.cx,sL=sumA(st.L),sR=sumA(st.R),net=sR-sL;
    let s=bgRoom(330);
    s+=`<g opacity=".55"><path d="M320 330 V352" stroke="${INK}" stroke-width="3"/><path d="M120 330 V300 l22 7 -22 7" fill="${BLUE}" stroke="${BLUE}" stroke-width="3"/><path d="M520 330 V300 l22 7 -22 7" fill="${RED}" stroke="${RED}" stroke-width="3"/></g>`;
    s+=`<line x1="14" y1="285" x2="626" y2="285" stroke="#8A6A48" stroke-width="6" stroke-linecap="round"/><line x1="14" y1="283" x2="626" y2="283" stroke="#B08D66" stroke-width="2"/>`;
    s+=shadow(cx,331,110)+`<rect x="${cx-52}" y="258" width="104" height="58" rx="10" fill="#5E7395"/><rect x="${cx-52}" y="258" width="104" height="12" rx="6" fill="#7F93B3"/>`+[-30,30].map(d=>`<circle cx="${cx+d}" cy="318" r="12" fill="${INK}"/><circle cx="${cx+d}" cy="318" r="4.5" fill="#C7D3DE"/>`).join("")+`<circle cx="${cx}" cy="286" r="7" fill="#FFC43D" stroke="#fff" stroke-width="2"/>`;
    for(const side of["L","R"])for(let i=0;i<4;i++){const x=slotX(side,i),v=st[side][i];
      if(v!=null){s+=`<g ${editable(side)?`data-drag="slot" data-side="${side}" data-i="${i}" style="cursor:grab"`:""}><line x1="${x}" y1="285" x2="${x}" y2="294" stroke="#6B5236" stroke-width="3"/>${tokenSvg(x,292,v,side,false)}</g>`;}
      else if(editable(side)){const hov=st.hover&&st.hover.side===side&&st.hover.i===i;s+=`<g data-zone="slot" data-side="${side}" data-i="${i}" style="cursor:pointer"><rect x="${x-28}" y="262" width="56" height="90" fill="#fff" fill-opacity="0"/><circle cx="${x}" cy="285" r="${hov?21:16}" fill="${hov?"#FFF3C4":"#fff"}" stroke="${side==="L"?BLUE:RED}" stroke-width="2.5" stroke-dasharray="4 3"/></g>`;}}
    if(S.forces&&st.show!=="none"){const mx=Math.max(sL,sR,1),sc=Math.min(1.7,230/mx),y=224,lL=Math.min(sL*sc,cx-20),lR=Math.min(sR*sc,616-cx);
      if(sL)s+=arrow(cx-4,y,cx-4-lL,y,13,BLUE);if(sR)s+=arrow(cx+4,y,cx+4+lR,y,13,RED);
      const xl=clamp(Math.min(cx-lL/2,cx-78),70,570),xr=clamp(Math.max(cx+lR/2,cx+78),70,570);
      if(sL)s+=T(xl,y-27,`چپ<tspan class="num">: ${fa(sL)}</tspan>`,{size:14,col:BLUE});if(sR)s+=T(xr,y-27,`راست<tspan class="num">: ${fa(sR)}</tspan>`,{size:14,col:RED});
      const ny=140;if(st.show!=="all"){}else if(net!==0){const nl=clamp(net*sc,20-cx,620-cx);s+=arrow(cx,ny,cx+nl,ny,15,PURP);s+=T(clamp(cx+nl/2,90,550),ny-31,`نیروی خالص<tspan class="num">: ${fa(Math.abs(net))}</tspan>`,{size:14,col:PURP});}
      else if(sL||sR)s+=T(cx,ny,"نیروی خالص: صفر (تعادل)",{size:15,col:PURP});}
    if(st.edit){s+=trayPanel("",404);
      for(const side of["L","R"]){if(st.edit!=="both"&&st.edit!==side)continue;const x0=side==="L"?170:470;
        st.tray.forEach((v,j)=>{const x=x0+(j-(st.tray.length-1)/2)*84,sel=st.sel&&st.sel.side===side&&st.sel.v===v;s+=`<g data-drag="tray" data-side="${side}" data-v="${v}" style="cursor:grab"><g transform="translate(${x} 440) scale(1.2) translate(${-x} -440)">${tokenSvg(x,432,v,side,sel)}</g></g>`;});}}
    P.paint(s);
    const q="<b>؟</b>",sh=st.show;
    A.counter(`<span class="cc l">چپ: ${sh==="none"?q:`<b class="num">${fa(sL)}</b> نیوتن`}</span><span class="cc r">راست: ${sh==="none"?q:`<b class="num">${fa(sR)}</b> نیوتن`}</span><span class="cc n">خالص: ${sh!=="all"?q:`<b class="num">${fa(Math.abs(net))}</b> ${net>0?"به راست":net<0?"به چپ":"(تعادل)"}`}</span>`);
    A.formula(FX(`${sy("F")} = ${sy("F","2")} − ${sy("F","1")}`,sh==="all"?`${sy("F")} = ${fa(Math.max(sL,sR))} − ${fa(Math.min(sL,sR))} = ${fa(Math.abs(net))} N`:"",[[sy("F"),"نیروی خالص"],[sy("F","2"),"جمع نیروهای طرفِ قوی‌تر"],[sy("F","1"),"جمع نیروهای طرفِ ضعیف‌تر"],["N","نیوتن"]]));
  }
  const nearSlot=(side,p)=>{let b=null,bd=70;for(let i=0;i<4;i++){if(st[side][i]!=null)continue;const d=Math.hypot(p.x-slotX(side,i),p.y-300);if(d<bd){bd=d;b=i;}}return b;};
  const place=(side,v,i)=>{if(i==null){i=st[side].indexOf(null);if(i<0){A.fb("همهٔ جاهای این طرف پر است.","info");return;}}st[side][i]=v;};
  dragKit(svg,{blocked:()=>A.locked||st.busy,
    start(d){if(d.drag==="tray"){if(!editable(d.side))return null;return{from:"tray",side:d.side,v:+d.v};}
      if(d.drag==="slot"){if(!editable(d.side))return null;const v=st[d.side][+d.i];return{from:"slot",side:d.side,i:+d.i,v};}return null;},
    begin(g,p){if(g.from==="slot"){st[g.side][g.i]=null;}st.sel=null;P.ghost(tokenSvg(0,-30,g.v,g.side,true),p.x,p.y);render();},
    move(g,p){P.move(p.x,p.y);const i=nearSlot(g.side,p);const h=i==null?null:{side:g.side,i};if(JSON.stringify(h)!==JSON.stringify(st.hover)){st.hover=h;render();}},
    end(g,p){P.clear();st.hover=null;const i=nearSlot(g.side,p);if(i!=null)st[g.side][i]=g.v;render();if(cfg.onChange)cfg.onChange();},
    tap(g){if(g.from==="tray"){st.sel={side:g.side,v:g.v};A.fb("حالا روی یکی از دایره‌های خالی روی طناب بزن، یا کشش را بکش و آنجا رها کن.","info");render();}
      else{st[g.side][g.i]=null;render();if(cfg.onChange)cfg.onChange();}},
    zoneTap(z){if(z.zone!=="slot")return;const side=z.side;if(st.sel&&st.sel.side===side){st[side][+z.i]=st.sel.v;st.sel=null;A.fb("");render();if(cfg.onChange)cfg.onChange();}
      else if(st.edit){A.fb("اول یکی از کشش‌های پایین صفحه را انتخاب کن یا بکش.","info");}}});
  function run(done){const net=sumA(st.R)-sumA(st.L);st.busy=true;const x0=st.cx;
    if(net===0){tween(900,p=>{st.cx=x0+Math.sin(p*Math.PI*6)*3*(1-p);render();},()=>{st.cx=x0;st.busy=false;render();done&&done(0);});return;}
    const dir=Math.sign(net),k=Math.abs(net);const xs=[];for(const sd of["L","R"])for(let i=0;i<4;i++)if(st[sd][i]!=null)xs.push(slotX(sd,i));const lim=Math.max(24,dir>0?610-Math.max(x0+60,...xs):Math.min(x0-60,...xs)-30);tween(2000,p=>{st.cx=x0+dir*Math.min(lim,200*Math.min(1,(k/10)*.45)*p*p*2.2);render();},()=>{st.busy=false;done&&done(dir);});}
  const reset=()=>{st.cx=320;render();};
  render();
  return{st,render,run,reset,place};
}

function makeFriction(A,F){
  const svg=A.svg,P=A.P;A.view(424);const lanes=[{n:"یخ",f:4,col:"#CFEFFB",edge:"#8CCFEA"},{n:"کف چوبی",f:15,col:"#E3B77F",edge:"#B9834A"},{n:"فرش",f:35,col:"#D9776B",edge:"#A94B41"}];
  const st={F,pos:[0,0,0],busy:false,pick:null};
  function lane(i){const L=lanes[i],y=46+i*124,sy=y+92;let tex="";
    if(i===0)tex=`<path d="M120 ${sy+10} l40 -6 M300 ${sy+18} l60 -8 M470 ${sy+9} l50 -6" stroke="#fff" stroke-width="3" stroke-linecap="round"/>`;
    else if(i===1)tex=[160,260,360,460,560].map(x=>`<line x1="${x}" y1="${sy}" x2="${x}" y2="${sy+26}" stroke="#B9834A" stroke-width="2"/>`).join("");
    else{for(let x=110;x<600;x+=18)tex+=`<circle cx="${x}" cy="${sy+8+(x%36?8:0)}" r="2.2" fill="#B85548"/>`;}
    const cx=196+st.pos[i],sel=st.pick===i;
    let s=`<g data-zone="lane" data-i="${i}" style="cursor:pointer"><rect x="84" y="${y+2}" width="540" height="118" rx="14" fill="${sel?"#FFF6D6":"#fff"}" fill-opacity="${sel?1:.5}" stroke="${sel?"#F0B429":"none"}" stroke-width="3"/><rect x="96" y="${sy}" width="516" height="26" rx="6" fill="${L.col}" stroke="${L.edge}" stroke-width="2"/>${tex}</g>`;
    s+=T(604,y+26,L.n,{size:15,col:INK,anchor:"start"});
    s+=shadow(cx,sy+1,70)+crateSvg(cx,sy,66,52,"",null);
    if(S.forces){const pl=Math.max(24,Math.min(80,F*1.6));s+=arrow(cx-36-pl,sy-38,cx-37,sy-38,10,BLUE)+T(cx-40,sy-63,`هل<tspan class="num"> ${fa(F)}</tspan>`,{size:13,col:BLUE,anchor:"start"});
      const f=Math.min(F,L.f);if(f>0){const fl=Math.max(16,Math.min(66,f*1.9));s+=arrow(cx-34,sy-7,cx-34-fl,sy-7,7,"#E8590C")+T(cx-48-fl,sy-2,"اصطکاک",{size:12,col:"#E8590C",anchor:"start"});}}
    return s;}
  function render(){let s=`<rect width="640" height="520" style="fill:var(--sw)"/>`;for(let i=0;i<3;i++)s+=lane(i);
    P.paint(s);}
  function run(done){st.busy=true;const tgt=lanes.map(L=>Math.max(0,F-L.f)*9);const p0=st.pos.slice();
    tween(1800,p=>{const e=1-Math.pow(1-p,3);st.pos=tgt.map((t,i)=>Math.min(260,p0[i]+t*e));render();},()=>{st.busy=false;done&&done();});}
  dragKit(svg,{blocked:()=>st.busy,start:()=>null,zoneTap(z){if(z.zone==="lane"&&A.onLane)A.onLane(+z.i);}});
  render();return{st,render,run,lanes,reset(){st.pos=[0,0,0];render();}};
}

const ST_force={key:"force",name:"نیرو",c:"#E8590C",sub:"هل دادن، کشیدن، نیروی خالص و اصطکاک",
 intro:"نیرو یعنی هل دادن یا کشیدن. در طناب‌کشی کشش‌ها را روی طناب بگذار و ببین جعبه به کدام طرف می‌رود. بعد اصطکاک را روی یخ، چوب و فرش امتحان کن.",
 art(){const s={};let h=bgRoom(330).replace(/id="g/g,'id="a'+"f").replace(/url\(#g/g,"url(#af");
   h+=`<line x1="14" y1="285" x2="626" y2="285" stroke="#8A6A48" stroke-width="6"/><rect x="268" y="258" width="104" height="58" rx="10" fill="#5E7395"/><rect x="268" y="258" width="104" height="12" rx="6" fill="#7F93B3"/><circle cx="290" cy="318" r="12" fill="${INK}"/><circle cx="350" cy="318" r="12" fill="${INK}"/>`+tokenSvg(225,292,20,"L")+tokenSvg(163,292,10,"L")+tokenSvg(415,292,50,"R")+arrow(316,222,256,222,13,BLUE)+arrow(324,222,404,222,13,RED)+arrow(320,170,370,170,15,PURP);return h;},
 lab(A){A.prompt("آزمایشگاه: کشش‌ها را از پایین روی طناب بکش. برای برداشتن، کشش را از طناب بیرون بکش یا رویش بزن. بعد «برو!» را بزن.");
   let mode="tug",tug=null;
   function tugMode(){mode="tug";A.formula("");tug=makeTug(A,{edit:"both",tray:KID()?[10]:[10,20,50]});A.refresh=()=>tug.render();
     const c=A.ctrl("");btn(c,"برو!","go",b=>{b.disabled=true;tug.run(dir=>{A.fb(dir===0?"جعبه تکان نخورد: نیروها برابرند و نیروی خالص صفر است.":`جعبه به ${dir>0?"راست":"چپ"} رفت، چون نیروی ${dir>0?"راست":"چپ"} بیشتر است.`,"info");b.disabled=false;});});
     btn(c,"برگرداندن جعبه","",()=>{tug.reset();A.fb("");});btn(c,"پاک کردن طناب","",()=>{tug.st.L=[null,null,null,null];tug.st.R=[null,null,null,null];tug.reset();A.fb("");});
     btn(c,"آزمایش اصطکاک","pri",fricMode);}
   function fricMode(){mode="fric";A.prompt("آزمایشگاه اصطکاک: اندازهٔ هل را انتخاب کن و «هل بده!» را بزن. ببین روی هر سطح جعبه چقدر جلو می‌رود.");A.counter("");
     let F=20,fr=makeFriction(A,F);A.formula(`<span class="fl">قانون</span><span>اصطکاک تا یک اندازه جلوی هل را می‌گیرد. اگر هل از آن اندازه بیشتر شود، جعبه راه می‌افتد.</span>`);A.refresh=()=>fr.render();
     const c=A.ctrl("");const sp=stepper(c,{init:F,min:5,max:60,steps:[5],unit:"نیوتن هل",onChange:v=>{F=v;fr=makeFriction(A,F);A.refresh=()=>fr.render();}});
     btn(c,"هل بده!","go",b=>{b.disabled=true;fr.reset();fr.run(()=>{b.disabled=false;const moved=fr.lanes.filter(L=>F>L.f).map(L=>L.n);A.fb(moved.length?`با ${fa(F)} نیوتن، جعبه روی ${andList(moved)} حرکت کرد.${moved.length<3?" روی بقیه، اصطکاک همهٔ هل را خنثی کرد.":""}`:"روی هیچ سطحی حرکت نکرد؛ هل آن‌قدر نبود که بر اصطکاک غلبه کند.","info");});});
     btn(c,"برگشت به طناب‌کشی","pri",()=>{A.prompt("آزمایشگاه: کشش‌ها را از پایین روی طناب بکش. بعد «برو!» را بزن.");A.fb("");tugMode();});}
   tugMode();},
 kid:[
  {title:"کدام طرف قوی‌تر است؟",desc:"کشش‌ها را بشمار و بگو کدام طرف می‌برد.",gen(r){const P=[[1,2],[3,1],[2,2],[1,3],[3,2]];return shuffle(r,P).map(([a,b])=>({t:"predict",L:Array(a).fill(10),R:Array(b).fill(10),spread:true}));}},
  {title:"جعبه را نگه دار",desc:"کشش بگذار تا دو طرف مساوی شوند.",gen(r){return[{t:"balance",fixed:[10],tray:[10]},{t:"balance",fixed:[10,10],tray:[10]},{t:"predict",L:[10,10],R:[10,10,10],spread:true},{t:"balance",fixed:[10,10,10],tray:[10],side:"L"},{t:"balance",fixed:[10,10],tray:[10],spread:true,side:"L"}];}},
  {title:"لیز یا زبر؟",desc:"جعبه روی یخ، چوب و فرش. کدام راحت‌تر سُر می‌خورد؟",gen(r){return[{t:"fric",q:1,F:20},{t:"fric",q:3,F:20},{t:"predict",L:[10,10,10,10],R:[10,10,10],spread:true},{t:"fric",q:2,F:20},{t:"balance",fixed:[10,10,10,10],tray:[10]}];}}],
 levels:[
  {title:"هل دادن و کشیدن",desc:"کدام طرف قوی‌تر است؟ با شمردن کشش‌ها طناب‌کشی را متعادل کن.",gen(r){const a=ri(r,1,3);let b=ri(r,1,3);if(b===a)b=a===3?1:a+1;const c=ri(r,2,3);const d=ri(r,1,3);
    return[{t:"predict",L:Array(a).fill(10),R:Array(b).fill(10)},{t:"balance",fixed:Array(ri(r,2,3)).fill(10),tray:[10]},{t:"predict",L:Array(c).fill(10),R:Array(c).fill(10),spread:true},{t:"fric",q:1,F:20},{t:"balance",fixed:Array(ri(r,1,4)).fill(10),tray:[10],spread:true},{t:"predict",L:Array(d).fill(10),R:Array(d===3?2:d+1).fill(10),spread:true}];}},
  {title:"جمع نیروها",desc:"کشش‌ها اندازه‌های مختلف دارند. تعداد مهم نیست؛ جمعِ اندازهٔ آن‌ها مهم است.",gen(r){return[{t:"predict",L:[10,10,10],R:[20]},{t:"balance",fixed:shuffle(r,[20,10]),tray:[10,20]},{t:"net",L:[20,20],R:[10]},{t:"fric",q:2,F:20},{t:"balance",fixed:shuffle(r,[20,20,10]),tray:[10,20],side:"L"},{t:"net",L:[10],R:shuffle(r,[20,20,10])}];}},
  {title:"نیروی خالص",desc:"نیروی خالص را حساب کن و طناب را طوری بچین که به اندازهٔ دلخواه جابه‌جا شود.",gen(r){return[{t:"make",fixed:[20,10],tray:[10,20,50],target:20,show:"sides"},{t:"net",L:[50],R:[20,10]},{t:"predict",L:[10,10,10,10],R:[50]},{t:"balance",fixed:shuffle(r,[50,20]),tray:[10,20,50],show:"sides",side:"L"},{t:"fric",q:3,F:30},{t:"make",fixed:[20],tray:[10,20,50],target:-30,side:"L",show:"sides"}];}},
  {title:"قهرمان نیرو",desc:"عددهای بزرگ‌تر، کشش‌های بیشتر و جای کم روی طناب.",gen(r){return[{t:"make",fixed:[50,20,10],tray:[20,50],target:40,show:"sides"},{t:"net",L:shuffle(r,[50,20,20,10]),R:shuffle(r,[50,50,10])},{t:"balance",fixed:shuffle(r,[50,50,20,10]),tray:[20,50,10],show:"sides"},{t:"predict",L:shuffle(r,[20,20,20,20]),R:shuffle(r,[50,20,10])},{t:"fric",q:2,F:30},{t:"make",fixed:shuffle(r,[50,20]),tray:[10,20,50],target:-40,side:"L",show:"sides"}];}}],
 endless(r,d){const vals=d<2?[10]:d<3.5?[10,20]:[10,20,50],tp=pick(r,d<2?["predict","balance","fric"]:["predict","balance","net","make","fric"]);const rand=n=>Array.from({length:n},()=>pick(r,vals));
   if(tp==="fric")return{t:"fric",q:pick(r,[1,2,3]),F:pick(r,[20,30])};
   if(tp==="predict"){const L=rand(ri(r,1,4));let R=rand(ri(r,1,4));return{t:"predict",L,R,spread:true};}
   if(tp==="net")return{t:"net",L:rand(ri(r,1,4)),R:rand(ri(r,1,4))};
   for(let k=0;k<50;k++){const L=rand(ri(r,1,3+Math.min(1,Math.floor(d/3))));if(tp==="balance"&&reach(sumA(L),vals,4))return{t:"balance",fixed:L,tray:vals,side:pick(r,["L","R"]),show:d>3?"sides":"all"};
     if(tp==="make"){const t=pick(r,[10,20,30,40]);if(reach(sumA(L)+t,vals,4))return{t:"make",fixed:L,tray:vals,target:t,show:"sides"};}}
   return{t:"balance",fixed:[10,10],tray:[10]};},
 mount(sp,A){
  if(sp.t==="fric")return fricChallenge(sp,A);
  const spread=(a,seed)=>{const out=[null,null,null,null];if(!a)return out;const idx=sp.spread?shuffle(rng(seed+a.length*7+sumA(a)),[0,1,2,3]).slice(0,a.length).sort():a.map((_,i)=>i);a.forEach((v,j)=>out[idx[j]]=v);return out;};
  if(sp.t==="predict"){A.prompt(KID()?"کدام طرف قوی‌تر است؟":`کدام طرف طناب‌کشی را می‌برد؟<small>عددهای روی کشش‌ها را جمع کن و قبل از دیدن حرکت، پیش‌بینی کن.</small>`);
    const tug=makeTug(A,{L:spread(sp.L,1),R:spread(sp.R,2),show:"none"});A.refresh=()=>tug.render();
    const sL=sumA(sp.L),sR=sumA(sp.R),ans=sR>sL?0:sR===sL?1:2;
    const reveal=()=>{tug.st.show="all";tug.render();tug.run();};
    const cL=sp.L.length,cR=sp.R.length,KK={ok:ans===1?"دو طرف مساوی‌اند؛ جعبه تکان نمی‌خورد.":`طرف ${ans===0?"راست":"چپ"} کشش‌های بیشتری دارد.`,retry:"کشش‌های هر طرف را بشمار.",final:`جواب: ${["راست","مساوی","چپ"][ans]}. چپ ${fa(cL)} کشش دارد و راست ${fa(cR)} کشش.`};
    const c=A.ctrl("");const m=mcq(c,KID()?[`<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12 H18 M13 6 L19 12 L13 18" stroke="${RED}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>راست قوی‌تر`,"مساوی",`چپ قوی‌تر<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12 H6 M11 6 L5 12 L11 18" stroke="${BLUE}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`]:["راست می‌برد →","هیچ‌کدام؛ تعادل","← چپ می‌برد"],(i,b)=>{if(A.locked)return;
      if(i===ans){m.disable();m.mark(i,"right");reveal();A.judge(true,{ok:ans===1?`هر دو طرف ${fa(sL)} است؛ نیروی خالص صفر است.`:`جمع ${ans===0?"راست":"چپ"} بیشتر است: ${fa(Math.max(sL,sR))} در برابر ${fa(Math.min(sL,sR))}.`,k:KK});}
      else{m.mark(i,"wrong");b.disabled=true;A.judge(false,{retry:"جمع عددهای هر طرف را مقایسه کن، نه تعداد کشش‌ها را.",final:`جواب: ${["راست می‌برد","تعادل","چپ می‌برد"][ans]}. جمع چپ ${fa(sL)} و جمع راست ${fa(sR)} است.`,k:KK});if(A.locked){m.disable();m.mark(ans,"right");reveal();}}});
    return;}
  if(sp.t==="balance"||sp.t==="make"){const side=sp.side||"R",other=side==="R"?"L":"R";
    const cfg={edit:side,tray:sp.tray,show:sp.show||"all"};cfg[other]=spread(sp.fixed,3);cfg[side]=[];
    const tug=makeTug(A,cfg);A.refresh=()=>tug.render();
    {const x0=side==="L"?170:470,n=sp.tray.length,tx=x0+(0-(n-1)/2)*84,sx=side==="L"?225:415;A.hint(`M${tx} 462 L${sx} 300`);}
    const fixedSum=sumA(sp.fixed),tgt=sp.t==="balance"?0:sp.target,need=side==="R"?fixedSum+tgt:fixedSum-tgt;
    const sn=side==="R"?"راست":"چپ";
    if(sp.t==="balance")A.prompt(KID()?"کاری کن جعبه تکان نخورد. هر چند بار خواستی امتحان کن.":`طناب‌کشی را متعادل کن تا جعبه تکان نخورد. هر چند بار خواستی امتحان کن.<small>کشش‌ها را از پایین صفحه بکش و روی طرف ${sn} طناب رها کن. بعد «برو!» را بزن.</small>`);
    else A.prompt(`طوری بچین که نیروی خالص <b>${fa(Math.abs(tgt))} نیوتن به سمت ${tgt>0?"راست":"چپ"}</b> شود. هر چند بار خواستی امتحان کن.<small>کشش‌ها را روی طرف ${sn} طناب بکش، بعد «برو!» را بزن.</small>`);
    const c=A.ctrl("");const go=btn(c,"برو!","go",()=>{const s=sumA(tug.st[side]);if(!s){A.fb("اول دست‌کم یک کشش روی طناب بگذار.","info");return;}go.disabled=true;
      tug.run(()=>{const net=sumA(tug.st.R)-sumA(tug.st.L),ok=net===tgt;
        const res=A.trial(ok,{k:{ok:"دو طرف مساوی شد؛ جعبه تکان نخورد.",retry:"کشش‌های دو طرف را بشمار. باید مساوی باشند.",final:`طرف ${sn} باید ${fa(sp.fixed.length)} کشش داشته باشد.`},ok:sp.t==="balance"?"دو طرف برابر شدند و نیروی خالص صفر است.":`نیروی خالص دقیقاً ${fa(Math.abs(tgt))} نیوتن شد.`,
          retry:sp.t==="balance"?`جمع طرف ${sn} باید با طرف دیگر (${fa(fixedSum)}) برابر شود. جعبه سر جایش برگشت؛ دوباره بچین.`:`نیروی خالص ${fa(Math.abs(net))} شد. جمع طرف ${sn} باید ${fa(need)} باشد.`,
          final:`جمع طرف ${sn} باید ${fa(need)} می‌شد؛ مثلاً ${solveStr(need,sp.tray)}.`});
        if(!res&&!A.locked){later(500,()=>{tug.reset();go.disabled=false;});}});});
    return;}
  if(sp.t==="net"){A.prompt(`نیروی خالص چقدر است و به کدام طرف؟<small>عدد را تنظیم کن، جهت را انتخاب کن و «بررسی» را بزن.</small>`);
    const tug=makeTug(A,{L:spread(sp.L,4),R:spread(sp.R,5),show:"sides"});A.refresh=()=>tug.render();
    const net=sumA(sp.R)-sumA(sp.L);let dir=null;const c=A.ctrl("");const stp=stepper(c,{init:0,max:400,steps:[10],unit:"نیوتن",label:"اندازهٔ نیروی خالص"});
    c.insertAdjacentHTML("beforeend",`<div class="ctrl" id="dirs"><button class="opt" data-d="1" type="button">به راست →</button><button class="opt" data-d="0" type="button">بدون جهت (صفر)</button><button class="opt" data-d="-1" type="button">← به چپ</button></div>`);
    const dirs=c.querySelector("#dirs");dirs.onclick=e=>{const b=e.target.closest("[data-d]");if(!b)return;dir=+b.dataset.d;dirs.querySelectorAll(".opt").forEach(x=>x.classList.toggle("sel",x===b));};
    const chk=btn(c,"بررسی","go",()=>{const v=stp.get();if(dir==null){A.fb("جهت را هم انتخاب کن.","info");return;}const ok=v===Math.abs(net)&&(net===0?dir===0:dir===Math.sign(net));
      A.judge(ok,{ok:`نیروی خالص ${fa(Math.abs(net))} نیوتن ${net>0?"به راست":net<0?"به چپ":""} است.`,retry:"اول جمع هر طرف را حساب کن، بعد کوچک‌تر را از بزرگ‌تر کم کن. جهت، طرفِ بزرگ‌تر است.",final:`جمع چپ ${fa(sumA(sp.L))} و جمع راست ${fa(sumA(sp.R))} است؛ نیروی خالص ${fa(Math.abs(net))} ${net>0?"به راست":net<0?"به چپ":"(تعادل)"}.`});
      if(A.locked){chk.disabled=true;stp.disable();tug.st.show="all";tug.render();tug.run();}});
    return;}
 }};
function solveStr(sum,vals){const res=[];(function f(s,acc){if(res.length)return;if(s===0){res.push(acc.slice());return;}if(acc.length>=4)return;for(const v of vals.slice().sort((a,b)=>b-a)){if(v<=s){acc.push(v);f(s-v,acc);acc.pop();}}})(sum,[]);return res.length?res[0].map(fa).join(" + "):fa(sum);}
function fricChallenge(sp,A){const fr=makeFriction(A,sp.F);A.refresh=()=>fr.render();A.counter("");
  A.formula(`<span class="fl">قانون</span><span>جعبه حرکت می‌کند اگر هل از اصطکاک بیشتر باشد</span>`);
  const q=sp.q;let ans,text,expl;
  if(q===1){ans=0;text=KID()?"کدام جعبه دورتر می‌رود؟":"هر سه جعبه را با یک اندازه هل می‌دهیم. کدام جعبه دورتر می‌رود؟";expl="روی یخ اصطکاک خیلی کم است؛ پس جعبه راحت سُر می‌خورد.";}
  else if(q===2){ans=2;text=KID()?"کدام جعبه تکان نمی‌خورد؟":`با نیروی ${fa(sp.F)} نیوتن هل می‌دهیم. روی کدام سطح جعبه اصلاً تکان نمی‌خورد؟`;expl="اصطکاکِ فرش آن‌قدر زیاد است که این هل نمی‌تواند جعبه را راه بیندازد.";}
  else{ans=2;text=KID()?"کدام سطح زبرتر است؟":"اصطکاک کدام سطح از همه بیشتر است؟";expl="پرزهای فرش جلوی سُر خوردن را می‌گیرند؛ پس فرش بیشترین اصطکاک را دارد.";}
  A.prompt(`${text}<small>روی یکی از سطح‌ها بزن یا از دکمه‌ها انتخاب کن.</small>`);
  const c=A.ctrl("");let m;const choose=i=>{if(A.locked)return;fr.st.pick=i;fr.render();
    if(i===ans){m.disable();m.mark(i,"right");fr.run(()=>A.judge(true,{ok:expl}));}
    else{m.mark(i,"wrong");const res=A.judge(false,{retry:"به زبری سطح فکر کن: هرچه زبرتر، اصطکاک بیشتر.",final:"جواب: "+fr.lanes[ans].n+". "+expl});if(A.locked){m.disable();m.mark(ans,"right");fr.run();}}};
  m=mcq(c,fr.lanes.map(L=>L.n),i=>choose(i));A.onLane=choose;}
