# 参考项目与研究

本文记录 `extract-book-principles` 的同类项目、方法来源和可借鉴设计。记录日期：2026-08-07。

## 直接参考：从书籍方法论生成 Skill

### life-design-coach

- 仓库：[TeigenZhang/life-design-coach](https://github.com/TeigenZhang/life-design-coach)
- 核对提交：[`ec9963f13f53f3e70943d9c2229cd5ccdcf036ac`](https://github.com/TeigenZhang/life-design-coach/tree/ec9963f13f53f3e70943d9c2229cd5ccdcf036ac)
- 许可证：MIT
- 原始方法：《Designing Your Life》，Bill Burnett、Dave Evans

这是目前最接近“单本书 → 多个应用型 Skill”的项目。它将人生设计方法拆成总控教练人格、八周计划、13 个阶段 Skill、进度状态和用户练习产物。

值得借鉴：

- 用总控规则统一角色、交互方式和阶段顺序。
- 将大型方法论拆成带前置条件的场景化 Skill。
- 明确每个练习的流程、硬约束、产出和下一步。
- 将公共方法与用户私人数据分离。

需要改进：

- 目前主要做到书籍级归因，缺少逐条概念对应的版次、章节和页码。
- 相同流程分散在 `PLAN.md`、`CLAUDE.md` 和多个 `SKILL.md` 中，需要手工同步。
- 本项目应让结构化知识包成为唯一事实来源，再自动生成阅读版和 Skill。

关键文件：

- [教练人格与总控规则](https://github.com/TeigenZhang/life-design-coach/blob/ec9963f13f53f3e70943d9c2229cd5ccdcf036ac/CLAUDE.md)
- [八周实践计划](https://github.com/TeigenZhang/life-design-coach/blob/ec9963f13f53f3e70943d9c2229cd5ccdcf036ac/PLAN.md)
- [人生仪表盘 Skill](https://github.com/TeigenZhang/life-design-coach/blob/ec9963f13f53f3e70943d9c2229cd5ccdcf036ac/.claude/skills/life-design-coach-dashboard/SKILL.md)
- [贡献和同步规则](https://github.com/TeigenZhang/life-design-coach/blob/ec9963f13f53f3e70943d9c2229cd5ccdcf036ac/CONTRIBUTING.md)

### life-design-skill

- 仓库：[chenhui0926/life-design-skill](https://github.com/chenhui0926/life-design-skill)
- 核对提交：[`4237c50e6dfd2e669417c8dc7b08326d79fc2d5e`](https://github.com/chenhui0926/life-design-skill/tree/4237c50e6dfd2e669417c8dc7b08326d79fc2d5e)
- 许可证：MIT
- 原始方法：《Designing Your Life》，Bill Burnett、Dave Evans

该项目采用一个主 `SKILL.md` 加一个理论参考文件的最小结构，接近“单本书 → 单个 Skill + 知识参考”。

值得借鉴：

- 将执行流程与背景理论分开，保持主 Skill 相对聚焦。
- 把书籍理念转换为连续对话和最终行动产物。
- 结构简单，容易安装和理解。

需要改进：

- 理论来源大多只记录作者或理论名称，没有完整书目信息。
- 关键概念没有逐条标注章节、页码或原文依据。
- 书籍理论、其他心理学理论和项目作者的扩展内容需要明确区分。

关键文件：

- [人生设计 Skill](https://github.com/chenhui0926/life-design-skill/blob/4237c50e6dfd2e669417c8dc7b08326d79fc2d5e/life-design/SKILL.md)
- [理论参考](https://github.com/chenhui0926/life-design-skill/blob/4237c50e6dfd2e669417c8dc7b08326d79fc2d5e/life-design/references/theory.md)

目前没有在这两个仓库中发现相互引用，因此不根据发布时间推断二者存在继承关系。

## 提炼方法参考

### Fabric / extract_wisdom

- 项目：[danielmiessler/Fabric](https://github.com/danielmiessler/Fabric)
- 模式：[extract_wisdom](https://github.com/danielmiessler/Fabric/blob/main/data/patterns/extract_wisdom/system.md)
- 许可证：MIT

`extract_wisdom` 从文本中提取概要、观点、洞察、引用、习惯、事实、参考资料和建议，是最接近“通用内容提炼器”的开源 Pattern。

可借鉴它的模块化 Pattern 和多类型信息提取；本项目需要进一步增加整书层级结构、稳定 ID、适用边界、版次信息和逐条证据。

### AI-Powered Study Plan and Book Summarization

- 项目：[Huzaifa-X/AI-Powered-Study-Planand-Book-Summarization](https://github.com/Huzaifa-X/AI-Powered-Study-Planand-Book-Summarization)
- 许可证：MIT

该项目按章节切分长书，先生成局部摘要，再合成为整书摘要。可借鉴其长文本分层处理方式，但其重点是摘要，不是原则知识包。

## 阅读、检索与交互参考

### Readwise

- 产品：[Readwise](https://readwise.io/)

聚合书籍和文章划线，支持标签、笔记、搜索、复习及导出。可借鉴来源位置保留、个人注释和长期复习体验。

### Glasp

- 产品：[Glasp](https://glasp.co/)

管理网页、PDF、YouTube 和 Kindle 划线，支持基于划线的 AI 问答，以及 Markdown、CSV 和 JSON 导出。可借鉴开放格式和 AI 可访问的个人阅读库设计。

### NotebookLM

- 产品：[Google NotebookLM](https://notebooklm.google/)

围绕用户提供的来源进行总结和问答。可借鉴来源约束和交互式研究方式，但本项目的知识包需要可离线保存、版本管理和跨 AI 使用。

## 研究与一手来源

### 递归总结整本书

- 论文：[Recursively Summarizing Books with Human Feedback](https://arxiv.org/abs/2109.10862)

论文采用“切分原文 → 总结小段 → 递归合并摘要”的方法处理整本书，并引入人类反馈。可借鉴层级摘要树、局部人工审核和从高层结论回溯原文的思路。

### Designing Your Life

- 出版商：[Penguin Random House](https://www.penguinrandomhouse.com/books/249885/designing-your-life-by-bill-burnett-and-dave-evans/)
- 作者：Bill Burnett、Dave Evans
- 出版年份：2016
- ISBN：`9781101875322`
- 官方机构：[Stanford Life Design Lab](https://lifedesignlab.stanford.edu/)

这是一手书目和课程来源。涉及中文译本时，应另外记录译者、出版社、年份和 ISBN，不能直接复用英文版页码。

### 相关理论来源

- 设计思维：[Stanford d.school](https://dschool.stanford.edu/stories/lets-stop-talking-about-the-design-process)
- 积极心理学：[Martin E. P. Seligman / UPenn Positive Psychology Center](https://ppc.sas.upenn.edu/people/martin-ep-seligman)
- 心流理论：Mihaly Csikszentmihalyi，《Flow: The Psychology of Optimal Experience》，1990，ISBN `0-06-016253-8`

引用相关理论时，应注明它来自原书、课程、学术理论还是项目作者的二次扩展，避免把所有内容都归给一本书。

## 本项目的溯源要求

后续新增参考项目时，至少记录：

- 项目名称和原始 URL。
- 核对日期；开源项目尽量固定到 commit SHA。
- 许可证。
- 借鉴的具体文件、结构或做法。
- 与本项目的相同点和差异。

后续新增书籍原则时，至少记录：

- 书名、作者、语言、版次、出版社、年份和 ISBN。
- 原则对应的章节、节标题及版本相关页码。
- `explicit`（作者明确提出）或 `inferred`（根据内容归纳）。
- 支持该原则的短证据、适用边界和可信度。
- AI 提炼版本、人工审核状态和最后修改时间。

参考项目用于学习结构和工作流，不替代对原书与一手资料的核验。
