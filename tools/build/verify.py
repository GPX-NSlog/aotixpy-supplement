# -*- coding: utf-8 -*-
"""校验：按游戏实际合并顺序模拟，确认补齐效果与无副作用覆盖"""
import os, re, json, collections

WORK = os.path.dirname(os.path.abspath(__file__))
SUP = os.path.join(os.path.dirname(os.path.dirname(WORK)), 'locale', 'zh-CN')
EN, MODZH, EXTRA = (os.path.join(WORK, x) for x in ('en', 'modzh', 'extra'))
AOTIXPY = os.environ.get('AOTIXPY_LOCALE', '')
if not os.path.isdir(AOTIXPY):
    raise SystemExit('请先设置环境变量 AOTIXPY_LOCALE 指向 aotixpy 的 locale/zh-CN 目录')
SEC = re.compile(r'^\s*\[([^\]]+)\]\s*$')
CJK = re.compile(r'[\u4e00-\u9fff]')

def parse_cfg(path, strict=False):
    out, sec = [], None
    for i, raw in enumerate(open(path, encoding='utf-8-sig', errors='strict' if strict else 'replace'), 1):
        line = raw.rstrip('\r\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        m = SEC.match(line)
        if m:
            sec = m.group(1)
            if strict and sec != sec.strip():
                print(f'  !! {os.path.basename(path)}:{i} 段落名有空白: {sec!r}')
            continue
        if '=' not in line:
            print(f'  !! {os.path.basename(path)}:{i} 无法解析: {line[:40]!r}')
            continue
        k, v = line.split('=', 1)
        out.append((sec, k.strip(), v))
    return out

def load(root, strict=False):
    d = {}
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            if f.endswith('.cfg'):
                for s, k, v in parse_cfg(os.path.join(dp, f), strict):
                    d[(s, k)] = v
    return d

# 现有生效值（按加载顺序：pY 自带 > aotixpy > ai_cn）
before = {}
for root in (EXTRA, AOTIXPY, MODZH):
    before.update(load(root))

sup = load(SUP, strict=True)
print(f'补充包词条: {len(sup)}')

after = dict(before)
after.update(sup)

# 1) 原判定缺失/英文的条目是否已补齐
targets = json.load(open(os.path.join(WORK, 'problem.json'), encoding='utf-8'))
bad = []
for t in targets:
    key = (t['section'], t['key'])
    val = after.get(key, '')
    if not CJK.search(val):
        bad.append((key, t['en'][:40], val[:30]))
print(f'仍未汉化的残留条目: {len(bad)}')
for x in bad:
    print('   ', x)

# 2) 覆盖了本已中文的词条？
overridden = []
for (s, k), v in sup.items():
    old = before.get((s, k))
    if old and CJK.search(old) and old.strip() != v.strip():
        overridden.append((s, k, old[:36], v[:36]))
print(f'覆盖了原有中文译文的条目: {len(overridden)}')
for x in overridden[:15]:
    print('   ', x)

# 3) 补充包内部重复键
dups = collections.Counter()
for mod_sec in sup:
    dups[mod_sec] += 1
print(f'重复键: {[k for k, n in dups.items() if n > 1]}')

# 4) 每条目是否含中文（排除纯标记/占位）
no_cjk = [(s, k, v) for (s, k), v in sup.items() if not CJK.search(v)]
print(f'无中文字符的条目（纯标记/占位，应可解释）: {len(no_cjk)}')
for x in no_cjk:
    print('   ', x)

json.dump({f'{s}|{k}': v for (s, k), v in sup.items()},
          open(os.path.join(WORK, 'sup_map.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)
