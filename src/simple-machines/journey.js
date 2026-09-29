/* ================= نقشهٔ سفر: ۱۲ منزل، به ترتیب جلسه‌های کلاس ================= */
const GRADES=["دوم","سوم","چهارم","پنجم","ششم"];
const trackOfG=g=>g<=1?"a":g===2?"b":"c";
const LANDS=[{n:"سرزمین نیرو",bg:"#FFF1E3",hex:"#E8590C",from:0,to:3},{n:"سرزمین ماشین‌ها",bg:"#E6F4EA",hex:"#22965A",from:4,to:9},{n:"کارگاه مهندسی",bg:"#EFE8FB",hex:"#7A3FC8",from:10,to:11}];
const landOf=i=>i<4?0:i<10?1:2;
/* هر منزل: اسم، ایستگاه مأموریت جانبی، مأموریت‌های اصلی هر مسیر [ایستگاه، شمارهٔ مرحله] */
const STOPS=[
 {n:"نیرو",side:"force",m:{a:[["force",1]],b:[["force",1]],c:[["force",1],["force",2]]}},
 {n:"جرم و وزن",side:"scale",m:{a:[["scale",1],["scale",2]],b:[["scale",1],["scale",2]],c:[["scale",1],["scale",2]]}},
 {n:"نیروسنج",side:"scale",m:{a:[["scale",3],["scale",4]],b:[["scale",3],["scale",4]],c:[["scale",3],["scale",4]]}},
 {n:"اصطکاک",side:"force",m:{a:[["force",2],["force",3]],b:[["force",2],["force",3]],c:[["force",3],["force",4]]}},
 {n:"اهرم ۱",side:"lever",m:{a:[["lever",1]],b:[["lever",1]],c:[["lever",1]]}},
 {n:"اهرم ۲",side:"lever",m:{a:[["lever",2],["lever",3]],b:[["lever",2],["lever",3]],c:[["lever",2],["lever",3],["lever",4]]}},
 {n:"سطح شیب‌دار",side:"ramp",m:{a:[["ramp",1],["ramp",2]],b:[["ramp",1],["ramp",2],["ramp",3]],c:[["ramp",1],["ramp",2],["ramp",3]]}},
 {n:"گوه و پیچ",side:"wedge",m:{a:[["wedge",1],["wedge",2]],b:[["wedge",1],["wedge",2],["wedge",3]],c:[["wedge",1],["wedge",2],["wedge",3]]}},
 {n:"چرخ و محور",side:"wheel",m:{a:[["wheel",1],["wheel",2]],b:[["wheel",1],["wheel",2],["wheel",3]],c:[["wheel",1],["wheel",2],["wheel",3]]}},
 {n:"قرقره",side:"pulley",m:{a:[["pulley",1],["pulley",2]],b:[["pulley",1],["pulley",2],["pulley",3]],c:[["pulley",1],["pulley",2],["pulley",3]]}},
 {n:"چالش مهندسی",side:"sort",m:{a:[["sort",1],["sort",2]],b:[["sort",1],["sort",2]],c:[["sort",1],["sort",2]]}},
 {n:"نمایشگاه",side:"sort",m:{a:[["sort",3]],b:[["sort",3],["sort",4]],c:[["sort",3],["sort",4]]}}];
/* کار خانه: همان تمرین خانهٔ برنامهٔ ترم؛ والدین می‌خوانند */
const HOME=["شکار نیرو: پنج هل و پنج کشش در خانه پیدا کند و نقاشی کند.","با چوب‌لباسی و دو کیسه ترازو بسازد و پنج میوه را از سبک به سنگین بچیند.","با کش مو یک کش‌سنج بسازد؛ یک کفش و یک جامدادی را بکشد و ببیند کدام کش را بیشتر باز کرد.","یک اسباب‌بازی را روی سرامیک، فرش و پتو بکشد و بگوید کدام سخت‌تر بود.","با خط‌کش و مداد اهرمی بسازد که یک پاک‌کن و یک تراش را صاف نگه دارد.","پنج اهرم در خانه پیدا کند و تکیه‌گاه هر کدام را با نقطهٔ قرمز نشان دهد.","با کتاب و یک تخته سطح شیب‌دار بسازد و یک ماشین اسباب‌بازی را از دو شیب رها کند.","مثلث کاغذی را دور مداد بپیچد و ترفندش را به خانواده نشان دهد.","دستگیرهٔ در را یک بار از خود دستگیره و یک بار از نزدیک میلهٔ وسط بچرخاند.","با کمک شما، با دستهٔ جارو و نخ یک کیسهٔ سبک را بالا ببرد.","با خانواده یک ماشین مرکب در خانه پیدا کند و ماشین‌های ساده‌اش را روی نقاشی نشان دهد.","در یک دقیقه برای خانواده توضیح دهد ماشین گروهشان چطور کار می‌کند."];
/* «امروز یاد گرفتی»: کوتاه برای دوم و سوم، کامل‌تر برای بقیه */
const LEARN=[
 ["طرفی که قوی‌تر می‌کشد، می‌برد.","نیرو یعنی هل دادن یا کشیدن. وقتی دو طرف می‌کشند، طرفی که نیروی بیشتری دارد می‌برد."],
 ["ترازو نشان می‌دهد کدام سنگین‌تر است.","جرم مقدار ماده است. ترازوی دوکفه‌ای جرم دو چیز را با هم مقایسه می‌کند."],
 ["روی ماه و در آب، فنر کمتر کشیده می‌شود.","نیروسنج وزن را می‌سنجد. روی ماه وزن کم می‌شود، ولی جرم نه. در آب، آب جسم را بالا هل می‌دهد."],
 ["روی فرش سُر خوردن سخت‌تر است.","اصطکاک با سُر خوردن مخالفت می‌کند. سطح زبرتر اصطکاک بیشتری دارد."],
 ["سنگین‌تر نزدیک وسط بنشیند.","در الاکلنگ، سنگین‌تر نزدیک‌تر به تکیه‌گاه و سبک‌تر دورتر می‌نشیند."],
 ["تکیه‌گاه نزدیک سنگ، نیروی کمتر.","تکیه‌گاه نزدیک بار یعنی نیروی کمتر، ولی دست راه بیشتری می‌رود."],
 ["راه درازتر، نیروی کمتر.","سطح طولانی‌تر و ملایم‌تر نیروی کمتری می‌خواهد، ولی راه بیشتر است."],
 ["گوه تیز است و چوب را باز می‌کند.","گوه دو سطح شیب‌دار پشت به پشت است. پیچ سطح شیب‌داری است که دور میله پیچیده شده."],
 ["دستهٔ بلندتر، چرخاندن راحت‌تر.","دستهٔ بلندتر یعنی نیروی کمتر، ولی دست دایرهٔ بزرگ‌تری می‌گردد."],
 ["با قرقره، طناب را پایین می‌کشیم و بار بالا می‌رود.","قرقرهٔ ثابت جهت کشیدن را عوض می‌کند. طناب‌های نگه‌دارندهٔ بیشتر یعنی نیروی کمتر."],
 ["بعضی وسیله‌ها از چند ماشین ساده ساخته شده‌اند.","ماشین مرکب از چند ماشین سادهٔ به هم وصل ساخته شده است."],
 ["شش ماشین ساده را می‌شناسی!","ماشین ساده نیرو را کم می‌کند یا جهتش را عوض می‌کند، ولی کار را کم نمی‌کند."]];
const WORDS={a:[["نیرو"],["جرم","وزن"],["نیروسنج","نیروی شناوری"],["اصطکاک"],["اهرم","تکیه‌گاه"],[],["سطح شیب‌دار"],["گوه","پیچ"],["چرخ و محور"],["قرقرهٔ ثابت"],["ماشین مرکب"],[]],
 b:[["نیرو","نیروی خالص"],["جرم","وزن"],["نیروسنج","نیروی شناوری"],["اصطکاک"],["اهرم","تکیه‌گاه"],["نیروی محرک","نیروی مقاوم"],["سطح شیب‌دار"],["گوه","پیچ"],["چرخ و محور"],["قرقرهٔ ثابت"],["ماشین مرکب"],[]],
 c:[["نیرو","نیروی خالص"],["جرم","وزن"],["نیروسنج","نیروی شناوری"],["اصطکاک","کار"],["اهرم","تکیه‌گاه"],["نیروی محرک","نیروی مقاوم"],["سطح شیب‌دار"],["گوه","پیچ"],["چرخ و محور"],["قرقرهٔ ثابت"],["ماشین مرکب"],["مزیت مکانیکی"]]};
