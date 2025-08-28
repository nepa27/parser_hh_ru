from logging import Logger
import time
import os

from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser_utils import parse_messages
from src.parser.abstract import AbstractSelenim
from src.parser.config import ParserConfig

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


class SeleniumUtils(AbstractSelenim):
    """Класс реализующий автоматическую работу браузера."""

    def __init__(
        self,
        config: ParserConfig,
        logger: Logger
    ) -> None:
        """
        Инициализация системы автоматизации работы.

        :param config: конфиг
        :param driver: драйвер браузера
        :param logger: логгер для сообщений
        """
        self.config = config
        self.logger = logger

    def driver_init(self) -> None:
        """
        Инициализация драйвера.

        Определяем рандомный user_agent.
        Добавляем user_agent в аргументы для создания драйвера.
        Инициализируем драйвер

        :return driver: драйвер браузера
        """
        user_agent = UserAgent().random

        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(options=options)

    def auth_hh_ru(self):
        """
        Аутентификация в hh.ru.

        Переходим на страницу, указанную в self.config.url.
        Находим кнопку 'Войти' и нажимаем на неё.
        Вводим номер телефона, пароль, логгинимся в системе.
        Берем PHONE_NUMBER и PASSWORD из .env.
        """
        try:
            self.driver.get(self.config.url)
            time.sleep(self.config.time_sleep_between_requests)

            come_in_button = self.driver.find_element(
                By.XPATH, '//button[.//span[contains(text(), "Войти")]]'
            )
            if come_in_button:
                come_in_button.click()

            time.sleep(self.config.time_sleep_between_requests)
            phone_number_field = self.driver.find_element(
                By.XPATH, '//input[@inputmode="tel"]'
            )
            phone_number_field.send_keys(PHONE_NUMBER)

            try:
                continue_button = self.driver.find_element(
                    By.XPATH, '//button[@data-qa="expand-login-by-password"]'
                )
                continue_button.click()

            # TODO: Странная обработки ошибки и отсутствие действия после её возникновения
            except BaseException:
                pass

            time.sleep(self.config.time_sleep_between_requests)
            password_field = self.driver.find_element(
                By.XPATH, '//input[@name="password"]'
            )
            password_field.send_keys(PASSWORD)

            # TODO: Странная обработки ошибки и отсутствие действия после её возникновения
            try:
                login_button = self.driver.find_element(
                    By.XPATH, '//button[@data-qa="submit-button"]'
                )
                login_button.click()
            except BaseException:
                pass

            time.sleep(self.config.time_sleep_between_requests)

        except BaseException as er:
            print(f'Возникла ошибка в {__name__}: {er}')

    def move_to_chat(self) -> None:
        """
        Переходит с главной страницу HH.ru на страницу чатов.
        Пролистывает всю страницу с чатами до конца.

        :return None
        """
        self.driver.get(self.config.url_chat)
        self.scrolling_chats()

    def scrolling_chats(self) -> None:
        """Скроллит траницу с чатами вниз."""
        chats_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "___chats")]'))
        )
        prev_chats = self.driver.find_elements(
            By.XPATH, '//a[contains(@data-qa, "chatik-open-chat-")]'
        )
        prev_count = len(prev_chats)
        attempts = 0
        max_attempts = 100

        while attempts < max_attempts:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight', chats_container
            )
            time.sleep(2)

            current_chats = self.driver.find_elements(
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

        with open('chats.html', 'w') as file:
            file.write(self.driver.page_source)

    def get_message_from_chats(self, chats_data: list):
        """Получает сообщения из чатов."""
        all_messages = []
        try:
            for chat_data in chats_data:
                chat_url = chat_data[0]['id']
                self.driver.get(f'https://chatik.hh.ru/chat/{chat_url}')
                print(f'Перешли в чат {chat_url}')
                time.sleep(2)

                messages = self.scroll_chat_up_and_get_message(self.driver)
                all_messages.append(messages)
                time.sleep(2)

        except BaseException as er:
            print(f'Возникла ошибка в {__name__}: {er}')
        finally:
            with open('messages.txt', 'w') as file:
                for message in all_messages:
                    file.write(str(message))
                    file.write("\n")
            self.driver.quit()


    def scroll_chat_up_and_get_message(self) -> str:
        """Скроллит чат вверх и возвращает сообщения."""
        chat_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "___content")]'))
        )

        self.driver.execute_script(
            'arguments[0].scrollTop = 0', chat_container
        )
        time.sleep(2)

        current_messages = self.driver.find_elements(
            By.XPATH, '//div[contains(@data-qa, "chatik-chat-message-")]'
        )
        current_count = len(current_messages)

        print(f'+ {current_count} сообщений')

        html = self.driver.page_source
        messages_data = parse_messages(html)
        return messages_data
        # with open('chats.txt', 'a') as file:
        #     file.write(messages)
