#!/usr/bin/env python3
"""ماسک بخش «رنگ‌پذیر» لباس هر کاراکتر (D76). ماسک = پیکسل‌های پررنگِ لباس، نه پوست، داخل ناحیهٔ لباس.
هر لباس یک پیکربندی دارد (CFG): ناحیهٔ قدی، بازهٔ فام (hue)، کمینهٔ سیری/روشنی.
خروجی: <outdir>/masks/<لباس>/<نام>.png (L، ۲۵۵ = رنگ‌پذیر) و ورق بازبینی <outdir>/review_<لباس>.png
استفاده: python3 make_recolor_masks.py <cacheDir> <outdir> [لباس...]   (cacheDir = _cache ماکت منو)"""
import sys, pathlib, numpy as np
from PIL import Image
from scipy import ndimage as ndi
NAMES = ['nima', 'roya', 'sam', 'tara', 'mani', 'goli']
# y0,y1: بازهٔ قدی (نسبت به ارتفاع)؛ hue: لیست (از،تا) درجه؛ s,v: کمینه
CFG = {
 'base':        dict(y=(.30,.56), hue=[(0,360)], s=.35, v=.30, note='بالاتنه'),
 'sports':      dict(y=(.28,.74), hue=[(200,260)], s=.45, v=.30, note='پیراهن و شورت آبی'),
 'winter':      dict(y=(.26,.58), hue=[(150,235)], s=.30, v=.25, note='ژاکت'),
 'construction':dict(y=(.28,.66), hue=[(10,70)], s=.45, v=.45, note='جلیقهٔ نارنجی'),
 'carpenter':   dict(y=(.34,.68), hue=[(15,45)], s=.45, v=.25, note='پیشبند چرمی'),
 'farmer':      dict(y=(.22,.90), hue=[(180,250)], s=.05, v=.15, note='سرتاسری جین'),
 'astronaut':   dict(y=(.26,.90), hue=[(165,235)], s=.12, v=.50, note='نوارها و نشان‌های رنگی'),
 'sailor':      dict(y=(.30,.62), hue=[(5,50)], s=.65, v=.55, note='جلیقهٔ نجات'),
}

# اصلاح‌های هر کاراکتر (بازبینی ۱۶ اکتبر): (لباس، نام) -> بازنویسی بخشی از CFG
OV = {
 ('base','nima'): dict(y=(.30,.64), hue=[(80,170)], minfrac=.008), ('base','roya'): dict(y=(.34,.64), hue=[(15,65)], minfrac=.008),
 ('base','sam'): dict(y=(.36,.66), hue=[(0,30)], minfrac=.008), ('base','tara'): dict(y=(.30,.60), hue=[(255,305)], minfrac=.008),
 ('base','mani'): dict(y=(.30,.64), hue=[(45,160)], minfrac=.008), ('base','goli'): dict(y=(.30,.66), hue=[(0,45),(335,360)], s=.35, v=.2, minfrac=.004, poly=[(0.379, 0.311), (0.609, 0.311), (0.679, 0.371), (0.878, 0.462), (0.938, 0.541), (0.878, 0.597), (0.788, 0.637), (0.679, 0.613), (0.319, 0.613), (0.2, 0.637), (0.1, 0.621), (0.05, 0.541), (0.12, 0.462), (0.319, 0.371)]),
 ('sports','mani'): dict(y=(.28,.78)),
 ('carpenter','roya'): dict(y=(.34,.74)), ('carpenter','sam'): dict(y=(.34,.74)),
 ('carpenter','tara'): dict(y=(.38,.80), hue=[(12,32)], s=.25, noskin=True, poly=[(.30,.40),(.50,.40),(.52,.52),(.60,.60),(.62,.77),(.18,.77),(.19,.62),(.27,.52)]), ('carpenter','goli'): dict(y=(.38,.74), xr=(.2,.8)), ('carpenter','mani'): dict(y=(.42,.82), hue=[(10,50)], s=.30, noskin=True, xr=(.03,.80), exclude=[(.66,.64,.76,.80)]),
}
for _n in NAMES:
    OV[('winter',_n)] = dict(y=(.26,.66), hue=[(140,240)], s=.18)
    OV[('astronaut',_n)] = dict(hue=[(150,240)], s=.08)
