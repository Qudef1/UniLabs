import visa as v
from datetime import date
class PassportIsExpired(Exception):
    def __init__(self):
        super().__init__("Passport is expired")
class Passport:
    def __init__(self,passport_num:str,name:str,surname:str,passport_expiration_date:v.date):
        
        self.visa = v.Visa("0","Belarus",date.today(),passport_expiration_date,1000)
        self.passport_num = passport_num
        self.passport_expiration_date = passport_expiration_date
        self.name = name
        self.surname = surname
        if passport_expiration_date < self.visa.get_expiration_date() or passport_expiration_date < v.date.today():
            raise PassportIsExpired()
    def set_visa(self,visa: v.Visa):
        self.visa = visa

    def __getattr__(self,name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            print("attribute not found")

    
        