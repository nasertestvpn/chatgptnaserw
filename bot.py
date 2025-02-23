from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai
import logging

# توکن‌های مورد نیاز
TELEGRAM_BOT_TOKEN = "7732712671:AAHnAWrVzKEe23qQ0_K5-_6brKe69zSdThs"
OPENAI_API_KEY = "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"

# تنظیم OpenAI
openai.api_key = OPENAI_API_KEY

# تنظیم لاگ‌گیری برای بررسی بهتر خطاها
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        # استفاده از مدل gpt-4o-mini
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # مدل gpt-4o-mini
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response['choices'][0]['message']['content']
        await update.message.reply_text(reply_text)
    
    except Exception as e:
        # در صورت بروز خطا، پیام دلخواه را به کاربر نشان می‌دهیم
        await update.message.reply_text(f"متاسفانه خطا رخ داده: {str(e)}")
        logger.error(f"Error occurred: {e}")  # لاگ خطا در سرور برای بررسی‌های بیشتر

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # دریافت پیام‌ها و ارسال به ChatGPT
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()
