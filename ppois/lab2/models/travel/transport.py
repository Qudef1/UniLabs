from datetime import datetime, timedelta
from typing import Optional
from .geography import City
from models.people.person import Person
from services.bank_account import BankAccount, Transaction, NotEnoughMoney
from random import randint


class Transport:
    """
    @brief Абстрактный базовый класс для всех видов транспорта
    @details Определяет общие атрибуты и метод бронирования для перемещения между городами.
    Используется как родительский класс для Flight, Train, Bus.
    """

    def __init__(
        self,
        start_point: City,
        end_point: City,
        start_time: datetime,
        end_time: datetime,
        price_for_hour: float,
        company_bank_account: Optional[BankAccount] = None
    ):
        """
        @brief Конструктор транспорта
        @param start_point Город отправления
        @param end_point Город назначения
        @param start_time Время отправления
        @param end_time Время прибытия
        @param price_for_hour Стоимость за час использования транспорта
        @param company_bank_account Банковский счёт компании-перевозчика (по умолчанию — общий счёт)
        """
        if company_bank_account is None:
            company_bank_account = BankAccount(0, "common_bank_account")
        self.start_point = start_point
        self.end_point = end_point
        self.start_time = start_time
        self.end_time = end_time
        self.price_for_hour = price_for_hour
        self.bank_account = company_bank_account

    def book(self, person: Person) -> bool:
        """
        @brief Бронирует транспорт для клиента с оплатой
        @param person Клиент, бронирующий транспорт
        @return True, если оплата прошла успешно; False в случае нехватки средств
        @note Стоимость рассчитывается как: price_for_hour * продолжительность (в часах)
        """
        duration_hours = (self.end_time - self.start_time).total_seconds() / 3600.0
        total_price = self.price_for_hour * duration_hours
        try:
            Transaction(person.bank_account, self.bank_account, total_price)
            return True
        except NotEnoughMoney:
            print("not enough money to book transport")
            return False

    def __str__(self) -> str:
        """
        @brief Строковое представление транспорта
        @return Строка в формате: "ClassName: Город1 - Город2, duration X.X hours"
        """
        duration = (self.end_time - self.start_time).total_seconds() / 3600.0
        return f"{self.__class__.__name__}: {self.start_point} - {self.end_point}, duration {duration} hours"


class Flight(Transport):
    """
    @brief Представляет авиаперелёт
    @details Расширяет Transport, добавляя номер рейса и тип класса (эконом, бизнес и т.д.).
    Стоимость = базовая цена * class_type.
    """

    def __init__(
        self,
        start_point: City,
        end_point: City,
        start_time: datetime,
        end_time: datetime,
        price: float,
        flight_number: str,
        class_type: int
    ):
        """
        @brief Конструктор авиаперелёта
        @param start_point Город отправления
        @param end_point Город назначения
        @param start_time Время вылета
        @param end_time Время посадки
        @param price Базовая стоимость билета
        @param flight_number Номер рейса (например, "AF1234")
        @param class_type Множитель цены за класс (1 = эконом, 2 = бизнес и т.д.)
        """
        super().__init__(
            start_point,
            end_point,
            start_time,
            end_time,
            price * class_type
        )
        self.flight_number = flight_number

    def __str__(self) -> str:
        """
        @brief Строковое представление авиаперелёта
        @return Строка в формате: "Flight AF1234, Город1 - Город2, duration X.X hours"
        """
        duration = (self.end_time - self.start_time).total_seconds() / 3600.0
        return f"Flight {self.flight_number}, {self.start_point} - {self.end_point}, duration {duration} hours"


class Train(Transport):
    """
    @brief Представляет железнодорожный поезд
    @details Расширяет Transport, добавляя номер поезда и тип класса.
    Стоимость = (базовая цена * class_type) / 2.
    Поддерживает задержки на границе.
    """

    def __init__(
        self,
        start_point: City,
        end_point: City,
        start_time: datetime,
        end_time: datetime,
        price: float,
        train_number: str,
        class_type: int
    ):
        """
        @brief Конструктор поезда
        @param start_point Город отправления
        @param end_point Город назначения
        @param start_time Время отправления
        @param end_time Время прибытия
        @param price Базовая стоимость билета
        @param train_number Номер поезда (например, "TGV789")
        @param class_type Множитель цены за класс (1 = плацкарт, 2 = купе и т.д.)
        """
        super().__init__(
            start_point,
            end_point,
            start_time,
            end_time,
            price * class_type / 2
        )
        self.train_number = train_number

    def __str__(self) -> str:
        """
        @brief Строковое представление поезда
        @return Строка в формате: "Train TGV789, Город1 - Город2, duration X.X hours"
        """
        duration = (self.end_time - self.start_time).total_seconds() / 3600.0
        return f"Train {self.train_number}, {self.start_point} - {self.end_point}, duration {duration} hours"

    def stuck_at_border(self):
        """
        @brief Моделирует задержку поезда на границе
        @details Случайным образом увеличивает время прибытия на 2–24 часа
        """
        self.end_time = self.end_time + timedelta(hours=randint(2, 24))