/* تعریف‌ها: [برای دوم و سوم، برای چهارم تا ششم] */
const JDEF={"نیرو":["هل دادن یا کشیدن.","هل دادن یا کشیدن. یکای نیرو نیوتن است."],"نیروی خالص":["","اثر همهٔ نیروهایی که با هم به یک چیز وارد می‌شوند. نیروهای مخالف از هم کم می‌شوند."],
 "جرم":["مقدار چیزی که یک جسم از آن ساخته شده. روی ماه هم همان است.","مقدار ماده‌ای که یک چیز دارد. با ترازوی دوکفه‌ای سنجیده می‌شود و روی ماه هم عوض نمی‌شود."],
 "وزن":["زمین هر چیزی را به طرف خودش می‌کشد. به این کشش وزن می‌گوییم.","نیرویی که زمین با آن چیزها را به طرف خودش می‌کشد. با نیروسنج سنجیده می‌شود و یکایش نیوتن است."],
 "نیروسنج":["وسیله‌ای با فنر. هرچه چیزی سنگین‌تر باشد، فنر بیشتر کش می‌آید.","وسیله‌ای با فنر که نیرو، مثلاً وزن، را به نیوتن نشان می‌دهد."],
 "نیروی شناوری":["آب چیزها را کمی به بالا هل می‌دهد.","نیروی رو به بالایی که آب به جسمِ درون خودش وارد می‌کند. برای همین نیروسنج در آب عدد کمتری نشان می‌دهد."],
 "اصطکاک":["نیرویی که جلوی سُر خوردن را می‌گیرد.","نیرویی بین دو سطحِ روی هم که با سُر خوردن آن‌ها مخالفت می‌کند. سطح زبرتر اصطکاک بیشتری دارد."],
 "کار":["","وقتی نیرویی چیزی را در جهت خودش جابه‌جا کند، کار انجام شده است."],
 "اهرم":["میله یا تخته‌ای که دور یک نقطه بالا و پایین می‌رود.","میله یا تخته‌ای که دور یک نقطهٔ ثابت می‌چرخد."],
 "تکیه‌گاه":["نقطه‌ای که اهرم رویش می‌چرخد.","نقطه‌ای که اهرم دور آن می‌چرخد."],
 "نیروی محرک":["","نیرویی که ما به ماشین وارد می‌کنیم."],"نیروی مقاوم":["","نیرویی که بار به ماشین وارد می‌کند؛ مثلاً وزن سنگی که بلند می‌کنیم."],
 "سطح شیب‌دار":["سطحی کج که بالا بردن چیزها را راحت‌تر می‌کند.","سطحی کج که جای پایین را به جای بالا وصل می‌کند. سطح طولانی‌تر نیروی کمتری می‌خواهد."],
 "گوه":["لبهٔ تیزی که چیزها را از هم باز می‌کند.","دو سطح شیب‌دار پشت به پشت که چیزها را به دو طرف باز می‌کند."],
 "پیچ":["میله‌ای که دورش شیار دارد و با چرخاندن فرو می‌رود.","سطح شیب‌داری که دور یک میله پیچیده شده. فاصلهٔ دو شیار را گام پیچ می‌گویند."],
 "چرخ و محور":["چرخ بزرگی که یک میلهٔ باریک را می‌چرخاند.","چرخ یا دسته‌ای بزرگ که به میله‌ای باریک وصل است و با هم می‌چرخند."],
 "قرقرهٔ ثابت":["چرخی بالای سر که طناب از رویش رد می‌شود.","چرخی که به سقف وصل است و جهت کشیدن طناب را عوض می‌کند."],
 "ماشین مرکب":["ماشینی که از چند ماشین ساده ساخته شده.","ماشینی که از دو یا چند ماشین ساده ساخته شده؛ مثل دوچرخه یا ناخن‌گیر."],
 "مزیت مکانیکی":["","نشان می‌دهد ماشین نیروی ما را چند برابر کرده است."]};
const SIDEG={a:[3,3,4],b:[4,5,6],c:[5,6,8]};
const TRAV=[{n:"ربات",c:"#3B6FD4"},{n:"موشک",c:"#E8590C"},{n:"ماشین",c:"#22965A"},{n:"بالن",c:"#C2417A"}];
const WL=()=>KID()?{main:"بازی",side:"جایزه"}:{main:"مأموریت اصلی",side:"مأموریت جانبی"};

/* ---------- وضعیت بازیکن ---------- */
const JP=()=>curP();
const trk=p=>trackOfG(p.g);
const missions=(p,i)=>STOPS[i].m[trk(p)];
const mStars=(p,i,j)=>{const [k,L]=missions(p,i)[j];const key=trk(p)+":"+k;const pg=p.S.prog[key];return pg?pg.lv[L-1]||0:0;};
const stopDone=(p,i)=>missions(p,i).every((_,j)=>mStars(p,i,j)>0);
const curStop=p=>{for(let i=0;i<12;i++)if(!stopDone(p,i))return i;return 12;};
const minStars=(p,i)=>Math.min(...missions(p,i).map((_,j)=>mStars(p,i,j)));
const totStars=p=>{let t=0;for(let i=0;i<12;i++)missions(p,i).forEach((_,j)=>t+=mStars(p,i,j));return t;};
const firstOpen=(p,i)=>{const ms=missions(p,i);for(let j=0;j<ms.length;j++)if(!mStars(p,i,j))return j;return 0;};
const mName=(p,i,j)=>{const [k,L]=missions(p,i)[j];return levelsOf(k)[L-1].title;};
function newProfile(name,g,t){return{id:"p"+Date.now().toString(36),name,g,t,S:{prog:{},nums:true,forces:true,formula:true,track:trackOfG(g)},home:Array(12).fill(0),side:Array(12).fill(0),words:Array(12).fill(0),at:null,coach:1};}

/* ---------- کد پیشرفت (داخل پیام معلم؛ همهٔ ستاره‌ها را نگه می‌دارد) ---------- */
const ABC="بپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی",B31=31n,CMASK=0x5A3F9C1E07B4D268A3C5F1n,CLEN=23;
function makeCode(p){let v=0n;const add=(x,b)=>{v=(v<<BigInt(b))|BigInt(x);};add(p.g,3);add(p.t,2);
  for(let i=0;i<12;i++)for(let j=0;j<3;j++)add(j<missions(p,i).length?mStars(p,i,j):0,2);
  for(let i=0;i<12;i++)add(p.home[i]?1:0,1);for(let i=0;i<12;i++)add(p.side[i]?1:0,1);
  add(Number(v%2039n),11);v^=CMASK;const out=[];for(let k=0;k<CLEN;k++){out.unshift(ABC[Number(v%B31)]);v/=B31;}return out.map((c,x)=>c+(x===CLEN-1?"":(x%4===3?" ":"\u200c"))).join("");}
function readCode(str){const s=(str||"").replace(/[\s\-‌]/g,"").replace(/ي/g,"ی").replace(/ك/g,"ک");if(s.length!==CLEN)return null;let v=0n;for(const ch of s){const k=ABC.indexOf(ch);if(k<0)return null;v=v*B31+BigInt(k);}v^=CMASK;
  const ck=Number(v&2047n);v>>=11n;if(Number(v%2039n)!==ck)return null;const take=b=>{const x=Number(v&((1n<<BigInt(b))-1n));v>>=BigInt(b);return x;};
  const side=[],home=[],st=[];for(let i=11;i>=0;i--)side[i]=take(1);for(let i=11;i>=0;i--)home[i]=take(1);
  for(let i=11;i>=0;i--){st[i]=[];for(let j=2;j>=0;j--)st[i][j]=take(2);}const t=take(2),g=take(3);if(g>4)return null;return{g,t,st,home,side};}
function applyCode(p,r){p.g=r.g;p.t=r.t;const tr=trackOfG(r.g);p.S.track=tr;p.S.prog=p.S.prog||{};
  for(let i=0;i<12;i++)STOPS[i].m[tr].forEach(([k,L],j)=>{const key=tr+":"+k;const pg=p.S.prog[key]||(p.S.prog[key]={lv:[0,0,0,0,0],best:0});pg.lv[L-1]=Math.max(pg.lv[L-1]||0,r.st[i][j]);});
  p.home=r.home.slice();p.side=r.side.slice();p.words=p.words.map((w,i)=>w||(i<=curStop(p)?1:0));p.at=null;}
