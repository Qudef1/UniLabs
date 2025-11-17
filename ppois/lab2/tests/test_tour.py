import unittest
import sys
import os
from datetime import date, datetime, timedelta
from models.travel.geography import Country, City
from models.docs.passport import Passport,PassportIsExpired
from models.docs.visa import Visa,VisaNotAvailable,VisaNoEnabledEntries,VisaInvalidDate
from services.bank_account import BankAccount
from models.people.person import Person, ContactInfo
from models.travel.accomodation import Hotel,Hostel,Apartment,StartAndEndDateError,AccomodationNotFoundOrExpired,Accomodation
from models.travel.transport import Flight,Bus,Train,CarRental
from services.services import Insurance,LuggageService,VisaSupportService
from models.travel.tour import Tour, TourAndVisaIncompatible, EndAndStartDateError
from models.travel.tourist_agency import TouristAgency, Route
from models.people.staff import Guide,TravelAgent,Manager
from models.travel.booking import AccomodationBooking, FlightBooking
from models.people.billing import Address,Order,Payment,Review, BookingPolicy, CancellationPolicy



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
        hotel_info = str(hotel)
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
    
    def test_passport(self):
        passport = Passport("1111",
                            name="Tralalelo",
                            surname="Tralala",
                            passport_expiration_date=date(2030,1,1))
        passport.surname
        with self.assertRaises(PassportIsExpired):
            Passport("1234",name="trippi",surname="troppa",passport_expiration_date=date(2020,2,2))
        with self.assertRaises(AttributeError):
            passport.nane

    def test_visa(self):
        future_date = date.today() + timedelta(days=30)
        past_date = date.today() - timedelta(days=10)
        visa = Visa(
            visa_number="V123456",
            country="France",
            issue_date=date.today(),
            expiration_date=future_date,
            entry_count=2
        )
        self.assertEqual(visa.visa_number, "V123456")
        visa.activate()
        with self.assertRaises(AttributeError):
            visa.tutu
        self.assertTrue(visa.is_valid())
        self.assertEqual(visa.days_until_expiration(), 30)

        visa.use_entry()
        self.assertEqual(visa.used_entries, 1)
        self.assertTrue(visa.is_active)

        visa.use_entry()
        self.assertEqual(visa.used_entries, 2)
        self.assertFalse(visa.is_active)

        with self.assertRaises(VisaNotAvailable):
            visa.use_entry()

        with self.assertRaises(VisaInvalidDate):
            Visa(
                visa_number="V789",
                country="Italy",
                issue_date=past_date + timedelta(days=100),
                expiration_date=past_date,
                entry_count=1
            )
        
        with self.assertRaises(VisaNoEnabledEntries):
            Visa(
                visa_number="V123456",
                country="France",
                issue_date=date.today(),
                expiration_date=future_date,
                entry_count=0
            )
        
    def test_person_mood_and_attribute(self):
        self.client.passport.name
        with self.assertRaises(AttributeError):
            self.client.vivi
        self.client.change_mood(100)
        self.client.change_mood(0)
        self.client.change_mood(-15)

    def test_all_accomodation(self):
        start = date.today() + timedelta(days=1)
        end = date.today() + timedelta(days=5)
        acc = Apartment(
            start_date=start,
            end_date=end,
            location=self.city,
            price_per_night=100.0,
            bank_account=BankAccount(100000,"apartment_bank_account_123"),
            bedrooms=4
        )
        self.assertEqual(acc.price, 400.0)
        self.assertEqual(acc.location, self.city)
        str(acc)
        acc.book(self.bank)
        start -= timedelta(days=10)
        end -=timedelta(days = 20)
        with self.assertRaises(StartAndEndDateError):
            Hostel(
                start_date=start,
                end_date=end,
                location=self.city,
                price_per_night=100.0,
                bank_account=BankAccount(100000,"apartment_bank_account_123"),
                persons_for_room=3
            )
        end = date.today()
        start = end - timedelta(days=5)
        with self.assertRaises(AccomodationNotFoundOrExpired):
            Hostel(
                start_date=start,
                end_date=end,
                location=self.city,
                price_per_night=100.0,
                bank_account=BankAccount(100000,"apartment_bank_account_123"),
                persons_for_room=3
            )
    
    def test_tourist_agency_global(self):
        tourist_agency = TouristAgency("super_Tour",BankAccount(1000000000,"super_tour_bank_account_1233243"))
        tourist_agency.add_guide(guide=Guide("miguel_123","miguel",date(2020,12,3),["endglish","french","spanish"],city=self.city))
        tour = Tour(1000,
                    date.today()+timedelta(days=3),
                    date.today()+timedelta(days=20),
                    self.city,
                    0.05)
        acc = Apartment(
            start_date=date.today()+timedelta(days=4),
            end_date=date.today()+timedelta(days=19),
            location=self.city,
            price_per_night=10.0,
            bank_account=BankAccount(100000,"apartment_bank_account_123"),
            bedrooms=4
        )
        tour.add_accommodation(acc)
        tour.add_service(Insurance(coverage="Medical insurance", price=80.0))
        tour.add_service(VisaSupportService(price=50.0))
        tour.add_service(LuggageService(weight_kg=23, price=30.0))
        
        tour.add_transport(Flight(
            start_point=self.city,
            end_point=City("Brest", self.country),
            start_time=date.today() + timedelta(days=5, hours=10),
            end_time=date.today() + timedelta(days=5, hours=12),
            price=250.0,
            flight_number="AF789",
            class_type=1 
        ))
        tour.add_transport(Bus(
            start_point=City("Brest",self.country),
            end_point=self.city,
            start_time=date.today() + timedelta(days=8, hours=10),
            end_time=date.today() + timedelta(days=8, hours=13),
            price_for_hour=3.0,
            bus_number="BUS-456",
            bus_company=101
        ))
        tour.add_transport(Train(
            start_point=self.city,
            end_point=City("Brussels",self.country),
            start_time=date.today() + timedelta(days=10, hours=7),
            end_time=date.today() + timedelta(days=10, hours=12),
            price=40.,
            train_number="123321_train_to_brussels",
            class_type=1
        ))
        tour.add_booking(AccomodationBooking(self.client,acc))
        tourist_agency.add_tour(tour=tour)
        tourist_agency.add_manager(manager=Manager("Vito_manager_best","Vito corleone",date(1980,1,1)))
        tourist_agency.add_agent(TravelAgent("michael_corleone_id_123321","Michael",date(2000,12,12)))
        tourist_agency.interact_with_person(self.client)
        route = Route(self.client,[tour])
        print(str(route))

    def test_transport_and_booking(self):
        test_person = Person(Passport("234","Ozon","671games",date(2030,4,4)),BankAccount(999999999,"Den_2"),10000000)
        flight = Flight(
            start_point=City("Moscow", Country("Russia", "RU")),
            end_point=self.city,
            start_time=datetime(2025, 7, 10, 10, 0),
            end_time=datetime(2025, 7, 10, 12, 30),
            price=300.0,
            flight_number="SU123",
            class_type=1
        )
        flight.book(test_person)
        print(str(flight))
        maseratti = CarRental(self.city,1.2,"maseratti",datetime(2027,2,21,13),datetime(2027,2,22,12))
        maseratti.rent(test_person)
        print(str(maseratti))
        booking_temp = FlightBooking(test_person,flight=flight)
        booking_temp.confirm()
        booking_temp.cancel()

    def test_billing_order_and_payment(self):
        tour = Tour(
            base_cost=500.0,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=10),
            destination=self.city,
        )
        order = Order(self.client, tour)
        invoice = order.place()
        receiver = BankAccount(0.0, "RECV_ACC")
        payment = Payment(invoice=invoice, payer=self.client.bank_account, receiver=receiver)
        processed = payment.process()
        self.assertTrue(processed)
        self.assertTrue(invoice.paid)
        self.assertIsNotNone(payment.paid_date)

    def test_billing_address_contact_review_policy(self):
        addr = Address("Lenina 1", "Moscow", "Russia", "101000")
        self.assertIn("Lenina", addr.full_address())

        contact = ContactInfo("a@example.com", "+70000000000")
        self.assertIn("@example.com", contact.formatted())

        
        tour = Tour(
            base_cost=200.0,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            destination=self.city,
        )
        review = Review(self.client, tour, rating=5, comment="Great!")
        review.publish()

        booking = AccomodationBooking(self.client, Accomodation(
            start_date=date.today()+timedelta(days=2),
            end_date=date.today()+timedelta(days=4),
            location=self.city,
            price_per_night=10.0
        ))
        bp = BookingPolicy("default")
        self.assertTrue(bp.is_allowed(booking))

        cp = CancellationPolicy("std", penalty_rate=0.05)
        penalty = cp.calculate_penalty(booking)
        self.assertIsInstance(penalty, float)

        
if __name__ == '__main__':
    unittest.main()


# coverage run -m unittest discover -s tests -p "test_*.py"

# coverage report -m