import unittest
import sys
import os
from datetime import date, datetime
from entities.geography import Country, City
from entities.passport import Passport
from entities.visa import Visa
from entities.bankAccount import BankAccount
from entities.person import Person
from entities.accomodation import Hotel
from entities.transport import Flight
from entities.services import Insurance
from entities.tour import Tour, TourAndVisaIncompatible, EndAndStartDateError

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestTour(unittest.TestCase):

    def setUp(self):
        self.country = Country("France", "FR")
        self.city = City("Paris", self.country)
        self.visa = Visa("V123", "France", date(2025, 1, 1), date(2025, 12, 31), 2)
        self.passport = Passport("P987", "Alice", "Smith", date(2030, 1, 1))
        self.passport.set_visa(self.visa)
        self.bank = BankAccount(10000.0, "ALICE123")
        self.client = Person(self.passport, self.bank)

    def test_tour_creation(self):
        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destination=self.city
        )
        self.assertEqual(tour.base_cost, 1000.0)
        self.assertEqual(tour.destination, self.city)
        self.assertEqual(tour.price, 1050.0)  

    def test_tour_creation_invalid_dates(self):
        with self.assertRaises(EndAndStartDateError):
            Tour(
                base_cost=1000.0,
                start_date=date(2025, 7, 20),
                end_date=date(2025, 7, 10),
                destination=self.city
            )

    def test_tour_price_includes_transport(self):
        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destination=self.city
        )

        flight = Flight(
            start_point=City("Moscow", Country("Russia", "RU")),
            end_point=self.city,
            start_time=datetime(2025, 7, 10, 10, 0),
            end_time=datetime(2025, 7, 10, 12, 30),
            price=300.0,
            flight_number="SU123",
            class_type=1
        )
        tour.add_transport(flight)

        
        expected = 1750 * 1.05
        self.assertAlmostEqual(tour.price, expected, places=2)

    def test_tour_price_includes_accommodation(self):
        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 15),  
            destination=self.city
        )

        hotel = Hotel(
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 15),
            location=self.city,
            price_per_night=200.0
        )
        tour.add_accommodation(hotel)

        
        expected = 2000 * 1.05
        self.assertAlmostEqual(tour.price, expected, places=2)

    def test_tour_price_includes_service(self):
        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destination=self.city
        )

        insurance = Insurance("Health", 100.0)
        tour.add_service(insurance)

        
        expected = 1100 * 1.05
        self.assertAlmostEqual(tour.price, expected, places=2)

    def test_check_visa_compatible(self):
        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destination=self.city
        )
        
        tour.check_visa(self.client)

    def test_check_visa_incompatible_country(self):
        visa = Visa("V456", "Germany", date(2025, 1, 1), date(2025, 12, 31), 2)
        passport = Passport("P999", "Bob", "Jones", date(2030, 1, 1))
        passport.set_visa(visa)
        bank = BankAccount(5000.0, "BOB999")
        client = Person(passport, bank)

        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destination=self.city
        )
        with self.assertRaises(TourAndVisaIncompatible):
            tour.check_visa(client)

    def test_book_tour_success(self):
        tour = Tour(
            base_cost=1000.0,
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destination=self.city
        )
        initial_balance = self.client.bank_account.sum
        result = tour.book(self.client)
        self.assertTrue(result)
        expected_spent = tour.price
        self.assertEqual(self.client.bank_account.sum, initial_balance - expected_spent)

    def test_book_tour_insufficient_funds(self):
        tour = Tour(
            base_cost=100000.0,  
            start_date=date(2025, 7, 10),
            end_date=date(2025, 7, 20),
            destintion=self.city
        )
        result = tour.book(self.client)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()