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
        model="x-ai/grok-4.1-fast:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    extra_body={"reasoning": {"enabled": True}}
    )
    completion = completion.choices[0].message.content
    messages = [
        {"role": "user", "content": prompt},
        {
            "role": "assistant",
            "content": completion.content,
            "reasoning_details": completion.reasoning_details  # Pass back unmodified
        },
        {"role": "user", "content": prompt}
    ]

    # Second API call - model continues reasoning from where it left off
    response2 = client.chat.completions.create(
        model="x-ai/grok-4.1-fast:free",
        messages=messages,
        extra_body={"reasoning": {"enabled": True}}
    )
    return completion

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

