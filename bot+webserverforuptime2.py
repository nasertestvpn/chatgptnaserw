import openai
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# توکن‌های مورد نیاز
TELEGRAM_BOT_TOKEN = "7732712671:AAHnAWrVzKEe23qQ0_K5-_6brKe69zSdThs"
OPENAI_API_KEY = "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"

# تنظیم OpenAI
openai.api_key = OPENAI_API_KEY

# تنظیم لاگ‌گیری
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# سرور Flask برای جلوگیری از خاموش شدن در هاست‌های رایگان
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)

# اجرای Flask در یک ترد جداگانه
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# تابع پردازش پیام و ارسال به ChatGPT
async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # استفاده از مدل gpt-4o-mini
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response['choices'][0]['message']['content']
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text("متاسفانه خطایی رخ داده، لطفاً بعداً امتحان کنید.")
        logger.error(f"خطا: {e}")

# راه‌اندازی ربات تلگرام
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    logger.info("ربات تلگرام در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
