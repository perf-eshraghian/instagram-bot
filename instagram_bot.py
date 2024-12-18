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

# تابعی که پوشه را چک می‌کند و در صورت نیاز آن را می‌سازد
def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# تابعی که URL را دریافت می‌کند و فایل مربوطه را دانلود و ارسال می‌کند
def download_and_send(update: Update, context: CallbackContext):
    # دریافت URL از پیام کاربر
    url = update.message.text
    
    try:
        # بررسی اینکه URL یک اینستاگرام است یا نه
        if "instagram.com" in url:
            # اسلاید کوتاه از URL استخراج می‌شود
            shortcode = url.split("/")[-2]
            
            # مسیر پوشه برای ذخیره فایل‌ها
            post_dir = os.path.join(DOWNLOAD_DIR, shortcode)
            
            # اطمینان از وجود پوشه مربوطه
            ensure_directory_exists(post_dir)
            
            # فایل نهایی که دانلود می‌شود
            filename = os.path.join(post_dir, f"{shortcode}.jpg")
            
            # اگر فایل موجود است، آن را حذف کن
            if os.path.exists(filename):
                os.remove(filename)
                update.message.reply_text(f"فایل قدیمی حذف شد و در حال دانلود مجدد هستیم...")

            # دانلود پست اینستاگرام
            L.download_post(L.get_post_by_shortcode(shortcode), target=post_dir)
            
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
