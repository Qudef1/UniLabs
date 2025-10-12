import visa as v
class PassportIsExpired(Exception):
    def __init__(self):
        super().__init__("Passport is expired")
class Passport:
    def __init__(self,visa: v.Visa,passport_num:str,name:str,surname:str,passport_expiration_date:v.date):
        
        self.visa = visa
        self.passport_num = passport_num
        self.passport_expiration_date = passport_expiration_date
        self.name = name
        self.surname = surname
        if passport_expiration_date < visa.get_expiration_date() or passport_expiration_date > v.date.today():
            raise PassportIsExpired()
    def set_visa(self,visa: v.Visa):
        self.visa = visa

    
        