# ✔️pY特调翻译·补充包（aotixpy-supplement）

[aotixpy](https://mods.factorio.com/mod/aotixpy)「pY 特调翻译」的**独立补充汉化包**，只补原汉化与 pY 模组自身都没覆盖到的词条。

- 游戏版本：Factorio 2.1
- mod 名称：`aotixpy-supplement`
- 依赖：全部为**可选依赖**（`?`），既可配合 aotixpy 使用，也可单独启用
- 原则：**只新增词条**，不覆盖、不修改任何原模组的文件与文本

## 一、补了什么

针对 pY 3.1.x 世代的模组组合，逐条比对「英文原词条」与「所有可用中文源（pY 模组自带 zh-CN + aotixpy + 其他汉化包）」，
并按游戏真实加载顺序（后加载覆盖先加载）算出每条词条**最终生效的译文**：

| 项目 | 数量 |
| --- | --- |
| pY 系模组英文词条（按 section + key 去重） | 7700 |
| 已有可用中文 | 7339（95.3%） |
| **本包补全** | **360** |

缺口集中在 **Pyanodons Streamlined（pysimple）**——aotixpy 未覆盖该模组，而它会用
`{"name.xxx"}` / `{"description.xxx"}` 重写大量显示名，缺少对应词条时这些文本会回落到英文：

- `[name]` 254 条：物品分类名（材料 / 流体 / 生物 / 环境 / 抽象…）、多产物配方名（如「煤、煤气、焦油、氧化铁」）、
  研究包、储罐、发电厂等重命名条目；
- `[description]` 38 条：被改写的科技、实体与配方描述；
- 设置项 34 条：`mod-setting-*` 与 `string-mod-setting-*`。

其余为 pY 各模组的残留英文：

- pY 替代能源：风速 / 潮汐地表属性名与单位、建筑产出提示、LFR 发电厂描述、乏控制棒再处理；
- pY 异星生命：C.A.G.S.、同类相食、埃特尔导航、狼王等科技名；
- pY 煤炭处理：pY 星际探险 / 异星生物的模组名、信标调幅 / 调频；
- pY 后处理：日志详细程度。

另外修正了 pY 自带 zh-CN 中两处**坏值**（不影响原文件，仅在本包内给出正确值）：

- 史前生物百科的 T.U.R.D. 条目链接被写成了 `[item=py-science-pack-1]`，点开是错误物品；
- `[turd] font` 的值被截断，导致字体标签失效。

## 二、加载顺序

`info.json` 使用可选依赖，因此：

- 同时装了 aotixpy 与各 pY 模组：本包排在其后加载，译文优先；
- 没装 aotixpy：本包仍可独立使用（自带完整中文，不依赖其他汉化包）。

```
? aotixpy, ? pysimple, ? pyalienlife, ? pyalternativeenergy, ? pycoalprocessing,
? pypostprocessing, ? pymodpack, ? pyindustry, ? pyrawores, ? pyhightech,
? pyfusionenergy, ? pypetroleumhandling
```

## 三、安装

1. 从 [Mod Portal](https://mods.factorio.com/mod/aotixpy-supplement) 订阅，或把 `dist/` 里的 zip 放进 Factorio 的 `mods` 目录；
2. 在游戏「模组」界面启用 `aotixpy-supplement`；
3. 语言需为简体中文（`zh-CN`）。

## 四、文件结构

```
aotixpy-supplement/
├── info.json                       mod 元数据
├── changelog.txt                   更新日志（首条版本须与 info.json 一致）
├── thumbnail.png                   门户缩略图
├── CREDITS.md                      致谢与来源说明
├── LICENSE                         GPL-3.0
├── locale/
│   ├── en/en.cfg                   英文回退（模组名 / 描述）
│   └── zh-CN/
│       ├── aotixpy-supplement.cfg  本包模组名 / 描述
│       ├── pysimple_1.1.4.cfg            331 条
│       ├── pyalienlife_3.1.8.cfg           8 条
│       ├── pyalternativeenergy_3.2.11.cfg 14 条
│       ├── pycoalprocessing_3.1.8.cfg      6 条
│       └── pypostprocessing_3.1.7.cfg      1 条
├── tools/
│   ├── package.ps1                 打包脚本
│   ├── publish.ps1                 发布到 Mod Portal 的脚本
│   └── build/                      词条比对与生成工具链（不随包发布）
└── dist/                           打包产物（git 忽略）
```

语言文件命名沿用 aotixpy 的 `<模组名>_<版本>.cfg` 习惯。文件名只影响可读性，
Factorio 会加载 `locale/<语言>/` 下的全部 `.cfg`，因此 pY 升版后无需改名也能继续生效。

## 五、打包与发布

打包（读取 `info.json` 版本，校验 `changelog.txt` 首条版本一致，输出 `dist/aotixpy-supplement_<版本>.zip`）：

```powershell
.\tools\package.ps1
```

发布到 Factorio Mod Portal（API Key 来自 <https://factorio.com/profile>）：

```powershell
$env:FACTORIO_API_KEY = '<你的 API Key>'
.\tools\publish.ps1 -Mode new       # 首次创建 mod
.\tools\publish.ps1 -Mode release   # 后续版本
```

也可以把 `$ApiKey = '...'` 写进 `tools/config.local.ps1`（已被 `.gitignore` 忽略）。
需要代理时设置 `$env:HTTPS_PROXY` 或传 `-Proxy http://127.0.0.1:7890`。

## 六、致谢

本包的每一条译文都建立在别人的工作之上：

- **[aotixpy](https://mods.factorio.com/mod/aotixpy)（pY 特调翻译）**，作者 **aotix**（GPL-3.0）——
  本包的模组命名、语言文件组织方式与绝大多数术语译名都沿用它，仅补其未覆盖的词条。
  没有这份汉化，本包无从谈起。
- **Pyanodons 系列模组**，作者 **Pyanodon** 及各位贡献者——原文、术语与 pY 各模组自带的 zh-CN 译文均来自上游。
- **pysimple（Pyanodons Streamlined）** 作者——本包主要的补全对象，其 `name.*` / `description.*` 重写机制决定了缺口位置。
- 其他汉化包（如 `ai_cn`）——比对时用作参照，本包不含其内容。

详细来源、比对方法与许可证说明见 [CREDITS.md](CREDITS.md)。

## 七、许可证

本包作为 aotixpy 的补充作品，沿用同一许可证：[GNU GPL v3.0](LICENSE)。
如果原作者认为本包与其规划冲突，可随时联系下线。

## 八、后续维护

`tools/build/` 保留完整工具链（打包时排除，不会进 zip）：

- `analyze2.py`：按加载顺序计算每条词条最终生效译文，输出 `problem.json`；
- `build_glossary.py`：从现有 en/zh 词条反向构建「英文→中文」术语表，保证新译文与既有译名一致；
- `gen.py` + `content.py`：产物列表拼装与手工词条（`content.py` 内的 `SEG` / `HEAD` / `MANUAL`）；
- `build.py`：写出本包的 `locale/`；`verify.py`：模拟合并、检查是否误覆盖已有中文、检查重复键。

pY 升版后：解包新版 en/zh 语言文件 → `analyze2.py` → 补 `content.py` → `gen.py` → `build.py` → `verify.py` → `package.ps1`。
