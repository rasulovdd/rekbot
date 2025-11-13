import requests
import json
from mysql.connector import MySQLConnection, Error
from dotenv import load_dotenv
import os

load_dotenv()

def read_db_config():
    """Читаем настройки БД из .env"""
    return {
        "host": os.getenv('host'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "database": os.getenv('database')
    }

def send_message(bot_token, chat_id, my_text):
    """Отправляем сообщение через Telegram Bot API"""
    session = requests.Session()
    params = {
        "chat_id": chat_id,
        "text": my_text
    }
    
    response = session.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        params=params
    )
    
    data = json.loads(response.text)
    return "ok" if data["ok"] else data["description"]

def set_status(user_id, status):
    """Устанавливаем статус пользователя в БД"""
    query = "UPDATE main SET status = %s WHERE user_id = %s"
    
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, (status, user_id))
        conn.commit()
    except Error as error:
        print(f"Ошибка БД: {error}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_users():
    """Получаем список всех user_id из БД"""
    all_users = []
    
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM main")
        rows = cursor.fetchall()
        
        all_users = [row[0] for row in rows] if rows else [0]
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return all_users
