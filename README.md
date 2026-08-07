# extract-book-principles

一个纯 Codex Skill：读取用户提供的书籍，提炼核心主旨、思想地图、关键原则、必要短引、AI 记忆句、误用边界和可执行实践，并默认沉淀为一份可长期保存的 `book-essence.md`。

Skill 不绑定 EPUB、Python、OCR 或格式转换工具。调用它的 AI 根据当前环境和源文件选择可用的 PDF、文档、终端、视觉或 OCR 能力，并对实际读取范围与不确定性保持诚实。

## 结构

```text
skills/extract-book-principles/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── book-essence-template.md
    └── quality-checklist.md

.agents/skills/extract-book-principles  # 仓库级发现入口
books/                                  # 已提炼的示例，不含原书
```

在 Codex 中调用 `$extract-book-principles` 并提供书籍或可访问位置即可。受版权保护的原书及可能还原全文的中间产物必须留在 `private/` 或其他不纳入版本控制的位置；不要提交原书、大段引文或全文转换结果。

`books/designing-your-life/zh-cn-2017-epub/book-essence.md` 是从旧知识包审慎合并而来的示例，保留原有提炼内容与审核状态，但不要求后续输出采用其 EPUB 技术定位。
