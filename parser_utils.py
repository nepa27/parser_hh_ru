import json
import re

from bs4 import BeautifulSoup

def parse_chats_url():
    """Парсит чаты."""
    with open("chats.html", "r") as f:
        file = f.read()
    soup = BeautifulSoup(file, 'lxml')
    try:
        chats = soup.find_all('a', id=re.compile('chat-cell-'))
        status = soup.find_all('div',class_=re.compile('___last-message-color'))
        vacancy = soup.find_all('div',class_=re.compile('___title'))
        company = soup.find_all('div',class_=re.compile('___subtitle'))
        json_data = []
        for ind, chat in enumerate(chats):
            chat_id = {
                'id': chat['id']
            }
            chat_url = {
                'url': chat['href']
            }
            chat_vacancy = {"vacancy": vacancy[ind].text}
            chat_company = {"status": company[ind].text}
            chat_status = {"company": check_chat_status(status[ind])}

            json_data.append((
                chat_id,
                chat_vacancy,
                chat_company,
                chat_url,
                chat_status
            ))

        json_data = json.dumps(json_data, ensure_ascii=False, indent=4)
        return json_data
    except BaseException as er:
        print(f'Возникла ошибка: {er}')
        return None


def check_chat_status(status):
    """Проверяет статус чата."""

    status_class = status["class"][1]
    status_text = status.text
    if 'color_red' in status_class:
        return 'refusal'
    elif 'color_green' in status_class and 'Приглашение' in status_text:
        return 'invitation'
    elif 'color_green' in status_class and 'Отклик' in status_text:
        return 'viewed'
    elif 'color_secondary' in status_class:
        return 'viewed'
    else:
        return None
