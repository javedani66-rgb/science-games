# palettes.py: منبع یگانهٔ پالت زمین‌ها (kit.css از همین‌جا پر می‌شود: gen_palette_css.py).
# اصل: پس‌زمینه روشنایی میانی-پایین (Y نسبی ≤ ~0.25) و کم‌اشباع‌تر؛ مسیر/گره/برچسب روشن‌ترین لایه.
def _lin(c):
    c/=255
    return c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
def Y(hexc):
    h=hexc.lstrip('#'); r,g,b=(int(h[i:i+2],16) for i in (0,2,4))
    return .2126*_lin(r)+.7152*_lin(g)+.0722*_lin(b)
def ratio(a,b):
    ya,yb=Y(a),Y(b)
    hi,lo=max(ya,yb),min(ya,yb)
    return (hi+.05)/(lo+.05)

# ثابت‌های لایهٔ «شکل» (مسیر/گره/برچسب) برای همهٔ زمین‌ها
FIG=dict(path_light='#fff4d2', path_done='#ffe9a6', path_edge='#24160a', foot='#6b4a1e')

PAL={
 # ورزشگاه: غروب گرم؛ نور از راست-بالا؛ تأکید فیروزه‌ای (مکمل خاک‌رس/سبز)
 'stadium':dict(name='ورزشگاه',light='warm',
   sky0='#5a3763',sky1='#a24f62',sky2='#b8664e',glow='#ffb066',far='#8a5870',stand='#82475a',
   pitch0='#4c7c4a',pitch1='#3d6a3f',track='#9a4e3a',front='#6b3a2c',deco='#e8b27a',
   accent='#2fd0c0',accent_d='#0d6f68',accent_l='#9af0e6'),
 # پایگاه فضایی: شب بنفش-نیلی با سحابی فیروزه‌ای/سرخابی؛ تأکید زرد ستاره‌ای
 'space':dict(name='پایگاه فضایی',light='cool',
   sky0='#140b34',sky1='#2c1a62',sky2='#4a2a7c',glow='#c0448a',far='#3e2a78',stand='#6a5a9a',
   pitch0='#5a3a82',pitch1='#46306e',track='#7a3f86',front='#34205a',deco='#f2d9ff',
   accent='#ffc93c',accent_d='#8a5a00',accent_l='#ffe9a0'),
 # مزرعه و آسیاب: غروب طلایی؛ تپه‌های مرزه‌ای؛ تأکید آبی آسمانی (مکمل گرم)
 'farm':dict(name='مزرعه و آسیاب',light='warm',
   sky0='#5e4678',sky1='#a65a60',sky2='#b8704f',glow='#ffc27a',far='#7b6585',stand='#9a6a5a',
   pitch0='#5a7c44',pitch1='#6b7a38',track='#2f8088',front='#5f6c30',deco='#e6c07a',
   accent='#55b8ff',accent_d='#14568a',accent_l='#b6e2ff'),
 # شهر ماشین‌ها: سپیده‌دم سرد فیروزه‌ای با روشنایی کهربایی؛ تأکید صورتی (مکمل فیروزه)
 'city':dict(name='شهر ماشین‌ها',light='cool',
   sky0='#183e52',sky1='#2f6c7c',sky2='#a06a58',glow='#ffbe74',far='#3d6a78',stand='#7a4650',
   pitch0='#3c5c66',pitch1='#33505a',track='#8a6a3a',front='#2c4650',deco='#ffd27a',
   accent='#ff86b8',accent_d='#8a1f56',accent_l='#ffc4dc'),
}
if __name__=='__main__':
    for k,p in PAL.items():
        print(k,{n:round(Y(v),3) for n,v in p.items() if isinstance(v,str) and v.startswith('#')})
    print('path light vs sky2/pitch', {k:(round(ratio(FIG['path_light'],p['sky2']),2),round(ratio(FIG['path_light'],p['pitch0']),2)) for k,p in PAL.items()})
