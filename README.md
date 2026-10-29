# 《蕨花》Kwiat Paproci — 中文翻译

波兰 Black Monk 出版社 2020 年出版的《克苏鲁的呼唤》第七版模组集，经 Chaosium 授权、由出版社**免费公开发布**。本仓库是它的非官方中文翻译。

> **原作**：*Kwiat Paproci. Zbiór scenariuszy do Zewu Cthulhu*，36 页，作者 Piotr Chojnacki、Łukasz Wachciński、Aleksandra Menio、Martyna Pietrzak、Aleksander Daukszewicz、Paweł Jurgiel。
> **版权**：CALL OF CTHULHU / ZEW CTHULHU / Kwiat Paproci © 2020 Chaosium Inc.，波兰语版 © Black Monk。
> 本仓库**不包含原始 PDF**，只包含解析后的文本与中文译文。请从出版社渠道获取原书。

---

## 三篇模组

| 篇目 | 作者 | 页 | 主题 |
|---|---|---|---|
| [最短夜](translation/10-最短夜.md) | Chojnacki / Wachciński | 3–14 | 1925 年波兰庄园，创伤记忆与黄衣之王 |
| [水上花环](translation/20-水上花环.md) | Menio / Pietrzak | 15–28 | 奥波莱水乡，许德拉母亲与十年一次的献祭 |
| [蕨花 AR](translation/30-蕨花AR.md) | Daukszewicz / Jurgiel | 29–35 | 当代波兰，增强现实游戏与莎布·尼古拉丝 |

三篇共用**库帕拉之夜**（Noc Kupały，斯拉夫夏至节）这一民俗基底，彼此独立，可分开跑。

![最短夜 · 主角阿莉齐娅](assets/images/06010a454bd86f0a37393ddd8cf20aa14ee3c353c382ddca60e8fe6ab903ab79.jpg)

## 仓库结构

```
translation/     三篇中文译文（分节翻译后合并）
source/          MinerU 解析出的波兰语原文 Markdown
glossary/        译名对照表（基准 + 增补）
concepts/        Obsidian 概念笔记：库帕拉之夜、蕨花、许德拉母亲
docs/workflow.md 完整工作流与踩坑记录
tools/           解析、切分、调度脚本
assets/images/   从原书提取的插图
```

用 [Obsidian](https://obsidian.md) 打开仓库根目录，`concepts/索引.md` 是入口，全部笔记已做双向链接。

## 翻译流程

1. **解析** — MinerU 精准模式（`mineru-open-api extract`），36 页 → 131 KB Markdown + 21 张图
2. **分章** — 按 H1 切 6 部分，按 H2 聚合成 36 个翻译单元（每单元 ≤ 4,200 字符）
3. **定术语** — 人工编写 [译名对照表](glossary/译名对照表.md)，覆盖规则术语、属性、神话、民俗、地名、人物
4. **分节翻译** — `mimo-v2.6-flash`，并发 4，`reasoning_effort: low`
5. **校对** — 脚本比对专名与结构，人工复核规则数据与民俗词

| 指标 | 数值 |
|---|---|
| 完成 | 36 / 36 节，零失败 |
| 总耗时 | 1,973 秒（并发 4） |
| 平均 | 55 秒 / 节 |
| Token | 输入 145 K / 输出 74 K |
| 译文字数 | 38,855 字 |
| 术语违规 | 0 |

## 译名对照表

全书的强制基准，节选：

| 波兰语 | 中文 | 备注 |
|---|---|---|
| Strażnik Tajemnic | 守秘人 | 不译"守护者" |
| Badacz / Badaczka | 调查员 | 原文分性别，中文不分 |
| Noc Kupały | 库帕拉之夜 | 不译"圣约翰夜" |
| Kwiat Paproci | 蕨花 | 传说母题 |
| Kwiat Jednej Nocy | 一夜花 | 书中另一概念，不可混用 |
| Matka Hydra | 许德拉母亲 | **不译"九头蛇"**，与希腊神话无关 |
| swaćba | 成婚仪式 | 古语，与普通婚礼 `ślub` 不同 |
| Nienazywalny | 不可名状者 | |
| Król w Żółci | 黄衣之王 | |

完整版见 [glossary/译名对照表.md](glossary/译名对照表.md)，补录词条见 [增补表](glossary/译名对照表-新增.md)。

## 已知问题

- `Pani Feziora` 仅在第二篇日记中出现一次，暂译"费齐奥拉女士"，疑为"湖中女士"的方言变体，待核对
- 版权页、作者简介、后记未译（非模组正文）
- 原文个别标题在 OCR 时被识别为正文，译文已按上下文统一为标题

详见 [docs/workflow.md](docs/workflow.md)。

## 许可

- **代码与脚本**（`tools/`）：MIT，见 [LICENSE](LICENSE)
- **译文与术语表**：仅限个人跑团使用，非商业。原作版权归 Chaosium Inc. 与 Black Monk 所有，本仓库不主张任何译文的独立版权
- **插图**：版权归原书插画师 Jakub Fajtanowski、Anna Jarmołowska-Goryńska 所有，此处仅作模组配套引用

## 权利声明

这是**非官方粉丝翻译**，与 Chaosium Inc. 及 Black Monk 无隶属关系，未获其背书。
原书由出版社免费公开，本翻译仅为中文玩家阅读便利而作，不用于任何商业目的。

若权利人认为本仓库不妥，请开 issue 或联系仓库所有者，将立即移除相关内容。
