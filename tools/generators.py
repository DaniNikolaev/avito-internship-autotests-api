import os
import random
import time


def generate_seller_id() -> int:
    unique = (int(str(time.time_ns())[-6:]) + os.getpid()) % 888888
    return 111111 + unique + random.randint(0, unique)
