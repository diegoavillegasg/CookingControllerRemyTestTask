from enum import Enum


class TaskStatus(Enum):
    CREATED_OK = 1
    IN_PROGRESS = 2
    FINISHED_OK = 3
    FINISHED_WARN = 4
    ERROR = 5


""" 
    @:param prod_line : (production line) refers to the near location of task to be performed 
    
"""


class Task(object):
    def __init__(self):
        self.assigned = False
        self.started = False
        self.finished = False
        self.current_status = TaskStatus.CREATED_OK
        self.production_line = None
        self.worker = None

    def assign_prod_line(self, prod_line):
        self.production_line = prod_line

    def has_worker_assigned(self):
        return self.assigned

    def has_prod_line_assigned(self):
        return not (self.production_line is None)

    def is_started(self):
        return self.started

    def is_finished(self):
        return self.finished

    def assign_worker(self, worker):
        self.worker = worker
        self.assigned = True
        self.started = True
        self.current_status = TaskStatus.IN_PROGRESS


class Spread(Task):
    def __init__(self, ingredient, times):
        super(Spread, self).__init__()
        self.ingredient_to_spread = ingredient
        self.times_spread = times


class Scatter(Task):
    def __init__(self, ingredient, times):
        super(Scatter, self).__init__()
        self.ingredient_to_scatter = ingredient
        self.times_scatter = times


class PlacePizzaInOven(Task):
    def __init__(self):
        super(PlacePizzaInOven, self).__init__()
        pass


class PickPizzaFromOven(Task):
    def __init__(self):
        super(PickPizzaFromOven, self).__init__()
        pass


class Slice(Task):
    def __init__(self, pieces):
        super(Slice, self).__init__()
        self.number_of_slices = pieces


class Pack(Task):
    def __init__(self, size):
        super(Pack, self).__init__()
        self.pack_size = size


class Oven(Task):
    def __init__(self, duration):
        super(Oven, self).__init__()
        self.oven_to_use = None
        self.cooking_duration = duration

    def assign_oven(self, oven):
        print("Assigning oven to Oven task..." + str(oven))
        self.oven_to_use = oven

