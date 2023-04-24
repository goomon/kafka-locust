import os

# Sampling rate of each data(Hz)
SAMPLING_RATE = 700
WINDOW_SIZE = 2 if os.getenv("WINDOW_SIZE") is None else int(os.getenv("WINDOW_SIZE"))
OVERLAP_RATIO = 0.5 if os.getenv("OVERLAP_RATIO") is None else float(os.getenv("OVERLAP_RATIO"))

# Topic
MAIN_TOPIC = "data"
