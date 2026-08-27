"""Quita el rótulo 'OUTLET' quemado en las fotos de producto de tienda.drdsll.com.

El rótulo es una isla de píxeles amarillo/naranja saturados sobre fondo blanco,
separada del producto. Se localizan las componentes conexas de tinta y se borran
las que son mayoritariamente amarillo-naranja y viven en la mitad inferior.
"""
import sys, os, glob
from collections import deque
import numpy as np
from PIL import Image

def analyse(path, out_path, report):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    H, W, _ = a.shape
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

    mx = a.max(axis=2)
    mn = a.min(axis=2)
    sat = mx - mn                      # saturación cruda 0..255
    ink = ~((R > 236) & (G > 236) & (B > 236))   # cualquier cosa que no sea blanco

    # amarillo/naranja/rojo brillante y muy saturado -> color del rótulo
    warm = (sat > 70) & (R > 150) & (R >= G) & (G >= B) & (B < 140)
    bright_warm = warm & (mx > 180)

    lab = -np.ones((H, W), dtype=np.int32)
    comps = []
    ink_l = ink.tolist()
    bw_l = bright_warm.tolist()
    lab_l = lab.tolist()

    cid = 0
    for y0 in range(H):
        row = ink_l[y0]
        for x0 in range(W):
            if not row[x0] or lab_l[y0][x0] != -1:
                continue
            q = deque([(y0, x0)])
            lab_l[y0][x0] = cid
            n = 0; nwarm = 0
            miny = maxy = y0; minx = maxx = x0
            while q:
                y, x = q.popleft()
                n += 1
                if bw_l[y][x]:
                    nwarm += 1
                if y < miny: miny = y
                if y > maxy: maxy = y
                if x < minx: minx = x
                if x > maxx: maxx = x
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < H and 0 <= nx < W and ink_l[ny][nx] and lab_l[ny][nx] == -1:
                        lab_l[ny][nx] = cid
                        q.append((ny, nx))
            comps.append(dict(id=cid, n=n, warm=nwarm/max(n,1),
                              box=(minx, miny, maxx, maxy)))
            cid += 1

    lab = np.array(lab_l, dtype=np.int32)
    out = a.copy()
    killed = []
    for c in comps:
        x0, y0, x1, y1 = c['box']
        h = y1 - y0 + 1
        w = x1 - x0 + 1
        # criterios del rótulo: cálido dominante, en la mitad inferior,
        # letra de tamaño razonable, no es el producto entero
        if (c['warm'] > 0.55 and c['n'] > 60
                and y0 > H * 0.45
                and h < H * 0.28 and w < W * 0.55):
            out[lab == c['id']] = 255
            killed.append(c)

    # el halo del JPEG deja fragmentos pálidos alrededor del rótulo; se borran
    # sólo las componentes que caen enteras dentro de la caja del rótulo, para
    # no tocar nunca el producto
    pad = 14
    report_extra = []
    for k in killed:
        kx0, ky0, kx1, ky1 = k['box']
        kx0 -= pad; ky0 -= pad; kx1 += pad; ky1 += pad
        for c in comps:
            if c is k or c['id'] in [z['id'] for z in killed]:
                continue
            x0, y0, x1, y1 = c['box']
            if x0 >= kx0 and y0 >= ky0 and x1 <= kx1 and y1 <= ky1:
                out[lab == c['id']] = 255
                report_extra.append(c['n'])

    # el halo mas palido ni siquiera cuenta como tinta: dentro de la caja del
    # rotulo se blanquea todo lo claro, que ahi nunca es producto
    pale = 0
    for k in killed:
        kx0, ky0, kx1, ky1 = k['box']
        kx0 = max(0, kx0 - 18); ky0 = max(0, ky0 - 18)
        kx1 = min(W - 1, kx1 + 18); ky1 = min(H - 1, ky1 + 18)
        sub = out[ky0:ky1+1, kx0:kx1+1]
        m = sub.min(axis=2) > 198
        pale += int(m.sum())
        sub[m] = 255

    Image.fromarray(out.astype(np.uint8)).save(out_path, quality=92, subsampling=0)
    report.append((os.path.basename(path), len(comps), len(killed),
                   sum(c['n'] for c in killed), len(report_extra)))

if __name__ == '__main__':
    src_dir, dst_dir = sys.argv[1], sys.argv[2]
    os.makedirs(dst_dir, exist_ok=True)
    rep = []
    for f in sorted(glob.glob(os.path.join(src_dir, '*.jpg'))):
        if 'logo' in os.path.basename(f):
            continue
        analyse(f, os.path.join(dst_dir, os.path.basename(f)), rep)
    for name, ncomp, nk, npx, ng in rep:
        print('%-52s comps=%-4d rotulo=%-3d px=%-7d fantasmas=%d' % (name, ncomp, nk, npx, ng))
