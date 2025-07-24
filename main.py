import telebot
from telebot import types
from logic import GigaChatAPI
from config import CLIENT_SECRET, TOKEN, MODEL

api = GigaChatAPI(CLIENT_SECRET, MODEL)
bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
search = types.KeyboardButton("🔎 Поиск")
help_btn = types.KeyboardButton("🆘 Помощь")
info_btn = types.KeyboardButton("📄 Инфо")
markup.add(search, help_btn, info_btn)

waiting = set()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎬 Привет! Я - бот, эксперт по кино и сериалам. \n"
        "Нажми '🔎 Поиск', чтобы найти фильмы или сериалы по описанию! 🤩\n"
        "Или выбери '🆘 Помощь' для инструкций. \n"
        "Также, ты можешь нажать на '📄 Инфо', чтобы узнать больше информации о боте!🤖",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == '📄 Инфо')
def info(message):
    bot.send_message(
        message.chat.id,
        '🤖 FilmAI - Новейший бот-эксперт в сфере Киноиндустрии! \n\n'
        ' -----------------Техническая Информация----------------- \n'
        ' - Версия бота: 0.3 \n'
        ' - Гит-репозиторий: https://github.com/DimaV11/FilmAI/ \n'
        ' - Нейросеть: GigaChat 2\n'
        ' - Авторы: @sirdezzan , @d42521 \n'
        ' ------------------------------------------------------------------------'
        )

@bot.message_handler(func=lambda m: m.text == '🔎 Поиск')
def start_search(message):
    waiting.add(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Отправь описание фильма или сериала (например, жанр, сюжет или настроение).",
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == '🆘 Помощь')
def help_message(message):
    bot.send_message(
        message.chat.id,
        "🆘 Я помогу найти фильмы и сериалы! \n"
        "1. Нажми *🔎 Поиск* и опиши, что хочешь посмотреть (например, 'фантастика про космос' или 'романтическая комедия'). \n"
        "2. Я найду 3-5 фильмов или сериалов с описанием и рейтингом. \n"
        "3. Если что-то не работает, напиши *🔎 Поиск* еще раз!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.chat.id in waiting:
        bot.send_chat_action(message.chat.id, 'typing')
        prompt = message.text
        waiting.remove(message.chat.id)
        try:
            films = api.get_films(prompt)
            if len(films) > 4096:
                films = films[:4090] + "..."
            bot.send_message(
                message.chat.id,
                films,
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            bot.send_message(
                message.chat.id,
                "😔 Произошла ошибка при запросе к API. Попробуй еще раз через *🔎 Поиск*!",
                reply_markup=markup,
                parse_mode="Markdown"
            )
            print(f"Ошибка: {e}")
    else:
        bot.send_message(
            message.chat.id,
            "Нажми *🔎 Поиск*, чтобы начать поиск фильмов!",
            reply_markup=markup,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
