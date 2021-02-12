import threading
from PyQt5 import QtCore

class ThreadPool():
    def __init__(self):
        self.max_num_threads = 8
        self.current_num_threads = 0
        self.threads = []

        for thread_index in range(self.max_num_threads):
            self.threads.append(threading.Thread())

    # find an available thread from the pool
    def get_thread(self, str_name):
        if thread_is_active(str_name):
            self.wait_for_thread(str_name)

    def thread_is_active(self, str_name):
        found_thread = self.find_thread(str_name)
        if found_thread != None:
            # thread is alive if can't join so it is active if it isn't alive
            # not too sure about this might just wanna subclass thread
            return found_thread.is_alive()
        return False

    def find_thread(self, str_name):
        for thread in self.threads:
            if thread.name == str_name:
                return thread
        return None

    def start_thread(self, str_thread_name):
        # find the first available and start it?
        for thread in self.threads:
            if thread.name == str_thread_name:
                if not thread.is_alive():
                    thread.name = str_thread_name
                    # idk how to handle the callback yet?
                    thread.start()
                    break
                else:
                    thread = self.wait_for_thread(str_thread_name)
                    thread.start()
                    break


    def wait_for_thread(self, str_name):
        current_thread = find_thread(str_name)
        busy_wait_thread = self.find_or_create_thread("Busy Wait " + str_name, self.busy_wait)
        # not using the wait thread: todo
        busy_wait_thread.start_thread("Busy Wait")
        current_thread = self.find_thread(str_name)
        return current_thread

    def busy_wait(self, desired_thread):
        while not desired_thread.is_alive():
            none = None

    # todo: doesnt respect size of max_num_threads
    def find_or_create_thread(self, str_name, _func, *kwargs):
        for thread in self.threads:
            if thread.name == str_name:
                print("found thread " + str_name)
                self.wait_for_thread(str_name)
                return thread
        else:
            if self.current_num_threads < self.max_num_threads:
                if len(kwargs) != 0:
                    print("not here")
                    new_thread = threading.Thread(target=_func, args=kwargs)
                else:
                    print("here")
                    new_thread = threading.Thread(target=_func)
                new_thread.name = str_name
                self.threads.append(new_thread)
                return new_thread
            else:
                raise Exception("too many threads, this will need revisited")

    def profile(self):
        str_return_msg = ""
        for thread in self.threads:
            if self.thread_is_active(thread):
                str_return_msg += "Active Thread: " + thread.name + "\n"
            else:
                str_return_msg += "Dead Thread: " + thread.name + "\n"
        return str_return_msg

class ProgressReporter():
    def __init__(self, event_name_str):
        self.name = event_name_str
        progress = 0.0

    def set_progress(self, percent):
        self.progress = percent
        # emit progress_changed

class Event():
    def __init__(self, str_name, _thread, _func, *kwargs):
        self.name = str_name
        self.thread = _thread
        self.func = _func
        self.args = kwargs
        self.progress = ProgressReporter(self.name)

    def pre_start(self):
        print("Starting event " + self.name)
        if self.thread is None:
            print(self.print())
            raise Exception("Event has no thread")
        if self.func is None:
            print(self.print())
            raise Exception("Event has no function attached")

    def print(self):
        str_return_msg = ""
        str_return_msg += "Event Name " + self.name + "\n"
        return str_return_msg

# The scheduler is the interface into the event system
# A scheduled event is an event that will run on its own
# thread and tell the scheduler when it finishes
# also will have support for recurring timed events
class Scheduler():
    def __init__(self):
        self.event_queue = [] # for now will be a history, but will eventually actually be a queue
        self.thread_pool = ThreadPool()
        self.scheduler_lock = threading.Lock()
        
        self.run = True

        self.scheduler_thread = self.thread_pool.find_or_create_thread("Scheduler", self._run_scheduler)
        self.thread_pool.start_thread("Scheduler")

    def create_event(self, str_event_name, _func, *kwargs):
        print("adding event " + str_event_name)
        self.scheduler_lock.acquire()

        event_thread = self.thread_pool.find_or_create_thread(str_event_name, _func, kwargs)
        new_event = Event(str_event_name, event_thread, _func, kwargs)
        self.event_queue.append(new_event)

        self.scheduler_lock.release()

    def profile(self):
        # no lock yolo, prob needs fixed
        print(self.thread_pool.profile())
        print("------- List of Events in our queue (history for now) reverse order")
        for event in self.event_queue:
            print("Event: " + event.print())

    def _run_scheduler(self):
        print("event loop outer")
        while self.run:
            self.scheduler_lock.acquire()

            for event in self.event_queue:
                print("event loop")
                # run checks and stuff
                event.pre_start()
                # kick off the thread (also handle waiting if we have to)
                self.thread_pool.start_thread(event.name)
            
            self.event_queue.clear()

            self.scheduler_lock.release()

    def join(self, str_event_name):
        thread = self.thread_pool.find_thread(str_event_name)
        if thread is not None:
            thread.join()

    def kill(self):
        self.run = False