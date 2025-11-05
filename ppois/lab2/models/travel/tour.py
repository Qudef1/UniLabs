from datetime import date
from typing import List
from .geography import City
from models.people.person import Person as Client
from models.docs.visa import Visa
from .accomodation import Accomodation
from .transport import Transport
from services.services import Service
from .booking import Booking
from services.bank_account import Transaction, BankAccount


class TourAndVisaIncompatible(Exception):
    """
    @brief Исключение: виза несовместима c туром
    @details Выбрасывается, если страна визы не совпадает co страной тура,
    даты тура выходят за рамки действия визы, или виза недействительна.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Your visa is incompatible with this tour")


class EndAndStartDateError(Exception):
    """
    @brief Исключение: некорректные даты начала и окончания тура
    @details Выбрасывается, если дата окончания тура не позже даты начала.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("End date must be after the start date")


class Tour:
    """
    @brief Представляет туристический тур
    @details Объединяет проживание, транспорт, услуги и достопримечательности в одном путешествии.
    Поддерживает проверку визы, расчёт полной стоимости и бронирование.
    """

    def __init__(
        self,
        base_cost: float,
        start_date: date,
        end_date: date,
        destination: City,
        commission_rate: float = 0.05,
        accommodations: List[Accomodation] = None,
        transports: List[Transport] = None,
        services: List[Service] = None,
        bookings: List[Booking] = None
    ):
        """
        @brief Конструктор тура
        @param base_cost Базовая стоимость тура (без проживания, транспорта и услуг)
        @param start_date Дата начала тура
        @param end_date Дата окончания тура
        @param destination Город назначения тура
        @param commission_rate Комиссия агентства (по умолчанию 5%)
        @param accommodations Список объектов проживания (по умолчанию пустой список)
        @param transports Список транспортных средств (по умолчанию пустой список)
        @param services Список дополнительных услуг (по умолчанию пустой список)
        @param bookings Список бронирований (по умолчанию пустой список)
        @exception EndAndStartDateError Если end_date <= start_date
        """
        if end_date <= start_date:
            raise EndAndStartDateError()

        self.base_cost = base_cost
        self.start_date = start_date
        self.end_date = end_date
        self.destination = destination
        self.accommodations = accommodations or []
        self.transports = transports or []
        self.services = services or []
        self.commission_rate = commission_rate
        self.sights = []
        self.bookings = bookings or []

        self.price = self.__calculate_total_price()

    def __calculate_total_price(self) -> float:
        """
        @brief Рассчитывает полную стоимость тура
        @details Суммирует базовую стоимость, проживание, транспорт, услуги и добавляет комиссию.
        @return Общая стоимость тура с комиссией
        """
        total = self.base_cost

        for trans in self.transports:
            hours = (trans.end_time - trans.start_time).total_seconds() / 3600
            total += trans.price_for_hour * hours

        for acc in self.accommodations:
            total += acc.price

        for service in self.services:
            total += service.price

        total += total * self.commission_rate

        return total

    def add_booking(self, booking: Booking):
        """
        @brief Добавляет бронирование в тур
        @param booking Объект Booking для добавления
        @note После добавления пересчитывается общая стоимость тура
        """
        self.bookings.append(booking)
        self.price = self.__calculate_total_price()

    def add_accommodation(self, accommodation: Accomodation):
        """
        @brief Добавляет проживание в тур
        @param accommodation Объект Accomodation для добавления
        @note После добавления пересчитывается общая стоимость тура
        """
        self.accommodations.append(accommodation)
        self.price = self.__calculate_total_price()

    def add_transport(self, transport: Transport):
        """
        @brief Добавляет транспорт в тур
        @param transport Объект Transport для добавления
        @note После добавления пересчитывается общая стоимость тура
        """
        self.transports.append(transport)
        self.price = self.__calculate_total_price()

    def add_service(self, service: Service):
        """
        @brief Добавляет дополнительную услугу в тур
        @param service Объект Service для добавления
        @note После добавления пересчитывается общая стоимость тура
        """
        self.services.append(service)
        self.price = self.__calculate_total_price()

    def add_sight(self, sight):
        """
        @brief Добавляет достопримечательность в тур
        @param sight Объект Sight для добавления
        @note Достопримечательность добавляется только если её город совпадает с destination
        """
        if sight.city == self.destination:
            self.sights.append(sight)
        else:
            print(f"Sight is not in the tour destination: {self.destination}")

    def check_visa(self, client: Client):
        """
        @brief Проверяет совместимость визы клиента с туром
        @param client Клиент (Person), у которого проверяется виза
        @exception TourAndVisaIncompatible Если:
            - Страна визы не совпадает со страной назначения
            - Даты тура выходят за рамки действия визы
            - Виза недействительна (просрочена, неактивна, исчерпаны въезды)
        @note При успехе выводит сообщение: "Your visa is compatible with this tour"
        """
        person_visa: Visa = client.passport.visa

        if person_visa.country != self.destination.country.name:
            raise TourAndVisaIncompatible()

        if not (self.start_date >= person_visa.issue_date and self.end_date <= person_visa.get_expiration_date()):
            raise TourAndVisaIncompatible()

        if not person_visa.is_valid():
            raise TourAndVisaIncompatible()

        print("Your visa is compatible with this tour")

    def book(self, client: Client, travel_agency_bank_account: BankAccount) -> bool:
        """
        @brief Бронирует тур для клиента
        @param client Клиент, бронирующий тур
        @param travel_agency_bank_account Банковский счёт туристического агентства
        @return True, если бронирование успешно; False в случае ошибки визы или нехватки средств
        @note При успехе создаётся транзакция на сумму self.price
        """
        try:
            self.check_visa(client)
        except TourAndVisaIncompatible as e:
            print(e)
            return False

        if client.bank_account.sum < self.price:
            print("Not enough money to book the tour.")
            return False

        Transaction(client.bank_account, travel_agency_bank_account, self.price)
        print(f"Tour to {self.destination} booked successfully for {self.price:.2f}!")
        return True

    def get_total_duration(self) -> int:
        """
        @brief Возвращает продолжительность тура в днях
        @return Количество дней между end_date и start_date (без учёта времени)
        """
        return (self.end_date - self.start_date).days

    def __str__(self) -> str:
        """
        @brief Строковое представление тура
        @return Строка в формате:
            "Tour to Город, Дата1 - Дата2, Total Price: X.XX, Duration: N days"
        """
        return (
            f"Tour to {self.destination}, "
            f"{self.start_date} - {self.end_date}, "
            f"Total Price: {self.price:.2f}, "
            f"Duration: {self.get_total_duration()} days"
        )

    def __getattr__(self, name):
        """
        @brief Обработка обращения к несуществующему атрибуту
        @param name Имя запрашиваемого атрибута
        @return None (вместо исключения)
        @note Выводит сообщение "attribute not found" в консоль
        @warning Этот подход скрывает ошибки опечаток в именах атрибутов
        """
        print("attribute not found")
        return None