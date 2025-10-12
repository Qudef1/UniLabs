import passport
import bankAccount
class Person:
    def __init__(self,passport: passport.Passport,bank_account:bankAccount.BankAccount):
        self.bank_account = bank_account
        self.passport = passport

    