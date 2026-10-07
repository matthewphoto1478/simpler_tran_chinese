# Simple English 中文版

讓你的 AI 像中文技術作者一樣思考：保留事實與邏輯邊界，區分事實、推斷與未知，不補造資訊、命令、路徑或恢復步驟，指明執行者，條件先於動作，保護機器可讀內容。

一個讓 LLM 按中文技術表達規範（C01–C24）撰寫或改寫中文技術文件的 Agent Skill。中文是預設語域；當使用者明確要求英文並提到 ASD-STE100、STE 時切換到英文 STE 詞典。預設面向普通讀者，需要時切換為嚴格的 STE 模式。

## 什麼是 Simple English 中文版

Simple English 中文版是一個 Agent Skill，讓 AI 助手（Claude Code、Cursor、VS Code Copilot、OpenAI Codex、Gemini CLI、Goose、OpenCode 等支援 Agent Skills 標準的工具）按 [中文技術表達規範（C01–C24）](skills/simple-english/references/cn-tech-spec.md) 撰寫或改寫中文技術文字。規則目標是讓讀者準確理解資訊、判斷適用條件，並在需要時正確操作：保留事實與邏輯邊界，區分事實、推斷與未知，不補造資訊、命令、路徑或恢復方法，一個概念一個術語，指明執行者、條件先於動作、保護機器可讀內容。

一句話：讓 AI 寫出能讓讀者準確執行與判斷的中文技術文件的 Agent Skill。

## 適用場景

- 程式碼改動說明：變更事實、驗證範圍、未做驗證。
- 介面文件與狀態訊息：不補造欄位、狀態碼、輪詢間隔。
- 操作手冊：必要條件與風險先於動作，可觀察的判斷條件。
- 排障報告與故障覆盤：區分現象、假設、檢查、結論。
- 概念解釋：逐步展開，類比必須說明邊界。
- 錯誤訊息與 UI 文字：系統行為不偽裝成人工步驟。

完整規則見 [`skills/simple-english/SKILL.md`](skills/simple-english/SKILL.md)。練習與正反對照見 [`skills/simple-english/references/cn-tech-examples.md`](skills/simple-english/references/cn-tech-examples.md)。

## 安裝

### 方式一：僅安裝 Skill（適用於 Claude Code、Cursor 等）

