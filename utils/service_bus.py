from flask import current_app
from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBus:
    def __init__(self):
        connection_string = current_app.config["UPLOAD_FOLDER"]
        self.client = ServiceBusClient.from_connection_string(connection_string)

    def send_message(self, queue_name, message):
        with self.client.get_queue_sender(queue_name) as sender:
            single_message = ServiceBusMessage(message)
            sender.send_messages(single_message)

    def dequeue(self, queue_name, max_wait_time=30):
        with self.client.get_queue_receiver(
            queue_name, max_wait_time=max_wait_time
        ) as receiver:
            for msg in receiver:  # ServiceBusReceiver instance is a generator.
                print(str(msg))

    def dequeue_loop(self, queue_name, callback, max_wait_time=30):
        with self.client.get_queue_receiver(
            queue_name, max_wait_time=max_wait_time
        ) as receiver:
            for msg in receiver:  # ServiceBusReceiver instance is a generator.
                callback(msg)
