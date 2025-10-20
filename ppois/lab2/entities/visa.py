from datetime import date

class VisaExpiredDate(Exception):
    def __init__(self,visa_number:str,expiration_date:date):
        super().__init__(f"Visa {visa_number} has expired on {expiration_date}")

class VisaNoEnabledEntries(Exception):
    def __init__(self):
        super().__init__(f"You have already used all your entries on this visa.")

class VisaNotAvailable(Exception):
    def __init__(self):
        super().__init__("Your visa is not available.")

class VisaInvalidDate(Exception):
    def __init__(self):
        super().__init__("Expiration date Error")

class Visa:
    pass

class Visa:
    def __init__(self,visa_number:str,country:str,issue_date:date,expiration_date:date,
                 entry_count:int=1):
        if expiration_date <= issue_date:
            raise VisaInvalidDate()
        if entry_count<=0:
            raise VisaNoEnabledEntries()
        self.visa_number = visa_number
        self.country = country
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        self.entry_count = entry_count
        self.used_entries = 0
        self.is_active = True

    def is_expired(self) -> bool:
        return date.today()>self.expiration_date

    def is_valid(self) -> bool:
        return not self.is_expired() and self.is_active and self.used_entries < self.entry_count
    def days_until_expiration(self) -> int:
        if self.is_expired():
            return 0
        return int((self.expiration_date - date.today()).days)
    

    def activate(self):
        self.is_active = True
    def deactivate(self):
        self.is_active = False

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            raise f"attribute {name} not found"

        

    def use_entry(self) -> None:
        """Использовать один въезд по визе"""
        if not self.is_valid():
            raise VisaNotAvailable()
        if self.is_expired():
            raise VisaExpiredDate(self.visa_number,self.expiration_date)
        if self.used_entries >= self.entry_count:
            raise VisaNoEnabledEntries()
        
        self.used_entries += 1
        
        
        if self.used_entries >= self.entry_count:
            self.deactivate()

    def get_expiration_date(self) -> date:
        return self.expiration_date
    
    


        