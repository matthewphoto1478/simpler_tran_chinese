# 規則目錄：ASD-STE100 Issue 9 軟體文字版

在 CHECK 模式、Strict 模式或需要規則編號時閱讀此檔案。核心 Skill 在 `SKILL.md` 中命名了最能改變輸出的規則。本檔案包含完整目錄。

9 個部分 53 條規則，源自 ASD-STE100 Issue 9，配有軟體示例。標記為 (S) 的規則僅在 Strict 模式下生效（見 `references/strict-vocabulary.md`）。官方措辭見 asd-ste100.org 的免費標準。

### 第 1 部分：詞彙（規則 1.1-1.14）

| 規則 | 指令 |
|---|---|
| 1.1-1.4, 1.6 (S) | 僅使用批准詞，遵循其列出的詞性、含義和形式。 |
| 1.5 | 可以將領域詞用作技術名詞（"webhook"、"commit"、"endpoint"）。 |
| 1.7 | 不要將技術名詞用作動詞。 |
| 1.8 | 使用你的專案或行業的技術名詞。 |
| 1.9 | 選擇技術名詞時，選簡短清晰的。 |
| 1.10 | 不要將地區詞、俚語或行話用作技術名詞。 |
| 1.11 | 一物一名。不要在這裡叫"config"在那裡叫"settings"。 |
| 1.12 | 可以將領域動詞用作技術動詞（"deploy"、"compile"、"merge"）。標準將計算機動詞合法命名為：click、type、copy、paste、delete、save、install、download、update 等。當常用動詞能做同樣的工作時，優先使用："find"而非"detect"。 |
| 1.13 | 不要將技術動詞用作名詞。 |
| 1.14 | 使用美式英語拼寫。 |

在 Plain 模式下，規則 1.5、1.8 和 1.12 使你的領域詞彙合法化。

錯誤：You can webhook the event, then do a deploy.
正確：Send the event to the webhook. Then deploy the service.

### 第 2 部分：多詞名詞（規則 2.1-2.2）

| 規則 | 指令 |
|---|---|
| 2.1 | 寫三個或更少詞的多詞名詞。 |
| 2.2 | 當技術名詞需要超過三個詞時，先寫全稱，再給縮寫或用連字元連線單位。 |

用介詞斷開長名詞鏈（of、on、in、for）：

錯誤：the connection pool timeout configuration value
正確：the timeout value for the connection pool

### 第 3 部分：動詞（規則 3.1-3.7）

| 規則 | 指令 |
|---|---|
| 3.1 (S) | 僅使用詞典給出的動詞形式。 |
| 3.2 | 僅使用：不定式、祈使句、一般現在時、一般過去時、一般將來時、過去分詞作形容詞。 |
| 3.3 | 僅將過去分詞用作形容詞（"the cached response"）。 |
| 3.4 | 不用助動詞構建複雜結構。不用現在完成時，不用"is to be installed"。 |
| 3.5 | 僅將 "-ing" 形式用作技術名詞或在其內部（"logging"、"the mounting bracket"），永遠不用作動詞。 |
| 3.6 | 主動語態。在描述性文字中，僅在主語未知時允許被動語態。修復無主語被動語態：用"you"（讀者）或"we"（你的公司）："Indexes are not used on this table" → "We do not use indexes on this table." |
| 3.7 | 用動詞描述動作，不用名詞（"compress the file"，而非"perform compression of the file"）。 |

批准的情態動詞：can、will、must。禁用：should、would、may、might、could。本檔案末尾的 modal ladder 給出每個禁用情態動詞的替代。

### 第 4 部分：句子（規則 4.1-4.5）

| 規則 | 指令 |
|---|---|
| 4.1 | 寫簡短清晰的句子。 |
| 4.2 | 不要用省略詞或縮寫來縮短句子。保留冠詞，保留"that"。 |
| 4.3 | 複雜文字用垂直列表：引導語後加冒號，大寫開頭，純句子項才加句號，不混用指令和事實，不巢狀。 |
| 4.4 | 在相關主題的句子之間用連線詞（"Then"、"As a result"）。 |
| 4.5 | 在適用的地方在名詞前加冠詞（the、a、an）或指示形容詞（this、these）。例外：當名詞後跟識別符號時不用冠詞："Restart pod web-7f9b2"。 |

規則 4.2 是反簡陋規則。平實英語是帶完整語法的簡短句子，不是電報式縮寫：

錯誤縮寫：Ensure file exists before running.
平實：Make sure that the file exists before you run the command.

### 第 5 部分：程式性寫作（規則 5.1-5.5）

| 規則 | 指令 |
|---|---|
| 5.1 | 每句最多 20 詞。包括警告和注意事項。 |
| 5.2 | 每句一條指令，除非兩個動作同時發生。一步可以加一句說明即時結果或限制。 |
| 5.3 | 用祈使句寫指令："Run the migration." |
| 5.4 | 將必需條件放在命令前，用逗號分隔："If the build fails, read the log." |
| 5.5 | 註釋提供資訊，永不提供指令或限制。限制屬於其動作。註釋測試：讀者刪除所有註釋後，程式仍能正常工作。 |

