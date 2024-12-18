import os
import instaloader
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن بات تلگرام خود را وارد کنید
TOKEN = "7069449754:AAFXt92cQnWkdSQsmEQUe-gi7fCvZXxfldw"

# یک نمونه از instaloader برای دانلود محتویات
L = instaloader.Instaloader()

# پوشه‌ای که فایل‌ها در آن ذخیره می‌شوند
DOWNLOAD_DIR = './downloads'

# بررسی و ساخت پوشه ذخیره‌سازی فایل‌ها
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# تابعی که URL را دریافت می‌کند و فایل مربوطه را دانلود و ارسال می‌کند
def download_and_send(update: Update, context: CallbackContext):
    # دریافت URL از پیام کاربر
    url = update.message.text
    
    try:
        # بررسی اینکه URL یک اینستاگرام است یا نه
        if "instagram.com" in url:
            # دانلود پست از اینستاگرام
            shortcode = url.split("/")[-2]
            filename = os.path.join(DOWNLOAD_DIR, f"{shortcode}.jpg")
            
            # دانلود پست
            L.download_post(L.get_post_by_shortcode(shortcode), target=DOWNLOAD_DIR)
            
            # ارسال فایل به کاربر
            update.message.reply_photo(photo=open(filename, 'rb'))
        else:
            update.message.reply_text("لطفاً یک URL معتبر ارسال کنید.")
    except Exception as e:
        update.message.reply_text(f"خطا در دانلود فایل: {str(e)}")

# تابع اصلی برای راه‌اندازی بات
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # اضافه کردن دستورات برای مدیریت پیام‌ها
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_and_send))

    # شروع بات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
