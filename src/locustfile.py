import time
import uuid

from locust import task, HttpUser, events
from sqlalchemy.orm import Session

from mock_generator import MockSensorDataGenerator
from db.models import Base, StartRecord
from db.database import engine, get_db

session: Session = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global session
    Base.metadata.create_all(engine)
    session = get_db()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    global session
    session.commit()
    session.close()
    print("test stop!");


class SpringLocust(HttpUser):
    client = None

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
        global session
        msg = self.generator.generate_data()
        if msg is not None:
            self.client.post("/", json=msg)
            data = StartRecord(
                connection_id=msg["connection_id"],
                timestamp=msg["timestamp"],
            )
            session.add(data)
        time.sleep(1)
