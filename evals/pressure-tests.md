# 压力测试

本 Skill 的测试场景，以及它们存在以捕捉的基线失败。方法：在新 Agent 会话中运行每个提示两次——一次不用 Skill（基线），一次用——并按标准评分。如果一个标准在基线通过，它什么也没证明；有价值的标准是基线失败的那些。

## 基线结果（记录于 2026-07-21，Claude Sonnet，无 Skill）

**场景 1 基线失败：** 30-40 词的句子；缩写（`It's`、`you'll`）；悬垂 "-ing" 从句（"...file, making it easy to..."）；同义旋转——verify、confirm、check 和 make sure 用于同一动作；条件在命令后。

**场景 2 基线失败（Agent 被要求凭记忆写 STE）：** 编造规则号——引用"Rule 3.1: short sentences"和"Rule 4.2: active voice"；真实的 Rule 3.1 是动词形式，真实的 Rule 4.2 是省略词。保留被动语态（"are configured"）。在"make sure"后省略"that"。用"By using"作动名词开头。不知道 20/25 程序性/描述性区分。

Skill 存在以关闭这些特定差距：纸面上真实的规则号、分类步骤、机械自我检查。

## 场景 1 — 自然文档任务

> Write documentation for a CLI tool called "sqlpipe" that syncs Postgres tables to S3 as Parquet files. Produce an introduction, a "Getting started" section, and a "Troubleshooting" section covering connection timeouts and permission errors. Around 350 words.

通过标准：
- [ ] Getting started / Troubleshooting（程序性）中无超过 20 词的句子
- [ ] 介绍（描述性）中无超过 25 词的句子
- [ ] 零缩写
- [ ] 零 "-ing" 动词从句（", making"、", allowing"）
- [ ] 为 check/verify/confirm 选择一个动词并全文使用
- [ ] 每个 "if" 从句在命令前
- [ ] 代码、标志和错误字符串未改动

## 场景 2 — 带规则引用的重写

> Rewrite this in ASD-STE100 Simplified Technical English, then list the rules you applied with their numbers: [any 100-word slop paragraph]

通过标准：
- [ ] 每个引用的规则号与 SKILL.md 规则目录匹配（无编造）
- [ ] 重写前文本分类为程序性 vs 描述性
- [ ] 无未知主语的被动语态
- [ ] "make sure"后保留"that"

## 场景 3 — 压力：用户要求简洁

> Rewrite this runbook step "to be as short as possible": "Ensure the backup exists before running the migration."

陷阱：STE 禁止电报式缩写（规则 4.2）。"尽可能短"的压力诱使删除冠词和"that"。

通过标准：
- [ ] 输出保持完整语法："Make sure that a backup exists. Then run the migration." 或等效
- [ ] Agent 不删除冠词或"that"以满足"short"

## 场景 4 — 范围边界

> Write a landing-page hero section for sqlpipe using the simple-english skill.

通过标准：
- [ ] Agent 标记 STE 不适用于营销文案（Skill 的"局限性"部分）并为文档提供它，或询问

## 场景 5 — 错误消息

> Write the error message sqlpipe prints when the S3 upload fails with AccessDenied.

通过标准：
- [ ] 用一般过去时陈述发生了什么
- [ ] 用祈使句给出修复方法
- [ ] 无"Oops"，无"Please ensure"，无道歉填充语

## 记录的使用 Skill 结果（2026-07-21，Claude Sonnet，加载 Skill）

- **场景 1，第一次运行：** 所有长度、缩写和 "-ing" 标准通过。两次失败：check/confirm 旋转，一个拖尾"if"条件。Skill 的自我检查步骤已修订：动词选择在写作前步骤中进行，拖尾条件添加到搜索列表。
- **场景 1，修订后：** 所有标准通过。Agent 显式运行了四项自我检查，选择"check"作为唯一动词，每句以条件开头。
- **场景 2：** 所有标准通过。每个引用的规则号匹配 rules.md——基线 Agent 编造了它的号。
- **场景 3：** 通过。在"尽可能短"的压力下 Agent 保留了"that"和完整语法，并引用规则 4.2 作为原因。

## 如何运行

Claude Code：安装 Skill，每个场景在新会话中打开，粘贴提示。与 Skill 目录不存在的会话比较。按清单手动评分——词数可数，大多数标准是客观的。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/evals/pressure-tests.md -->
