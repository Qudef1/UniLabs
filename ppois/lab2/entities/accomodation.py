import datetime as dt
from typing import Optional
from .geography import City
from .bankAccount import BankAccount, Transaction, NotEnoughMoney

class AccomodationNotFoundOrExpired(Exception):
    def __init__(self):
        super().__init__("Accomodation not found or expired")
class StartAndEndDateError(Exception):
    def __init__(self):
        super().__init__("start date must be before end date")
class Accomodation:
    def __init__(self,start_date=dt.date.today(),end_date=dt.date.today(),location:Optional[City]=0, 
                 price_per_night: float=0.0,bank_account:Optional[BankAccount]=None):
        self.start_date = start_date
        self.end_date = end_date
        self.price = price_per_night*(end_date-start_date).days
        self.price_per_night = price_per_night
        self.location = location
        self.bank_account = bank_account
        if start_date>=end_date:
            raise StartAndEndDateError()
        if self.end_date == dt.date.today():
            raise AccomodationNotFoundOrExpired()  
    def __getattr__(self, name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            print("attribute not found")
    def book(self,client_bank_account: BankAccount):
        total_price = self.price
        try:
            Transaction(client_bank_account,self.bank_account,total_price)
            return True
        except NotEnoughMoney:
            return False
        


    
class Hotel(Accomodation):
    def __init__(self,start_date=dt.date.today(),end_date=dt.date.today(),location:Optional[City]=0, 
                 price_per_night: float=0.0,bank_account:Optional[BankAccount]=None,stars=1):
        super().__init__(start_date, end_date, location, price_per_night, bank_account)
        self.star_rating = stars
        self.services = ["Bedroom","Breakfast","Room Service"]

    def add_service(self,service:str):
        self.services.append(service)
    def __str__(self):
        return f"Hotel in {self.location}, {self.star_rating}-star, services {', '.join(self.services)}, price: {self.price_per_night}/night"

class Hostel(Accomodation):
    def __init__(self,start_date=dt.date.today(),end_date=dt.date.today(),location:Optional[City]=0, 
                 price_per_night: float=0.0,bank_account:Optional[BankAccount]=None,persons_for_room=2):
        super().__init__(start_date, end_date, location, price_per_night, bank_account)
        self.persons_for_room = persons_for_room
    
    def __str__(self):
        return f"Hostel in {self.location}, price: {self.price_per_night}/night, {self.persons_for_room} persons in one room"


class Apartment(Accomodation):
    def __init__(self,start_date=dt.date.today(),end_date=dt.date.today(),location:Optional[City]=0, 
                 price_per_night: float=0.0,bank_account:Optional[BankAccount]=None, bedrooms = 1):
        super().__init__(start_date, end_date, location, price_per_night, bank_account)
        self.bedrooms = bedrooms

    def __str__(self):
        return f"Hostel in {self.location}, price: {self.price_per_night}/night, has {self.bedrooms} bedrooms"


        


