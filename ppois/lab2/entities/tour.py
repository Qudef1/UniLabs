import person
from datetime import date

class Tour:
    def __init__(self,cost:float,start_date:date,end_date:date,country:str):
        self.cost = cost
        self.start_date = start_date
        self.end_date = end_date
        self.country = country
    def check_visa(self,person:person.Person):
        person_visa = person.passport.visa
        
        
    def __getattr__(self,name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            print("attribute not found")