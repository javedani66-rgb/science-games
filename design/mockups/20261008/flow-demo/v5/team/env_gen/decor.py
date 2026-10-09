# تزئین هر زمین (کلاه خودش) + دروازهٔ شروع + کاشی‌های منو + بنر اسکله
from shapes import *
from buildings import *
import buildings as X
LN = 'var(--l-line,#241a5e)'
def D(name, fn, vb, ox, oy, rx, ry, bbox, win=False):
    b = B('env_dec_' + name); fn(b); return b.svg(vb, ox, oy, rx, ry, bbox, win)
# ورزشگاه
def d_cone(b): b.poly([(-10, 0), (10, 0), (0, -26)], PK, 2.6); b.rect(-13, -3, 26, 6, '#fff', 2.6, 2); b.line(-4, -14, 4, -14, '#fff', 1.2)
def d_hedge(b): b.path('M-34,0 Q-38,-14 -22,-16 Q-20,-28 -4,-22 Q10,-30 20,-18 Q38,-18 34,0Z', '#66993b', 2.6); b.line(-14, -8, -6, -14, '#a6d86a', 1.2)
def d_bench(b): b.rect(-30, -22, 60, 8, WD, 2.6, 2); b.rect(-26, -14, 6, 14, WD2, 2.6, 1); b.rect(20, -14, 6, 14, WD2, 2.6, 1); b.rect(-30, -34, 60, 8, WD, 2.6, 2)
def d_goal(b): b.rect(-30, -34, 4, 34, '#fff', 2.6, 1); b.rect(26, -34, 4, 34, '#fff', 2.6, 1); b.rect(-30, -38, 60, 5, '#fff', 2.6, 1); b.path('M-26,-33 L26,-33 M-26,-22 L26,-22 M-26,-11 L26,-11 M-13,-33 V0 M0,-33 V0 M13,-33 V0', 'none', 1.2, clip=False)
def d_hurdle(b): b.rect(-24, -22, 48, 8, '#fff', 2.6, 2); b.rect(-24, -14, 5, 14, ST2, 2.6, 1); b.rect(19, -14, 5, 14, ST2, 2.6, 1); b.rect(-10, -22, 20, 8, PK, 0, 1)
def d_stand(b):
    for i in range(3): b.rect(-34 + i * 6, -12 - i * 10, 68 - i * 12, 10, [BL, '#7fb3ea', '#a9cdf2'][i], 2.6, 2)
def d_lamp(b): b.rect(-3, -46, 6, 46, ST2, 2.6, 1); b.rect(-14, -58, 28, 14, CR, 2.6, 3); b.window(-11, -55, 22, 8)
def d_flags(b):
    for x, c in ((-14, PK), (6, BL)): b.rect(x - 1.5, -44, 3, 44, ST, 2.6, 1); b.poly([(x + 1.5, -44), (x + 18, -38), (x + 1.5, -32)], c, 2.6)
