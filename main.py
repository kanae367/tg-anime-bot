from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Application, ContextTypes, ConversationHandler, MessageHandler, filters
from AnilistPython import Anilist
import os

TG_BOT_KEY = os.getenv('TG_BOT_KEY')
ANIME_ARR = ["Название", "Название(Eng)", "Выход первой серии", "Выход последней серии", "Обложка", "Баннер",
             "Формат выпуска", "Статус", "Количество серий", "Сезон", "Описание", "Средняя оценка", "Жанры",
             "Дата выхода следующего эпизода"]

MANGA_ARR = ['Название', 'Название(Eng)', 'Дата выхода первой главы', 'Дата выхода последней главы', 'Обложка',
             'Баннер', \
             'Формат выпуска', 'Статус выхода', 'Главы', 'Томы', 'Описание', 'Средняя оценка', 'Средняя оценка', \
             'Жанры', 'Другие названия']

CHARACTER_ARR = ["Имя", "Фамилия", "Имя на японском", "Описание", "Картинка"]

CHOOSE, ANIME, MANGA, CHARACTER, QUERY = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [["Аниме", "Мангу", "Персонажа"], ["Отмена"]]
    await update.message.reply_text(
        "Привет, я помогу тебе найти информацию об аниме, персонаже или манге. Что ты хочешь найти?",

        reply_markup=ReplyKeyboardMarkup(

            keyboard, one_time_keyboard=True, input_field_placeholder="Что ты хочешь найти?"

        )
    )
    return CHOOSE


async def select_variant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == 'Отмена':
        return ConversationHandler.END

    await update.message.reply_text(
        "Ты выбрал " + choice.lower() + "\nВведи имя/название",
        reply_markup=ReplyKeyboardRemove()
    )

    if choice == "Аниме":
        return ANIME
    elif choice == "Мангу":
        return MANGA
    elif choice == "Персонажа":
        return CHARACTER
    elif choice == "Отмена":
        return ConversationHandler.END

    return ConversationHandler.END


async def get_manga(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    result = anilist.get_manga(text)
    formatted_result = ''
    counter = 0
    for key, value in result.items():
        if key == 'desc' and len(str(value)) > 3000:
            formatted_result += str(MANGA_ARR[counter]) + ': ' + str(value).replace('<br>', '')[0:3000] + '...\n\n'
        else:
            formatted_result += str(MANGA_ARR[counter]) + ': ' + str(value).replace('<br>', '') + '\n\n'
        counter += 1
    await update.message.reply_text(
        "Ваш результат:\n\n" + str(formatted_result)
    )
    return ConversationHandler.END


async def get_anime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    result = anilist.get_anime(text)
    formatted_result = ''
    counter = 0
    for key, value in result.items():
        if key == 'desc' and len(str(value)) > 3000:
            formatted_result += str(ANIME_ARR[counter]) + ': ' + str(value).replace('<br>', '')[0:3000] + '...\n\n'
        else:
            formatted_result += str(ANIME_ARR[counter]) + ': ' + str(value).replace('<br>', '') + '\n\n'
        counter += 1
    await update.message.reply_text(
        "Ваш результат: \n\n" + str(formatted_result)
    )
    return ConversationHandler.END


async def get_character(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    result = anilist.get_character(text)
    formatted_result = ''
    counter = 0
    for key, value in result.items():
        if key == 'desc' and len(str(value)) > 3000:
            formatted_result += str(CHARACTER_ARR[counter]) + ': ' + str(value).replace('<br>', '')[0:3000] + '...\n\n'
        else:
            formatted_result += str(CHARACTER_ARR[counter]) + ': ' + str(value).replace('<br>', '') + '\n\n'
        counter += 1
    await update.message.reply_text(
        "Ваш результат:\n\n " + str(formatted_result)
    )
    return ConversationHandler.END


async def get_from_database(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ошибка: " + str(context.error)
    )


application = Application.builder().token(TG_BOT_KEY).build()
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_variant)],
        MANGA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_manga)],
        ANIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_anime)],
        CHARACTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_character)],
        QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_from_database)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)
application.add_handler(conv_handler)
application.add_error_handler(error_handler)
anilist = Anilist()
application.run_polling()
