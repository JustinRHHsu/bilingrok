# 組裝各種 Message Type 成 all_messages 變數，讓 reply_message.py 可以送給 LINE server 發送
    
# (1) Image Message: create_image_message(img_url, img_url)
bucket_name = 'linebot_materials'
blob_name = 'sub_1.png'
signed_url = generate_signed_url(bucket_name, blob_name, 120)
image_message = create_image_message(signed_url, signed_url)

# (2) Text Message only
text = "Hello, world!"
message_1 = create_text_message(text)

# (3) Text Message with Quick Reply Items: create_quick_reply_message(text, purchase_items)
text = "選擇您想訂閱的服務類型？"
# 從 purchase_items.csv 讀取所有支援的購買項目
purchase_items = []
with open('./config/purchase_items.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not row:  # 檢查是否為空行
            continue
        print(f"row:{row}")
        purchase_items.append({'label': row[1], 'text': row[0]})  # 組裝成指定格式
        print(f"purchase_items:{purchase_items[-1]}")

text_message = create_quick_reply_message(text, purchase_items)

# (3) Flex Message: create_flex_message(alt, flex_filename)
alt = 'Subscribe NOW!'
flex_filename = 'flex_purchase'
flex_message = create_flex_message(alt, flex_filename)

# (4) 組裝所有訊息
all_messages = [image_message_1, image_message_2, flex_message, text_message]