# فضا
def d_crater(b): b.ell(0, 0, 24, 8, '#5c459c', 1.2); b.ell(2, 2, 17, 5, '#44306e', 0); b.path('M-24,0 Q0,-6 24,0', 'none', 1.2, clip=False)
def d_rock(b): b.poly([(-16, 0), (-20, -12), (-8, -24), (8, -20), (20, -6), (16, 0)], '#9a7ee0', 2.6); b.poly([(-8, -24), (8, -20), (2, -8)], '#b9a3f0', 0); b.line(-4, -14, 4, -4, '#5c459c', 1.2)
def d_rock2(b): b.poly([(-12, 0), (-10, -14), (4, -18), (14, -4), (10, 0)], '#7a5cd0', 2.6); b.poly([(4, -18), (14, -4), (4, -6)], '#9a7ee0', 0)
def d_anten(b): b.line(0, 0, 0, -50, LN, 4.5); b.line(0, -50, 0, -50, LN, 1); b.circ(0, -54, 5, PK, 2.6); b.line(-14, -10, 0, -36, LN, 2.6); b.line(14, -10, 0, -36, LN, 2.6)
def d_dome(b): b.path('M-18,0 a18,20 0 0 1 36,0z', ST, 2.6); b.wcirc(0, -10, 4); b.circ(0, -10, 4, '#9fdcf2', 2.6)
def d_solar(b): b.poly([(-26, -6), (22, -6), (30, -28), (-18, -28)], BL, 2.6); b.line(-22, -17, 26, -17, '#a9cdf2', 1.2); b.line(-6, -28, -10, -6, '#a9cdf2', 1.2); b.line(10, -28, 8, -6, '#a9cdf2', 1.2); b.line(-4, -6, -4, 0, LN, 2.6)
def d_star(b): b.poly([(0, -14), (3, -4), (13, 0), (3, 4), (0, 14), (-3, 4), (-13, 0), (-3, -4)], '#fff', 0)
def d_ufo(b): b.ell(0, -12, 20, 7, ST2, 2.6); b.path('M-10,-14 a10,10 0 0 1 20,0z', '#9fdcf2', 2.6)
# مزرعه
def d_wheat(b):
    for x in (-18, -9, 0, 9, 18): b.line(x, 0, x, -26, '#aba16e', 1.2); b.ell(x, -28, 3.2, 7, '#e8c64a', 1.2)
def d_fence(b):
    for x in (-30, -10, 10, 30): b.rect(x - 3, -26, 6, 26, WD, 2.6, 1)
    b.rect(-34, -22, 68, 5, WD2, 2.6, 1); b.rect(-34, -10, 68, 5, WD2, 2.6, 1)
def d_bale(b): b.rect(-20, -26, 40, 26, '#e8c64a', 2.6, 8); b.line(-20, -17, 20, -17, '#aba16e', 1.2); b.line(-20, -9, 20, -9, '#aba16e', 1.2); b.line(-6, -26, -6, 0, WD2, 1.2); b.line(6, -26, 6, 0, WD2, 1.2)
def d_scare(b): b.line(0, 0, 0, -48, WD2, 4.5); b.line(-20, -34, 20, -34, WD2, 4.5); b.circ(0, -52, 9, '#e8c64a', 2.6); b.poly([(-12, -58), (12, -58), (0, -74)], VI, 2.6); b.rect(-6, -40, 12, 14, BL, 2.6, 2)
def d_haycone(b): b.poly([(-20, 0), (20, 0), (0, -44)], '#e8c64a', 2.6); b.line(-12, -14, 12, -14, '#aba16e', 1.2); b.line(-6, -28, 6, -28, '#aba16e', 1.2)
def d_trough(b): b.rect(-26, -14, 52, 14, WD, 2.6, 3); b.ell(0, -14, 24, 4, '#3fb6e0', 1.2)
def d_sunf(b): b.line(0, 0, 0, -30, '#66993b', 2.6); b.circ(0, -34, 9, '#e8c64a', 2.6); b.circ(0, -34, 4, WD2, 0)
def d_bucket(b): b.poly([(-10, -20), (10, -20), (8, 0), (-8, 0)], ST2, 2.6); b.path('M-9,-20 Q0,-36 9,-20', 'none', 2.6, clip=False)
# شهر
def d_low(b): b.rect(-26, -30, 52, 30, '#8aa0b8', 2.6, 2); b.rect(-26, -34, 52, 6, '#5f7694', 2.6, 2); b.window(-18, -22, 10, 8); b.window(0, -22, 10, 8); b.rect(14, -16, 8, 16, DV, 2.6, 1)
def d_mid(b): b.rect(-20, -56, 40, 56, '#7a93ae', 2.6, 2); b.rect(-24, -60, 48, 6, '#44566c', 2.6, 2); [b.window(x, y, 8, 8) for x in (-12, 4) for y in (-48, -32, -16)]
def d_slamp(b): b.line(0, 0, 0, -44, LN, 4.5); b.path('M0,-44 q10,-6 18,0', 'none', 4.5, clip=False); b.circ(18, -42, 4, CR, 2.6); b.wcirc(18, -42, 4)
def d_rail(b):
    b.rect(-34, -6, 68, 4, ST2, 2.6, 1); b.rect(-34, -16, 68, 4, ST2, 2.6, 1)
    for x in (-26, -10, 6, 22): b.rect(x, -20, 6, 24, WD, 2.6, 1)
