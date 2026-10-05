# Simple English 中文版

让你的 AI 像中文技术作者一样思考：保留事实与逻辑边界，区分事实、推断与未知，不补造信息、命令、路径或恢复步骤，指明执行者，条件先于动作，保护机器可读内容。

一个让 LLM 按中文技术表达规范（C01–C24）撰写或改写中文技术文档的 Agent Skill。中文是默认语域；当用户明确要求英文并提到 ASD-STE100、STE 时切换到英文 STE 词典。默认面向普通读者，需要时切换为严格的 STE 模式。

## 什么是 Simple English 中文版

Simple English 中文版是一个 Agent Skill，让 AI 助手（Claude Code、Cursor、VS Code Copilot、OpenAI Codex、Gemini CLI、Goose、OpenCode 等支持 Agent Skills 标准的工具）按 [中文技术表达规范（C01–C24）](skills/simple-english/references/cn-tech-spec.md) 撰写或改写中文技术文本。规则目标是让读者准确理解信息、判断适用条件，并在需要时正确操作：保留事实与逻辑边界，区分事实、推断与未知，不补造信息、命令、路径或恢复方法，一个概念一个术语，指明执行者、条件先于动作、保护机器可读内容。

一句话：让 AI 写出能让读者准确执行与判断的中文技术文档的 Agent Skill。

## 适用场景

- 代码改动说明：变更事实、验证范围、未做验证。
- 接口文档与状态消息：不补造字段、状态码、轮询间隔。
- 操作手册：必要条件与风险先于动作，可观察的判断条件。
- 排障报告与故障复盘：区分现象、假设、检查、结论。
- 概念解释：逐步展开，类比必须说明边界。
- 错误消息与 UI 文字：系统行为不伪装成人工步骤。

完整规则见 [`skills/simple-english/SKILL.md`](skills/simple-english/SKILL.md)。练习与正反对照见 [`skills/simple-english/references/cn-tech-examples.md`](skills/simple-english/references/cn-tech-examples.md)。

## 安装

### 方式一：仅安装 Skill（适用于 Claude Code、Cursor 等）

