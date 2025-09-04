from abc import ABC, abstractmethod


class AbstractSelenim(ABC):
    """Базовый класс для Selenium."""

    @abstractmethod
    def driver_init(self) -> None:
        """Инициализация драйвера."""
        ...