def d_barrels(b):
    for x, y in ((-12, 0), (12, 0), (0, -18)): b.rect(x - 9, y - 20, 18, 20, BL, 2.6, 5); b.line(x - 9, y - 12, x + 9, y - 12, '#a9cdf2', 1.2)
def d_truck_box(b): b.rect(-30, -26, 40, 22, CR, 2.6, 3); b.rect(10, -20, 20, 16, VI, 2.6, 3); b.circ(-18, -4, 6, DV, 2.6); b.circ(20, -4, 6, DV, 2.6); b.window(16, -17, 10, 6)
def d_truck_crane(b): b.rect(-30, -18, 52, 12, WD, 2.6, 2); b.rect(14, -30, 18, 22, TL, 2.6, 3); b.window(18, -26, 10, 7); b.circ(-20, -4, 6, DV, 2.6); b.circ(24, -4, 6, DV, 2.6); b.line(-22, -18, -8, -52, 'var(--l-line,#241a5e)', 6); b.line(-22, -18, -8, -52, PK, 2.6); b.line(-8, -52, -8, -34, 'var(--l-line,#241a5e)', 1.2); b.rect(-13, -34, 10, 8, WD2, 2.6, 1)
def d_forklift(b): b.rect(-10, -22, 26, 18, '#fff4d2', 2.6, 3); b.rect(-6, -34, 18, 12, BL, 2.6, 3); b.rect(-24, -48, 5, 46, ST2, 2.6, 1); b.rect(-30, -20, 22, 5, ST2, 2.6, 1); b.circ(-2, -4, 5, DV, 2.6); b.circ(12, -4, 5, DV, 2.6)
def d_tank(b): b.rect(-20, -34, 40, 34, ST, 2.6, 6); b.ell(0, -34, 20, 6, ST2, 2.6); b.line(-20, -20, 20, -20, ST2, 1.2); b.rect(-4, -48, 8, 14, ST2, 2.6, 1)
SET = {
 'sports': [('cone', d_cone, 34), ('hedge', d_hedge, 40), ('bench', d_bench, 36), ('goal', d_goal, 40), ('hurdle', d_hurdle, 30), ('stand', d_stand, 40), ('lamp', d_lamp, 24), ('flags', d_flags, 30)],
 'space': [('crater', d_crater, 30), ('rock', d_rock, 24), ('rock2', d_rock2, 20), ('anten', d_anten, 22), ('dome', d_dome, 22), ('solar', d_solar, 34), ('star', d_star, 16), ('ufo', d_ufo, 24)],
 'farm': [('wheat', d_wheat, 24), ('fence', d_fence, 38), ('bale', d_bale, 24), ('scare', d_scare, 24), ('haycone', d_haycone, 24), ('trough', d_trough, 30), ('sunf', d_sunf, 14), ('bucket', d_bucket, 14)],
 'city': [('low', d_low, 30), ('mid', d_mid, 28), ('slamp', d_slamp, 22), ('rail', d_rail, 38), ('barrels', d_barrels, 26), ('truck_box', d_truck_box, 36), ('truck_crane', d_truck_crane, 38), ('forklift', d_forklift, 30), ('tank', d_tank, 26)],
}
def decor_svgs():
    out = {}
    for z, items in SET.items():
        for name, fn, rx in items:
            n = z + '_' + name; out['dec_' + n] = D(n, fn, (120, 120), 60, 100, rx, 6, (-rx, -70, rx, 4), True)
    return out
