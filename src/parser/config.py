from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParserConfig:
    """Конфигурация для парсера HH.ru."""

    url_chat: str = 'https://chatik.hh.ru'
    url: str = 'https://hh.ru/account/login?role=applicant&backurl=%2F'
    time_sleep_between_requests: int = 3
    time_sleep_between_scroll: int = 5
    chats_container_await: int = 10
    min_attempts_to_scroll: int = 0
    max_attempts_to_scroll: int = 100