OV[('winter','sam')] = dict(y=(.26,.66), hue=[(130,250)], s=.10, v=.12)
OV[('winter','mani')] = dict(y=(.26,.62), hue=[(130,250)], s=.10, v=.12)
OV[('astronaut','mani')] = dict(y=(.36,.90), hue=[(150,240)], s=.08)
# دور دوم بازبینی (ایجنت mask-reviewer، ۱۶ اکتبر)
OV[('winter','nima')] = dict(y=(.26,.58), hue=[(140,240)], s=.18)
OV[('winter','goli')] = dict(y=(.26,.58), hue=[(140,240)], s=.18)
OV[('winter','mani')] = dict(y=(.26,.67), hue=[(130,250)], s=.10, v=.12)
OV[('construction','roya')] = dict(y=(.36,.60))
OV[('sailor','roya')] = dict(y=(.36,.62))
OV[('astronaut','roya')] = dict(y=(.40,.90), hue=[(150,240)], s=.08)
OV[('astronaut','nima')] = dict(y=(.26,.80), hue=[(150,240)], s=.08)
OV[('base','mani')] = dict(y=(.30,.70), hue=[(45,160)], s=.25, v=.15, minfrac=.008)
OV[('carpenter','nima')] = dict(y=(.34,.72), hue=[(12,32)])

# دور سوم (بازبینی از خروجی واقعی، ۱۶ اکتبر ۱۵:۱۹)
for _n in ['nima','roya','sam','tara','goli']:
    OV[('winter',_n)] = dict(y=(.26,.66), hue=[(140,235)], s=.25, v=.32, exclude=[(.30,.24,.70,.38)])
OV[('winter','mani')] = dict(y=(.26,.70), hue=[(130,250)], s=.10, v=.12, exclude=[(.30,.24,.70,.38)])
OV[('winter','sam')] = dict(y=(.26,.66), hue=[(140,235)], s=.20, v=.30, exclude=[(.30,.24,.70,.38)])
OV[('base','nima')] = dict(y=(.28,.64), hue=[(80,170)], s=.20, v=.18, minfrac=.004)
OV[('base','goli')] = {**OV[('base','goli')], 's': .25, 'v': .15}
OV[('base','mani')] = dict(y=(.30,.70), hue=[(40,170)], s=.15, v=.15, minfrac=.008)
OV[('sports','mani')] = dict(y=(.28,.80))
OV[('construction','mani')] = dict(y=(.28,.68))
OV[('construction','roya')] = dict(y=(.36,.62))
OV[('carpenter','nima')] = dict(y=(.34,.72), hue=[(10,40)], v=.15)
OV[('carpenter','mani')] = {**OV[('carpenter','mani')], 'exclude': [(.66,.64,.76,.80), (0,.38,.08,.62)]}
OV[('sailor','mani')] = dict(y=(.26,.62), hue=[(0,55)], v=.35)
for _n in ['nima','roya','sam','tara','goli']:
    OV[('sailor',_n)] = {**OV.get(('sailor',_n), {}), 'v': .35}

# دور چهارم (۱۶ اکتبر ۱۷:۲۰): شال تارا/مانی، لگن نیما/گلی/سام
for _n in ['tara','mani']:
    OV[('winter',_n)] = {**OV[('winter',_n)], 'exclude': [(.25,.22,.75,.40)]}
for _n in ['nima','goli','sam']:
    OV[('winter',_n)] = {**OV[('winter',_n)], 'y': (.26,.63)}

def hsv(a):
    a = a / 255.; mx = a.max(2); mn = a.min(2); d = mx - mn + 1e-9
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h % 360, np.where(mx > 0, (mx - mn) / (mx + 1e-9), 0), mx

def skin_color(a, alpha, h, s, v):
    H, W = alpha.shape
    box = np.zeros_like(alpha); box[int(H * .07):int(H * .22), int(W * .3):int(W * .7)] = True
    sel = box & alpha & (h > 5) & (h < 40) & (s > .25) & (s < .75) & (v > .35)
    return np.median(a[sel][:, :3], axis=0) if sel.sum() > 50 else np.array([200., 140., 100.])

def near_skin_all(a, sk): return np.sqrt(((a[..., :3] - sk) ** 2).sum(2)) < 38

def hue_wide(h, cfg):
    r = np.zeros(h.shape, bool)
    for lo, hi in cfg['hue']: r |= (h >= lo - 15) & (h <= hi + 15)
    return r

