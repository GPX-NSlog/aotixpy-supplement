# 致谢与来源说明

本包（`aotixpy-supplement`）不含任何原创美术资源，也不含任何原模组的文件副本。
它的全部内容都是**新写的语言词条**，用来补上原汉化与 pY 模组自身没有覆盖的显示文本。
译名、术语与语言文件组织方式均沿用上游既有译文，在此向所有上游作者致谢。

## 一、原汉化：aotixpy（pY 特调翻译）

- 名称：aotixpy（游戏内标题「✔️pY特调翻译」）
- 作者：**aotix**
- 发布页：<https://mods.factorio.com/mod/aotixpy>
- 许可证：GNU General Public License v3.0
- 本包对其的依赖方式：

| 沿用项 | 说明 |
| --- | --- |
| 模组命名 | `aotixpy-supplement` 与 `aotixpy` 同源，便于识别为同一系列 |
| 语言文件组织 | 沿用 `locale/zh-CN/<模组名>_<版本>.cfg` 的命名习惯 |
| 术语与译名 | 以 aotixpy 现有译文为**唯一基准**，新译文与其保持一致 |
| 加载顺序 | 以可选依赖 `? aotixpy` 声明在其之后加载 |

本包**只补 aotixpy 未覆盖的词条**，不改动、不重写 aotixpy 已有的任何译文。
如果你只需要 aotixpy 已覆盖的部分，单独安装 aotixpy 即可，本包可以不装。

## 二、原文来源：Pyanodons 系列模组

- 作者：**Pyanodon** 及各位贡献者
- 作者页：<https://mods.factorio.com/user/pyanodon>
- 涉及的模组（比对时的版本）：`pysimple` 1.1.4、`pyalienlife` 3.1.8、
  `pyalternativeenergy` 3.2.11、`pycoalprocessing` 3.1.8、`pypostprocessing` 3.1.7、
  `pyindustry` 3.1.6、`pyrawores` 3.1.4、`pyfusionenergy` 3.1.6、`pyhightech` 3.1.5、
  `pypetroleumhandling` 3.1.5、`pymodpack` 3.1.0
- 英文原文、物品 / 流体的设定与 pY 各模组自带的 zh-CN 译文，版权均归上游作者所有

其中 **Pyanodons Streamlined（`pysimple`）** 是本包主要的补全对象。它会在数据阶段用
`{"name.xxx"}` / `{"description.xxx"}` 改写大量原型的显示名，并为物品分类重新分组；
这些键一旦在语言文件里找不到，游戏就会回落显示英文，本包补的正是这部分。

## 三、参照与比对来源

- pY 各模组自带的 `locale/zh-CN/`（随模组分发）
- aotixpy 的 `locale/zh-CN/`（GPL-3.0）
- 其他第三方汉化包（如 `ai_cn`）——**仅用于比对与核对译名**，本包不含其任何内容

比对方法：抽取英文词条（`section` + `key` 去重）→ 按游戏真实加载顺序（后加载覆盖先加载）
计算每条词条最终生效的译文 → 取「仍为英文」或「无词条」的条目 → 逐条人工翻译。
术语表由既有 en/zh 词条反向构建，以保证「尾矿 / 酸性气体 / 柏油 / 沥青 / 蓝坷垃」等叫法与游戏中完全一致。

## 四、本包的原创部分

- 360 条新译词条（`locale/zh-CN/` 下各文件）
- `locale/en/en.cfg` 中的英文回退文本
- `thumbnail.png`（按 aotixpy 缩略图的风格另行绘制，未使用其原始图像文件）
- 打包 / 发布 / 比对工具链（`tools/`）

## 五、许可证

本包作为 aotixpy 的补充作品，按 **GNU General Public License v3.0** 分发，全文见 `LICENSE`。

再分发时请保留本文件、`LICENSE`，以及 `info.json` 中的致谢信息。
若原作者 aotix 或 Pyanodon 认为本包与其规划冲突，可随时联系下线。
