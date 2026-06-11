import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# ───── TOKEN ─────
TOKEN = "8937716606:AAGVFt5O1A40c-EZMuCAbGm9GjNYrWPLgLQ"
bot = telebot.TeleBot(TOKEN)

# ───── تنظیمات ─────
CHANNELS = ["@v2ray_freex", "@ekko_vpn"]
BOT_USERNAME = "YOUR_BOT_USERNAME"
DATA_FILE = "data.json"

# ───── دیتابیس ─────
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

ref_count = data.get("ref_count", {})
user_refs = data.get("user_refs", {})
reward_done = data.get("reward_done", {})

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "ref_count": ref_count,
            "user_refs": user_refs,
            "reward_done": reward_done
        }, f, ensure_ascii=False, indent=4)

# ───── منو ─────
def menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("🎁 سرویس رایگان", "🛍️ خرید سرویس")
    m.add("👤 پشتیبانی")
    return m

# ───── جوین اجباری ─────
def join_button():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📢 کانال 1", url="https://t.me/v2ray_freex"))
    m.add(InlineKeyboardButton("📢 کانال 2", url="https://t.me/ekko_vpn"))
    m.add(InlineKeyboardButton("✅ بررسی عضویت", callback_data="check"))
    return m

def is_member(user_id):
    try:
        for ch in CHANNELS:
            member = bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

# ───── /start ─────
@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.from_user.id)
    args = message.text.split()

    if not is_member(message.from_user.id):
        bot.send_message(message.chat.id, "❗ اول عضو کانال‌ها شو 👇", reply_markup=join_button())
        return

    referral_sent = False

    # ───── رفرال ─────
    if len(args) > 1:
        ref_id = str(args[1])

        try:
            if (
                ref_id != user_id and
                user_id not in user_refs and
                ref_id.isdigit()
            ):

                user_refs[user_id] = ref_id
                ref_count[ref_id] = int(ref_count.get(ref_id, 0)) + 1

                save_data()

                bot.send_message(ref_id, "🎉 +1 رفرال گرفتی!")

                # ───── جایزه هر ۴ نفر ─────
                if ref_count[ref_id] % 4 == 0 and reward_done.get(ref_id) != ref_count[ref_id]:

                    reward_done[ref_id] = ref_count[ref_id]
                    save_data()

                    bot.send_message(
                        ref_id,
                        "🎉 تبریک!\n۴ دعوت کامل شد ✔\nبرای دریافت کانفیگ روی دکمه زیر بزن 👇",
                        reply_markup=InlineKeyboardMarkup().add(
                            InlineKeyboardButton("📋 دریافت کانفیگ", callback_data="get_config")
                        )
                    )

                referral_sent = True

        except:
            pass

    if not referral_sent:
        bot.send_message(
            message.chat.id,
            "👋 خوش آمدی\nیکی از گزینه‌ها را انتخاب کن:",
            reply_markup=menu()
        )

# ───── کانفیگ ─────
@bot.callback_query_handler(func=lambda call: call.data == "get_config")
def get_config(call):

    CONFIG = """
🎁 اشتراک هدیه شما آماده شد

👤 نام کاربری: YRh_4046946
🔢 پلن: زیرمجموعه
📌 لوکیشن: مولتی لوکیشن
📈 حجم: نامحدود

🔑 کانفیگ‌ها:

vless://0058c215-ab1e-400c-a403-b5b2fda7e846@151.101.109.223:80
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@speedtest.net:80
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@167.82.0.1:80

vless://0058c215-ab1e-400c-a403-b5b2fda7e846@151.101.0.1:80
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@fast-domain-gb.dhbhvfbhfbvhfbvhfbhv.shop:2096
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@fast-domain-gb.dhbhvfbhfbvhfbvhfbhv.shop:2095
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@pishdad.org:8080
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@www.speedtest.org:8080
vless://0058c215-ab1e-400c-a403-b5b2fda7e846@www.parsvds.com:8080
"""

    bot.send_message(call.message.chat.id, CONFIG)

# ───── بررسی عضویت ─────
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if is_member(call.from_user.id):
        bot.send_message(call.message.chat.id, "✔ عضویت تایید شد", reply_markup=menu())
    else:
        bot.send_message(call.message.chat.id, "❌ هنوز عضو کانال‌ها نیستی")

# ───── سرویس رایگان ─────
@bot.message_handler(func=lambda m: m.text == "🎁 سرویس رایگان")
def free(m):

    user_id = str(m.from_user.id)
    link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    text = f"""
🎁 چگونه سرویس رایگان بگیریم؟

📲 لینک دعوت:
{link}

📊 تعداد دعوت: {ref_count.get(user_id,0)} نفر

🎯 هر ۴ دعوت = کانفیگ رایگان

⚠️ عضویت در کانال الزامی است
"""

    bot.send_message(m.chat.id, text, reply_markup=menu())

# ───── خرید ─────
@bot.message_handler(func=lambda m: m.text == "🛍️ خرید سرویس")
def buy(m):
    bot.send_message(m.chat.id, "❌ فروشگاه فعلاً بسته است")

# ───── پشتیبانی ─────
@bot.message_handler(func=lambda m: m.text == "👤 پشتیبانی")
def support(m):
    bot.send_message(m.chat.id, "📩 پشتیبانی: @SARAV2RAY")

print("Bot is running...")
bot.infinity_polling()
