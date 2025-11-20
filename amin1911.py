import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI
import asyncio
import random

ai_token='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'
bot_token = '8429360617:AAEq7tbtVLbQ2P7Bx92vKW8-4gcnIW-mBGs'

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger(__name__)

async def generate_resp(prompt, maxretries=5):
    """генерация с экспоненциальной задержкой при ошибках"""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ai_token,
    )

    for attempt in range(maxretries):
        try:
            completion = client.chat.completions.create(
                model="qwen/qwen3-4b:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            if attempt == maxretries -1:
                logger.error(f'все попытки завершились {e}')
                return "ИЗвините, сервис временно не доступен, попробуйте позже."

            base_del= 2**attempt
            jitter = random.uniform(0.1, 0.5)
            delay = base_del + jitter

            logger.warning(f'Попытка {attempt+1} {e} не удалась. Повтор через {delay:.1f}')

            await asyncio.sleep(delay)
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    welcome_text = """      
    Привет! Я бот с ИИ
    Мои команды:
     /start - начать работу
     /help - помощь
     /about - о боте
     /reset - сбросить диалог
     
     Напишите мне что-нибудь!
     """
    await update.message.reply_text(welcome_text)

async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    help_text = """Кнапишите мне и ИИ ответит! Как пользоваться:
    1. перессказ"""
    await update.message.reply_text(help_text)

async def about(update:Update, context:ContextTypes.DEFAULT_TYPE):
    about_text = """Бот - литературный помощник с искусственным интелектом"""
    await update.message.reply_text(about_text)


async def reset_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # очищаем историю разговооров
    if 'history' in context.user_data:
        context.user_data['history'] = []
    await update.message.reply_text('диалог сброшен')

async def handlemes(update: Update, context:ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.chat.send_action(action='typing')
    try:
        bot_response = await generate_resp(user_text)

        await update.message.reply_text(bot_response)

    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        await update.message.reply_text("произошла непредвиденная ошибка.")



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

