import os
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv

# asyncio patch
nest_asyncio.apply()

# .env fayldan TOKEN ni olish
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Har bir viloyat uchun ma'lumotlar
VILOYATLAR = {
    "toshkent": {
        "matn": "Toshkent – O‘zbekiston poytaxti, zamonaviy va tarixiy joylar uyg‘unligi bilan mashhur.",
        "rasm": "images/toshkent.jpg"
    },
    "samarqand": {
        "matn": "Samarqand – Registon maydoni, Go‘ri Amir maqbarasi va qadimiy madaniy meros markazi.",
        "rasm": "images/samarqand.jpg"
    },
    "buxoro": {
        "matn": "Buxoro – Ark qal’asi, Minorai Kalon va tarixiy madrasa bilan mashhur.",
        "rasm": "images/buxoro.jpg"
    },
    "xiva": {
        "matn": "Xiva – Ichan-Qal’a majmuasi bilan YuNESKO merosi ro‘yxatiga kiritilgan shahar.",
        "rasm": "images/xorazm.jpg"
    },
    "farg'ona": {
        "matn": "Farg‘ona – tog‘lar, bog‘lar va hunarmandchilik markazi bilan tanilgan.",
        "rasm": "images/fargona.jpg"
    },
    "andijon": {
        "matn": "Andijon – Bobur vatani, tarixiy yodgorliklar va zamonaviy markazlar joylashgan.",
        "rasm": "images/andijon.jpg"
    },
    "namangan": {
        "matn": "Namangan – gullar shahri, go‘zal tabiat va madaniy joylari bilan mashhur.",
        "rasm": "images/namangan.jpg"
    },
    "shahrisabz": {
        "matn": "Qashqadaryo – Shahrisabz shahri, Amir Temur vatani sifatida tanilgan.",
        "rasm": "images/qashqadaryo.jpg"
    },
    "surxondaryo": {
        "matn": "Surxondaryo – Termiz, Fayoztepa, Jarkurgan minorasi kabi tarixiy joylarga ega.",
        "rasm": "images/surxondaryo.jpg"
    },
    "jizzax": {
        "matn": "Jizzax – Zomin milliy bog‘i, tog‘li dam olish joylari bilan tanilgan.",
        "rasm": "images/jizzax.jpg"
    },
    "navoiy": {
        "matn": "Navoiy – sanoat markazi, shuningdek Sarmishsoy darasi bilan mashhur.",
        "rasm": "images/navoiy.jpg"
    },
    "sirdaryo": {
        "matn": "Sirdaryo – go‘zal tabiatli, suv omborlari va dam olish maskanlari bor viloyat.",
        "rasm": "images/sirdaryo.jpg"
    }
}


# /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name.capitalize(), callback_data=name)] for name in VILOYATLAR.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🏙 Qaysi viloyatni tanlaysiz?", reply_markup=reply_markup)


# Tugma bosilganda ishlaydi
async def viloyat_tanlandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tanlangan = query.data
    viloyat = VILOYATLAR[tanlangan]

    if os.path.exists(viloyat["rasm"]):
        with open(viloyat["rasm"], "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption=f"📍 {tanlangan.capitalize()}\n\n{viloyat['matn']}"
            )
    else:
        await query.message.reply_text(viloyat["matn"])


# Botni ishga tushirish
async def main():
    print("🤖 Bot ishga tushmoqda...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(viloyat_tanlandi))

    print("✅ Bot muvaffaqiyatli ishga tushdi!")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
