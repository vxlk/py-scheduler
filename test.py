from scheduler.scheduler import *
from threading import *

scheduler = Scheduler()

print("main thread: " + threading.current_thread().name)

def linear_loop_mil():
    print("in")
    dontOptimizeMe = 0
    for i in range(1000000000):
        dontOptimizeMe += 1
    dontOptimizeMe += 2
    return dontOptimizeMe

#scheduler.join("Scheduler")

scheduler.create_event("Event 1", linear_loop_mil)
scheduler.create_event("Event 2", linear_loop_mil)
print(scheduler.profile())

# kill the scheduler thread
scheduler.kill()