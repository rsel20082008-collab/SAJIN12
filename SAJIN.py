import os
import re
import time
import httpx
from telebot import TeleBot, types

# ==================== Config / الإعدادات ====================
BOT_TOKEN = "8755365386:AAGEpYaJIpseoB3wLyNNBljbygcBzDidqjA"
ADMIN_ID = 8206337665
BOT_RIGHTS = "سجـ⚔️ـين"

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

# قاعدة بيانات مصغرة في الذاكرة لحفظ مستخدمي البوت للإحصائيات
USERS_FILE = "users.txt"

def get_users():
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def add_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

# هيدرز متصفح حقيقي متطور لتجاوز أنظمة الحظر والبروكسي
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

# ==================== Keyboards / لوحات التحكم والأزرار ====================
def main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_stats = types.KeyboardButton("📊 إحصائيات النظام")
    btn_help = types.KeyboardButton("ℹ️ كيفية الاستخدام")
    markup.add(btn_stats, btn_help)
    
    if user_id == ADMIN_ID:
        btn_admin = types.KeyboardButton("⚡ لوحة التحكم بالآدمن")
        markup.add(btn_admin)
        
    return markup

def inline_developer_markup():
    markup = types.InlineKeyboardMarkup()
    btn_dev = types.InlineKeyboardButton("👑 المطور: سجـ⚔️ـين", url=f"tg://user?id={ADMIN_ID}")
    markup.add(btn_dev)
    return markup

# ==================== Handlers / معالجات الأوامر ====================

