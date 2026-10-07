# Strict 模式：詞典規範

當使用者提到 STE、ASD-STE100 或合規時閱讀此檔案。Strict 模式將詞典規則新增到文件。它不改變對使用者的回覆，回覆保持 Plain 模式。

官方詞典（約 900 個批准詞和 1,200 個不批准詞及其替代）版權歸 ASD 所有，此處不復現。本檔案給出依賴詞典的規則、軟體作者最常遇到的裁定，以及標準命名的反覆出現的錯誤。告訴使用者，每對話一次、一句話：此索引有損，完整合規需要官方詞典（免費在 asd-ste100.org）。

## 僅隨詞典存在的規則

| 規則 | 指令 |
|---|---|
| 1.1 | 僅使用批准詞、技術名詞或技術動詞。 |
| 1.2 | 僅按詞典列出的詞性使用批准詞。 |
| 1.3 | 僅按詞典批准的含義使用批准詞。 |
| 1.4 | 僅使用批准形式的動詞和形容詞。 |
| 1.6 | 僅當不批准詞是技術名詞或技術名詞的一部分時才可使用。 |
| 3.1 | 僅使用詞典給出的動詞形式。 |
| 9.2 | 正確使用每個批准詞：批准的含義、批准的詞性。 |
| GR-5 | 避免假朋友：看起來像讀者母語中的詞但含義不同的詞。 |
| GR-8 | 僅在確定正確時才使用所有格撇號。不確定時，寫"the file of the user"。 |

Issue 9 在詞典導言部分增加了批准動詞快速參考。在其中檢查你的動詞。

## 詞性裁定

| 詞 | 裁定 |
|---|---|
| test, check, work | 僅作名詞。"Do a test"，而非"test the pump"。"Check that X"變為"make sure that X"。 |
| oil | 僅作技術名詞。動詞形式詞典給出"lubricate"："Lubricate the linkage with oil." |
| help | 僅作動詞。名詞形式詞典給出"aid"："with the aid of"。 |
| fall (名詞) | 不批准。用"decrease"表示值減少。僅將"fall"（動詞）用於重力下的向下運動："Make sure that the tools do not fall into the engine." |
| follow | 僅表示"跟在後面"，永不用"obey"。寫"obey the instructions"。 |
| above, below | 僅用於物理位置。限值寫"more than"、"less than"。 |

## 常見軟體動詞的詞典裁定

標準已經做出選擇。使用批准詞。

| 你寫了 | 詞典狀態 | 用什麼替代 |
|---|---|---|
| check（動詞）、verify、confirm、ensure | 全部作為動詞不批准 | 按意圖路由：`make sure that`（一種狀態）、`examine`（查詢故障："examine the log"）、`measure`（獲取值）、或用名詞："do a check of"。 |
| validate | 不在詞典中 | 作為技術動詞合法（規則 1.12），或替換為 `make sure that`。 |
| delete、drop（動詞）、destroy | 全部作為詞典動詞不批准 | `erase`（資料）、`remove`（物理）。在計算機語境中`delete`也是合法技術動詞（規則 1.12）。不用`drop`或`destroy`。 |
| remove | 批准動詞 | 保留。 |
| run、execute | 都不批准 | `operate` 表示 run，`do` 表示 execute。 |
| invoke、launch | 不在詞典中 | 作為技術動詞合法（規則 1.12）。 |
| display（動詞）、render、present（動詞） | 全部不批准 | `show` 涵蓋大多數軟體情況。官方替代：display → `show`、render → `make`、present → `give` 或 `show`。 |
| issue | 不在詞典中 | 作為技術名詞使用，或替換為`problem`（批准）。 |
| failure | 一般使用不批准；作為效能損耗的技術名詞批准 | 僅用於效能錯誤："a failure of the pump"。 |
| error、problem | 批准名詞 | 保留。 |

## 標準命名的反覆出現的錯誤

詞典導言列出了作者最常出錯的詞。這是軟體相關集，僅裁定。

| 你寫了 | STE 寫法 |
|---|---|
| however | but |
| therefore | thus、as a result |
| since (= because) | because |
| any | 刪除它，或重構："if you have any questions" → "if you have questions" |
| now | at this time。更好，刪除它："now start the service" → "start the service" |
| need to、have to | 程式中用祈使句；描述性文字中用"it is necessary to" |
| perform | do |
| insert | put（但 SQL `INSERT` 保留：這是引用的文字） |
| reach | get、get to |
| avoid | prevent |
| repeat | do … again |
| acceptable | permitted。更好，給出限制："a latency of less than 200 ms" |
| complete（形容詞） | completed |
| the example below、the section above | 命名目標，或將引用放在之後："the example that follows" |

## 嚴格自我檢查

在 SKILL.md 的自我檢查中新增這兩步：

1. 在草稿中搜尋上兩表中每個動詞。將每個命中替換為批准詞。
2. 搜尋你構建短語動詞（"set up"、"go down"）。用單詞動詞替換每個（規則 9.3："install"、"decrease"）。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/strict-vocabulary.md -->
