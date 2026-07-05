import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN, PROJECT_NAME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Главное меню
menu = [
    ["🆓 Бесплатно", "📦 Уценка"],
    ["♻️ Б/У", "🏭 Опт"],
    ["💰 Заработать", "📊 Аналитика"],
    ["⭐ Проверка", "⚙️ Настройки"]
]

keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💎 {PROJECT_NAME}\n\nВыберите раздел:",
        reply_markup=keyboard
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🆓 Бесплатно":
        await update.message.reply_text("Поиск бесплатных товаров (пока заглушка)")
    elif text == "📦 Уценка":
        await update.message.reply_text("Поиск уценки (пока заглушка)")
    elif text == "♻️ Б/У":
        await update.message.reply_text("Раздел Б/У (будем расширять)")
    elif text == "🏭 Опт":
        await update.message.reply_text("Оптовые предложения (скоро)")
    elif text == "💰 Заработать":
        await update.message.reply_text("Раздел заработка (AI стратегия)")
    elif text == "📊 Аналитика":
        await update.message.reply_text("Аналитика цен (в разработке)")
    elif text == "⭐ Проверка":
        await update.message.reply_text("Проверка продавца (скоро)")
    elif text == "⚙️ Настройки":
        await update.message.reply_text("Настройки пользователя")
    else:
        await update.message.reply_text("Выберите пункт меню 👇")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
