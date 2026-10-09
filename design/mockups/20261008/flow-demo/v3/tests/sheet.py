import sys, pathlib
from PIL import Image
S = pathlib.Path(__file__).resolve().parents[1] / 'shots'
tag, size, names, out = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4]
ims = [Image.open(next(S.glob(f'{tag}_{size}_{n}*.png'))) for n in names]
W = sum(i.width for i in ims) + 8 * (len(ims) - 1); H = max(i.height for i in ims)
c = Image.new('RGB', (W, H), (60, 60, 60)); x = 0
for i in ims: c.paste(i, (x, 0)); x += i.width + 8
c.save(out)
