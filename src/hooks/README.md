# Simple English hooks 中文版

Claude Code 和 Codex 外掛包含一個 `SessionStart` hook。當會話啟動、恢復、清除或壓縮時，hook 載入 Simple English 寫作規則。你不需要命名 Skill。

hook 需要 Node.js。兩個外掛都用 `node` 命令執行 `src/hooks/simple-english-activate.js`。

## 安裝

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

Codex 會要求你在首次執行前審查並信任 hook。開啟 `/hooks` 批准。

## Hook 傳送的內容

Hook 將 `prompts/system-prompt.md` 的圍欄規則塊寫入標準輸出，約 3,500 個字元。頁面標題、貼上說明和精簡版變體不包含。完整 Skill `skills/simple-english/SKILL.md` 約 7,500 個字元，Claude Code 將 hook 輸出上限設為 10,000 個字元。超過上限的輸出寫入檔案，模型只得到預覽。精簡規則可以裝下，hook 命名完整 Skill 路徑以便模型為合規檢查或嚴格模式讀取它。

Codex 對 hook 上下文應用自己的上限。`.codex-plugin/hooks.json` 中的 `additionalContextLimit: 0` 設定關閉了溢位到磁碟閾值。它不移除上限。精簡規則可以裝下。

如果 hook 無法讀取提示檔案，它會嘗試下一個位置。如果每個位置都失敗，它列印一個簡短的備用規則集並以 0 退出。會話仍會啟動。

## 每個工具載入 hook 的位置

- Claude Code：`.claude-plugin/plugin.json` 中的 `hooks` 欄位。
- Codex：`.codex-plugin/hooks.json`，由 `.codex-plugin/plugin.json` 中的 `hooks` 欄位命名。市場目錄是 `.agents/plugins/marketplace.json`。

## 測試

從倉庫根目錄執行：

```bash
node --test src/hooks/simple-english-activate.test.js
```

## 諮詢性寫作檢查（Claude Code）

另外兩個 hook 在 Claude Code 下執行，都是諮詢性的。都不阻塞。

- `PostToolUse` 在 `Write` 和 `Edit` 上：當檔案是 Markdown 時，`src/hooks/lint_hook.py` 用 `evals/ste_lint.py` 檢查它，並向模型顯示違規的一行摘要。
- `Stop`：同一指令碼讀取最後回覆，並在回覆違反語域時新增系統訊息：破折號、加粗、標題、列表項、廢話開頭或結尾，或冗餘詞。

Codex 僅執行 `SessionStart` hook。用 `python3 src/hooks/test_lint_hook.py` 測試檢查。

## 檔案檢查跳過什麼

寫作規則覆蓋你為讀者寫的文件。它們不覆蓋 Agent 為自己保留的檔案，如記憶體檔案。在這樣的檔案中顯示違規摘要只是浪費 token。因此 `PostToolUse` 檢查跳過三組路徑：

- Claude 配置目錄下每個路徑。檢查讀取 `CLAUDE_CONFIG_DIR` 並回退到 `~/.claude`。
- 每個包含 `.claude` 目錄元件的路徑，例如 `my-project/.claude/agent-memory/reviewer/MEMORY.md`。你在 `.claude/` 下編寫的 Skill 或命令也被跳過。
- 每個匹配 `SIMPLE_ENGLISH_LINT_EXCLUDE` 中 glob 的路徑。

符號連結不能繞過跳過。檢查以兩種形式測試絕對路徑：原樣和解析符號連結後。任一形式的匹配都足以跳過。

`SIMPLE_ENGLISH_LINT_EXCLUDE` 包含 glob 模式，用平臺路徑分隔符分隔（Linux 和 macOS 用 `:`，Windows 用 `;`）。在模式中，`*` 也匹配 `/`。檢查將開頭的 `~` 展開為你的主目錄。

```bash
export SIMPLE_ENGLISH_LINT_EXCLUDE="$HOME/notes/*:*/CHANGELOG.md"
```

要關閉檔案檢查，將變數設為 `*`。`Stop` 回覆檢查保持開啟。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/src/hooks/README.md -->
