#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从现有 en/zh 词条构建 英文->中文 术语对照表，并解析缺失条目中的产品列表"""
import os, re, json, collections

WORK = os.path.dirname(os.path.abspath(__file__))
EN, MODZH, EXTRA = (os.path.join(WORK, x) for x in ('en', 'modzh', 'extra'))
AOTIXPY = os.environ.get('AOTIXPY_LOCALE', '')
if not os.path.isdir(AOTIXPY):
    raise SystemExit('请先设置环境变量 AOTIXPY_LOCALE 指向 aotixpy 的 locale/zh-CN 目录')
SEC = re.compile(r'^\s*\[([^\]]+)\]\s*$')

def parse_cfg(path):
    out, sec = [], None
    for raw in open(path, encoding='utf-8-sig', errors='replace'):
        line = raw.rstrip('\r\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        m = SEC.match(line)
        if m:
            sec = m.group(1).strip(); continue
        if '=' in line and sec:
            k, v = line.split('=', 1)
            if k.strip():
                out.append((sec, k.strip(), v))
    return out

def load(root):
    d = {}
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            if f.endswith('.cfg'):
                for s, k, v in parse_cfg(os.path.join(dp, f)):
                    d[(s, k)] = v
    return d

en = load(EN)
# 优先级：pY 自带 zh > aotixpy > ai_cn
zh_final = {}
for root in (MODZH, AOTIXPY, EXTRA):
    zh_final.update(load(root))

CJK = re.compile(r'[\u4e00-\u9fff]')
NAME_SECS = {'item-name', 'fluid-name', 'entity-name', 'recipe-name', 'technology-name',
             'item-group-name', 'ore-name', 'tile-name', 'equipment-name', 'fuel-category-name',
             'virtual-signal-name', 'resource-category-name', 'ammo-category-name', 'quality-name'}

gloss = {}
for (s, k), ev in en.items():
    zv = zh_final.get((s, k))
    if not zv or not CJK.search(zv):
        continue
    ev2, zv2 = ev.strip(), zv.strip()
    if not ev2 or '\\n' in ev2 or len(ev2) > 60 or '[' in ev2:
        continue
    gloss.setdefault(ev2, zv2)

# 常见单词兜底
extra_gloss = {
    'stone': '石头', 'gravel': '砂砾', 'sand': '沙子', 'steam': '蒸汽', 'water': '水',
}
for k, v in extra_gloss.items():
    gloss.setdefault(k, v)

json.dump(gloss, open(os.path.join(WORK, 'glossary.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0, sort_keys=True)
print('术语表条目:', len(gloss))

# 解析待译产品列表，看解析率
targets = json.load(open(os.path.join(WORK, 'missing.json'), encoding='utf-8'))
seen = {}
for t in targets:
    seen.setdefault((t['section'], t['key']), t)

unresolved = collections.Counter()
for (s, k), t in seen.items():
    if s != 'name' or k in ('storage',):
        continue
    val = t['en']
    body = val.split(' - ', 1)[1] if ' - ' in val else val
    for seg in [x.strip() for x in body.split(', ')]:
        base = re.sub(r'\s*\(grade \d\)$', '', seg)
        if seg not in gloss and base not in gloss:
            unresolved[seg] += 1
print('未解析片段:', len(unresolved))
for seg, n in unresolved.most_common():
    print(f'  {seg}  x{n}')
