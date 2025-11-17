import datetime as dt
from typing import Optional
from .geography import City
from services.bank_account import BankAccount, Transaction, NotEnoughMoney
from random import randint


class AccomodationNotFoundOrExpired(Exception):
    """
    @brief Исключение: проживание недоступно или просрочено
    @details Выбрасывается при попытке создать бронирование с датой окончания,
    равной текущей дате (согласно текущей логике класса).
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Accomodation not found or expired")


class StartAndEndDateError(Exception):
    """
    @brief Исключение: некорректные даты проживания
    @details Выбрасывается, если дата начала не раньше даты окончания.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("start date must be before end date")

class Accomodation:
    """
    @brief Абстрактный базовый класс для проживания
    @details Определяет общую логику бронирования жилья: расчёт стоимости,
    проверку дат и выполнение платежа. Используется как родительский для Hotel, Hostel, Apartment.
    """

    def __init__(
        self,
        start_date=dt.date.today(),
        end_date=dt.date.today(),
        location: Optional[City] = None,
        price_per_night: float = 0.0,
        bank_account: Optional[BankAccount] = None
    ):
        """
        @brief Конструктор проживания
        @param start_date Дата заезда (по умолчанию — сегодня)
        @param end_date Дата выезда (по умолчанию — сегодня)
        @param location Город размещения (по умолчанию None)
        @param price_per_night Стоимость за ночь
        @param bank_account Банковский счёт владельца жилья
        @exception StartAndEndDateError Если start_date >= end_date
        @exception AccomodationNotFoundOrExpired Если end_date == сегодняшняя дата
        @note Продолжительность проживания = (end_date - start_date).days
        """
        self.start_date = start_date
        self.end_date = end_date
        self.price = price_per_night * (end_date - start_date).days
        self.price_per_night = price_per_night
        self.location = location
        self.bank_account = bank_account
        if start_date >= end_date:
            raise StartAndEndDateError()
        if self.end_date == dt.date.today():
            raise AccomodationNotFoundOrExpired()

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
            print(f"attribute {name} not found")
            raise

    def book(self, client_bank_account: BankAccount) -> bool:
        """
        @brief Бронирует проживание для клиента
        @param client_bank_account Банковский счёт клиента
        @return True, если оплата прошла успешно; False при нехватке средств
        @note Использует метод make_transaction() из BankAccount
        """
        total_price = self.price
        try:
            client_bank_account.make_transaction(self.bank_account, total_price)
            return True
        except NotEnoughMoney:
            return False


class Hotel(Accomodation):
    """
    @brief Представляет отель
    @details Расширяет базовое проживание, добавляя рейтинг звёзд и список услуг.
    """

    def __init__(
        self,
        start_date=dt.date.today(),
        end_date=dt.date.today(),
        location: Optional[City] = None,
        price_per_night: float = 0.0,
        bank_account: Optional[BankAccount] = None,
        stars: int = 1
    ):
        """
        @brief Конструктор отеля
        @param start_date Дата заезда
        @param end_date Дата выезда
        @param location Город размещения
        @param price_per_night Стоимость за ночь
        @param bank_account Банковский счёт отеля
        @param stars Количество звёзд отеля (по умолчанию 1)
        """
        super().__init__(start_date, end_date, location, price_per_night, bank_account)
        self.star_rating = stars
        self.services = ["Bedroom", "Breakfast", "Room Service"]

    def add_service(self, service: str):
        """
        @brief Добавляет дополнительную услугу в отель
        @param service Название разных услуг
        """
        self.services.append(service)

    def __str__(self) -> str:
        """
        @brief Строковое представление отеля
        @return Строка в формате:
            "Hotel in Город, X-star, services ..., price: Y/night"
        """
        return f"Hotel in {self.location}, {self.star_rating}-star, services {', '.join(self.services)}, price: {self.price_per_night}/night"


class Hostel(Accomodation):
    """
    @brief Представляет хостел
    @details Расширяет базовое проживание, добавляя количество мест в комнате.
    """

    def __init__(
        self,
        start_date=dt.date.today(),
        end_date=dt.date.today(),
        location: Optional[City] = None,
        price_per_night: float = 0.0,
        bank_account: Optional[BankAccount] = None,
        persons_for_room: int = 2
    ):
        """
        @brief Конструктор хостела
        @param start_date Дата заезда
        @param end_date Дата выезда
        @param location Город размещения
        @param price_per_night Стоимость за ночь
        @param bank_account Банковский счёт хостела
        @param persons_for_room Количество человек в одной комнате (по умолчанию 2)
        """
        super().__init__(start_date, end_date, location, price_per_night, bank_account)
        self.persons_for_room = persons_for_room

    def property_stolen(self,client_bank_account: BankAccount, amount: float) -> bool:
        """
        @brief Метод для имитации кражи имущества в хостеле
        @param client_bank_account Банковский счёт клиента
        @param amount Сумма кражи
        @return True, если списание прошло успешно; False при нехватке средств
        @note Использует метод make_transaction() из BankAccount
        """
        try:
            client_bank_account.make_transaction(self.bank_account, amount)
            return True
        except NotEnoughMoney:
            return False
    def __str__(self) -> str:
        """
        @brief Строковое представление хостела
        @return Строка в формате:
            "Hostel in Город, price: X/night, N persons in one room"
        """
        return f"Hostel in {self.location}, price: {self.price_per_night}/night, {self.persons_for_room} persons in one room"


class Apartment(Accomodation):
    """
    @brief Представляет апартаменты
    @details Расширяет базовое проживание, добавляя количество спален.
    @warning В методе __str__() используется слово "Hostel" по ошибке.
    Рекомендуется заменить на "Apartment".
    """

    def __init__(
        self,
        start_date=dt.date.today(),
        end_date=dt.date.today(),
        location: Optional[City] = None,
        price_per_night: float = 0.0,
        bank_account: Optional[BankAccount] = None,
        bedrooms: int = 1
    ):
        """
        @brief Конструктор апартаментов
        @param start_date Дата заезда
        @param end_date Дата выезда
        @param location Город размещения
        @param price_per_night Стоимость за ночь
        @param bank_account Банковский счёт владельца апартаментов
        @param bedrooms Количество спален (по умолчанию 1)
        """
        super().__init__(start_date, end_date, location, price_per_night, bank_account)
        self.bedrooms = bedrooms
        self.floor = None
    
    def get_floor(self) -> int:
        """
        @brief генерирует этаж апартаментов
        @return номер этажа (случайное число от 1 до 10)
        """
        self.floor = randint(1, 10)
        return self.floor
    
    def __str__(self) -> str:
        """
        @brief Строковое представление апартаментов
        @return Строка в формате:
            "Hostel in Город, price: X/night, has N bedrooms"
        @note В оригинальном коде используется "Hostel" вместо "Apartment".
        Это, вероятно, опечатка.
        """
        if self.floor is None:  
            return f"Apartment in {self.location}, price: {self.price_per_night}/night, has {self.bedrooms} bedrooms"
        return f"Apartment in {self.location}, price: {self.price_per_night}/night, has {self.bedrooms} bedrooms, floor: {self.floor}"