function codeFromMsg(txt){const m=(txt||"").match(/کد\s*:\s*([^\n]+)/);if(m){const r=readCode(m[1]);if(r)return r;}const t=(txt||"").replace(/[\s‌]/g,"");for(let a=0;a+CLEN<=t.length;a++){const r=readCode(t.slice(a,a+CLEN));if(r)return r;}return null;}
function teacherMsg(p){return `کارگاه ماشین‌های ساده\nنام: ${p.name}\nپایه: ${GRADES[p.g]}\n${curStop(p)>=12?"هر ۱۲ منزل تمام شد":`منزل: ${fa(curStop(p)+1)} از ۱۲`} · ستاره: ${fa(totStars(p))}\nکد: ${makeCode(p)}`;}

/* ---------- ابزار ---------- */
function jtoast(t){document.querySelectorAll(".j-toast").forEach(x=>x.remove());const e=document.createElement("div");e.className="j-toast";e.setAttribute("role","status");e.textContent=t;document.body.appendChild(e);setTimeout(()=>e.remove(),2600);}
function clearToasts(){document.querySelectorAll(".j-toast").forEach(x=>x.remove());}
const JSTAR=on=>`<path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z" fill="${on?"#F0B429":"#D4E1E9"}" stroke="${on?"#C98A06":"#B7C6D4"}" stroke-width="1.2" stroke-linejoin="round"/>`;
function travSvg(t,s){s=s||1;const c=TRAV[t].c;const g=[
 `<rect x="-16" y="-14" width="32" height="26" rx="9" fill="${c}"/><rect x="-11" y="-8" width="22" height="12" rx="5" fill="#fff"/><circle cx="-5" cy="-2" r="3" fill="#1B2A41"/><circle cx="5" cy="-2" r="3" fill="#1B2A41"/><path d="M0 -14 V-22" stroke="${c}" stroke-width="3"/><circle cx="0" cy="-24" r="4" fill="#F0B429"/><rect x="-12" y="12" width="24" height="12" rx="4" fill="${c}" opacity=".75"/>`,
 `<path d="M0 -26 C12 -14 12 6 8 16 H-8 C-12 6 -12 -14 0 -26Z" fill="#fff" stroke="${c}" stroke-width="3"/><circle cx="0" cy="-6" r="6" fill="${c}"/><path d="M-8 8 L-16 20 L-8 16Z M8 8 L16 20 L8 16Z" fill="${c}"/><path d="M-5 18 Q0 30 5 18Z" fill="#F0B429"/>`,
 `<path d="M-22 10 V0 Q-20 -6 -12 -6 L-6 -16 H8 L14 -6 Q22 -6 22 0 V10Z" fill="${c}"/><rect x="-4" y="-13" width="10" height="7" rx="2" fill="#DDF3FF"/><circle cx="-12" cy="12" r="7" fill="#1B2A41"/><circle cx="12" cy="12" r="7" fill="#1B2A41"/><circle cx="-12" cy="12" r="2.5" fill="#fff"/><circle cx="12" cy="12" r="2.5" fill="#fff"/>`,
 `<ellipse cx="0" cy="-10" rx="17" ry="19" fill="${c}"/><path d="M-6 -28 Q-12 -10 -6 8 M6 -28 Q12 -10 6 8" stroke="#fff" stroke-width="2.5" fill="none" opacity=".7"/><path d="M-6 8 L-5 16 M6 8 L5 16" stroke="#8A5427" stroke-width="2"/><rect x="-7" y="16" width="14" height="10" rx="2" fill="#B8743A"/>`][t];return `<g transform="scale(${s})">${g}</g>`;}
const travIcon=(t,sz)=>`<svg viewBox="-30 -32 60 62" width="${sz||40}" height="${sz||40}" aria-hidden="true">${travSvg(t)}</svg>`;
function stopIcon(i,col){const s=`stroke="${col}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"`,f=`fill="${col}"`;return [
 `<rect x="-2" y="-8" width="16" height="16" rx="3" ${f}/><path d="M-16 0 H-6 M-10 -5 L-5 0 L-10 5" ${s}/>`,
 `<path d="M0 -13 V12 M-8 12 H8 M-14 -8 H14" ${s}/><path d="M-14 -8 L-18 2 H-10Z M14 -8 L10 2 H18Z" ${f}/>`,
 `<path d="M-6 -14 H6 M0 -14 V-10 L-6 -7 L6 -3 L-6 1 L6 5 L0 8 V11" ${s}/><rect x="-6" y="11" width="12" height="5" rx="1.5" ${f}/>`,
 `<rect x="-8" y="-9" width="16" height="12" rx="2" ${f}/><path d="M-15 7 H15 M-13 11 l3 -4 M-6 11 l3 -4 M1 11 l3 -4 M8 11 l3 -4" ${s}/>`,
 `<path d="M-15 -2 L15 -8" ${s}/><path d="M0 -5 L-5 8 H5Z" ${f}/><circle cx="-12" cy="-7" r="3.5" ${f}/>`,
 `<path d="M-15 4 L14 -10" ${s}/><path d="M-4 0 L-9 10 H1Z" ${f}/><rect x="-17" y="-3" width="9" height="7" rx="2" ${f}/>`,
 `<path d="M-15 11 L14 -9 V11Z" ${f} opacity=".35"/><path d="M-15 11 L14 -9 V11Z" ${s}/><rect x="-5" y="-4" width="8" height="8" rx="1.5" transform="rotate(-34 -1 0)" ${f}/>`,
 `<path d="M-14 -10 H-2 L-8 12Z" ${f}/><path d="M6 -12 H14 M10 -12 V12 M6 -6 L14 -8 M6 0 L14 -2 M6 6 L14 4" ${s}/>`,
 `<circle cx="0" cy="0" r="11" ${s}/><circle cx="0" cy="0" r="3" ${f}/><path d="M0 0 L9 -9 M9 -9 h5" ${s}/>`,
 `<circle cx="0" cy="-7" r="7" ${s}/><path d="M-7 -7 V12 M7 -7 V6" ${s}/><rect x="3" y="6" width="8" height="7" rx="1.5" ${f}/>`,
 `<circle cx="0" cy="0" r="6" ${s}/><path d="M0 -13 V-8 M0 8 V13 M-13 0 H-8 M8 0 H13 M-9 -9 l3.5 3.5 M5.5 5.5 L9 9 M-9 9 l3.5 -3.5 M5.5 -5.5 L9 -9" ${s}/>`,
 `<path d="M-9 -12 H9 V-4 A9 9 0 0 1 -9 -4Z" ${f}/><path d="M-9 -9 H-14 Q-14 -2 -8 -1 M9 -9 H14 Q14 -2 8 -1 M0 5 V10 M-6 12 H6" ${s}/>`][i];}
const JLOCK=`<g><rect x="-7" y="-2" width="14" height="11" rx="2.5" fill="#8C9BB0"/><path d="M-4 -2 V-5 A4 4 0 0 1 4 -5 V-2" stroke="#8C9BB0" stroke-width="2.5" fill="none"/></g>`;
const MAPICON=`<svg viewBox="0 0 28 28" width="26" height="26" aria-hidden="true"><path d="M3 7 L10 4 L18 7 L25 4 V21 L18 24 L10 21 L3 24Z" fill="#E6F4EA" stroke="#22965A" stroke-width="2"/><path d="M10 4 V21 M18 7 V24" stroke="#22965A" stroke-width="2"/></svg>`;
function holdBtn(label,id){return `<button class="btn j-hold" id="${id}" type="button" style="width:100%"><span class="fill"></span><span style="position:relative">${label}</span></button>`;}
function wireHold(b,done){let t0=0,raf=0;const f=b.querySelector(".fill");const stop=()=>{cancelAnimationFrame(raf);t0=0;f.style.transform="scaleX(0)";};
  const tick=()=>{const k=Math.min(1,(performance.now()-t0)/2000);f.style.transform=`scaleX(${k})`;if(k>=1){stop();done();return;}raf=requestAnimationFrame(tick);};
  const go=e=>{e.preventDefault();if(t0)return;if(e.pointerId!=null){try{b.setPointerCapture(e.pointerId);}catch(_){}}t0=performance.now();raf=requestAnimationFrame(tick);};
  b.addEventListener("pointerdown",go);["pointerup","pointercancel"].forEach(ev=>b.addEventListener(ev,stop));
  b.addEventListener("keydown",e=>{if(e.key===" "||e.key==="Enter"){if(!t0)go(e);else e.preventDefault();}});b.addEventListener("keyup",stop);b.addEventListener("contextmenu",e=>e.preventDefault());}
