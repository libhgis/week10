from abc import ABC, abstractmethod

class Order:

    def __init__(self):
        self.items: list[str] = []
        self.quantities: list[int] = []
        self.prices: list[float] = []
        self.status: str = "open"

    def add_item(self, name: str, quantity: int, price: float) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self) -> float:
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order: Order, security_code:str) -> None:
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order, security_code:str) -> None:
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order , security_code:str) -> None:
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


def main():
    order = Order()
    order.add_item("Keyboard", 1, 200)
    order.add_item("SSD", 1, 800)
    order.add_item("USB cable", 2, 50)

    print(f'Total price: { order.total_price() }')

    processor = DebitPaymentProcessor()
    processor.pay(order, "123456")

if __name__ == '__main__':
    main()