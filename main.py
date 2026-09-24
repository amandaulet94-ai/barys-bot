import os
import time
import requests
from bs4 import BeautifulSoup
from telebot import TeleBot

TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_БОТА")
CHAT_ID = os.getenv("CHAT_ID", "ВАШ_CHAT_ID")

bot = TeleBot(TOKEN)

# Ссылка на общую страницу Барыс Арены со всеми матчами
TARGET_URL = "https://afisha.yandex.kz/astana/sport/places/barys-arena"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def check_barys_schedule():
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"Ошибка доступа к странице арены: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Ищем все блоки матчей/событий на странице
        # На Яндекс Афише карточки событий обычно содержат ссылки на конкретные матчи
        events = soup.find_all("a", href=lambda href: href and "/astana/sport/" in href)
        
        matches_found = []
        for event in events:
            text = event.get_text(strip=True)
            # Фильтруем только то, что связано с Барысом
            if "Барыс" in text or "Барсы" in text:
                if text not in matches_found:
                    matches_found.append(text)

        if matches_found:
            print(f"Найдено матчей на странице: {len(matches_found)}")
            # Можем сформировать сообщение со списком ближайших игр
            message = "🏒 Ближайшие матчи на Барыс Арене:\n\n" + "\n".join(matches_found[:5])
            
            # Раскомментируйте строку ниже, чтобы бот отправлял это в Telegram:
            # bot.send_message(CHAT_ID, message)
        else:
            print("Матчи Барыса не найдены на странице (возможно, изменилась верстка).")

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")

if __name__ == "__main__":
    print("Бот мониторинга расписания Барыса запущен...")
    
    while True:
        check_barys_schedule()
        time.sleep(100)  # Проверка каждые 15 минут
