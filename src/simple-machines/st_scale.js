/* ================= ایستگاه جرم و وزن: ترازو و نیروسنج ================= */
const OB={
 melon:{n:"هندوانه",w:76,h:54,d:`<ellipse cx="0" cy="-27" rx="38" ry="27" fill="#3E9B4F"/><path d="M-26 -47 q-8 20 0 40 M-9 -53 q-6 26 0 52 M9 -53 q6 26 0 52 M26 -47 q8 20 0 40" stroke="#26713A" stroke-width="4" fill="none"/><ellipse cx="-14" cy="-40" rx="10" ry="5" fill="#fff" opacity=".22"/>`},
 apple:{n:"سیب",w:30,h:34,d:`<circle cx="0" cy="-14" r="14" fill="#E23E3E"/><path d="M0 -27 q2 -6 6 -8" stroke="#6B4A2B" stroke-width="2.5" fill="none"/><ellipse cx="9" cy="-31" rx="6" ry="3" fill="#4CAF50" transform="rotate(-25 9 -31)"/><ellipse cx="-5" cy="-19" rx="3.5" ry="5" fill="#fff" opacity=".4"/>`},
 balloon:{n:"بادکنک",w:54,h:72,d:`<path d="M0 -4 l-6 -7 h12z" fill="#D63F55"/><ellipse cx="0" cy="-42" rx="26" ry="31" fill="#FF6F7D"/><ellipse cx="-10" cy="-54" rx="7" ry="11" fill="#fff" opacity=".45"/>`},
 pillow:{n:"بالش",w:86,h:38,d:`<path d="M-43 -4 Q-46 -19 -41 -34 Q0 -40 41 -34 Q46 -19 43 -4 Q0 2 -43 -4Z" fill="#F7F9FC" stroke="#B7C6D4" stroke-width="2"/><path d="M-26 -19 h52" stroke="#D5E0EA" stroke-width="2" stroke-dasharray="4 4"/>`},
 book:{n:"کتاب",w:62,h:22,d:`<rect x="-31" y="-22" width="62" height="22" rx="3" fill="#3E6FD8"/><rect x="-24" y="-17" width="52" height="6" fill="#fff" opacity=".92"/><rect x="-31" y="-22" width="8" height="22" fill="#2D56B3"/>`},
 stone:{n:"سنگ",w:42,h:26,d:`<path d="M-20 0 Q-24 -14 -11 -21 Q0 -27 13 -20 Q24 -11 20 0Z" fill="#8D96A3"/><path d="M-20 0 Q-10 -6 20 0Z" fill="#6F7885"/><path d="M-8 -17 Q0 -21 8 -17" stroke="#fff" stroke-width="2.5" opacity=".45" fill="none"/>`},
 brick:{n:"آجر",w:56,h:26,d:`<rect x="-28" y="-26" width="56" height="26" rx="2" fill="#C8553D"/><path d="M-28 -13 h56 M-9 -26 v13 M10 -13 v13" stroke="#EBA08E" stroke-width="2"/>`},
 rice:{n:"کیسهٔ برنج",w:56,h:64,d:`<path d="M-26 0 Q-30 -36 -18 -52 L-6 -58 L6 -58 L18 -52 Q30 -36 26 0Z" fill="#EAD9B3" stroke="#B89A5E" stroke-width="2"/><rect x="-9" y="-62" width="18" height="7" rx="3" fill="#B89A5E"/><rect x="-18" y="-36" width="36" height="18" rx="4" fill="#fff"/><text x="0" y="-22" text-anchor="middle" font-size="11" font-weight="700" fill="#8A6A2E">برنج</text>`},
 backpack:{n:"کیف مدرسه",w:52,h:60,d:`<rect x="-24" y="-58" width="48" height="58" rx="14" fill="#4F7FD8"/><rect x="-16" y="-28" width="32" height="22" rx="7" fill="#3B66B8"/><path d="M-12 -58 q12 -12 24 0" stroke="#2D56B3" stroke-width="4" fill="none"/>`},
 dumbbell:{n:"دمبل",w:66,h:30,d:`<rect x="-24" y="-17" width="48" height="6" rx="3" fill="#8C9BB0"/><rect x="-33" y="-30" width="13" height="30" rx="4" fill="#34425E"/><rect x="20" y="-30" width="13" height="30" rx="4" fill="#34425E"/>`},
 car:{n:"ماشین اسباب‌بازی",w:58,h:32,d:`<path d="M-28 -10 V-18 Q-26 -22 -18 -22 L-10 -32 H10 L18 -22 Q26 -22 28 -18 V-10Z" fill="#E4553A"/><rect x="-6" y="-30" width="13" height="8" rx="2" fill="#CFEFFB"/><circle cx="-15" cy="-8" r="7" fill="${INK}"/><circle cx="15" cy="-8" r="7" fill="${INK}"/>`},
 cotton:{n:"کیسهٔ پنبه",w:92,h:68,d:`<path d="M-42 0 Q-50 -30 -34 -44 Q-30 -62 -12 -60 Q0 -72 14 -60 Q34 -62 36 -44 Q52 -30 42 0Z" fill="#FFFFFF" stroke="#C7D3DE" stroke-width="2.5"/><text x="0" y="-22" text-anchor="middle" font-size="13" font-weight="700" fill="#7D8CA3">پنبه</text>`},
 iron:{n:"تکهٔ آهن",w:40,h:24,d:`<path d="M-20 0 V-18 L-12 -24 H20 V-6 L12 0Z" fill="#4A5566"/><path d="M-20 -18 H12 L20 -24" stroke="#6C7890" stroke-width="2" fill="none"/><text x="-4" y="-6" text-anchor="middle" font-size="10" font-weight="700" fill="#D6DEE8">آهن</text>`},
 myA:{n:"جعبهٔ الف",w:48,h:48,d:`<rect x="-24" y="-48" width="48" height="48" rx="6" fill="#8B5CD6"/><rect x="-24" y="-48" width="48" height="10" rx="5" fill="#A57FE3"/><text x="0" y="-12" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">؟</text>`},
 myB:{n:"استوانهٔ ب",w:44,h:56,d:`<rect x="-22" y="-50" width="44" height="50" fill="#1F9E8E"/><ellipse cx="0" cy="-50" rx="22" ry="7" fill="#43C0AF"/><ellipse cx="0" cy="0" rx="22" ry="7" fill="#1F9E8E"/><text x="0" y="-14" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">؟</text>`},
 myC:{n:"بستهٔ ج",w:56,h:42,d:`<rect x="-28" y="-42" width="56" height="42" rx="8" fill="#E8590C"/><path d="M-28 -24 h56 M0 -42 v42" stroke="#FFD2B5" stroke-width="3"/><text x="13" y="-6" text-anchor="middle" font-size="18" font-weight="700" fill="#fff">؟</text>`}
};
const MASS={cube:{balloon:1,apple:2,pillow:2,book:3,car:4,stone:5,rice:6,melon:8,myA:7,myB:9,myC:6,cotton:4,iron:4},/* هر چیز در کیلوگرم و گرم یک جرم دارد (گرم = ۱۰۰۰ × کیلوگرم)؛ چیزهایی که جرمشان کیلوگرمِ درست نیست فقط در گرم آمده‌اند */
 kg:{dumbbell:3,melon:4,rice:5,stone:5,myA:7,myC:12,cotton:1,iron:1},g:{apple:200,book:600,car:300,myB:1300,cotton:1000,iron:1000,backpack:1800,rice:5000}};
const WDIM={cube:{1:[32,32]},kg:{1:[42,32],2:[48,38],5:[58,46],10:[66,54]},g:{100:[36,28],200:[42,32],500:[50,38],1000:[58,46],2000:[64,52]}};
function fmtM(v,u){if(u==="cube")return `${fa(v)} مکعب`;if(u==="kg")return `${fa(v)} کیلوگرم`;if(v>=1000&&v%1000===0)return `${fa(v/1000)} کیلوگرم`;if(v>1000)return `${fa(Math.floor(v/1000))} کیلوگرم و ${fa(v%1000)} گرم`;return `${fa(v)} گرم`;}
function wLabel(v,u){if(u==="cube")return "";return fa(v);}
function wLabelLong(v,u){if(u==="cube")return "۱ مکعب";if(u==="kg")return `${fa(v)} کیلوگرم`;return v>=1000?`${fa(v/1000)} کیلوگرم`:`${fa(v)} گرم`;}
function wSvg(x,yb,v,u,hl){const dm=(WDIM[u]||{})[v]||[40,34],w=dm[0],h=dm[1];
  if(u==="cube")return `<g><rect x="${x-w/2}" y="${yb-h}" width="${w}" height="${h}" rx="5" fill="#FFC43D" stroke="${hl?"#1E6FD9":"#D99A12"}" stroke-width="${hl?3.5:2}"/><rect x="${x-w/2+4}" y="${yb-h+4}" width="${w-8}" height="6" rx="3" fill="#FFE08A"/></g>`;
  return `<g><rect x="${x-5}" y="${yb-h-7}" width="10" height="9" rx="3" fill="#6F7E93"/><rect x="${x-w/2}" y="${yb-h}" width="${w}" height="${h}" rx="7" fill="#93A2B6" stroke="${hl?"#1E6FD9":"#5E6E86"}" stroke-width="${hl?3.5:2}"/><rect x="${x-w/2+3}" y="${yb-h+3}" width="${w-6}" height="${h*.28}" rx="5" fill="#B9C5D3"/>${T(x,yb-h*.28,wLabel(v,u),{size:v>=1000?13:16,col:"#1B2A41",halo:false})}</g>`;}
