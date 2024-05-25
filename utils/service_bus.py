from azure.servicebus import ServiceBusClient, ServiceBusMessage
from os import environ
import json


class ServiceBus:
    def __init__(self):
        connection_string = environ.get("SERVICE_BUS_CONNECTION_STRING")
        self.client = ServiceBusClient.from_connection_string(connection_string)

    def send_message(self, queue_name, message):
        """Send a message to a queue."""
        with self.client.get_queue_sender(queue_name) as sender:
            serialized_msg = self.serialize_message(message)
            single_message = ServiceBusMessage(serialized_msg)
            sender.send_messages(single_message)
            print(
                f"Service Bus Message sent to '{queue_name}' queue:\n{serialized_msg}"
            )

    def dequeue(self, queue_name, max_wait_time=30):
        """Dequeue messages from a queue."""
        with self.client.get_queue_receiver(
            queue_name, max_wait_time=max_wait_time
        ) as receiver:
            for msg in receiver:  # ServiceBusReceiver instance is a generator.
                print(str(msg))

    def dequeue_loop(self, queue_name, callback, max_wait_time=30):
        """Dequeue messages from a queue and call a callback function for each message."""
        with self.client.get_queue_receiver(
            queue_name, max_wait_time=max_wait_time
        ) as receiver:
            for msg in receiver:  # ServiceBusReceiver instance is a generator.
                deserialized_msg = self.deserialize_message(msg)
                callback(deserialized_msg)

    def serialize_message(self, message):
        """Serialize a message to JSON string."""
        return json.dumps(message, indent=4, sort_keys=True, default=str)

    def deserialize_message(self, message):
        """Deserialize a JSON string to a message."""
        return json.loads(message)
