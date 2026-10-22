#!/usr/bin/env python3
"""ایستگاه M05 «انبار تیرآهن» (سکوی شهر، city). id=beam_store؛ لایهٔ متحرک node_beam_store_prop.
نمای سه‌چهارم: تیرآهن I‌شکل از سر به سمت بیننده است؛ مقطع I (۲۶ پهن، ۲۴ بلند، بال ۶، جان ۸) روی سر نزدیک (روی زمین) دیده می‌شود
و تیر با بردار D=(-46,-40) بالا و به عقب (سمت چپ) می‌رود؛ سر دور بالا آمده است. جعبه روی سر دورِ تیر نشسته.
اجزا (از پشت به جلو؛ واحد symbol، y منفی = بالا، زمین G=10):
 ۱) سایهٔ تماس: زیر سر نزدیک تیر و زیر تکیه‌گاه.
 ۲) تکیه‌گاه (لایهٔ prop): بلوک مکعبی نارنجی-آجری ۲۲ پهن #e0702a/#ffa561/#a64a16؛ لبهٔ بالای آن موازی زیر تیر و داخل تیر؛ تیر آن را می‌پوشاند.
    حرکت: ≈۸px (به‌صورت جابه‌جایی موازی تیر به سوی جعبه)؛ حالت ایستا = پایان.
 ۳) تیرآهن: جسم کشیده‌شدهٔ مقطع I با سه پله فلز کرمی-خاکستری #e6dfca (پایه) / #fffaf0 (روی بال بالا) / #b3aa92 (جان و سایه)،
    رخ مقطع روی سر نزدیک با خط INNER، دور بیرونی PART.
 ۴) جعبه بنفش #8a5ad0 / #b992f0 (رو) / #5b3a9c (پهلو): رخ ۲۴×۲۴ با ضربدر و رو و پهلوی کم‌عمق، روی بال بالایی نزدیک سر دور.
 رنگ‌مایه: فلز ≈۴۵°، تکیه‌گاه ≈۲۲°، جعبه ≈۲۶۵°، سکوی شهر ≈۲۱۱° (همه ≥۳۵° از سکو)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
from shapely.geometry import Polygon
from shapely.ops import unary_union
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/beam_store'

S_B, S_L, S_D = '#e6dfca', '#fffaf0', '#b3aa92'
F_B, F_L, F_D = '#e0702a', '#ffa561', '#a64a16'
B_B, B_L, B_D = '#8a5ad0', '#b992f0', '#5b3a9c'
YEL = '#ffd84d'
G = 10
FX = 22                                   # مرکز سر نزدیک تیر
D = (-50, -22)                            # امتداد تیر
DD = 0                                    # بخش «عمق» روی زمین
M = D[1] / D[0]                           # شیب زیر تیر
FB = -10                                  # کف سر نزدیک تیر نسبت به زمین (در هوا)
BY = G + FB
XF = (1.1, -13, -2)
W, H, TF, TW = 34, 32, 9, 12
I0 = [(-W / 2, -H), (W / 2, -H), (W / 2, -H + TF), (TW / 2, -H + TF), (TW / 2, -TF), (W / 2, -TF), (W / 2, 0), (-W / 2, 0),
      (-W / 2, -TF), (-TW / 2, -TF), (-TW / 2, -H + TF), (-W / 2, -H + TF)]
SLIDE = 14.3                                 # واحد symbol، موازی تیر: (dx,dy)
SL = (9, 4)    # جابه‌جایی نهایی نسبت به شروع (x، y): تکیه‌گاه به سمت جعبه
XC = -33                                  # مرکز نهایی تکیه‌گاه (x نسبی به FX)


def at(pts, dx=0, dy=0): return [(FX + x + dx, BY + y + dy) for x, y in pts]


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def para(a, b, v): return [a, b, (b[0] + v[0], b[1] + v[1]), (a[0] + v[0], a[1] + v[1])]


def under(x):                              # لبهٔ زیرِ تیر (مختصات نسبی به (FX,G)) برای x < -W/2
    return FB + (x + W / 2) * (D[1] / D[0])


def prop(p):
    """تکیه‌گاه: مکعب (مستطیل) از زمین تا زیر تیر؛ لبهٔ بالای آن موازی تیر و ۷ واحد داخل تیر."""
    xc = XC; hw = 13; ins = 7
    ytop = lambda x: under(x) - ins
    pts = [(FX + xc - hw, G), (FX + xc + hw, G), (FX + xc + hw, G + ytop(xc + hw)), (FX + xc - hw, G + ytop(xc - hw))]
    p.shape(pts, F_B, PART, j=.1, step=6, clip=False)
    poly(p, [(FX + xc - hw + 3.5, G - 3), (FX + xc - hw + 7, G - 3), (FX + xc - hw + 7, G + under(xc - hw + 5) + 12), (FX + xc - hw + 3.5, G + under(xc - hw + 4) + 12)], F_L)
    poly(p, [(FX + xc + 4, G - 3), (FX + xc + hw - 3.5, G - 3), (FX + xc + hw - 3.5, G + under(xc + hw) + 12), (FX + xc + 4, G + under(xc + 4) + 12)], F_D)
    p.stroke(pts, PART, j=.1, step=6)


def beam(p):
    sil = unary_union([Polygon(I0), Polygon([(x + D[0], y + D[1]) for x, y in I0])] +
                      [Polygon(para(I0[i], I0[(i + 1) % 12], D)) for i in range(12) if Polygon(para(I0[i], I0[(i + 1) % 12], D)).area > 0]).buffer(0)
    ext = list(sil.exterior.coords)[:-1]
    p.shape(at(ext), S_B, PART, j=.05, step=7, clip=False)
    poly(p, at(para(I0[0], I0[1], D)), S_L)                                   # روی بال بالایی
    poly(p, at(para(I0[0], I0[11], D)), S_B)                                  # پهلوی چپ بال بالا
    poly(p, at(para(I0[10], I0[9], D)[:]), S_D)                               # پهلوی چپ جان
    poly(p, at(para(I0[8], I0[9], D)), S_L)                                   # روی بال پایین (درون کانال)
    poly(p, at(para(I0[7], I0[8], D)), S_B)
    p.shape(at(I0), S_B, INNER, j=.05, step=6, clip=False)                    # رخ مقطع I
    p.stroke(at(ext), PART, j=.05, step=6)


def box(p):
    t0 = .25; w = 24; h = 24
    bx, by = FX + t0 * D[0], BY - H + t0 * D[1]          # وسط لبهٔ جلوی ردپا روی روی بال
    q = (0, -6)               # عمق کم جعبه
    A, B_ = (bx - w / 2, by), (bx + w / 2, by)
    front = [A, B_, (B_[0], by - h), (A[0], by - h)]
    topf = para((A[0], by - h), (B_[0], by - h), q)
    left = para(A, (A[0], by - h), q)
    p.shape(front, B_B, PART, j=.1, step=6, clip=False)
    p.ln((A[0] + 6, by - h + 11), (B_[0] - 6, by - 5), INNER, B_D, j=0); p.ln((B_[0] - 6, by - h + 11), (A[0] + 6, by - 5), INNER, B_D, j=0)
    poly(p, [(A[0] + 4, by - h + 4), (B_[0] - 4, by - h + 4), (B_[0] - 4, by - h + 7.5), (A[0] + 4, by - h + 7.5)], B_L)
    p.stroke(front, PART, j=.1, step=6)


def build(out=OUTD):
    p = Pen('beam_store', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(FX, G + 2, 15)
    xc = FX + XC
    p.tipshadow(xc, G + 1, 17); p.foot_tip(xc, G, 12)
    with layer(p, 'prop'): prop(p)
    beam(p)
    box(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [p.V((-SL[0] * k, -SL[1] * k)) for k in (1, .75, .5, .25, 0)]
    r = finish(p, 'beam_store', STAND, motion={'prop': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_beam_store_prop': dict(translate_from=[round(-SL[0], 1), round(-SL[1], 1)], translate_to=[0, 0], dur_s=1.6, repeat=1,
                         note='تکیه‌گاه ≈۸px موازی تیر به سوی جعبه (سر دور) می‌لغزد و می‌ماند؛ تیر و جعبه ثابت؛ لبهٔ بالای تکیه‌گاه همیشه پشت تیر؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'تکیه‌گاه در جای نهایی'}
    (OUTD / 'beam_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
