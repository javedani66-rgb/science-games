import sys,math; sys.path.insert(0,'.')
from lib4 import *
LINE='#2b190a'; HALO='#fff7e0'
GD=lg('gd',[(0,'#f6dc92'),(.45,'#dbac54'),(1,'#a97b2c')],0,0,.6,1)
CX,CY=60,56
def pad(fill_id,fill_def,r=52):
    return circ(CX,CY,57.5,HALO,.95)+circ(CX,CY,54.5,LINE)+circ(CX,CY,r,f'url(#{fill_id})')
def medallion(face='fc'):
    s=circ(CX,CY,39,'url(#gd)',ex=f'stroke="{LINE}" stroke-width="2.5"')+circ(CX,CY,33,'none',ex=f'stroke="{LINE}" stroke-opacity=".35" stroke-width="2"')
    s+=circ(CX,CY,31,f'url(#{face})',ex=f'stroke="{LINE}" stroke-opacity=".5" stroke-width="1.6"')
    s+=path(f'M{CX-27},{CY-12} A31,31 0 0 1 {CX+3},{CY-30}',st='#fff',sw=3,op=.6)
    for a in (45,135,225,315):
        s+=circ(CX+36*math.cos(math.radians(a)),CY+36*math.sin(math.radians(a)),2.2,'#f6dc92',ex=f'stroke="{LINE}" stroke-opacity=".6" stroke-width="1"')
    return s
SH=blur('b3',3)
SHADOW=ell(60,112,44,7,'#1b1008',.4,ex='filter="url(#b3)"')
FACE=rg('fc',[(0,'#fffaf0'),(1,'#f6e2b0')],.4,.3,.85)
def node_open():
    d=GD+SH+FACE+lg('pc',[(0,'#fffaf0'),(1,'#f1d99c')])
    b=SHADOW+pad('pc','')+circ(CX,CY,47,'none',ex='stroke="#d9b878" stroke-width="2"')
    for i in range(24):
        a=2*math.pi*i/24; b+=circ(CX+44*math.cos(a),CY+44*math.sin(a),1.5,'#d9b878')
    svg('node4-open.svg',120,120,b+medallion(),d)
def node_done():
    d=GD+SH+lg('pt',[(0,'#2f7a73'),(1,'#184441')])+rg('fw',[(0,'#fff6d0'),(1,'#ffd966')],.4,.3,.85)
    b=SHADOW+pad('pt','')+circ(CX,CY,47,'none',ex='stroke="#fff0c9" stroke-opacity=".3" stroke-width="2"')
    for i in range(28):
        a=2*math.pi*i/28; b+=circ(CX+43.5*math.cos(a),CY+43.5*math.sin(a),2,'#fff0c9')
    b+=medallion('fw')
    b+=f'<g transform="translate(70,10)"><path d="M0,26 V0" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/><path d="M1.5,1 L22,8 L1.5,16Z" fill="#f6c453" stroke="{LINE}" stroke-width="2.2" stroke-linejoin="round"/><circle cx="0" cy="-1" r="2.6" fill="#f6dc92" stroke="{LINE}" stroke-width="1.4"/></g>'
    svg('node4-done.svg',120,120,b,d)
def node_locked():
    d=SH+lg('ps',[(0,'#cfc6b6'),(1,'#9a8f7c')])+lg('ms',[(0,'#b9b09f'),(1,'#8f8576')])
    b=SHADOW+pad('ps','')+circ(CX,CY,47,'none',ex='stroke="#6e6455" stroke-opacity=".5" stroke-width="2"')
    b+=circ(CX,CY,37,'url(#ms)',ex=f'stroke="{LINE}" stroke-width="2.5"')+path(f'M{CX-26},{CY-12} A31,31 0 0 1 {CX+3},{CY-30}',st='#fff',sw=3,op=.4)
    b+=path(f'M{CX-9},{CY-4} v-10 a9,9 0 0 1 18,0 v10',st=LINE,sw=9)+path(f'M{CX-9},{CY-4} v-10 a9,9 0 0 1 18,0 v10',st='#6e6455',sw=5)
    b+=rect(CX-16,CY-4,32,26,'#6e6455',5,1,f'stroke="{LINE}" stroke-width="2.5"')+circ(CX,CY+8,3.6,LINE)+rect(CX-1.6,CY+9,3.2,7,LINE,1.4)
    svg('node4-locked.svg',120,120,b,d)
