# Saving checks (2026-10-01): old star data migrates to level ids, stops 7/8 swap,
# progress code v3 round-trip, v2 codes still read, broken data never crashes. Prints nothing when fine.
from harness import *
JURL='file://'+D+'jtest.html'
OLD={"profiles":[{"id":"pold","name":"قدیمی","g":3,"t":2,"shirt":"","lvl":None,"done":"","quiz":[1,0,0,0,0],"stash":{},"cards":[],
  "S":{"prog":{"c:force":{"lv":[3,2,1,0,0],"best":4},"c:ramp":{"lv":[2,0,0,0,0],"best":0},"c:wedge":{"lv":[3,0,0,0,0],"best":0}},"nums":True,"forces":True,"formula":False,"track":"c"},
  "home":[1,0,0,0,0,0,1,0,0,0,0,0],"side":[0]*12,"words":[1]*12,"at":None,"coach":0}],"cur":"pold","week":None}
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(JURL); pg.evaluate("d=>{localStorage.clear();localStorage.setItem('sm-journey-v1',JSON.stringify(d))}",OLD); pg.reload(); pg.wait_for_timeout(300)
    r=pg.evaluate("""()=>{const {curP,mStars,makeCode,readCode}=__J;const p=curP();
      const o={ls:p.S.ls,home:p.home,f0:mStars(p,0,0),f1:mStars(p,0,1),s6:mStars(p,6,0),s7:mStars(p,7,0),sv:p.sv};
      const c=makeCode(p);const rr=readCode(c);o.len=c.replace(/[\\s\\u200c]/g,'').length;o.rt=JSON.stringify(rr.st)==JSON.stringify([...Array(12)].map((_,i)=>[0,1,2].map(j=>j<__J.missions(p,i).length?mStars(p,i,j):0)));
      o.home2=rr.home;return o;}""")
    exp_ls={'c:force.2':3,'c:force.3':2,'c:force.4':1,'c:ramp.2':2,'c:wedge.2':3}
    if r['ls']!=exp_ls: print('migrate ls',r['ls'])
    if r['home'][6]!=0 or r['home'][7]!=1: print('home swap',r['home'])
    if (r['f0'],r['f1'])!=(3,2): print('stop1 stars',r['f0'],r['f1'])
    if r['s6']!=3 or r['s7']!=2: print('stop7 wedge / stop8 ramp stars',r['s6'],r['s7'])
    if r['len']!=31 or not r['rt']: print('code v3',r['len'],r['rt'])
    # a v2 code made by the published version (26 letters): build one with the old encoder inline
    v2=pg.evaluate("""()=>{const ABC="بپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی",B31=31n,M=0x1B7E3C95A0F24D6C8E1357A9B2D46F0n;let v=0n;const add=(x,b)=>{v=(v<<BigInt(b))|BigInt(x);};
      add(3,3);add(2,3);add(0,3);add(2,2);add(0,4);for(let i=0;i<12;i++)for(let j=0;j<3;j++)add(i===6?1:i===7?3:0,2);for(let i=0;i<12;i++)add(i===6?1:0,1);for(let i=0;i<12;i++)add(0,1);for(let i=0;i<5;i++)add(0,1);
      add(Number(v%2039n),11);v^=M;const out=[];for(let k=0;k<26;k++){out.unshift(ABC[Number(v%B31)]);v/=B31;}const r=__J.readCode(out.join(''));return r&&{s6:r.st[6],s7:r.st[7],h:r.home};}""")
    if not v2 or v2['s6']!=[3,3,3] or v2['s7']!=[1,1,1] or v2['h'][7]!=1: print('v2 read',v2)
    for bad in ['{"profiles":[{"id":"x","S":{"prog":{"c:force":{"lv":"zz"}}}}],"cur":"x"}','{"profiles":[{"id":"y","name":"a","g":1,"t":0,"S":{"prog":null,"track":"a"}}],"cur":"y"}','not json']:
        pg.evaluate("d=>{localStorage.clear();localStorage.setItem('sm-journey-v1',d)}",bad); pg.reload(); pg.wait_for_timeout(300)
    if errs: print('ERR',errs[:5])
    b.close()