def mask(im, cfg, debug=False):
    """v2: مؤلفه‌های متصلِ رنگ لباس که خط دور تیره از هم جدایشان می‌کند؛ پوست را مؤلفه‌به‌مؤلفه کنار می‌گذارد."""
    a = np.asarray(im).astype(float); alpha = a[..., 3] > 200
    h, s, v = hsv(a[..., :3]); H = a.shape[0]
    lum = a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114
    ink = lum < cfg.get('ink', 58)
    band = np.zeros_like(alpha); band[int(H * cfg['y'][0]):int(H * cfg['y'][1])] = True
    hue = np.zeros_like(alpha)
    for lo, hi in cfg['hue']: hue |= (h >= lo) & (h <= hi)
    xr = np.ones_like(alpha)
    if 'xr' in cfg:
        W = a.shape[1]; xr[:] = False; xr[:, int(W * cfg['xr'][0]):int(W * cfg['xr'][1])] = True
    if 'poly' in cfg:
        from PIL import ImageDraw
        pm = Image.new('L', (a.shape[1], a.shape[0]), 0); ImageDraw.Draw(pm).polygon([(x * a.shape[1], y * a.shape[0]) for x, y in cfg['poly']], fill=255)
        xr = np.asarray(pm) > 0
    cand = xr & alpha & band & hue & ~ink & (s >= cfg['s']) & (v >= cfg['v'])
    sk = skin_color(a, alpha, h, s, v)
    seg = ndi.binary_erosion(cand, iterations=1)
    lab, n = ndi.label(seg)
    if n == 0: return np.zeros_like(alpha)
    ids = list(range(1, n + 1)); sz = np.array(ndi.sum(seg, lab, ids))
    keep = []
    for i, z in zip(ids, sz):
        if z < cfg.get('minfrac', .02) * sz.max(): continue
        sel = lab == i; mc = a[sel][:, :3].mean(0); d = float(np.sqrt(((mc - sk) ** 2).sum())); ms = float(s[sel].mean())
        is_skin = d < cfg.get('skind', 30) and ms < .72 and not cfg.get('noskin')
        if debug: print('  comp', i, int(z), 'dist-skin %.0f' % d, 'sat %.2f' % ms, 'SKIN' if is_skin else 'ok')
        if not is_skin: keep.append(i)
    m = ndi.binary_dilation(np.isin(lab, keep), iterations=2) & cand
    grow = ndi.binary_dilation(m, iterations=2) & alpha & band & xr & ~ink & (s >= cfg['s'] * .5) & (v >= cfg['v'] * .6)
    if not cfg.get('noskin'): grow &= ~(near_skin_all(a, sk) & (s < .70))
    m = m | (grow & hue_wide(h, cfg))
    m = m | (ndi.binary_closing(m, iterations=2) & alpha & band & xr & ~ink)
    for x0, y0, x1, y1 in cfg.get('exclude', []):  # مستطیل‌های ممنوع (دستهٔ چکش و …)
        m[int(a.shape[0] * y0):int(a.shape[0] * y1), int(a.shape[1] * x0):int(a.shape[1] * x1)] = False
    # حفره‌های ریز (نقطهٔ سفید دانه‌بندی) پر شوند؛ جزئیات بزرگ (ستاره، نشان) نه
    holes = ndi.binary_fill_holes(m) & ~m; hl, hn = ndi.label(holes)
    for k in range(1, hn + 1):
        if (hl == k).sum() < 25: m |= hl == k
    return m & alpha & band

def shifted(im, m, deg):
    a = np.asarray(im).astype(float); h, s, v = hsv(a[..., :3])
    h2 = np.where(m, h + deg, h) % 360; hh = h2 / 60; c = v * s; x = c * (1 - abs(hh % 2 - 1)); mm = v - c; z = np.zeros_like(c); i = hh.astype(int) % 6
    rgb = np.stack([np.choose(i, [c, x, z, z, x, c]) + mm, np.choose(i, [x, c, c, x, z, z]) + mm, np.choose(i, [z, z, x, c, c, x]) + mm], -1) * 255
    out = a.copy(); out[..., :3] = np.where(m[..., None], rgb, a[..., :3])
    return Image.fromarray(out.clip(0, 255).astype('uint8'), 'RGBA')

def main():
    cache = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); outfits = sys.argv[3:] or list(CFG)
    for o in outfits:
        (out / 'masks' / o).mkdir(parents=True, exist_ok=True)
        Hh = 300; W = 150; cols = 4
        sheet = Image.new('RGB', (W * cols, Hh * len(NAMES)), (255, 243, 196))
        for r, n in enumerate(NAMES):
            im = Image.open(cache / o / f'{n}.webp').convert('RGBA'); m = mask(im, {**CFG[o], **OV.get((o, n), {})}, debug=bool(__import__('os').environ.get('MDBG')) and (o, n) in [('carpenter','mani'),('winter','sam')])
            Image.fromarray((m * 255).astype('uint8')).save(out / 'masks' / o / f'{n}.png')
            ov = np.asarray(im).copy(); ov[m, :3] = (ov[m, :3] * .3 + np.array([255, 0, 255]) * .7).astype('uint8')
            tiles = [im, Image.fromarray(ov), shifted(im, m, 140), shifted(im, m, 260)]
            for c, t in enumerate(tiles):
                t = t.resize((round(t.width * Hh / t.height), Hh), Image.LANCZOS); sheet.paste(t, (c * W + (W - t.width) // 2, r * Hh), t)
            print(o, n, 'سطح ماسک %.1f%%' % (100 * m.mean() / max(alpha_frac(im), 1e-9)))
        sheet.save(out / f'review_{o}.png')

def alpha_frac(im): return (np.asarray(im)[..., 3] > 200).mean()
if __name__ == '__main__': main()
