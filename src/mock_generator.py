import time
import uuid
from typing import List, Generator, Optional

from schema import ChestDeviceSensorRecord, Axis, \
    ChestDeviceSensorValue
from config.constants import *


def read_lines(filename: str) -> Generator[str, None, None]:
    if filename is None:
        filename = "../data/respiban.txt"
    while True:
        with open(filename) as f:
            for line in f:
                yield line.strip()


def calc_sample_rate() -> int:
    return int(WINDOW_SIZE * (1 - OVERLAP_RATIO))


class MockSensorDataGenerator:

    def __init__(self, user_id):
        self.user_id = user_id
        self.sampling_rate: int = calc_sample_rate()
        self.counter: int = 0
        self.file_reader: Generator[str, None, None] = read_lines(None)
        self.record_queue: List[ChestDeviceSensorValue] = []

    def generate_data(self) -> Optional[ChestDeviceSensorRecord]:
        # Data generating function is called every one second.
        self.counter += 1

        chest_acc: List[Axis] = []
        chest_ecg: List[int] = []
        chest_eda: List[int] = []
        chest_emg: List[int] = []
        chest_temp: List[int] = []
        chest_resp: List[int] = []
        cnt = 0
        for line in self.file_reader:
            line = line.split("\t")
            # Sampling rate of Respiban dataset is 700Hz.
            if cnt > SAMPLING_RATE:
                break
            cnt += 1
            # Insert sensor data from target file.
            chest_ecg.append(int(line[0]))
            chest_eda.append(int(line[1]))
            chest_emg.append(int(line[2]))
            chest_temp.append(int(line[3]))
            chest_acc.append({
                "x": int(line[4]),
                "y": int(line[5]),
                "z": int(line[6])
            })
            chest_resp.append(int(line[7]))

        template: ChestDeviceSensorValue = {
            "chest_acc": {
                "hz": SAMPLING_RATE,
                "value": chest_acc
            },
            "chest_ecg": {
                "hz": SAMPLING_RATE,
                "value": chest_ecg
            },
            "chest_eda": {
                "hz": SAMPLING_RATE,
                "value": chest_eda
            },
            "chest_emg": {
                "hz": SAMPLING_RATE,
                "value": chest_emg
            },
            "chest_temp": {
                "hz": SAMPLING_RATE,
                "value": chest_temp
            },
            "chest_resp": {
                "hz": SAMPLING_RATE,
                "value": chest_resp
            }
        }
        self.record_queue.append(template)
        # If record_queue size is greater than window size, pop it.
        if len(self.record_queue) > WINDOW_SIZE:
            self.record_queue = self.record_queue[1:]

        if len(self.record_queue) == WINDOW_SIZE and self.counter % self.sampling_rate == 0:
            return {
                "user_id": self.user_id,
                "connection_id": str(uuid.uuid4()),
                "timestamp": int(time.time() * 1000),
                "window_size": WINDOW_SIZE,
                "value": self.record_queue
            }
        else:
            return None
