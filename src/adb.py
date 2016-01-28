import random
import time


def logcat_worker(callback):
    while True:
        i = random.uniform(0.002, 0.2)
        time.sleep(i)
        callback(i)
