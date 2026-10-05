# Simple English hooks 中文版

Claude Code 和 Codex 插件包含一个 `SessionStart` hook。当会话启动、恢复、清除或压缩时，hook 加载 Simple English 写作规则。你不需要命名 Skill。

hook 需要 Node.js。两个插件都用 `node` 命令运行 `src/hooks/simple-english-activate.js`。

## 安装

Claude Code:

```bash
claude plugin marketplace add TranChinese/SimpleEnglish-zh
claude plugin install simple-english@simple-english
```

Codex:

```bash
codex plugin marketplace add TranChinese/SimpleEnglish-zh
codex plugin add simple-english@simple-english
```

Codex 会要求你在首次运行前审查并信任 hook。打开 `/hooks` 批准。

## Hook 发送的内容

Hook 将 `prompts/system-prompt.md` 的围栏规则块写入标准输出，约 3,500 个字符。页面标题、粘贴说明和精简版变体不包含。完整 Skill `skills/simple-english/SKILL.md` 约 7,500 个字符，Claude Code 将 hook 输出上限设为 10,000 个字符。超过上限的输出写入文件，模型只得到预览。精简规则可以装下，hook 命名完整 Skill 路径以便模型为合规检查或严格模式读取它。

Codex 对 hook 上下文应用自己的上限。`.codex-plugin/hooks.json` 中的 `additionalContextLimit: 0` 设置关闭了溢出到磁盘阈值。它不移除上限。精简规则可以装下。

如果 hook 无法读取提示文件，它会尝试下一个位置。如果每个位置都失败，它打印一个简短的备用规则集并以 0 退出。会话仍会启动。

## 每个工具加载 hook 的位置

- Claude Code：`.claude-plugin/plugin.json` 中的 `hooks` 字段。
- Codex：`.codex-plugin/hooks.json`，由 `.codex-plugin/plugin.json` 中的 `hooks` 字段命名。市场目录是 `.agents/plugins/marketplace.json`。

## 测试

从仓库根目录运行：

```bash
node --test src/hooks/simple-english-activate.test.js
```

## 咨询性写作检查（Claude Code）

另外两个 hook 在 Claude Code 下运行，都是咨询性的。都不阻塞。

- `PostToolUse` 在 `Write` 和 `Edit` 上：当文件是 Markdown 时，`src/hooks/lint_hook.py` 用 `evals/ste_lint.py` 检查它，并向模型显示违规的一行摘要。
- `Stop`：同一脚本读取最后回复，并在回复违反语域时添加系统消息：破折号、加粗、标题、列表项、废话开头或结尾，或冗余词。

Codex 仅运行 `SessionStart` hook。用 `python3 src/hooks/test_lint_hook.py` 测试检查。

## 文件检查跳过什么

写作规则覆盖你为读者写的文档。它们不覆盖 Agent 为自己保留的文件，如内存文件。在这样的文件中显示违规摘要只是浪费 token。因此 `PostToolUse` 检查跳过三组路径：

- Claude 配置目录下每个路径。检查读取 `CLAUDE_CONFIG_DIR` 并回退到 `~/.claude`。
- 每个包含 `.claude` 目录组件的路径，例如 `my-project/.claude/agent-memory/reviewer/MEMORY.md`。你在 `.claude/` 下编写的 Skill 或命令也被跳过。
- 每个匹配 `SIMPLE_ENGLISH_LINT_EXCLUDE` 中 glob 的路径。

符号链接不能绕过跳过。检查以两种形式测试绝对路径：原样和解析符号链接后。任一形式的匹配都足以跳过。

`SIMPLE_ENGLISH_LINT_EXCLUDE` 包含 glob 模式，用平台路径分隔符分隔（Linux 和 macOS 用 `:`，Windows 用 `;`）。在模式中，`*` 也匹配 `/`。检查将开头的 `~` 展开为你的主目录。

```bash
export SIMPLE_ENGLISH_LINT_EXCLUDE="$HOME/notes/*:*/CHANGELOG.md"
```

要关闭文件检查，将变量设为 `*`。`Stop` 回复检查保持开启。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/src/hooks/README.md -->
