exec(open('steps.py').read().split("M=json.load(open('lever3_meta.json'))")[0])
L=dict(L1);L['hbd']='#2A1A14'
def wtile(img,label,used=False,mh=52):
    return f'<div class="wt{" used" if used else ""}"><img style="max-height:{mh}px" src="{b64(img)}">{label}</div>'
VB='0 60 800 760'
tray=wtile('w1.png','۱ کیلوگرم',mh=34)+wtile('w1.png','۱ کیلوگرم',mh=34)+wtile('w2.png','۲ کیلوگرم',mh=44)+wtile('w5.png','۵ کیلوگرم',mh=48)
before=f'''<style>{CSS2}</style><section class="ph" style="{var(L)}">{hdr2(L,"کارگاه نجاری",2,"جرم و وزن",0)}
{scene('bal_before.png',vb=VB)}<div class="panel">
<div class="who"><div class="nm">{bust(1,"thinking",52,"#1F6F6B","#FFF6E6")}اوستا هستی</div><p>جرمِ این جعبه را پیدا کن. وزنه‌ها را روی کفهٔ دیگرِ <span class="term">ترازو</span> بگذار تا دو کفه هم‌تراز&nbsp;شوند.</p></div>
<div class="tray">{tray}</div>
<div class="bar"><button class="btn pri full">بررسی کن</button></div></div></section>'''
after=f'''<style>{CSS2}</style><section class="ph" style="{var(L)}">{hdr2(L,"کارگاه نجاری",2,"جرم و وزن",2)}
{scene('bal_after.png',vb=VB)}<div class="panel">
<div class="who"><div class="nm">{bust(1,"happy",52,"#1F6F6B","#FFF6E6")}اوستا هستی</div><p style="font-weight:700;color:#0F4F2A">آفرین! دو کفه هم‌تراز شدند؛ پس جرمِ جعبه با جرمِ وزنه‌ها برابر است: ۳&nbsp;کیلوگرم.</p></div>
<div class="fx">۱ kg + ۲ kg = ۳ kg<small>ترازوی دوکفه‌ای جرمِ دو چیز را با هم مقایسه&nbsp;می‌کند.</small></div>
<div class="bar"><button class="btn pri full">مأموریتِ بعد</button></div></div></section>'''
open('b_before.html','w').write('<meta charset=utf8>'+before);open('b_after.html','w').write('<meta charset=utf8>'+after)
