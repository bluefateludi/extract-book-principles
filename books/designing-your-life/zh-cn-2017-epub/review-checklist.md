# 《斯坦福大学人生设计课》人工复核清单

当前知识包状态为 `reviewing`。下列 15 条原则由 AI 提炼，必须由人工对照已登记的私有 EPUB 逐条核验后，才能改为 `verified`。

## 逐条核验

每一行都需要确认四项：locator 能定位到原文；原则陈述被原文支持；提炼类型与置信度合理；应用和边界没有扩大原意。

| 状态 | 原则 ID | 定位 | 陈述 | 类型/置信度 | 应用/边界 | 复核备注 |
| --- | --- | --- | --- | --- | --- | --- |
| [ ] | `identify-the-right-problem-first` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `reframe-gravity-problems` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `assess-health-work-play-love` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `treat-balance-as-contextual` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `turn-dashboard-signals-into-experiments` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `align-work-and-life-views` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `track-engagement-and-energy` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `generate-before-judging` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `create-three-odyssey-plans` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `prototype-before-committing` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `understand-the-hiring-system` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `explore-opportunities-through-conversations` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `choose-then-move-forward` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `reframe-failures-for-learning` | [ ] | [ ] | [ ] | [ ] | |
| [ ] | `design-with-a-team` | [ ] | [ ] | [ ] | [ ] | |

## 放行条件

- 15 行全部完成，且不存在未解决的复核备注。
- 在本文件记录复核人、复核日期和 EPUB 的 SHA-256；该哈希必须与 `metadata.yaml` 一致。
- 全部原则通过后，将其 `review_status` 统一改为 `verified`，同时把 `metadata.yaml` 的 `processing.status` 改为 `verified` 并添加 `human_reviewed: true`；在此之前保持 `reviewing`。
- 重新生成 `principles.md`，执行完整测试与 `validate --check-generated`，确认未提交 EPUB、章节文本或大段引文。

复核人：待填写

复核日期：待填写

复核 EPUB SHA-256：`a546268af89a729df3dec8060ecf475a7f7072e9a00685b4208c66fcecf0b329`
