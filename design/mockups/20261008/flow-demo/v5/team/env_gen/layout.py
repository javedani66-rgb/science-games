# چینش ۳۴ گره روی بوم عمودی (منبع واحد برای node_map/slots/env_sheet)
import json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'assets' / 'env'
W = 390
ORDER = ['F01','F02','F03','F04','F06','F07','F08','F09','W01','W02','F05','W03','W04','E01','E02','E07','M01','B01','B02','M04','M05','M06','E05','M03','M09','M10','E03','M02','M07','M08','M11','E06','E04','M12']
ZONE = {}
for i, k in enumerate(ORDER):
    ZONE[k] = 'sports' if i < 8 else 'space' if i < 13 else 'farm' if i < 16 else 'city'
# گره ← بنای شاخص (node_NN) یا پروپ (prop_NN)
LAND = {'F01':3,'F06':2,'W02':4,'F05':5,'W04':6,'E01':8,'M04':7,'M03':1,'M09':9,'M07':10,'M11':11,'M08':12}
PROP = {'F02':9,'F03':10,'F04':12,'F07':1,'F08':6,'F09':7,'W01':2,'W03':8,'E02':5,'E07':11,'M01':16,'B01':7,'B02':2,'M05':7,'M06':13,'E05':13,'M10':14,'E03':3,'M02':5,'E06':4,'E04':15}
# شعاع پایه (rx, ry) و ارتفاع سیلوئت بالای مرکز پایه (h)
LRX = {1:(70,24,78),2:(80,27,112),3:(84,28,124),4:(56,19,100),5:(58,20,118),6:(76,26,116),7:(64,22,86),8:(66,23,128),9:(52,18,104),10:(54,19,132),11:(82,28,124),12:(84,28,132)}
PRX = {1:(36,12,40),2:(36,12,44),3:(38,13,40),4:(34,12,44),5:(38,13,44),6:(38,13,38),7:(40,13,36),8:(34,12,64),9:(36,12,64),10:(36,12,62),11:(36,12,58),12:(36,12,48),13:(36,12,44),14:(34,12,40),15:(36,12,104),16:(44,14,72)}
HARD_X = set(range(26, 32))   # گذرگاه بندر: مسیر راست‌گرا
def build():
    nodes = []
    for p, k in enumerate(ORDER):
        if k in LAND: kind, n = 'landmark', LAND[k]; rx, ry, h = LRX[n]; asset = 'node_%02d' % n
        elif k in PROP: kind, n = 'prop', PROP[k]; rx, ry, h = PRX[n]; asset = 'prop_%02d' % n
        else: kind, n = 'landmark', 11; rx, ry, h = LRX[11]; asset = 'node_11'   # M12 پنهان
        nodes.append(dict(id=k, p=p, zone=ZONE[k], kind=kind, n=n, asset=asset, rx=rx, ry=ry, h=h))
    # y از پایین
    gap = lambda a, b: 190 if (a['kind'] == 'landmark' and b['kind'] == 'landmark' and a['h'] > 110 and b['h'] > 110) else 160 if (a['kind'] == 'landmark' or b['kind'] == 'landmark') and (a['h'] > 90 or b['h'] > 90) else 132
    y = None
    for i, nd in enumerate(nodes):
        if i == 0: nd['_y'] = 0
        else: nd['_y'] = nodes[i-1]['_y'] - gap(nodes[i-1], nd)
    TOP = 470; BOT = 330
    miny = min(n['_y'] for n in nodes); Hh = int(-miny + TOP + BOT)
    for i, nd in enumerate(nodes):
        nd['cy'] = round(nd['_y'] - miny + TOP)
        left = i % 2 == 0
        xl, xr = (168, 286) if i in HARD_X else (118, 272)
        j = [0, 12, -10, 16, -14, 8, -6, 14][i % 8]
        x = (xl if left else xr) + j
        x = max(nd['rx'] + 26, min(W - nd['rx'] - 26, x))
        nd['cx'] = round(x)
        del nd['_y']
    return nodes, Hh
NODES, H = build()
START = (NODES[0]['cx'] + 10, NODES[0]['cy'] + 205)
def zone_bounds():
    b = {}
    for z in ('sports', 'space', 'farm', 'city'):
        ys = [n['cy'] for n in NODES if n['zone'] == z]; b[z] = (min(ys), max(ys))
    # مرز = میانگین آخرین گرهٔ پایین‌تر و اولین گرهٔ بالاتر
    order = ['city', 'farm', 'space', 'sports']      # از بالا به پایین
    bounds = {}; top = 0
    for i, z in enumerate(order):
        if i < 3:
            nxt = order[i+1]; bot = round((b[z][1] + b[nxt][0]) / 2)
        else: bot = H
        bounds[z] = (top, bot); top = bot
    return bounds
ZB = zone_bounds()
def path_pts():
    pts = [START] + [(n['cx'], n['cy']) for n in NODES[:33]]   # M12 پنهان در مسیر نیست
    return pts
def path_d(pts):
    # Catmull-Rom → bezier
    d = 'M%.1f,%.1f' % pts[0]; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*c1, *c2, *p2)
    return d
def path_samples(pts, n=14):
    P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for s in range(n):
            t = s / n
            f = lambda a, b, c, d: .5 * ((2*b) + (-a + c) * t + (2*a - 5*b + 4*c - d) * t*t + (-a + 3*b - 3*c + d) * t**3)
            out.append((f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])))
    out.append(pts[-1]); return out
def slots():
    S = {}
    for n in NODES:
        cx, cy, rx, ry, h = n['cx'], n['cy'], n['rx'], n['ry'], n['h']
        S[n['id']] = dict(
            asset=n['asset'], zone=n['zone'], base_center=[cx, cy], base_rx=rx, base_ry=ry, silhouette_h=h,
            place_at=[cx - (100 if n['kind'] == 'landmark' else 60), cy - (150 if n['kind'] == 'landmark' else 78)],
            hit_box=[cx - max(48, rx), cy - max(48, int(h * .7)), 2 * max(48, rx), max(96, int(h * .7) + ry + 8)],
            difficulty_pill_center=[cx + rx - 4, cy - h - 4], difficulty_corner='top-start (راست در RTL)',
            lock_done_center=[cx + int(rx * .72), cy + int(ry * .9) + 8], lock_done_corner='bottom-start (راست-پایین)',
            b1_foot=[cx, cy + int(ry * .55)], label_slot_center=[cx, cy + ry + 44], label_note='پلاک رابط (UI)؛ ≥8px از مسیر')
    return S
if __name__ == '__main__':
    print(H, ZB, len(NODES))
    for n in NODES: print(n['p'], n['id'], n['zone'], n['asset'], n['cx'], n['cy'])
def path_seg_d(pts, a, b):
    """بخشی از مسیر از اندیس a تا b (همان Catmull-Rom مسیر کامل)"""
    P = [pts[0]] + pts + [pts[-1]]; d = 'M%.1f,%.1f' % pts[a]
    for i in range(a + 1, b + 1):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*c1, *c2, *p2)
    return d
