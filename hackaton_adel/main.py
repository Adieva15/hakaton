from message_handlers import *
from confyg import *

async def error_handler(update, context):
    """Глобальный обработчик ошибок"""
    logger.error(f"Ошибка в боте: {context.error}", exc_info=True)

def main():
    try:
        logger.info("Запуск бота...")
        application = Application.builder().token(bot_token).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('help', help_command))
        application.add_handler(CommandHandler('about', about))
        application.add_handler(CommandHandler('reset', reset_command))

        # обработка сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlemes))

        logger.info("бот запущен!")
        application.run_polling()

    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        print("где-то пошла ошибка")


if __name__=="__main__":
    main()
