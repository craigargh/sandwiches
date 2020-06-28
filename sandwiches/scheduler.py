from typing import List

from sandwiches.constants import SANDWICH, SERVE_TASK, MAKE_SANDWICH_TASK, BREAK_TASK
from sandwiches.models import Order, Task


class CafeScheduler:
    def __init__(self):
        self.orders: List[Order] = []

    def add_order(self, order_number: int, items: List[str]) -> None:
        self.orders.append(
            Order(order_number, items)
        )

    def schedule(self) -> List[Task]:
        tasks = []
        for order in self.orders:
            order_tasks = process_order(order)
            tasks.extend(order_tasks)

        break_task = Task(
            order_id=None,
            description='Take a break',
            task_type=BREAK_TASK,
        )
        tasks.append(break_task)

        tasks = calculate_timing(tasks)

        return tasks

    def printable_schedule(self) -> str:
        task_strings = []
        for schedule_number, task in enumerate(self.schedule()):
            start_time = convert_secs_to_mins(task.start_time_seconds)

            output = f'{schedule_number + 1}.\t{start_time}\t{task.description}'
            task_strings.append(output)

        return '\n'.join(task_strings)


def process_order(order: Order) -> List[Task]:
    tasks = []

    for sandwiches_count, food_item in enumerate(order.items):
        if food_item != SANDWICH:
            continue

        make_task = Task(
            order_id=order.order_id,
            description=f'Make sandwich {sandwiches_count + 1} for Order {order.order_id}',
            task_type=MAKE_SANDWICH_TASK,
        )
        tasks.append(make_task)

    serve_task = generate_serve_task(order)
    tasks.append(serve_task)

    return tasks


def generate_serve_task(order: Order) -> Task:
    description = f'Serve Order {order.order_id}'

    return Task(
        order_id=order.order_id,
        description=description,
        task_type=SERVE_TASK
    )


def calculate_timing(tasks: List[Task]) -> List[Task]:
    timing_map = {
        SERVE_TASK: 60,
        MAKE_SANDWICH_TASK: 150,
        BREAK_TASK: 0,
    }

    elapsed_time = 0

    for task in tasks:
        task.start_time_seconds = elapsed_time
        elapsed_time += timing_map[task.task_type]

    return tasks


def convert_secs_to_mins(seconds: int) -> str:
    minutes = seconds // 60
    seconds = seconds % 60
    return f'{minutes:02d}:{seconds:02d}'
