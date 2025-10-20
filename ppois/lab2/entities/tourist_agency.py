from tour import Tour
from person import Person
from typing import List


class TouristAgency:
    def __init__(self, name: str):
        self.name = name
        self.available_tours: List[Tour] = []

    def add_tour(self, tour: Tour):
        self.available_tours.append(tour)

    def list_available_tours(self):
        print(f"\nAvailable tours in {self.name}:")
        for i, tour in enumerate(self.available_tours):
            print(f"{i+1}. {tour}")

    def get_tour_by_index(self, index: int) -> Tour:
        if 0 <= index < len(self.available_tours):
            return self.available_tours[index]
        else:
            raise IndexError("Tour index out of range")



class Itinerary:
    def __init__(self, client: Person, tours: List[Tour]):
        self.client = client
        self.tours = tours

    def get_total_cost(self) -> float:
        return sum(tour.cost for tour in self.tours)
 
    def __str__(self):
        return f"Itinerary for {self.client.passport.name}: {len(self.tours)} tours, Total: {self.get_total_cost()}"