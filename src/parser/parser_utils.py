import re

import bs4
from bs4 import BeautifulSoup

from src.logger_config import logging_decorator


@logging_decorator
def parse_chats_url() -> list:
    """Парсит чаты."""
    with open("chats.html", "r") as f:
        file = f.read()
    soup = BeautifulSoup(file, 'lxml')
    try:
        chats = soup.find_all('a', id=re.compile('chat-cell-'))
        status = soup.find_all('div', class_=re.compile('___last-message-color'))
        vacancy = soup.find_all('div', class_=re.compile('___title'))
        company = soup.find_all('div', class_=re.compile('___subtitle'))
        chats_data = []
        for ind, chat in enumerate(chats):
            chat_id = {
                'id': chat['id'].replace('chat-cell-', '')
            }
            chat_vacancy = {'vacancy': vacancy[ind].text}
            chat_company = {'company': company[ind].text}
            chat_status = {'status': check_chat_status(status[ind])}

            chats_data.append((
                chat_id,
                chat_vacancy,
                chat_company,
                chat_status
            ))

        return chats_data
    except BaseException as er:
        print(f'Возникла ошибка в {__name__}: {er}')
        return None


@logging_decorator
def check_chat_status(status: bs4.element.Tag):
    """Проверяет статус чата."""
    status_class = status['class'][1]
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


@logging_decorator
def parse_messages(html: str):
    """Парсит сообщения."""
    soup = BeautifulSoup(html, 'lxml')
    messages = []
    seen_ids = set()

    name_company = soup.find(
        'div', attrs={'data-qa': re.compile('participant')}
    )

    message_elements = soup.find_all(
        'div', attrs={'data-qa': re.compile('^chatik-chat-message-')}
    )

    for message in message_elements:
        try:
            message_id = message.get('data-qa', '').replace('chatik-chat-message-', '')
            if message_id.endswith('text'):
                continue
            if not message_id or message_id in seen_ids:
                continue

            seen_ids.add(message_id)
            author_elem = message.find(
                'span', attrs={'data-qa': 'chat-bubble-author-name'}
            )
            author = author_elem.text.strip() if author_elem else 'user'

            title_elem = message.find('div', attrs={'data-qa': 'chat-bubble-title'})
            title = title_elem.text.strip() if title_elem else None

            text = message.find('span', attrs={'data-qa': 'chat-bubble-text'})
            text = text.text.strip() if text else None

            time_elem = message.find(
                'span', attrs={'data-qa': 'chat-buble-display-time'}
            )
            time = time_elem.text.strip() if time_elem else None

            date_elem = message.find_previous(
                'div', class_=re.compile('___date-change')
            )
            date = (
                date_elem.find('div', class_=re.compile('___chat-date')).text.strip()
                if date_elem
                else None
            )

            bubble = message.find('div', class_=re.compile('___chat-bubble_incoming'))
            message_type = (
                'incoming'
                if bubble
                else 'outgoing'
            )

            messages.append(
                {'id': message_id,
                 'name_company': name_company.text.strip() if name_company else None,
                 'author': author,
                 'title': title,
                 'text': text,
                 'time': time,
                 'date': date,
                 'type': message_type,
                 }
            )

        except Exception as e:
            print(f'Ошибка при парсинге сообщения: {e}')
            continue

    return messages
