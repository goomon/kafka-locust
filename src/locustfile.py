import time
import uuid
import json

from confluent_kafka import Producer
from locust import task, User, events
from sqlalchemy.orm import Session

from mock_generator import MockSensorDataGenerator

session: Session = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global session
    # Base.metadata.create_all(engine)
    # session = get_db()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    global session
    # session.commit()
    # session.close()
    print("test stop!");


class KafkaLocust(User):
    conf = {"bootstrap.servers": "localhost:19092"}
    producer = Producer(conf)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.generator = None

    def on_start(self):
        self.user_id = str(uuid.uuid4())
        self.generator = MockSensorDataGenerator(self.user_id)
        return super().on_start()

    @task
    def send_data(self):
        data = self.generator.generate_data()
        if data is not None:
            try:
                self.producer.produce(
                    topic="chest",
                    value=json.dumps(data),
                    key=self.user_id,
                )
                self.producer.flush()
            except RuntimeError as e:
                pass
            print("success!")
        time.sleep(1)
