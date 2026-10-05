# 压缩研究

## 为什么使用纯文本词表

本仓库使用纯文本文件存储批准词和不批准词（`approved.txt` 和 `not-approved.tsv`），而非符号表示（如 JSON、YAML 或自定义格式）。

## 研究发现

在调查中，符号表示方案无法跨模型家族迁移。这意味着一个模型能理解的表示在另一个模型上可能无法工作。

纯文本格式具有以下优点：

1. **跨模型兼容性**：所有模型都能读取和理解纯文本
2. **易于调试**：可以直接查看和编辑
3. **确定性输出**：相同输入产生相同输出

## 实现细节

提取器 (`parse_dict.py`) 从 ASD-STE100 Issue 9 PDF 的文本转储中解析第 2 部分，生成 JSON 格式的中间表示。

发射器 (`emit.py`) 将 JSON 转换为两个纯文本文件：

- `approved.txt`：每行一个批准词及其词性
- `not-approved.tsv`：制表符分隔的表格，包含不批准词、词性和批准替代

## 结论

纯文本词表是在各种 AI 模型中保持一致行为的最佳选择。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/tools/ste-dictionary/COMPRESSION-RESEARCH.md -->
