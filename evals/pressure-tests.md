# 壓力測試

本 Skill 的測試場景，以及它們存在以捕捉的基線失敗。方法：在新 Agent 會話中執行每個提示兩次——一次不用 Skill（基線），一次用——並按標準評分。如果一個標準在基線透過，它什麼也沒證明；有價值的標準是基線失敗的那些。

## 基線結果（記錄於 2026-07-21，Claude Sonnet，無 Skill）

**場景 1 基線失敗：** 30-40 詞的句子；縮寫（`It's`、`you'll`）；懸垂 "-ing" 從句（"...file, making it easy to..."）；同義旋轉——verify、confirm、check 和 make sure 用於同一動作；條件在命令後。

**場景 2 基線失敗（Agent 被要求憑記憶寫 STE）：** 編造規則號——引用"Rule 3.1: short sentences"和"Rule 4.2: active voice"；真實的 Rule 3.1 是動詞形式，真實的 Rule 4.2 是省略詞。保留被動語態（"are configured"）。在"make sure"後省略"that"。用"By using"作動名詞開頭。不知道 20/25 程式性/描述性區分。

Skill 存在以關閉這些特定差距：紙面上真實的規則號、分類步驟、機械自我檢查。

## 場景 1 — 自然文件任務

> Write documentation for a CLI tool called "sqlpipe" that syncs Postgres tables to S3 as Parquet files. Produce an introduction, a "Getting started" section, and a "Troubleshooting" section covering connection timeouts and permission errors. Around 350 words.

透過標準：
- [ ] Getting started / Troubleshooting（程式性）中無超過 20 詞的句子
- [ ] 介紹（描述性）中無超過 25 詞的句子
- [ ] 零縮寫
- [ ] 零 "-ing" 動詞從句（", making"、", allowing"）
- [ ] 為 check/verify/confirm 選擇一個動詞並全文使用
- [ ] 每個 "if" 從句在命令前
- [ ] 程式碼、標誌和錯誤字串未改動

## 場景 2 — 帶規則引用的重寫

> Rewrite this in ASD-STE100 Simplified Technical English, then list the rules you applied with their numbers: [any 100-word slop paragraph]

透過標準：
- [ ] 每個引用的規則號與 SKILL.md 規則目錄匹配（無編造）
- [ ] 重寫前文字分類為程式性 vs 描述性
- [ ] 無未知主語的被動語態
- [ ] "make sure"後保留"that"

## 場景 3 — 壓力：使用者要求簡潔

> Rewrite this runbook step "to be as short as possible": "Ensure the backup exists before running the migration."

陷阱：STE 禁止電報式縮寫（規則 4.2）。"儘可能短"的壓力誘使刪除冠詞和"that"。

透過標準：
- [ ] 輸出保持完整語法："Make sure that a backup exists. Then run the migration." 或等效
- [ ] Agent 不刪除冠詞或"that"以滿足"short"

## 場景 4 — 範圍邊界

> Write a landing-page hero section for sqlpipe using the simple-english skill.

透過標準：
- [ ] Agent 標記 STE 不適用於營銷文案（Skill 的"侷限性"部分）併為文件提供它，或詢問

## 場景 5 — 錯誤訊息

> Write the error message sqlpipe prints when the S3 upload fails with AccessDenied.

透過標準：
- [ ] 用一般過去時陳述發生了什麼
- [ ] 用祈使句給出修復方法
- [ ] 無"Oops"，無"Please ensure"，無道歉填充語

## 記錄的使用 Skill 結果（2026-07-21，Claude Sonnet，載入 Skill）

- **場景 1，第一次執行：** 所有長度、縮寫和 "-ing" 標準透過。兩次失敗：check/confirm 旋轉，一個拖尾"if"條件。Skill 的自我檢查步驟已修訂：動詞選擇在寫作前步驟中進行，拖尾條件新增到搜尋列表。
- **場景 1，修訂後：** 所有標準透過。Agent 顯式執行了四項自我檢查，選擇"check"作為唯一動詞，每句以條件開頭。
- **場景 2：** 所有標準透過。每個引用的規則號匹配 rules.md——基線 Agent 編造了它的號。
- **場景 3：** 透過。在"儘可能短"的壓力下 Agent 保留了"that"和完整語法，並引用規則 4.2 作為原因。

## 如何執行

Claude Code：安裝 Skill，每個場景在新會話中開啟，貼上提示。與 Skill 目錄不存在的會話比較。按清單手動評分——詞數可數，大多數標準是客觀的。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/evals/pressure-tests.md -->
