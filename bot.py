import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# ───── TOKEN ─────
TOKEN = "8937716606:AAGVFt5O1A40c-EZMuCAbGm9GjNYrWPLgLQ"
bot = telebot.TeleBot(TOKEN)

# ───── SETTINGS ─────
CHANNELS = ["@v2ray_freex", "@ekko_vpn"]
BOT_USERNAME = "V2RAY_FREEX1_bot"
DATA_FILE = "data.json"

# ───── CONFIG ─────
CONFIG_TEXT = """
✅ اشتراک هدیه شما

📌 لوکیشن: Germany
📈 حجم: نامحدود

🔑 کانفیگ‌ها:

vless://0058c215-ab1e-400c-a403-b5b2fda7e846@151.101.109.223:80?security=none&type=ws

vless://0058c215-ab1e-400c-a403-b5b2fda7e846@speedtest.net:80?security=none&type=ws

vless://0058c215-ab1e-400c-a403-b5b2fda7e846@167.82.0.1:80?security=none&type=ws
"""

# ───── LOAD DATA ─────
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

# ───── SAVE ─────
def save():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "ref_count": ref_count,
            "user_refs": user_refs,
            "reward_done": reward_done
        }, f, ensure_ascii=False, indent=4)

# ───── MENU ─────
def menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add("🎁 سرویس رایگان", "🛍️ خرید سرویس")
    m.add("👤 پشتیبانی")
    return m

# ───── JOIN BUTTON ─────
def join_btn():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📢 کانال 1", url="https://t.me/v2ray_freex"))
    m.add(InlineKeyboardButton("📢 کانال 2", url="https://t.me/ekko_vpn"))
    m.add(InlineKeyboardButton("✅ بررسی عضویت", callback_data="check"))
    return m

# ───── CHECK MEMBER ─────
def is_member(user_id):
    try:
        for ch in CHANNELS:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

# ───── START ─────
@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.from_user.id)
    args = message.text.split()

    if not is_member(message.from_user.id):
        bot.send_message(message.chat.id, "❌ اول عضو کانال‌ها شو", reply_markup=join_btn())
        return

    sent = False

    # ───── REFERRAL ─────
    if len(args) > 1:
        ref_id = str(args[1])

        try:
            if (
                ref_id != user_id and
                user_id not in user_refs and
                ref_id.isdigit()
            ):

                user_refs[user_id] = ref_id
                ref_count[ref_id] = ref_count.get(ref_id, 0) + 1
                save()

                bot.send_message(ref_id, "🎉 +1 رفرال گرفتی!")

                # ───── REWARD ─────
                if ref_count[ref_id] % 4 == 0 and reward_done.get(ref_id) != ref_count[ref_id]:

                    reward_done[ref_id] = ref_count[ref_id]
                    save()

                    btn = InlineKeyboardMarkup()
                    btn.add(InlineKeyboardButton("📦 دریافت کانفیگ", callback_data="config"))

                    bot.send_message(
                        ref_id,
                        "🎉 ۴ رفرال کامل شد!",
                        reply_markup=btn
                    )

                sent = True

        except:
            pass

    if not sent:
        bot.send_message(message.chat.id, "👋 خوش آمدی", reply_markup=menu())

# ───── CONFIG BUTTON ─────
@bot.callback_query_handler(func=lambda c: c.data == "config")
def config(call):
    bot.send_message(call.message.chat.id, CONFIG_TEXT)

# ───── CHECK JOIN ─────
@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(call):
    if is_member(call.from_user.id):
        bot.send_message(call.message.chat.id, "✅ تایید شد", reply_markup=menu())
    else:
        bot.send_message(call.message.chat.id, "❌ هنوز عضو نیستی")

# ───── FREE ─────
@bot.message_handler(func=lambda m: m.text == "🎁 سرویس رایگان")
def free(m):
    user_id = str(m.from_user.id)
    link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    bot.send_message(
        m.chat.id,
        f"🎁 لینک دعوت:\n{link}\n\n📊 رفرال: {ref_count.get(user_id,0)}",
        reply_markup=menu()
    )

# ───── BUY ─────
@bot.message_handler(func=lambda m: m.text == "🛍️ خرید سرویس")
def buy(m):
    bot.send_message(m.chat.id, "❌ فعلاً بسته است")

# ───── SUPPORT ─────
@bot.message_handler(func=lambda m: m.text == "👤 پشتیبانی")
def support(m):
    bot.send_message(m.chat.id, "📩 @SARAV2RAY")

print("Bot running...")
bot.infinity_polling()
