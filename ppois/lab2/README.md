# Туристическое агентство листинг классов
    
Passport 5 3 -> Visa, PassportIsExpired

Visa 7 9 -> VisaExpiredDate, VisaNoEnabledEntries,VisaNotAvailable,VisaInvalidDate

Person 3 4 -> Passport, BankAccount, ContactInfo

Salary 2 3 -> 

WorkSchedule 4 2 -> Employee

Employee 5 2 -> Salary, WorkSchedule

Salary 2 3 ->

WorkSchedule 4 2 -> Salary, WorkSchedule

TravelAgent 8 4 -> Booking, BankAccount, Salary, WorkSchedule, 
BookingTourFailed

Manager 6 4 -> Salary, WorkSchedule

Guide 8 5 -> City, Salary, WorkSchedule, EmployeeIsUnavailable


Accomodation 6 3 -> BankAccount, StartAndEndDateError, 
AccomodationNotFoundOrExpired

Hotel 6 3 -> Accomodation

Hostel 6 3 -> Accomodation

Apartment 6  3 -> Accomodation

Booking 4 5 -> Person

FlightBooking 2 2 -> Flight, Booking

AccomodationBooking 1 2 -> Accomodation, Booking

Country 3 5 ->

City 2 3 -> Country

Sight 3 2 -> City

Tour 11 12 -> City, Accomodation, Transport, Service, Booking, Sight, TourAndVisaIncompitable, StartAndEndDateError

ProcessClientChoice 2 2 ->

WorkWithClient 2 2 -> TouristAgency, Person, WorkWithClientFailed, ProcessClientChoice

Route 2 3 -> Person, Tour

TouristAgency 6 8 -> TravelAgent, Manager, Guide, Tour, BankAccount, WorkWithClient

TourFiltration 2 7 -> Person, Tour

Transport 6 3 -> BankAccount

Flight 1 2 -> Transport

Train 1 3 -> Transport

Bus 2 4 -> Transport

CarRental 8 3 -> Transport, Person, BankAccount

Service 2 2 -> Person

Insurance 1 2 -> Service

VisaSupportService 1 2 -> Service

LuggageService 1 2 -> Service 

Transaction 4 4 -> BankAccount, NotEnoughMoney

BankAccount 2 5 -> Transaction, NotEnoughMoney


Address 4 1 -> Person, TouristAgency, Accomodation

ContactInfo 2 1 -> Person

Invoice 5 3 -> Booking, BankAccount

Payment 4 1 -> Invoice, BankAccount

Order 4 2 -> Person, Tour

Review 5 1 -> Person, Tour

BookingPolicy 2 1 -> Booking

CancellationPolicy 3 1 -> Booking

## Исключения:

PassportIsExpired 0 1 ->

VisaExpiredDate 0 1 ->

VisaNoEnabledEntries 0 1 ->

VisaNotAvailable 0 1 ->

VisaInvalidDate 0 1 ->

AccomodationNotFoundOrExpired 0 1 ->

StartAndEndDateError 0 1 ->

EmployeeIsUnavailable 0 1 ->

BookingTourFailed 0 1 ->

TourAndVisaIncompatible 0 1 ->

EndAndStartDateError 0 1 ->

EmptyStaffListOrTours 0 1 ->

WorkWithClientFailed 0 1 ->

NotEnoughMoney 0 1 ->

PassportIsExpired 0 1 ->

### Итоги: 

Классы: 61

Поля: 170

Методы: 90

Ассоциации: 30+

Исключения: 15
