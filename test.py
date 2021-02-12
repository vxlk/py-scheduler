from scheduler.scheduler import *

def linear_loop_mil():
    print("in")
    for i in range(1000000000):
        none = None

#scheduler.join("Scheduler")

print ("running event 1")
scheduler.create_event("Event 1", linear_loop_mil)
print ("running event 2")
scheduler.create_event("Event 2", linear_loop_mil)
print(scheduler.profile())
scheduler.join("Event 1")
scheduler.join("Event 2")

# kill the scheduler thread
scheduler.kill()