使用 [skills CLI](https://github.com/vercel-labs/skills)：

```bash
npx skills add TranChinese/SimpleEnglish-zh
```

这仅安装 Skill，不安装会话 hook 或输出样式。如果不使用 Claude Code 插件，设置 `outputStyle` 为 `simple-english:simple-english` 无效。

### 方式二：安装 Claude Code 插件（含会话 hook 和输出样式）

```bash
claude plugin marketplace add TranChinese/SimpleEnglish-zh
claude plugin install simple-english@simple-english
```

输出样式名为 `simple-english:simple-english`。短名称无法解析。在 `/config` 的 Output style 下选择，或在 `~/.claude/settings.json` 中添加 `{"outputStyle": "simple-english:simple-english"}`。

### 方式三：安装 Codex 插件（含会话 hook）

```bash
codex plugin marketplace add TranChinese/SimpleEnglish-zh
codex plugin add simple-english@simple-english
```

Codex 首次运行前会询问你是否信任 hook。请打开 `/hooks` 批准。Hook 需要 Node.js。详见 [`src/hooks/README.md`](src/hooks/README.md)。

### 方式四：无 Skill 支持

将 [`prompts/system-prompt.md`](prompts/system-prompt.md) 中的规则块粘贴到你的系统提示、`AGENTS.md` 或 `.cursorrules` 中。文件末尾提供了精简版。

然后直接提出任何技术写作需求，或说「按中文技术表达规范改写」「用 C01–C24 重写」。

## 效果示例

左侧是未经处理的真实 Claude 输出。右侧是加载 Skill 后的同一模型输出。

| 不使用 Skill | 使用 Skill |
|---|---|
| 利用 sqlpipe 的强大架构，用户可以无缝地将 Postgres 表同步到 S3，配置开销极小。开始之前，你应该确保 AWS 凭证已正确配置——这对于避免后续令人沮丧的权限问题至关重要。 | sqlpipe 将 Postgres 表复制到 S3。它需要一个配置文件。开始之前，确认 AWS 凭证正确。如果凭证错误，S3 因权限错误拒绝上传。 |

更多重写示例见 [`examples/before-after.md`](examples/before-after.md)：涵盖 README、运维手册、故障报告、错误消息、发布说明等。

## 规则体系

[`SKILL.md`](skills/simple-english/SKILL.md) 中有两套规则：中文文档规则（24 条，C01–C24）+ 中文回复规则（9 条）。完整规则与术语约定在 [`cn-tech-spec.md`](skills/simple-english/references/cn-tech-spec.md)。Issue 9 的 53 条英文 STE 编号规则位于 [`rule-catalog.md`](skills/simple-english/references/rule-catalog.md)，用于英文写作的 Strict 模式。

### 中文文档规则（C01–C24，按场景分组）

- 正确性与词语（C01–C06）：保留事实边界、区分事实/推断/未知、不补造信息、一个概念一个术语、按语境判断词义、保留并解释专业术语。
- 句子与关系（C07–C12）：指明执行者、一句一个关系、写清逻辑、明确否定、拆开长定语、用具体动作词。
- 概念解释（C13–C16）：从读者问题展开、每段一主题、类比说明边界、区分改变与证据。
- 操作说明（C17–C20）：必要条件与风险先于动作、一步一操作、可观察判断条件、具体风险提示。
- 故障排查（C21–C22）：区分现象假设检查结论、优先低风险检查。
- 格式与交付（C23–C24）：保护机器可读内容、复查语义与任务可用性。

### 中文回复规则

| 规则 | 消除内容 |
|---|---|
| 答案或结果放第一句 | 「好的」「当然」「好问题」 |
| 用散文，不用标题/项目符号/加粗/表格 | 一句话答案周围堆积的格式 |
| 术语首次出现用几个词解释 | 读者必须查的行话 |
| 不补造未知信息与恢复方法 | AI 幻觉 |
| 不引用开场白与结束语 | 「希望有帮助」「如有需要再问」 |
| 条件与必要前提放动作前 | 读者执行时太晚才读到的条件 |

### 英文模式

当用户明确要求英文并提到 ASD-STE100、STE、Simplified Technical English 或合规时启用。规则见 [`strict-vocabulary.md`](skills/simple-english/references/strict-vocabulary.md) 与 [`rule-catalog.md`](skills/simple-english/references/rule-catalog.md)。

## 基准测试

下方每个数字都由 `python3 evals/check_numbers.py` 从已提交的原始文件重新计算，CI 在每次推送时运行。所有 Claude 运行：claude-sonnet-4-6，low effort，不加载设置。评判模型是 Claude text 上的 Claude 模型，因此可能存在家族偏见。

**下列数字描述 2.0.1 版本。v2.2.0 未运行基准测试**，因此这些数字不代表中文规则集的效果；中文场景的效果尚未测量。

**回复测试**（8 个含行话术语的聊天问题，两次运行）——与不使用 Skill 相比，2.0.1 减少了 **95% 的可见缺陷**（破折号、加粗、标题、项目符号）：218 → 11。

| 条件 | 词数 | 句子数 | 破折号 | 加粗 | 标题 | 项目符号 |
|---|---:|---:|---:|---:|---:|---:|
| 无 Skill | 216 | 16.8 | 62 | 79 | 25 | 52 |
| 2.0.0 | 184 | 14.4 | 43 | 72 | 4 | 52 |
| 2.0.1 | 146 | 7.9 | 5 | 2 | 0 | 4 |

在 gpt-4.1-mini 上，相同 8 个问题从每 8 条回复 23 个句子、64 个加粗、101 个项目符号。使用 2.0.1 后降至 5.2 个句子，零格式。

**文档测试**（8 个 sqlpipe 写作任务，用 STE linter 评分）——在此模型上每次运行变化约 0.5，请将行视为「持平或更好」，而非排名。

| 条件 | 违规/100词 | 减少幅度 |
|---|---:|---:|
| 无 Skill | 4.09 | |
| 1.3.0 | 2.11 | 48% |
| 2.0.0 | 1.70 | 58% |
| 2.0.1 | 0.91 | 78% |

Linter 历史：9 个 Claude 模型（144 次生成）的 linter 违规减少 81.3%。详见 [`evals/results/RESULTS.md`](evals/results/RESULTS.md)。

## 常见问题

**这能让输出获得中文技术表达规范认证吗？** 没有「认证」一说。本规范是独立可执行的规则集，按 C01–C24 自查即可。

**能让输出获得 STE 认证吗？** 不能。没有任何工具能获得认证，因为 ASD 不对任何工具进行认证。Strict 模式最接近。逐词的裁定见官方标准（[免费下载](https://www.asd-ste100.org/request.html)）。

**我的文档会听起来像机器人吗？** 中文文档规则要求保真与明确执行者，因此听起来更像工程手册：平淡但不可能被误读。博客文章请保持你的文风。

**为什么不直接提示「写得清楚点」？** 「清楚」是一种观点。「不补造恢复步骤」「不把系统行为写成人工步骤」「C23 保护机器可读内容」是规格。Agent 遵循规格。

**与 1.x 系列的关系？** v2.0 起默认采用 Plain 模式（响应域外读者）。v2.2.0 起中文场景默认采用中文技术表达规范 C01–C24；英文模式仍保留 ASD-STE100。

**词表检查器在哪里？** `evals/ste_lint.py` 测量机械规则，看不到词汇选择。[`tools/ste-dictionary/`](tools/ste-dictionary/README.md) 包含一个提取器，从你自己的免费 Issue 9 PDF 副本构建英文 STE 词表。Linter 读取这些词表。仓库附带工具，不附带词典内容，因为标准禁止在未经 ASD 书面授权的情况下复制。

## 贡献

欢迎提交 Issue 提问和报告 Bug。Pull request 欢迎。改变已发布数字的更改必须附带原始文件，且 `python3 evals/check_numbers.py` 必须通过。在推送前运行 `python3 evals/ste_lint.py --self-test`。在 PR 中说明 Agent 是否写了代码，不要添加归属 trailers。

## 许可证

MIT 许可证。本仓库为教学目的复述规则，不复制任何规范文本或词典内容。

**非官方翻译项目**，与 ASD 或 STEMG 无关联。ASD-STE100 是 ASD 的注册商标。中文字面引用按「合理使用」注明来源；不在产品中再分发原始 Subtitle 数据。

<!-- 来源：E:\ChromeDownload\中文技术表达规范.pdf_by_PaddleOCR-VL-1.6.md（C01–C24 + 第 27 节精简指令） -->