# ---------- دروازهٔ شروع ----------
def start_gate():
    b = B('env_start_gate')
    b.rect(-72, -4, 12, 6, ST2, 2.6, 2); b.rect(60, -4, 12, 6, ST2, 2.6, 2)
    b.rect(-70, -92, 9, 90, ST, 4.5, 3); b.rect(61, -92, 9, 90, ST, 4.5, 3)
    b.rect(-80, -112, 160, 32, CR, 4.5, 10)
    for i in range(10):
        for j in range(2): b.rect(-76 + i * 15.2, -108 + j * 12, 7.6, 12, '#241a5e' if (i + j) % 2 == 0 else '#fff', 0, 0, clip=False)
    b.rect(-80, -112, 160, 32, 'none', 4.5, 10)
    return b.svg((170, 130), 85, 120, 76, 8, (-82, -114, 82, 4))
# ---------- کاشی‌های منو 160×(≥132) ----------
def tile_map():
    b = B('env_tile_map'); pad(b, 'sports', 66, 20); b.path('M-52,6 Q-26,-46 4,-34 Q30,-30 52,6Z', '#7fbf4a', 4.5)
    b.line(-30, -2, -18, -18, '#66993b', 1.2); b.line(14, -2, 24, -16, '#66993b', 1.2)
    b.rect(-2, -86, 5, 56, ST, 4.5, 2)
    for i in range(3):
        for j in range(2): b.rect(3 + i * 10, -86 + j * 10, 10, 10, '#241a5e' if (i + j) % 2 == 0 else '#fff', 0, 0, clip=False)
    b.rect(3, -86, 30, 20, 'none', 2.6, 2)
    return b.svg((160, 140), 80, 100, 62, 20, (-56, -90, 56, 20), False)
def tile_cards():
    b = B('env_tile_cards'); pad(b, 'city', 66, 21)
    b.rect(-46, -70, 92, 76, WD, 4.5, 4); b.rect(-40, -64, 80, 64, WD2, 2.6, 3); b.line(-40, -32, 40, -32, LN, 2.6)
    for i, c in enumerate((TL, PK, BL)): b.rect(-34 + i * 24, -58, 18, 24, c, 2.6, 3); b.rect(-34 + i * 24, -26, 18, 22, c, 2.6, 3)
    return b.svg((160, 140), 80, 100, 62, 20, (-56, -74, 56, 20), False)
def tile_practice():
    b = B('env_tile_practice'); pad(b, 'city', 66, 22)
    b.rect(-44, -44, 88, 48, WD, 4.5, 4); b.poly([(-44, -44), (44, -44), (52, -60), (-36, -60)], '#e0b070', 4.5); b.rect(-14, -32, 28, 8, CR, 2.6, 3)
    for i, c in enumerate((TL, PK, BL)): b.rect(-30 + i * 22, -78, 16, 26, c, 2.6, 3, rot=(-8 + i * 8, -22 + i * 22, -52))
    return b.svg((160, 140), 80, 100, 62, 20, (-56, -80, 56, 20), False)
def tile_guide():
    b = B('env_tile_guide'); pad(b, 'sports', 66, 23)
    b.rect(-34, -40, 68, 44, CR, 4.5, 4); b.poly([(-42, -40), (42, -40), (0, -80)], VI, 4.5)
    b.path('M-8,4 v-18 a8,8 0 0 1 16,0 v18z', TL, 2.6); b.rect(-28, -30, 14, 12, '#9fdcf2', 2.6, 2); b.rect(14, -30, 14, 12, '#9fdcf2', 2.6, 2)
    b.path('M-14,-62 a14,12 0 0 1 28,0z', CR, 2.6)
    return b.svg((160, 140), 80, 100, 62, 20, (-56, -84, 56, 20), False)
