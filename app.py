from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import telebot
from dotenv import load_dotenv
import os
from time import sleep
import logging
from src import db
from src import logger

load_dotenv()

# Создаем папку, если её нет
if not os.path.exists('logs'):
    try:
        os.mkdir('logs')
    except Exception as my_error:
        print(f"Ошибка: {my_error}")

# Загружаем переменные из .env
api_tokken = os.getenv('api_tokken')
app_debug = os.getenv('debug_on')
my_host = os.getenv('my_host')
my_port = os.getenv('my_port')
bot_tokken = os.getenv('bot_tokken')
admins_id = os.getenv('admins_id')
bot_username = os.getenv('bot_username')

Bot = telebot.TeleBot(bot_tokken)

def notifications(number, status):
    """Уведомляем пользователей"""
    db.set_number(number)
    my_text = (
        f"{status} Новый пользователь\n<b>📱 {number}\n</b>"
    )
    all_users = db.get_all_users(1)
    for id in all_users:
        try:
            Bot.send_message(id, my_text, parse_mode="HTML")
            if app_debug == "1":
                logger.info(f'[BOT] [UserID: {id}] Сообщение отправлено')
        except Exception as my_error:
            print(f"Ошибка: {my_error}")
            if app_debug == "1":
                logger.error(f'[BOT] Ошибка: {my_error}')


# Настройка команд бота
Bot.delete_my_commands(scope=None, language_code=None)
Bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "🏠 Главное меню"),
        telebot.types.BotCommand("id", "👤 Телеграм ID"),
    ]
)

# Обработка команды /start
@Bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    if db.is_user_exists(user_id):
        all_users = db.get_all_users(1)
        Bot.send_message(user_id, "Привет 🤝\nРад видеть вас снова")
        if int(user_id) in all_users:
            Bot.send_message(user_id, "✅ Теперь я буду уведомлять тебя о пользователях")
        else:
            Bot.send_message(user_id, "❌ У тебя нету доступа.\nОбратись пожалуйста к @oka_admin_777")
            Bot.send_message(user_id, f"Твой ID: {user_id}")
    else:
        if int(user_id) == int(admins_id):
            db.set_user_id(user_id, full_name, 1)
        else:
            db.set_user_id(user_id, full_name, 0)

        all_users = db.get_all_users(1)
        if int(user_id) in all_users:
            Bot.send_message(user_id, "Привет 🤝\n✅ Теперь я буду уведомлять тебя о пользователях")
        else:
            Bot.send_message(user_id, "Привет 🤝\n❌ У тебя нету доступа.\nОбратись пожалуйста к @oka_admin_777")
            Bot.send_message(user_id, f"Твой ID: {user_id}")
            NEW_USER_TEMPLATE = (
                "🆕 <b>Новый пользователь</b>/n"
                f"👤 <b>ID:</b> <code>{user_id}</code>/n"
                f"{full_name}/n"
                f"🕐 <b>Время:</b>/n"
                f'🔍 <a href="https://t.me/{bot_username}?start=user_{user_id}'>Открыть в боте</a>'
            )
            Bot.send_message(admins_id, NEW_USER_TEMPLATE, parse_mode="HTML")


    if app_debug == "1":
        logger.info(f'[BOT] [UserID: {user_id}] Сообщение отправлено')

# Обработка команды /id
@Bot.message_handler(commands=['id'])
def send_id(message):
    if message.chat.type != 'private':
        Bot.send_message(message.chat.id, f"ID чата: {message.chat.id}")
    else:
        Bot.send_message(message.from_user.id, f"Ваш ID: {message.from_user.id}")

# Обработка команды /admin
@Bot.message_handler(commands=['admin'])
def command_admin(message):
    text = message.text
    user_id = message.from_user.id

    if int(user_id) == int(admins_id):
        try:
            manager_id = text.split(" ")[1]
        except:
            Bot.send_message(user_id, f"❌ Такая команда не поддерживается!")
            return

        db.set_admin(manager_id, 1)
        Bot.send_message(user_id, f"✅ UserID: {manager_id} Права админа, выданы")
        Bot.send_message(manager_id, "✅ Доступ получен!\nТеперь я буду уведомлять тебя о пользователях")
        if app_debug == "1":
            logger.info(f'[BOT] [UserID: {user_id}] Добавил менеджера {manager_id}')
    else:
        Bot.send_message(user_id, "❌ У Вас нет прав администратора")
        if app_debug == "1":
            logger.info(f'[BOT] [UserID: {user_id}] не имеет права админ')

# Запуск Бота
if __name__ == '__main__':
    while True:
        try:
            #отправляем уведомеление в чат админу
            Bot.send_message(2964812, "REKBOT запустился") 
            #Непрекращающаяся прослушка наших чатов
            Bot.polling(none_stop=True, interval=0,  timeout=60) 
        except Exception as my_bot_error:
            Bot.send_message(admins_id, f"Ошибка: {my_bot_error}") # отправляем сообщение админу
            logger.info(f'[BOT] startup, Ждем 10 секунд ........')
            sleep(10) #ждем 10 сек
            logger.info(f'[BOT] упал отжался и встал')
            # отправляем сообщение админу
            Bot.send_message(admins_id, "Bot упал отжался и встал") # отправляем сообщение админу
    
    

    