function jsheet(html,label,col){const o=overlay(`<div class="sheet j-sheet">${html}</div>`,label,col);return o;}
function jtop(extra){return `<header class="j-top"><button class="j-ib" id="jmap" type="button">${MAPICON}<span>نقشه</span></button>${extra||""}</header>`;}

/* ---------- شروع ---------- */
function startApp(){const h=(location.hash||"").slice(1);const wm=h.match(/^m(\d{1,2})$/);if(wm){const w=+wm[1];if(w>=1&&w<=12){DB.week=w-1;save();}}
  if(TESTMODE){applyNums();home();return;}
  if(h==="teacher"){teacherPage();return;}
  if(!DB.profiles.length){welcome();return;}
  if(DB.profiles.length>1||!JP()){pickPlayer();return;}
  useProfile(JP());applyNums();jmap({scroll:true});}
function pickPlayer(){epoch++;closeOv();clearToasts();document.body.classList.remove("tr-a","tr-b","tr-c");
  app.innerHTML=`<div class="j-page"><h1 class="j-h1">کی هستی؟</h1><div class="j-list">${DB.profiles.map(p=>`<button class="j-part j-pick" data-id="${p.id}" type="button"><span class="ic" style="background:#fff">${travIcon(p.t,52)}</span><span class="tx"><span class="n">${esc(p.name)}</span><span class="d">پایهٔ ${GRADES[p.g]} · منزل ${fa(Math.min(12,curStop(p)+1))} از ۱۲</span></span></button>`).join("")}</div><button class="btn" id="np" type="button" style="width:100%">+ بازیکن تازه</button></div>`;
  app.querySelectorAll("[data-id]").forEach(b=>b.onclick=()=>{useProfile(DB.profiles.find(p=>p.id===b.dataset.id));save();applyNums();jmap({scroll:true});});$("#np").onclick=()=>welcome(true);window.scrollTo(0,0);}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function welcome(canBack){epoch++;closeOv();clearToasts();document.body.classList.remove("tr-a","tr-b","tr-c");const st={step:0,name:"",g:null,t:null};
  const draw=()=>{let body="";
    if(st.step===0)body=`<h1 class="j-h1">سلام! به سفر ماشین‌های ساده خوش آمدی.</h1><label for="jnm" class="j-q">اسمت چیست؟</label><input type="text" id="jnm" class="j-in" maxlength="20" autocomplete="off" value="${esc(st.name)}"><p class="j-note">اگر نوشتن سخت است، از یک بزرگ‌تر کمک بگیر.</p><button class="btn go j-wide" id="jnx" type="button">بعدی</button>`;
    if(st.step===1)body=`<h2 class="j-h2">کلاس چندمی؟</h2><div class="j-grid5" role="group" aria-label="پایه">${GRADES.map((g,i)=>`<button class="j-choice" type="button" data-g="${i}" aria-pressed="${st.g===i}">${g}</button>`).join("")}</div><button class="btn go j-wide" id="jnx" type="button" ${st.g==null?"disabled":""}>بعدی</button>`;
    if(st.step===2)body=`<h2 class="j-h2">همسفرت را انتخاب کن</h2><p class="j-note">روی نقشه، همسفرت نشان می‌دهد کجا هستی.</p><div class="j-grid2" role="group" aria-label="همسفر">${TRAV.map((t,i)=>`<button class="j-choice" type="button" data-t="${i}" aria-pressed="${st.t===i}">${travIcon(i,72)}${t.n}</button>`).join("")}</div><button class="btn go j-wide" id="jnx" type="button" ${st.t==null?"disabled":""}>بزن بریم!</button>`;
    app.innerHTML=`<div class="j-page"><span class="j-step">قدم ${fa(st.step+1)} از ۳</span>${body}${st.step||canBack?`<button class="btn" id="jbk" type="button">برگشت</button>`:""}</div>`;
    const nx=$("#jnx"),bk=$("#jbk");
    if(st.step===0){const i=$("#jnm");i.focus();i.oninput=()=>{st.name=i.value;};i.onkeydown=e=>{if(e.key==="Enter")nx.click();};nx.onclick=()=>{st.name=i.value.trim();if(!st.name){i.focus();jtoast("اول اسمت را بنویس.");return;}st.step=1;draw();};}
    if(st.step===1){app.querySelectorAll("[data-g]").forEach(b=>b.onclick=()=>{st.g=+b.dataset.g;draw();});nx.onclick=()=>{st.step=2;draw();};}
    if(st.step===2){app.querySelectorAll("[data-t]").forEach(b=>b.onclick=()=>{st.t=+b.dataset.t;draw();});nx.onclick=()=>{const p=newProfile(st.name,st.g,st.t);DB.profiles.push(p);useProfile(p);save();applyNums();jmap({scroll:true});};}
    if(bk)bk.onclick=()=>{if(st.step){st.step--;draw();}else if(DB.profiles.length)pickPlayer();};};
  draw();window.scrollTo(0,0);}

