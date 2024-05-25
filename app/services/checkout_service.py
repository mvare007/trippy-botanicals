from utils.service_bus import ServiceBus
from app.extensions import db


class CheckoutService:
    def __init__(self, order):
        self.order = order
        self.service_bus = ServiceBus()

    def process(self):
        self.__send_to_transport_company()
        self.__subtract_inventory()

    def __subtract_inventory(self):
        for item in self.order.items:
            product = item.product
            product.stock -= item.quantity
            db.session.add(product)
        db.session.commit()

    def __send_to_transport_company(self):
        self.service_bus.send_message("orders", self.order.to_dict())
