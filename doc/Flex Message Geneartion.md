

# 1. Find an example from Google

# 2. Paste the screen to ChatGPT to generate the Flex Message JSON

# 3. Paste the Flex Message JSON on Flex Message JSON simulator
https://developers.line.biz/flex-simulator/?status=success

# 4. Create a Flex Message .json file
/Users/JustinHsu/aiagent/grok-lang-companion/line_message_template/flex_library/flex_purchase.json

# 5. Call `create_flex_message` from line_bot_message_builder.py 
create_flex_message(alt_text, json_filename)