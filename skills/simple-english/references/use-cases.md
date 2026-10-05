# 文档以外的使用场景

STE 为飞机维护手册而构建。同样的属性转移到任何误读会造成损失的文本：一词一义、简短句子、条件优先命令。以下每种场景指明模式和适配。

## 错误消息和 CLI 输出

模式：程序性。错误消息是对正处于失败中的读者的指令。

模式：陈述发生了什么（一般过去时），陈述原因如果已知，给出修复的命令或条件。

> 错误前：Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials are properly configured and try again.
> 错误后：Connection to the database failed. The password for user `app` was not correct. Set `DB_PASSWORD` and connect again.

## 运维手册和标准操作程序

模式：程序性。值班运维手册是维护手册，而维护手册正是 STE 为之编写的文本类型。

- 每步都是祈使句，每步一条指令，条件优先。
- 警告在其步骤之前：命令优先，风险其次。
- 每句不超过 20 词。

## 故障报告和事后分析

模式：描述性，仅用一般过去时。完成时态的现在完成时（"we have identified"）隐藏了事情发生的时间。

> 错误前：We have identified an issue that may have impacted some users' ability to access the service.
> 错误后：Between 14:02 and 14:31 UTC, 12% of requests failed. A deploy at 14:00 removed the cache warmup step.

STE 禁止模糊表达如"may have impacted"。报告陈述已知内容，其余说"unknown"。

## 提交消息和 PR 描述

模式：祈使句标题，描述性正文。惯例已符合 STE。应用词替换和正文 25 词限制。删除"this PR aims to"。

## API 变更日志和发布说明

模式：描述性。可能时一条内容、一个变更、一句话。"Breaking:" 条目遵循警告模式，命令优先："Update your calls to `v2/users`. The `name` field split into `first_name` and `last_name`."

## AI 代理指令（提示、AGENTS.md、Skill）

模式：程序性。系统提示是对无法提问的读者的程序。

- 每句一条指令使每条规则可引用、难以半途而废。
- 一词一义防止模型将"check"、"verify"和"validate"视为三个操作。
- 条件优先（"If the build fails, stop"）胜过拖尾条件，模型会忽略拖尾条件。
- 不用"should"。模型将"should"视为可选。写"must"或删除规则。

## 支持宏和状态页更新

模式：描述性，25 词限制。这些消息的许多读者是母语非英语者。

> 错误前：We sincerely apologize for any inconvenience this may have caused.
> 错误后：The API was down for 18 minutes. Uploads made during this time were saved and will process today.

## 翻译和本地化准备

模式：严格。STE 如此编写以使母语非英语的维护人员能阅读英语手册。同样的规则为机器翻译准备文本。一词一义和完整语法（冠词、"that"）消除了译者必须猜测的许多歧义。

## UI 文字和空状态

模式：程序性，硬性长度限制。按钮和标签是技术名称，免于规则。正文遵循规则："No projects yet. Create a project to start."

## STE 不适用的地方

不要将 STE 用于营销页面、发布帖子、博客帖子或品牌写作。STE 删除说服力。用你自己的文风写那些文本，用 STE 写它们链接到的文档。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/use-cases.md -->
