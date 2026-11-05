#!/usr/bin/env python3
"""سنجش ضخامت خط‌های سرمه‌ای داخل نمادهای نقشه (D197).
درخواست مالک ۴ نوامبر: «خیلی جاها ضخامت خطوط داخلی (مثلاً میان تیر و ستون) به اندازهٔ خطوط بیرونی شده.»
عامل‌ها: symbol-line-weight-inspector (سنجش + تأیید چشمی) و symbol-line-closeup-reviewer (نظر دوم مستقل).

قاعدهٔ کیت (station_kit): خط دور بیرونی OUT=۷٫۶ واحد ≈ ۵٫۵px نقشه؛ مرز اجزا PART=۵٫۸ ≈ ۴٫۲px؛ درز/خط داخلی INNER=۳٫۹ ≈ ۲٫۸px.
هر نماد در خود نقشه (حالت ایستا، بدون سایه/نور) با بزرگ‌نمایی ۶ رندر می‌شود؛ خط‌های سرمه‌ای جدا و اسکلت‌شان گرفته می‌شود؛
پهنای خط در هر نقطهٔ اسکلت = ۲ × فاصله تا لبهٔ خط. خط‌هایی که «داخل» نمادند (دورتر از ۶٫۲px از زمینه) و پهنایشان ≥ ۴٫۸px است
(یعنی هم‌اندازهٔ خط دور بیرونی) یافته می‌شوند: THICK_INNER؛ اگر روی کمان مرز رویه و دیوارهٔ سکو باشد PAD_SEAM (جدا، چون در همهٔ سکوها یکسان است). خط داخلی خیلی نازک (< ۱٫۸px، کمتر از حداقل خوانایی) هم: TOO_THIN.
خروجی در LINES_OUT (پیش‌فرض scratchpad/lines):
  <node>_lw.png     نقشهٔ رنگی ضخامت: آبی = خط دور بیرونی، سبز = داخلی نازک (درست)، زرد = مرز جزء، قرمز = داخلی هم‌اندازهٔ بیرونی (مشکوک)
  <node>.png        خود نماد (برای مقایسه)
  <node>_q0..q3.png چهار ربع بزرگ نماد
  <node>_l<n>.png   برش بزرگ دور هر یافته با دایرهٔ قرمز
  lines.json        یافته‌ها: نوع، جای وسط (px نقشه در برش)، طول، پهنای میانه و بیشینه
اجرا: python3 line_scan.py [F01 M03 ...]  (بدون آرگومان: هر ۳۴ ایستگاه). فقط می‌خواند؛ چیزی عوض نمی‌شود."""
import sys, os, json, pathlib, io
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import skeletonize
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
MAP = HERE.parent.parent / 'index.html'
OUTDIR = pathlib.Path(os.environ.get('LINES_OUT', '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/lines'))
D = 6
PAD = 16
OUTER_ZONE = 6.2      # px نقشه از زمینه: نوار خط دور بیرونی
THICK = 4.8           # px نقشه: از این پهن‌تر = هم‌اندازهٔ خط دور بیرونی
PART = 3.4            # px نقشه: مرز نازک/جزء
THIN = 1.8            # px نقشه: نازک‌تر از این خوانا نیست
NAVY = np.array([36, 26, 94])
HIDE = ('html,body,#page,#sc,#world{background:transparent!important}'
        '#world>:not(svg){display:none!important}#blk,#dv,#rv,#bar,#bot,#hud,#dock,#ov{display:none!important}'
        'svg.map *{visibility:hidden}')


