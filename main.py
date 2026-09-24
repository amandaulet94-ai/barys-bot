import os
import time
import requests
import telebot
from bs4 import BeautifulSoup
import threading

TOKEN = "8748773086:AAEN-SdmM0--Uc0yCthgGxOFckgdCpWks6Y"
ADMIN_CHAT_ID = "1014105979"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    bot.reply_to(
        message, 
        f"Привет! Бот-монитор билетов ХК «Барыс» успешно запущен и работает! 🏒\nВаш Chat ID: `{chat_id}`",
        parse_mode="Markdown"
    )

def check_tickets():
    """
    Функция для проверки билетов.
    Здесь бот периодически обращается к сайту.
    """
    try:
        url = "https://hcbarys.kz/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        # Делаем запрос к сайту (таймаут 10 секунд)
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Здесь в будущем мы добавим проверку HTML-кода (например, поиск текста "Купить" или цен)
            print("Сайт «Барыса» доступен, проверка прошла успешно.")
            
            # Пример уведомления (можно закомментировать, чтобы не спамило каждые 2 минуты):
            # bot.send_message(ADMIN_CHAT_ID, "🟢 Бот проверил сайт: всё работает, ждем билеты!")
        else:
            print(f"Сайт ответил с кодом: {response.status_code}")
            
    except Exception as e:
        print(f"Ошибка при запросе к сайту: {e}")

def background_checker():
    """Бесконечный фоновый цикл проверки"""
    while True:
        check_tickets()
        # Интервал проверки в секундах (сейчас стоит 120 секунд / 2 минуты)
        time.sleep(120)

if __name__ == '__main__':
    print("Бот запускается...")
    
    checker_thread = threading.Thread(target=background_checker)
    checker_thread.daemon = True
    checker_thread.start()
    
    bot.infinity_polling()