@bot.message_handler(commands=['start'])
def welcome_start(message):
    add_user(message.chat.id)
    name = message.from_user.first_name
    
    welcome_msg = (
        f"<b>🌐 أهلاً بك يا {name} في أقوى بوت سحب سورس كود المواقع ⚡</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ <b>مميزات البوت:</b>\n"
        f"• سحب كود HTML الكامل بأعلى سرعة.\n"
        f"• تجاوز الحماية وجدران النارية بدون بروكسي معطل.\n"
        f"• إرسال السورس كملف جاهز للتعديل والاستخدام.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <b>أرسل رابط أي موقع الآن للبدء بالسحب مباشرة!</b>\n\n"
        f"👑 <b>الحقوق والملكية: {BOT_RIGHTS}</b>"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_msg,
        reply_markup=main_keyboard(message.chat.id)
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ كيفية الاستخدام")
def help_info(message):
    help_text = (
        f"<b>📖 طريقة الاستخدام البسيطة:</b>\n\n"
        f"1️⃣ قم بنسخ رابط الموقع المراد سحبه (مثال: <code>https://example.com</code>).\n"
        f"2️⃣ أرسل الرابط مباشرة هنا في المحادثة.\n"
        f"3️⃣ سينتظر البوت بضع ثوانٍ ويتصل بالسيرفر ليجلب لك الكود كاملاً داخل ملف جاهز.\n\n"
        f"👑 <b>تطوير وتصميم: {BOT_RIGHTS}</b>"
    )
    bot.reply_to(message, help_text, reply_markup=inline_developer_markup())

@bot.message_handler(func=lambda m: m.text == "📊 إحصائيات النظام")
def system_stats(message):
    total_users = len(get_users())
    stats_text = (
        f"<b>📊 إحصائيات البوت الحالية:</b>\n\n"
        f"👤 <b>عدد المستخدمين النشطين:</b> <code>{total_users}</code>\n"
        f"⚡ <b>حالة الخادم:</b> <code>ممتازة 🟢 (Railway Engine)</code>\n"
        f"👑 <b>صاحب البوت: {BOT_RIGHTS}</b>"
    )
    bot.reply_to(message, stats_text, reply_markup=inline_developer_markup())

@bot.message_handler(func=lambda m: m.text == "⚡ لوحة التحكم بالآدمن" and m.chat.id == ADMIN_ID)
def admin_panel(message):
    total_users = len(get_users())
    admin_text = (
        f"<b>⚡ لوحة تحكم الأدمن الرئيسي ({BOT_RIGHTS})</b>\n\n"
        f"👥 **إجمالي المشتركين:** <code>{total_users}</code>\n"
        f"🛠️ **يمكنك إدارة البوت وتفقده من هذه اللوحة.**"
    )
    bot.reply_to(message, admin_text)

# ==================== Main Fetch Logic / منطق سحب المواقع ====================

@bot.message_handler(func=lambda m: True)
def process_url_extraction(message):
    add_user(message.chat.id)
    raw_url = message.text.strip()
    
    # التخطي إذا كانت الكلمات خاصة باللوحة
    if raw_url in ["📊 إحصائيات النظام", "ℹ️ كيفية الاستخدام", "⚡ لوحة التحكم بالآدمن"]:
        return

    # ضبط صيغة الرابط
    url = raw_url
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    regex = r"^(https?://)?([\w.-]+)+[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?$"
    if not re.match(regex, url):
        bot.reply_to(
            message,
            "⚠️ <b>تنبيه:</b> يرجى إرسال رابط موقع إلكتروني صحيح ومعتمد!",
            reply_markup=main_keyboard(message.chat.id)
        )
        return

    start_time = time.time()
    
    status_msg = bot.reply_to(
        message,
        f"<b>⏳ جاري الاتصال المباشر وسحب السورس كود الكامل...</b>\n\n"
        f"🔗 <b>الموقع المطلوب:</b> <code>{url}</code>\n"
        f"👑 <b>بواسطة: {BOT_RIGHTS}</b>"
    )

    try:
        # الاتصال بالسيرفر سريعا باستخدام httpx المطور وبدون بروكسي محظور
        with httpx.Client(
            headers=HEADERS,
            verify=False,
            timeout=20.0,
            follow_redirects=True
        ) as client:
            response = client.get(url)

        elapsed_time = round(time.time() - start_time, 2)

        if response.status_code == 200:
            # استخراج النطاق لتسمية الملف بأناقة
            domain = url.split("//")[-1].split("/")[0].replace("www.", "")
            file_name = f"source_{domain}.html"

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(response.text)

            caption_text = (
                f"<b>✅ تم سحب السورس كود بنجاح وفخامة!</b>\n\n"
                f"🌐 <b>الموقع:</b> <code>{url}</code>\n"
                f"⚡ <b>استغرق السحب:</b> <code>{elapsed_time} ثانية</code>\n"
                f"📦 <b>حجم الملف:</b> <code>{len(response.content) / 1024:.1f} KB</code>\n\n"
                f"👑 <b>الحقوق والملكية: {BOT_RIGHTS}</b>"
            )

            with open(file_name, "rb") as file_to_send:
                bot.send_document(
                    message.chat.id,
                    file_to_send,
                    caption=caption_text,
                    reply_to_message_id=message.message_id,
                    reply_markup=inline_developer_markup()
                )

            bot.delete_message(message.chat.id, status_msg.message_id)

            if os.path.exists(file_name):
                os.remove(file_name)

        else:
            bot.edit_message_text(
                f"❌ <b>فشل الاتصال بالموقع المطلوب!</b>\n\n"
                f"⚠️ <b>رمز الاستجابة (Status Code):</b> <code>{response.status_code}</code>\n"
                f"👑 <b>الحقوق: {BOT_RIGHTS}</b>",
                chat_id=message.chat.id,
                message_id=status_msg.message_id
            )

    except Exception as err:
        error_details = str(err)[:150]
        bot.edit_message_text(
            f"❌ <b>حدث خطأ غير متوقع أثناء عملية السحب:</b>\n\n"
            f"<code>{error_details}</code>\n\n"
            f"👑 <b>تطوير: {BOT_RIGHTS}</b>",
            chat_id=message.chat.id,
            message_id=status_msg.message_id
        )

# ==================== التشغيل المستمر ====================
if __name__ == "__main__":
    print("========================================")
    print(f"  SAJIN BOT IS RUNNING SUCCESSFULLY!   ")
    print(f"  ADMIN ID: {ADMIN_ID}                ")
    print("========================================")
    bot.infinity_polling(skip_pending=True)