/* ---------- نقشه ---------- */
const MW=400,MSP=150,MBAN=96;
function mlayout(){const pos=[];let y=40;for(let i=0;i<12;i++){if(i===0||i===4||i===10)y+=MBAN;pos.push({x:200+118*Math.sin(i*1.05+.5),y});y+=MSP;}return{pos,H:y+10};}
function jmap(opt){opt=opt||{};epoch++;closeOv();clearToasts();const p=JP();if(!p){startApp();return;}useProfile(p);applyNums();setC("scale");
  const cs=curStop(p),{pos,H}=mlayout(),W=MW,L=WL();
  let s=`<svg class="j-map" direction="rtl" viewBox="0 0 ${W} ${H}" role="group" aria-label="نقشهٔ سفر">`;
  LANDS.forEach((Ld,li)=>{const y0=pos[Ld.from].y-MBAN-34,y1=li===2?H:pos[Ld.to+1].y-MBAN-34;s+=`<rect x="0" y="${y0}" width="${W}" height="${y1-y0}" rx="26" fill="${Ld.bg}"/><text class="ttl" x="${W-18}" y="${y0+44}" text-anchor="start" font-size="26" fill="${Ld.hex}">${Ld.n}</text><text x="${W-18}" y="${y0+72}" text-anchor="start" font-size="15" fill="#56677F">جلسهٔ ${fa(Ld.from+1)} تا ${fa(Ld.to+1)}</text>`;});
  let d=`M${pos[0].x} ${pos[0].y}`,dd=d;for(let i=1;i<12;i++){const a=pos[i-1],b=pos[i],seg=` C${a.x} ${a.y+MSP*.55} ${b.x} ${b.y-MSP*.55} ${b.x} ${b.y}`;d+=seg;if(i<=cs)dd+=seg;}
  s+=`<path d="${d}" stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round"/><path d="${d}" stroke="#C9D5DE" stroke-width="10" fill="none" stroke-dasharray="2 16" stroke-linecap="round"/>`;if(cs>0)s+=`<path d="${dd}" stroke="#F0B429" stroke-width="10" fill="none" stroke-linecap="round"/>`;
  pos.forEach((q,i)=>{const sx=q.x>200?q.x-104:q.x+104,sy=q.y+18,open=i<=cs,dn=p.side[i],hx=LANDS[landOf(i)].hex;
    s+=`<path d="M${q.x+(sx>q.x?36:-36)} ${q.y+8} L${sx+(sx>q.x?-22:22)} ${sy}" stroke="${open?hx:"#C9D5DE"}" stroke-width="3" stroke-dasharray="3 6" stroke-linecap="round"/>`;
    s+=`<g class="j-stop" data-side="${i}" tabindex="${open?0:-1}" role="button" aria-label="${L.side} منزل ${fa(i+1)}${dn?"، انجام شده":open?"":"، هنوز بسته"}"><circle cx="${sx}" cy="${sy}" r="32" fill="#fff" fill-opacity="0"/><rect class="ring" x="${sx-19}" y="${sy-19}" width="38" height="38" rx="8" transform="rotate(45 ${sx} ${sy})" fill="${dn?"#F0B429":open?"#fff":"#EEF2F5"}" stroke="${dn?"#C98A06":open?hx:"#C9D5DE"}" stroke-width="3"/>${dn?`<g transform="translate(${sx-12} ${sy-12})">${JSTAR(true)}</g>`:open?`<text x="${sx}" y="${sy+7}" text-anchor="middle" font-size="20" font-weight="700" fill="${hx}">؟</text>`:`<g transform="translate(${sx} ${sy})">${JLOCK}</g>`}</g>`;});
  pos.forEach((q,i)=>{const hx=LANDS[landOf(i)].hex,done=stopDone(p,i),now=i===cs,locked=i>cs,fill=done?hx:now?"#fff":"#E6ECF1",ic=done?"#fff":now?hx:"#A9B6C4";
    s+=`<g class="j-stop" data-stop="${i}" tabindex="${locked?-1:0}" role="button" aria-label="منزل ${fa(i+1)}: ${STOPS[i].n}${done?"، تمام‌شده":now?"، تو اینجایی":"، هنوز بسته"}">`;
    if(now)s+=`<circle class="j-pulse" cx="${q.x}" cy="${q.y}" r="40" fill="none" stroke="${hx}" stroke-width="4"/>`;
    s+=`<circle cx="${q.x}" cy="${q.y}" r="46" fill="#fff" fill-opacity="0"/><circle class="ring" cx="${q.x}" cy="${q.y}" r="36" fill="${fill}" stroke="${locked?"#C9D5DE":hx}" stroke-width="${now?6:3}"/><g transform="translate(${q.x} ${q.y}) scale(1.25)">${stopIcon(i,ic)}</g>`;
    s+=`<circle cx="${q.x+27}" cy="${q.y-27}" r="14" fill="${locked?"#fff":hx}" stroke="#fff" stroke-width="3"/><text x="${q.x+27}" y="${q.y-21}" text-anchor="middle" font-size="15" font-weight="700" fill="${locked?"#8C9BB0":"#fff"}">${fa(i+1)}</text>`;
    if(locked)s+=`<g transform="translate(${q.x-27} ${q.y+26})"><circle r="13" fill="#fff"/>${JLOCK}</g>`;
    s+=`<text x="${q.x}" y="${q.y+62}" text-anchor="middle" font-size="18" font-weight="700" fill="${locked?"#8C9BB0":"#1B2A41"}">${STOPS[i].n}</text>`;
    if(done){const m=minStars(p,i);s+=`<g transform="translate(${q.x-33} ${q.y+70})">${[0,1,2].map(j=>`<g transform="translate(${j*22} 0)">${JSTAR(j<m)}</g>`).join("")}</g>`;}
    if(DB.week===i&&!done)s+=`<g transform="translate(${q.x-30} ${q.y-52})"><path d="M0 26 V0 L18 6 L0 12" fill="#E4553A" stroke="#B53A22" stroke-width="2"/></g>`;
    s+=`</g>`;});
  if(cs<12){const q=pos[cs],tx=q.x>200?q.x+60:q.x-60;s+=`<g transform="translate(${tx} ${q.y-4})"><g class="j-bob">${travSvg(p.t,1.05)}</g></g><g transform="translate(${q.x-50} ${q.y+74})"><rect width="100" height="30" rx="15" fill="#1B2A41"/><text x="50" y="21" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">تو اینجایی</text></g>`;}
  else{const q=pos[11];s+=`<g transform="translate(${q.x} ${q.y+118})">${travSvg(p.t,1.2)}</g>`;}
  s+=`</svg>`;
  const week=DB.week!=null&&cs<DB.week?`<div class="j-week"><svg width="22" height="22" viewBox="0 0 28 28" aria-hidden="true"><path d="M6 26 V2 L22 8 L6 14" fill="#E4553A" stroke="#B53A22" stroke-width="2"/></svg><span>کلاس به منزل ${fa(DB.week+1)} رسیده؛ تو در منزل ${fa(cs+1)} هستی.</span></div>`:"";
  app.innerHTML=`<header class="j-top"><div class="j-who">${travIcon(p.t,40)}<span class="nm">${esc(p.name)}</span><span class="pill"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">${JSTAR(true)}</svg> ${fa(totStars(p))}</span></div>
    <button class="j-ib" id="jbp" type="button"><svg viewBox="0 0 28 28" width="26" height="26" aria-hidden="true"><rect x="5" y="8" width="18" height="17" rx="5" fill="#B8743A"/><path d="M10 8 V6 a4 4 0 0 1 8 0 V8" stroke="#8A5427" stroke-width="2.5" fill="none"/><rect x="9" y="15" width="10" height="6" rx="2" fill="#E0A45F"/></svg><span>کوله</span></button>
    <button class="j-ib" id="jad" type="button"><svg viewBox="0 0 28 28" width="26" height="26" aria-hidden="true"><circle cx="14" cy="9" r="5" fill="#8C9BB0"/><path d="M4 25 a10 9 0 0 1 20 0Z" fill="#8C9BB0"/></svg><span>بزرگ‌ترها</span></button></header>
    <main class="j-mapwrap">${s}</main>
    <div class="j-cont"><div class="in">${week}<button class="btn go" id="jgo" type="button">${cs<12?`ادامه بده<small>${contLabel(p)}</small>`:`سفر تمام شد!<small>کوله‌پشتی‌ات را ببین</small>`}</button></div></div>`;
  app.querySelectorAll("[data-stop]").forEach(g=>{const i=+g.dataset.stop;const act=()=>{if(i>cs){jtoast(`منزل ${fa(i+1)} هنوز بسته است. اول منزل ${fa(cs+1)} را تمام کن.`);return;}stopSheet(i);};g.onclick=act;g.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();act();}};});
  app.querySelectorAll("[data-side]").forEach(g=>{const i=+g.dataset.side;const act=()=>{if(i>cs){jtoast(`اول منزل ${fa(i+1)} باید باز شود.`);return;}sideSheet(i);};g.onclick=act;g.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();act();}};});
  $("#jgo").onclick=()=>{if(cs>=12)backpack();else resume(p);};$("#jbp").onclick=()=>backpack();$("#jad").onclick=adultGate;
  if(opt.scroll!==false){const q=pos[Math.min(cs,11)];requestAnimationFrame(()=>{const svg=app.querySelector(".j-map");if(!svg)return;const r=svg.getBoundingClientRect(),k=r.width/W;window.scrollTo({top:Math.max(0,r.top+window.scrollY+q.y*k-window.innerHeight*.42),behavior:opt.smooth?"smooth":"auto"});});}
  if(p.coach){p.coach=0;save();setTimeout(()=>coach(p),350);}
  if(opt.msg)setTimeout(()=>jtoast(opt.msg),300);}
function contLabel(p){const cs=curStop(p);const j=p.at&&p.at.i===cs?p.at.j:firstOpen(p,cs);return `منزل ${fa(cs+1)}: ${STOPS[cs].n} · ${esc(mName(p,cs,j))}${p.at&&p.at.i===cs&&p.at.r?` · چالش ${fa(p.at.r.i+1)}`:""}`;}
function resume(p){const cs=curStop(p);if(p.at&&p.at.i===cs)runMission(cs,p.at.j,p.at.r);else runMission(cs,firstOpen(p,cs));}
function coach(p){const K=KID();const o=jsheet(`<div class="shead"><h2>این نقشهٔ سفر توست</h2></div><div style="display:flex;gap:12px;align-items:center">${travIcon(p.t,64)}<p class="j-say">${K?"هر دایره یک منزل است. همسفرت نشان می‌دهد کجا هستی.":"هر دایره یک «منزل» است و هر هفته یکی را با کلاس می‌روی. همسفرت نشان می‌دهد کجا هستی."}</p></div><p class="j-say">${K?"هر بار که آمدی، دکمهٔ سبز «ادامه بده» را بزن.":"هر بار که آمدی، دکمهٔ سبز «ادامه بده» را بزن. لوزی‌های کنار راه مأموریت جانبی‌اند؛ اختیاری‌اند و جایزه دارند."}</p><p class="j-note">کلاست را اشتباه زدی؟ به یک بزرگ‌تر بگو از دکمهٔ «بزرگ‌ترها» بالای صفحه درستش کند.</p><button class="btn go j-wide" id="jok" type="button">فهمیدم</button>`,"راهنمای نقشه");o.querySelector("#jok").onclick=closeOv;o.querySelector("#jok").focus();}

