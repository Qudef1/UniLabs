from datetime import datetime
from typing import List, Optional
from person import Person
from transport import Transport, Flight, CarRental
from accomodation import Accomodation
from tour import Tour
from bankAccount import Transaction,NotEnoughMoney


class Booking:
    def __init__(self, person: Person, booking_date: datetime = None):
        self.person = person
        self.booking_date = booking_date or datetime.now()
        self.is_confirmed = False
        self.booking_id = self.generate_booking_id()

    def generate_booking_id(self) -> str:
        return f"BOOK_{self.person.bank_account.id}_{self.booking_date.strftime('%Y%m%d%H%M%S')}"

    def confirm(self) -> bool:
        self.is_confirmed = True
        print(f"Booking {self.booking_id} confirmed.")
        return True

    def cancel(self) -> bool:
        if not self.is_confirmed:
            print("Booking is not confirmed yet.")
            return False
        self.is_confirmed = False
        print(f"Booking {self.booking_id} cancelled.")
        return True

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Confirmed: {self.is_confirmed}"


class FlightBooking(Booking):
    def __init__(self, person: Person, flight: Flight):
        super().__init__(person)
        self.flight = flight
        self.is_confirmed = self.flight.book(person) 
    def __str__(self):
        return f"Flight Booking: {self.booking_id} | {self.flight}"


class AccomodationBooking(Booking):
    def __init__(self, person: Person, accommodation: Accomodation):
        super().__init__(person)
        self.accommodation = accommodation
        if self.is_confirmed:
            try:
                Transaction(person.bank_account,accommodation.bank_account,accommodation.price)
            except NotEnoughMoney:
                print("not enough money to rent this accomodation")

    def __str__(self):
        return f"Hotel Booking: {self.booking_id} | {self.accommodation}"


class TourBooking(Booking):
    def __init__(self, person: Person, tour: Tour):
        super().__init__(person)
        self.tour = tour
        self.is_confirmed = self.tour.check_visa(person) and person.bank_account.sum >= tour.cost
        if self.is_confirmed:
            person.bank_account.withdraw(tour.cost)

    def __str__(self):
        return f"Tour Booking: {self.booking_id} | Tour to {self.tour.destination}"