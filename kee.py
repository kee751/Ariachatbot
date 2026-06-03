import os
from telethon import TelegramClient
from telethon.tl.functions.stories import GetPeerStoriesRequest
import asyncio

# Render သို့မဟုတ် Local Environment Variables မှ ယူခြင်း
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
# Session file name ကို သေချာသတ်မှတ်ပေးပါ
session_name = 'my_story_bot'

client = TelegramClient(session_name, int(api_id), api_hash)

async def download_stories(username):
    await client.start()
    try:
        entity = await client.get_input_entity(username)
        result = await client(GetPeerStoriesRequest(peer=entity))
        stories = result.stories.stories
        
        if not stories:
            return "No stories found."

        # Render မှာ file တွေ သိမ်းဖို့အတွက် /tmp folder ကို သုံးတာ ပိုကောင်းပါတယ်
        save_path = f"/tmp/{username}"
        os.makedirs(save_path, exist_ok=True)
        
        for i, story in enumerate(stories):
            await client.download_media(story.media, file=f"{save_path}/story_{i+1}")
        
        return f"Successfully downloaded {len(stories)} stories to {save_path}"
    except Exception as e:
        return f"Error: {str(e)}"

# အသုံးပြုရန်အတွက် loop 
if __name__ == '__main__':
    # ဤနေရာတွင် Bot ကို အမြဲ Run နေစေရန် logic ထည့်နိုင်သည်
    print("Bot is running...")
    client.run_until_disconnected()
    
