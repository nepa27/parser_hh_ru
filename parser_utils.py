import re

from bs4 import BeautifulSoup

def parse_chats_url():
    """Парсит ссылки на чаты."""
    with open("chats.html", "r") as f:
        file = f.read()
    response = parse_chats_url(file)
    soup = BeautifulSoup(response, 'lxml')
    try:
        chats = soup.find_all('a', id=re.compile('chat-cell-'))
        chat_urls = [chat['href'] for chat in chats]
        return chat_urls
    except BaseException as er:
        print(f'Возникла ошибка: {er}')
        return None
