from .visa import Visa
from datetime import date
from typing import Optional

class PassportIsExpired(Exception):
    """
    @brief Исключение: паспорт просрочен
    @details Выбрасывается при создании паспорта с датой окончания срока действия в прошлом.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Passport is expired")


class Passport:
    """
    @brief Представляет заграничный паспорт человека
    @details Хранит персональные данные, номер паспорта, дату окончания срока действия
    и привязанную визу. Проверяет валидность срока действия при создании.
    """

    def __init__(
        self,
        passport_num: str,
        name: str,
        surname: str,
        passport_expiration_date: date,
        visa: Optional[Visa] = None
    ):
        """
        @brief Конструктор паспорта
        @param passport_num Уникальный номер паспорта (например, "P987654")
        @param name Имя владельца паспорта
        @param surname Фамилия владельца паспорта
        @param passport_expiration_date Дата окончания срока действия паспорта
        @param visa Опциональная виза, привязанная к паспорту
        @exception PassportIsExpired Если дата окончания раньше текущей даты
        """
        self.visa = visa
        self.__passport_num = passport_num
        self.passport_expiration_date = passport_expiration_date
        self.name = name
        self.surname = surname
        if passport_expiration_date < date.today():
            raise PassportIsExpired()

    def set_visa(self, visa: Visa):
        """
        @brief Привязывает визу к паспорту
        @param visa Объект Visa, который будет привязан к паспорту
        @note Заменяет предыдущую визу, если она существовала
        """
        self.visa = visa

    def __getattribute__(self, name):
        """
        @brief Переопределённый метод доступа к атрибутам
        @details Логирует попытки доступа к несуществующим атрибутам.
        @param name Имя запрашиваемого атрибута
        @exception AttributeError Если атрибут не найден
        """
        try:
            return super().__getattribute__(name)
        except AttributeError:
            print("Attribute not found")
            raise