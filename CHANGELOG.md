# 变更日志

每个条目列出版本号、日期和已测量的效果（如果有）。

## 2.2.0, 2026-10-04

- **重大**：中文场景的默认规则集从 ASD-STE100 衍生规则切换到中文技术表达规范（C01–C24，独立使用版 v1.0）。`skills/simple-english/SKILL.md` 与 `prompts/system-prompt.md` 重写为 C01–C24；新增 `skills/simple-english/references/cn-tech-spec.md`（24 条规则中文摘录）与 `skills/simple-english/references/cn-tech-examples.md`（练习 1–8 + 第 15–20 节正反对照）。
- 英文模式保留：用户明确要求英文并提到 ASD-STE100、STE、Simplified Technical English 或合规时，`references/strict-vocabulary.md` 与 `references/rule-catalog.md` 仍然生效。
- `output-styles/simple-english.md`、`README.md`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json` 的描述与版本号同步更新到 v2.2.0。
- `examples/before-after.md`、`src/hooks/`、`evals/`、`tools/ste-dictionary/`、`word-swaps.md`、`use-cases.md`、`rule-catalog.md`、`strict-vocabulary.md` 保留原状（适用于英文写作与代码检查）。
- 没有运行基准测试。已发布数字仍然描述 2.0.1 版本。

## 2.1.1, 2026-09-30

- 更改：从 Skill 中移除了违反自身规则的措辞。SKILL.md 中的 12 条文档规则不再使用加粗引导语。规则 11 不再使用"不是 X，而是 Y"这样的标题。参考文献列表、rule-catalog.md 标题和 word-swaps.md 中的四个单元格移除了破折号。规则内容本身没有变化。
- 移除：填充语和无来源的主张。SKILL.md 移除了"疲惫的机修工"、"本文件中的其他内容都不可或缺"和"最后阅读，首先应用"。use-cases.md 移除了"凌晨 2 点的压力读者"和"STE 降低错误率和成本"。rule-catalog.md 移除了"代理最常违反的是 1.7、1.11 和 1.13"。SKILL.md 示例现在标记为"AI 输出"而非"真实 AI 输出"，因为没有任何已提交的评估文件持有它。
- 更改：SKILL.md、`prompts/system-prompt.md` 和 `output-styles/simple-english.md` 中的句子"The same rule covers a fact, not just a word"现在以"Also name the host"开头。两份镜像文件保持字节一致。
- 没有运行基准测试。已发布的数字仍然描述 2.0.1 版本。

## 2.1.0, 2026-09-16

- 移除：回复的五句话上限。该规则已从 SKILL.md、输出样式、系统提示、自我检查、Stop hook 和 linter 中移除。用户反映多部分问题的回复变成了一段文字。对 2026-09-02 已提交的回复重新评分显示，该上限仅在 16 条回复中的 5 条中被触发，且这些回复中 18.9% 的句子超过 25 个单词，而发布版 2.0.0（无格式规则）的这一比例为 5.7%。该上限既未保持也未缩短句子。（#35）
- 更改：`reader_check()` 不再在 `visible_total` 中计算超限句子，因为该 Skill 不再要求五句话。已发布的回复数字从 406 降至 58（减少 86%）更新为从 218 降至 11（减少 95%），由 `python3 evals/check_numbers.py` 从相同原始文件重新计算。计数的类别现在是破折号、加粗、标题和项目符号。`sentences` 仍作为计数报告，但不是限制。

## 2.0.2, 2026-09-08

- 修复：PostToolUse hook 消息说"在交付前运行 SKILL.md 中的自我检查"。至少有一个测试工具将其理解为在安装文件夹中搜索文件的指令。它读取了这个而非运行已加载 Skill 中的检查。消息现在直接说明变更。（#31）

## 2.0.1, 2026-09-04 至 2026-09-06

- 围绕两个语域（文档和回复）重建了 Skill，此前一次审计发现旧基准测试测量的是对 linter 的服从度，而非读者实际看到的内容。SKILL.md 为 1,825 个 token。53 条规则目录移至 `references/rule-catalog.md`。可见回复缺陷（超限句子、破折号、加粗、标题、项目符号）在 claude-sonnet-4-6 的 16 条回复中从 406 降至 58。盲测法官在 16 对比较中 14 次偏好 2.0.1 而非 2.0.0。完整方法：`evals/results/rebuild-2026-09-02/RESULTS.md`。
- 添加 `evals/check_numbers.py`，从原始文件重新计算每个已发布数字，并在不匹配时使构建失败。接入 CI。
- 修复了 Codex hook 文件冲突：Claude Code 自动发现插件根目录下的 `hooks/hooks.json`，因此 Codex 配置移至 `.codex-plugin/hooks.json`。
- 修复：Markdown 中的表格行被 linter 整体清空，导致每个单元格内的内容免于所有检查。每个单元格现在都是独立的句子单元。
- 修复：PostToolUse hook 对 Claude 自身的内存和配置文件进行了 lint 检查。现在跳过 Claude 配置目录和 `SIMPLE_ENGLISH_LINT_EXCLUDE` glob 命名的任何路径。
- 修复：`claude-opus-4-8` 基准测试行（基线 1.05）未复现。使用干净的基线重新运行：3.64。旧文件移至 `evals/results/raw-superseded/`。
- 移除 `references/checklist.md`。没有任何内容加载它，其内容只是重复了自我检查、目录和 linter。
- 从一个已关闭的 pull request 中获取了 ASD-STE100 词表提取器和词汇选择 linter，但不包含提取的词表本身：标准禁止在未经 ASD 书面授权的情况下复制。用户从免费 PDF 的本地副本在 `tools/ste-dictionary/` 中构建词表。
- 在 linter 基准测试中添加了 claude-fable-5-1 和 claude-fable-5 行，以及七个 opencode 模型行。

## 2.0.0, 2026-09-01

- 将默认模式从严格的 ASD-STE100 强制执行转向 Plain：相同的结构规则，加上针对领域外读者的规则和回复语域，Strict 作为仅文档覆盖层保留。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/CHANGELOG.md -->
