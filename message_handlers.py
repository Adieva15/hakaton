from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from aisett import generate_resp
from confyg import *
import logging

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    '''функция старт'''
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

    context.user_data['history']=[]
    context.user_data['user_name']=update.effective_user.first_name


async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    '''функция помощь'''
    help_text = """Напишите мне и ИИ ответит! Как пользоваться:
        1. перессказ
        2. анализ персонажей
        3. помощь с рецензией
        """
    await update.message.reply_text(help_text)

async def about(update:Update, context:ContextTypes.DEFAULT_TYPE):
    '''функция о боте'''
    about_text = """Бот - литературный помощник с искусственным интелектом"""
    await update.message.reply_text(about_text)


async def reset_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    '''функция сброс диалога'''
    # очищаем историю разговооров
    if 'history' in context.user_data:
        context.user_data['history'] = []
    await update.message.reply_text('диалог сброшен')


async def handlemes(update: Update, context:ContextTypes.DEFAULT_TYPE):
    '''обработка текстовых сообщений'''
    user_text = update.message.text
    user_name = update.effective_user.first_name

    logger.info(f'сообщение от {user_name}: {user_text}')

    # if contains_bad_words(user_text):
    #     await update.message.reply_text("прошу избегать нецензурных выражений")
    #     return
    #
    # if len(user_text)>100:
    #     await update.message.reply_text("Сообщение слишком длинное, пожалуйста сократите до 100 символов: ")
    #     return

    await update.message.chat.send_action(action='typing')

    try:
        # prompt = context_prompt(user_text, context)
        if user_text.lower() in ['привет', 'здравствуй', 'добрый день', 'добрый вечер', 'доброе утро']:
            bot_response = f'Привет, {user_name}! Чем могу помочь?'
        elif user_text.lower() in ['как дела', 'как ты', 'как твое здоровье']:
            bot_response = "У меня отлично! Спасибо, что спросили!"
        else:
            bot_response = await generate_resp(user_text)

        # update_conversh(context, user_text, bot_response)

        await update.message.reply_text(bot_response)
        logger.info('Ответ успешно отправлен пользователю')
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
