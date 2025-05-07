import time
import os

from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constatns import URL, CHATIK
from parser_utils import parse_messages

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


def driver_init():
    """Инициализация драйвера."""
    user_agent = UserAgent().random

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    return driver


def login_hh_ru(driver: webdriver.Chrome):
    """Логин в hh.ru."""
    url: str = URL
    chatik: str = CHATIK

    try:
        driver.get(url)
        time.sleep(3)

        come_in_button = driver.find_element(
            By.XPATH, '//button[.//span[contains(text(), "Войти")]]'
        )
        if come_in_button:
            come_in_button.click()

        time.sleep(3)
        phone_number_field = driver.find_element(
            By.XPATH, '//input[@inputmode="tel"]'
        )
        phone_number_field.send_keys(PHONE_NUMBER)

        try:
            continue_button = driver.find_element(
                By.XPATH, '//button[@data-qa="expand-login-by-password"]'
            )
            continue_button.click()
        except BaseException:
            pass

        time.sleep(2)
        password_field = driver.find_element(
            By.XPATH, '//input[@name="password"]'
        )
        password_field.send_keys(PASSWORD)

        try:
            login_button = driver.find_element(
                By.XPATH, '//button[@data-qa="submit-button"]'
            )
            login_button.click()
        except BaseException:
            pass

        time.sleep(3)

        driver.get(chatik)
        scrolling_chats(driver)

    except BaseException as er:
        print(f'Возникла ошибка в {__name__}: {er}')


def scrolling_chats(driver: webdriver.Chrome):
    """Скроллит траницу с чатами вниз."""
    chats_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "___chats")]'))
    )
    prev_chats = driver.find_elements(
        By.XPATH, '//a[contains(@data-qa, "chatik-open-chat-")]'
    )
    prev_count = len(prev_chats)
    attempts = 0
    max_attempts = 100

    while attempts < max_attempts:
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight', chats_container
        )
        time.sleep(2)

        current_chats = driver.find_elements(
            By.XPATH, '//a[contains(@data-qa, "chatik-open-chat-")]'
        )
        current_count = len(current_chats)

        print(f'Попытка {attempts + 1}: было {prev_count}, стало {current_count} чатов')

        if current_count == prev_count:
            break

        prev_count = current_count
        attempts += 1

    print(f'Всего загружено чатов: {prev_count}')
    time.sleep(5)

    html = driver.page_source
    with open('chats.html', 'w') as file:
        file.write(html)


def scroll_chat_up_and_get_message(driver: webdriver.Chrome) -> str:
    """Скроллит чат вверх и возвращает сообщения."""
    chat_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "___content")]'))
    )

    driver.execute_script(
        'arguments[0].scrollTop = 0', chat_container
    )
    time.sleep(2)

    current_messages = driver.find_elements(
        By.XPATH, '//div[contains(@data-qa, "chatik-chat-message-")]'
    )
    current_count = len(current_messages)

    print(f'+ {current_count} сообщений')

    html = driver.page_source
    messages_data = parse_messages(html)
    return messages_data
    # with open('chats.txt', 'a') as file:
    #     file.write(messages)


def get_message_from_chats(chats_data: list, driver: webdriver.Chrome):
    """Получает сообщения из чатов."""
    all_messages = []
    try:
        for chat_data in chats_data:
            chat_url = chat_data[0]['id']
            driver.get(f'https://chatik.hh.ru/chat/{chat_url}')
            print(f'Перешли в чат {chat_url}')
            time.sleep(2)

            messages = scroll_chat_up_and_get_message(driver)
            all_messages.append(messages)
            time.sleep(2)

    except BaseException as er:
        print(f'Возникла ошибка в {__name__}: {er}')
    finally:
        with open('messages.txt', 'w') as file:
            for message in all_messages:
                file.write(str(message))
                file.write("\n")
        driver.quit()
