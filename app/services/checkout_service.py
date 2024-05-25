from utils.service_bus import ServiceBus
from app.extensions import db
import logging
from config import environment


class CheckoutService:
    """Service to process an order."""

    def __init__(self, order, queue_name="orders"):
        self.order = order
        self.service_bus = ServiceBus()
        self.queue_name = queue_name
        self.logger = logging.getLogger(__name__)

    def process(self):
        self.__validate_checkout_conditions()

        try:
            self.logger.info(f"Processing order {self.order.id}")
            self.__send_to_transport_company()
            self.__set_order_status_to_processed()
            self.__subtract_inventory()
            db.session.commit()
            self.logger.info(f"Order {self.order.id} processed successfully")
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Failed to process order {self.order.id}: {e}")
            raise e

    def __subtract_inventory(self):
        self.logger.info("Subtracting inventory for order {self.order.id}")
        for item in self.order.items:
            product = item.product
            product.stock -= item.quantity
            db.session.add(product)
            self.logger.info(f"Product {product.id} stock reduced by {item.quantity}")

    def __send_to_transport_company(self):
        """Send the order to the service bus queue where any transport company can pick it up."""
        if environment == "production":
            self.service_bus.send_message(self.queue_name, self.__order_dict())
        else:
            self.logger.debug(
                f"[DEVELOPMENT]Order {self.order.id} sent to {self.queue_name}"
            )

    def __set_order_status_to_processed(self):
        self.order.status = "Processed"
        db.session.add(self.order)

    def __validate_checkout_conditions(self):
        if self.order.status != "Pending":
            raise Exception("Order is not pending")

        if not self.order.items:
            raise Exception("Order has no items")

    def __order_dict(self):
        return self.order.to_dict(
            show=[
                "id",
                "user",
                "user.first_name",
                "user.last_name",
                "user.email",
                "user.phone",
                "user.address",
                "user.zip_code",
                "user.location",
                "user.vat_number",
                "items",
                "items.quantity",
                "items.product_id",
                "items.product.name",
                "items.product.price",
            ]
        )
