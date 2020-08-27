from enum import Enum


class WorkerState(Enum):
    IDLE = 0
    BUSY = 1


class Worker(object):
    def __init__(self, prod_line, capable_tasks):
        self.has_task_assigned = False
        self.id = id(self)
        self.state = WorkerState.IDLE
        for (k, v) in capable_tasks.items():
            if k not in self.__dict__:
                self.__dict__[k] = v
                print("added a new Task for this worker: " + k)

    def is_capable_of(self, task_required):
        if task_required in self.__dict__:
            return True
        else:
            return False

    def is_busy(self):
        return self.state == WorkerState.BUSY

    def print_description(self):
        print("Worker capabilities: ")
        print("Id: " + str(self.id))
        print(*self.__dict__.items(), sep='\n')

