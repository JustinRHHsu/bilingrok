# 支持多語系
支持語系列表 `/config/language_list.csv`
各語系文案配置檔 `/config/translation`

# 支持範圍
- LINE Message
- LINE Quick Reply Item
- LINE Flex Message (Alt Content, Title, Button)
x LINE Welcome Message
x LINE 選單圖示


# 配置規則說明
- 語系設置：用戶能設置母語(native_lang)和目標學習語言(target_lang)，默認設置 native_lang=zh-tw、target_lang=en-us
- Message
    - Command Message：系統訊息，使用 native_lang 幫助用戶完成相關的設置，包括 message, flex message 的 title, content, alt content 等
    - General Message：一般訊息，聊天內容使用 target_lang 和用戶聊天對話，以練習該目標語言
- 存取各語系 script 的系統邏輯
    - reply message 的組裝：
        - Text_Message, Flex Message 的消息類型組裝時
        - 指定 native_lang 後，讀取該語言配置檔，如：/config/translations/zh-tw.json
        - 業務邏輯中，存取特定的文案變數 (如：translations['api_key_success'])，存取到該語系的文案
- 配置文件說明
    - key ：文案編號
    - value：儲存該語言的文案內容
        - Type: 
            - sys_msg         ：為 LINE message，為系統的回應文案
            - warning         ：為 LINE message，為系統警示的文案
            - quick_reply_btn ：為 LINE 快捷回捷(Quick Reply Item) 標籤
            - flex_ 開題       ：為 Flex Message，如：flex_alt_content, flex_body_title, flex_btn
        - Text:
            該文案在該語言的翻譯內容
        - Desc:
            全為繁體中文，說明該文案使用的位置、情境等
    - 說明資料：
        第一筆記錄，為該語系的配置檔說明，用來提供給該語言為母語人士的編輯者、審閱者，更好瞭解該語系配置檔的結構 schema
        "json_format_description": {
            "text": "此語系配置檔的翻譯內容",
            "desc": "描述顯示此翻譯內容的觸發條件和位置等",
            "type": "sys_msg, warning 為 LINE message； quick_reply_btn 為 LINE 快捷回捷標籤； flex_ 開題為 Flex Message，如：flex_alt_content, flex_body_title, flex_btn"
        }



# 注意事項
- 字串內用單引號：
    顯示的文案中應使用單引號，使用雙引號會造成解析錯誤。例如：{"btn_title": "Let's Go!"}
- Key-Value 用雙引號：
    JSON 格式資料中，Key 和 Value 要用雙引號表示，整數和布林型態可以不用。例如：{"btn_title": "Let's Go!"}
- 存取字典的資料用雙引號：
    當 JSON 讀出儲存在 Dictionary 型態的變數時，key 值要用雙引號。例如：translations["btn_title"]
- LINE 的字數限制：
    各 type 類型對應的長度限制
    - sys_msg, warning 類型：
        每則 message 的長度不超過 2000 個字元
    - quick_reply_btn 類型：
        - 每個 item 最多 20 個字元
    - flex_ 開題類型：
        - flex_alt_content：最多 400 個字元
        - flex_body_title：最多 400 個字元
        - flex_btn：
            - label：每個 item 最多 20 個字元
            - text：不超過 300 個字元
- Reply Message 限制：
    - User 每一則 message 會獲得一個 reply_token
    - 一個 reply_token 的時效約 30 秒
    - 一個 reply_token 最多可以回覆 5 則 message，可以是各種類型的 message
    - LINE 平台對於每次請求最多可包含 5 則訊息的限制
    - 單則文字訊息的內容長度限制為 2000 個字元
    - 總字元數超過 10000 個可能需要進行多次請求


# 更新各語系文案流程
- 以 zh-tw 台灣繁體為主要編輯
- 利用 Github Copilot 協作





## 情況 I：檢查長度
    - 選擇全部文案配置檔，成為上下文
    - 讓 AI 具體檢查符合"條件" 的 "每筆" 資料
    - 提供"每筆"記錄完成的配置內容
    - Apply in Editor

Prompt Exaplme
///
計算出每筆 type = quick_reply_btn 的 text 資料，有多少字元
將超過 20字元的文案重新翻譯，符合其規則
///


///
計算每筆 type=flex_btn 的 text 資料，是否有超過 30 個字元。如果有，重新翻譯文案
///