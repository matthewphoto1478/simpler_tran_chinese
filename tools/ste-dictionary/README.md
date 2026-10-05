# ASD-STE100 词表，在你的机器上生成

此目录包含提取器和词汇检查器。不包含词典内容。ASD-STE100 Issue 9 在第 2 页声明，未经 ASD 书面授权，不得以任何形式复制标准或其任何部分。因此仓库附带工具，你需要从自己的免费 PDF 副本生成词表。

## 生成词表

1. 在 asd-ste100.org/request.html 请求免费 PDF。
2. 转换为文本：`pdftotext -layout ASD-STE100_ISSUE9.pdf ste9.txt`
3. 解析词典：`python3 parse_dict.py ste9.txt`。这会写入 `dict.json`。
4. 输出词表：`python3 emit.py .`。这会写入 `approved.txt`（841 行）和 `not-approved.tsv`（1,297 行）。

输出是确定性的。在 2026-09-04 两次文件逐字节匹配。所有四个生成的文件都在 `.gitignore` 中。不要提交它们。

## 检查词汇选择

`evals/ste_lint.py` 测量机械规则。看不到词汇选择。此检查器读取 `not-approved.tsv` 并报告标准不批准的每个词，附有批准替代。它还将 `evals/slop.tsv` 中的 LLM-tell 词作为单独数字计数。

```bash
python3 ste_dict_lint.py file.md
python3 ste_dict_lint.py --self-test
```

已知限制：匹配基于基本形式和简单变形，没有词性消歧。从此工具得到的数字比较通过同一版本的文本。它们不是合规裁定。

`COMPRESSION-RESEARCH.md` 记录了为什么词表是纯文本而非符号表示：符号方案在所调查的研究中无法跨模型家族迁移。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/tools/ste-dictionary/README.md -->
