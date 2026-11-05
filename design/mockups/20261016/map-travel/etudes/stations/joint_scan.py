#!/usr/bin/env python3
"""اسکن اتصال اجزای نمادهای نقشه، در خود نقشه و در طول حرکتشان (D196).
درخواست مالک ۴ نوامبر: «کابل اصلاً به جعبه متصل نیست»، «انتهای تیر با انتهای ستون مچ نیست» → عامل‌های symbol-joint-inspector و symbol-closeup-reviewer.

برای هر ایستگاه، ماکت نقشه (../../index.html#enter-M12) باز می‌شود، همه‌چیز جز همان نماد پنهان می‌شود (سایه/نور/زیرسایه هم)،
حرکت رسیدن ایستگاه پخش می‌شود و در ۴ ثانیه چند قاب با بزرگ‌نمایی ۶ گرفته می‌شود. در هر قاب:
  A_floating  تکهٔ ماتی که به بدنهٔ اصلی وصل نیست (جعبهٔ آویزانی که کابلش نمی‌رسد، قطعهٔ معلق)
  B_near_gap  دو تکهٔ جدا با شکاف کمتر از ~۲٫۴px نقشه (کابل یک‌ذره کوتاه، درز ریز)
  C_step      پله/زائدهٔ کوتاه و پُر روی لبه (۱ تا ۳px)، مثل سر تیری که از ستون کمی بیرون زده یا عقب مانده
یافته‌های نزدیک به هم در قاب‌های مختلف یکی می‌شوند (اولین قاب نگه داشته می‌شود).
خروجی در JOINTS_OUT (پیش‌فرض scratchpad/joints): <node>.png، <node>_q0..3.png (چهار ربع بزرگ برای بازبینی چشمی، حالت ایستا)،
<node>_f<n>.png (برش بزرگ دور هر یافته با دایرهٔ قرمز)، findings.json.
اجرا: python3 joint_scan.py [F01 M03 ...]   (بدون آرگومان: هر ۳۴ ایستگاه). فقط می‌خواند؛ هیچ فایل نمادی عوض نمی‌شود.
یافته «احتمال» است؛ تصمیم «ایراد واقعی یا عمدی» با بازبین چشمی است."""
import sys, os, json, pathlib, io, time
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
MAP = HERE.parent.parent / 'index.html'
OUTDIR = pathlib.Path(os.environ.get('JOINTS_OUT', '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/joints'))
D = 6            # پیکسل دستگاه به ازای هر پیکسل نقشه
PAD = 24         # حاشیه دور جعبهٔ نماد (px نقشه)
DUR = 4.0        # ثانیه‌های ضبط حرکت
HIDE = ('html,body,#page,#sc,#world{background:transparent!important}'
        '#world>:not(svg){display:none!important}#blk,#dv,#rv,#bar,#bot,#hud,#dock,#ov{display:none!important}'
        'svg.map *{visibility:hidden}')


def disk(r):
    yy, xx = np.ogrid[-r:r + 1, -r:r + 1]; return xx * xx + yy * yy <= r * r


def analyse(img):
    a = np.array(img)[:, :, 3] > 150
    lab, n = ndi.label(a); out = []
    if not n: return out
    sizes = ndi.sum(a, lab, range(1, n + 1)); main = int(np.argmax(sizes)) + 1
    dist_main = ndi.distance_transform_edt(lab != main)
    for k in range(1, n + 1):
        if k == main or sizes[k - 1] < (2 * D) ** 2: continue
        ys, xs = np.nonzero(lab == k)
        out.append(dict(kind='A_floating', x=xs.mean() / D, y=ys.mean() / D, gap_px=round(float(dist_main[ys, xs].min()) / D, 2),
                        box=[xs.min() / D, ys.min() / D, xs.max() / D, ys.max() / D]))
    closed = ndi.binary_closing(a, structure=disk(int(1.2 * D)))
    gl, m = ndi.label(closed & ~a)
    for k in range(1, m + 1):
        msk = gl == k; ys, xs = np.nonzero(msk)
        if len(ys) < D * D * .4: continue
        touched = set(np.unique(lab[ndi.binary_dilation(msk, iterations=2) & a])) - {0}
        if len(touched) >= 2:
            out.append(dict(kind='B_near_gap', x=xs.mean() / D, y=ys.mean() / D, box=[xs.min() / D, ys.min() / D, xs.max() / D, ys.max() / D]))
    opened = ndi.binary_opening(a, structure=disk(int(1.2 * D)))
    nl, q = ndi.label(a & ~opened)
    for k in range(1, q + 1):
        ys, xs = np.nonzero(nl == k); h, w = np.ptp(ys) + 1, np.ptp(xs) + 1
        if len(ys) < D * D * .8 or max(h, w) > 4 * D or len(ys) / (h * w) < .5: continue
        out.append(dict(kind='C_step', x=xs.mean() / D, y=ys.mean() / D, box=[xs.min() / D, ys.min() / D, xs.max() / D, ys.max() / D]))
    return out