/* ---------- برگهٔ منزل ---------- */
function stopSheet(i){const p=JP(),Ld=LANDS[landOf(i)],ms=missions(p,i),L=WL(),K=KID();
  const rows=ms.map(([k,Lv],j)=>{const st=mStars(p,i,j),open=j===0||mStars(p,i,j-1)>0;return `<div class="j-part ${st?"done":""}"><span class="ic" style="background:${Ld.bg}"><svg viewBox="-16 -16 32 32">${stopIcon(i,Ld.hex)}</svg></span><span class="tx"><span class="k">${L.main}${ms.length>1?" "+fa(j+1)+" از "+fa(ms.length):""}</span><span class="n">${esc(mName(p,i,j))}</span>${st?`<span>${[0,1,2].map(x=>`<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">${JSTAR(x<st)}</svg>`).join("")}</span>`:""}</span><button class="btn ${st?"":"go"}" type="button" data-m="${j}" ${open?"":"disabled"}>${st?"دوباره":"شروع"}</button></div>`;}).join("");
  const o=jsheet(`<div class="shead"><div><span class="j-tag" style="background:${Ld.hex}">${Ld.n}</span><h2 style="color:var(--ink)">منزل ${fa(i+1)}: ${STOPS[i].n}</h2></div><button class="chip-btn" id="jcx" type="button">بستن</button></div>${rows}
   <div class="j-part ${p.side[i]?"done":""}"><span class="ic" style="background:#FFF6D6"><svg viewBox="0 0 32 32"><rect x="8" y="8" width="16" height="16" rx="3" transform="rotate(45 16 16)" fill="${p.side[i]?"#F0B429":"#fff"}" stroke="#C98A06" stroke-width="2.5"/></svg></span><span class="tx"><span class="k">${L.side}${K?"":" · اختیاری"}</span><span class="n">${K?`${fa(SIDEG.a[landOf(i)])} جواب درست بده`:`${fa(SIDEG[trk(p)][landOf(i)])} جواب درست در چالش بی‌پایان`}</span></span><button class="btn" type="button" id="jsd">${p.side[i]?"دوباره":"برو"}</button></div>
   <div class="j-part"><span class="ic" style="background:#EEF5FF"><svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="10" fill="none" stroke="#2F6BD0" stroke-width="3"/><path d="M16 6 v4 M16 22 v4 M6 16 h4 M22 16 h4" stroke="#2F6BD0" stroke-width="3"/></svg></span><span class="tx"><span class="k">آزمایشگاه</span><span class="n">${K?"بازی آزاد":"آزادانه امتحان کن"}</span></span><button class="btn" type="button" id="jlab">برو</button></div>
   <div class="j-part ${p.home[i]?"done":""}"><span class="ic" style="background:#EEF5FF"><svg viewBox="0 0 32 32"><path d="M5 15 L16 6 L27 15 V27 H5Z" fill="#9CC0F0"/><rect x="13" y="18" width="6" height="9" fill="#fff"/></svg></span><span class="tx"><span class="k">کار خانه${p.home[i]?" · تأیید شد":" · با یک بزرگ‌تر"}</span><span class="d">${HOME[i]}</span></span></div>
   ${p.home[i]?"":holdBtn("بزرگ‌ترِ خانه: برای تأیید ۲ ثانیه نگه دارید","jhh")}
   <button class="chip-btn" id="jdf" type="button">واژه‌ها، تعریف‌ها و فیلم‌ها</button>
   <p class="j-note">${stopDone(p,i)?"این منزل تمام شده. هر وقت خواستی دوباره بازی کن.":`با گرفتن دست‌کم یک ستاره در هر ${L.main}، منزل بعدی باز می‌شود.`}</p>`,`منزل ${fa(i+1)}`,Ld.hex);
  o.querySelector("#jcx").onclick=closeOv;o.querySelectorAll("[data-m]").forEach(b=>b.onclick=()=>runMission(i,+b.dataset.m));
  o.querySelector("#jsd").onclick=()=>runSide(i);o.querySelector("#jlab").onclick=()=>{const k=missions(p,i)[0][0];const A=board(k,{mode:"lab",backLabel:"نقشه",sub:"آزمایشگاه",back:()=>jmap({})});ST[k].lab(A);window.scrollTo(0,0);};
  o.querySelector("#jdf").onclick=()=>openDef(missions(p,i)[0][0]);
  const hh=o.querySelector("#jhh");if(hh)wireHold(hh,()=>{p.home[i]=1;save();jtoast("کار خانه تأیید شد.");stopSheet(i);});o.querySelector("#jcx").focus();}
function sideSheet(i){const p=JP(),K=KID(),goal=SIDEG[trk(p)][landOf(i)];
  const o=jsheet(`<div class="shead"><div><span class="j-tag" style="background:#C98A06">${WL().side}${K?"":" · اختیاری"}</span><h2 style="color:var(--ink)">منزل ${fa(i+1)}</h2></div><button class="chip-btn" id="jcx" type="button">بستن</button></div>
   <p class="j-say">${K?`${fa(goal)} جواب درست بده. سه قلب داری؛ هر جواب غلط یک قلب کم می‌کند.`:`در چالش بی‌پایانِ «${ST[STOPS[i].side].name}» ${fa(goal)} جواب درست بده. سه جان داری و هر جواب درست چالش بعدی را کمی سخت‌تر می‌کند.`}</p>
   <p class="j-note">${p.side[i]?"این نشان را گرفته‌ای. می‌توانی دوباره بازی کنی.":"جایزه: نشان طلایی برای کوله‌پشتی. راه منزل بعد را نمی‌بندد."}</p><button class="btn go j-wide" id="jsd" type="button">${p.side[i]?"دوباره بازی کن":"شروع"}</button>`,"مأموریت جانبی","#C98A06");
  o.querySelector("#jcx").onclick=closeOv;o.querySelector("#jsd").onclick=()=>runSide(i);o.querySelector("#jsd").focus();}

/* ---------- کارت واژه و اجرای مأموریت ---------- */
function wordCard(i,then){const p=JP(),ws=WORDS[trk(p)][i],K=KID();if(!ws.length||p.words[i]){then();return;}
  const o=jsheet(`<span class="j-step" style="text-align:center">${K?"واژهٔ تازه":"کارت واژهٔ تازه"}</span>${ws.map((w,x)=>`<div class="j-word"><span class="w">${w}</span><p>${JDEF[w][K?0:1]||JDEF[w][1]}</p></div>`).join("")}<p class="j-note" style="text-align:center">این کارت در کوله‌پشتی‌ات می‌ماند.</p><button class="btn go j-wide" id="jgo2" type="button">${K?"بزن بریم":"شروع مأموریت"}</button>`,"کارت واژه","#2F6BD0");
  o.querySelector("#jgo2").onclick=()=>{p.words[i]=1;save();closeOv();then();};o.querySelector("#jgo2").focus();}
function runMission(i,j,r){const p=JP();wordCard(i,()=>{const [k,L]=missions(p,i)[j],ms=missions(p,i),before=curStop(p);
  const sub=`منزل ${fa(i+1)} · ${WL().main}${ms.length>1?" "+fa(j+1)+" از "+fa(ms.length):""}: ${mName(p,i,j)}`;
  playLevel(k,L,{sub,resume:r&&r.specs?r:null,
    keep:st=>{p.at=st.done?null:{i,j,r:{specs:st.specs,res:st.res,i:st.i}};save();},
    back:()=>jmap({msg:"هر وقت برگردی، از همین چالش ادامه می‌دهی."}),
    finish:(stars,pts,max)=>{p.at=null;save();const after=curStop(p),opened=after>before,more=j+1<ms.length&&stars>0,K=KID();
      const o=overlay(`<div class="sheet res"><h2>${stars===3?"عالی بود!":stars===2?"آفرین!":stars===1?"خوب بود!":"یک بار دیگر امتحان کن"}</h2><div class="bigst">${[1,2,3].map(x=>`<span style="--d:${x*.18}s">${starSvg(x<=stars,52)}</span>`).join("")}</div>
        ${stars?`<div class="j-part" style="text-align:right"><span class="ic" style="background:#FFF6D6"><svg viewBox="0 0 24 24" width="30" height="30">${JSTAR(true)}</svg></span><span class="tx"><span class="k">امروز یاد گرفتی</span><span class="n" style="font-size:18px">${LEARN[i][K?0:1]}</span></span></div>`:`<p class="lead">${K?"برای منزل بعد، دست‌کم یک ستاره لازم است.":"برای باز شدن منزل بعد، دست‌کم یک ستاره لازم است. بیشتر چالش‌ها را در بار اول درست جواب بده."}</p>`}
        ${opened?`<p style="font-size:20px;font-weight:700;color:#1F8A4C">${after>=12?"سفر تمام شد! همهٔ منزل‌ها را رفتی.":`منزل ${fa(after+1)} باز شد!`}</p>`:""}
        <div class="nav" style="justify-content:center;flex-direction:column"><button class="btn go" id="jn" type="button">${more?`${WL().main} بعدی: ${esc(mName(p,i,j+1))}`:stars?"برگرد به نقشه":"دوباره امتحان کن"}</button>${stars&&!more?"":`<button class="btn" id="jm" type="button">برگرد به نقشه</button>`}</div></div>`,"نتیجه",ST[k].c);
      o.querySelector("#jn").onclick=()=>{if(more)runMission(i,j+1);else if(stars)jmap({smooth:true,msg:opened?(after>=12?"سفر تمام شد! نشان‌هایت را در کوله‌پشتی ببین.":`همسفرت به منزل ${fa(after+1)} رسید!`):null});else runMission(i,j);};const jm=o.querySelector("#jm");if(jm)jm.onclick=()=>jmap({});o.querySelector("#jn").focus();if(stars>=2)confetti();}});});}
