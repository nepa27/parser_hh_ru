from selenium_utils import driver_init, login_hh_ru, get_message_from_chats
from parser_utils import parse_chats_url


def main():
    """Основная функция."""
    driver = None
    try:
        driver = driver_init()
        login_hh_ru(driver)
        chats_data = parse_chats_url()
        get_message_from_chats(chats_data, driver)
    except BaseException as er:
        print(f'Возникла ошибка в {__name__}: {er}')
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    main()