使用 [skills CLI](https://github.com/vercel-labs/skills)：

```bash
npx skills add TranChinese/SimpleEnglish-zh
```

這僅安裝 Skill，不安裝會話 hook 或輸出樣式。如果不使用 Claude Code 外掛，設定 `outputStyle` 為 `simple-english:simple-english` 無效。

### 方式二：安裝 Claude Code 外掛（含會話 hook 和輸出樣式）

```bash
claude plugin marketplace add TranChinese/SimpleEnglish-zh
claude plugin install simple-english@simple-english
```

輸出樣式名為 `simple-english:simple-english`。短名稱無法解析。在 `/config` 的 Output style 下選擇，或在 `~/.claude/settings.json` 中新增 `{"outputStyle": "simple-english:simple-english"}`。

### 方式三：安裝 Codex 外掛（含會話 hook）

```bash
codex plugin marketplace add TranChinese/SimpleEnglish-zh
codex plugin add simple-english@simple-english
```

Codex 首次執行前會詢問你是否信任 hook。請開啟 `/hooks` 批准。Hook 需要 Node.js。詳見 [`src/hooks/README.md`](src/hooks/README.md)。

### 方式四：無 Skill 支援

將 [`prompts/system-prompt.md`](prompts/system-prompt.md) 中的規則塊貼上到你的系統提示、`AGENTS.md` 或 `.cursorrules` 中。檔案末尾提供了精簡版。

然後直接提出任何技術寫作需求，或說「按中文技術表達規範改寫」「用 C01–C24 重寫」。

## 效果示例

左側是未經處理的真實 Claude 輸出。右側是載入 Skill 後的同一模型輸出。

| 不使用 Skill | 使用 Skill |
|---|---|
| 利用 sqlpipe 的強大架構，使用者可以無縫地將 Postgres 表同步到 S3，配置開銷極小。開始之前，你應該確保 AWS 憑證已正確配置——這對於避免後續令人沮喪的許可權問題至關重要。 | sqlpipe 將 Postgres 表複製到 S3。它需要一個配置檔案。開始之前，確認 AWS 憑證正確。如果憑證錯誤，S3 因許可權錯誤拒絕上傳。 |

更多重寫示例見 [`examples/before-after.md`](examples/before-after.md)：涵蓋 README、運維手冊、故障報告、錯誤訊息、釋出說明等。

## 規則體系

[`SKILL.md`](skills/simple-english/SKILL.md) 中有兩套規則：中文文件規則（24 條，C01–C24）+ 中文回覆規則（9 條）。完整規則與術語約定在 [`cn-tech-spec.md`](skills/simple-english/references/cn-tech-spec.md)。Issue 9 的 53 條英文 STE 編號規則位於 [`rule-catalog.md`](skills/simple-english/references/rule-catalog.md)，用於英文寫作的 Strict 模式。

### 中文文件規則（C01–C24，按場景分組）

- 正確性與詞語（C01–C06）：保留事實邊界、區分事實/推斷/未知、不補造資訊、一個概念一個術語、按語境判斷詞義、保留並解釋專業術語。
- 句子與關係（C07–C12）：指明執行者、一句一個關係、寫清邏輯、明確否定、拆開長定語、用具體動作詞。
- 概念解釋（C13–C16）：從讀者問題展開、每段一主題、類比說明邊界、區分改變與證據。
- 操作說明（C17–C20）：必要條件與風險先於動作、一步一操作、可觀察判斷條件、具體風險提示。
- 故障排查（C21–C22）：區分現象假設檢查結論、優先低風險檢查。
- 格式與交付（C23–C24）：保護機器可讀內容、複查語義與任務可用性。

### 中文回覆規則

| 規則 | 消除內容 |
|---|---|
| 答案或結果放第一句 | 「好的」「當然」「好問題」 |
| 用散文，不用標題/專案符號/加粗/表格 | 一句話答案周圍堆積的格式 |
| 術語首次出現用幾個詞解釋 | 讀者必須查的行話 |
| 不補造未知資訊與恢復方法 | AI 幻覺 |
| 不引用開場白與結束語 | 「希望有幫助」「如有需要再問」 |
| 條件與必要前提放動作前 | 讀者執行時太晚才讀到的條件 |

### 英文模式

當使用者明確要求英文並提到 ASD-STE100、STE、Simplified Technical English 或合規時啟用。規則見 [`strict-vocabulary.md`](skills/simple-english/references/strict-vocabulary.md) 與 [`rule-catalog.md`](skills/simple-english/references/rule-catalog.md)。

## 基準測試

下方每個數字都由 `python3 evals/check_numbers.py` 從已提交的原始檔案重新計算，CI 在每次推送時執行。所有 Claude 執行：claude-sonnet-4-6，low effort，不載入設定。評判模型是 Claude text 上的 Claude 模型，因此可能存在家族偏見。

**下列數字描述 2.0.1 版本。v2.2.0 未執行基準測試**，因此這些數字不代表中文規則集的效果；中文場景的效果尚未測量。

**回覆測試**（8 個含行話術語的聊天問題，兩次執行）——與不使用 Skill 相比，2.0.1 減少了 **95% 的可見缺陷**（破折號、加粗、標題、專案符號）：218 → 11。

| 條件 | 詞數 | 句子數 | 破折號 | 加粗 | 標題 | 專案符號 |
|---|---:|---:|---:|---:|---:|---:|
| 無 Skill | 216 | 16.8 | 62 | 79 | 25 | 52 |
| 2.0.0 | 184 | 14.4 | 43 | 72 | 4 | 52 |
| 2.0.1 | 146 | 7.9 | 5 | 2 | 0 | 4 |

在 gpt-4.1-mini 上，相同 8 個問題從每 8 條回覆 23 個句子、64 個加粗、101 個專案符號。使用 2.0.1 後降至 5.2 個句子，零格式。

**文件測試**（8 個 sqlpipe 寫作任務，用 STE linter 評分）——在此模型上每次執行變化約 0.5，請將行視為「持平或更好」，而非排名。

| 條件 | 違規/100詞 | 減少幅度 |
|---|---:|---:|
| 無 Skill | 4.09 | |
| 1.3.0 | 2.11 | 48% |
| 2.0.0 | 1.70 | 58% |
| 2.0.1 | 0.91 | 78% |

Linter 歷史：9 個 Claude 模型（144 次生成）的 linter 違規減少 81.3%。詳見 [`evals/results/RESULTS.md`](evals/results/RESULTS.md)。

## 常見問題

**這能讓輸出獲得中文技術表達規範認證嗎？** 沒有「認證」一說。本規範是獨立可執行的規則集，按 C01–C24 自查即可。

**能讓輸出獲得 STE 認證嗎？** 不能。沒有任何工具能獲得認證，因為 ASD 不對任何工具進行認證。Strict 模式最接近。逐詞的裁定見官方標準（[免費下載](https://www.asd-ste100.org/request.html)）。

**我的文件會聽起來像機器人嗎？** 中文文件規則要求保真與明確執行者，因此聽起來更像工程手冊：平淡但不可能被誤讀。部落格文章請保持你的文風。

**為什麼不直接提示「寫得清楚點」？** 「清楚」是一種觀點。「不補造恢復步驟」「不把系統行為寫成人工步驟」「C23 保護機器可讀內容」是規格。Agent 遵循規格。

**與 1.x 系列的關係？** v2.0 起預設採用 Plain 模式（響應域外讀者）。v2.2.0 起中文場景預設採用中文技術表達規範 C01–C24；英文模式仍保留 ASD-STE100。

**詞表檢查器在哪裡？** `evals/ste_lint.py` 測量機械規則，看不到詞彙選擇。[`tools/ste-dictionary/`](tools/ste-dictionary/README.md) 包含一個提取器，從你自己的免費 Issue 9 PDF 副本構建英文 STE 詞表。Linter 讀取這些詞表。倉庫附帶工具，不附帶詞典內容，因為標準禁止在未經 ASD 書面授權的情況下複製。

## 貢獻

歡迎提交 Issue 提問和報告 Bug。Pull request 歡迎。改變已釋出數字的更改必須附帶原始檔案，且 `python3 evals/check_numbers.py` 必須透過。在推送前執行 `python3 evals/ste_lint.py --self-test`。在 PR 中說明 Agent 是否寫了程式碼，不要新增歸屬 trailers。

推送前執行 `bash scripts/check.sh`，跑過本倉庫的七個本地檢查（與原 CI 一致）。CI 流程檔案未隨倉庫釋出，因為 GitHub 要求 Personal Access Token 具備 `workflow` 作用域才能推送。

## 許可證

MIT 許可證。本倉庫為教學目的複述規則，不復制任何規範文字或詞典內容。

**非官方翻譯專案**，與 ASD 或 STEMG 無關聯。ASD-STE100 是 ASD 的註冊商標。中文字面引用按「合理使用」註明來源；不在產品中再分發原始 Subtitle 資料。

<!-- 來源：E:\ChromeDownload\中文技術表達規範.pdf_by_PaddleOCR-VL-1.6.md（C01–C24 + 第 27 節精簡指令） -->