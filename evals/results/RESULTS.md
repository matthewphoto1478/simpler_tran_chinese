# 基准测试结果

**使用 Skill 后，9 个模型 × 8 个任务（144 次生成）平均每 100 词的 STE 违规减少 81.3%。**

| 模型 | 基线违规/100词 | Skill 违规/100词 | 减少幅度 | 基线句长 | Skill 句长 | 输出 Token (基线->Skill) |
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

## 评判通过（盲测成对比较）

对于每个模型 × 场景对，claude-opus-4-8 对基线文本和 Skill 文本按 0-10 评分表评分，每个顺序各两次以抵消位置偏差。评判者看不到标签。

结果：Skill 输出在 72 对中的 62 对得分更高，6 对持平，4 对落后。平均评分：使用 Skill 为 8.31，不使用为 6.20。

| 模型 | Skill 胜 | 持平 | 落后 |
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

注意事项：一个评判模型，每个顺序评判一次。评判是 Claude 模型，文本是 Claude 输出，因此可能存在家族偏见。评判文件在精力固定前完成继承，因此评判通过不统一：72 对中的 32 对记录了 `judge_effort`，其余在精力固定之前。原始评判文件：results/raw/*__judge__*.json。用 `python3 evals/run_bench.py --judge` 重现。

## 诚实数字警告

- Linter 是正则表达式通过（见 ste_lint.py 头注释）。它低估了真实 STE 违规：没有被动语态或词性检测。它以相同方式对两种条件计数，因此比较是公平的，即使绝对数字较低。
- Skill 条件在提示中发送 SKILL.md，因此其输入 token 本身更高。报告输出 token；得出你自己的结论。
- 推理努力固定在 `low` 并在每个原始文件中记录。raw/ 中存在的努力级别：`low`、`unrecorded`。标记为 unrecorded 的行在精力固定之前继承环境 effortLevel；表格假设它们也是 `low`，这与其测量的输出 token 轮廓匹配，但将其视为推断。不同努力级别移动数字，因此仅在同一努力级别下比较行。
- 输出 token 包括推理 token。raw/ 中最高的 `thinking_tokens` 是 298。在推理模型上，该列多于最终文本。
- 每个单元格一次生成。重新运行矩阵以获取方差；运行器可恢复，删除 results/raw 从头开始。
- 没有任何工具能保证 ASD-STE100 合规，包括本工具。

重现：`python3 evals/run_bench.py`（Claude Code CLI，需登录）。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/evals/results/RESULTS.md -->
