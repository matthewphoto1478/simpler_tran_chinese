# 壓縮研究

## 為什麼使用純文字詞表

本倉庫使用純文字檔案儲存批准詞和不批准詞（`approved.txt` 和 `not-approved.tsv`），而非符號表示（如 JSON、YAML 或自定義格式）。

## 研究發現

在調查中，符號表示方案無法跨模型家族遷移。這意味著一個模型能理解的表示在另一個模型上可能無法工作。

純文字格式具有以下優點：

1. **跨模型相容性**：所有模型都能讀取和理解純文字
2. **易於除錯**：可以直接檢視和編輯
3. **確定性輸出**：相同輸入產生相同輸出

## 實現細節

提取器 (`parse_dict.py`) 從 ASD-STE100 Issue 9 PDF 的文字轉儲中解析第 2 部分，生成 JSON 格式的中間表示。

發射器 (`emit.py`) 將 JSON 轉換為兩個純文字檔案：

- `approved.txt`：每行一個批准詞及其詞性
- `not-approved.tsv`：製表符分隔的表格，包含不批准詞、詞性和批准替代

## 結論

純文字詞表是在各種 AI 模型中保持一致行為的最佳選擇。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/tools/ste-dictionary/COMPRESSION-RESEARCH.md -->
