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
        total: float = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass


class SMSAuthorizer(Authorizer):

    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f"Verifying SMS code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class GoogleAuthorizer(Authorizer):

    def __init__(self):
        self.authorized = False

    def verify_code(self, code):
        print(f"Verifying google code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order: Order) -> None:
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str, authorizer: Authorizer):
        self.security_code = security_code
        self.authorizer = authorizer
    
    def pay(self, order: Order) -> None:
        if not self.authorizer.is_authorized():
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

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email: str, authorizer: Authorizer):
        self.email = email 
        self.authorizer = authorizer
    
    def pay(self, order: Order) -> None:
        if not self.authorizer.is_authorized():
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

    authorizer = SMSAuthorizer()
    authorizer.verify_code(654321)

    processor = DebitPaymentProcessor("123456", authorizer)
    processor.pay(order)

if __name__ == '__main__':
    main()