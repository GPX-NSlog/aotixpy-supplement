# -*- coding: utf-8 -*-
"""汇总译文并生成 aotixpy-supplement 的语言文件"""
import os, re, json, sys, collections
import content

WORK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.dirname(WORK))  # 项目根目录
SEC = re.compile(r'^\s*\[([^\]]+)\]\s*$')

SEG = dict(content.SEG)
HEAD = content.HEAD
SEG_NORM = {k.lower(): v for k, v in SEG.items()}
HEAD_NORM = {k.lower(): v for k, v in HEAD.items()}

GRADE = re.compile(r'^(.+?)\s*\((?:grade|Grade)\s*(\d)\)$')
STAGE = re.compile(r'^(.+?)\s*\((stage|Stage)\s*(\d)\)$')

unresolved = collections.OrderedDict()

def tr_seg(seg):
    if seg in SEG:
        return SEG[seg]
    low = seg.lower()
    if low in SEG_NORM:
        return SEG_NORM[low]
    m = GRADE.match(seg)
    if m:
        base, n = m.group(1), m.group(2)
        b = tr_seg(base)
        if b:
            return f'{n}级{b}'
    m = STAGE.match(seg)
    if m:
        base, n = m.group(1), m.group(3)
        b = tr_seg(base)
        if b:
            return f'{b}（{n} 阶段）'
    if low.rstrip('s') in SEG_NORM:
        return SEG_NORM[low.rstrip('s')]
    return None

def tr_label(en):
    if ' - ' in en:
        head, body = en.split(' - ', 1)
        zh_head = HEAD.get(head) or HEAD_NORM.get(head.lower())
        if zh_head is None:
            unresolved.setdefault(('HEAD', head), 0)
            unresolved[('HEAD', head)] += 1
            zh_head = head
        parts = [tr_seg(x.strip()) or x.strip() for x in body.split(',')]
        for x in [x.strip() for x in body.split(',')]:
            if tr_seg(x) is None:
                unresolved[(('SEG', x))] = unresolved.get(('SEG', x), 0) + 1
        return f'{zh_head} - ' + '、'.join(parts)
    if ',' in en:
        parts = []
        for x in [x.strip() for x in en.split(',')]:
            z = tr_seg(x)
            if z is None:
                unresolved[('SEG', x)] = unresolved.get(('SEG', x), 0) + 1
                z = x
            parts.append(z)
        return '、'.join(parts)
    z = tr_seg(en)
    if z is None:
        unresolved[('SEG', en)] = unresolved.get(('SEG', en), 0) + 1
        return None
    return z

# ---- 收集条目 ----
entries = collections.defaultdict(lambda: collections.defaultdict(dict))  # mod -> section -> key -> zh
missing = json.load(open(os.path.join(WORK, 'missing.json'), encoding='utf-8'))
seen = collections.OrderedDict()
for m in missing:
    seen.setdefault((m['section'], m['key']), m)

for (sec, key), m in seen.items():
    if (sec, key) in content.SKIP:
        continue
    mod = m['mod']
    if sec == 'name':
        zh = tr_label(m['en'].strip())
        if zh:
            entries[mod][sec][key] = zh
    # 其余由 MANUAL 提供

missing_manual = []
for mod, secs in content.MANUAL.items():
    for sec, kv in secs.items():
        for k, v in kv.items():
            entries[mod][sec][k] = v

# 检查 MANUAL 未覆盖的非 name 条目
for (sec, key), m in seen.items():
    if sec == 'name' or (sec, key) in content.SKIP:
        continue
    if key not in entries[m['mod']].get(sec, {}):
        missing_manual.append((m['mod'], sec, key, m['en']))

if unresolved:
    print('!! 未解析片段:')
    for (kind, s), n in unresolved.items():
        print(f'   [{kind}] {s}  x{n}')
print('\n!! 未覆盖的非 name 条目:', len(missing_manual))
for x in missing_manual:
    print('   ', x)

total = sum(len(kv) for m in entries.values() for kv in m.values())
print(f'\n待写入条目 {total} 条：')
for mod in entries:
    n = sum(len(kv) for kv in entries[mod].values())
    print(f'  {mod:26s} {n}')

json.dump({m: {s: kv for s, kv in secs.items()} for m, secs in entries.items()},
          open(os.path.join(WORK, 'entries.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