class Bus(Transport):
    """
    @brief Представляет автобусный маршрут
    @details Расширяет Transport, добавляя номер автобуса и идентификатор компании.
    Поддерживает поломки (прокол шины) и задержки на границе.
    """

    def __init__(
        self,
        start_point: City,
        end_point: City,
        start_time: datetime,
        end_time: datetime,
        price_for_hour: float,
        bus_number: str,
        bus_company: int
    ):
        """
        @brief Конструктор автобуса
        @param start_point Город отправления
        @param end_point Город назначения
        @param start_time Время отправления
        @param end_time Время прибытия
        @param price_for_hour Стоимость за час поездки
        @param bus_number Номер автобуса (например, "BUS-456")
        @param bus_company Идентификатор транспортной компании
        """
        super().__init__(
            start_point,
            end_point,
            start_time,
            end_time,
            price_for_hour
        )
        self.bus_number = bus_number
        self.bus_company = bus_company

    def __str__(self) -> str:
        """
        @brief Строковое представление автобуса
        @return Строка в формате: "Bus BUS-456, BUS-456, Город1 - Город2, duration X.X hours"
        @note Номер автобуса выводится дважды (как в оригинальном коде)
        """
        duration = (self.end_time - self.start_time).total_seconds() / 3600.0
        return f"Bus {self.bus_number}, {self.bus_number}, {self.start_point} - {self.end_point}, duration {duration} hours"

    def puncture_tire(self):
        """
        @brief Моделирует прокол шины
        @details Увеличивает время прибытия на 3 часа
        """
        self.end_time = self.end_time + timedelta(hours=3)

    def stuck_at_border(self):
        """
        @brief Моделирует задержку автобуса на границе
        @details Случайным образом увеличивает время прибытия на 2–24 часа
        """
        self.end_time = self.end_time + timedelta(hours=randint(2, 24))


class CarRental:
    """
    @brief Представляет услугу аренды автомобиля
    @details Позволяет арендовать автомобиль в конкретном городе на заданный период.
    @warning Этот класс НЕ наследуется от Transport, поэтому не может быть добавлен
    через метод Tour.add_transport(). Если требуется интеграция с транспортом —
    рассмотрите наследование от Transport.
    """

    def __init__(
        self,
        city: City,
        price_per_hour: float,
        car_model: str,
        start_date: datetime,
        end_date: datetime
    ):
        """
        @brief Конструктор аренды автомобиля
        @param city Город, где доступна аренда
        @param price_per_hour Стоимость аренды за час
        @param car_model Модель автомобиля (например, "Renault Clio")
        @param start_date Время начала аренды
        @param end_date Время окончания аренды
        """
        self.city = city
        self.price_per_hour = price_per_hour
        self.car_model = car_model
        self.start_date = start_date
        self.end_date = end_date
        self.is_rented = False
        self.total_price = (end_date - start_date).total_seconds() / 3600.0 * price_per_hour
        self.rental_service_bank_account = BankAccount(100000, f"{car_model}_{price_per_hour}")

    def rent(self, person: Person) -> bool:
        """
        @brief Арендует автомобиль для клиента
        @param person Клиент, желающий арендовать автомобиль
        @return True, если аренда успешна; False, если автомобиль уже арендован или недостаточно средств
        @exception NotEnoughMoney Если на счёте клиента недостаточно средств
        """
        if self.is_rented:
            print(f"{self.car_model} is already rented")
            return False
        try:
            Transaction(person.bank_account, self.rental_service_bank_account, self.total_price)
        except NotEnoughMoney:
            print("Not enough money")
            return False

        self.is_rented = True
        print(f"Car {self.car_model} rented in {self.city} for {self.total_price:.2f}")
        return True

    def __str__(self) -> str:
        """
        @brief Строковое представление аренды автомобиля
        @return Строка в формате: "CarRental: Модель в Город, X.XX total"
        """
        return f"CarRental: {self.car_model} in {self.city}, {self.total_price:.2f} total"