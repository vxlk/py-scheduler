import threading
from PyQt5 import QtCore

class ThreadPool():
    def __init__(self):
        self.max_num_threads = 8
        self.current_num_threads = 0
        self.threads = []

        for thread_index in max_num_threads:
            threads.append(threading.thread())

    # find an available thread from the pool
    def get_thread(self, str_name):
        if thread_is_active(str_name):
            self.wait_for_thread(str_name)

    def thread_is_active(self, str_name):
        found_thread = self.find_thread(str_name)
        if found_thread != None:
            # thread is alive if can't join so it is active if it isn't alive
            # not too sure about this might just wanna subclass thread
            return not found_thread.is_alive()
        return False

    def find_thread(self, str_name):
        for thread in self.threads:
            if thread.name == str_name
                return thread
        return None

    def find_or_create_thread(self, str_name)
        found_thread = self.find_thread(str_name)
        if not found_thread:
            return self.open_thread(str_name)
        return self.create_thread(str_name)
        

    def start_thread(self, str_thread_name, func, *kwargs):
        # find the first available and start it?
        for thread in self.threads:
            if thread.is_alive():
                thread.name = str_thread_name
                # idk how to handle the callback yet?
                thread.start(func, *kwargs)


    def wait_for_thread(self, str_name)
        current_thread = find_thread(str_name)
        busy_wait_thread = self.create_thread("Busy Wait " + str_name)
        # not using the wait thread: todo
        busy_wait_thread.start(lambda: self.busy_wait, current_thread)
        current_thread = self.find_thread(str_name)
        return current_thread

    def busy_wait(self, desired_thread):
        while not desired_thread.is_alive():
            none = None

class ProgressReporter():
    def __init__(self, event_name_str):
        self.name = event_name_str
        progress = 0.0

    def set_progress(self, percent)
        self.progress = percent
        # emit progress_changed

class Event():
    def __init__(self, str_name, _func, *kwargs, _thread = None):
        self.name = str_name
        self.thread = _thread
        self.func = _func
        self.args = *kwargs
        self.progress = ProgressReporter(self.name)

# The scheduler is the interface into the event system
# A scheduled event is an event that will run on its own
# thread and tell the scheduler when it finishes
# also will have support for recurring timed events
class Scheduler():
    def __init__(self):
        self.event_queue = []
        self.thread_pool = ThreadPool()

    def create_event(self):
        none = None

scheduler = Scheduler()