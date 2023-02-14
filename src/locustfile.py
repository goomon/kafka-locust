import json
import time
import uuid

from locust import task, User

from kafka_client import KafkaClient
from mock_generator import MockSensorDataGenerator


class KafkaLocust(User):
    mock_generator = MockSensorDataGenerator
    client = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        KafkaLocust.client = KafkaClient(config_path="config/cloud.ini")

    def on_start(self):
        self.user_id = str(uuid.uuid4())
        return super().on_start()

    @task
    def send_acc(self):
        msg = KafkaLocust.mock_generator.get_acc(self.user_id)
        self.client.send("acc", key=self.user_id, message=json.dumps(msg))
        time.sleep(1)

    @task
    def send_hr(self):
        msg = KafkaLocust.mock_generator.get_hr(self.user_id)
        self.client.send("hr", key=self.user_id, message=json.dumps(msg))
        time.sleep(1)
