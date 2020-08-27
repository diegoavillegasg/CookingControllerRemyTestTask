from enum import Enum

from CookingController.GlobalConfigs import CONFIGS, TASKS, BEFORE_OVEN_TASKS, AFTER_OVEN_TASKS, OVEN_DURATION
from CookingController.Task import *


class ClientOrderState(Enum):
    CREATED = 0
    PROCESSING = 1
    FINISHED = 2


class ClientOrder(object):
    def __init__(self, client_id, qty, size, config):
        self.client_id = client_id
        self.id = id(self)
        self.qty = int(qty)
        self.size = size
        self.config = config
        # a list of subtasks
        self.work_orders_list = []
        # a list of tasks
        self.order_tasks_list = []
        self.state = None

    def create_list_of_tasks(self):
        # ###################################################### #
        #                   BEFORE OVEN [Spread, Scatter]
        # ###################################################### #
        for prep_config in BEFORE_OVEN_TASKS:
            print("Config: " + prep_config)

            current_ingredient = "Unknown"
            current_qty = -1
            found_ingredient = False
            found_qty = False
            for key, value in self.config.items():
                if key.startswith(prep_config) and value == 'true':
                    print("Current config => " + prep_config + " : " + value)
                    current_ingredient = key[len(prep_config):]
                    print("Ingredient : " + current_ingredient)
                    found_ingredient = True

                if key.startswith('Qty') and (prep_config in key):
                    print("Qty : " + value)
                    current_qty = int(value)
                    found_qty = True

                if found_qty and found_ingredient:
                    break

            new_task = eval(prep_config)(ingredient=current_ingredient, times=current_qty)
            print("new task created... " + str(new_task))
            self.order_tasks_list.append(new_task)

        # ###################################################### #
        #                           OVEN
        # ###################################################### #
        new_task = PlacePizzaInOven()
        self.order_tasks_list.append(new_task)
        print("new task created... " + str(new_task))

        new_task = Oven(duration=OVEN_DURATION)
        self.order_tasks_list.append(new_task)
        print("new task created... " + str(new_task))
        # This task requires an oven is assigned related to the production line selected for the previous tasks

        new_task = PickPizzaFromOven()
        self.order_tasks_list.append(new_task)
        print("new task created... " + str(new_task))

        # ###################################################### #
        #                       AFTER OVEN [Slice]
        # ###################################################### #
        for post_config in AFTER_OVEN_TASKS:
            print("Config: " + post_config)

            current_qty = -1
            for key, value in self.config.items():
                if key.startswith('Qty') and (post_config in key):
                    print("Qty : " + value)
                    current_qty = int(value)
                    break

            new_task = eval(post_config)(pieces=current_qty)
            print("new task created... " + str(new_task))
            self.order_tasks_list.append(new_task)

        # ###################################################### #
        #                       PACKAGING
        # ###################################################### #
        new_task = Pack(size=self.size)
        self.order_tasks_list.append(new_task)
        print("new task created... " + str(new_task))

    def set_created_state(self):
        self.state = ClientOrderState.CREATED

    def get_state(self):
        return self.state

    def is_created(self):
        return self.state == ClientOrderState.CREATED

    def is_processing(self):
        return self.state == ClientOrderState.PROCESSING

    def is_finished(self):
        return self.state == ClientOrderState.FINISHED

    def get_size(self):
        return self.size

    def get_qty(self):
        return self.qty

    def print_description(self):
        message = "ClientOrder info" + "\n" \
                  "Object id: " + str(self.id) + "\n" \
                  "Client id: " + str(self.client_id) + "\n" \
                  "Qty : " + str(self.qty) + "\n" \
                  "Config: " + str(self.config.items()) + "\n"
        print(message)
