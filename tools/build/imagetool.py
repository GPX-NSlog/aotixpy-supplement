"""纯 Python 的 PNG 裁剪/缩放工具（无 PIL 环境下的替代方案）。

支持 8bit 的灰度 / 灰度+alpha / RGB / RGBA / 调色板（非交错）PNG。
只做两件事：按像素矩形裁剪 + 面积平均缩放 + 重新编码。
"""
import struct
import sys
import zlib


def read_png(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', 'not a png'
    pos = 8
    idat = bytearray()
    palette = None
    trns = None
    while pos < len(data):
        (length,) = struct.unpack('>I', data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b'IHDR':
            w, h, depth, color, comp, filt, inter = struct.unpack('>IIBBBBB', chunk)
            assert depth == 8 and comp == 0 and filt == 0 and inter == 0, \
                'unsupported png format: depth=%s color=%s interlace=%s' % (depth, color, inter)
        elif ctype == b'PLTE':
            palette = chunk
        elif ctype == b'tRNS':
            trns = chunk
        elif ctype == b'IDAT':
            idat += chunk
        elif ctype == b'IEND':
            break
    raw = zlib.decompress(bytes(idat))
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
    bpp = channels
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif f == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        elif f != 0:
            raise ValueError('bad filter %d' % f)
        out[y * stride:(y + 1) * stride] = line
        prev = line

    # 统一转成 RGB 三元组列表的二维数组
    px = []
    for y in range(h):
        row = []
        base = y * stride
        for x in range(w):
            o = base + x * bpp
            if color == 2:
                row.append((out[o], out[o + 1], out[o + 2]))
            elif color == 6:
                row.append((out[o], out[o + 1], out[o + 2]))
            elif color == 0:
                v = out[o]
                row.append((v, v, v))
            elif color == 4:
                v = out[o]
                row.append((v, v, v))
            else:  # palette
                i = out[o] * 3
                row.append((palette[i], palette[i + 1], palette[i + 2]))
        px.append(row)
    return px


def crop(px, box):
    x0, y0, x1, y1 = box
    return [row[x0:x1] for row in px[y0:y1]]


def resize(px, size):
    """面积平均缩放（box filter），缩小时质量好于最近邻。"""
    h = len(px)
    w = len(px[0])
    out = []
    for ty in range(size):
        sy0 = ty * h / size
        sy1 = (ty + 1) * h / size
        y_lo, y_hi = int(sy0), min(h, int(-(-sy1 // 1)))
        row = []
        for tx in range(size):
            sx0 = tx * w / size
            sx1 = (tx + 1) * w / size
            x_lo, x_hi = int(sx0), min(w, int(-(-sx1 // 1)))
            r = g = b = 0
            n = 0
            for y in range(y_lo, y_hi):
                for x in range(tx * 0 + x_lo, x_hi):
                    p = px[y][x]
                    r += p[0]
                    g += p[1]
                    b += p[2]
                    n += 1
            row.append((r // n, g // n, b // n))
        out.append(row)
    return out


def _chunk(t, d):
    return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)


def write_png(path, px, level=9):
    h = len(px)
    w = len(px[0])
    raw = bytearray()
    for row in px:
        raw.append(0)
        for p in row:
            raw += bytes(p)
    png = b'\x89PNG\r\n\x1a\n'
    png += _chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
    png += _chunk(b'IDAT', zlib.compress(bytes(raw), level))
    png += _chunk(b'IEND', b'')
    open(path, 'wb').write(png)


def median_cut(px, ncolors=256, bits=5):
    """按出现频率做 median cut 量化，返回调色板（列表 RGB）。"""
    shift = 8 - bits
    hist = {}
    for row in px:
        for (r, g, b) in row:
            k = ((r >> shift) << (2 * bits)) | ((g >> shift) << bits) | (b >> shift)
            hist[k] = hist.get(k, 0) + 1
    boxes = [list(hist.items())]

    def box_range(box):
        lo = [1 << bits] * 3
        hi = [-1] * 3
        for k, _ in box:
            ch = ((k >> (2 * bits)) & ((1 << bits) - 1),
                  (k >> bits) & ((1 << bits) - 1),
                  k & ((1 << bits) - 1))
            for i in range(3):
                lo[i] = min(lo[i], ch[i])
                hi[i] = max(hi[i], ch[i])
        return lo, hi

    while len(boxes) < ncolors:
        best = None
        best_score = -1
        for i, box in enumerate(boxes):
            if len(box) < 2:
                continue
            lo, hi = box_range(box)
            span = [hi[j] - lo[j] for j in range(3)]
            axis = span.index(max(span))
            pop = sum(c for _, c in box)
            score = max(span) * pop
            if score > best_score:
                best_score = score
                best = (i, axis)
        if best is None:
            break
        i, axis = best
        box = sorted(boxes[i], key=lambda kv: (kv[0] >> ((2 - axis) * bits)) & ((1 << bits) - 1))
        total = sum(c for _, c in box)
        acc = 0
        cut = len(box) // 2
        for j, (_, c) in enumerate(box):
            acc += c
            if acc >= total / 2:
                cut = max(1, min(len(box) - 1, j))
                break
        boxes[i:i + 1] = [box[:cut], box[cut:]]

    pal = []
    for box in boxes:
        tr = tg = tb = tw = 0
        for k, c in box:
            ch = ((k >> (2 * bits)) & ((1 << bits) - 1),
                  (k >> bits) & ((1 << bits) - 1),
                  k & ((1 << bits) - 1))
            tr += ch[0] * c
            tg += ch[1] * c
            tb += ch[2] * c
            tw += c
        if tw == 0:
            continue
        # 还原到 8bit：取桶中心
        step = 1 << shift
        pal.append((min(255, (tr // tw) * step + step // 2),
                    min(255, (tg // tw) * step + step // 2),
                    min(255, (tb // tw) * step + step // 2)))
    return pal


def write_palette_png(path, px, level=9, dither=True):
    """量化成 256 色调色板 PNG，体积远小于真彩 PNG。"""
    h = len(px)
    w = len(px[0])
    pal = median_cut(px, 256)
    idx = [[0] * w for _ in range(h)]
    cache = {}

    def nearest(p):
        key = (p[0] >> 2, p[1] >> 2, p[2] >> 2)
        v = cache.get(key)
        if v is None:
            best = 0
            bd = 1 << 30
            for i, q in enumerate(pal):
                dr = p[0] - q[0]
                dg = p[1] - q[1]
                db = p[2] - q[2]
                d = dr * dr + dg * dg + db * db
                if d < bd:
                    bd = d
                    best = i
            cache[key] = v = best
        return v

    cur = [[list(p) for p in row] for row in px]
    for y in range(h):
        for x in range(w):
            p = cur[y][x]
            p = (max(0, min(255, int(p[0]))), max(0, min(255, int(p[1]))), max(0, min(255, int(p[2]))))
            i = nearest(p)
            idx[y][x] = i
            if dither:
                q = pal[i]
                er, eg, eb = p[0] - q[0], p[1] - q[1], p[2] - q[2]
                for dx, dy, f in ((1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and ny < h:
                        t = cur[ny][nx]
                        t[0] += er * f / 16.0
                        t[1] += eg * f / 16.0
                        t[2] += eb * f / 16.0

    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += bytes(idx[y])
    plte = bytearray()
    for p in pal:
        plte += bytes(p)
    png = b'\x89PNG\r\n\x1a\n'
    png += _chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 3, 0, 0, 0))
    png += _chunk(b'PLTE', bytes(plte))
    png += _chunk(b'IDAT', zlib.compress(bytes(raw), level))
    png += _chunk(b'IEND', b'')
    open(path, 'wb').write(png)


if __name__ == '__main__':
    src, dst, size, l, t, r, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), *map(int, sys.argv[4:8])
    px = read_png(src)
    H, W = len(px), len(px[0])
    print('src %dx%d' % (W, H))
    px = crop(px, (l, t, r, b))
    print('crop -> %dx%d' % (len(px[0]), len(px)))
    px = resize(px, size)
    write_png(dst, px)
    import os
    print('out %dx%d %.1f KB' % (size, size, os.path.getsize(dst) / 1024))
