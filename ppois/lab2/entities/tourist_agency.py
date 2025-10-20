from .tour import Tour
from .person import Person
from .staff import Guide, Manager, TravelAgent
from typing import List
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
        
    def interact_with_person(self,person:Person):
        travel_agent = random.choice(self.travel_agents)
        manager = random.choice(self.managers)
        manager.offer_tours_to_client(self.__available_tours)
        picked_tour = random.choice(self.__available_tours)
        travel_agent.book_tour_for_client(person,picked_tour)
        if len(picked_tour.sights)>0:
            guide = random.choice(self.guides)
            guide.go_to_tour(picked_tour)

        



class Route:
    def __init__(self, client: Person, tours: List[Tour]):
        self.client = client
        self.tours = tours

    def get_total_cost(self) -> float:
        return sum(tour.cost for tour in self.tours)
 
    def __str__(self):
        return f"Route for {self.client.passport.name}: {len(self.tours)} tours, Total: {self.get_total_cost()}"