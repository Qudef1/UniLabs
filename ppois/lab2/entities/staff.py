from datetime import datetime
from typing import List, Optional
from person import Person as Client
from booking import Booking
from tour import Tour
from geography import City
from tourist_agency import TouristAgency


class Employee:
    def __init__(self, employee_id: str, name: str, position: str, hire_date: datetime):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.hire_date = hire_date
        self.is_active = True

    def __str__(self):
        return f"Employee: {self.name}, Position: {self.position}, ID: {self.employee_id}"


class TravelAgent(Employee):
    def __init__(self, employee_id: str, name: str, hire_date: datetime, commission_rate: float = 0.05):
        super().__init__(employee_id, name, "Travel Agent", hire_date)
        self.commission_rate = commission_rate
        self.bookings_handled = 0

    def book_tour_for_client(self, client: Client, tour: Tour) -> Optional[Booking]:
        """Помогает клиенту забронировать тур"""
        if not tour.check_visa(client):
            print(f"{client.passport.name} does not have valid visa for {tour.destination.country.name}")
            return None
        if client.bank_account.sum < tour.price:  
            print(f"{client.passport.name} does not have enough money for tour.")
            return None

        client.bank_account.withdraw(tour.price)
        self.bookings_handled += 1
        print(f"Tour booked by agent {self.name} for {client.passport.name}. Commission: {tour.price * self.commission_rate:.2f}")
        return Booking(client)

    def __str__(self):
        return f"TravelAgent: {self.name}, Bookings handled: {self.bookings_handled}"


class Manager(Employee):
    def __init__(self, employee_id: str, name: str, hire_date: datetime, department: str):
        super().__init__(employee_id, name, "Manager", hire_date)
        self.department = department
        self.subordinates: List[Employee] = []

    def add_subordinate(self, emp: Employee):
        self.subordinates.append(emp)

    def view_team_status(self):
        print(f"Manager {self.name} manages {len(self.subordinates)} employees:")
        for emp in self.subordinates:
            print(f"- {emp}")

    def offer_tours_to_client(self, client: Client, agency: TouristAgency):
        """
        Предлагает туры пользователю из агентства
        """
        agency.list_available_tours()
        try:
            choice = int(input(f"{client.passport.name}, choose a tour (1-{len(agency.available_tours)}): ")) - 1
            selected_tour = agency.get_tour_by_index(choice)
            print(f"\nYou selected: {selected_tour}")
            print(f"Total price: {selected_tour.price:.2f}")
            confirm = input("Confirm booking? (y/n): ")
            if confirm.lower() == 'y':
                success = selected_tour.book(client)
                if success:
                    print("Booking successful!")
                else:
                    print("Booking failed.")
            else:
                print("Booking cancelled.")
        except (ValueError, IndexError):
            print("Invalid choice.")

    def __str__(self):
        return f"Manager: {self.name}, Department: {self.department}"


class Guide(Employee):
    def __init__(self, employee_id: str, name: str, hire_date: datetime, languages: List[str], city: City):
        super().__init__(employee_id, name, "Guide", hire_date)
        self.languages = languages
        self.city = city  # город, где работает гид
        self.is_available = True

    def assign_to_tour(self, tour: Tour) -> bool:
        """Проверяет, может ли гид вести тур в этом городе"""
        if not self.is_available or tour.destination != self.city:
            print(f"Guide {self.name} is not available or not assigned to {tour.destination}")
            return False
        self.is_available = False
        print(f"Guide {self.name} assigned to tour in {tour.destination}")
        return True

    def __str__(self):
        return f"Guide: {self.name}, Languages: {', '.join(self.languages)}, City: {self.city}"


class Salary:
    def __init__(self, base_salary: float, bonus: float = 0.0):
        self.base_salary = base_salary
        self.bonus = bonus

    def total_salary(self) -> float:
        return self.base_salary + self.bonus

    def __str__(self):
        return f"Base: {self.base_salary}, Bonus: {self.bonus}, Total: {self.total_salary()}"


class WorkSchedule:
    def __init__(self, employee: Employee, start_time: str, end_time: str, days: List[str]):
        self.employee = employee
        self.start_time = start_time  
        self.end_time = end_time      
        self.days = days              

    def __str__(self):
        return f"Schedule for {self.employee.name}: {', '.join(self.days)}, {self.start_time}-{self.end_time}"