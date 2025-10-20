from .person import Person
from .bankAccount import BankAccount, Transaction, NotEnoughMoney
from .geography import City



class Service:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def book(self, client: Person) -> bool:
        try:
            Transaction(client.bank_account, BankAccount(10000, f"SERVICE_{self.name}"), self.price)
            print(f"Service '{self.name}' booked for {client.passport.name}")
            return True
        except NotEnoughMoney:
            print("Not enough money to book service")
            return False


class Insurance(Service):
    def __init__(self, coverage: str, price: float):
        super().__init__("Travel Insurance", price)
        self.coverage = coverage 

    def claim(self):
        print(f"Claim submitted for {self.coverage} insurance")


class VisaSupportService(Service):
    def __init__(self, price: float):
        super().__init__("Visa Support", price)

    def assist(self, client: Person, country: str):
        print(f"Visa support provided for {client.passport.name} to {country}")
    
    
class LuggageService(Service):
    def __init__(self, weight_kg: int, price: float):
        super().__init__("Luggage Service", price)
        self.weight_kg = weight_kg

    def send_luggage(self, from_city: City, to_city: City):
        print(f"Luggage ({self.weight_kg} kg) sent from {from_city} to {to_city}")


