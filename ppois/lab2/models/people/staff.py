from datetime import datetime
from typing import List, Optional
from .person import Person as Client
from models.travel.booking import Booking
from models.travel.tour import Tour
from models.travel.geography import City
from random import random
from services.bankAccount import BankAccount


GUIDE_SUCCESS_RATE = 0.3
"""
@brief Константа: вероятность успешного завершения гидом тура
@details Используется для расчёта бонусов. Если случайное число > GUIDE_SUCCESS_RATE,
гид получает бонус.
"""


class EmployeeIsUnavailable(Exception):
    """
    @brief Исключение: сотрудник недоступен
    @details Выбрасывается, когда гид не может быть назначен на тур
    (занят или не соответствует городу).
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Employee is unavailable for this moment")


class BookingTourFailed(Exception):
    """
    @brief Исключение: не удалось забронировать тур
    @details Обобщённая ошибка, возникающая при сбое в процессе бронирования агентом.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Tour booking was failed")


class Salary:
    """
    @brief Представляет заработную плату сотрудника
    @details Включает базовую ставку и бонус, поддерживает расчёт общей суммы.
    """

    def __init__(self, base_salary: float, bonus: float = 0.0):
        """
        @brief Конструктор заработной платы
        @param base_salary Базовая зарплата
        @param bonus Бонус (по умолчанию 0.0)
        """
        self.base_salary = base_salary
        self.bonus = bonus

    def total_salary(self) -> float:
        """
        @brief Рассчитывает общую заработную плату
        @return Сумма базовой зарплаты и бонуса
        """
        return self.base_salary + self.bonus

    def __str__(self) -> str:
        """
        @brief Строковое представление зарплаты
        @return Строка в формате:
            "Base: X, Bonus: Y, Total: Z"
        """
        return f"Base: {self.base_salary}, Bonus: {self.bonus}, Total: {self.total_salary()}"


class WorkSchedule:
    """
    @brief Представляет график работы сотрудника
    @details Хранит временные рамки и дни недели, в которые сотрудник работает.
    """

    def __init__(self, employee: 'Employee', start_time: str, end_time: str, days: List[str]):
        """
        @brief Конструктор графика работы
        @param employee Сотрудник, к которому применяется график
        @param start_time Время начала работы (в формате "HH.MM")
        @param end_time Время окончания работы (в формате "HH.MM")
        @param days Список рабочих дней (например, ["Mon", "Tue", ...])
        """
        self.employee = employee
        self.start_time = start_time
        self.end_time = end_time
        self.days = days

    def __str__(self) -> str:
        """
        @brief Строковое представление графика
        @return Строка в формате:
            "Schedule for Имя: Пн, Вт, ..., HH.MM-HH.MM"
        """
        return f"Schedule for {self.employee.name}: {', '.join(self.days)}, {self.start_time}-{self.end_time}"


class Employee:
    """
    @brief Базовый класс для всех сотрудников туристического агентства
    @details Содержит общую информацию: ID, имя, должность, дату приёма на работу и статус активности.
    """

    def __init__(self, employee_id: str, name: str, position: str, hire_date: datetime):
        """
        @brief Конструктор сотрудника
        @param employee_id Уникальный идентификатор сотрудника
        @param name Имя сотрудника
        @param position Должность (например, "Travel Agent", "Manager")
        @param hire_date Дата приёма на работу
        """
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.hire_date = hire_date
        self.is_active = True

    def __str__(self) -> str:
        """
        @brief Строковое представление сотрудника
        @return Строка в формате:
            "Employee: Имя, Position: Должность, ID: XXX"
        """
        return f"Employee: {self.name}, Position: {self.position}, ID: {self.employee_id}"


