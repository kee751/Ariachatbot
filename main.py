import os
from flask import Flask, request
import google.generativeai as genai
from telegram import Bot, Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Your name is Aria.

You are a friendly, intelligent AI assistant.
When someone asks your name, answer: My name is Aria.

Reply naturally and helpfully.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)


@app.route("/")
def home():
    return "Aria is running!"


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(
            request.get_json(force=True),
            bot
        )

        if not update.message:
            return "ok"

        if not update.message.text:
            return "ok"

        user = update.effective_user

        if user.username:
            mention = f"@{user.username}"
        else:
            mention = user.first_name or "User"

        user_message = update.message.text

        response = model.generate_content(user_message)

        ai_text = response.text

        final_text = f"{mention}\n\n{ai_text}"

        # User က Aria ရဲ့ message ကို reply လုပ်ထားရင်
        if (
            update.message.reply_to_message
            and update.message.reply_to_message.from_user
            and update.message.reply_to_message.from_user.id == bot.id
        ):
            bot.send_message(
                chat_id=update.effective_chat.id,
                text=final_text,
                reply_to_message_id=update.message.message_id
            )

        else:
            bot.send_message(
                chat_id=update.effective_chat.id,
                text=final_text
            )

    except Exception as e:
        print(f"Error: {e}")

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
        )
