from datetime import datetime

class BankAccount:
    def __init__(self,sum:float,id:str):
        self.sum = sum
        self.id = id

    def make_transaction(self,other,price:float):
        try:
            self.transaction = Transaction(self,other,price)
            print(f"transaction {self.transaction.transaction_number} has successfully processed")
        except NotEnoughMoney:
            raise NotEnoughMoney()

    def withdraw(self,price):
        if self.sum - price>0:
            self.sum -= price
            
    def transfer(self,price):
        self.sum += price
    
    def get_sum(self):
        return self.sum
        
class NotEnoughMoney(Exception):
    def __init__(self):
        super().__init__("Not enough money. Transaction Failed")

class Transaction:
    def __init__(self,bank_sender:BankAccount,bank_receiver:BankAccount,price:float):
        self.price = price
        self.sender = bank_sender
        self.receiver = bank_receiver
        self.transaction_number = (bank_sender.id+"_"+bank_receiver.id+"_"+datetime.now().strftime("%Y%m%d%H%M%S"))
        self.process_transaction()
        

    def process_transaction(self):
        if (self.sender.sum - self.price*1.03<0):
            raise NotEnoughMoney()
        
        self.sender.withdraw(self.price*1.03) 
        self.receiver.transfer(self.price)

    def get_transaction_number(self):
        return self.transaction_number
    def __str__(self):
        return self.transaction_number

            

    