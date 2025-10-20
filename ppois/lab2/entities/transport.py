from datetime import datetime, timedelta
from typing import Optional
from .geography import City
from .person import Person
from .bankAccount import BankAccount,Transaction,NotEnoughMoney
from random import randint

class Transport:
    def __init__(self,start_point:City,end_point:City,start_time:datetime,
                 end_time: datetime,price_for_hour:float,company_bank_account:Optional[BankAccount]=None):
        self.start_point = start_point
        self.end_point = end_point
        self.start_time = start_time
        self.end_time = end_time
        self.price_for_hour = price_for_hour
        self.bank_account = company_bank_account

    def book(self,person: Person):
        try:
            Transaction(person.bank_account,self.bank_account,self.price_for_hour*(self.end_time-self.start_time).total_seconds()/3600.)
        except NotEnoughMoney:
            print("not enough money to book transport")
            return False
        return True

    def __str__(self):
        return f"{self.__class__.__name__}: {self.start_point} - {self.end_point}, duration {(self.end_time-self.start_time).total_seconds()/3600.} hours"
    
class Flight(Transport):
    def __init__(
        self, start_point: City, end_point: City, start_time: datetime, end_time: datetime, 
        price: float, flight_number: str, class_type: int
    ):
        super().__init__(
            start_point,
            end_point,
            start_time,
            end_time,
            price*class_type
        )
        self.flight_number = flight_number
    
    def __str__(self):
        return f"Flight {self.flight_number}, {self.start_point} - {self.end_point}, duration {(self.end_time-self.start_time).total_seconds()/3600.} hours"
    
    

class Train(Transport):
    def __init__(
        self, start_point: City, end_point: City, start_time: datetime, end_time: datetime, 
        price: float, train_number: str, class_type: int
    ):
        super().__init__(
            start_point,
            end_point,
            start_time,
            end_time,
            price*class_type/2
        )
        self.train_number = train_number

    def __str__(self):
        return f"Train {self.train_number}, {self.start_point} - {self.end_point}, duration {(self.end_time-self.start_time).total_seconds()/3600.} hours"

    def stuck_at_border(self):
        self.end_time = self.end_time + timedelta(hours = randint(2,24))
    

class Bus(Transport):
    def __init__(
        self, start_point: City, end_point: City, start_time: datetime, end_time: datetime, 
        price_for_hour: float, bus_number: str, bus_company: int
    ):
        super().__init__(
            start_point,
            end_point,
            start_time,
            end_time,
            price_for_hour
        )
        self.bus_number = bus_number
        self.bus_company = bus_company

    def __str__(self):
        return f"Bus {self.bus_number}, {self.bus_number}, {self.start_point} - {self.end_point}, duration {(self.end_time-self.start_time).total_seconds()/3600.} hours"
    
    def puncture_tire(self):
        self.end_time = self.end_time + timedelta(hours=3)

    def stuck_at_border(self):
        self.end_time = self.end_time + timedelta(hours = randint(2,24))


class CarRental:
    def __init__(
        self,
        city: City,
        price_per_hour: float,
        car_model: str,
        start_date: datetime,
        end_date: datetime
    ):
        self.city = city
        self.price_per_hour = price_per_hour
        self.car_model = car_model
        self.start_date = start_date
        self.end_date = end_date
        self.is_rented = False
        self.total_price = (end_date - start_date).total_seconds()/3600.*price_per_hour
        self.rental_service_bank_account = BankAccount(100000,f"{car_model}_{price_per_hour}")

    def rent(self, person: Person) -> bool:
        if self.is_rented:
            print(f"{self.car_model} is already rented")
            return False
        try:
            Transaction(person.bank_account,self.rental_service_bank_account,self.total_price)
        except NotEnoughMoney():
            print("Not enough money")
            return False

        self.is_rented = True
        print(f"Car {self.car_model} rented in {self.city} for {self.total_price:.2f}")
        return True

    def __str__(self):
        return f"CarRental: {self.car_model} in {self.city}, {self.total_price:.2f} total"




    



       