const itW=(it,u)=>it.k==="w"?((WDIM[u]||{})[it.v]||[40])[0]:OB[it.id].w;
const itM=(it,u)=>it.k==="w"?it.v:MASS[u][it.id];
function itSvg(it,x,yb,u,hl){if(it.k==="w")return wSvg(x,yb,it.v,u,hl);return `<g transform="translate(${x} ${yb})">${OB[it.id].d}</g>`;}
function layoutPan(items,cx,py,u){const out=[];let row=[],rw=0,yb=py+2;const rows=[];
  items.forEach(it=>{const w=itW(it,u)+4;if(rw+w>184&&row.length){rows.push(row);row=[];rw=0;}row.push(it);rw+=w;});if(row.length)rows.push(row);
  rows.forEach(r=>{const tw=r.reduce((a,it)=>a+itW(it,u)+4,0);let x=cx-tw/2;let mh=0;r.forEach(it=>{const w=itW(it,u)+4;out.push({it,x:x+w/2,yb});x+=w;mh=Math.max(mh,it.k==="w"?((WDIM[u]||{})[it.v]||[0,34])[1]+7:OB[it.id].h);});yb-=mh+2;});
  return out;}

function makeBalance(A,cfg){
  const svg=A.svg,P=A.P,u=cfg.unit;A.view(cfg.edit?520:404);
  const st={L:(cfg.L||[]).map(x=>Object.assign({},x)),R:(cfg.R||[]).map(x=>Object.assign({},x)),edit:cfg.edit||"",tray:cfg.tray||[],objTray:cfg.objTray||null,trayMode:"w",locked:cfg.locked!==false,a:0,sel:null,hover:null,busy:false,hideL:!!cfg.hideL,hideR:!!cfg.hideR};
  const mass=side=>st[side].reduce((s,it)=>s+itM(it,u),0);
  const canEdit=side=>!A.locked&&(st.edit==="both"||st.edit===side);
  const geo=()=>{const cx=320,cy=112,Lb=196,rad=st.a*Math.PI/180,c=Math.cos(rad),s=Math.sin(rad);return{cx,cy,lx:cx-Lb*c,ly:cy+Lb*s,rx:cx+Lb*c,ry:cy-Lb*s};};
  const panY=(y)=>y+150;
  function render(){const g=geo(),mL=mass("L"),mR=mass("R"),bal=mL===mR&&!st.locked;
    let s=cfg.bg==="moon"?moonBg(392)+placeTag("moon",540,40):bgRoom(392);
    s+=`<rect x="250" y="382" width="140" height="14" rx="7" fill="#46546E"/><rect x="312" y="${g.cy}" width="16" height="272" rx="6" fill="#5E6E86"/>`;
    const arcR=64;s+=`<path d="M${g.cx-arcR*Math.sin(.5)} ${g.cy-arcR*Math.cos(.5)} A${arcR} ${arcR} 0 0 1 ${g.cx+arcR*Math.sin(.5)} ${g.cy-arcR*Math.cos(.5)}" stroke="#C7D3DE" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M${g.cx} ${g.cy-arcR-6} V${g.cy-arcR+6}" stroke="${GRN}" stroke-width="4"/>`;
    const na=-st.a*Math.PI/180;s+=`<line x1="${g.cx}" y1="${g.cy}" x2="${g.cx+Math.sin(na)*-58}" y2="${g.cy-Math.cos(na)*58}" stroke="${bal?GRN:"#C93B22"}" stroke-width="4" stroke-linecap="round"/>`;
    s+=`<line x1="${g.lx}" y1="${g.ly}" x2="${g.rx}" y2="${g.ry}" stroke="#34425E" stroke-width="10" stroke-linecap="round"/><circle cx="${g.cx}" cy="${g.cy}" r="10" fill="#FFC43D" stroke="#34425E" stroke-width="3"/>`;
    for(const side of["L","R"]){const x=side==="L"?g.lx:g.rx,y=side==="L"?g.ly:g.ry,py=panY(y),hov=st.hover===side;
      if(st.locked)s+=`<rect x="${x-10}" y="${py+14}" width="20" height="${392-py-14}" fill="#E8590C" opacity=".85"/><path d="M${x-10} ${py+30} l20 -12 M${x-10} ${py+60} l20 -12 M${x-10} ${py+90} l20 -12" stroke="#fff" stroke-width="4" opacity=".6"/>`;
      s+=`<path d="M${x} ${y} L${x-84} ${py} M${x} ${y} L${x+84} ${py}" stroke="#7D8CA3" stroke-width="2.5"/><circle cx="${x}" cy="${y}" r="5" fill="#34425E"/>`;
      s+=`<g data-zone="pan" data-side="${side}"><path d="M${x-96} ${py} Q${x} ${py+34} ${x+96} ${py}Z" fill="${hov?"#FFF3C4":"#D5DEE8"}" stroke="${hov?"#F0B429":"#8C9BB0"}" stroke-width="3"/>${canEdit(side)?`<rect x="${x-100}" y="${py-150}" width="200" height="190" fill="#fff" fill-opacity="0"/>`:""}</g>`;
      layoutPan(st[side],x,py,u).forEach((p,i)=>{const drag=canEdit(side)&&!p.it.fixed;s+=`<g ${drag?`data-drag="pan" data-side="${side}" data-i="${st[side].indexOf(p.it)}" style="cursor:grab"`:""}>${itSvg(p.it,p.x,p.yb,u)}</g>`;});
      if(S.forces&&st[side].length){const m=mass(side),gg=cfg.bg==="moon"?1.6:10,hide=side==="L"?st.hideL:st.hideR,len=(18+Math.min(60,m/(u==="g"?60:u==="kg"?1.3:1)*6))*(gg/10)+8,ax=x+(side==="L"?64:-64),L2=Math.max(30,Math.min(len,314-(py+22))),col=side==="L"?BLUE:RED,tip=py+22+L2;s+=arrow(ax,py+22,ax,tip,10,col);const side2=tip+54>398,lx2=side2?ax+(side==="L"?16:-16):ax,ly=side2?py+22+L2/2-4:tip+22,lo=side2?{size:12,col,anchor:side==="L"?"end":"start"}:{size:12,col};s+=T(lx2,ly,"وزن",lo);if(!(hide||u==="cube"))s+=T(lx2,ly+26,`<tspan class="num">${fa(r1((u==="g"?m/1000:m)*gg))} نیوتن</tspan>`,lo);}}
    if(st.edit){s+=trayPanel("",404);
      if(st.trayMode==="w"&&u!=="cube")s+=T(28,436,u==="kg"?"کیلوگرم":"گرم",{size:12,col:MUT,anchor:"end"});
      if(st.trayMode==="w"){const n=st.tray.length;st.tray.forEach((v,j)=>{const x=320+(j-(n-1)/2)*Math.min(90,560/n),sel=st.sel&&st.sel.k==="w"&&st.sel.v===v;s+=`<g data-drag="tray" data-k="w" data-v="${v}" style="cursor:grab"><rect x="${x-44}" y="420" width="88" height="90" fill="#fff" fill-opacity="0"/><g transform="translate(${x} 500) scale(1.2) translate(${-x} -500)">${wSvg(x,500,v,u,sel)}</g></g>`;});}
      else{const n=st.objTray.length;st.objTray.forEach((id,j)=>{const x=320+(j-(n-1)/2)*Math.min(96,600/n),sc=Math.min(1,62/OB[id].h,60/OB[id].w),sel=st.sel&&st.sel.id===id;s+=`<g data-drag="tray" data-k="o" data-id="${id}" style="cursor:grab"><rect x="${x-44}" y="426" width="88" height="84" rx="12" fill="${sel?"#FFF3C4":"#fff"}" fill-opacity="${sel?1:0}"/><g transform="translate(${x} 500) scale(${sc})">${OB[id].d}</g></g>`;});}}
    P.paint(s);
    const lab=(side)=>{const hide=side==="L"?st.hideL:st.hideR;return hide?"<b>؟</b>":`<b class="num">${fmtM(mass(side),u)}</b>`;};
    A.counter(`<span class="cc l">جرم کفهٔ چپ: ${lab("L")}</span><span class="cc r">جرم کفهٔ راست: ${lab("R")}</span><span class="cc">وزنه‌های روی ترازو: <b>${fa(st.L.concat(st.R).filter(it=>it.k==="w").length)}</b></span>`);
    const note=`<span class="lg"><span class="lgi">ترازوی دوکفه‌ای کشش زمین (وزن) روی دو کفه را با هم مقایسه می‌کند. چون زمین هر کیلوگرم را در هر دو کفه یکسان می‌کشد، ترازوی صاف یعنی جرم دو طرف برابر است. روی ماه هم همین جواب را می‌دهد، چون وزنِ هر دو کفه به یک نسبت کم می‌شود و ترازو باز هم صاف می‌ماند.</span></span>`;
    if(u==="cube")A.formula(`<span class="fl">قانون ترازو</span><span>وقتی دو کفه هم‌جرم باشند، ترازو صاف می‌ماند.</span>`+note);
    else{const un=u==="g"?"g":"kg",mL=mass("L"),mR=mass("R"),showN=!st.hideL&&!st.hideR&&st.L.length&&st.R.length&&!st.locked;A.formula(FX(`${sy("m","1")} = ${sy("m","2")}`,showN?`${fa(mL)} ${un} ${mL===mR?"=":mL>mR?"&gt;":"&lt;"} ${fa(mR)} ${un}`:"",[[sy("m","1"),"جرم کفهٔ چپ"],[sy("m","2"),"جرم کفهٔ راست"]])+note);}
  }
  function settle(done){const mL=mass("L"),mR=mass("R"),d=mL-mR,mx=Math.max(mL,mR,1);let to=0;if(!st.locked&&d!==0)to=Math.sign(d)*clamp(Math.abs(d)/mx*24,4,13);
    const from=st.a,id=st.tw=(st.tw||0)+1;if(Math.abs(to-from)<.01){render();done&&done();return;}st.busy=true;tween(600,p=>{if(id!==st.tw)return;st.a=from+(to-from)*ease(p);render();},()=>{if(id!==st.tw)return;st.busy=false;render();done&&done();});}
  const panHit=p=>{const g=geo();for(const side of["L","R"]){const x=side==="L"?g.lx:g.rx,py=panY(side==="L"?g.ly:g.ry);if(Math.abs(p.x-x)<112&&p.y>py-170&&p.y<py+50)return side;}return null;};
  const addTo=(side,g)=>{st[side].push(g.k==="w"?{k:"w",v:g.v}:{k:"o",id:g.id});};
  dragKit(svg,{blocked:()=>A.locked,
    start(d){if(d.drag==="tray")return{from:"tray",k:d.k,v:+d.v,id:d.id};if(d.drag==="pan"){if(!canEdit(d.side))return null;const it=st[d.side][+d.i];return{from:"pan",side:d.side,i:+d.i,k:it.k,v:it.v,id:it.id};}return null;},
    begin(g,p){if(g.from==="pan")st[g.side].splice(g.i,1);st.sel=null;P.ghost(g.k==="w"?`<g transform="scale(1.2)">${wSvg(0,20,g.v,u,true)}</g>`:`<g transform="translate(0 30)">${OB[g.id].d}</g>`,p.x,p.y);render();},
    move(g,p){P.move(p.x,p.y);const h=panHit(p);const h2=h&&canEdit(h)?h:null;if(h2!==st.hover){st.hover=h2;render();}},
    end(g,p){P.clear();st.hover=null;const h=panHit(p);if(h&&canEdit(h))addTo(h,g);settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();},
    tap(g){if(g.from==="tray"){st.sel={k:g.k,v:g.v,id:g.id};A.fb("حالا روی یکی از کفه‌ها بزن.","info");render();}else{st[g.side].splice(g.i,1);settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();}},
    zoneTap(z){if(z.zone==="pan"&&st.sel&&canEdit(z.side)){addTo(z.side,st.sel);A.fb("");settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();}}});
  const setLock=(v,done)=>{st.locked=v;settle(done);};
  settle();
  return{st,render,settle,setLock,mass};
}


