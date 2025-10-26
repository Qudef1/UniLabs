from datetime import date

class Country:
    """
    @brief Представляет страну в системе туризма
    @details Хранит название, уникальный код (например, ISO) и информацию о необходимости визы.
    Код страны инкапсулирован и доступен только через метод get_code().
    """
    
    def __init__(self, name: str, code: str, visa_required: bool = True):
        """
        @brief Конструктор класса Country
        @param name Название страны (например, "France")
        @param code Уникальный код страны (например, "FR" по ISO 3166)
        @param visa_required Флаг: требуется ли виза для въезда (по умолчанию True)
        """
        self.name = name
        self.__code = code
        self.visa_required = visa_required

    def get_code(self) -> str:
        """
        @brief Возвращает код страны
        @return Код страны в виде строки (например, "FR")
        """
        return self.__code
    
    def compare(self, other) -> bool:
        """
        @brief Сравнивает текущую страну с другой
        @param other Объект для сравнения
        @return True, если оба объекта — Country и совпадают название и код; иначе False
        """
        if isinstance(other, Country):
            return self.__code == other.get_code() and self.name == other.name
        return False
    
    def __getattribute__(self, name):
        """
        @brief Переопределённый метод доступа к атрибутам
        @details Перехватывает попытки доступа к несуществующим атрибутам.
        @param name Имя запрашиваемого атрибута
        @exception AttributeError Если атрибут не найден
        """
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            raise AttributeError(f"attribute {name} not found")
    
    def __str__(self):
        """
        @brief Возвращает строковое представление страны
        @return Строка в формате: "Название, КОД, visa required = True/False"
        """
        return f"{self.name}, {self.__code}, visa required = {self.visa_required}"


class City:
    """
    @brief Представляет город, привязанный к стране
    @details Город не может существовать без страны. Используется для локализации туров, отелей и достопримечательностей.
    """
    
    def __init__(self, name: str, country: Country):
        """
        @brief Конструктор класса City
        @param name Название города (например, "Paris")
        @param country Объект Country, к которому принадлежит город
        """
        self.name = name
        self.country = country
    
    def compare(self, other):
        """
        @brief Сравнивает текущий город с другим
        @param other Объект для сравнения
        @return True, если оба объекта — City и совпадают название и страна; иначе False или None
        """
        if isinstance(other, City):
            return other.name == self.name and other.country == self.country
    
    def __str__(self):
        """
        @brief Возвращает строковое представление города
        @return Название города (например, "Paris")
        """
        return f"{self.name}"


class Sight:
    """
    @brief Представляет достопримечательность
    @details Связывает название достопримечательности с конкретным городом и страной.
    Поддерживает вывод описания при посещении.
    """
    
    def __init__(self, name, country: Country, city: City):
        """
        @brief Конструктор класса Sight
        @param name Название достопримечательности (например, "Eiffel Tower")
        @param country Страна, где расположена достопримечательность
        @param city Город, где расположена достопримечательность
        """
        self.name = name
        self.country = country
        self.city = city

    def visit(self, sight_info: str = "This sight is unknown for now"):
        """
        @brief Имитирует посещение достопримечательности
        @param sight_info Описание достопримечательности (по умолчанию — заглушка)
        @note Выводит информацию в консоль
        """
        print(sight_info)