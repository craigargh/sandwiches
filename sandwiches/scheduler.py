from collections import namedtuple
from typing import List

from sandwiches.constants import SANDWICH
from sandwiches.models import FoodItem, Order, Task

OrderDetails = namedtuple('OrderDetails', ['tasks', 'elapsed_time', 'sandwiches_count'])


class CafeScheduler:
    def __init__(self):
        self.orders: List[Order] = []

    def add_order(self, order_number: int, items: List[FoodItem]) -> None:
        self.orders.append(
            Order(order_number, items)
        )

    def schedule(self) -> List[Task]:
        sandwiches_count = 0
        elapsed_time = 0

        tasks = []
        for order in self.orders:
            order_details = process_order(order, elapsed_time, sandwiches_count)
            tasks.extend(order_details.tasks)

            elapsed_time = order_details.elapsed_time
            sandwiches_count = order_details.sandwiches_count

        break_task = Task(
            order_id=None,
            description='Take a break',
            start_time_seconds=elapsed_time,
        )
        tasks.append(break_task)

        return tasks

    def printable_schedule(self) -> str:
        task_strings = []
        for schedule_number, task in enumerate(self.schedule()):
            minutes = task.start_time_seconds // 60
            seconds = task.start_time_seconds % 60
            start_time = f'{minutes:02d}:{seconds:02d}'

            output = f'{schedule_number + 1}.\t{start_time}\t{task.description}'
            task_strings.append(output)

        return '\n'.join(task_strings)


def process_order(order: Order, elapsed_time: int, sandwiches_count: int) -> OrderDetails:
    tasks = []

    for food_item in order.items:
        if food_item.item_type != SANDWICH:
            continue

        sandwiches_count += 1
        make_task = Task(
            order_id=order.order_id,
            description=f'Make sandwich {sandwiches_count}',
            start_time_seconds=elapsed_time,
        )
        tasks.append(make_task)
        elapsed_time += 150

    serve_task = make_serve_task(order, sandwiches_count, elapsed_time)
    tasks.append(serve_task)
    elapsed_time += 60

    return OrderDetails(tasks, elapsed_time, sandwiches_count)


def make_serve_task(order: Order, sandwiches_count, elapsed_time) -> Task:
    description = serve_task_description(order, sandwiches_count)

    return Task(
        order_id=order.order_id,
        description=description,
        start_time_seconds=elapsed_time,
    )


def serve_task_description(order: Order, sandwiches_count: int) -> str:
    sandwiches = [
        food_item
        for food_item in order.items
        if food_item.item_type == SANDWICH
    ]

    if len(sandwiches) == 1:
        serve_description = f'Serve sandwich {sandwiches_count}'
    else:
        sandwich_numbers = [
            str(sandwich_id + 1)
            for sandwich_id in range(sandwiches_count - len(sandwiches), sandwiches_count)
        ]
        sandwiches_string = " and ".join([", ".join(sandwich_numbers[:-1]), sandwich_numbers[-1]])

        serve_description = f'Serve sandwiches {sandwiches_string}'

    return serve_description
