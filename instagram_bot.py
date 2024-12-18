import os
import instaloader
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# توکن ربات تلگرام خود را اینجا وارد کنید
TELEGRAM_BOT_TOKEN = '7069449754:AAFXt92cQnWkdSQsmEQUe-gi7fCvZXxfldw'
# پوشه‌ای که فایل‌ها در آن ذخیره می‌شوند
DOWNLOAD_FOLDER = './downloads/'

# بررسی وجود پوشه دانلود
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# تنظیمات اینستالودر
L = instaloader.Instaloader()

# تابع دانلود پست اینستاگرام
def download_instagram_post(url):
    try:
        # دریافت شناسه پست از URL
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # دانلود پست
        L.download_post(post, target=DOWNLOAD_FOLDER)
        return True
    except Exception as e:
        print(f"Error downloading post: {e}")
        return False

# تابع ارسال فایل به تلگرام
def send_file(chat_id, file_path):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        print(f"File sent to {chat_id}")
    except Exception as e:
        print(f"Error sending file: {e}")

# تابع هندلر پیام تلگرام
def handle_message(update, context):
    chat_id = update.message.chat_id
    message_text = update.message.text

    # بررسی اینکه آیا URL معتبر ارسال شده است
    if "instagram.com" in message_text:
        # دانلود پست اینستاگرام
        if download_instagram_post(message_text):
            # فایلی که دانلود شده است را ارسال کنید
            for file_name in os.listdir(DOWNLOAD_FOLDER):
                if file_name.endswith(".jpg") or file_name.endswith(".mp4"):
                    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
                    send_file(chat_id, file_path)
                    break
        else:
            update.message.reply_text("Error downloading the Instagram post.")
    else:
        update.message.reply_text("Please send a valid Instagram post URL.")

# تابع راه‌اندازی ربات
def start(update, context):
    update.message.reply_text("Send me an Instagram post URL and I will download and send the file.")

def main():
    # راه‌اندازی ربات تلگرام
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # اضافه کردن هندلرهای پیام و شروع
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # شروع کردن polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