function runSide(i){const p=JP(),goal=SIDEG[trk(p)][landOf(i)],k=STOPS[i].side;closeOv();
  playEndless(k,{goal,sub:`منزل ${fa(i+1)} · ${WL().side}`,back:()=>jmap({}),
    win:()=>{p.side[i]=1;save();const o=overlay(`<div class="sheet res"><svg width="96" height="96" viewBox="0 0 32 32" style="margin-inline:auto"><rect x="8" y="8" width="16" height="16" rx="3" transform="rotate(45 16 16)" fill="#F0B429" stroke="#C98A06" stroke-width="2"/></svg><h2>نشان طلایی منزل ${fa(i+1)}!</h2><p class="lead">${fa(goal)} جواب درست دادی. نشانت در کوله‌پشتی است.</p><div class="nav" style="justify-content:center"><button class="btn go" id="jm" type="button">برگرد به نقشه</button></div></div>`,"جایزه","#C98A06");o.querySelector("#jm").onclick=()=>jmap({});o.querySelector("#jm").focus();confetti();},
    lose:right=>{const o=overlay(`<div class="sheet res"><h2>قلب‌ها تمام شد</h2><p class="lead">${fa(right)} جواب درست از ${fa(goal)}. ${KID()?"دوباره امتحان کن!":"یک بار دیگر امتحان کن؛ هر بار از اول می‌شماریم."}</p><div class="nav" style="justify-content:center"><button class="btn go" id="jr" type="button">دوباره</button><button class="btn" id="jm" type="button">برگرد به نقشه</button></div></div>`,"پایان","#C98A06");o.querySelector("#jr").onclick=()=>runSide(i);o.querySelector("#jm").onclick=()=>jmap({});o.querySelector("#jr").focus();}});}

/* ---------- کوله‌پشتی ---------- */
function backpack(tab){epoch++;closeOv();clearToasts();const p=JP();tab=tab||"b";const K=KID();
  const tabs=[["b","نشان‌ها"],["w",K?"واژه‌ها":"کارت‌های واژه"],["c","فرستادن برای معلم"]];let body="";
  if(tab==="b")body=`<div class="j-badges">${STOPS.map((S0,i)=>{const hx=LANDS[landOf(i)].hex,ok=stopDone(p,i);return `<div class="j-badge ${ok?"":"off"}"><svg viewBox="-20 -20 40 40" width="44" height="44"><circle r="18" fill="${hx}"/><g transform="scale(.9)">${stopIcon(i,"#fff")}</g></svg>${S0.n}${ok?`<span>${[0,1,2].map(x=>`<svg width="14" height="14" viewBox="0 0 24 24">${JSTAR(x<minStars(p,i))}</svg>`).join("")}</span>`:""}</div>`;}).join("")}${STOPS.map((S0,i)=>p.side[i]?`<div class="j-badge"><svg width="44" height="44" viewBox="0 0 32 32"><rect x="8" y="8" width="16" height="16" rx="3" transform="rotate(45 16 16)" fill="#F0B429" stroke="#C98A06" stroke-width="2"/></svg>نشان طلایی ${fa(i+1)}</div>`:"").join("")}</div>`;
  if(tab==="w"){const ws=[];WORDS[trk(p)].forEach((a,i)=>{if(p.words[i])a.forEach(w=>ws.push(w));});body=ws.length?ws.map(w=>`<div class="j-word" style="text-align:right"><span class="w" style="font-size:28px">${w}</span><p>${JDEF[w][K?0:1]||JDEF[w][1]}</p></div>`).join(""):`<p class="j-say">هنوز واژه‌ای نداری. اول هر منزل یک کارت واژه می‌گیری.</p>`;}
  if(tab==="c")body=`<p class="j-say">${K?"این پیام را یک بزرگ‌تر برای معلم می‌فرستد.":"این پیام همهٔ پیشرفتت را دارد. آن را در تلگرام یا واتساپ برای معلم بفرست."}</p><textarea id="jmsg" class="j-ta" readonly aria-label="پیام برای معلم">${esc(teacherMsg(p))}</textarea><button class="btn go j-wide" id="jcp" type="button">کپی پیام</button>
    <h3 class="j-h3">پیشرفتت روی دستگاه دیگری است؟</h3><p class="j-note">پیامی را که قبلاً برای معلم فرستاده‌ای، اینجا بچسبان.</p><textarea id="jin" class="j-ta" aria-label="چسباندن پیام" style="min-height:110px"></textarea><button class="btn j-wide" id="jld" type="button">برگرداندن پیشرفت</button><p class="fb" id="jcf" aria-live="polite"></p>`;
  app.innerHTML=jtop(`<h2 class="j-h2" style="flex:1">کوله‌پشتی ${esc(p.name)}</h2>`)+`<div class="j-page"><div class="j-tabs" role="tablist">${tabs.map(([k,n])=>`<button class="chip-btn" role="tab" type="button" data-tab="${k}" aria-selected="${k===tab}">${n}</button>`).join("")}</div>${body}</div>`;
  $("#jmap").onclick=()=>jmap({});app.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>backpack(b.dataset.tab));
  if(tab==="c"){$("#jcp").onclick=()=>{const t=$("#jmsg").value,ok=()=>jtoast("کپی شد. حالا در تلگرام یا واتساپ بچسبان."),fail=()=>{const ta=$("#jmsg");ta.focus();ta.select();jtoast("متن انتخاب شد؛ آن را کپی کن.");};try{navigator.clipboard.writeText(t).then(ok,fail);}catch(e){fail();}};
    $("#jld").onclick=()=>{const r=codeFromMsg($("#jin").value),f=$("#jcf");if(!r){f.className="fb no";f.textContent="در این متن کد درستی پیدا نشد. همهٔ پیام را کپی کن و دوباره بچسبان.";return;}applyCode(p,r);useProfile(p);save();applyNums();f.className="fb ok";f.textContent="پیشرفتت برگشت!";later(900,()=>jmap({scroll:true}));};}
  window.scrollTo(0,0);}