class TravelAgent(Employee):
    """
    @brief Туристический агент
    @details Отвечает за бронирование туров для клиентов, получает комиссию и бонусы.
    """

    def __init__(self, employee_id: str, name: str, hire_date: datetime, commission_rate: float = 0.05):
        """
        @brief Конструктор туристического агента
        @param employee_id Уникальный идентификатор
        @param name Имя агента
        @param hire_date Дата приёма на работу
        @param commission_rate Процент комиссии от стоимости тура (по умолчанию 5%)
        """
        super().__init__(employee_id, name, "Travel Agent", hire_date)
        self.commission_rate = commission_rate
        self.bookings_handled = 0
        self.salary = Salary(2000, 3000)
        self.work_schedule = WorkSchedule(self, "9.00", "18.00", ["Mnd", "Tue", "Wed", "Thu", "Fri"])

    def book_tour_for_client(self, client: Client, tour: Tour, travel_agency_bank_account: BankAccount) -> Optional[Booking]:
        """
        @brief Бронирует тур для клиента
        @param client Клиент (Person)
        @param tour Тур для бронирования
        @param travel_agency_bank_account Банковский счёт агентства
        @return Объект Booking при успехе; None не возвращается (всегда создаётся Booking)
        @exception BookingTourFailed Если tour.book() завершился с ошибкой
        @note Увеличивает счётчик обработанных бронирований и начисляет бонус
        """
        try:
            tour.book(client, travel_agency_bank_account)
        except Exception:
            raise BookingTourFailed()
        self.bookings_handled += 1
        self.get_bonus()
        print(f"Tour booked by agent {self.name} for {client.passport.name}. Commission: {tour.price * self.commission_rate:.2f}")
        return Booking(client)

    def get_bonus(self):
        """
        @brief Начисляет бонус к зарплате
        @details Увеличивает текущий бонус на 12% (умножает на 1.12)
        """
        self.salary.bonus *= 1.12

    def __str__(self) -> str:
        """
        @brief Строковое представление агента
        @return Строка в формате:
            "TravelAgent: Имя, Bookings handled: N"
        """
        return f"TravelAgent: {self.name}, Bookings handled: {self.bookings_handled}"


class Manager(Employee):
    """
    @brief Менеджер туристического агентства
    @details Отвечает за предложение туров клиентам и управление бонусами.
    """

    def __init__(self, employee_id: str, name: str, hire_date: datetime):
        """
        @brief Конструктор менеджера
        @param employee_id Уникальный идентификатор
        @param name Имя менеджера
        @param hire_date Дата приёма на работу
        """
        super().__init__(employee_id, name, "Manager", hire_date)
        self.salary = Salary(3000, 5000)
        self.work_schedule = WorkSchedule(self, "9.00", "18.00", ["Mnd", "Tue", "Wed", "Thu", "Fri"])

    def __increase_bonus(self):
        """
        @brief Увеличивает бонус менеджера на 10%
        @details Приватный метод, вызываемый при предложении туров
        """
        self.salary.bonus *= 1.1

    def offer_tours_to_client(self, tours: List[Tour]):
        """
        @brief Предлагает клиенту список доступных туров
        @param tours Список объектов Tour для предложения
        @note Автоматически увеличивает бонус менеджера
        @note Выводит все туры в консоль (для демонстрации)
        """
        self.__increase_bonus()
        print(*tours)

    def __str__(self) -> str:
        """
        @brief Строковое представление менеджера
        @return Строка в формате:
            "Manager: Имя, Department: ..."
        @warning Атрибут self.department не определён в классе — может вызвать ошибку.
        """
        # ⚠️ Исправление: убрано обращение к несуществующему атрибуту
        return f"Manager: {self.name}"


class Guide(Employee):
    """
    @brief Гид
    @details Проводит экскурсии в определённом городе, владеет языками,
    может быть недоступен после назначения на тур.
    """

    def __init__(self, employee_id: str, name: str, hire_date: datetime, languages: List[str], city: City):
        """
        @brief Конструктор гида
        @param employee_id Уникальный идентификатор
        @param name Имя гида
        @param hire_date Дата приёма на работу
        @param languages Список языков, которыми владеет гид
        @param city Город, в котором гид проводит экскурсии
        """
        super().__init__(employee_id, name, "Guide", hire_date)
        self.languages = languages
        self.city = city
        self.is_available = True
        self.salary = Salary(1000, 2000)

    def __assign_to_tour(self, tour: Tour) -> bool:
        """
        @brief Проверяет и назначает гида на тур
        @param tour Тур для назначения
        @return True, если гид доступен и город совпадает; иначе False
        @note При успешном назначении гид становится недоступным (is_available = False)
        """
        if not self.is_available or tour.destination != self.city:
            return False
        self.is_available = False
        return True

    def go_to_tour(self, tour: Tour):
        """
        @brief Отправляет гида на тур
        @param tour Тур для сопровождения
        @exception EmployeeIsUnavailable Если гид недоступен или город не совпадает
        @note С вероятностью (1 - GUIDE_SUCCESS_RATE) начисляется бонус
        """
        if self.__assign_to_tour(tour):
            if random() > GUIDE_SUCCESS_RATE:
                self.__increase_bonus()
            return None
        raise EmployeeIsUnavailable()

    def __increase_bonus(self):
        """
        @brief Увеличивает бонус гида на 20%
        @details Приватный метод, вызываемый при успешном завершении тура
        """
        self.salary.bonus *= 1.2

    def __str__(self) -> str:
        """
        @brief Строковое представление гида
        @return Строка в формате:
            "Guide: Имя, Languages: ..., City: ..."
        """
        return f"Guide: {self.name}, Languages: {', '.join(self.languages)}, City: {self.city}"