/* ================= نیروسنج، ماه و آب ================= */
const GV={earth:10,moon:1.6};
/* هر سه جسم زیر آب: حجم ۱ یا ۲ لیتر؛ نیروی شناوری روی زمین = ۱۰ نیوتن برای هر لیتر */
const SPR={stone:{m:5,Fb:20,sc:1.7},brick:{m:2,Fb:10,sc:1.6},iron:{m:8,Fb:10,sc:1.6}};
function moonBg(fy){let s=`<rect width="640" height="520" fill="#1B2440"/>`;
  [[40,40],[120,90],[210,30],[300,70],[420,24],[500,96],[590,140],[80,170],[250,150],[360,120],[460,180]].forEach(([x,y])=>s+=`<circle cx="${x}" cy="${y}" r="1.8" fill="#fff" opacity=".8"/>`);
  s+=`<circle cx="604" cy="36" r="16" fill="#3E7BD8"/><path d="M594 30 q7 -5 12 2 q-3 7 -10 5z M607 42 q5 -2 7 3 q-5 4 -8 0z" fill="#4CAF50"/>`;
  s+=`<rect y="${fy}" width="640" height="${520-fy}" fill="#B9C2CF"/><ellipse cx="150" cy="${fy+24}" rx="30" ry="6" fill="#9AA4B3"/><ellipse cx="480" cy="${fy+40}" rx="44" ry="8" fill="#9AA4B3"/><rect y="${fy}" width="640" height="3" fill="#8E98A8"/>`;return s;}
function placeTag(place,x,y){return `<g><rect x="${x-62}" y="${y-22}" width="124" height="36" rx="18" fill="${place==="moon"?"#E9EDF3":"#FFFFFF"}" stroke="${place==="moon"?"#8E98A8":"#8ACB74"}" stroke-width="2"/>`+T(x,y+4,place==="moon"?"روی ماه":"روی زمین",{size:15,col:INK,halo:false})+`</g>`;}

