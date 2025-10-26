from datetime import date

class VisaExpiredDate(Exception):
    """
    @brief Исключение: виза просрочена
    @details Выбрасывается при попытке использовать визу после даты окончания срока действия.
    """
    def __init__(self, visa_number: str, expiration_date: date):
        """
        @brief Конструктор исключения
        @param visa_number Номер просроченной визы
        @param expiration_date Дата окончания срока действия визы
        """
        super().__init__(f"Visa {visa_number} has expired on {expiration_date}")


class VisaNoEnabledEntries(Exception):
    """
    @brief Исключение: закончились доступные въезды по визе
    @details Выбрасывается при попытке использовать визу, у которой исчерпан лимит въездов.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("You have already used all your entries on this visa")


class VisaNotAvailable(Exception):
    """
    @brief Исключение: виза недоступна
    @details Выбрасывается, если виза неактивна, просрочена или исчерпаны въезды.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Your visa is not available")


class VisaInvalidDate(Exception):
    """
    @brief Исключение: некорректные даты выдачи/окончания
    @details Выбрасывается, если дата окончания <= даты выдачи.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Expiration date Error")


class Visa:
    """
    @brief Представляет визу для въезда в страну
    @details Управляет сроком действия, количеством въездов, статусом активности.
    Поддерживает проверку валидности и использование въездов.
    """

    def __init__(self, visa_number: str, country: str, issue_date: date, expiration_date: date,
                 entry_count: int = 1):
        """
        @brief Конструктор визы
        @param visa_number Уникальный номер визы (например, "V123456")
        @param country Страна назначения (например, "France")
        @param issue_date Дата выдачи визы
        @param expiration_date Дата окончания срока действия
        @param entry_count Количество разрешённых въездов (по умолчанию 1)
        @exception VisaInvalidDate Если expiration_date <= issue_date
        @exception VisaNoEnabledEntries Если entry_count <= 0
        """
        if expiration_date <= issue_date:
            raise VisaInvalidDate()
        if entry_count <= 0:
            raise VisaNoEnabledEntries()
        self.visa_number = visa_number
        self.country = country
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.entry_count = entry_count
        self.used_entries = 0
        self.is_active = True

    def is_expired(self) -> bool:
        """
        @brief Проверяет, просрочена ли виза
        @return True, если текущая дата позже expiration_date; иначе False
        """
        return date.today() > self.expiration_date

    def is_valid(self) -> bool:
        """
        @brief Проверяет, можно ли использовать визу
        @return True, если виза не просрочена, активна и есть доступные въезды; иначе False
        """
        return not self.is_expired() and self.is_active and self.used_entries < self.entry_count

    def days_until_expiration(self) -> int:
        """
        @brief Возвращает количество дней до окончания срока действия
        @return Число дней (0, если уже просрочена)
        """
        if self.is_expired():
            return 0
        return int((self.expiration_date - date.today()).days)

    def activate(self):
        """@brief Активирует визу (устанавливает is_active = True)"""
        self.is_active = True

    def deactivate(self):
        """@brief Деактивирует визу (устанавливает is_active = False)"""
        self.is_active = False

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

    def use_entry(self) -> None:
        """
        @brief Использует один въезд по визе
        @details Увеличивает счётчик использованных въездов.
        Если въезды исчерпаны — деактивирует визу.
        @exception VisaNotAvailable Если виза недоступна (неактивна/просрочена/нет въездов)
        @exception VisaExpiredDate Если виза просрочена (дополнительная проверка)
        @exception VisaNoEnabledEntries Если все въезды уже использованы
        """
        if not self.is_valid():
            raise VisaNotAvailable()
        if self.is_expired():
            raise VisaExpiredDate(self.visa_number, self.expiration_date)
        if self.used_entries >= self.entry_count:
            raise VisaNoEnabledEntries()

        self.used_entries += 1

        if self.used_entries >= self.entry_count:
            self.deactivate()

    def get_expiration_date(self) -> date:
        """
        @brief Возвращает дату окончания срока действия визы
        @return Дата в формате datetime.date
        """
        return self.expiration_date