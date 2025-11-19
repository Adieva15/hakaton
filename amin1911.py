import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

bot_token = '8429360617:AAEq7tbtVLbQ2P7Bx92vKW8-4gcnIW-mBGs'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLonger(__name__)


async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    welcome_text = """
     /start
     /help
     /about
     /reset
     """
    await update.message.reply_text(welcome_text)

async def help(update:Update, context:ContextTypes.DEFAULT_TYPE):
    help_text = """Как пользоваться:
    1. перессказ"""
    await update.message.reply_text(help_text)

async def about(update:Update, context:ContextTypes.DEFAULT_TYPE):
    about_text = """о боте
    литературный помощник с искусственным интелектом"""
    await update.message.reply_text(about_text)


async def reset_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    pass

async def handlemes(update: Update, context:ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    bot_response = """...(user_text)"""

    await update.message.reply_text(bot_response)


def main():
    try:
        logger.info("Запуская бота...")
        application = Application.builder().token(bot_token).build()

        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('help', help))
        application.add_handler(CommandHandler('about', about))
        application.add_handler(CommandHandler('reset', reset_command))

        logger.info("бот запущен!")
        application.run_polling()

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        print("где-то пошла ошибка")

if __name__=="__main__":
    main()