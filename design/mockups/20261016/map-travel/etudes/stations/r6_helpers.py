"""کمک‌های مشترک دور ۶ (فقط ترسیم‌های ساده با کیت): جعبهٔ ¾، استوانهٔ ایستاده، دایره. به کیت دست نمی‌زند."""
from station_kit import *


def ident(q): return q
ident.dir = lambda v: v


def box(p, x0, y0, w, h, d, cols, sw=OUT, f=ident, seam=INNER, clip=True):
    """جعبهٔ ¾: مستطیل جلو (x0,y0 بالا-چپ، w×h)، عمق d=(dx,dy) به بالا-راست. cols=(جلو، رویه، کنار)."""
    dx, dy = d
    F = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    T = [(x0, y0), (x0 + w, y0), (x0 + w + dx, y0 + dy), (x0 + dx, y0 + dy)]
    R = [(x0 + w, y0), (x0 + w + dx, y0 + dy), (x0 + w + dx, y0 + h + dy), (x0 + w, y0 + h)]
    sil = [(x0, y0 + h), (x0, y0), (x0 + dx, y0 + dy), (x0 + w + dx, y0 + dy), (x0 + w + dx, y0 + h + dy), (x0 + w, y0 + h)]
    p.shape(TP(f, sil), cols[0], sw, j=.15, step=8, clip=clip)
    p.fill(TP(f, T), cols[1]); p.fill(TP(f, R), cols[2])
    p.ln(f((x0, y0)), f((x0 + w, y0)), seam, NAVY, j=.05); p.ln(f((x0 + w, y0)), f((x0 + w, y0 + h)), seam, NAVY, j=.05)
    p.ln(f((x0 + w, y0)), f((x0 + w + dx, y0 + dy)), seam, NAVY, j=.05)
    p.stroke(TP(f, sil), sw, j=.15, step=8)


def cyl(p, cx, yb, r, h, cols, ry=None, sw=OUT, lit=.45, f=ident, top=True):
    """استوانهٔ ایستاده: cols=(میانی، روشن، تیره، رویه)."""
    ry = ry or .34 * r; yt = yb - h
    sil = ell(cx, yb, r, ry, 0, 180, 16) + ell(cx, yt, r, ry, 180, 360, 16)
    p.shape(TP(f, sil), cols[0], sw, j=.15, step=8)
    p.fill(TP(f, [(cx - r + 2, yt), (cx - r * (1 - lit), yt), (cx - r * (1 - lit), yb + ry), (cx - r + 2, yb)]), cols[1])
    p.fill(TP(f, [(cx + r * .38, yt), (cx + r - 2, yt), (cx + r - 2, yb), (cx + r * .38, yb + ry * .9)]), cols[2], .9)
    p.stroke(TP(f, sil), sw, j=.15, step=8)
    if top: p.shape(TP(f, ell(cx, yt, r, ry, 0, 360, 28)), cols[3], PART, j=.1, step=99, clip=False)


def disc(p, x, y, r, col, f=ident):
    a, b = p.X(f((x, y))); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))