/* ---------- بزرگ‌ترها و معلم ---------- */
function adultGate(){const o=jsheet(`<div class="shead"><h2 style="color:var(--ink)">بخش بزرگ‌ترها</h2><button class="chip-btn" id="jcx" type="button">بستن</button></div><p class="j-say">این بخش برای والدین و معلم است.</p>${holdBtn("برای ورود ۲ ثانیه نگه دارید","jgh")}`,"بخش بزرگ‌ترها");o.querySelector("#jcx").onclick=closeOv;wireHold(o.querySelector("#jgh"),()=>{closeOv();adults();});}
function adults(){epoch++;closeOv();clearToasts();const p=JP(),cs=curStop(p);document.body.classList.remove("tr-a");
  const rows=STOPS.map((S0,i)=>i>cs?"":`<tr><td><b>${fa(i+1)}. ${S0.n}</b><br><span class="j-small">کار خانه: ${HOME[i]}</span></td><td>${stopDone(p,i)?[0,1,2].map(x=>`<svg width="14" height="14" viewBox="0 0 24 24">${JSTAR(x<minStars(p,i))}</svg>`).join(""):"در حال انجام"}</td><td>${p.side[i]?"دارد":"-"}</td><td><button class="btn" type="button" data-h="${i}" aria-pressed="${!!p.home[i]}" style="min-height:44px;${p.home[i]?"background:#E3F6EA":""}">${p.home[i]?"تأیید شد":"تأیید"}</button></td></tr>`).join("")+(cs<11?`<tr><td colspan="4" class="j-small">منزل‌های بعدی وقتی باز شوند، اینجا می‌آیند.</td></tr>`:"");
  app.innerHTML=jtop(`<h2 class="j-h2" style="flex:1">بزرگ‌ترها</h2>`)+`<div class="j-page">
   <section class="j-sec"><h3 class="j-h3">پیشرفت ${esc(p.name)} · پایهٔ ${GRADES[p.g]}</h3><p>الان در منزل ${fa(Math.min(12,cs+1))} از ۱۲ است و ${fa(totStars(p))} ستاره دارد. وقتی کار خانهٔ هر منزل انجام شد، آن را تأیید کنید.</p><div class="j-scroll"><table class="j-tbl"><thead><tr><th>منزل</th><th>ستاره</th><th>جانبی</th><th>کار خانه</th></tr></thead><tbody>${rows}</tbody></table></div></section>
   <section class="j-sec"><h3 class="j-h3">پایهٔ ${esc(p.name)}</h3><p>اگر پایه اشتباه انتخاب شده، اینجا درستش کنید.</p><div class="j-grid5" role="group" aria-label="پایه">${GRADES.map((g,i)=>`<button class="j-choice" type="button" data-g="${i}" aria-pressed="${p.g===i}">${g}</button>`).join("")}</div><div id="jgc"></div></section>
   <section class="j-sec"><h3 class="j-h3">کار این هفته</h3><p>معلم هر هفته می‌گوید کلاس به کدام منزل رسیده. آن را اینجا انتخاب کنید تا روی نقشه پرچم بخورد.</p><div class="j-grid6">${STOPS.map((S0,i)=>`<button class="j-choice" type="button" data-w="${i}" aria-pressed="${DB.week===i}">${fa(i+1)}</button>`).join("")}</div><button class="chip-btn" id="jnw" type="button">بدون پرچم</button></section>
   <section class="j-sec"><h3 class="j-h3">بازیکن‌های این دستگاه</h3>${DB.profiles.map(q=>`<div class="j-row"><span style="flex:1;display:flex;gap:8px;align-items:center">${travIcon(q.t,32)} ${esc(q.name)} · ${GRADES[q.g]}</span>${q.id===p.id?`<span class="j-small">(الان)</span>`:`<button class="chip-btn" type="button" data-sw="${q.id}">رفتن به این بازیکن</button>`}<button class="chip-btn" type="button" data-del="${q.id}">پاک کردن</button></div>`).join("")}<button class="chip-btn" id="jadd" type="button">+ بازیکن تازه</button><div id="jdel"></div></section>
   <section class="j-sec"><h3 class="j-h3">همهٔ ایستگاه‌ها</h3><p>همهٔ مرحله‌ها و آزمایشگاه‌ها، بیرون از ترتیب سفر.</p><button class="chip-btn" id="jall" type="button">رفتن به ایستگاه‌ها</button></section>
   <section class="j-sec"><h3 class="j-h3">صفحهٔ معلم</h3><p>پیام‌هایی را که بچه‌ها از کوله‌پشتی فرستاده‌اند، یکجا بچسبانید تا جدول کلاس ساخته شود.</p><button class="chip-btn" id="jtp" type="button">رفتن به صفحهٔ معلم</button></section></div>`;
  $("#jmap").onclick=()=>jmap({});
  app.querySelectorAll("[data-h]").forEach(b=>b.onclick=()=>{const i=+b.dataset.h;p.home[i]=p.home[i]?0:1;save();adults();});
  app.querySelectorAll("[data-w]").forEach(b=>b.onclick=()=>{DB.week=+b.dataset.w;save();adults();jtoast(`پرچم روی منزل ${fa(DB.week+1)} گذاشته شد.`);});
  app.querySelectorAll("[data-g]").forEach(b=>b.onclick=()=>{const g=+b.dataset.g;if(g===p.g)return;const same=trackOfG(g)===trk(p),TN={a:"کاوشگر",b:"سازنده",c:"مهندس"};
    $("#jgc").innerHTML=`<div class="j-week" style="flex-direction:column;align-items:stretch"><span>${same?`پایه از ${GRADES[p.g]} به ${GRADES[g]} عوض شود؟ مسیر بازی همان «${TN[trk(p)]}» می‌ماند و چیزی عوض نمی‌شود.`:`پایه از ${GRADES[p.g]} به ${GRADES[g]} عوض شود؟ بازی به مسیر «${TN[trackOfG(g)]}» می‌رود که مرحله‌ها و متن‌هایش فرق دارد. ستاره‌های مسیر «${TN[trk(p)]}» پاک نمی‌شوند و اگر دوباره برگردید، سر جایشان هستند.`}</span><div class="j-row"><button class="btn go" id="jgy" type="button">بله، عوض کن</button><button class="btn" id="jgn" type="button">نه</button></div></div>`;
    $("#jgn").onclick=()=>{$("#jgc").innerHTML="";};$("#jgy").onclick=()=>{p.g=g;p.S.track=trackOfG(g);p.at=null;useProfile(p);save();applyNums();adults();jtoast(`پایه شد ${GRADES[g]}.`);};$("#jgy").focus();});
  $("#jnw").onclick=()=>{DB.week=null;save();adults();};
  app.querySelectorAll("[data-sw]").forEach(b=>b.onclick=()=>{useProfile(DB.profiles.find(q=>q.id===b.dataset.sw));save();applyNums();jmap({scroll:true});});
  app.querySelectorAll("[data-del]").forEach(b=>b.onclick=()=>{const q=DB.profiles.find(x=>x.id===b.dataset.del);$("#jdel").innerHTML=`<div class="j-week" style="flex-direction:column;align-items:stretch"><span>همهٔ پیشرفت ${esc(q.name)} پاک شود؟ این کار برنمی‌گردد، مگر اینکه پیام معلمش را داشته باشید.</span><div class="j-row"><button class="btn" id="jdy" type="button" style="background:#C93B22;color:#fff">بله، پاک کن</button><button class="btn" id="jdn" type="button">نه</button></div></div>`;
    $("#jdn").onclick=()=>{$("#jdel").innerHTML="";};$("#jdy").onclick=()=>{DB.profiles=DB.profiles.filter(x=>x.id!==q.id);if(DB.cur===q.id)useProfile(DB.profiles[0]||null);save();if(!DB.profiles.length)welcome();else adults();};});
  $("#jadd").onclick=()=>welcome(true);$("#jall").onclick=()=>{applyNums();home();};$("#jtp").onclick=teacherPage;window.scrollTo(0,0);}
function teacherPage(){epoch++;closeOv();clearToasts();document.body.classList.remove("tr-a");
  app.innerHTML=jtop(`<h2 class="j-h2" style="flex:1">صفحهٔ معلم</h2>`)+`<div class="j-page"><p>پیام‌های بچه‌ها را از تلگرام یا واتساپ کپی کنید و همه را با هم اینجا بچسبانید. جدول، کسانی را که عقب‌ترند اول نشان می‌دهد.</p><textarea id="jta" class="j-ta" aria-label="پیام‌های بچه‌ها" style="min-height:160px"></textarea><div class="j-row"><button class="btn go" id="jmk" type="button">ساختن جدول</button></div><div id="jout"></div></div>`;
  $("#jmap").onclick=()=>{if(JP())jmap({});else startApp();};
  $("#jmk").onclick=()=>{const txt=$("#jta").value,re=/نام\s*:\s*([^\n]+)[\s\S]*?کد\s*:\s*([^\n]+)/g;let m,rows=[],bad=0;
    while((m=re.exec(txt))){const r=readCode(m[2]);if(!r){bad++;continue;}const q=newProfile(m[1].trim(),r.g,r.t);applyCode(q,r);const cs=curStop(q);
      rows.push({name:m[1].trim(),g:r.g,cs,stars:totStars(q),home:r.home.filter(Boolean).length,side:r.side.filter(Boolean).length,per:STOPS.map((_,i)=>i<cs?minStars(q,i):null)});}
    rows.sort((a,b)=>a.cs-b.cs);
    $("#jout").innerHTML=rows.length?`<div class="j-scroll"><table class="j-tbl"><thead><tr><th>نام</th><th>پایه</th><th>منزل</th><th>ستاره</th><th>کار خانه</th><th>جانبی</th><th>منزل‌های کم‌ستاره</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.name)}</td><td>${GRADES[r.g]}</td><td>${r.cs>=12?"تمام":fa(r.cs+1)}</td><td>${fa(r.stars)}</td><td>${fa(r.home)}</td><td>${fa(r.side)}</td><td>${r.per.map((v,i)=>v===1?fa(i+1):null).filter(Boolean).join("، ")||"-"}</td></tr>`).join("")}</tbody></table></div>${bad?`<p class="fb no">${fa(bad)} پیام خوانده نشد؛ احتمالاً کامل کپی نشده است.</p>`:""}`:`<p class="fb no">پیام درستی پیدا نشد. هر پیام باید «نام:» و «کد:» داشته باشد.</p>`;};
  window.scrollTo(0,0);}

if(window.__JT)window.__J={curP,missions,mStars,curStop,levelsOf,closeOv};
startApp();
