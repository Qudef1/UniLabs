from datetime import date
from typing import List
from .geography import City
from people.person import Person as Client
from docs.visa import Visa
from .accomodation import Accomodation
from .transport import Transport
from services.services import Service


class TourAndVisaIncompatible(Exception):
    def __init__(self):
        super().__init__("Your visa is incompatible with this tour")
class EndAndStartDateError(Exception):
    def __init__(self):
        super().__init__("End date must be after the start date")

class Tour:
    def __init__(
        self,
        base_cost: float,  
        start_date: date,
        end_date: date,
        destination: City,
        commission_rate: float = 0.05,  
        accommodations: List[Accomodation] = None,
        transports: List[Transport] = None,
        services: List[Service] = None
    ):
        if end_date <= start_date:
            raise EndAndStartDateError()

        self.base_cost = base_cost
        self.start_date = start_date
        self.end_date = end_date
        self.destination = destination
        self.accommodations = accommodations or []
        self.transports = transports or []
        self.services = services or []
        self.commission_rate = commission_rate
        self.sights = []

        self.price = self._calculate_total_price()

    def _calculate_total_price(self) -> float:
        total = self.base_cost

        for trans in self.transports:
            hours = (trans.end_time - trans.start_time).total_seconds() / 3600
            total += trans.price_for_hour * hours

        for acc in self.accommodations:
            total += acc.price

        for service in self.services:
            total += service.price

        total += total * self.commission_rate

        return total

    def add_accommodation(self, accommodation: Accomodation):
        self.accommodations.append(accommodation)
        self.price = self._calculate_total_price() 
    

    def add_transport(self, transport: Transport):
        self.transports.append(transport)
        self.price = self._calculate_total_price()

    def add_service(self, service: Service):
        self.services.append(service)
        self.price = self._calculate_total_price()

    def add_sight(self, sight):
        if sight.city == self.destination:
            self.sights.append(sight)
        else:
            print(f"Sight is not in the tour destination: {self.destination}")

    def check_visa(self, client: Client):
        person_visa: Visa = client.passport.visa

        if person_visa.country != self.destination.country.name:
            raise TourAndVisaIncompatible()

        if not (self.start_date >= person_visa.issue_date and self.end_date <= person_visa.get_expiration_date()):
            raise TourAndVisaIncompatible()

        if not person_visa.is_valid():
            raise TourAndVisaIncompatible()

        print("Your visa is compatible with this tour")

    def book(self, client: Client) -> bool:
        try:
            self.check_visa(client)
        except TourAndVisaIncompatible as e:
            print(e)
            return False

        if client.bank_account.sum < self.price:
            print("Not enough money to book the tour.")
            return False

        client.bank_account.withdraw(self.price)
        print(f"Tour to {self.destination} booked successfully for {self.price:.2f}!")
        return True

    def get_total_duration(self) -> int:
        return (self.end_date - self.start_date).days

    def __str__(self):
        return (
            f"Tour to {self.destination}, "
            f"{self.start_date} - {self.end_date}, "
            f"Total Price: {self.price:.2f}, "
            f"Duration: {self.get_total_duration()} days"
        )

    def __getattr__(self, name):
        print("attribute not found")
        return None