錯誤：You'll want to grab the API key from the dashboard before configuring the client, which you can do under Settings.
正確：Get the API key from the dashboard, under Settings. Then configure the client with this key.

### 第 6 部分：描述性寫作（規則 6.1-6.6）

| 規則 | 指令 |
|---|---|
| 6.1 | 逐步提供資訊：每句一個新事實。 |
| 6.2 | 用關鍵詞和短語給文字賦予邏輯結構。 |
| 6.3 | 每句最多 25 詞。 |
| 6.4 | 將相關資訊分組到段落中。 |
| 6.5 | 每段一個主題。 |
| 6.6 | 每段最多六句。 |

### 第 7 部分：安全說明（規則 7.1-7.3）

| 規則 | 指令 |
|---|---|
| 7.1 | 用表示風險級別的詞（"WARNING"=傷害，"CAUTION"=損壞）。當兩種風險同時發生時，用"WARNING"。 |
| 7.2 | 以清晰的命令或條件開頭。 |
| 7.3 | 然後給出風險或可能的結果。 |

將指令放在解釋前。對破壞性 CLI 標誌和無法撤銷的遷移使用相同模式。

錯誤：Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
正確：CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

### 第 8 部分：標點和詞數（規則 8.1-8.7）

| 規則 | 指令 |
|---|---|
| 8.1 | 除分號外所有標準標點都合法。改為寫兩個句子。 |
| 8.2 | 用連字元連線作為整體起作用的詞。 |
| 8.3 | 括號可用於引用、項號、縮寫、複數形式、解釋、替代項。 |
| 8.4 | 在垂直列表中，引導語冒號結束一個句子用於詞數統計。冒號後的每項算一個新句子，各有自己的 20/25 詞預算。 |
| 8.5-8.7 | 以下各計為一個詞：括號內文字、連字元連線的詞、數字、帶單位的數字、縮寫、識別符號、引用的文字、標題、標籤、專有名詞。 |

規則 8.6 對軟體文字重要：`sqlpipe run --config sqlpipe.yaml` 在反引號中計為一個詞。

破折號（本 Skill 的規則，非標準）：em 破折號（`—`）拼接兩個陳述，隱藏其間的邏輯。指明關係（"because"、"but"、"for example"）或寫成兩個句子。用空格分隔或雙連字元的破折號是同樣的破折號。範圍（`5–10`）、列表標記和標誌（`--force`）不是。

### 第 9 部分：寫作實踐（規則 9.1-9.4，GR-1 至 GR-8）

| 規則 | 指令 |
|---|---|
| 9.1 | 當逐詞替換不起作用時，重構句子。 |
| 9.2 (S) | 正確使用每個批准詞：批准的含義、批准的詞性。 |
| 9.3 | 優先使用單詞動詞而非短語動詞（"decrease"，而非"go down"；"install"，而非"set up"）。Strict 模式：短語動詞是違規。 |
| 9.4 | 在整個文件中保持一致的樣式和術語。 |

通用建議：保留"that"（GR-1），"with"後先主要動詞再工具（GR-2: "Fetch the URL with curl"），清晰指代（GR-3），"this + 名詞"（GR-4），包容性語言（GR-7）。GR-6："e.g." → "for example"，"i.e." → "that is"，刪除"etc."並列出專案。

### Modal Ladder

| 你寫了 | 改為 |
|---|---|
| should（要求） | must |
| should（建議） | 刪除，或陳述為事實："X 更好因為 Y。" |
| should（倒裝條件："should a failure occur"） | if："If a failure occurs" |
| may / might / could（可能性） | can |
| may（許可） | can |
| would（假設） | can，或重構："If X occurs, Y occurs." |

## AI 寫作的跡象

AI 文字向已知方向漂移（Wikipedia "Signs of AI writing"）。上述規則已消除部分。透過方向防範其餘（在文件和回覆中）：

- 膨脹的重要性：不用"vital"、"crucial"、"a testament"。陳述事實。
- 負面平行：不用"not just X, it is Y"。
- 三連詞規則：不用裝飾性三連。
- 模糊歸屬：不用"研究表明"。命名來源，或放棄主張。
- 虛假範圍：不用"從 X 到 Y 不等"除非有真實限制。
- 重述摘要：不用"總之"段落。
- 編輯旁白：不用"值得注意的是"。
- 協作殘餘：不用"I hope this helps"，不用"Let me know"。
- 格式習慣：不用裝飾性加粗，不用加粗引導語，不用 emoji 作為結構，不用兩句話的標題。

對於具體的過度使用詞，`references/word-swaps.md` 將每個對映到平實替代。如果一個詞不帶事實，刪除它而非替換。

## 詞彙選擇

全文一個詞一個含義、一個詞性（規則 1.11、9.4）。

- 設定檔案是 `configuration`，在同一文件中永遠不是 config、settings 或 options。
- verify 概念是 `make sure that`，作為動詞永遠不是 check、verify、confirm、validate 或 ensure。Strict 模式用 `references/strict-vocabulary.md` 路由其餘。
- 常見替換：however → but、therefore → as a result、since (= because) → because、perform → do、avoid → prevent、repeat → do again、acceptable → permitted、now → 刪除它。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/rule-catalog.md -->
