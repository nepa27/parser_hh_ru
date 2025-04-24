import time
import os

from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constatns import URL, CHATIK

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


def login_hh_ru():
    url = URL
    chatik = CHATIK
    user_agent = UserAgent().random

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

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
        print(f'Возникла ошибка: {er}')
    finally:
        driver.quit()

def scrolling_chats(driver):
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
    with open(f'chats.html', 'w') as file:
        file.write(html)