function makeSpring(A,cfg){
  const svg=A.svg,P=A.P;A.view(404);
  const o=OB[cfg.obj],sp=SPR[cfg.obj]||{sc:1.2},sc=cfg.sc||sp.sc,oh=o.h*sc,WT=262,ROD=170,TUB=104;
  const st={hy:cfg.water?40:64,place:cfg.place||"earth",hide:!!cfg.hide};
  const W=()=>cfg.m*GV[st.place],FB=()=>(cfg.Fb||0)*GV[st.place]/10;
  const sub=()=>{if(!cfg.water)return 0;const bot=st.hy+ROD+oh;return clamp((bot-WT)/oh,0,1);};
  const read=()=>r1(W()-sub()*FB());
  const mx=cfg.max||Math.max(20,Math.ceil(cfg.m*10*1.15/10)*10);
  function render(){const moon=st.place==="moon",cx=320,hy=st.hy;let s=moon?moonBg(382):bgRoom(382);
    s+=`<rect x="96" y="10" width="16" height="368" rx="5" fill="#8C9BB0"/><rect x="96" y="10" width="${cx-60}" height="14" rx="6" fill="#8C9BB0"/><rect x="66" y="372" width="76" height="12" rx="5" fill="#5E6E86"/>`;
    s+=placeTag(st.place,540,cfg.water?110:70);
    if(cfg.water)s+=`<rect x="166" y="${WT-34}" width="308" height="${384-WT+34}" rx="12" fill="#fff" fill-opacity=".45" stroke="#7FA7C4" stroke-width="4"/><rect x="170" y="${WT}" width="300" height="${380-WT}" rx="8" fill="#6EC3EA" fill-opacity=".6"/><path d="M170 ${WT} q37.5 -6 75 0 t75 0 t75 0 t75 0" stroke="#3E9BD0" stroke-width="3" fill="none"/>`+T(452,368,"آب",{size:13,col:"#1D6FA5",anchor:"start",halo:false});
    const tt=hy+8,tb=hy+TUB,y0=tt+14,y1=tb-12,py=v=>y0+(y1-y0)*clamp(v/mx,0,1),pv=read();
    let g=`<line x1="${cx}" y1="24" x2="${cx}" y2="${hy}" stroke="#5E6E86" stroke-width="3"/>`;
    g+=`<rect x="${cx-28}" y="${tt}" width="56" height="${tb-tt}" rx="14" fill="#fff" stroke="#8C9BB0" stroke-width="3"/>`;
    for(let i=0;i<=10;i++){const y=py(mx*i/10);g+=`<line x1="${cx+8}" y1="${y}" x2="${cx+(i%5?16:22)}" y2="${y}" stroke="#8C9BB0" stroke-width="2"/>`;}
    if(NUMS()&&!st.hide)[0,.5,1].forEach(f=>g+=T(cx+30,py(mx*f)+4,fa(mx*f),{size:11,col:MUT,halo:false,anchor:"end"}));
    if(sub()>0.02)g+=`<line x1="${cx-24}" y1="${py(W())}" x2="${cx+24}" y2="${py(W())}" stroke="#E8590C" stroke-width="2.5" stroke-dasharray="4 4" opacity=".8"/>`;
    let zz=`M${cx-4} ${y0-12}`;const n=8,ye=py(pv)-5;for(let i=1;i<=n;i++)zz+=` L${cx+(i%2?-14:4)} ${y0-12+i*(ye-y0+12)/n}`;
    g+=`<path d="${zz}" stroke="#7D8CA3" stroke-width="3" fill="none"/><rect x="${cx-22}" y="${py(pv)-4}" width="36" height="8" rx="3" fill="#E8590C"/>`;
    g+=`<line x1="${cx}" y1="${py(pv)}" x2="${cx}" y2="${hy+ROD}" stroke="#5E6E86" stroke-width="3"/>`;
    const ob=hy+ROD+oh;g+=`<g transform="translate(${cx} ${ob}) scale(${sc})">${o.d}</g>`;
    if(cfg.lower)g+=`<circle cx="${cx}" cy="${hy}" r="15" fill="#FFC43D" stroke="#D99A12" stroke-width="3"/><path d="M${cx} ${hy-8} v16 M${cx-5} ${hy-3} l5 -5 5 5 M${cx-5} ${hy+3} l5 5 5 -5" stroke="#8A5A00" stroke-width="2" fill="none"/>`;
    s+=cfg.lower?`<g data-drag="hook" style="cursor:grab"><rect x="${cx-70}" y="${hy-24}" width="140" height="${ob-hy+30}" fill="#fff" fill-opacity="0"/>${g}</g>`:g;
    s+=T(cx-40,tt+30,"نیروسنج",{size:12,col:INK,anchor:"start",haloCol:moon?"#DDE3EC":"#fff"});
    if(NUMS())s+=T(cx-40,tt+60,st.hide?"؟ نیوتن":`${fa(pv)} نیوتن`,{size:15,col:"#C93B22",anchor:"start"});
    if(S.forces){const top=ob-oh,wl=14+Math.min(46,W()*.6);s+=arrow(cx+58,top,cx+58,top+wl,9,RED)+T(cx+76,top+16,"وزن",{size:12,col:RED,anchor:"end"});
      if(sub()>0.02){const bl=10+Math.min(46,FB()*sub()*1.4);const bw=KID()?["نیروی","آب"]:["نیروی","شناوری"];s+=arrow(cx-54,ob,cx-54,ob-bl,9,BLUE)+T(cx-70,Math.min(ob-bl/2,348)-12,bw[0],{size:12,col:BLUE,anchor:"start"})+T(cx-70,Math.min(ob-bl/2,348)+18,bw[1],{size:12,col:BLUE,anchor:"start"});}}
    P.paint(s);
    if(NUMS())A.counter(`<span class="cc">عدد نیروسنج: <b class="num">${st.hide?"؟":fa(pv)+" نیوتن"}</b></span>${cfg.water?`<span class="cc">${sub()>.98?"کاملاً زیر آب":sub()>.02?"تا نیمه در آب":"بیرون از آب"}</span>`:""}<span class="cc">جرم: <b class="num">${cfg.hideM?"؟":fa(cfg.m)+" کیلوگرم"}</b></span>`);
    else A.counter("");
    if(cfg.onRender)cfg.onRender();}
  const hmin=40,hmax=cfg.water?Math.min(150,372-ROD-oh):64;
  dragKit(svg,{blocked:()=>A.locked&&!A.lab,start:(d,p)=>d.drag==="hook"&&cfg.lower?{h0:st.hy,y0:p.y}:null,
    move(g,p){st.hy=clamp(g.h0+(p.y-g.y0),hmin,hmax);render();},end(g,p){if(p.y>-9000)st.hy=clamp(g.h0+(p.y-g.y0),hmin,hmax);render();if(cfg.onDrop)cfg.onDrop(sub());}});
  render();
  return{st,render,read,sub,W,FB,setPlace(pl){st.place=pl;render();}};
}
/* دو نیروسنج کنار هم: زمین و ماه */
function springPanel(x0,w,where,massKg,reading,label){const moon=where==="moon";let s=`<g><rect x="${x0}" y="16" width="${w}" height="376" rx="18" fill="${moon?"#1E2A44":"#DDF0F8"}"/>`;
  if(moon)s+=`<circle cx="${x0+w-40}" cy="54" r="16" fill="#3E7BD8"/>`+[30,90,150,220].map((x,i)=>`<circle cx="${x0+x}" cy="${40+i*17%50}" r="1.6" fill="#fff"/>`).join("");
  else s+=`<circle cx="${x0+w-44}" cy="60" r="20" fill="#FFD66B"/>`;
  s+=`<rect x="${x0}" y="352" width="${w}" height="40" fill="${moon?"#B9C2CF":"#8ACB74"}"/>`+T(x0+w/2,378,moon?"روی ماه":"روی زمین",{size:17,col:moon?INK:"#1B4D2A",halo:false});
  const cx=x0+w/2,hung=reading!=null,sl=hung?40+Math.min(110,reading*1.6):34;
  s+=`<rect x="${cx-40}" y="30" width="80" height="10" rx="4" fill="#5E6E86"/><line x1="${cx}" y1="40" x2="${cx}" y2="56" stroke="#5E6E86" stroke-width="3"/>`;
  s+=`<rect x="${cx-34}" y="56" width="68" height="${sl+40}" rx="10" fill="#fff" stroke="#8C9BB0" stroke-width="2.5"/>`;
  let zz=`M${cx} 66`;const n=9;for(let i=1;i<=n;i++)zz+=` L${cx+(i%2?-12:12)} ${66+i*(sl-10)/n}`;s+=`<path d="${zz}" stroke="#7D8CA3" stroke-width="3" fill="none"/>`;
  const ry=66+sl;s+=`<rect x="${cx-26}" y="${ry-4}" width="52" height="8" rx="3" fill="#E8590C"/>`;
  s+=T(cx+44,ry+7,!hung?"؟":NUMS()?`${fa(reading)} نیوتن`:"",{size:14,col:"#C93B22",anchor:"end",haloCol:moon?"#1E2A44":"#fff"});
  if(hung)s+=`<line x1="${cx}" y1="${ry+4}" x2="${cx}" y2="${96+sl+14}" stroke="#5E6E86" stroke-width="3"/><g transform="translate(${cx} ${150+sl+10}) scale(.9)">${OB.rice.d}</g>`+T(cx,160+sl+22,label,{size:13,col:moon?"#fff":INK,haloCol:moon?"#1E2A44":"#fff"});
  else s+=`<g transform="translate(${cx+60} 350) scale(.8)">${OB.rice.d}</g>`;
  return s+"</g>";}
/* ترازوی حمام روی ماه */
function bathScene(){let s=moonBg(330)+placeTag("moon",540,110);
  s+=`<rect x="226" y="300" width="188" height="40" rx="16" fill="#F2F5F9" stroke="#8C9BB0" stroke-width="3"/><rect x="282" y="308" width="76" height="22" rx="5" fill="#1B2A41"/>`+T(320,325,"؟ کیلوگرم",{size:12,col:"#7CF2A5",halo:false});
  s+=`<g transform="translate(320 300)"><rect x="-22" y="-120" width="44" height="70" rx="18" fill="#E4553A"/><circle cx="0" cy="-138" r="20" fill="#F6C9A6"/><rect x="-18" y="-52" width="14" height="52" rx="6" fill="#34425E"/><rect x="4" y="-52" width="14" height="52" rx="6" fill="#34425E"/><rect x="-26" y="-150" width="52" height="20" rx="10" fill="#fff" opacity=".85"/><circle cx="0" cy="-140" r="22" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/></g>`;
  return s;}

