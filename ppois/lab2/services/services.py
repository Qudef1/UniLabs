from models.people.person import Person
from .bank_account import BankAccount, Transaction, NotEnoughMoney
from models.travel.geography import City


class Service:
    """
    @brief Базовый класс для туристических услуг
    @details Предоставляет общую функциональность бронирования услуги с оплатой через банковскую транзакцию.
    Является родительским для всех конкретных типов услуг.
    """

    def __init__(self, name: str, price: float):
        """
        @brief Конструктор базовой услуги
        @param name Название услуги (например, "Travel Insurance")
        @param price Стоимость услуги в валюте счёта
        """
        self.name = name
        self.price = price

    def book(self, client: Person) -> bool:
        """
        @brief Бронирует услугу для клиента с оплатой
        @param client Объект Person, который бронирует услугу
        @return True, если оплата прошла успешно; False, если недостаточно средств
        @note При успешной оплате создаётся транзакция на счёт сервиса "SERVICE_<name>"
        """
        try:
            Transaction(
                client.bank_account,
                BankAccount(10000, f"SERVICE_{self.name}"),
                self.price
            )
            print(f"Service '{self.name}' booked for {client.passport.name}")
            return True
        except NotEnoughMoney:
            print("Not enough money to book service")
            return False


class Insurance(Service):
    """
    @brief Страховка для путешествий
    @details Расширяет базовую услугу, добавляя тип покрытия и возможность подачи заявки на возмещение.
    """

    def __init__(self, coverage: str, price: float):
        """
        @brief Конструктор страховки
        @param coverage Тип страхового покрытия (например, "Medical", "Trip Cancellation")
        @param price Стоимость страховки
        """
        super().__init__("Travel Insurance", price)
        self.coverage = coverage 

    def claim(self):
        """
        @brief Подача заявки на страховое возмещение
        @note Выводит сообщение в консоль (в реальной системе — отправка запроса в страховую)
        """
        return f"Claim submitted for {self.coverage} insurance"


class VisaSupportService(Service):
    """
    @brief Услуга поддержки по оформлению визы
    @details Помогает клиенту с подготовкой документов и консультациями по визе в указанную страну.
    """

    def __init__(self, price: float):
        """
        @brief Конструктор услуги поддержки по визе
        @param price Стоимость услуги
        """
        super().__init__("Visa Support", price)

    def assist(self, client: Person, country: str):
        """
        @brief Оказывает поддержку клиенту по визе в указанную страну
        @param client Клиент, запрашивающий помощь
        @param country Страна назначения для визы
        @note Выводит информационное сообщение в консоль
        """
        return f"Visa support provided for {client.passport.name} to {country}"


class LuggageService(Service):
    """
    @brief Услуга доставки багажа
    @details Обеспечивает транспортировку багажа между городами с указанием веса.
    """

    def __init__(self, weight_kg: int, price: float):
        """
        @brief Конструктор услуги доставки багажа
        @param weight_kg Вес багажа в килограммах
        @param price Стоимость доставки
        """
        super().__init__("Luggage Service", price)
        self.weight_kg = weight_kg

    def send_luggage(self, from_city: City, to_city: City):
        """
        @brief Организует отправку багажа из одного города в другой
        @param from_city Город отправления
        @param to_city Город назначения
        @note Выводит информацию о доставке в консоль
        """
        return f"Luggage ({self.weight_kg} kg) sent from {from_city} to {to_city}"