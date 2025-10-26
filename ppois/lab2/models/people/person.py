from models.docs.passport import Passport
from services.bankAccount import BankAccount


class Person:
    def __init__(self,passport: Passport,bank_account:BankAccount,mood:int = 15):
        self.bank_account = bank_account
        self.passport = passport
        self.__mood = mood

    def __getattribute__(self,name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            print(f"attribute {name} not found")
            raise 

    def __check_mood(self):
        if self.__mood <=10:
            print("you are now sad, go make some activities")
        elif 10<=self.__mood<=20:
            print("you feel yourself fine")
        else:
            print("you feel very well") 
            
    def change_mood(self,mood_value):
        self.__mood += mood_value
        self.__check_mood()
        
    


    
        
    