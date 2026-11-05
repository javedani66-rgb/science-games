def L(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    x,y=L(a),L(b)
    if x<y:x,y=y,x
    return round((x+.05)/(y+.05),2)
if __name__=='__main__':
    H={'easy':'#28853f','mid':'#e08a1e','hard':'#c4262e'}
    for k,v in H.items():
        print(k,'peak cream',cr(v,'#fff3c4'),'peak dark',cr(v,'#241a5e'),'white',cr(v,'#ffffff'),'L',round(L(v),3))
    for n,bg in dict(sea='#075a73',grass='#3f9a2b',farm='#9a8a10',space='#c4502f',bar='#241a5e',night='#190539',cream='#fff3c4').items():
        print('fill vs',n,{k:cr(v,bg) for k,v in H.items()},'outline241a5e',cr('#241a5e',bg),'0d0426',cr('#0d0426',bg))
    print('--- buttons text')
    for n,(bg,ink) in dict(primary=('#46f0d8','#241a5e'),sec=('#fff3c4','#241a5e'),video=('#ff7be5','#241a5e'),hold=('#8a4fe0','#ffffff'),gold=('#ffd23f','#241a5e'),chip=('#4b3b9e','#fff3c4'),chipon=('#ffd23f','#241a5e'),disabled=('#d9d3e8','#4a4268'),tile_v=('#4b3b9e','#fff3c4')).items():
        print(n,bg,ink,cr(bg,ink))
    print('chip on vs chip',cr('#ffd23f','#4b3b9e'),'chip vs bar',cr('#4b3b9e','#241a5e'),'gold vs bar',cr('#ffd23f','#241a5e'))
    print('gray L diffs: yellow',round(L('#ffd23f'),2),'purple',round(L('#4b3b9e'),2))
