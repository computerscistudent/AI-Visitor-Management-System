import time

unknown_count = 0
last_unknown_time = 0

COOLDOWN = 5  # seconds

def increment_unknown():
    global unknown_count,last_unknown_time

    current_time = time.time()

    if current_time-last_unknown_time > COOLDOWN:
        unknown_count +=1
        last_unknown_time = current_time


def get_unknown_count():
    return unknown_count

def reset_unknown():
    global unknown_count, last_unknown_time
    unknown_count = 0
    last_unknown_time = 0