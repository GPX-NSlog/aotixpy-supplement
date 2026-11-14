# -*- coding: utf-8 -*-
"""写出 aotixpy-supplement 的完整 mod 目录"""
import os, json, collections

WORK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.dirname(WORK))  # 项目根目录

NAME = 'aotixpy-supplement'
VERSION = '1.0.0'
FACTORIO_VERSION = '2.1'

# 目标 pY 系 mod 与其在存档中的版本（用于文件命名，与 aotixpy 的 <mod>_<ver>.cfg 习惯一致）
TARGETS = collections.OrderedDict([
    ('pysimple', '1.1.4'),
    ('pyalienlife', '3.1.8'),
    ('pyalternativeenergy', '3.2.11'),
    ('pycoalprocessing', '3.1.8'),
    ('pypostprocessing', '3.1.7'),
])

SECTION_ORDER = [
    'mod-name', 'mod-description',
    'mod-setting-name', 'mod-setting-description',
    'string-mod-setting', 'string-mod-setting-description',
    'map-gen-preset-name', 'map-gen-preset-description',
    'name', 'description',
    'item-name', 'item-description',
    'entity-name', 'entity-description', 'entity-tooltip',
    'recipe-name', 'recipe-description',
    'technology-name', 'technology-description',
    'fluid-name', 'fluid-description',
    'surface-property-name', 'surface-property-unit',
    'beacon-modifier', 'tooltip', 'pywiki-sections', 'turd', 'caravan-gui',
]

FILE_HEADER = (
    '# pY 特调翻译·补充包 —— 由 aotixpy 补充汉化项目生成\n'
    '# 说明：本文件只补全 aotixpy 与原模组均未覆盖的词条，不修改任何原模组内容。\n'
)

entries = json.load(open(os.path.join(WORK, 'entries.json'), encoding='utf-8'))

# ---------- info.json ----------
deps = ['"base >= 2.1.0"', '"? aotixpy"']
deps += [f'"? {m}"' for m in TARGETS]
deps += ['"? pymodpack"', '"? pyindustry"', '"? pyrawores"', '"? pyhightech"',
         '"? pyfusionenergy"', '"? pypetroleumhandling"']
deps = list(dict.fromkeys(deps))

info = collections.OrderedDict([
    ('name', NAME),
    ('version', VERSION),
    ('title', '✔️pY特调翻译·补充包'),
    ('author', 'Gpx；译名基准来自 aotix 的 aotixpy，原文版权归 pY 系列模组作者 Pyanodon 及贡献者'),
    ('contact', ''),
    ('homepage', 'https://github.com/GPX-NSlog/aotixpy-supplement'),
    ('description',
     # 门户把这个字段直接当作 Summary 展示，且不渲染 BBCode / Markdown，
     # 所以只写一句纯文本；详细说明放在门户的 Description 字段（见 PORTAL.md）。
     '「pY 特调翻译」的补充汉化包，独立成模组。'
     '补全 pY 精简（Pyanodons Streamlined）的物品分类名、多产物配方名称、设置项与描述，'
     '以及 pY 各模组仍显示英文的残留词条，共 360 条。'
     '全部为可选依赖，可单独启用，不覆盖或修改任何原模组的文件与文本。'),
    ('factorio_version', FACTORIO_VERSION),
    ('dependencies', [d.strip('"') for d in deps]),
])

files = {}
files['info.json'] = json.dumps(info, ensure_ascii=False, indent='\t')

# ---------- changelog ----------
changelog = """---------------------------------------------------------------------------------------------------
Version: 1.0.0
Date: 2026-11-13
  Features:
    - 首次发布。补全 pY 系模组（pY 3.1.x 世代）中最终仍显示英文的 360 条词条。
    - 补全 pY 精简（Pyanodons Streamlined）的全部物品分类名、254 条多产物配方名称、38 条描述改写与 34 条设置项。
    - 补全 pY 替代能源的风速/潮汐地表属性与单位、信标调幅调频、pY 异星生命的残留科技名。
    - 全部为新增词条，不覆盖、不修改原模组文件；通过可选依赖排在 aotixpy 与各 pY 模组之后加载。
  Bugfixes:
    - 修正 pY 异星生命史前生物百科条目中残留的错误物品链接（T.U.R.D.）。
    - 修正 pY 异星生命字体标签被截断导致的显示异常。
  Info:
    - 致谢 aotixpy（作者 aotix）与 pY 系列模组作者 Pyanodon 及贡献者，详见 CREDITS.md。
---------------------------------------------------------------------------------------------------
"""
files['changelog.txt'] = changelog

# ---------- 各语言文件 ----------
def render(mod, secs):
    out = [FILE_HEADER]
    order = [s for s in SECTION_ORDER if s in secs] + [s for s in secs if s not in SECTION_ORDER]
    for sec in order:
        kv = secs[sec]
        if not kv:
            continue
        out.append(f'[{sec}]\n')
        for k in kv:
            out.append(f'{k}={kv[k]}\n')
        out.append('\n')
    return ''.join(out)

locale_dir = os.path.join(OUT, 'locale', 'zh-CN')
os.makedirs(locale_dir, exist_ok=True)
os.makedirs(os.path.join(OUT, 'locale', 'en'), exist_ok=True)

count = {}
for mod, ver in TARGETS.items():
    secs = entries.get(mod, {})
    if not secs:
        continue
    text = render(mod, secs)
    fn = f'{mod}_{ver}.cfg'
    files[os.path.join('locale', 'zh-CN', fn)] = text
    count[fn] = sum(len(v) for v in secs.values())

# mod 自身的名称
self_zh = (
    '[mod-name]\n'
    f'{NAME}=pY特调翻译·补充包\n\n'
    '[mod-description]\n'
    f'{NAME}=「pY特调翻译」的补充汉化包：补全 pY 精简的分类与配方名、以及各 pY 模组中残留的英文词条。\n'
)
files[os.path.join('locale', 'zh-CN', f'{NAME}.cfg')] = FILE_HEADER + self_zh
files[os.path.join('locale', 'en', 'en.cfg')] = (
    '[mod-name]\n'
    f'{NAME}=pY Custom Translation - Supplement\n\n'
    '[mod-description]\n'
    f'{NAME}=A standalone supplement for the aotixpy Chinese translation: completes Py Streamlined '
    'display names and the entries that remained untranslated in the pY mods.\n'
)

for rel, text in files.items():
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

print('已写入', len(files), '个文件')
for k, v in count.items():
    print(f'  {k:34s} {v} 条')
