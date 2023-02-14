import random
import time
from collections import defaultdict


class MockSensorDataGenerator:
    timestamp_map: dict[str, float] = defaultdict(time.time)
    base_template = {
        "user_id": None,
        "timestamp": None
    }

    @staticmethod
    def get_acc(user_id):
        tpl = MockSensorDataGenerator.base_template
        tpl["user_id"] = user_id
        tpl["timestamp"] = MockSensorDataGenerator.timestamp_map["acc"]
        MockSensorDataGenerator.timestamp_map["acc"] += 1/32
        tpl["x"] = random.uniform(-20, 20)
        tpl["y"] = random.uniform(-20, 20)
        tpl["z"] = random.uniform(-20, 20)
        return tpl

    @staticmethod
    def get_hr(user_id):
        tpl = MockSensorDataGenerator.base_template
        tpl["user_id"] = user_id
        tpl["timestamp"] = MockSensorDataGenerator.timestamp_map["hr"]
        MockSensorDataGenerator.timestamp_map["hr"] += 1
        tpl["value"] = random.uniform(-20, 20)
        return tpl
