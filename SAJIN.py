import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

# ------------------------------------------------------------------------------
# Config & Setup
# ------------------------------------------------------------------------------
TOKEN = "8755365386:AAGEpYaJIpseoB3wLyNNBljbygcBzDidqjA"
ADMIN_ID = 8206337665  # أصلح هذا الأيدي لاحقاً بآيدي حسابه
BOT_VERSION = " SAJIN TOP s1 "

bot = telebot.TeleBot(TOKEN)

# Storage (In-Memory for performance)
users_db = set()
stats_db = {"scrapes": 0, "start_time": time.time()}
user_cache = {}

# Header Spoofing for Fast Scraping
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

# ------------------------------------------------------------------------------
# Keyboards & Formatting Engine
# ------------------------------------------------------------------------------
def get_main_keyboard(is_admin=False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("👑 المطور", url="https://t.me/A0_XX")
    b2 = types.InlineKeyboardButton("💯 القناة الرسمية", url="https://t.me/X_I_I_1")
    b3 = types.InlineKeyboardButton("📊 إحصائيات النظام", callback_data="system_stats")
    b4 = types.InlineKeyboardButton("⚙️ الميزات المتقدمة", callback_data="bot_features")
    
    markup.add(b1, b2)
    markup.add(b3, b4)
    if is_admin:
        markup.add(types.InlineKeyboardButton("⚡ لوحة التحكم بالآدمن", callback_data="admin_panel"))
    return markup

def get_action_keyboard(url):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_html = types.InlineKeyboardButton("🌐 HTML Source", callback_data="act_html")
    btn_txt = types.InlineKeyboardButton("📝 Raw Text", callback_data="act_raw")
    btn_headers = types.InlineKeyboardButton("🛡️ HTTP Headers", callback_data="act_headers")
    btn_tech = types.InlineKeyboardButton("🔍 كشف التقنيات", callback_data="act_tech")
    btn_links = types.InlineKeyboardButton("🔗 استخراج الروابط", callback_data="act_links")
    btn_media = types.InlineKeyboardButton("🖼️ استخراج الصور", callback_data="act_media")
    btn_info = types.InlineKeyboardButton("📌 معلومات SEO", callback_data="act_seo")
    btn_refresh = types.InlineKeyboardButton("🔄 إعادة فحص", callback_data="act_recheck")
    btn_dev = types.InlineKeyboardButton("👑 المطور", url="https://t.me/A0_XX")
    btn_chan = types.InlineKeyboardButton("💯 القناة", url="https://t.me/X_I_I_1")
    
    markup.add(btn_html, btn_txt)
    markup.add(btn_headers, btn_tech)
    markup.add(btn_links, btn_media)
    markup.add(btn_info, btn_refresh)
    markup.add(btn_dev, btn_chan)
    return markup

# ------------------------------------------------------------------------------
# Core Logic & Utilities
# ------------------------------------------------------------------------------
def clean_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def get_uptime():
    seconds = int(time.time() - stats_db["start_time"])
    return str(datetime.timedelta(seconds=seconds))

def save_and_send_file(chat_id, content, filename, caption):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    with open(filename, "rb") as f:
        bot.send_document(chat_id, f, caption=caption, parse_mode="Markdown")
    if os.path.exists(filename):
        os.remove(filename)

# ------------------------------------------------------------------------------
# Command Handlers
# ------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    users_db.add(message.chat.id)
    is_admin = (message.chat.id == ADMIN_ID)
    
    start_text = (
        "⚡ ═════════════════════ ⚡\n"
        "🔥 **أهلاً بك في البوت الأسطوري لسحب وتفكيك المواقع** 🔥\n"
        "⚡ ═════════════════════ ⚡\n\n"
        "👑 **صاحب الحقوق والمطور:** [SAJIN](https://t.me/A0_XX)\n"
        "📢 **القناة الرسمية للسورس:** [@X_I_I_1](https://t.me/X_I_I_1)\n"
        f"🚀 **إصدار المحرك:** `{BOT_VERSION}`\n"
        "───────────────────\n\n"
        "🌐 **مميزات البوت:**\n"
        " • سحب كود الـ HTML كاملاً بدقة عالية.\n"
        " • استخراج الملفات المباشرة والنصوص الخام.\n"
        " • كشف تقنيات الموقع (Server, CMS, Frameworks).\n"
        " • استخراج الروابط المضمنة والوسائط بالكامل.\n"
        " • فحص وسحب بيانات الـ HTTP Headers و SEO.\n\n"
        "🎯 **طريقة الاستخدام:**\n"
        "أرسل رابط أي موقع الآن مباشرة للشات (مثال: `google.com`)"
    )
    
    bot.reply_to(
        message, 
        start_text, 
        parse_mode="Markdown", 
        reply_markup=get_main_keyboard(is_admin),
        disable_web_page_preview=True
    )

@bot.message_handler(commands=['stats'])
def handle_stats_cmd(message):
    msg = (
        "📊 **إحصائيات النظام الفائقة:**\n\n"
        f"👥 عدد المستخدمين: `{len(users_db)}`\n"
        f"⚡ إجمالي عمليات السحب: `{stats_db['scrapes']}`\n"
        f"⏱️ مدة تشغيل السيرفر: `{get_uptime()}`\n"
        f"🟢 حالة الخادم: `Online (High Performance)`"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

# ------------------------------------------------------------------------------
# URL Processing
# ------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: True)
def process_user_url(message):
    url = clean_url(message.text)
    users_db.add(message.chat.id)
    
    regex = r"^(?:http|ftp)s?://" \
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))" \
            r"(?::\d+)?" \
            r"(?:/?|[/?]\S+)$"
            
    if not re.match(regex, url, re.IGNORECASE):
        bot.reply_to(message, "❌ **الرابط غير صالح!** يرجى التأكد من كتابة رابط موقع صحيح.")
        return

    user_cache[message.chat.id] = url
    
    text = (
        "⚡ ═════════════════════ ⚡\n"
        "🎯 **تم استلام الرابط وتجهيز المحرك!**\n"
        "⚡ ═════════════════════ ⚡\n\n"
        f"🔗 **الموقع المحدد:** `{url}`\n"
        "👑 **المطور:** @A0_XX | 📢 **القناة:** @X_I_I_1\n\n"
        "👇 **اختر العملية المطلوب تنفيذها فوراً من الأزرار التالية:**"
    )
    
    bot.reply_to(message, text, parse_mode="Markdown", reply_markup=get_action_keyboard(url), disable_web_page_preview=True)

