import asyncio
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, PROJECT_NAME

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔎 Найти бесплатное"],
        ["📦 Мои находки"],
        ["ℹ️ О проекте"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"Привет! 👋\n\n"
        f"Ты в {PROJECT_NAME}.\n"
        f"Ищу бесплатные и выгодные предложения.",
        reply_markup=reply_markup
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{PROJECT_NAME}\n"
        f"Версия 0.3\n\n"
        f"Проект поиска бесплатных возможностей и выгодных предложений."
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Функция находится в разработке. 🚀"
    )

async def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN не задан. Добавь токен Telegram в переменные окружения Render."
        )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(
        MessageHandler(
            filters.Regex("^ℹ️ О проекте$"),
            about
        )
    )
    app.add_handler(
        MessageHandler(
            filters.ALL,
            unknown
        )
    )

    print("BOT STARTED", flush=True)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