def crop(img, f, path):
    x0, y0, x1, y1 = f['box']; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = max(9, (x1 - x0) / 2 + 6, (y1 - y0) / 2 + 6)
    bg = Image.new('RGBA', img.size, (205, 205, 205, 255)); bg.alpha_composite(img)
    c = bg.crop((int((cx - R) * D), int((cy - R) * D), int((cx + R) * D), int((cy + R) * D))).resize((360, 360), Image.LANCZOS)
    k = 360 / (2 * R); dr = ImageDraw.Draw(c)
    dr.ellipse((k * (x0 - cx + R) - 7, k * (y0 - cy + R) - 7, k * (x1 - cx + R) + 7, k * (y1 - cy + R) + 7), outline=(230, 0, 0), width=3)
    c.save(path)


def main():
    from playwright.sync_api import sync_playwright
    OUTDIR.mkdir(parents=True, exist_ok=True)
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=D)
        pg.goto(MAP.as_uri() + '#enter-M12'); pg.wait_for_timeout(3500)
        ids = sys.argv[1:] or pg.evaluate('ORDER')
        pg.add_style_tag(content=HIDE)
        for nid in ids:
            sel = '.node[data-id="%s"]' % nid
            css = pg.add_style_tag(content=sel + ',' + sel + ' *{visibility:visible!important}' + sel + ' [id$="_shadow"],' + sel + ' [id$="_lit"],' + sel + ' [id$="_shade"],' + sel + ' .under{visibility:hidden!important}')
            pg.evaluate("id=>{document.getElementById('sc').scrollTop=NODES[id].y-300}", nid); pg.wait_for_timeout(150)
            r = pg.evaluate("s=>{const e=document.querySelector(s).getBoundingClientRect();return [e.left,e.top,e.width,e.height]}", sel)
            x0 = max(0, r[0] - PAD); clip = {'x': x0, 'y': max(0, r[1] - PAD), 'width': min(390 - x0, r[2] + 2 * PAD), 'height': r[3] + 2 * PAD}
            frames = []
            pg.evaluate("id=>playStation(id)", nid); t0 = time.time()
            while time.time() - t0 < DUR:
                frames.append((round(time.time() - t0, 2), Image.open(io.BytesIO(pg.screenshot(omit_background=True, clip=clip))).convert('RGBA')))
            pg.wait_for_timeout(2500)
            rest = Image.open(io.BytesIO(pg.screenshot(omit_background=True, clip=clip))).convert('RGBA')
            frames.append(('rest', rest))
            # تصویرهای بازبین چشمی: کل نماد، چهار ربعِ جعبهٔ واقعیِ نماد (بزرگ)، و نوار ۸ قاب حرکت
            def flat(im):
                g_ = Image.new('RGBA', im.size, (205, 205, 205, 255)); g_.alpha_composite(im); return g_.convert('RGB')
            bb = None
            for _, im in frames:
                q_ = im.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
                if q_: bb = q_ if bb is None else (min(bb[0], q_[0]), min(bb[1], q_[1]), max(bb[2], q_[2]), max(bb[3], q_[3]))
            m_ = 3 * D; bb = (max(0, bb[0] - m_), max(0, bb[1] - m_), min(rest.width, bb[2] + m_), min(rest.height, bb[3] + m_))
            bg = flat(rest).crop(bb); bg.resize((bg.width // 2, bg.height // 2), Image.LANCZOS).save(OUTDIR / (nid + '.png'))
            W, H = bg.size
            for qi, (x, y) in enumerate(((0, 0), (W // 2, 0), (0, H // 2), (W // 2, H // 2))):
                bg.crop((x, y, x + W // 2 + 2 * D, y + H // 2 + 2 * D)).save(OUTDIR / ('%s_q%d.png' % (nid, qi)))
            pick = [frames[int(i * (len(frames) - 2) / 7)] for i in range(8)]
            hh = 300; tiles = [flat(im).crop(bb) for _, im in pick]; tiles = [t_.resize((int(t_.width * hh / t_.height), hh), Image.LANCZOS) for t_ in tiles]
            strip = Image.new('RGB', (sum(t_.width for t_ in tiles) + 6 * 7, hh), 'white'); x_ = 0
            for t_ in tiles: strip.paste(t_, (x_, 0)); x_ += t_.width + 6
            strip.save(OUTDIR / (nid + '_anim.png'))
            found = []
            for t, img in frames:
                for f in analyse(img):
                    if any(g['kind'] == f['kind'] and abs(g['x'] - f['x']) < 3 and abs(g['y'] - f['y']) < 3 for g in found): continue
                    f['t'] = t; f['img'] = '%s_f%d.png' % (nid, len(found)); crop(img, f, OUTDIR / f['img'])
                    for k_, v_ in list(f.items()):
                        if isinstance(v_, float): f[k_] = round(v_, 1)
                    f['box'] = [round(float(v), 1) for v in f['box']]
                    found.append(f)
            res[nid] = dict(frames=len(frames), findings=found)
            print(nid, len(frames), 'frames;', ' '.join('%s@%.0f,%.0f(t=%s)' % (f['kind'][0], f['x'], f['y'], f['t']) for f in found), flush=True)
            pg.evaluate("e=>e.remove()", css)
        b.close()
    (OUTDIR / 'findings.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
