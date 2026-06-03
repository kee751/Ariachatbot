import os
from flask import Flask
from threading import Thread

# ရိုးရှင်းတဲ့ Web Server တစ်ခု တည်ဆောက်ခြင်း
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Bot မစခင် Web Server ကို အရင် run ပေးခြင်း
t = Thread(target=run)
t.start()

import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Environment Variables မှ Key များကို ခေါ်ယူခြင်း
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def get_ai_response(user_input):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly, sweet, and helpful girl named Aria. Always speak in a polite and feminine tone in Burmese. Use emojis occasionally."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"အို... တစ်ခုခုမှားသွားပြီရှင်။ ({e})"

# Telegram Bot အတွက် စာပြန်ပေးမည့် Function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = get_ai_response(user_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

if __name__ == '__main__':
    # Telegram Application ကို တည်ဆောက်ခြင်း
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Message ရောက်လာရင် handle_message ကို သွားခိုင်းခြင်း
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    print("Aria Bot is running...")
    application.run_polling()
    
