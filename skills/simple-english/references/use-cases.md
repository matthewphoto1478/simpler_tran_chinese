# 文件以外的使用場景

STE 為飛機維護手冊而構建。同樣的屬性轉移到任何誤讀會造成損失的文字：一詞一義、簡短句子、條件優先命令。以下每種場景指明模式和適配。

## 錯誤訊息和 CLI 輸出

模式：程式性。錯誤訊息是對正處於失敗中的讀者的指令。

模式：陳述發生了什麼（一般過去時），陳述原因如果已知，給出修復的命令或條件。

> 錯誤前：Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials are properly configured and try again.
> 錯誤後：Connection to the database failed. The password for user `app` was not correct. Set `DB_PASSWORD` and connect again.

## 運維手冊和標準操作程式

模式：程式性。值班運維手冊是維護手冊，而維護手冊正是 STE 為之編寫的文字型別。

- 每步都是祈使句，每步一條指令，條件優先。
- 警告在其步驟之前：命令優先，風險其次。
- 每句不超過 20 詞。

## 故障報告和事後分析

模式：描述性，僅用一般過去時。完成時態的現在完成時（"we have identified"）隱藏了事情發生的時間。

> 錯誤前：We have identified an issue that may have impacted some users' ability to access the service.
> 錯誤後：Between 14:02 and 14:31 UTC, 12% of requests failed. A deploy at 14:00 removed the cache warmup step.

STE 禁止模糊表達如"may have impacted"。報告陳述已知內容，其餘說"unknown"。

## 提交訊息和 PR 描述

模式：祈使句標題，描述性正文。慣例已符合 STE。應用詞替換和正文 25 詞限制。刪除"this PR aims to"。

## API 變更日誌和釋出說明

模式：描述性。可能時一條內容、一個變更、一句話。"Breaking:" 條目遵循警告模式，命令優先："Update your calls to `v2/users`. The `name` field split into `first_name` and `last_name`."

## AI 代理指令（提示、AGENTS.md、Skill）

模式：程式性。系統提示是對無法提問的讀者的程式。

- 每句一條指令使每條規則可引用、難以半途而廢。
- 一詞一義防止模型將"check"、"verify"和"validate"視為三個操作。
- 條件優先（"If the build fails, stop"）勝過拖尾條件，模型會忽略拖尾條件。
- 不用"should"。模型將"should"視為可選。寫"must"或刪除規則。

## 支援宏和狀態頁更新

模式：描述性，25 詞限制。這些訊息的許多讀者是母語非英語者。

> 錯誤前：We sincerely apologize for any inconvenience this may have caused.
> 錯誤後：The API was down for 18 minutes. Uploads made during this time were saved and will process today.

## 翻譯和本地化準備

模式：嚴格。STE 如此編寫以使母語非英語的維護人員能閱讀英語手冊。同樣的規則為機器翻譯準備文字。一詞一義和完整語法（冠詞、"that"）消除了譯者必須猜測的許多歧義。

## UI 文字和空狀態

模式：程式性，硬性長度限制。按鈕和標籤是技術名稱，免於規則。正文遵循規則："No projects yet. Create a project to start."

## STE 不適用的地方

不要將 STE 用於營銷頁面、釋出帖子、部落格帖子或品牌寫作。STE 刪除說服力。用你自己的文風寫那些文字，用 STE 寫它們連結到的文件。

<!-- 原文：https://github.com/AminBlg/SimpleEnglish/blob/main/skills/simple-english/references/use-cases.md -->
