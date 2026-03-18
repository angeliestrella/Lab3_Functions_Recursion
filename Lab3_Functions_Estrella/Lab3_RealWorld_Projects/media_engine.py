# media_engine.py

# Decorator to monitor the generator
def monitor(func):
    def wrapper(limit):
        print("Processing Started")
        for value in func(limit):
            yield value
        print("Processing Completed")
    return wrapper

# Generator to yield squared even numbers
@monitor
def play_count_stream(limit):
    for i in range(limit):
        if i % 2 == 0:
            yield i**2