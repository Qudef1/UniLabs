from models.docs.passport import Passport
from services.bank_account import BankAccount

class ContactInfo:
    """
    @brief Контактная информация пользователя.
    @details Хранит email и телефон. Используется в классе Person.
    """

    def __init__(self, email: str = "", phone: str = ""):
        """
        @brief Конструктор контактной информации.
        @param email Электронная почта.
        @param phone Номер телефона.
        """
        self.email = email
        self.phone = phone

    def formatted(self) -> str:
        """
        @brief Форматированный вывод контактных данных.
        @return Строка вида "email / phone".
        """
        return f"{self.email} / {self.phone}"

class Person:
    """
    @brief Представляет туриста или клиента туристического агентства
    @details Связывает паспорт, банковский счёт и эмоциональное состояние (настроение).
    Используется для моделирования взаимодействия с туристическими услугами.
    """

    def __init__(self, passport: Passport, bank_account: BankAccount, mood: int = 15):
        """
        @brief Конструктор класса Person
        @param passport Объект Passport, принадлежащий человеку
        @param bank_account Банковский счёт для оплаты услуг
        @param mood Начальное значение настроения (по умолчанию 15, диапазон: любое целое число)
        """
        self.bank_account = bank_account
        self.passport = passport
        self.__mood = mood
        self.contact_info = None

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
    
    def set_contact_info(self, contact_info: ContactInfo):
        """
        @brief Устанавливает контактную информацию для человека
        @param contact_info Объект ContactInfo с данными контакта
        """
        self.contact_info = contact_info
    def __check_mood(self):
        """
        @brief Проверяет текущее настроение и выводит соответствующее сообщение
        @details Приватный метод, вызываемый при изменении настроения.
        @note Сообщения:
             - mood <= 10: "you are now sad, go make some activities"
             - 10 < mood <= 20: "you feel yourself fine"
             - mood > 20: "you feel very well"
        """
        if self.__mood <= 10:
            print("you are now sad, go make some activities")
        elif 10 < self.__mood <= 20:
            print("you feel yourself fine")
        else:
            print("you feel very well")

    def change_mood(self, mood_value: int):
        """
        @brief Изменяет настроение человека на заданное значение
        @param mood_value Целое число, которое прибавляется к текущему настроению
        @note После изменения вызывается приватный метод __check_mood()
        """
        self.__mood += mood_value
        self.__check_mood()