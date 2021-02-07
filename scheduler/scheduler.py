import threading
from PyQt5 import QtCore

class ThreadPool():
    def __init__(self):
        self.max_num_threads = 8
        self.current_num_threads = 0
        self.threads = []

    # find an available thread from the pool
    def get_thread(self):
        if self.current_num_threads < self.max_num_threads:
            return thread()

class Event():
    def __init__(self, str_name, _thread, _func):
        self.name = str_name
        self.thread = _thread
        self.func = _func

# The scheduler is the interface into the event system
# A scheduled event is an event that will run on its own
# thread and tell the scheduler when it finishes
class Scheduler():
    def __init__(self):
        self.event_queue = []
        self.thread_pool = ThreadPool()

    def create_event(self):
        none = None

scheduler = Scheduler()