const ST_scale={key:"scale",name:"جرم و وزن",c:"#3B6FD4",sub:"ترازوی دوکفه‌ای، نیروسنج، ماه و آب",
 intro:"ترازوی دوکفه‌ای جرم دو چیز را با هم مقایسه می‌کند. نیروسنج وزن را اندازه می‌گیرد، و وزن یک نیروست. روی ماه و در آب ببین کدام عوض می‌شود و کدام نه.",
 art(){let h=bgRoom(392).replace(/id="g/g,'id="as').replace(/url\(#g/g,"url(#as");h+=`<rect x="250" y="382" width="140" height="14" rx="7" fill="#46546E"/><rect x="312" y="112" width="16" height="272" rx="6" fill="#5E6E86"/>`;const a=-8*Math.PI/180,lx=320-196*Math.cos(a),ly=112+196*Math.sin(a),rx=320+196*Math.cos(a),ry=112-196*Math.sin(a);
   h+=`<line x1="${lx}" y1="${ly}" x2="${rx}" y2="${ry}" stroke="#34425E" stroke-width="10" stroke-linecap="round"/><circle cx="320" cy="112" r="10" fill="#FFC43D" stroke="#34425E" stroke-width="3"/>`;
   for(const [x,y] of[[lx,ly],[rx,ry]]){const py=y+150;h+=`<path d="M${x} ${y} L${x-84} ${py} M${x} ${y} L${x+84} ${py}" stroke="#7D8CA3" stroke-width="2.5"/><path d="M${x-96} ${py} Q${x} ${py+34} ${x+96} ${py}Z" fill="#D5DEE8" stroke="#8C9BB0" stroke-width="3"/>`;}
   h+=`<g transform="translate(${lx} ${ly+152})">${OB.balloon.d}</g>`+wSvg(rx-24,ry+152,5,"kg")+wSvg(rx+26,ry+152,2,"kg");return h;},
 lab(A){
   let mode="bal",b,spr,obj="stone",place="earth";
   function balMode(){mode="bal";A.prompt("آزمایشگاه ترازوی دوکفه‌ای: وزنه یا شیء را روی هر کفه بکش. برای برداشتن، آن را بیرون بکش یا رویش بزن.");
     let u=KID()?"cube":"kg";const mk=()=>{b=makeBalance(A,{unit:u,edit:"both",tray:u==="cube"?[1]:u==="kg"?[1,2,5,10]:[100,200,500,1000],objTray:["melon","apple","balloon","pillow","book","stone","rice","cotton","iron","dumbbell","backpack"].filter(id=>MASS[u][id]!=null),locked:false});A.refresh=()=>b.render();};
     mk();const c=A.ctrl("");
     btn(c,"وزنه‌ها","",()=>{b.st.trayMode="w";b.render();});btn(c,"اشیا","",()=>{b.st.trayMode="o";b.render();});
     if(!KID())btn(c,"کیلوگرم / گرم","",()=>{u=u==="kg"?"g":"kg";mk();A.fb(u==="g"?"حالا وزنه‌ها به گرم است. هر کیلوگرم ۱۰۰۰ گرم است.":"حالا وزنه‌ها به کیلوگرم است.","info");});
     btn(c,"خالی کردن کفه‌ها","",()=>{b.st.L=[];b.st.R=[];b.settle();});
     btn(c,"نیروسنج و آب","pri",sprMode);}
   function sprMode(){mode="spr";A.prompt(KID()?"سنگ را با دستگیرهٔ زرد پایین ببر و در آب فرو کن. به فنر نگاه کن.":"آزمایشگاه نیروسنج: دستگیرهٔ زرد را پایین بکش تا جسم در آب برود. جسم را عوض کن یا به ماه برو و ببین عدد نیروسنج چه می‌شود.");A.fb("");
     const mk=()=>{spr=makeSpring(A,{obj,m:SPR[obj].m,Fb:SPR[obj].Fb,place,water:true,lower:true});A.refresh=()=>spr.render();};mk();
     A.formula(FX(`${sy("W")} = ${sy("m")} × ${sy("g")}`,"",[[sy("W"),"وزن (N)"],[sy("m"),"جرم (kg)"],[sy("g"),"وزنِ هر کیلوگرم (نیوتن بر کیلوگرم)؛ زمین ≈ ۱۰ و ماه ≈ ۱٫۶"]]));
     const c=A.ctrl("");
     ["stone","brick","iron"].forEach(id=>btn(c,OB[id].n,"",()=>{obj=id;mk();}));
     const pb=btn(c,"رفتن به ماه","",()=>{place=place==="earth"?"moon":"earth";pb.textContent=place==="earth"?"رفتن به ماه":"برگشت به زمین";spr.setPlace(place);});
     btn(c,"ترازوی دوکفه‌ای","pri",balMode);}
   balMode();},
 kid:[
  {id:"scale.a1",title:"کدام سنگین‌تر است؟",desc:"پیش‌بینی کن کدام کفه پایین می‌رود.",gen(r){return shuffle(r,[{t:"heavier",u:"cube",L:["apple"],R:["melon"]},{t:"heavier",u:"cube",L:["balloon"],R:["stone"]},{t:"heavier",u:"cube",L:["book"],R:["book"]},{t:"heavier",u:"cube",L:["car"],R:["pillow"]},{t:"heavier",u:"cube",L:["rice"],R:["melon"]}]);}},
  {id:"scale.a2",title:"با مکعب صاف کن",desc:"مکعب بگذار تا ترازو صاف شود و بشمار چند مکعب شد.",gen(r){return shuffle(r,["apple","book","car","stone","pillow"]).map(id=>({t:"balance",u:"cube",obj:[id],tray:[1]}));}},
  {id:"scale.a3",title:"بزرگ اما سبک",desc:"چیزهای بزرگ همیشه سنگین نیستند!",gen(r){return[{t:"heavier",u:"cube",L:["cotton"],R:["iron"]},{t:"heavier",u:"cube",L:["balloon","pillow"],R:["car"]},{t:"balance",u:"cube",obj:["balloon","apple"],tray:[1]},{t:"heavier",u:"cube",L:["pillow"],R:["stone"]},{t:"balance",u:"cube",obj:["melon"],tray:[1]}];}},
  {id:"scale.a4",title:"روی ماه و در آب",desc:"نیروسنج را به ماه ببر و سنگ را در آب فرو کن. چه چیزی عوض می‌شود؟",gen(r){return[{t:"moon",q:1,ans:2},{t:"massq",ans:1},{t:"moonbal",ans:1},{t:"water",obj:"stone",ans:2},{t:"water",obj:"brick",ans:2}];}}],
 levels:[
  {id:"scale.1",title:"کدام سنگین‌تر است؟",desc:"با ترازوی دوکفه‌ای مقایسه کن و با مکعب‌ها جرم هر چیز را بشمار. بزرگ همیشه سنگین نیست!",gen(r){const b=pick(r,["book","pillow","car"]),m=pick(r,["melon","rice"]);
    return[{t:"heavier",u:"cube",L:["apple"],R:[m]},{t:"balance",u:"cube",obj:[b],tray:[1]},{t:"heavier",u:"cube",L:["balloon"],R:["stone"]},{t:"balance",u:"cube",obj:["pillow"],tray:[1]},{t:"heavier",u:"cube",L:["cotton"],R:["iron"]},{t:"balance",u:"cube",obj:[m],tray:[1]}];}},
  {id:"scale.2",title:"کیلوگرم و گرم",desc:"جرم را با وزنه‌های کیلوگرمی و گرمی بسنج. هر کیلوگرم ۱۰۰۰ گرم است.",gen(r){return[{t:"balance",u:"kg",obj:["melon"],tray:[1,2]},{t:"mystery",u:"kg",obj:["myA"],tray:[1,2,5]},{t:"heavier",u:"kg",L:["dumbbell","iron"],R:["melon"]},{t:"mystery",u:"g",obj:["book"],tray:[100,200,500]},{t:"heavier",u:"g",L:["cotton"],R:["iron"]},{t:"mystery",u:"g",obj:["myB"],tray:[100,200,500,1000]}];}},
  {id:"scale.3",title:"کمترین وزنه",desc:"ترازو را با کمترین تعداد وزنه صاف کن.",gen(r){return[{t:"fewest",u:"g",obj:["apple"],tray:[100,200,500]},{t:"mystery",u:"kg",obj:["myC"],tray:[1,2,5,10]},{t:"fewest",u:"g",obj:["book","apple"],tray:[100,200,500]},{t:"fewest",u:"kg",obj:["stone","dumbbell"],tray:[1,2,5]},{t:"mystery",u:"g",obj:["backpack"],tray:[100,200,500,1000]},{t:"fewest",u:"g",obj:["car","backpack"],tray:[100,200,500,1000]}];}},
  {id:"scale.4",title:"جرم و وزن",desc:"جرم مقدار ماده است و روی ماه عوض نمی‌شود. وزن نیروست و روی ماه کم می‌شود.",gen(r){const c=S.track==="c";
    return[{t:"moon",q:1,ans:2},{t:"wcalc",m:pick(r,[3,4,6,7]),where:"earth",obj:"rice"},{t:"massq",ans:1},{t:"moonbal",ans:1},c?{t:"wcalc",m:pick(r,[5,10,15]),where:"moon",obj:"rice"}:{t:"mcalc",W:pick(r,[20,30,40]),obj:"rice"},{t:"bath",ans:0}];}},
  {id:"scale.5",title:"وزن در آب",desc:"جسم را در آب فرو کن. آب آن را به بالا هل می‌دهد و عدد نیروسنج کم می‌شود.",gen(r){const c=S.track==="c";
    return[{t:"water",obj:"stone",ans:2},{t:"waterF",obj:"brick"},{t:"waterWhy",obj:"iron",ans:1},{t:"waterF",obj:"stone"},c?{t:"mcalc",W:80,obj:"iron"}:{t:"waterF",obj:"iron"},{t:"massq",ans:1,water:true}];}}],
 bLv:[0,1,3,4],cLv:[1,2,3,4],
 endless(r,d){const tp=pick(r,d<2?["heavier","balance"]:d<3.5?["heavier","balance","mystery","fewest","water"]:["mystery","fewest","wcalc","heavier","waterF","mcalc"]);
   if(tp==="wcalc"){const moon=(S.track==="c"||S.track==="d")&&r()<.5;return{t:"wcalc",m:moon?pick(r,[5,10,15]):ri(r,2,9),where:moon?"moon":"earth",obj:"rice"};}
   if(tp==="mcalc")return{t:"mcalc",W:ri(r,2,9)*10,obj:"rice"};
   if(tp==="water")return{t:"water",obj:pick(r,["stone","brick","iron"]),ans:2};
   if(tp==="waterF")return{t:"waterF",obj:pick(r,["stone","brick","iron"])};
   const u=d<2?"cube":d<3.5?"kg":"g",ids=Object.keys(MASS[u]).filter(k=>k!=="cotton"&&k!=="iron");
   if(tp==="heavier"){const vis=ids.filter(k=>!k.startsWith("my"));const a=pick(r,vis);let b=pick(r,vis);return{t:"heavier",u,L:[a],R:[b]};}
   const n=d>4?2:1,obj=shuffle(r,ids).slice(0,n);return{t:tp,u,obj,tray:u==="cube"?[1]:u==="kg"?[1,2,5,10]:[100,200,500,1000]};},
 mount(sp,A){
  if(["moon","wcalc","mcalc","massq","moonbal","bath","water","waterF","waterWhy"].includes(sp.t))return massWeight(sp,A);
  const u=sp.u;
  if(sp.t==="heavier"){const mL=sp.L.reduce((s,id)=>s+MASS[u][id],0),mR=sp.R.reduce((s,id)=>s+MASS[u][id],0),ans=mR>mL?0:mR===mL?1:2;
    const names=a=>andList(a.map(id=>OB[id].n));
    A.prompt(KID()?`پایه‌ها را برمی‌داریم. کدام کفه پایین می‌رود؟`:`روی کفهٔ چپ ${names(sp.L)} و روی کفهٔ راست ${names(sp.R)} است. وقتی پایه‌ها را برداریم، چه می‌شود؟<small>اول پیش‌بینی کن؛ بعد ترازو آزاد می‌شود.</small>`);
    const b=makeBalance(A,{unit:u,L:sp.L.map(id=>({k:"o",id,fixed:1})),R:sp.R.map(id=>({k:"o",id,fixed:1})),locked:true,hideL:true,hideR:true});A.refresh=()=>b.render();
    const reveal=()=>{b.st.hideL=b.st.hideR=false;b.setLock(false);};
    const cotton=sp.L.includes("cotton")||sp.R.includes("cotton"),big=sp.L.includes("balloon")||sp.L.includes("pillow")||sp.R.includes("balloon")||sp.R.includes("pillow");
    const expl=ans===1?`هر دو کفه ${fmtM(mL,u)} است.${cotton?" این پنبه و این آهن هم‌جرم‌اند؛ پنبه فقط جای بیشتری می‌گیرد.":""}`:`کفهٔ ${ans===0?"راست":"چپ"} جرم بیشتری دارد: ${fmtM(Math.max(mL,mR),u)} در برابر ${fmtM(Math.min(mL,mR),u)}.${big?" بزرگ‌تر بودن یعنی سنگین‌تر بودن نیست!":""}`;
    const kexp=ans===1?(cotton?"دو طرف هم‌جرم‌اند. پنبه فقط جای بیشتری می‌گیرد.":"دو طرف هم‌جرم‌اند؛ ترازو صاف ماند."):`کفهٔ ${ans===0?"راست":"چپ"} سنگین‌تر است.${big?" بزرگ‌تر همیشه سنگین‌تر نیست!":""}`;
    const c=A.ctrl("");const m=mcq(c,["کفهٔ راست پایین می‌رود","صاف می‌ماند","کفهٔ چپ پایین می‌رود"],(i,bt)=>{if(A.locked)return;
      if(i===ans){m.disable();m.mark(i,"right");reveal();A.judge(true,{ok:expl,k:{ok:kexp}});}
      else{m.mark(i,"wrong");bt.disabled=true;A.judge(false,{retry:"به جنس چیزها فکر کن، نه فقط به اندازه‌شان.",final:expl,k:{retry:"به جنس چیزها فکر کن، نه فقط به اندازه.",final:kexp}});if(A.locked){m.disable();m.mark(ans,"right");reveal();}}});
    return;}
  const target=sp.obj.reduce((s,id)=>s+MASS[u][id],0),objNames=andList(sp.obj.map(id=>OB[id].n));
  /* ترازوی زنده: پایه ندارد؛ هر وزنه که روی کفه برود، شاهین همان لحظه کج یا صاف می‌شود. صاف ماند = تمام (برای «جرم نامعلوم»: بعد جرم را می‌پرسد) */
  const minN=minCoins(target,sp.tray),unitW=u==="cube"?"مکعب":"وزنه";let asked=false,stp=null,chk=null;
  const c=A.ctrl("");
  const onSettle=()=>{if(A.locked||asked)return;const mR=b.mass("R"),n=b.st.R.length,eq=mR===target;
    if(!n){A.fb("");return;}
    if(!eq){A.fb(KID()?(mR>target?"کفهٔ مکعب‌ها پایین رفت. یک مکعب بردار.":"کفهٔ چپ هنوز پایین است. مکعب اضافه کن."):(mR>target?`کفهٔ راست پایین رفت؛ ${unitW}ها زیاد است. روی یکی بزن تا برداشته شود.`:`کفهٔ چپ هنوز پایین است؛ ${unitW} اضافه کن.`),"info");return;}
    if(sp.t==="fewest"&&n!==minN){A.trial(false,{retry:`صاف شد، ولی با ${fa(n)} وزنه. با وزنه‌های بزرگ‌تر می‌شود با وزنه‌های کمتری صافش کرد.`});return;}
    if(sp.t==="mystery"){asked=true;b.st.edit="";b.render();A.fb("ترازو صاف شد! حالا جرم وزنه‌های کفهٔ راست را جمع بزن.","info");
      A.prompt(`ترازو صاف است. پس جرم ${objNames} چقدر است؟<small>جرم ${objNames} با جرم وزنه‌های کفهٔ راست برابر است. آن‌ها را جمع بزن.</small>`);
      stp=stepper(c,{init:0,max:u==="g"?9000:99,steps:u==="g"?[100,1000]:[1,10],unit:u==="kg"?"کیلوگرم":"گرم",label:"جرم"});
      chk=btn(c,"بررسی","go",()=>{const ok=stp.get()===target;
        A.trial(ok,{ok:`جرم ${objNames} ${fmtM(target,u)} است: ${b.st.R.map(it=>fa(it.v)).join(" + ")} = ${fa(target)}.`,retry:`جرم وزنه‌های کفهٔ راست را یکی‌یکی جمع بزن: ${b.st.R.map(it=>fa(it.v)).join(" + ")}.`});
        if(A.locked){chk.disabled=true;stp.disable();b.st.hideL=b.st.hideR=false;b.render();}});return;}
    b.st.hideL=false;A.trial(true,{ok:sp.t==="balance"?(u==="cube"?`${objNames} هم‌جرمِ ${fa(target)} مکعب است.`:`جرم ${objNames} ${fmtM(target,u)} است.`):`با ${fa(n)} وزنه صاف شد؛ کمتر از این نمی‌شد.`,k:{ok:`ترازو صاف شد! ${fa(target)} مکعب.`}});b.render();};
  const b=makeBalance(A,{unit:u,L:sp.obj.map(id=>({k:"o",id,fixed:1})),edit:"R",tray:sp.tray,locked:false,hideL:true,hideR:sp.t==="mystery",onSettle});A.refresh=()=>b.render();
  A.prompt(KID()?"مکعب‌ها را روی کفهٔ راست بگذار تا ترازو صاف شود.":sp.t==="fewest"?`ترازو را با <b>کمترین تعداد وزنه</b> صاف کن.<small>وزنه‌ها را روی کفهٔ راست بکش؛ ترازو همان لحظه نشان می‌دهد کدام طرف سنگین‌تر است. با وزنه‌های بزرگ‌تر شروع کن. برای برداشتن وزنه، رویش بزن.</small>`
    :`${sp.t==="mystery"?`جرم ${objNames} چقدر است؟ اول ترازو را صاف کن.`:`ترازو را صاف کن. جرم ${objNames} را نمی‌دانی.`}<small>${u==="cube"?"مکعب‌ها":"وزنه‌ها"} را روی کفهٔ راست بکش؛ ترازو همان لحظه نشان می‌دهد کدام طرف سنگین‌تر است. برای برداشتن، رویش بزن.</small>`);
  A.hint(`M${320+(0-(sp.tray.length-1)/2)*Math.min(90,560/sp.tray.length)} 478 L516 215`);
 }};
function minCoins(t,vals){const dp=Array(t+1).fill(Infinity);dp[0]=0;const g=vals.reduce((a,b)=>gcd(a,b));for(let s=g;s<=t;s+=g)for(const v of vals)if(v<=s&&dp[s-v]+1<dp[s])dp[s]=dp[s-v]+1;return dp[t];}
function gcd(a,b){return b?gcd(b,a%b):a;}
function minCoinsStr(t,vals,u){const out=[];let s=t;const vs=vals.slice().sort((a,b)=>b-a);
  while(s>0){let best=null;for(const v of vs)if(v<=s&&minCoins(s-v,vals)+1===minCoins(s,vals)){best=v;break;}if(best==null)break;out.push(best);s-=best;}
  return out.map(v=>wLabelLong(v,u)).join(" + ");}

const FX_W=(sub)=>FX(`${sy("W")} = ${sy("m")} × ${sy("g")}`,sub||"",[[sy("W"),"وزن (N)"],[sy("m"),"جرم (kg)"],[sy("g"),"وزنِ هر کیلوگرم (نیوتن بر کیلوگرم)؛ زمین ≈ ۱۰ و ماه ≈ ۱٫۶"]]);
const FX_B=(sub)=>FX(`${sy("W","آب")} = ${sy("W")} − ${sy("F","b")}`,sub||"",[[sy("W"),"وزن جسم (N)"],[sy("F","b"),"نیروی شناوری: نیروی رو به بالای آب (N)"],[sy("W","آب"),"عدد نیروسنج در آب (وزن ظاهری)"]]);
function mwMcq(A,opts,ans,msg){const c=A.ctrl("");const m=mcq(c,opts,(i,bt)=>{if(A.locked)return;if(msg.gate&&!msg.gate())return;
    if(i===ans){m.disable();m.mark(i,"right");if(msg.reveal)msg.reveal();A.judge(true,{ok:msg.ok,k:msg.k?{ok:msg.k.ok}:undefined});}
    else{m.mark(i,"wrong");bt.disabled=true;A.judge(false,{retry:msg.retry,final:msg.ok,k:msg.k?{retry:msg.k.retry,final:msg.k.ok}:undefined});if(A.locked){m.disable();m.mark(ans,"right");if(msg.reveal)msg.reveal();}}});return m;}
function massWeight(sp,A){const P=A.P,K=KID();A.counter("");
  if(sp.t==="moon"){A.view(404);const draw=rev=>P.paint(`<rect width="640" height="520" style="fill:var(--sw)"/>`+springPanel(16,296,"earth",5,50,K?"کیسهٔ برنج":"کیسهٔ ۵ کیلوگرمی")+springPanel(328,296,"moon",5,rev?8:null,"همان کیسه"));draw(false);
    A.formula(FX_W(`${sy("W")} = ۵ × ۱۰ = ۵۰ N`));
    A.prompt(K?"همین کیسه را به ماه بردیم و به نیروسنج آویزان کردیم. فنر چه می‌شود؟":"همین کیسه را به ماه بردیم. نیروسنج روی ماه چه عددی نشان می‌دهد؟<small>نیروسنج وزن را اندازه می‌گیرد، و وزن یک نیروست.</small>");
    mwMcq(A,K?["بیشتر کشیده می‌شود","همان‌قدر کشیده می‌شود","کمتر کشیده می‌شود"]:["بیشتر از ۵۰ نیوتن","همان ۵۰ نیوتن","کمتر از ۵۰ نیوتن"],2,{reveal:()=>draw(true),
      ok:"ماه چیزها را خیلی کمتر از زمین به طرف خودش می‌کشد: حدود یک‌ششمِ زمین. پس وزن کیسه روی ماه ۸ نیوتن است: ۵ × ۱٫۶ = ۸. جرم کیسه همان ۵ کیلوگرم می‌ماند.",retry:"ماه از زمین خیلی کوچک‌تر است. آیا چیزها را به همان اندازه می‌کشد؟",
      k:{ok:"ماه کیسه را کمتر از زمین به طرف خودش می‌کشد؛ پس فنر کمتر کشیده می‌شود. برنجِ کیسه همان است.",retry:"ماه از زمین خیلی کوچک‌تر است."}});return;}
  if(sp.t==="massq"){A.view(404);P.paint((sp.water?bgRoom(382):moonBg(382))+placeTag(sp.water?"earth":"moon",540,70)+(sp.water?`<rect x="206" y="228" width="228" height="156" rx="12" fill="#fff" fill-opacity=".45" stroke="#7FA7C4" stroke-width="4"/><rect x="210" y="262" width="220" height="118" rx="8" fill="#6EC3EA" fill-opacity=".6"/><g transform="translate(320 360) scale(1.7)">${OB.stone.d}</g>`:`<g transform="translate(320 382) scale(1.6)">${OB.rice.d}</g>`));
    A.formula(sp.water?FX_B(""):FX_W(""));
    if(sp.water){A.prompt(K?"سنگ را در آب گذاشتیم. مقدار سنگ کم می‌شود؟":"سنگ ۵ کیلوگرمی زیر آب است و نیروسنج عدد کمتری نشان می‌دهد. جرم سنگ در آب چقدر است؟");
      mwMcq(A,K?["کم می‌شود","همان است","زیاد می‌شود"]:["کمتر از ۵ کیلوگرم","همان ۵ کیلوگرم","بیشتر از ۵ کیلوگرم"],1,{ok:"جرم یعنی مقدار ماده. هیچ تکه‌ای از سنگ کم نشده؛ پس جرمش همان ۵ کیلوگرم است. وزنش هم عوض نشده؛ فقط آب آن را به بالا هل می‌دهد و عدد نیروسنج کم می‌شود.",retry:"آیا تکه‌ای از سنگ در آب حل شد یا کنده شد؟",k:{ok:"هیچ تکه‌ای از سنگ کم نشده؛ پس مقدارش همان است.",retry:"آیا تکه‌ای از سنگ کم شد؟"}});return;}
    A.prompt(K?"کیسهٔ برنج را از زمین به ماه بردیم. مقدار برنجِ توی کیسه چه می‌شود؟":"جرم این کیسه روی زمین ۵ کیلوگرم است. آن را به ماه بردیم. روی ماه جرمش چقدر است؟");
    mwMcq(A,K?["کمتر می‌شود","همان است","بیشتر می‌شود"]:["حدود ۱ کیلوگرم","۵ کیلوگرم","صفر"],1,{ok:"جرم یعنی مقدار ماده. هیچ برنجی کم یا زیاد نشده؛ پس جرم همان ۵ کیلوگرم است. آنچه روی ماه کم می‌شود وزن است، یعنی نیرویی که ماه کیسه را با آن می‌کشد.",retry:"جرم یعنی مقدار ماده. آیا در سفر، برنجی از کیسه بیرون ریخت؟",k:{ok:"هیچ برنجی کم یا زیاد نشده؛ پس مقدارش همان است. فقط ماه آن را کمتر می‌کشد.",retry:"آیا در سفر، برنجی از کیسه بیرون ریخت؟"}});return;}
  if(sp.t==="moonbal"){const u=K?"cube":"kg";const b=makeBalance(A,{unit:u,L:[{k:"o",id:"rice",fixed:1}],R:u==="cube"?Array.from({length:MASS.cube.rice},()=>({k:"w",v:1,fixed:1})):[{k:"w",v:5,fixed:1}],locked:true,bg:"moon"});A.refresh=()=>b.render();
    A.prompt(K?"این ترازو روی زمین صاف بود. آن را به ماه بردیم. پایه‌ها را برداریم، چه می‌شود؟":"روی زمین، کیسهٔ برنج با وزنهٔ ۵ کیلوگرمی روی ترازوی دوکفه‌ای صاف بود. همین ترازو را به ماه بردیم. وقتی پایه‌ها را برداریم، چه می‌شود؟");
    mwMcq(A,["کفهٔ کیسه پایین می‌رود","ترازو صاف می‌ماند","کفهٔ وزنه پایین می‌رود"],1,{reveal:()=>b.setLock(false),ok:"روی ماه هم کیسه و هم وزنه کمتر کشیده می‌شوند، هر دو به یک نسبت. پس ترازو باز هم صاف می‌ماند. ترازوی دوکفه‌ای جرم را مقایسه می‌کند و جرم روی ماه عوض نمی‌شود.",retry:"ماه هر دو کفه را کمتر می‌کشد. کدام بیشتر کم می‌شود؟",k:{ok:"ماه هر دو کفه را به یک اندازه کمتر می‌کشد؛ پس ترازو صاف می‌ماند.",retry:"ماه هر دو کفه را کمتر می‌کشد."}});return;}
  if(sp.t==="bath"){A.view(404);P.paint(bathScene());A.formula(FX_W(""));
    A.prompt("ترازوی حمام در اصل نیرو را می‌سنجد و آن را به «کیلوگرمِ زمینی» نشان می‌دهد. بچه‌ای که روی زمین ۳۰ کیلوگرم نشان می‌دهد، با همین ترازو روی ماه می‌رود. ترازو چه عددی نشان می‌دهد؟");
    mwMcq(A,["حدود ۵ کیلوگرم","۳۰ کیلوگرم","بیشتر از ۳۰ کیلوگرم"],0,{ok:"ترازوی حمام وزن را می‌سنجد و روی ماه وزن حدود یک‌ششم است؛ پس حدود ۵ نشان می‌دهد: ۳۰ × ۱٫۶ ÷ ۱۰ ≈ ۵. ولی جرم این بچه همان ۳۰ کیلوگرم است. برای سنجیدن جرم روی ماه باید ترازوی دوکفه‌ای برد.",retry:"این ترازو نیرو را می‌سنجد، نه جرم را. روی ماه نیرو چه می‌شود؟"});return;}
  const o=SPR[sp.obj]||{m:sp.m},m=sp.m||o.m;
  if(sp.t==="wcalc"){const moon=sp.where==="moon",ans=r1(m*GV[sp.where]);
    const s=makeSpring(A,{obj:sp.obj||"rice",sc:1.2,m,place:sp.where,hide:true});A.refresh=()=>s.render();A.formula(FX_W(""));
    A.prompt(`جرم این کیسه ${fa(m)} کیلوگرم است. نیروسنج ${moon?"<b>روی ماه</b>":"روی زمین"} چند نیوتن نشان می‌دهد؟`);
    const c=A.ctrl("");const stp=stepper(c,{init:0,max:200,steps:[1,10],unit:"نیوتن"});
    const chk=btn(c,"بررسی","go",()=>{const v=stp.get(),ok=Math.abs(v-ans)<1e-6;
      A.judge(ok,{ok:`وزن = ${fa(m)} × ${moon?"۱٫۶":"۱۰"} = ${fa(ans)} نیوتن.${moon?` جرم همان ${fa(m)} کیلوگرم است؛ فقط وزن کم شد.`:""}`,retry:moon?"روی ماه، جرم را در ۱٫۶ ضرب کن.":"جرم را در ۱۰ ضرب کن.",final:`${fa(m)} × ${moon?"۱٫۶":"۱۰"} = ${fa(ans)} نیوتن.`});
      if(A.locked){chk.disabled=true;stp.disable();s.st.hide=false;s.render();}});return;}
  if(sp.t==="mcalc"){const mm=sp.W/10,s=makeSpring(A,{obj:sp.obj,sc:sp.obj==="rice"?1.2:undefined,m:mm,place:"earth",hideM:true});A.refresh=()=>s.render();A.formula(FX_W(""));
    A.prompt(`نیروسنج روی زمین ${fa(sp.W)} نیوتن نشان می‌دهد. جرم ${OB[sp.obj].n} چند کیلوگرم است؟`);
    const c=A.ctrl("");const stp=stepper(c,{init:0,max:99,steps:[1,10],unit:"کیلوگرم"});
    const chk=btn(c,"بررسی","go",()=>{const ok=stp.get()===mm;
      A.judge(ok,{ok:`${fa(sp.W)} ÷ ۱۰ = ${fa(mm)} کیلوگرم. روی زمین هر کیلوگرم حدود ۱۰ نیوتن وزن دارد.`,retry:"وزن را بر ۱۰ تقسیم کن.",final:`جرم = وزن ÷ ۱۰ = ${fa(sp.W)} ÷ ۱۰ = ${fa(mm)} کیلوگرم.`});
      if(A.locked){chk.disabled=true;stp.disable();}});return;}
  /* آب */
  let dunked=false;const s=makeSpring(A,{obj:sp.obj,m:o.m,Fb:o.Fb,place:"earth",water:true,lower:true,onDrop:f=>{if(f>.98&&!dunked){dunked=true;A.fb(K?"حالا به فنر نگاه کن.":`در هوا ${fa(o.m*10)} نیوتن بود؛ حالا ${fa(o.m*10-o.Fb)} نیوتن است.`,"info");}}});A.refresh=()=>s.render();
  A.hint(`M320 40 L320 150`);
  const gate=()=>{if(s.sub()<.98){A.fb(K?`اول ${OB[sp.obj].n} را با دستگیرهٔ زرد تا ته در آب ببر.`:`اول ${OB[sp.obj].n} را کامل در آب ببر (دستگیرهٔ زرد را پایین بکش).`,"info");return false;}return true;};
  A.formula(FX_B(""));
  const wOk=`آب ${OB[sp.obj].n} را به بالا هل می‌دهد؛ به این نیرو «نیروی شناوری» می‌گویند. وزن جسم عوض نشده، ولی نیروسنج عدد کمتری نشان می‌دهد. به این عدد «وزن ظاهری» می‌گویند.`;
  if(sp.t==="water"){A.prompt(K?`${OB[sp.obj].n} را آرام در آب ببر. فنر نیروسنج چه می‌شود؟`:`${OB[sp.obj].n} را با دستگیرهٔ زرد آرام در آب ببر. عدد نیروسنج چه می‌شود؟`);
    mwMcq(A,K?["بیشتر کشیده می‌شود","همان می‌ماند","کمتر کشیده می‌شود"]:["بیشتر می‌شود","همان می‌ماند","کمتر می‌شود"],2,{gate,ok:wOk,retry:"دوباره به عقربهٔ نارنجی نگاه کن. خط‌چین جای قبلی آن است.",k:{ok:`آب ${OB[sp.obj].n} را کمی به بالا هل می‌دهد؛ برای همین فنر کمتر کشیده می‌شود. ${OB[sp.obj].n} کوچک‌تر نشده است.`,retry:"به عقربهٔ نارنجی نگاه کن. خط‌چین جای قبلی آن است."}});return;}
  if(sp.t==="waterWhy"){A.prompt(`${OB[sp.obj].n} را در آب ببر. چرا عدد نیروسنج کم می‌شود؟`);
    mwMcq(A,["چون وزن آهن کم می‌شود","چون آب آن را به بالا هل می‌دهد","چون جرم آهن کم می‌شود"],1,{gate,ok:wOk+" جرم و وزن واقعی آهن همان است.",retry:"وقتی در استخر هستی، آب تو را به کدام طرف هل می‌دهد؟"});return;}
  A.prompt(`${OB[sp.obj].n} را کامل در آب ببر. آب با چند نیوتن آن را به بالا هل می‌دهد؟<small>عدد نیروسنج در هوا را با عددش در آب مقایسه کن.</small>`);
  const c=A.ctrl("");const stp=stepper(c,{init:0,max:100,steps:[1,10],unit:"نیوتن"});
  const chk=btn(c,"بررسی","go",()=>{if(!gate())return;const ok=stp.get()===o.Fb;
    A.judge(ok,{ok:`نیروی شناوری = ${fa(o.m*10)} − ${fa(o.m*10-o.Fb)} = ${fa(o.Fb)} نیوتن.`,retry:"عدد نیروسنج در آب را از عددش در هوا کم کن.",final:`در هوا ${fa(o.m*10)} و در آب ${fa(o.m*10-o.Fb)} نیوتن؛ پس نیروی شناوری ${fa(o.Fb)} نیوتن است.`});
    if(A.locked){chk.disabled=true;stp.disable();}});
}
