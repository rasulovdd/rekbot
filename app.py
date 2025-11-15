from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import telebot
from dotenv import load_dotenv
import os
from time import sleep
import logging
from src import db
from src import logger
from src.text import *

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
rek_link= os.getenv('rek_link')

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
    
    markup = telebot.types.InlineKeyboardMarkup()
    
    # Создаем ссылку
    main_bot_button = telebot.types.InlineKeyboardButton(
        text="🚀 Перейти в основного бота", 
        url=rek_link
    )
    
    markup.add(main_bot_button)

    try:
        # Определяем статусы
        is_existing_user = db.is_user_exists(user_id)
        is_admin = int(user_id) == int(admins_id)
        
        # Обработка регистрации
        if is_existing_user:
            #Bot.send_message(user_id, "Привет 🤝\nРад видеть вас снова")
            Bot.send_message(
                    user_id, welcome_text, reply_markup=markup, parse_mode='HTML'
                )
        else:
            # Регистрируем нового пользователя
            user_status = 1 if is_admin else 0
            db.set_user_id(user_id, full_name, user_status)
            
            # Уведомляем админа о новом пользователе
            text = NEW_USER_TEMPLATE.format(
                user_id=user_id,
                full_name=full_name,
                bot_username=bot_username
            )
            Bot.send_message(admins_id, text, parse_mode="HTML")
            
            # Приветствие для нового пользователя
            if is_admin:
                Bot.send_message(user_id, "Привет 🤝\n✅ Теперь я буду уведомлять тебя о пользователях")
            else:
                Bot.send_message(
                    user_id, welcome_text, reply_markup=markup, parse_mode='HTML'
                )

        
        # Логирование
        if app_debug == "1":
            logger.info(f'[BOT] [UserID: {user_id}] Команда /start обработана')
            
    except Exception as e:
        logger.error(f'[BOT] [UserID: {user_id}] Ошибка в /start: {str(e)}')
        Bot.send_message(user_id, "❌ Произошла ошибка. Попробуйте позже.")

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
    import time
    
    # Ждем немного перед первым запуском
    time.sleep(5)
    
    # Уведомление о запуске
    try:
        Bot.send_message(admins_id, "REKBOT запустился")
    except Exception as e:
        logger.error(f'[BOT] Не удалось отправить уведомление о запуске: {e}')
    
    restart_count = 0
    
    while True:
        try:
            restart_count += 1
            logger.info(f'[BOT] Запуск polling (попытка #{restart_count})...')
            
            # Непрекращающаяся прослушка наших чатов
            Bot.polling(none_stop=True, interval=0, timeout=60)
            
        except Exception as my_bot_error:
            logger.error(f'[BOT] Ошибка polling: {my_bot_error}')
            
            # Отправляем уведомление только после нескольких перезапусков
            if restart_count > 1:
                try:
                    Bot.send_message(admins_id, f"🔄 Перезапуск бота (попытка #{restart_count})\nОшибка: {my_bot_error}")
                except:
                    pass
            
            logger.info('[BOT] Ждем 10 секунд перед перезапуском...')
            sleep(10)
    
    

    
