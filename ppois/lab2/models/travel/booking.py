from datetime import datetime
from typing import List, Optional
from models.people.person import Person
from .transport import Flight, CarRental
from .accomodation import Accomodation
from services.bank_account import Transaction, NotEnoughMoney


class Booking:
    """
    @brief Базовый класс для бронирования туристических услуг
    @details Представляет общую логику бронирования: генерацию ID, подтверждение и отмену.
    Используется как родительский для специализированных типов бронирования.
    """

    def __init__(self, person: Person, booking_date: datetime = None):
        """
        @brief Конструктор базового бронирования
        @param person Клиент, совершающий бронирование
        @param booking_date Дата и время бронирования (по умолчанию — текущее время)
        """
        self.person = person
        self.booking_date = booking_date or datetime.now()
        self.is_confirmed = False
        self.booking_id = self.generate_booking_id()

    def generate_booking_id(self) -> str:
        """
        @brief Генерирует уникальный идентификатор бронирования
        @return Строка в формате: "BOOK_<bank_account_id>_<YYYYMMDDHHMMSS>"
        """
        return f"BOOK_{self.person.bank_account.id}_{self.booking_date.strftime('%Y%m%d%H%M%S')}"

    def confirm(self) -> bool:
        """
        @brief Подтверждает бронирование
        @return True после успешного подтверждения
        @note Выводит сообщение в консоль
        """
        self.is_confirmed = True
        print(f"Booking {self.booking_id} confirmed.")
        return True

    def cancel(self) -> bool:
        """
        @brief Отменяет бронирование
        @return True, если бронирование было подтверждено и успешно отменено; False, если не подтверждено
        @note Выводит соответствующее сообщение в консоль
        """
        if not self.is_confirmed:
            print("Booking is not confirmed yet.")
            return False
        self.is_confirmed = False
        print(f"Booking {self.booking_id} cancelled.")
        return True

    def __str__(self) -> str:
        """
        @brief Строковое представление бронирования
        @return Строка в формате: "Booking ID: BOOK_..., Confirmed: True/False"
        """
        return f"Booking ID: {self.booking_id}, Confirmed: {self.is_confirmed}"


class FlightBooking(Booking):
    """
    @brief Бронирование авиаперелёта
    @details Расширяет базовое бронирование, автоматически пытаясь забронировать рейс
    при создании объекта.
    """

    def __init__(self, person: Person, flight: Flight):
        """
        @brief Конструктор бронирования авиаперелёта
        @param person Клиент, бронирующий перелёт
        @param flight Объект Flight, который нужно забронировать
        @note При создании автоматически вызывается flight.book(person),
        и результат сохраняется в self.is_confirmed
        """
        super().__init__(person)
        self.flight = flight
        self.is_confirmed = self.flight.book(person)

    def __str__(self) -> str:
        """
        @brief Строковое представление бронирования перелёта
        @return Строка в формате: "Flight Booking: BOOK_... | Flight ..."
        """
        return f"Flight Booking: {self.booking_id} | {self.flight}"


class AccomodationBooking(Booking):
    """
    @brief Бронирование проживания (отель, хостел, квартира)
    @details Расширяет базовое бронирование, связывая его с объектом проживания.
    """

    def __init__(self, person: Person, accommodation: Accomodation):
        """
        @brief Конструктор бронирования проживания
        @param person Клиент, бронирующий проживание
        @param accommodation Объект Accomodation для бронирования
        @note Метод accommodation.book(person) вызывается только если бронирование уже подтверждено
        (в текущей реализации — никогда, так как is_confirmed = False по умолчанию).
        """
        super().__init__(person)
        self.accommodation = accommodation
        if self.is_confirmed:
            self.accommodation.book(person)

    def __str__(self) -> str:
        """
        @brief Строковое представление бронирования проживания
        @return Строка в формате: "Hotel Booking: BOOK_... | <accommodation>"
        """
        return f"Hotel Booking: {self.booking_id} | {self.accommodation}"