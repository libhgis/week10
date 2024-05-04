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
    def pay(self, order: Order) -> None:
        pass

class PaymentProcessorSMS(PaymentProcessor):
    @abstractmethod
    def auth_sms(self, code):
        pass


class DebitPaymentProcessor(PaymentProcessorSMS):
    def __init__(self, security_code: str):
        self.security_code = security_code
        self.verified = False  

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True
    
    def pay(self, order: Order) -> None:
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str):
        self.security_code = security_code  

    def pay(self, order: Order) -> None:
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessorSMS):
    def __init__(self, email: str):
        self.email = email 
        self.verified = False  

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True
    
    def pay(self, order: Order) -> None:
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email}")
        order.status = "paid"

def main():
    order = Order()
    order.add_item("Keyboard", 1, 200)
    order.add_item("SSD", 1, 800)
    order.add_item("USB cable", 2, 50)

    print(f'Total price: { order.total_price() }')

    processor = DebitPaymentProcessor("123456")
    processor.auth_sms(654321)
    processor.pay(order)

if __name__ == '__main__':
    main()