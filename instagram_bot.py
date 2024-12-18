from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader
import os

# توکن ربات خود را جایگزین کنید
TELEGRAM_BOT_TOKEN = "7069449754:AAFXt92cQnWkdSQsmEQUe-gi7fCvZXxfldw"
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# پیام خوشامدگویی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک پست اینستاگرام رو برام بفرست تا محتواش رو برات دانلود کنم.")

# دانلود محتوای اینستاگرام
async def download_instagram_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    # بررسی لینک
    if "instagram.com" not in url:
        await update.message.reply_text("لطفاً یک لینک معتبر اینستاگرام ارسال کنید.")
        return

    try:
        # استفاده از Instaloader برای دانلود
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        filename = f"{post.owner_username}_{post.shortcode}.jpg"

        # دانلود پست به پوشه‌ای مشخص
        target_dir = f"./downloads/{post.owner_username}"
        os.makedirs(target_dir, exist_ok=True)
        loader.download_post(post, target=target_dir)

        # ارسال فایل به کاربر
        file_path = os.path.join(target_dir, filename)
        with open(file_path, "rb") as file:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)
        await update.message.reply_text("پست با موفقیت دانلود شد!")
    except Exception as e:
        await update.message.reply_text(f"مشکلی پیش اومده: {str(e)}")

# تنظیم ربات
def main():
    # ساخت برنامه ربات
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # اضافه کردن دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram_post))

    # راه‌اندازی ربات
    application.run_polling()

if __name__ == "__main__":
    main()
