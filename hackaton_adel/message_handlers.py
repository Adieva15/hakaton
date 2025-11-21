from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from aisett import generate_resp
from filtrr import *
import logging

logging.basicConfig( format='%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
    '''функция старт'''
    welcome_text = """      
        Привет! Я бот с ИИ Литературный помощник!
        Я умею делать краткие пересказы произведений и отвечать на ваши вопросы по литературе.
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
        1. Можешь попросить сделать перессказ
        2. Сделать анализ персонажей
        3. Помочь с рецензией
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


def update_conversh(context, user_text: str, bot_response: str):
    """Обновляет историю диалога"""
    if 'history' not in context.user_data:
        context.user_data['history'] = []

    # Добавляем новое сообщение в историю
    context.user_data['history'].append({"role": "user", "content": user_text})
    context.user_data['history'].append({"role": "assistant", "content": bot_response})

    # Ограничиваем размер истории (последние 6 сообщений)
    if len(context.user_data['history']) > 6:
        context.user_data['history'] = context.user_data['history'][-6:]


def context_prompt(user_text: str, context) -> str:
    """Строит промпт с учетом истории диалога"""
    if 'history' not in context.user_data or not context.user_data['history']:
        return user_text

    # Берем последние сообщения из истории
    recent_history = context.user_data['history'][-4:] if len(context.user_data['history']) > 4 else context.user_data[
        'history']

    prompt = "Предыдущий диалог:\n"
    for msg in recent_history:
        role = "Пользователь" if msg["role"] == "user" else "Ассистент"
        prompt += f"{role}: {msg['content']}\n"

    prompt += f"\nНовое сообщение пользователя: {user_text}\nОтвет ассистента:"
    return prompt


async def handlemes(update: Update, context:ContextTypes.DEFAULT_TYPE):
    '''обработка текстовых сообщений'''
    user_text = update.message.text
    user_name = update.effective_user.first_name

    logger.info(f'сообщение от {user_name}: {user_text}')

    if contains_bad_words(user_text):
        await update.message.reply_text("прошу избегать нецензурных выражений")
        return

    if len(user_text)>100:
        await update.message.reply_text("Сообщение слишком длинное, пожалуйста сократите до 100 символов: ")
        return

    await update.message.chat.send_action(action='typing')

    try:
        # Сначала пробуем получить статический ответ
        static_response = generation_litresponse(user_text)
        if static_response:
            await update.message.reply_text(static_response)
            update_conversh(context, user_text, static_response)
            return

        # Если статического ответа нет, используем AI с контекстом
        prompt = context_prompt(user_text, context)
        bot_response = await generate_resp([{"role": "user", "content": prompt}])

        update_conversh(context, user_text, bot_response)

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
        return None

