# mappath.py: هندسهٔ مسیر نقشه (منبع یگانه؛ نسخهٔ JS همین‌جاست: ../mappath.js)
# مختصات: «داخلی» = داخل قاب (پهنا ۳۴۶، ارتفاع H). ستون‌های ثابت: R=248 و L=98. شعاع گره ۴۸.
import math
W_IN=346; COL_R=248; COL_L=98; NODE_R=48; K=.62
def col_x(i, first_col=COL_R):          # گره‌ها متناوب: راست، چپ، راست، چپ …
    return first_col if i%2==0 else (COL_L if first_col==COL_R else COL_R)
def seg(a,b):
    """از مرکز گرهٔ a با مماس افقی بیرون می‌آید و از بالا (مماس عمودی) به گرهٔ b می‌رسد: یک قوس ملایم، بدون پیچ‌وخم."""
    (xa,ya),(xb,yb)=a,b
    if abs(xa-xb)<1: return f'M{xa} {ya}L{xb} {yb}'
    return f'M{xa} {ya}C{xa+K*(xb-xa):.1f} {ya} {xb} {yb-K*(yb-ya):.1f} {xb} {yb}'
def bez_pts(a,b,n=200):
    (xa,ya),(xb,yb)=a,b
    if abs(xa-xb)<1: return [(xa,ya+(yb-ya)*t/n) for t in range(n+1)]
    p=[(xa,ya),(xa+K*(xb-xa),ya),(xb,yb-K*(yb-ya)),(xb,yb)]
    out=[]
    for i in range(n+1):
        t=i/n;u=1-t
        out.append((u**3*p[0][0]+3*u*u*t*p[1][0]+3*u*t*t*p[2][0]+t**3*p[3][0], u**3*p[0][1]+3*u*u*t*p[1][1]+3*u*t*t*p[2][1]+t**3*p[3][1]))
    return out
def footprints(a,b,step=30,margin=34):
    """ردپا: نقطه‌ها روی منحنی با فاصلهٔ ثابت، چپ/راست متناوب. (x,y,زاویهٔ درجه)"""
    pts=bez_pts(a,b); L=[0]
    for i in range(1,len(pts)): L.append(L[-1]+math.dist(pts[i],pts[i-1]))
    res=[];side=1;s=margin
    while s<L[-1]-margin:
        j=next(i for i in range(len(L)) if L[i]>=s); p=pts[j];q=pts[min(j+1,len(pts)-1)]
        an=math.atan2(q[1]-p[1],q[0]-p[0])
        res.append((p[0]+math.cos(an+math.pi/2)*3.4*side,p[1]+math.sin(an+math.pi/2)*3.4*side,math.degrees(an)+90))
        s+=step;side=-side
    return res
