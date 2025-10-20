from datetime import date 
from visa import Visa

class Country:
    def __init__(self,name:str,code:str,visa_required:bool=True):
        self.name = name
        self.__code = code
        self.visa_required = visa_required

    def get_code(self) -> str:
        return self.__code
    
    def compare(self,other) -> bool:
        if isinstance(other,Country):
            return self.__code == other.get_code() and self.name == other.name
        return False
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            raise f"attribute {name} not found"
    def __str__(self):
        return f"{self.name}, {self.__code}, visa required = {self.visa_required}"
    
    
    
        
    
class City:
    def __init__(self,name:str,country:Country):
        self.name = name
        self.country = country
    
    def compare(self,other):
        if isinstance(other,City):
            return other.name == self.name and other.country == self.country
    def __str__(self):
        return f"{self.name}"

class Sight:
    def __init__(self,name,country:Country,city:City):
        self.name = name
        self.country = country
        self.city = city

    def visit(self):
        print("sight info")
        
        
        

        