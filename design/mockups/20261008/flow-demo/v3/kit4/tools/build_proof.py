"""proof.html از strings.fa.json (متن‌ها) + داده‌های نمونه؛ هیچ متنی در JS/CSS دستی نیست."""
import json,pathlib
H=pathlib.Path(__file__).resolve().parents[1]
S={k:v['text'] for k,v in json.load(open(H/'strings.fa.json',encoding='utf-8')).items()}
def N(i,sym,state,here=False,lock=None,trial=False):
    tags=[]
    if here: tags.append(dict(cls='here',text=S['flow.map.here'],ic=1))
    if lock: tags.append(dict(cls='lock',text=S['flow.lock.reason'].replace('{name}',S['v4.node.'+lock]),ic=1))
    if trial: tags.append(dict(cls='trial',text=S['flow.land.experimental'],ic=1))
    return dict(id=i,env=S['v4.node.'+i],sym=sym,state=state,here=here,tags=tags)
frames=[
 dict(skin='stadium',plate=S['v4.land.stadium'],sym='force',first=True,last=False,exitDone=False,nodes=[N('F01','force','done'),N('F02','force','done'),N('F03','force','open',True),N('F04','force','locked',lock='F03')]),
 dict(skin='space',plate=S['v4.land.space'],sym='weight',first=False,last=False,exitDone=False,nodes=[N('W01','weight','done'),N('W02','weight','done'),N('F05','weight','done'),N('W03','weight','open',True),N('W04','weight','locked',lock='W03')]),
 dict(skin='farm',plate=S['v4.land.farm'],sym='energy',first=False,last=False,exitDone=True,nodes=[N('E01','energy','done'),N('E02','energy','open',True),N('E07','energy','trial',trial=True)]),
 dict(skin='city',plate=S['v4.land.city'],sym='machine',first=False,last=True,exitDone=False,nodes=[N('M01','machine','done'),N('B01','machine','open',True),N('B02','machine','locked',lock='B01')]),
]
js_S=dict(start=S['flow.map.start'],end=S['flow.map.end'])
html=f'''<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>اثبات kit4: جداسازی لایه‌ای نقشه (ماکت ایستا، آزموده با کودک نشده)</title>
<link rel="stylesheet" href="../kit/kit.css"><link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="map4.css">
<style>
html,body{{margin:0;height:100%;background:#1d1d1d}}
#phone{{position:relative;width:390px;height:800px;margin:0 auto;overflow:hidden;display:flex;flex-direction:column;background:var(--parchment);isolation:isolate}}
.body{{flex:1;min-height:0;overflow:auto;position:relative;scrollbar-width:none}}.body::-webkit-scrollbar{{display:none}}
.topbar .mbtn{{flex:none;min-height:48px;padding:0 12px;gap:6px;font-size:15px}}.topbar .mbtn .ic{{width:26px;height:26px}}
.topbar h1.t-title{{margin:0;flex:1;min-width:0;font-size:24px;line-height:1.2;text-align:center}}
.scrim4{{position:absolute;inset:0;z-index:50;background:rgba(15,46,44,.55)}}
.sheet4{{position:absolute;left:0;right:0;bottom:0;z-index:51;padding-bottom:16px}}
.sheet4 .tiles{{gap:12px;margin-top:14px}}.sheet4 .tile{{min-height:98px;padding:8px;gap:2px}}.sheet4 .tile__ic{{width:50px;height:50px}}
.sheet4 .row{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:14px}}
.sheet4 .adults{{color:var(--ink);opacity:.9;border-color:var(--gold-dark);background:rgba(255,255,255,.35)}}
.sheet4 .btn{{min-height:52px}}
</style></head><body class="kit">
<div id="phone"><div class="topbar" id="tb"></div><div class="body" id="mb"><div class="map4" id="map"></div></div></div>
<script src="map4.js"></script>
<script>
var DATA={json.dumps(dict(frames=frames),ensure_ascii=False)}, S={json.dumps(js_S,ensure_ascii=False)}, G={json.dumps({k:S[k] for k in ['v4.grade.cap','v4.grade.1','v4.grade.2','v4.grade.3','v4.grade.aria','flow.menu.map','flow.menu.cards','flow.menu.practice','flow.menu.guide','flow.menu.adults','flow.menu.back','flow.map.title','flow.menu.open']},ensure_ascii=False)};
var q=new URLSearchParams(location.search), V=q.get('v')||'stadium', GR=+(q.get('g')||2); if(V==='menu2')GR=3;
var tb=document.getElementById('tb');
tb.innerHTML='<button class="gbadge" data-g="'+GR+'" aria-label="'+G['v4.grade.aria']+'"><i></i><bdi>'+G['v4.grade.'+GR]+'</bdi></button><h1 class="t-title">'+G['flow.map.title']+'</h1><button class="btn btn--secondary btn--sm mbtn"><i class="ic ic-menu"></i><span>'+G['flow.menu.open']+'</span></button>';
var map=document.getElementById('map'),mb=document.getElementById('mb');
Map4.build(map,DATA,S);
(document.fonts&&document.fonts.ready||Promise.resolve()).then(function(){{
  Map4.layout(map,DATA);
  var ws=map.querySelectorAll('.landwrap');
  function topOf(i){{return ws[i].offsetTop}}
  var m={{stadium:function(){{return 0}},space:function(){{return topOf(1)-16}},farm:function(){{return topOf(2)-16}},city:function(){{return topOf(3)-16}},join12:function(){{return topOf(1)-330}},join34:function(){{return topOf(3)-330}},join23:function(){{return topOf(2)-330}},menu:function(){{return 0}},menu2:function(){{return 0}}}};
  mb.scrollTop=(m[V]||m.stadium)();
  if(V==='menu'||V==='menu2'){{
    if(V==='menu2')GR=3;
    var gs=[1,2,3].map(function(g){{return '<button class="grade" role="radio" data-g="'+g+'" aria-checked="'+(g===GR)+'"><i class="gi"></i><bdi>'+G['v4.grade.'+g]+'</bdi></button>'}}).join('');
    var d=document.createElement('div');
    d.innerHTML='<div class="scrim4"></div><div class="sheet4 sheet"><p class="gcap">'+G['v4.grade.cap']+'</p><div class="grades" role="radiogroup" aria-label="'+G['v4.grade.aria']+'">'+gs+'</div>'
     +'<div class="tiles"><button class="tile tile--map"><i class="tile__ic"></i>'+G['flow.menu.map']+'</button><button class="tile tile--cards"><i class="tile__ic"></i>'+G['flow.menu.cards']+'</button><button class="tile tile--practice"><i class="tile__ic"></i>'+G['flow.menu.practice']+'</button><button class="tile tile--guide"><i class="tile__ic"></i>'+G['flow.menu.guide']+'</button></div>'
     +'<div class="row"><span class="adults"><i class="ic"></i>'+G['flow.menu.adults']+'</span><button class="btn btn--secondary"><i class="ic ic-back"></i>'+G['flow.menu.back']+'</button></div></div>';
    document.getElementById('phone').append.apply(document.getElementById('phone'),d.children.length?[...d.children]:[]);
    var cur=document.querySelector('.grade[aria-checked=true]'); 
  }}
  document.documentElement.dataset.ready='1';
}});
</script></body></html>'''
(H/'proof.html').write_text(html,encoding='utf-8'); print('proof ok')