# ------------------------------------------------------------------------------
# Callback Query Handler (Fast Action Engine)
# ------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    # إجابة فورية للأزرار لمنع التحميل المستمر
    bot.answer_callback_query(call.id, text="⚡ جاري تنفيذ الطلب بواسطة محرك SAJIN...")
    
    chat_id = call.message.chat.id
    url = user_cache.get(chat_id)
    
    # 1. System Options
    if call.data == "system_stats":
        msg = (
            "📊 **إحصائيات البوت المباشرة** 📊\n\n"
            f"👤 عدد الأعضاء: `{len(users_db)}`\n"
            f"🚀 العمليات الناجحة: `{stats_db['scrapes']}`\n"
            f"⏱️ التشغيل المستمر: `{get_uptime()}`\n\n"
            "👑 **تطوير:** @A0_XX"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")
        return

    elif call.data == "bot_features":
        feat = (
            "⚡ **ميزات نظام SAJIN SCRAPER Ultimate:**\n\n"
            "1️⃣ **سحب السورس كاملاً:** بدون فقدان أي كود.\n"
            "2️⃣ **استخراج الوسائط:** جميع صور الصفحات بنفس اللحظة.\n"
            "3️⃣ **كشف التقنيات:** معرفة لغات ومكتبات الموقع.\n"
            "4️⃣ **استخراج الروابط:** تجميع جميع اللينكات داخل ملف.\n"
            "5️⃣ **سرعة الخادم:** معالجة فائقة بدون توقف."
        )
        bot.send_message(chat_id, feat, parse_mode="Markdown")
        return

    elif call.data == "admin_panel" and chat_id == ADMIN_ID:
        adm = (
            "⚙️ **لوحة تحكم المسؤول (ADMIN):**\n\n"
            f"• إجمالي المستخدمين: `{len(users_db)}`\n"
            f"• عمليات السحب: `{stats_db['scrapes']}`\n"
            f"• السيرفر: `Active`"
        )
        bot.send_message(chat_id, adm, parse_mode="Markdown")
        return

    # Check URL existence
    if not url:
        bot.send_message(chat_id, "❌ **خطأ:** انتهت الجلسة. أرسل رابط الموقع مجدداً.")
        return

    # Fetch Request
    try:
        start_t = time.time()
        res = requests.get(url, headers=HEADERS, timeout=12)
        end_t = round(time.time() - start_t, 2)
        stats_db["scrapes"] += 1
        
        # Actions
        if call.data == "act_html":
            filename = f"Source_{chat_id}.html"
            caption = (
                "✅ **تم سحب ملف الـ HTML بنجاح!**\n\n"
                f"🌐 **الموقع:** `{url}`\n"
                f"⏱️ **استغرق:** `{end_t} ثانية`\n\n"
                "👑 **تطوير:** @A0_XX | 📢 **القناة:** @X_I_I_1"
            )
            save_and_send_file(chat_id, res.text, filename, caption)

        elif call.data == "act_raw":
            soup = BeautifulSoup(res.text, 'html.parser')
            text_content = soup.get_text(separator='\n')
            filename = f"RawText_{chat_id}.txt"
            caption = (
                "📝 **تم استخراج النص الخام بالموقع!**\n\n"
                f"🌐 **الموقع:** `{url}`\n\n"
                "👑 **تطوير:** @A0_XX | 📢 **القناة:** @X_I_I_1"
            )
            save_and_send_file(chat_id, text_content, filename, caption)

        elif call.data == "act_headers":
            headers_str = "\n".join([f"{k}: {v}" for k, v in res.headers.items()])
            msg = (
                "🛡️ **معلومات الـ HTTP Response Headers:**\n\n"
                f"🌐 `{url}`\n"
                f"📊 **Status Code:** `{res.status_code}`\n\n"
                f"```yaml\n{headers_str}\n```\n"
                "👑 **تطوير:** @A0_XX"
            )
            bot.send_message(chat_id, msg, parse_mode="Markdown")

        elif call.data == "act_tech":
            server = res.headers.get("Server", "غير معروف")
            powered = res.headers.get("X-Powered-By", "غير معروف")
            soup = BeautifulSoup(res.text, 'html.parser')
            
            scripts = [s.get('src') for s in soup.find_all('script') if s.get('src')]
            has_react = any("react" in s.lower() for s in scripts)
            has_vue = any("vue" in s.lower() for s in scripts)
            has_jquery = any("jquery" in s.lower() for s in scripts)
            has_bootstrap = any("bootstrap" in str(soup).lower() for s in soup.find_all('link'))
            
            tech_msg = (
                "🔍 **تحليل وتقنيات الموقع (Tech Detection):**\n\n"
                f"🌐 **الموقع:** `{url}`\n"
                f"🖥️ **السيرفر:** `{server}`\n"
                f"⚡ **محرّك التشغيل:** `{powered}`\n"
                "───────────────\n"
                "📌 **المكتبات المكتشفة:**\n"
                f"• React.js: {'✅ نعم' if has_react else '❌ لا'}\n"
                f"• Vue.js: {'✅ نعم' if has_vue else '❌ لا'}\n"
                f"• jQuery: {'✅ نعم' if has_jquery else '❌ لا'}\n"
                f"• Bootstrap: {'✅ نعم' if has_bootstrap else '❌ لا'}\n\n"
                "👑 **تطوير:** @A0_XX | @X_I_I_1"
            )
            bot.send_message(chat_id, tech_msg, parse_mode="Markdown")

        elif call.data == "act_links":
            soup = BeautifulSoup(res.text, 'html.parser')
            links = list(set([a.get('href') for a in soup.find_all('a') if a.get('href')]))
            content = f"🔗 إجمالي الروابط المستخرجة من {url} ({len(links)} رابط):\n\n" + "\n".join(links)
            filename = f"Links_{chat_id}.txt"
            caption = f"🔗 **تم استخراج جميع روابط الموقع!** ({len(links)} رابط)\n\n👑 **تطوير:** @A0_XX"
            save_and_send_file(chat_id, content, filename, caption)

        elif call.data == "act_media":
            soup = BeautifulSoup(res.text, 'html.parser')
            images = list(set([img.get('src') for img in soup.find_all('img') if img.get('src')]))
            content = f"🖼️ إجمالي روابط الصور في {url} ({len(images)} صورة):\n\n" + "\n".join(images)
            filename = f"Media_{chat_id}.txt"
            caption = f"🖼️ **تم استخراج جميع صور الموقع!** ({len(images)} صورة)\n\n👑 **تطوير:** @A0_XX"
            save_and_send_file(chat_id, content, filename, caption)

        elif call.data == "act_seo":
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.string if soup.title else "بدون عنوان"
            desc = "غير محدد"
            keywords = "غير محدد"
            
            for meta in soup.find_all('meta'):
                if meta.get('name', '').lower() == 'description':
                    desc = meta.get('content', 'غير محدد')
                if meta.get('name', '').lower() == 'keywords':
                    keywords = meta.get('content', 'غير محدد')
                    
            seo_msg = (
                "📌 **تحليل بيانات SEO للموقع:**\n\n"
                f"🌐 **الموقع:** `{url}`\n"
                f"✏️ **العنوان (Title):** `{title}`\n"
                f"📝 **الوصف (Description):** `{desc}`\n"
                f"🔑 **الكلمات المفتاحية:** `{keywords}`\n\n"
                "👑 **تطوير:** @A0_XX"
            )
            bot.send_message(chat_id, seo_msg, parse_mode="Markdown")

        elif call.data == "act_recheck":
            bot.send_message(chat_id, "🔄 **تم تحديث الجلسة، يمكنك إعادة اختيار العملية.**")

    except Exception as e:
        bot.send_message(chat_id, f"❌ **حدث خطأ أثناء الاتصال بالموقع:**\n`{str(e)}`", parse_mode="Markdown")

# ------------------------------------------------------------------------------
# Boot Engine
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("==================================================")
    print("  SAJIN ULTIMATE SCRAPER BOT STARTED SUCCESSFULLY ")
    print("  DEVELOPED BY: @A0_XX | CHANNEL: @X_I_I_1        ")
    print("==================================================")
    bot.infinity_polling(skip_pending=True)
