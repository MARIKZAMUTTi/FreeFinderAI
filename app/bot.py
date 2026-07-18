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
    level=logging.INFO,
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    keyboard = [
        ["🔎 Найти бесплатное"],
        ["📦 Мои находки"],
        ["ℹ️ О проекте"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

    await update.message.reply_text(
        f"Привет! 👋\n\n"
        f"Ты в {PROJECT_NAME}.\n"
        f"Ищу бесплатные и выгодные предложения.",
        reply_markup=reply_markup,
    )


async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        f"{PROJECT_NAME}\n"
        f"Версия 0.3\n\n"
        f"Проект поиска бесплатных возможностей "
        f"и выгодных предложений."
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = update.message.text

    if text == "🔎 Найти бесплатное":
        await update.message.reply_text(
            "🔎 Поиск бесплатных предложений скоро будет доступен."
        )

    elif text == "📦 Мои находки":
        await update.message.reply_text(
            "📦 Здесь будут сохранённые находки."
        )

    elif text == "ℹ️ О проекте":
        await about(update, context)

    else:
        await update.message.reply_text(
            "Выберите раздел из меню 👇"
        )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN не задан. "
            "Добавь токен Telegram в переменные окружения Render."
        )

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("about", about)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
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
