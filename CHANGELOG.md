# 變更日誌

每個條目列出版本號、日期和已測量的效果（如果有）。

## 2.2.0, 2026-10-04

- **重大**：中文場景的預設規則集從 ASD-STE100 衍生規則切換到中文技術表達規範（C01–C24，獨立使用版 v1.0）。`skills/simple-english/SKILL.md` 與 `prompts/system-prompt.md` 重寫為 C01–C24；新增 `skills/simple-english/references/cn-tech-spec.md`（24 條規則中文摘錄）與 `skills/simple-english/references/cn-tech-examples.md`（練習 1–8 + 第 15–20 節正反對照）。
- 英文模式保留：使用者明確要求英文並提到 ASD-STE100、STE、Simplified Technical English 或合規時，`references/strict-vocabulary.md` 與 `references/rule-catalog.md` 仍然生效。
- `output-styles/simple-english.md`、`README.md`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json` 的描述與版本號同步更新到 v2.2.0。
- `examples/before-after.md`、`src/hooks/`、`evals/`、`tools/ste-dictionary/`、`word-swaps.md`、`use-cases.md`、`rule-catalog.md`、`strict-vocabulary.md` 保留原狀（適用於英文寫作與程式碼檢查）。
- 沒有執行基準測試。已釋出數字仍然描述 2.0.1 版本。

## 2.1.1, 2026-09-30

- 更改：從 Skill 中移除了違反自身規則的措辭。SKILL.md 中的 12 條文件規則不再使用加粗引導語。規則 11 不再使用"不是 X，而是 Y"這樣的標題。參考文獻列表、rule-catalog.md 標題和 word-swaps.md 中的四個單元格移除了破折號。規則內容本身沒有變化。
- 移除：填充語和無來源的主張。SKILL.md 移除了"疲憊的機修工"、"本檔案中的其他內容都不可或缺"和"最後閱讀，首先應用"。use-cases.md 移除了"凌晨 2 點的壓力讀者"和"STE 降低錯誤率和成本"。rule-catalog.md 移除了"代理最常違反的是 1.7、1.11 和 1.13"。SKILL.md 示例現在標記為"AI 輸出"而非"真實 AI 輸出"，因為沒有任何已提交的評估檔案持有它。
- 更改：SKILL.md、`prompts/system-prompt.md` 和 `output-styles/simple-english.md` 中的句子"The same rule covers a fact, not just a word"現在以"Also name the host"開頭。兩份映象檔案保持位元組一致。
- 沒有執行基準測試。已釋出的數字仍然描述 2.0.1 版本。

## 2.1.0, 2026-09-16

- 移除：回覆的五句話上限。該規則已從 SKILL.md、輸出樣式、系統提示、自我檢查、Stop hook 和 linter 中移除。使用者反映多部分問題的回覆變成了一段文字。對 2026-09-02 已提交的回覆重新評分顯示，該上限僅在 16 條回覆中的 5 條中被觸發，且這些回覆中 18.9% 的句子超過 25 個單詞，而釋出版 2.0.0（無格式規則）的這一比例為 5.7%。該上限既未保持也未縮短句子。（#35）
- 更改：`reader_check()` 不再在 `visible_total` 中計算超限句子，因為該 Skill 不再要求五句話。已釋出的回覆數字從 406 降至 58（減少 86%）更新為從 218 降至 11（減少 95%），由 `python3 evals/check_numbers.py` 從相同原始檔案重新計算。計數的類別現在是破折號、加粗、標題和專案符號。`sentences` 仍作為計數報告，但不是限制。

## 2.0.2, 2026-09-08

- 修復：PostToolUse hook 訊息說"在交付前執行 SKILL.md 中的自我檢查"。至少有一個測試工具將其理解為在安裝資料夾中搜尋檔案的指令。它讀取了這個而非執行已載入 Skill 中的檢查。訊息現在直接說明變更。（#31）

## 2.0.1, 2026-09-04 至 2026-09-06

- 圍繞兩個語域（文件和回覆）重建了 Skill，此前一次審計發現舊基準測試測量的是對 linter 的服從度，而非讀者實際看到的內容。SKILL.md 為 1,825 個 token。53 條規則目錄移至 `references/rule-catalog.md`。可見回覆缺陷（超限句子、破折號、加粗、標題、專案符號）在 claude-sonnet-4-6 的 16 條回覆中從 406 降至 58。盲測法官在 16 對比較中 14 次偏好 2.0.1 而非 2.0.0。完整方法：`evals/results/rebuild-2026-09-02/RESULTS.md`。
- 新增 `evals/check_numbers.py`，從原始檔案重新計算每個已釋出數字，並在不匹配時使構建失敗。接入 CI。
- 修復了 Codex hook 檔案衝突：Claude Code 自動發現外掛根目錄下的 `hooks/hooks.json`，因此 Codex 配置移至 `.codex-plugin/hooks.json`。
- 修復：Markdown 中的表格行被 linter 整體清空，導致每個單元格內的內容免於所有檢查。每個單元格現在都是獨立的句子單元。
- 修復：PostToolUse hook 對 Claude 自身的記憶體和配置檔案進行了 lint 檢查。現在跳過 Claude 配置目錄和 `SIMPLE_ENGLISH_LINT_EXCLUDE` glob 命名的任何路徑。
- 修復：`claude-opus-4-8` 基準測試行（基線 1.05）未復現。使用乾淨的基線重新執行：3.64。舊檔案移至 `evals/results/raw-superseded/`。
- 移除 `references/checklist.md`。沒有任何內容載入它，其內容只是重複了自我檢查、目錄和 linter。
- 從一個已關閉的 pull request 中獲取了 ASD-STE100 詞表提取器和詞彙選擇 linter，但不包含提取的詞表本身：標準禁止在未經 ASD 書面授權的情況下複製。使用者從免費 PDF 的本地副本在 `tools/ste-dictionary/` 中構建詞表。
- 在 linter 基準測試中新增了 claude-fable-5-1 和 claude-fable-5 行，以及七個 opencode 模型行。

## 2.0.0, 2026-09-01

- 將預設模式從嚴格的 ASD-STE100 強制執行轉向 Plain：相同的結構規則，加上針對領域外讀者的規則和回覆語域，Strict 作為僅文件覆蓋層保留。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/CHANGELOG.md -->
