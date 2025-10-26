from .visa import Visa
from datetime import date
from typing import Optional
class PassportIsExpired(Exception):
    def __init__(self):
        super().__init__("Passport is expired")
        
class Passport:
    def __init__(self,passport_num:str,name:str,surname:str,passport_expiration_date:date,visa: Optional[Visa] = None):
        
        self.visa = visa
        self.__passport_num = passport_num
        self.passport_expiration_date = passport_expiration_date
        self.name = name
        self.surname = surname
        if passport_expiration_date < date.today():
            raise PassportIsExpired()
    def set_visa(self,visa: Visa):
        self.visa = visa

    def __getattribute__(self,name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            print("Attribute not found")
            raise 

    
