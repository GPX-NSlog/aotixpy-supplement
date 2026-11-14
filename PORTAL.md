# Mod Portal 填写内容

门户的 **Summary** 与 **Description** 是两个独立字段，只能在网页端 Edit 页面修改
（`init_publish` 只写入 `summary`，`init_upload` 不接受这两个字段，API 也没有 PATCH 入口）。

本文件保存两个字段的最终文案，改版时直接复制粘贴。

页面：<https://mods.factorio.com/mod/aotixpy-supplement/edit>

---

## 一、Summary（短简介，纯文本）

> 注意：Summary **不渲染** BBCode / Markdown，写 `[color=orange]` 会原样显示，所以这里只用纯文本。

```text
「pY 特调翻译」的补充汉化包，独立成模组。补全 pY 精简（Pyanodons Streamlined）的物品分类名、多产物配方名称、设置项与描述，以及 pY 各模组仍显示英文的残留词条，共 360 条。全部为可选依赖，可单独启用，不覆盖或修改任何原模组的文件与文本。
```

---

## 二、Description（详细描述，Markdown）

> 注意：Description **按 Markdown 渲染**（`#`→h1、`##`→h2、`-`→列表、`**b**`→粗体）。
> 不要使用 BBCode；表格支持不稳定，统一用列表。

```markdown
# pY 特调翻译·补充包

给 pY 3.1.x 模组组合补上最后一层中文。原汉化 aotixpy 已覆盖约 95% 的词条，本包只补它和 pY 各模组自身都没有覆盖到的 360 条，其他文本一律不动。

## 这个包解决什么

pY 3.1.x 的各模组其实自带中文，aotixpy 也覆盖了大部分。但按游戏真实加载顺序（后加载覆盖先加载）逐条核对后，仍有 360 条词条最终显示为英文。原因集中在 **pY 精简（Pyanodons Streamlined，pysimple）**：它会用 `name.*` / `description.*` 主动重写大量显示名，这些键一旦没有对应词条就回落到英文，而 aotixpy 从未覆盖这个模组。

## 补了什么

比对范围：存档启用的 11 个 pY 模组，共 7700 条英文词条（按 section + key 去重），其中已有中文 7339 条（95.3%）。

- **pysimple 331 条**：物品分类栏名称（材料 / 流体 / 生物 / 环境 / 抽象等）、254 条多产物配方名、38 条被改写的科技与实体描述、34 条设置项
- **pyalternativeenergy 14 条**：风速与潮汐地表属性、单位
- **pyalienlife 8 条**：科技名、史前生物百科条目
- **pycoalprocessing 6 条**：信标界面的「调幅 / 调频」等
- **pypostprocessing 1 条**：乏燃料相关条目

顺带修复 pY 自带中文里的三处坏值：

- 史前生物百科的 T.U.R.D. 链接被写成了错误的物品 `[item=py-science-pack-1]`
- 字体标签 `[turd] font` 的值被截断，导致标签失效
- 段落名带尾随空格（`[entity-name] `）导致 18 条实体名不生效

## 你需要做什么

装好、勾选、进游戏，没有额外操作。分类栏、配方名、设置项会直接变成中文。

## 安装与加载顺序

- 全部依赖写成可选依赖（`?`），所以**不装 aotixpy 也能单独用**
- 同时装了 aotixpy 时，本包会排在它和所有 pY 模组之后加载，译文优先生效
- 只新增词条，不覆盖、不修改任何原模组的文件与文本，卸载后不留残留

## 兼容性

- 游戏版本：Factorio 2.1
- 针对 pY 3.1.x 世代编写并核对：pysimple 1.1.4、pyalienlife 3.1.8、pyalternativeenergy 3.2.11、pycoalprocessing 3.1.8、pypostprocessing 3.1.7
- pY 升级后可能出现新的英文词条，届时会跟随更新

## English

A supplementary Chinese translation for the Pyanodons (pY) mod suite, packaged as a standalone mod. The existing aotixpy translation already covers about 95% of strings; this pack fills the remaining 360 entries, mostly from Pyanodons Streamlined (pysimple), which rewrites display names via `name.*` / `description.*` keys and therefore falls back to English wherever a key is missing. Covers item group names, multi-output recipe names, settings, and rewritten descriptions, plus leftover English strings in other pY mods.

All dependencies are optional, so the mod works with or without aotixpy. It only adds new entries and never overrides or modifies files from other mods.

## Credits

This pack builds entirely on other people's work:

- **aotixpy (pY 特调翻译)** by **aotix** (GPL-3.0) — the mod naming, locale file layout, and the vast majority of terminology come from this translation. Without it this pack would not exist.
- **Pyanodons mods** by **Pyanodon** and contributors — the original English text and the bundled zh-CN translations.
- **pysimple (Pyanodons Streamlined)** — the main target of this pack, since its `name.*` / `description.*` rewriting is what creates the gaps.

Full source list, file references and license notes: see CREDITS.md in the repository.

## License and source

- License: GNU GPL v3.0
- Source code: https://github.com/GPX-NSlog/aotixpy-supplement
- Original translation: https://mods.factorio.com/mod/aotixpy
```

---

## 三、其他字段

| 字段 | 值 |
| --- | --- |
| License | `GNU GPLv3`（下拉框直接选；API 枚举值是 `gnugplv3`） |
| Source | `https://github.com/GPX-NSlog/aotixpy-supplement` |
| Category | `Localizations` |
| Homepage | `https://github.com/GPX-NSlog/aotixpy-supplement` |

## 四、为什么必须网页改

- `license` / `source_url` / `category` 只在 `init_publish`（首次创建 mod）时提交，
  之后 API 没有 PATCH / DELETE 入口（实测均返回 404）。
- `summary` 由 `init_publish` 时的 `description` 写入，`init_upload`（后续版本）
  不带这个字段，所以发新版本**不会**更新 Summary。
- `description` 是门户侧的富文本字段，API 全程没有写入入口。

结论：这四项只能在这个页面改一次：<https://mods.factorio.com/mod/aotixpy-supplement/edit>
