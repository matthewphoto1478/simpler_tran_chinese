# 规则目录：ASD-STE100 Issue 9 软件文本版

在 CHECK 模式、Strict 模式或需要规则编号时阅读此文件。核心 Skill 在 `SKILL.md` 中命名了最能改变输出的规则。本文件包含完整目录。

9 个部分 53 条规则，源自 ASD-STE100 Issue 9，配有软件示例。标记为 (S) 的规则仅在 Strict 模式下生效（见 `references/strict-vocabulary.md`）。官方措辞见 asd-ste100.org 的免费标准。

### 第 1 部分：词汇（规则 1.1-1.14）

| 规则 | 指令 |
|---|---|
| 1.1-1.4, 1.6 (S) | 仅使用批准词，遵循其列出的词性、含义和形式。 |
| 1.5 | 可以将领域词用作技术名词（"webhook"、"commit"、"endpoint"）。 |
| 1.7 | 不要将技术名词用作动词。 |
| 1.8 | 使用你的项目或行业的技术名词。 |
| 1.9 | 选择技术名词时，选简短清晰的。 |
| 1.10 | 不要将地区词、俚语或行话用作技术名词。 |
| 1.11 | 一物一名。不要在这里叫"config"在那里叫"settings"。 |
| 1.12 | 可以将领域动词用作技术动词（"deploy"、"compile"、"merge"）。标准将计算机动词合法命名为：click、type、copy、paste、delete、save、install、download、update 等。当常用动词能做同样的工作时，优先使用："find"而非"detect"。 |
| 1.13 | 不要将技术动词用作名词。 |
| 1.14 | 使用美式英语拼写。 |

在 Plain 模式下，规则 1.5、1.8 和 1.12 使你的领域词汇合法化。

错误：You can webhook the event, then do a deploy.
正确：Send the event to the webhook. Then deploy the service.

### 第 2 部分：多词名词（规则 2.1-2.2）

| 规则 | 指令 |
|---|---|
| 2.1 | 写三个或更少词的多词名词。 |
| 2.2 | 当技术名词需要超过三个词时，先写全称，再给缩写或用连字符连接单位。 |

用介词断开长名词链（of、on、in、for）：

错误：the connection pool timeout configuration value
正确：the timeout value for the connection pool

### 第 3 部分：动词（规则 3.1-3.7）

| 规则 | 指令 |
|---|---|
| 3.1 (S) | 仅使用词典给出的动词形式。 |
| 3.2 | 仅使用：不定式、祈使句、一般现在时、一般过去时、一般将来时、过去分词作形容词。 |
| 3.3 | 仅将过去分词用作形容词（"the cached response"）。 |
| 3.4 | 不用助动词构建复杂结构。不用现在完成时，不用"is to be installed"。 |
| 3.5 | 仅将 "-ing" 形式用作技术名词或在其内部（"logging"、"the mounting bracket"），永远不用作动词。 |
| 3.6 | 主动语态。在描述性文本中，仅在主语未知时允许被动语态。修复无主语被动语态：用"you"（读者）或"we"（你的公司）："Indexes are not used on this table" → "We do not use indexes on this table." |
| 3.7 | 用动词描述动作，不用名词（"compress the file"，而非"perform compression of the file"）。 |

批准的情态动词：can、will、must。禁用：should、would、may、might、could。本文件末尾的 modal ladder 给出每个禁用情态动词的替代。

### 第 4 部分：句子（规则 4.1-4.5）

| 规则 | 指令 |
|---|---|
| 4.1 | 写简短清晰的句子。 |
| 4.2 | 不要用省略词或缩写来缩短句子。保留冠词，保留"that"。 |
| 4.3 | 复杂文本用垂直列表：引导语后加冒号，大写开头，纯句子项才加句号，不混用指令和事实，不嵌套。 |
| 4.4 | 在相关主题的句子之间用连接词（"Then"、"As a result"）。 |
| 4.5 | 在适用的地方在名词前加冠词（the、a、an）或指示形容词（this、these）。例外：当名词后跟标识符时不用冠词："Restart pod web-7f9b2"。 |

规则 4.2 是反简陋规则。平实英语是带完整语法的简短句子，不是电报式缩写：

错误缩写：Ensure file exists before running.
平实：Make sure that the file exists before you run the command.

### 第 5 部分：程序性写作（规则 5.1-5.5）

| 规则 | 指令 |
|---|---|
| 5.1 | 每句最多 20 词。包括警告和注意事项。 |
| 5.2 | 每句一条指令，除非两个动作同时发生。一步可以加一句说明即时结果或限制。 |
| 5.3 | 用祈使句写指令："Run the migration." |
| 5.4 | 将必需条件放在命令前，用逗号分隔："If the build fails, read the log." |
| 5.5 | 注释提供信息，永不提供指令或限制。限制属于其动作。注释测试：读者删除所有注释后，程序仍能正常工作。 |