def node_trial():
    d=GD+SH+FACE+lg('pc',[(0,'#fffaf0'),(1,'#f1d99c')])+'<pattern id="st" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#fff6dc"/><rect width="3.5" height="8" fill="#e3c789"/></pattern>'
    b=SHADOW+pad('pc','')+circ(CX,CY,46,'none',ex='stroke="#1f6f68" stroke-width="3.2" stroke-dasharray="8 6"')
    b+=circ(CX,CY,39,'url(#gd)',ex=f'stroke="{LINE}" stroke-width="2.5"')+circ(CX,CY,31,'url(#st)',ex=f'stroke="{LINE}" stroke-opacity=".5" stroke-width="1.6"')
    b+=f'<g transform="translate(30,88)">{circ(0,0,15,"#184441",ex=f"stroke=\"{LINE}\" stroke-width=\"2.5\"")}{circ(0,0,12.5,"none",ex="stroke=\"#f6dc92\" stroke-width=\"1.8\"")}<path d="M-3,-8 h6 v6 l6,10 a2,2 0 0 1 -1.8,3 h-14.4 a2,2 0 0 1 -1.8,-3 l6,-10Z" fill="#fff0c9"/><path d="M-6,3 h12 l3,5 h-18Z" fill="#17a79f"/></g>'
    svg('node4-trial.svg',120,120,b,d)
def portal():
    d=GD+rg('hl',[(0,'#1b4a47'),(.7,'#0b2523'),(1,'#041210')])+blur('pb',1.4)
    b=ell(32,57,22,4.5,'#1b1008',.4,ex='filter="url(#pb)"')+circ(32,30,31,HALO,.95)+circ(32,30,29,LINE)+circ(32,30,27,'url(#gd)')
    b+=circ(32,30,20.5,LINE)+circ(32,30,18.6,'url(#hl)')+path('M16,24 A17,17 0 0 1 36,13',st='#4aa59b',sw=2,op=.55)
    for a in (45,135,225,315): b+=circ(32+23.6*math.cos(math.radians(a)),30+23.6*math.sin(math.radians(a)),1.9,'#fff0c9',ex=f'stroke="{LINE}" stroke-opacity=".6" stroke-width=".8"')
    svg('portal4.svg',64,64,b,d)
# آیکون‌های پایه (۱–۲ دانه/جوانه، ۳–۴ نهال گل‌دار، ۵–۶ درخت)؛ برگ‌ها فیروزه‌ای (نه سبز سختی)
def grade_icons():
    T='#17a79f'; TD='#0b6762'; SO='#8e5252'; SOD='#5b3138'
    soil=ell(32,54,22,6,SO,1,ex=f'stroke="{LINE}" stroke-width="2.4"')
    leaf=lambda x,y,rot,s=1,col=T:f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M0,0 C-10,-4 -12,-16 0,-22 C12,-16 10,-4 0,0Z" fill="{col}" stroke="{LINE}" stroke-width="2.2" stroke-linejoin="round"/><path d="M0,-3 V-17" stroke="{TD}" stroke-width="1.6" stroke-linecap="round"/></g>'
    g1=soil+path('M32,52 V38',st=LINE,sw=6)+path('M32,52 V38',st=TD,sw=2.6)+leaf(32,40,-42)+leaf(32,40,42)+circ(32,57,2.4,'#f6dc92',ex=f'stroke="{LINE}" stroke-width="1.2"')
    svg('grade4-1.svg',64,64,g1)
    g2=soil+path('M32,52 V26',st=LINE,sw=6)+path('M32,52 V26',st=TD,sw=2.6)+leaf(32,46,-55,.9)+leaf(32,46,55,.9)+leaf(32,34,-35,.9)+leaf(32,34,35,.9)+circ(32,22,6.5,'#df84a5',ex=f'stroke="{LINE}" stroke-width="2.2"')+circ(32,22,2.4,'#fee761')
    svg('grade4-2.svg',64,64,g2)
    g3=soil+rect(28,32,8,22,'#884b2b',2,1,f'stroke="{LINE}" stroke-width="2.2"')+circ(32,22,16,T,1,f'stroke="{LINE}" stroke-width="2.4"')+circ(20,28,10,TD,1,f'stroke="{LINE}" stroke-width="2.2"')+circ(44,28,10,TD,1,f'stroke="{LINE}" stroke-width="2.2"')+circ(32,22,13,T)+circ(26,19,2.6,'#fee761')+circ(38,25,2.6,'#fee761')+circ(31,14,2.4,'#df84a5')
    svg('grade4-3.svg',64,64,g3)
def tick():
    svg('tick4.svg',32,32,circ(16,16,14.5,'#184441',1,f'stroke="#f6dc92" stroke-width="2.4"')+path('M9,16.5 l5,5 l9,-10.5',st='#fff0c9',sw=3.6))
if __name__=='__main__':
    node_open();node_done();node_locked();node_trial();portal();grade_icons();tick();print('parts ok')
