from enum import Enum


class OvenState(Enum):
    IDLE = 0
    # PREHEATING = 1
    # to include this state it should be considered time the first pizza is placed in Oven,
    # waiting for the next pizza is prepared. It depends on how many pizzas a robot can handle,
    # how much time is prepared for and how the pick&place robots can handle pizzas from different work areas.
    COOKING = 2
    FINISHING_TASK = 3


class Oven(object):
    def __init__(self, prod_line, max_capacity):
        self.id = id(self)
        self.production_line = prod_line
        self.max_capacity = int(max_capacity)
        self.current_qty = 0
        self.state = OvenState.IDLE

    def get_oven_state(self):
        return self.state

    def add_new_pizza(self):
        self.current_qty += 1

    def oven(self):
        self.state = OvenState.COOKING

    def print_description(self):
        message = "Oven description : " + "\n" \
                  "Id: " + str(self.id) + "\n" \
                  "ProductionLine attached: " + str(self.production_line) + "\n" \
                  "MaxCapacity: " + str(self.max_capacity) + "\n" \
                  "Current number of pizzas entered: " + str(self.current_qty) + "\n" \
                  "State: " + str(self.state)
        print(message)
