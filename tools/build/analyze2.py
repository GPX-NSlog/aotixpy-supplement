#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按真实加载顺序（后者覆盖前者）计算 pY 词条的最终生效译文，识别实际仍显示英文的条目"""
import os, re, json, collections

WORK = os.path.dirname(os.path.abspath(__file__))
EN = os.path.join(WORK, 'en')
MODZH = os.path.join(WORK, 'modzh')
EXTRA = os.path.join(WORK, 'extra')
# aotixpy 的 locale/zh-CN 目录：从解压后的 aotixpy mod 取得，用环境变量指定
AOTIXPY = os.environ.get('AOTIXPY_LOCALE', '')
if not os.path.isdir(AOTIXPY):
    raise SystemExit('请先设置环境变量 AOTIXPY_LOCALE 指向 aotixpy 的 locale/zh-CN 目录')

SEC = re.compile(r'^\s*\[([^\]]+)\]\s*$')
CJK = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
LATIN_WORD = re.compile(r'[A-Za-z]{2,}')

def parse_cfg(path):
    out, sec = [], None
    with open(path, 'r', encoding='utf-8-sig', errors='replace') as f:
        for raw in f:
            line = raw.rstrip('\r\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            m = SEC.match(line)
            if m:
                sec = m.group(1).strip(); continue
            if '=' not in line or sec is None:
                continue
            k, v = line.split('=', 1)
            k = k.strip()
            if k:
                out.append((sec, k, v))
    return out

def load_dir(root):
    d = {}
    for dirpath, _, files in os.walk(root):
        for fn in sorted(files):
            if fn.endswith('.cfg'):
                for sec, k, v in parse_cfg(os.path.join(dirpath, fn)):
                    d[(sec, k)] = v
    return d

# en 基准
en = {}
enmod = {}
for mod in sorted(os.listdir(EN)):
    p = os.path.join(EN, mod)
    if os.path.isdir(p):
        for (sec, k), v in load_dir(p).items():
            en[(mod, sec, k)] = v
            enmod[(sec, k)] = mod

# 中文源，按游戏加载顺序赋值：数字越大越晚加载（越优先）
# 估算加载顺序: ai_cn < aotixpy < pysimple / py* (字母序，a..z)
def order_of(mod):
    return {'ai_cn': 10, 'aotixpy': 20, 'aotixpy-supplement': 90}.get(mod, 30)

layers = collections.defaultdict(list)  # (sec,key) -> [(order, src, value)]
for src, root in [('ai_cn', EXTRA), ('aotixpy', AOTIXPY)]:
    for (sec, k), v in load_dir(root).items():
        layers[(sec, k)].append((order_of(src), src, v))
for mod in sorted(os.listdir(MODZH)):
    p = os.path.join(MODZH, mod)
    if os.path.isdir(p):
        for (sec, k), v in load_dir(p).items():
            layers[(sec, k)].append((order_of(mod), mod, v))

def has_cjk(s):
    return bool(CJK.search(s))

rows = []
cnt = collections.Counter()
for (mod, sec, k), v in en.items():
    lay = layers.get((sec, k), [])
    if not lay:
        cnt['无任何译文'] += 1
        rows.append((mod, sec, k, v, '', 'NONE'))
        continue
    lay.sort(key=lambda x: x[0])
    order, src, val = lay[-1]
    chinese_anywhere = [x for x in lay if has_cjk(x[2])]
    if not has_cjk(val):
        # 最终生效值无中文
        if LATIN_WORD.search(v):
            cnt['生效值为英文'] += 1
            rows.append((mod, sec, k, v, val, f'EN-WINS({src})' if not chinese_anywhere else f'EN-WINS_但{chinese_anywhere[-1][1]}有中文'))
        else:
            cnt['非文本(符号/数字)'] += 1
    else:
        cnt['正常中文'] += 1

print('统计:')
for k, v in cnt.most_common():
    print(f'  {k}: {v}')
print('\n问题条目按 mod/section:')
c = collections.Counter((r[0], r[1]) for r in rows)
for (m, s), n in sorted(c.items(), key=lambda x: -x[1]):
    print(f'  {m:24s} {s:28s} {n}')
print('\n样例:')
for r in rows[:15]:
    print(f'  {r[0]:20s} {r[1]:20s} {r[2][:34]:34s} en={r[3][:40]!r} -> {r[4][:30]!r} [{r[5]}]')

json.dump([{'mod': r[0], 'section': r[1], 'key': r[2], 'en': r[3], 'effective': r[4], 'why': r[5]} for r in rows],
          open(os.path.join(WORK, 'problem.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n合计问题条目:', len(rows))
