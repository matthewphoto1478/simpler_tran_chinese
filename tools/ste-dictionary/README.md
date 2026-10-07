# ASD-STE100 詞表，在你的機器上生成

此目錄包含提取器和詞彙檢查器。不包含詞典內容。ASD-STE100 Issue 9 在第 2 頁宣告，未經 ASD 書面授權，不得以任何形式複製標準或其任何部分。因此倉庫附帶工具，你需要從自己的免費 PDF 副本生成詞表。

## 生成詞表

1. 在 asd-ste100.org/request.html 請求免費 PDF。
2. 轉換為文字：`pdftotext -layout ASD-STE100_ISSUE9.pdf ste9.txt`
3. 解析詞典：`python3 parse_dict.py ste9.txt`。這會寫入 `dict.json`。
4. 輸出詞表：`python3 emit.py .`。這會寫入 `approved.txt`（841 行）和 `not-approved.tsv`（1,297 行）。

輸出是確定性的。在 2026-09-04 兩次檔案逐位元組匹配。所有四個生成的檔案都在 `.gitignore` 中。不要提交它們。

## 檢查詞彙選擇

`evals/ste_lint.py` 測量機械規則。看不到詞彙選擇。此檢查器讀取 `not-approved.tsv` 並報告標準不批准的每個詞，附有批准替代。它還將 `evals/slop.tsv` 中的 LLM-tell 詞作為單獨數字計數。

```bash
python3 ste_dict_lint.py file.md
python3 ste_dict_lint.py --self-test
```

已知限制：匹配基於基本形式和簡單變形，沒有詞性消歧。從此工具得到的數字比較透過同一版本的文字。它們不是合規裁定。

`COMPRESSION-RESEARCH.md` 記錄了為什麼詞表是純文字而非符號表示：符號方案在所調查的研究中無法跨模型家族遷移。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/tools/ste-dictionary/README.md -->
