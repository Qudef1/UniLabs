from .tour import Tour
from models.people.person import Person
from models.people.staff import Guide, Manager, TravelAgent
from typing import List, Optional
import random
from services.bank_account import BankAccount


class EmptyStaffListOrTours(Exception):
    """
    @brief Исключение: отсутствуют сотрудники или туры в агентстве
    @details Выбрасывается, когда список для выбора (агенты, менеджеры, гиды, туры) пуст.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("There aren't any objects of this type in agency")


class ProcessClientChoice:
    """
    @brief Вспомогательный класс для случайного выбора элемента из списка
    @details Используется для имитации выбора клиента при взаимодействии с агентством.
    """

    def __init__(self, lst: Optional[List] = None):
        """
        @brief Конструктор выбора
        @param lst Список объектов для случайного выбора
        @exception EmptyStaffListOrTours Если список пуст или None
        """
        if lst is None or len(lst) == 0:
            raise EmptyStaffListOrTours()
        self.lst = lst
        self.selected = self.__process_client_choice()

    def __process_client_choice(self):
        """
        @brief Выполняет случайный выбор элемента из списка
        @return Случайный элемент из self.lst
        """
        return random.choice(self.lst)


class WorkWithClientFailed(Exception):
    """
    @brief Исключение: не удалось обработать клиента
    @details Обобщённая ошибка, возникающая при сбое в процессе взаимодействия
    с клиентом (бронирование, выбор тура и т.д.).
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("work with client was failed")

class TouristAgency:
    pass

class WorkWithClient:
    """
    @brief Класс для автоматизированного взаимодействия с клиентом
    @details Организует полный цикл: выбор менеджера и агента, предложение туров,
    бронирование и назначение гида (если есть достопримечательности).
    """

    def __init__(self, agency: TouristAgency, client: Person):
        """
        @brief Конструктор взаимодействия с клиентом
        @param agency Туристическое агентство
        @param client Клиент (Person)
        @exception WorkWithClientFailed При любой ошибке в процессе обработки
        """
        self.agency = agency
        self.client = client
        try: 
            self.__interact_with_person()
        except Exception:
            raise WorkWithClientFailed()

    def __interact_with_person(self):
        """
        @brief Выполняет полный цикл обслуживания клиента
        @details Последовательно:
            - Выбирает случайного агента и менеджера
            - Менеджер предлагает доступные туры
            - Клиент (случайно) выбирает тур
            - Агент бронирует тур
            - Если в туре есть достопримечательности — назначается гид
        @exception WorkWithClientFailed При ошибке бронирования или отсутствии персонала
        """
        travel_agent = ProcessClientChoice(self.agency.travel_agents).selected
        manager = ProcessClientChoice(self.agency.managers).selected
        available_tours = self.agency.get_avaiable_tours()
        manager.offer_tours_to_client(available_tours)
        picked_tour = ProcessClientChoice(available_tours).selected
        try: 
            travel_agent.book_tour_for_client(self.client, picked_tour, self.agency.bank_account)
        except Exception:
            raise WorkWithClientFailed()
        if len(picked_tour.sights) >= 1:
            guide = ProcessClientChoice(self.agency.guides).selected
            guide.go_to_tour(picked_tour)


class Route:
    """
    @brief Представляет маршрут клиента, состоящий из нескольких туров
    @details Позволяет рассчитать общую стоимость и получить строковое представление.
    """

    def __init__(self, client: Person, tours: List[Tour]):
        """
        @brief Конструктор маршрута
        @param client Владелец маршрута
        @param tours Список туров, включённых в маршрут
        """
        self.client = client
        self.tours = tours

    def get_total_cost(self) -> float:
        """
        @brief Рассчитывает общую стоимость всех туров в маршруте
        @return Сумма цен всех туров
        """
        return sum(tour.price for tour in self.tours)

    def __str__(self) -> str:
        """
        @brief Строковое представление маршрута
        @return Строка в формате:
            "Route for Имя: N tours, Total: X.XX"
        """
        return f"Route for {self.client.passport.name}: {len(self.tours)} tours, Total: {self.get_total_cost()}"


class TouristAgency:
    """
    @brief Туристическое агентство
    @details Управляет списком туров, персоналом (менеджеры, агенты, гиды)
    и взаимодействием с клиентами.
    """

    def __init__(self, name: str, bank_account: BankAccount):
        """
        @brief Конструктор туристического агентства
        @param name Название агентства
        @param bank_account Банковский счёт агентства
        """
        self.bank_account = bank_account
        self.name = name
        self.__available_tours: List[Tour] = []
        self.managers: List[Manager] = []
        self.travel_agents: List[TravelAgent] = []
        self.guides: List[Guide] = []

    def add_tour(self, tour: Tour):
        """
        @brief Добавляет тур в список доступных
        @param tour Объект Tour для добавления
        """
        self.__available_tours.append(tour)

    def add_guide(self, guide: Guide):
        """
        @brief Добавляет гида в штат агентства
        @param guide Объект Guide для добавления
        """
        self.guides.append(guide)

    def add_agent(self, agent: TravelAgent):
        """
        @brief Добавляет туристического агента в штат
        @param agent Объект TravelAgent для добавления
        """
        self.travel_agents.append(agent)

    def add_manager(self, manager: Manager):
        """
        @brief Добавляет менеджера в штат агентства
        @param manager Объект Manager для добавления
        """
        self.managers.append(manager)

    def get_tour_by_index(self, index: int) -> Tour:
        """
        @brief Возвращает тур по индексу
        @param index Индекс тура в списке
        @return Объект Tour
        @exception IndexError Если индекс выходит за границы списка
        """
        if 0 <= index < len(self.__available_tours):
            return self.__available_tours[index]
        else:
            raise IndexError("Tour index out of range")

    def get_avaiable_tours(self) -> List[Tour]:
        """
        @brief Возвращает список всех доступных туров
        @return Список объектов Tour
        """
        return self.__available_tours

    def interact_with_person(self, person: Person):
        """
        @brief Инициирует автоматизированное взаимодействие с клиентом
        @param person Клиент (Person)
        @exception WorkWithClientFailed При сбое в процессе обслуживания
        @note Создаётся объект WorkWithClient, который выполняет полный цикл бронирования
        """
        WorkWithClient(self, person)