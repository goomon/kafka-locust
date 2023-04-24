import time
import uuid

from locust import task, HttpUser

from mock_generator import MockSensorDataGenerator


class SpringLocust(HttpUser):
    client = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None

    def on_start(self):
        self.user_id = str(uuid.uuid4())
        return super().on_start()

    @task
    def send_data(self):
        msg = MockSensorDataGenerator.generate_data(self.user_id)
        if msg is not None:
            self.client.post("/", json=msg)
        time.sleep(1)
