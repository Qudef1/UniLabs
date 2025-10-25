from .tour import Tour
from .person import Person
from .staff import Guide, Manager, TravelAgent
from typing import List,Optional
import random


class TouristAgency:
    def __init__(self, name: str):
        self.name = name
        self.__available_tours: List[Tour] = []
        self.managers: List[Manager] = []
        self.travel_agents: List[TravelAgent] = []
        self.guides: List[Guide]
    def add_tour(self, tour: Tour):
        self.available_tours.append(tour)

    def add_guide(self,guide:Guide):
        self.guides.append(guide)

    def add_manager(self,manager: Manager):
        self.managers.append(manager)

    def get_tour_by_index(self, index: int) -> Tour:
        if 0 <= index < len(self.available_tours):
            return self.available_tours[index]
        else:
            raise IndexError("Tour index out of range")
    
    def get_avaiable_tours(self):
        return self.__available_tours
    def interact_with_person(self,person:Person):
        WorkWithClient(self,person)

class WorkWithClient:
    def __init__(self,agency:TouristAgency,client:Person):
        self.agency = agency
        self.client = client
        try: 
            self.__interact_with_person()
        except:
            raise WorkWithClientFailed()
        
    def __interact_with_person(self):
        travel_agent = ProcessClientChoice(self.agency.travel_agents)
        manager = ProcessClientChoice(self.agency.managers)
        available_tours = self.agency.get_avaiable_tours()
        manager.offer_tours_to_client(available_tours)
        picked_tour = ProcessClientChoice(self.__available_tours)
        if len(picked_tour.sights)>1:
            guide = ProcessClientChoice(self.agency.guides)
            guide.go_to_tour(picked_tour)

class WorkWithClientFailed(Exception):
    def __init__(self):
        super().__init__("work with client was failed")

class EmptyStaffListOrTours(Exception):
    def __init__(self):
        super().__init__(f"There aren`t any objects of this type in agency")

class ProcessClientChoice:
    def __init__(self,lst: Optional[List]=None):
        if lst == None:
            raise EmptyStaffListOrTours()
        self.lst = lst
    def __process_client_choice(self):
        return random.choice(self.lst)
    
class Route:
    def __init__(self, client: Person, tours: List[Tour]):
        self.client = client
        self.tours = tours

    def get_total_cost(self) -> float:
        return sum(tour.cost for tour in self.tours)
 
    def __str__(self):
        return f"Route for {self.client.passport.name}: {len(self.tours)} tours, Total: {self.get_total_cost()}"