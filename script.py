import datetime
import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ============================================================
#  CONFIG — edit everything in this section freely
# ============================================================

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Timezone offset from UTC — Algeria is UTC+1
TIMEZONE = datetime.timezone(datetime.timedelta(hours=1))

# ------ Fixed times ----------------------------------------

MORNING_DHIKR_HOUR   = 7    # 7:00 AM
MORNING_DHIKR_MINUTE = 0

EVENING_DHIKR_HOUR   = 18   # 6:00 PM
EVENING_DHIKR_MINUTE = 0

# ------ Interval -------------------------------------------

TASBIH_INTERVAL_HOURS = 2   # every 2 hours

# ------ Messages -------------------------------------------

WELCOME_MESSAGE = (
    "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ 🌿\n\n"
    "أنا بوت بعبق للأذكار، سأرسل لك:\n\n"
    "🌅 أذكار الصباح كل يوم الساعة 7:00 صباحاً\n"
    "🌆 أذكار المساء كل يوم الساعة 6:00 مساءً\n"
    "🤲 تذكير بالتسبيح والحوقلة كل ساعتين\n\n"
    "نسأل الله أن يجعلها في ميزان حسناتك 🤍"
)

WELCOME_HAWQALA = (
    "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ ✨\n\n"
    "قال عنها النبي ﷺ: «كنز من كنوز الجنة»"
)

MORNING_DHIKR_MESSAGE = (
    "🌅 أذكار الصباح\n\n"
    "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ.\n\n"
    "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ هَذَا الْيَوْمِ وَخَيْرَ مَا فِيهِ.\n\n"
    "حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ. (×7)\n\n"
    "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ. (×3)"
)

EVENING_DHIKR_MESSAGE = (
    "🌆 أذكار المساء\n\n"
    "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ.\n\n"
    "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ هَذِهِ اللَّيْلَةِ وَخَيْرَ مَا فِيهَا.\n\n"
    "حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ. (×7)\n\n"
    "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ. (×3)"
)

TASBIH_MESSAGE = (
    "🤲 تذكير بالتسبيح والحوقلة\n\n"
    "سُبْحَانَ اللَّهِ (×33)\n"
    "الْحَمْدُ لِلَّهِ (×33)\n"
    "اللَّهُ أَكْبَرُ (×33)\n\n"
    "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ ✨"
)

# ============================================================
#  SUBSCRIBERS — no need to edit below this line
# ============================================================

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(subscribers), f)

subscribers = load_subscribers()

# ============================================================
#  BOT LOGIC — no need to edit below this line
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        save_subscribers(subscribers)
    await update.message.reply_text(WELCOME_MESSAGE)
    await update.message.reply_text(WELCOME_HAWQALA)

async def broadcast(context, text):
    for chat_id in list(subscribers):
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            # user blocked the bot or deleted the chat — remove them
            subscribers.discard(chat_id)
            save_subscribers(subscribers)

async def send_morning_dhikr(context):
    await broadcast(context, MORNING_DHIKR_MESSAGE)

async def send_evening_dhikr(context):
    await broadcast(context, EVENING_DHIKR_MESSAGE)

async def send_tasbih(context):
    await broadcast(context, TASBIH_MESSAGE)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    jq = app.job_queue

    jq.run_daily(
        send_morning_dhikr,
        time=datetime.time(
            hour=MORNING_DHIKR_HOUR,
            minute=MORNING_DHIKR_MINUTE,
            tzinfo=TIMEZONE
        ),
        name="morning_dhikr"
    )

    jq.run_daily(
        send_evening_dhikr,
        time=datetime.time(
            hour=EVENING_DHIKR_HOUR,
            minute=EVENING_DHIKR_MINUTE,
            tzinfo=TIMEZONE
        ),
        name="evening_dhikr"
    )

    jq.run_repeating(
        send_tasbih,
        interval=datetime.timedelta(hours=TASBIH_INTERVAL_HOURS),
        first=datetime.timedelta(seconds=10),
        name="tasbih_reminder"
    )

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()