def analyse(img, pad=None):
    """pad = (cx, cy, rx, ry) سکو در px نقشهٔ برش: خط مرز رویه و دیوارهٔ سکو (کمان پایین رویه) جدا گزارش می‌شود: PAD_SEAM."""
    arr = np.array(img).astype(int); A = arr[:, :, 3] > 150
    N = (np.abs(arr[:, :, :3] - NAVY).sum(2) < 60) & (arr[:, :, 3] > 200)
    dbg = ndi.distance_transform_edt(A) / D                      # فاصله تا زمینه (px نقشه)
    dN = ndi.distance_transform_edt(N) / D
    sk = skeletonize(N); width = 2 * dN * sk
    inner = sk & (dbg > OUTER_ZONE)
    out = []
    for kind, sel in (('THICK_INNER', inner & (width >= THICK)), ('TOO_THIN', inner & (width > 0) & (width < THIN))):
        lab, n = ndi.label(ndi.binary_dilation(sel, iterations=3))
        for k in range(1, n + 1):
            pts = sel & (lab == k); ys, xs = np.nonzero(pts)
            L = len(ys) / D
            if L < (3 if kind == 'THICK_INNER' else 4): continue
            w = width[pts]; kd = kind
            if pad and kind == 'THICK_INNER':
                cx, cy, rx, ry = pad; X = xs / D - cx; Y = ys / D - cy
                on = (np.abs(X) < rx) & (np.abs(Y - ry * np.sqrt(np.clip(1 - (X / rx) ** 2, 0, 1))) < 3.5)
                if on.mean() > .6: kd = 'PAD_SEAM'
            out.append(dict(kind=kd, x=round(xs.mean() / D, 1), y=round(ys.mean() / D, 1), length_px=round(L, 1),
                            w_median=round(float(np.median(w)), 2), w_max=round(float(w.max()), 2),
                            box=[round(xs.min() / D, 1), round(ys.min() / D, 1), round(xs.max() / D, 1), round(ys.max() / D, 1)]))
    # نقشهٔ رنگی ضخامت
    base = Image.new('RGBA', img.size, (235, 235, 235, 255)); base.alpha_composite(img)
    g = np.array(base.convert('L').convert('RGB')).astype(float); g = 255 - (255 - g) * .35
    col = np.zeros_like(g); m = ndi.binary_dilation(sk, iterations=max(1, D // 3))
    wd = ndi.grey_dilation(width, size=(2 * (D // 3) + 1,) * 2); dz = ndi.grey_dilation(dbg * sk, size=(2 * (D // 3) + 1,) * 2)
    cls = np.where(dz <= OUTER_ZONE, 0, np.where(wd >= THICK, 3, np.where(wd >= PART, 2, 1)))
    pal = {0: (40, 90, 230), 1: (20, 170, 60), 2: (240, 180, 0), 3: (230, 20, 20)}
    for c, rgb in pal.items(): col[m & (cls == c)] = rgb
    g[m] = col[m]
    return out, Image.fromarray(g.astype(np.uint8))


def crop(im, f, path):
    x0, y0, x1, y1 = f['box']; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = max(8, (x1 - x0) / 2 + 5, (y1 - y0) / 2 + 5)
    c = im.crop((int((cx - R) * D), int((cy - R) * D), int((cx + R) * D), int((cy + R) * D))).resize((360, 360), Image.LANCZOS)
    k = 360 / (2 * R); ImageDraw.Draw(c).ellipse((k * (x0 - cx + R) - 7, k * (y0 - cy + R) - 7, k * (x1 - cx + R) + 7, k * (y1 - cy + R) + 7), outline=(230, 0, 0), width=3)
    c.save(path)


def main():
    from playwright.sync_api import sync_playwright
    OUTDIR.mkdir(parents=True, exist_ok=True); res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=D)
        pg.goto(MAP.as_uri() + '#enter-M12'); pg.wait_for_timeout(3500)
        ids = sys.argv[1:] or pg.evaluate('ORDER')
        pg.add_style_tag(content=HIDE)
        for nid in ids:
            sel = '.node[data-id="%s"]' % nid
            css = pg.add_style_tag(content=sel + ',' + sel + ' *{visibility:visible!important}' + sel + ' [id$="_shadow"],' + sel + ' [id$="_lit"],' + sel + ' [id$="_shade"],' + sel + ' .under{visibility:hidden!important}')
            pg.evaluate("id=>{document.getElementById('sc').scrollTop=NODES[id].y-300}", nid); pg.wait_for_timeout(200)
            r = pg.evaluate("s=>{const e=document.querySelector(s).getBoundingClientRect();return [e.left,e.top,e.width,e.height]}", sel)
            x0 = max(0, r[0] - PAD); clip = {'x': x0, 'y': max(0, r[1] - PAD), 'width': min(390 - x0, r[2] + 2 * PAD), 'height': r[3] + 2 * PAD}
            img = Image.open(io.BytesIO(pg.screenshot(omit_background=True, clip=clip))).convert('RGBA')
            q = pg.evaluate("id=>{const n=NODES[id],w=document.getElementById('world').getBoundingClientRect();return [w.left+n.x,w.top+n.y,n.pad[0],n.pad[1]]}", nid)
            found, heat = analyse(img, (q[0] - clip['x'], q[1] - clip['y'], q[2], q[3]))
            bb = img.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox(); m_ = 3 * D
            bb = (max(0, bb[0] - m_), max(0, bb[1] - m_), min(img.width, bb[2] + m_), min(img.height, bb[3] + m_))
            flat = Image.new('RGBA', img.size, (205, 205, 205, 255)); flat.alpha_composite(img); flat = flat.convert('RGB')
            fc = flat.crop(bb); fc.resize((fc.width // 2, fc.height // 2), Image.LANCZOS).save(OUTDIR / (nid + '.png'))
            hc = heat.crop(bb); hc.resize((hc.width // 2, hc.height // 2), Image.LANCZOS).save(OUTDIR / (nid + '_lw.png'))
            W, H = fc.size
            for qi, (x, y) in enumerate(((0, 0), (W // 2, 0), (0, H // 2), (W // 2, H // 2))):
                fc.crop((x, y, x + W // 2 + 2 * D, y + H // 2 + 2 * D)).save(OUTDIR / ('%s_q%d.png' % (nid, qi)))
            for i, f in enumerate(found):
                f['img'] = '%s_l%d.png' % (nid, i); crop(flat, f, OUTDIR / f['img'])
            res[nid] = found
            print(nid, ' '.join('%s@%.0f,%.0f w%.1f L%.0f' % (f['kind'][:5], f['x'], f['y'], f['w_median'], f['length_px']) for f in found), flush=True)
            pg.evaluate("e=>e.remove()", css)
        b.close()
    (OUTDIR / 'lines.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
