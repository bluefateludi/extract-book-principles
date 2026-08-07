# 双读者架构设计

## 设计结论

`extract-book-principles` 同时服务人类和 AI 是合适的，但不应分别维护两套知识。项目采用：

> 一个事实来源，两种阅读视图。

- 人类需要连贯、易读、能快速理解和行动的 Markdown。
- AI 需要字段稳定、可检索、可验证、可组合的 YAML。
- 两种视图表达同一份知识；可生成的 Markdown 不允许手工维护。

## 双读者契约

### 人类阅读契约

- 先呈现全书结构和核心论点，再呈现原则。
- 每条原则使用自然语言解释，并给出场景、行动建议和适用边界。
- 通过脚注或来源块展示章节和页码，不强迫读者阅读 YAML。
- 明确区分作者原意、AI 归纳和项目作者扩展。

### AI 阅读契约

- 为书籍、版本、来源和原则提供稳定 ID。
- 使用固定字段和有限枚举，避免依赖标题猜测含义。
- 每条原则必须能解析到已登记的书籍版本和证据位置。
- 支持按主题、场景、可信度和审核状态检索。
- 只按需加载相关原则与证据，不默认加载整本知识包。

## 单本书知识包

```text
books/<book-id>/<edition-id>/
├── metadata.yaml       # 书籍、版本、语言和处理状态
├── sources.yaml        # 本知识包使用的一手与辅助来源
├── book-map.md         # 全书结构、论证路径和概念关系
├── summary.md          # 人类与 AI 都可直接阅读的内容概要
├── principles.yaml     # 原则的唯一事实来源
├── principles.md       # 从 principles.yaml 生成的人类阅读版
└── evidence.md         # 从 principles.yaml 生成的证据索引
```

其中：

- `book-map.md` 和 `summary.md` 是兼顾人类与 AI 的叙述型原始内容。
- `principles.yaml` 是原则、边界和证据关系的唯一事实来源。
- `principles.md` 与 `evidence.md` 是生成物，文件头必须标记“请勿直接编辑”。
- 原书文件属于输入材料，不默认提交到公开仓库。

## 三级溯源

### 第一层：方法与项目溯源

记录项目借鉴过哪些工具、仓库和工作流，包括 URL、固定提交、许可证和具体借鉴点。

这层回答：“我们为什么这样设计？”

它不能用于证明某条原则是原书作者的观点。例如，借鉴 `life-design-coach` 的分阶段 Skill 结构，并不代表某条人生原则来自该仓库。

项目级记录放在 [reference-projects.md](reference-projects.md)，未来需要自动检查时再增加结构化注册表。

### 第二层：书籍版本溯源

每个知识包必须固定到具体版本：

```yaml
id: designing-your-life-en-2016
type: book
title: Designing Your Life
authors:
  - Bill Burnett
  - Dave Evans
publisher: Knopf
year: 2016
isbn: "9781101875322"
language: en
```

中文版、修订版和电子版分别登记。页码只在同一版次内有效，因此原则不能只保存一个脱离版本的页码。

### 第三层：原则证据溯源

每条原则保存自己的推导类型和证据位置：

```yaml
- id: reframe-gravity-problems
  title: 接受不可改变的现实，重新设计可行动的问题
  statement: 将无法改变的条件视为边界，把精力转向可以设计的问题。
  extraction_type: explicit
  source_refs:
    - source_id: designing-your-life-en-2016
      chapter: 1
      section: Gravity Problems
      page: 15
      evidence_type: paraphrase
  applications:
    - 识别问题中哪些条件无法由自己改变
  boundaries:
    - 不要把暂时困难误判为绝对不可改变
  confidence: high
  review_status: reviewed
```

这层回答：“为什么可以把这句话归给这本书？”

原则的 `source_refs` 只指向书籍或其他内容来源。参考项目仅记录为实现影响；除非原则确实取自该项目，否则不要放入原则证据。

## 内容类型边界

知识包中的每个重要结论应标记为以下类型之一：

- `explicit`：作者在来源中明确表达。
- `inferred`：根据多个段落或章节归纳。
- `adapted`：为了实际应用而重写或扩展。
- `external`：来自原书之外的理论或资料。

`inferred` 和 `adapted` 不能伪装成作者原话。`external` 必须登记独立来源。

## 生成与维护规则

```text
输入书籍
  → 登记版本与来源
  → 生成书籍地图和概要
  → 提炼候选原则
  → 补充证据、边界和标签
  → 结构校验
  → 人工复核
  → 生成 principles.md 与 evidence.md
  → 按需生成书籍 Skill
```

维护时遵守：

1. 修改原则时只编辑 `principles.yaml`。
2. 修改后重新生成所有阅读版和书籍 Skill。
3. 校验所有 `source_id`、原则 ID 和证据位置是否有效。
4. 使用 `draft`、`reviewing`、`verified`、`published` 表示成熟度。
5. 书籍版本变化时创建新知识包，不覆盖旧版定位信息。

## Skill 与知识包的关系

通用 `extract-book-principles` Skill 负责“怎样处理书”；书籍知识包保存“处理后的内容”；独立书籍 Skill 负责“怎样把这本书用于具体任务”。

```text
通用提炼 Skill
      ↓ 生成
标准化书籍知识包
      ↓ 按需发布
一个或多个应用型书籍 Skill
```

简单书籍可以生成一个综合 Skill。方法复杂、包含多个独立练习的书，可以像 `life-design-coach` 一样拆成总控 Skill 与多个阶段 Skill，但这些 Skill 应从知识包生成或引用知识包，避免手工复制理论内容。

## 最小可行版本

第一版只实现：

1. `metadata.yaml`、`sources.yaml` 和 `principles.yaml` 的字段规范。
2. 从 `principles.yaml` 生成 `principles.md`。
3. 校验 ID、必要字段和来源引用。
4. 用一本书完成从提炼到人工复核的闭环。

跨书检索、自动生成多个 Skill 和复杂知识图谱放到样本书验证之后。
