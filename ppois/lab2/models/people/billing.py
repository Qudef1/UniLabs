from datetime import datetime, date
from typing import List, Optional
from models.travel.booking import Booking
from models.people.person import Person
from models.travel.tour import Tour
from services.bank_account import BankAccount, Transaction, NotEnoughMoney


class Address:
    """
    @brief Адрес.
    @details Используется в классах Person, TouristAgency, Accomodation.
    """

    def __init__(self, street: str, city: str, country: str, postal_code: str = ""):
        """
        @brief Конструктор адреса.
        @param street Улица.
        @param city Город.
        @param country Страна.
        @param postal_code Почтовый индекс.
        """
        self.street = street
        self.city = city
        self.country = country
        self.postal_code = postal_code

    def full_address(self) -> str:
        """
        @brief Возвращает полный адрес в формате строки.
        @return Строка вида "Street,од контактных данных.
        @return Строка вида "email / phone".
        """
        return f"{self.street} / {self.city} / {self.country} / {self.postal_code}"

class Invoice:
    """
    @brief Счёт за бронирование.
    @details Связан с Booking и BankAccount. Используется для оплаты заказов.
    """
    
    def __init__(self, booking: Booking, issuer_account: BankAccount, amount: float):
        """
        @brief Создаёт новый счёт.
        @param booking Объект бронирования.
        @param issuer_account Банковский аккаунт, выставляющий счёт.
        @param amount Сумма к оплате.
        """
        self.invoice_id = self.generate_id(booking)
        self.booking = booking
        self.issuer_account = issuer_account
        self.amount = amount
        self.issued_date = datetime.now()
        self.paid = False

    def generate_id(self, booking: Booking) -> str:
        """
        @brief Генерирует уникальный ID счёта.
        @param booking Бронирование, к которому привязан счёт.
        @return Строка ID.
        """
        return f"INV_{booking.booking_id}_{int(datetime.now().timestamp())}"

    def mark_paid(self):
        """
        @brief Помечает счёт как оплаченный.
        """
        self.paid = True

    def send(self, recipient: Person) -> None:
        """
        @brief Отправляет счёт получателю.
        @details В реальной системе — по email; здесь — вывод в лог.
        @param recipient Получатель счёта.
        """
        print(f"Invoice {self.invoice_id} sent to {recipient.passport.name}")


class Payment:
    """
    @brief Платёж, связанный со счетом (Invoice).
    @details Проводится между BankAccount payer -> receiver.
    """

    def __init__(self, invoice: Invoice, payer: BankAccount, receiver: BankAccount):
        """
        @brief Создаёт платёж.
        @param invoice Связанный счёт.
        @param payer Аккаунт плательщика.
        @param receiver Аккаунт получателя.
        """
        self.payment_id = f"PAY_{invoice.invoice_id}_{int(datetime.now().timestamp())}"
        self.invoice = invoice
        self.payer = payer
        self.receiver = receiver
        self.amount = invoice.amount
        self.paid_date: Optional[datetime] = None

    def process(self) -> bool:
        """
        @brief Проводит платёж.
        @details Реализует логику перевода денег через Transaction.
        @return True если успешно, иначе False.
        @exception NotEnoughMoney Недостаточно средств на счёте.
        """
        try:
            Transaction(self.payer, self.receiver, self.amount)
            self.paid_date = datetime.now()
            self.invoice.mark_paid()
            print(f"Payment {self.payment_id} processed for {self.amount}")
            return True
        except NotEnoughMoney:
            print("Payment failed: not enough money")
            return False


class Order:
    """
    @brief Заказ тура.
    @details Ассоциации: Order → Tour, Order → Person, Order → Invoice.
    """

    def __init__(self, person: Person, tour: Tour):
        """
        @brief Создаёт новый заказ.
        @param person Покупатель.
        @param tour Выбранный тур.
        """
        self.order_id = f"ORDER_{person.passport.name}_{int(datetime.now().timestamp())}"
        self.person = person
        self.tour = tour
        self.created_at = datetime.now()
        self.status = "created"

    def place(self) -> Invoice:
        """
        @brief Размещает заказ и создаёт счёт.
        @return Созданный объект Invoice.
        """
        # Import Booking here to avoid circular import at module import time
        from models.travel.booking import Booking

        invoice = Invoice(
            booking=Booking(self.person),
            issuer_account=self.person.bank_account,
            amount=self.tour.price
        )
        print(f"Order {self.order_id} placed, invoice {invoice.invoice_id} created")
        return invoice

    def cancel(self) -> None:
        """
        @brief Отменяет заказ.
        @note Статус устанавливается в cancelled.
        """
        self.status = "cancelled"
        print(f"Order {self.order_id} cancelled")


class Review:
    """
    @brief Отзыв клиента о туре или жилье.
    @details Ассоциации: Review → Person, Review → Tour/Accomodation.
    """

    def __init__(self, author: Person, target: Optional[Tour] = None, rating: int=1, comment: str = ""):
        """
        @brief Создаёт отзыв.
        @param author Автор отзыва.
        @param target Объект, о котором отзыв (Tour или Accomodation).
        @param rating Оценка 1–5.
        @param comment Текст комментария.
        """
        self.review_id = f"REV_{author.passport.name}_{int(datetime.now().timestamp())}"
        self.author = author
        self.target = target
        self.rating = rating
        self.comment = comment
        self.date = date.today()

    def publish(self) -> None:
        """
        @brief Публикует отзыв.
        """
        return f"Review {self.review_id} by {self.author.passport.name}: {self.rating}/5 - {self.comment}"


class BookingPolicy:
    """
    @brief Набор правил бронирования.
    @details Может использоваться как стратегия валидации Booking.
    """

    def __init__(self, name: str, rules: Optional[List[str]] = None):
        """
        @brief Создаёт политику бронирования.
        @param name Название политики.
        @param rules Список правил.
        """
        self.name = name
        self.rules = rules or []

    def is_allowed(self, booking: Booking) -> bool:
        """
        @brief Проверяет, разрешено ли бронирование.
        @details Демоверсия: всегда True.
        @param booking Бронирование.
        @return True если разрешено.
        """
        return True


class CancellationPolicy:
    """
    @brief Политика отмены бронирования.
    @details Используется для расчёта штрафов.
    """

    def __init__(self, name: str, penalty_rate: float = 0.1, allow_until_days_before: int = 7):
        """
        @brief Создаёт политику отмен.
        @param name Название политики.
        @param penalty_rate Процент штрафа.
        @param allow_until_days_before Кол-во дней до начала услуги, когда отмена разрешена.
        """
        self.name = name
        self.penalty_rate = penalty_rate
        self.allow_until_days_before = allow_until_days_before

    def calculate_penalty(self, booking: Booking) -> float:
        """
        @brief Рассчитывает сумму штрафа.
        @details Демологика: штраф = часть средств пользователя.
        @param booking Бронирование.
        @return Сумма штрафа.
        """
        return booking.person.bank_account.get_sum() * self.penalty_rate


