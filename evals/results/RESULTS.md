# 基準測試結果

**使用 Skill 後，9 個模型 × 8 個任務（144 次生成）平均每 100 詞的 STE 違規減少 81.3%。**

| 模型 | 基線違規/100詞 | Skill 違規/100詞 | 減少幅度 | 基線句長 | Skill 句長 | 輸出 Token (基線->Skill) |
|---|---|---|---|---|---|---|
| claude-fable-5-1 | 1.77 | 0.33 | 81.4% | 12.9 | 9.8 | 348 -> 236 |
| claude-fable-5 | 2.73 | 0.51 | 81.3% | 15.1 | 9.6 | 285 -> 250 |
| claude-opus-5 | 2.13 | 0.32 | 85.0% | 14.1 | 10.8 | 272 -> 241 |
| claude-opus-4-8 | 3.64 | 0.45 | 87.6% | 16.9 | 11.4 | 278 -> 200 |
| claude-opus-4-7 | 2.28 | 0.42 | 81.6% | 13.0 | 10.8 | 243 -> 226 |
| claude-opus-4-6 | 2.24 | 0.4 | 82.1% | 10.9 | 9.0 | 185 -> 176 |
| claude-opus-4-5-20251101 | 2.55 | 0.57 | 77.6% | 11.1 | 8.5 | 196 -> 159 |
| claude-sonnet-5 | 2.67 | 0.53 | 80.1% | 10.0 | 9.7 | 266 -> 205 |
| claude-sonnet-4-6 | 2.06 | 0.52 | 74.8% | 11.7 | 10.2 | 168 -> 162 |

## 評判透過（盲測成對比較）

對於每個模型 × 場景對，claude-opus-4-8 對基線文字和 Skill 文字按 0-10 評分表評分，每個順序各兩次以抵消位置偏差。評判者看不到標籤。

結果：Skill 輸出在 72 對中的 62 對得分更高，6 對持平，4 對落後。平均評分：使用 Skill 為 8.31，不使用為 6.20。

| 模型 | Skill 勝 | 持平 | 落後 |
|---|---|---|---|
| claude-fable-5-1 | 8 | 0 | 0 |
| claude-fable-5 | 8 | 0 | 0 |
| claude-opus-5 | 7 | 1 | 0 |
| claude-opus-4-8 | 6 | 2 | 0 |
| claude-opus-4-7 | 7 | 1 | 0 |
| claude-opus-4-6 | 8 | 0 | 0 |
| claude-opus-4-5-20251101 | 6 | 0 | 2 |
| claude-sonnet-5 | 5 | 2 | 1 |
| claude-sonnet-4-6 | 7 | 0 | 1 |

注意事項：一個評判模型，每個順序評判一次。評判是 Claude 模型，文字是 Claude 輸出，因此可能存在家族偏見。評判檔案在精力固定前完成繼承，因此評判透過不統一：72 對中的 32 對記錄了 `judge_effort`，其餘在精力固定之前。原始評判檔案：results/raw/*__judge__*.json。用 `python3 evals/run_bench.py --judge` 重現。

## 誠實數字警告

- Linter 是正規表示式透過（見 ste_lint.py 頭註釋）。它低估了真實 STE 違規：沒有被動語態或詞性檢測。它以相同方式對兩種條件計數，因此比較是公平的，即使絕對數字較低。
- Skill 條件在提示中傳送 SKILL.md，因此其輸入 token 本身更高。報告輸出 token；得出你自己的結論。
- 推理努力固定在 `low` 並在每個原始檔案中記錄。raw/ 中存在的努力級別：`low`、`unrecorded`。標記為 unrecorded 的行在精力固定之前繼承環境 effortLevel；表格假設它們也是 `low`，這與其測量的輸出 token 輪廓匹配，但將其視為推斷。不同努力級別移動數字，因此僅在同一努力級別下比較行。
- 輸出 token 包括推理 token。raw/ 中最高的 `thinking_tokens` 是 298。在推理模型上，該列多於最終文字。
- 每個單元格一次生成。重新執行矩陣以獲取方差；執行器可恢復，刪除 results/raw 從頭開始。
- 沒有任何工具能保證 ASD-STE100 合規，包括本工具。

重現：`python3 evals/run_bench.py`（Claude Code CLI，需登入）。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/evals/results/RESULTS.md -->
