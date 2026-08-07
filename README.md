# extract-book-principles

从书籍中提炼核心内容与可执行原则，将阅读转化为可理解、可追溯、可应用的行动指南。

## 项目目标

本项目同时服务人类读者与 AI：

1. 构建通用的书籍原则提炼 Skill，规范书籍解析、内容总结、原则提炼和质量检查流程。
2. 为每本书生成标准化知识包，既方便人类阅读，也方便 AI 检索、验证和应用。
3. 按需将高价值知识包发布为独立的书籍 Skill。

## 当前结构

```text
src/book_principles/       # 确定性的 EPUB、校验和渲染工具包
skills/                    # 通用书籍原则提炼 Skill 源目录
.agents/skills/            # Codex 仓库级 Skill 发现入口
books/                     # 每本书的标准化知识包
tests/                     # 结构与质量验证
```

项目采用“Python 工具包 + Skill + 知识包”分层：工具包执行确定性操作，Skill 负责提炼、分类和审核流程，知识包保存可追溯结果。

## 安装与使用

需要 Python 3.10 或更高版本：

```bash
python -m pip install -e .
book-principles inspect private/inputs/book.epub --chapter 1 --output private/chapter-1.json
book-principles validate books/<book-id>/<edition-id> --check-generated
book-principles render books/<book-id>/<edition-id>
```

源码检出但尚未安装时，可直接运行 Skill 中保留的兼容入口：

```bash
python skills/extract-book-principles/scripts/parse_epub.py private/inputs/book.epub --chapter 1
python skills/extract-book-principles/scripts/validate_book_package.py books/<book-id>/<edition-id> --check-generated
```

本仓库的 Skill 通过 `.agents/skills/extract-book-principles` 被 Codex 发现。0.1 版本定位为仓库级 Skill；未来需要独立分发时再打包为插件。

所有受版权保护的书籍和可能包含全文的解析输出必须放在 `private/` 下。常见电子书格式也由 `.gitignore` 默认拦截。

每个书籍知识包包含：

```text
metadata.yaml              # 书籍版本与处理状态
book-map.md                # 全书结构和论证脉络
summary.md                 # 人类友好的内容概要
principles.yaml            # AI 友好的结构化原则，作为唯一事实来源
principles.md              # 从 YAML 生成的人类阅读版
```

当前 MVP 将证据摘要与定位保存在 `principles.yaml`，并生成到 `principles.md`；独立的 `evidence.md` 留待完整样本闭环验证后再决定。

## 实施阶段

### 第一阶段：定义标准

- 确定知识包目录和字段规范。
- 定义原则的必要字段、来源类型和可信度等级。
- 建立防止重复、失真和断章取义的质量标准。

### 第二阶段：实现通用 Skill

- 创建 `extract-book-principles` Skill。
- 支持生成书籍地图、概要、原则和出处索引。
- 增加知识包结构校验工具。

### 第三阶段：完成样本书籍

- 选择一本结构清晰的书作为首个样本。
- 完成 AI 提炼和人工复核。
- 根据实际使用结果调整结构与流程。

### 第四阶段：发布与扩展

- 从知识包自动生成人类阅读版。
- 按需生成独立的书籍 Skill。
- 逐步支持跨书籍原则检索、比较与场景化应用。

## 维护原则

- 通用 Skill 维护方法，书籍知识包维护内容，发布 Skill 维护交付形式。
- Python 工具包维护确定性能力；Skill 脚本只保留兼容入口。
- `principles.yaml` 是原则内容的唯一事实来源，其他格式由它生成。
- 区分作者明确提出的原则与 AI 根据内容归纳的原则。
- 每条原则保留适用条件、边界和原书依据。
- 不在公开仓库提交完整的受版权保护书籍原文。

## 参考资料

- [双读者架构设计](docs/architecture.md)
- [参考项目与研究](docs/reference-projects.md)
