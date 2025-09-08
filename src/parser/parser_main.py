from src.parser.selenium_worker import SeleniumUtils
from src.parser.parser_utils import parse_chats_url
from src.parser.config import ParserConfig

from src.logger_config import logger

def main() -> None:
    """
    Основная функция работы парсера.

    Определяем экземпляр класса SeleniumUtils.
    Инициализируем драйвер для дальнейшей работы driver_init().
    Аутентифицируемся на HH.ru auth_hh_ru().
    Переходим на страницу с личными чатами соискателя move_to_chat().

    Сохраням данные чатов в виде HTML страницы и парсим уже её,
    чтобы не работать напрямую с браузером.
    Парсим чаты parse_chats_url().
    Далее проходим по каждому чату и получаем данные get_message_from_chats().

    """
    selenium_worker: SeleniumUtils = None
    try:
        config = ParserConfig()

        selenium_worker = SeleniumUtils(
            config,
            logger
        )
        selenium_worker.driver_init()
        selenium_worker.auth_hh_ru()
        selenium_worker.move_to_chat()

        chats_data: list = parse_chats_url()
        selenium_worker.get_message_from_chats(chats_data)

    except BaseException as er:
        logger.error(f'Возникла ошибка в {__name__}: {er}')
    finally:
        if selenium_worker is not None:
            selenium_worker.quit_driver()


if __name__ == '__main__':
    main()
