import passport
import bankAccount
from datetime import date

class Person:
    def __init__(self,passport: passport.Passport,bank_account:bankAccount.BankAccount):
        self.bank_account = bank_account
        self.passport = passport
    def __getattr__(self,name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            print("attribute not found")
    

if __name__ == "__main__":
    passport_temp = passport.Passport("1232","BOBa","huu",date(2025,12,21))
    visa = passport.v.Visa("111","Poland",date(2025,11,10),date(2025,12,21))
    passport_temp.set_visa(visa)
    bank_account = bankAccount.BankAccount(10000.0,"BOBaHuu1232")
    person = Person(passport_temp,bank_account)
    print(person.passport.visa.expiration_date)
    
        
    