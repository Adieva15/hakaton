import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

ai_token='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'

bot_token = '8429360617:AAEq7tbtVLbQ2P7Bx92vKW8-4gcnIW-mBGs'

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger(__name__)

async def generate_resp(prompt):

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ai_token,
    )

    completion = client.chat.completions.create(
        extra_body={},
        model="qwen/qwen3-4b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    welcome_text = """      
    Привет! я
     /start - начать работу
     /help - помощь
     /about - о боте
     /reset - сбросить диалог
     """
    await update.message.reply_text(welcome_text)

async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    help_text = """Как пользоваться:
    1. перессказ"""
    await update.message.reply_text(help_text)

async def about(update:Update, context:ContextTypes.DEFAULT_TYPE):
    about_text = """о боте
    литературный помощник с искусственным интелектом"""
    await update.message.reply_text(about_text)


async def reset_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # очищаем историю разговооров
    if 'history' in context.user_data:
        context.user_data['history'] = []
    await update.message.reply_text('диалог сброшен')

async def handlemes(update: Update, context:ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text
    bot_response = """...(user_text)"""

    await update.message.reply_text(bot_response)
    response = await generate_resp(user_text)
    await update.message.answer(f'{response}')


def generation_litresponse(user_text):
    textlower = user_text.lower()
    if any(word in textlower for word in ['привет','здравствуйте','hello']):
        return 'Привет! я Литературный помощник, чем могу помочь?'

    elif any(word in textlower for word in ['пересказ', "перескажи", "кратко", "краткий"]):
        return "Я готов сделать краткий перессказ произведения, пришлите название произведения или книги."
    else:
        return f"Вы написали: {user_text} \n\n Спасибо за интересный запрос, но, пожалуйста, используйте: \n - 'Перескажи [название]'\n -  ... "


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
        logger.error(f"Ошибка: {e}")
        print("где-то пошла ошибка")


if __name__=="__main__":
    main()

