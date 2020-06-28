from unittest import TestCase

from sandwiches.constants import SANDWICH, SNACK, DRINK
from sandwiches.models import FoodItem, Task
from sandwiches.scheduler import CafeScheduler


class TestCafeSchedulder(TestCase):
    def test_can_add_a_sandwich_order_to_the_schedule(self):
        scheduler = CafeScheduler()

        order_items = [FoodItem(SANDWICH)]
        scheduler.add_order(12, order_items)

        self.assertEqual(1, len(scheduler.orders))
        self.assertEqual(12, scheduler.orders[0].order_id)
        self.assertEqual(order_items, scheduler.orders[0].items)

    def test_can_add_multiple_orders_to_the_schedule(self):
        scheduler = CafeScheduler()

        scheduler.add_order(122, [FoodItem(SANDWICH)])
        scheduler.add_order(123, [FoodItem(SANDWICH)])

        self.assertEqual(2, len(scheduler.orders))
        self.assertEqual(122, scheduler.orders[0].order_id)
        self.assertEqual(123, scheduler.orders[1].order_id)

    def test_can_add_multiple_sandwiches_in_a_single_order(self):
        scheduler = CafeScheduler()

        order_items = [
            FoodItem(SANDWICH),
            FoodItem(SANDWICH),
            FoodItem(SANDWICH),
        ]
        scheduler.add_order(453, order_items)

        self.assertEqual(1, len(scheduler.orders))
        self.assertEqual(3, len(scheduler.orders[0].items))
        self.assertEqual(order_items, scheduler.orders[0].items)

    def test_schedule_returns_list_of_tasks_with_a_description(self):
        scheduler = CafeScheduler()

        scheduler.add_order(34, [FoodItem(SANDWICH)])
        scheduler.add_order(35, [FoodItem(SANDWICH)])

        tasks = scheduler.schedule()

        self.assertEqual(5, len(tasks))
        self.assertEqual("Make sandwich 1 for Order 34", tasks[0].description)
        self.assertEqual("Serve Order 34", tasks[1].description)
        self.assertEqual("Make sandwich 1 for Order 35", tasks[2].description)
        self.assertEqual("Serve Order 35", tasks[3].description)
        self.assertEqual("Take a break", tasks[4].description)

    def test_start_time_is_incremented_for_each_item_in_schedule(self):
        scheduler = CafeScheduler()

        scheduler.add_order(34, [FoodItem(SANDWICH)])
        scheduler.add_order(35, [FoodItem(SANDWICH)])

        tasks = scheduler.schedule()

        self.assertEqual(5, len(tasks))
        self.assertEqual(0, tasks[0].start_time_seconds)
        self.assertEqual(150, tasks[1].start_time_seconds)
        self.assertEqual(210, tasks[2].start_time_seconds)
        self.assertEqual(360, tasks[3].start_time_seconds)
        self.assertEqual(420, tasks[4].start_time_seconds)

    def test_order_number_is_set_for_each_item_in_schedule(self):
        scheduler = CafeScheduler()

        scheduler.add_order(34, [FoodItem(SANDWICH)])
        scheduler.add_order(35, [FoodItem(SANDWICH)])

        tasks = scheduler.schedule()

        self.assertEqual(5, len(tasks))
        self.assertEqual(34, tasks[0].order_id)
        self.assertEqual(34, tasks[1].order_id)
        self.assertEqual(35, tasks[2].order_id)
        self.assertEqual(35, tasks[3].order_id)
        self.assertEqual(None, tasks[4].order_id)

    def test_schedule_returns_tasks_for_each_sandwich_in_an_order_with_multiple_sandwiches(self):
        scheduler = CafeScheduler()

        order_items = [
            FoodItem(SANDWICH),
            FoodItem(SANDWICH),
            FoodItem(SANDWICH),
        ]
        scheduler.add_order(87, order_items)

        tasks = scheduler.schedule()

        expected_tasks = [
            Task(
                order_id=87,
                description='Make sandwich 1 for Order 87',
                start_time_seconds=0,
                task_type='MAKE_SANDWICH'
            ),
            Task(
                order_id=87,
                description='Make sandwich 2 for Order 87',
                start_time_seconds=150,
                task_type='MAKE_SANDWICH'
            ),
            Task(
                order_id=87,
                description='Make sandwich 3 for Order 87',
                start_time_seconds=300,
                task_type='MAKE_SANDWICH'
            ),
            Task(order_id=87, description='Serve Order 87', start_time_seconds=450, task_type='SERVE'),
            Task(order_id=None, description='Take a break', start_time_seconds=510, task_type='BREAK'),
        ]

        self.assertEqual(5, len(tasks))
        self.assertEqual(expected_tasks, tasks)

    def test_adding_an_order_updates_the_schedule(self):
        scheduler = CafeScheduler()

        scheduler.add_order(12, [FoodItem(SANDWICH)])
        tasks_1 = scheduler.schedule()

        scheduler.add_order(13, [FoodItem(SANDWICH)])
        tasks_2 = scheduler.schedule()

        self.assertNotEqual(tasks_1, tasks_2)
        self.assertEqual(3, len(tasks_1))
        self.assertEqual(5, len(tasks_2))

    def test_non_sandwich_order_items_are_ignored_by_schedule(self):
        scheduler = CafeScheduler()

        order_items = [
            FoodItem(SANDWICH),
            FoodItem(SNACK),
            FoodItem(DRINK),
        ]
        scheduler.add_order(12, order_items)
        tasks = scheduler.schedule()

        expected_tasks = [
            Task(order_id=12, description='Make sandwich 1 for Order 12', start_time_seconds=0, task_type='MAKE_SANDWICH'),
            Task(order_id=12, description='Serve Order 12', start_time_seconds=150, task_type='SERVE'),
            Task(order_id=None, description='Take a break', start_time_seconds=210, task_type='BREAK'),
        ]

        self.assertEqual(3, len(tasks))
        self.assertEqual(expected_tasks, tasks)

    def test_printable_schedule_returns_schedule_as_a_string(self):
        scheduler = CafeScheduler()

        scheduler.add_order(34, [FoodItem(SANDWICH)])
        scheduler.add_order(35, [FoodItem(SANDWICH)])

        printable_schedule = scheduler.printable_schedule()

        expected_output = (
            "1.\t00:00\tMake sandwich 1 for Order 34\n"
            "2.\t02:30\tServe Order 34\n"
            "3.\t03:30\tMake sandwich 1 for Order 35\n"
            "4.\t06:00\tServe Order 35\n"
            "5.\t07:00\tTake a break"
        )
        self.assertEqual(expected_output, printable_schedule)