错误：You'll want to grab the API key from the dashboard before configuring the client, which you can do under Settings.
正确：Get the API key from the dashboard, under Settings. Then configure the client with this key.

### 第 6 部分：描述性写作（规则 6.1-6.6）

| 规则 | 指令 |
|---|---|
| 6.1 | 逐步提供信息：每句一个新事实。 |
| 6.2 | 用关键词和短语给文本赋予逻辑结构。 |
| 6.3 | 每句最多 25 词。 |
| 6.4 | 将相关信息分组到段落中。 |
| 6.5 | 每段一个主题。 |
| 6.6 | 每段最多六句。 |

### 第 7 部分：安全说明（规则 7.1-7.3）

| 规则 | 指令 |
|---|---|
| 7.1 | 用表示风险级别的词（"WARNING"=伤害，"CAUTION"=损坏）。当两种风险同时发生时，用"WARNING"。 |
| 7.2 | 以清晰的命令或条件开头。 |
| 7.3 | 然后给出风险或可能的结果。 |

将指令放在解释前。对破坏性 CLI 标志和无法撤销的迁移使用相同模式。

错误：Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
正确：CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

### 第 8 部分：标点和词数（规则 8.1-8.7）

| 规则 | 指令 |
|---|---|
| 8.1 | 除分号外所有标准标点都合法。改为写两个句子。 |
| 8.2 | 用连字符连接作为整体起作用的词。 |
| 8.3 | 括号可用于引用、项号、缩写、复数形式、解释、替代项。 |
| 8.4 | 在垂直列表中，引导语冒号结束一个句子用于词数统计。冒号后的每项算一个新句子，各有自己的 20/25 词预算。 |
| 8.5-8.7 | 以下各计为一个词：括号内文本、连字符连接的词、数字、带单位的数字、缩写、标识符、引用的文本、标题、标签、专有名词。 |

规则 8.6 对软件文本重要：`sqlpipe run --config sqlpipe.yaml` 在反引号中计为一个词。

破折号（本 Skill 的规则，非标准）：em 破折号（`—`）拼接两个陈述，隐藏其间的逻辑。指明关系（"because"、"but"、"for example"）或写成两个句子。用空格分隔或双连字符的破折号是同样的破折号。范围（`5–10`）、列表标记和标志（`--force`）不是。

### 第 9 部分：写作实践（规则 9.1-9.4，GR-1 至 GR-8）

| 规则 | 指令 |
|---|---|
| 9.1 | 当逐词替换不起作用时，重构句子。 |
| 9.2 (S) | 正确使用每个批准词：批准的含义、批准的词性。 |
| 9.3 | 优先使用单词动词而非短语动词（"decrease"，而非"go down"；"install"，而非"set up"）。Strict 模式：短语动词是违规。 |
| 9.4 | 在整个文档中保持一致的样式和术语。 |

通用建议：保留"that"（GR-1），"with"后先主要动词再工具（GR-2: "Fetch the URL with curl"），清晰指代（GR-3），"this + 名词"（GR-4），包容性语言（GR-7）。GR-6："e.g." → "for example"，"i.e." → "that is"，删除"etc."并列出项目。

### Modal Ladder

| 你写了 | 改为 |
|---|---|
| should（要求） | must |
| should（建议） | 删除，或陈述为事实："X 更好因为 Y。" |
| should（倒装条件："should a failure occur"） | if："If a failure occurs" |
| may / might / could（可能性） | can |
| may（许可） | can |
| would（假设） | can，或重构："If X occurs, Y occurs." |

## AI 写作的迹象

AI 文本向已知方向漂移（Wikipedia "Signs of AI writing"）。上述规则已消除部分。通过方向防范其余（在文档和回复中）：

- 膨胀的重要性：不用"vital"、"crucial"、"a testament"。陈述事实。
- 负面平行：不用"not just X, it is Y"。
- 三连词规则：不用装饰性三连。
- 模糊归属：不用"研究表明"。命名来源，或放弃主张。
- 虚假范围：不用"从 X 到 Y 不等"除非有真实限制。
- 重述摘要：不用"总之"段落。
- 编辑旁白：不用"值得注意的是"。
- 协作残余：不用"I hope this helps"，不用"Let me know"。
- 格式习惯：不用装饰性加粗，不用加粗引导语，不用 emoji 作为结构，不用两句话的标题。

对于具体的过度使用词，`references/word-swaps.md` 将每个映射到平实替代。如果一个词不带事实，删除它而非替换。

## 词汇选择

全文一个词一个含义、一个词性（规则 1.11、9.4）。

- 设置文件是 `configuration`，在同一文档中永远不是 config、settings 或 options。
- verify 概念是 `make sure that`，作为动词永远不是 check、verify、confirm、validate 或 ensure。Strict 模式用 `references/strict-vocabulary.md` 路由其余。
- 常见替换：however → but、therefore → as a result、since (= because) → because、perform → do、avoid → prevent、repeat → do again、acceptable → permitted、now → 删除它。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/rule-catalog.md -->
