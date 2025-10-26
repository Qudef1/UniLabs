from datetime import datetime

class NotEnoughMoney(Exception):
    """
    @brief Исключение: недостаточно средств на счёте
    @details Выбрасывается при попытке совершить транзакцию, если на счёте недостаточно денег
    с учётом комиссии.
    """
    def __init__(self):
        """@brief Конструктор исключения"""
        super().__init__("Not enough money. Transaction Failed")


class Transaction:
    """
    @brief Представляет банковскую транзакцию между двумя счетами
    @details Автоматически обрабатывает перевод средств с комиссией 3%.
    Генерирует уникальный номер транзакции на основе ID счетов и времени.
    """

    def __init__(self, bank_sender, bank_receiver, price: float):
        """
        @brief Конструктор транзакции
        @param bank_sender Счёт-отправитель средств
        @param bank_receiver Счёт-получатель средств
        @param price Сумма перевода (до удержания комиссии)
        @exception NotEnoughMoney Если на счёте отправителя недостаточно средств
        с учётом комиссии 3%
        """
        self.price = price
        self.sender = bank_sender
        self.receiver = bank_receiver
        self.transaction_number = (
            bank_sender.id + "_" + bank_receiver.id + "_" + 
            datetime.now().strftime("%Y%m%d%H%M%S")
        )
        self.process_transaction()

    def process_transaction(self):
        """
        @brief Выполняет обработку транзакции
        @details Списывает сумму + 3% комиссии с отправителя и зачисляет сумму получателю.
        @exception NotEnoughMoney Если средств недостаточно для покрытия суммы и комиссии
        """
        if (self.sender.sum - self.price * 1.03 < 0):
            raise NotEnoughMoney()
        
        self.sender.withdraw(self.price * 1.03) 
        self.receiver.transfer(self.price)

    def get_transaction_number(self) -> str:
        """
        @brief Возвращает уникальный номер транзакции
        @return Строка в формате: "senderID_receiverID_YYYYMMDDHHMMSS"
        """
        return self.transaction_number

    def __str__(self) -> str:
        """
        @brief Строковое представление транзакции
        @return Уникальный номер транзакции
        """
        return self.transaction_number


class BankAccount:
    """
    @brief Представляет банковский счёт клиента
    @details Поддерживает операции снятия, пополнения и перевода средств.
    Используется для оплаты туристических услуг.
    """

    def __init__(self, sum: float, id: str):
        """
        @brief Конструктор банковского счёта
        @param sum Начальный баланс счёта
        @param id Уникальный идентификатор счёта (например, "ALICE123")
        """
        self.sum = sum
        self.id = id

    def make_transaction(self, other, price: float):
        """
        @brief Инициирует транзакцию на другой счёт
        @param other Счёт получателя
        @param price Сумма перевода
        @exception NotEnoughMoney Если средств недостаточно для перевода с комиссией
        @note При успешной транзакции создаётся объект Transaction и сохраняется в self.transaction
        """
        try:
            self.transaction = Transaction(self, other, price)
            print(f"transaction {self.transaction.transaction_number} has successfully processed")
        except NotEnoughMoney:
            raise NotEnoughMoney()

    def withdraw(self, price: float):
        """
        @brief Списывает сумму со счёта
        @param price Сумма для снятия
        @note Операция выполняется только если остаток остаётся положительным
        """
        if self.sum - price > 0:
            self.sum -= price

    def transfer(self, price: float):
        """
        @brief Пополняет счёт на указанную сумму
        @param price Сумма пополнения
        """
        self.sum += price

    def get_sum(self) -> float:
        """
        @brief Возвращает текущий баланс счёта
        @return Текущая сумма на счёте
        """
        return self.sum