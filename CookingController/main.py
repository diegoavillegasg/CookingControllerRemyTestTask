import configparser
import glob
import os
import time

from CookingController.ClientOrder import ClientOrder
from CookingController.GlobalConfigs import CONFIGS, TASKS
from CookingController.Oven import Oven
from CookingController.Worker import Worker

CLIENT_ORDERS_LIST = []
WORKERS_LIST = []
PRODUCTION_LINE_DICT = {}


def start_pizza_maker():
    print("Hello Pizza Maker!!")
    options = configparser.ConfigParser()
    options.optionxform = str
    options.read(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'options.cfg'))
    prod_lines = options['PRODUCTION LINES']
    for k in range(1, prod_lines.getint('Qty')+1):
        print("Qty of Prod Lines: " + prod_lines.get('Qty'))
        PRODUCTION_LINE_DICT[str(k)] = 0  # 0: FREE  -  1: BUSY

    # ################ #
    #       WORKERS
    # ################ #
    workers_info = options['WORKERS']
    for key, value in workers_info.items():
        print("worker type: " + key + " Qty:" + value)
        for i in range(int(value)):
            print("adding a new Worker ID: " + str(i + 1))
            identifier = key + " " + str(i+1)
            print("Identifier computed: " + identifier)

            capable_tasks_dict = {}
            for task in TASKS:
                capable_tasks_dict[task] = options[identifier][task]
            if options[identifier].get('ProductionLine') > prod_lines['Qty']:
                raise ValueError("Please confirm you have setup the correct number of ProductionLine for all "
                                 "robots and ovens in `options.cfg` file")
                return

            new_worker = Worker(prod_line=options[identifier].get('ProductionLine'),
                                capable_tasks=capable_tasks_dict)
            WORKERS_LIST.append(new_worker)

    print("Qty of Workers found : " + str(len(WORKERS_LIST)))
    for worker in WORKERS_LIST:
        worker.print_description()

    # ################ #
    #       OVENS
    # ################ #
    ovens_list = []
    ovens_info = options['OVENS']
    ovens_qty = ovens_info.getint('Qty')
    print("ovens Qty:" + str(ovens_qty))
    for i in range(ovens_qty):
        identifier = "Oven " + str(i+1)
        print("Oven Identifier computed: " + identifier)
        new_oven = Oven(prod_line=options[identifier].get('ProductionLine'),
                        max_capacity=options[identifier].get('MaxCapacity'))
        ovens_list.append(new_oven)

    print("Qty of Ovens found : " + str(len(ovens_list)))
    for oven in ovens_list:
        oven.print_description()

    #while True:

    # ###################### #
    #   LOOK FOR NEW ORDERS
    # ###################### #
    look_new_order()

    # ###################### #
    #   MANAGE ORDERS
    # ###################### #
    # CREATE LIST OF DIFFS OF CURRENT ORDER QTY AND OVEN MAX CAPACITY
    list_of_ovens = [(oven_.max_capacity - current_order.get_qty(), oven_)
                     for current_order in CLIENT_ORDERS_LIST
                     for oven_ in ovens_list
                     if (oven_.max_capacity - current_order.get_qty()) >= 0]
    list_of_ovens.sort(key=lambda x: x[0], reverse=True)
    if len(list_of_ovens) > 0:
        print("Found at least %d Oven ", len(list_of_ovens))
    else:
        raise ValueError("Ovens not found to serve this order. Make sure the orders are being "
                         "created taking into account "
                         "the maximum capacity of current ovens in used.")
        return

    # ################################# #
    # ITERATION OVER GLOBAL ORDERS LIST
    # ################################# #
    for i in range(len(CLIENT_ORDERS_LIST)):
        current_order = CLIENT_ORDERS_LIST[i]

        if current_order.is_created():
            assert len(current_order.order_tasks_list) > 0, "Order created without tasks"

        # ##################################### #
        # ITERATION OVER TASKS OF A GIVEN ORDER
        # ##################################### #
        prod_line_to_use_in_task = None
        for j in range(len(current_order.order_tasks_list)):
            if j > 0:
                prev_task = current_order.order_tasks_list[j-1]

            current_task = current_order.order_tasks_list[j]

            if current_task.production_line is None and j == 0:  # only for the first task
                print("Task without production line assigned ")
                prod_line_assigned = False

                # COMPARE OVEN MAX CAPACITY AND ORDER QTY
                for _, oven_to_use in list_of_ovens:
                    if not PRODUCTION_LINE_DICT[oven_to_use.production_line]:
                        current_task.assign_prod_line(prod_line=oven_to_use.production_line)
                        PRODUCTION_LINE_DICT[oven_to_use.production_line] = 1 # IN USE
                        prod_line_to_use_in_task = oven_to_use.production_line
                        print("ProdLine " + prod_line_to_use_in_task + " assigned to task " + str(current_task))
                        prod_line_assigned = True
                        break
                    else:
                        print("ProdLine %s is Busy", oven_to_use.production_line)
            else:
                current_task.assign_prod_line(prod_line=prod_line_to_use_in_task)

            # ###################### #
            # ASSIGN WORKER TO TASK
            # ###################### #
            if j == 0:
                # for the first tasks
                if not current_task.is_assigned() and not current_task.is_finished():
                    assign_worker_to_task(current_task)

            else:
                # for the rest of tasks
                if prev_task.is_finished() and current_task.is_assigned() and not current_task.is_finished():
                    assign_worker_to_task(current_task)

    time.sleep(3)


def assign_worker_to_task(task):
    worker_assigned = False
    for worker_ in WORKERS_LIST:
        print("Task " + str(task) + " Type: " + str(task.__class__))
        if worker_.is_capable_of(task.__class__) and not worker_.is_busy():
            task.assign_worker(worker=worker_)
            print("Worker assigned to task ...")
            return
    if not task.is_assigned():
        print("All worker are busy.")


def look_new_order():
    # ################ #
    #       ORDERS
    # ################ #
    print("looking for a new order... ")
    orders_files = glob.glob(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "order*"))
    print("order files found: " + str(len(orders_files)))
    print(orders_files)
    for new_order_file in orders_files:
        orders = configparser.ConfigParser()
        orders.optionxform = str
        orders.read(new_order_file)
        order = orders['ORDER']
        print("# ##################### #")
        print("Current order received: \n [" + new_order_file + "]\n")
        print("(KEY : VALUE )")
        print(*order.items(), sep="\n")
        print("# ##################### #")

        # check qty of order and compare with MaxCapacity of each Oven available
        order_qty = order.get('Qty')
        configs = {}
        for config in CONFIGS:
            configs[config] = order.get(config)
        new_order = ClientOrder(client_id=order.get('ClientId'), qty=order.get('Qty'), size=order.get('Size'),
                                config=configs)
        new_order.set_created_state()
        new_order.create_list_of_tasks()
        CLIENT_ORDERS_LIST.append(new_order)
        print("adding a new order...")
        new_order.print_description()


if __name__ == '__main__':

    try:
        start_pizza_maker()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')

