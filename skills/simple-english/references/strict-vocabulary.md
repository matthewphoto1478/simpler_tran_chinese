# Strict 模式：词典规范

当用户提到 STE、ASD-STE100 或合规时阅读此文件。Strict 模式将词典规则添加到文档。它不改变对用户的回复，回复保持 Plain 模式。

官方词典（约 900 个批准词和 1,200 个不批准词及其替代）版权归 ASD 所有，此处不复现。本文件给出依赖词典的规则、软件作者最常遇到的裁定，以及标准命名的反复出现的错误。告诉用户，每对话一次、一句话：此索引有损，完整合规需要官方词典（免费在 asd-ste100.org）。

## 仅随词典存在的规则

| 规则 | 指令 |
|---|---|
| 1.1 | 仅使用批准词、技术名词或技术动词。 |
| 1.2 | 仅按词典列出的词性使用批准词。 |
| 1.3 | 仅按词典批准的含义使用批准词。 |
| 1.4 | 仅使用批准形式的动词和形容词。 |
| 1.6 | 仅当不批准词是技术名词或技术名词的一部分时才可使用。 |
| 3.1 | 仅使用词典给出的动词形式。 |
| 9.2 | 正确使用每个批准词：批准的含义、批准的词性。 |
| GR-5 | 避免假朋友：看起来像读者母语中的词但含义不同的词。 |
| GR-8 | 仅在确定正确时才使用所有格撇号。不确定时，写"the file of the user"。 |

Issue 9 在词典导言部分增加了批准动词快速参考。在其中检查你的动词。

## 词性裁定

| 词 | 裁定 |
|---|---|
| test, check, work | 仅作名词。"Do a test"，而非"test the pump"。"Check that X"变为"make sure that X"。 |
| oil | 仅作技术名词。动词形式词典给出"lubricate"："Lubricate the linkage with oil." |
| help | 仅作动词。名词形式词典给出"aid"："with the aid of"。 |
| fall (名词) | 不批准。用"decrease"表示值减少。仅将"fall"（动词）用于重力下的向下运动："Make sure that the tools do not fall into the engine." |
| follow | 仅表示"跟在后面"，永不用"obey"。写"obey the instructions"。 |
| above, below | 仅用于物理位置。限值写"more than"、"less than"。 |

## 常见软件动词的词典裁定

标准已经做出选择。使用批准词。

| 你写了 | 词典状态 | 用什么替代 |
|---|---|---|
| check（动词）、verify、confirm、ensure | 全部作为动词不批准 | 按意图路由：`make sure that`（一种状态）、`examine`（查找故障："examine the log"）、`measure`（获取值）、或用名词："do a check of"。 |
| validate | 不在词典中 | 作为技术动词合法（规则 1.12），或替换为 `make sure that`。 |
| delete、drop（动词）、destroy | 全部作为词典动词不批准 | `erase`（数据）、`remove`（物理）。在计算机语境中`delete`也是合法技术动词（规则 1.12）。不用`drop`或`destroy`。 |
| remove | 批准动词 | 保留。 |
| run、execute | 都不批准 | `operate` 表示 run，`do` 表示 execute。 |
| invoke、launch | 不在词典中 | 作为技术动词合法（规则 1.12）。 |
| display（动词）、render、present（动词） | 全部不批准 | `show` 涵盖大多数软件情况。官方替代：display → `show`、render → `make`、present → `give` 或 `show`。 |
| issue | 不在词典中 | 作为技术名词使用，或替换为`problem`（批准）。 |
| failure | 一般使用不批准；作为性能损耗的技术名词批准 | 仅用于性能错误："a failure of the pump"。 |
| error、problem | 批准名词 | 保留。 |

## 标准命名的反复出现的错误

词典导言列出了作者最常出错的词。这是软件相关集，仅裁定。

| 你写了 | STE 写法 |
|---|---|
| however | but |
| therefore | thus、as a result |
| since (= because) | because |
| any | 删除它，或重构："if you have any questions" → "if you have questions" |
| now | at this time。更好，删除它："now start the service" → "start the service" |
| need to、have to | 程序中用祈使句；描述性文本中用"it is necessary to" |
| perform | do |
| insert | put（但 SQL `INSERT` 保留：这是引用的文本） |
| reach | get、get to |
| avoid | prevent |
| repeat | do … again |
| acceptable | permitted。更好，给出限制："a latency of less than 200 ms" |
| complete（形容词） | completed |
| the example below、the section above | 命名目标，或将引用放在之后："the example that follows" |

## 严格自我检查

在 SKILL.md 的自我检查中添加这两步：

1. 在草稿中搜索上两表中每个动词。将每个命中替换为批准词。
2. 搜索你构建短语动词（"set up"、"go down"）。用单词动词替换每个（规则 9.3："install"、"decrease"）。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/strict-vocabulary.md -->
