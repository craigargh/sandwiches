# sandwiches
A small project to model the schedule of a sandwich shop

## Decisions

When designing and developing the sandwiches library, I made the following decisions that are not included in the task specification:

1. As the library is meant to be used by a separate application, it needed to be agnostic of any DB. This means that it does not use a DB and only stores data in memory. It is possible to extend the library so that it can be used with a DB, but this is not implemented.
2. Since the library has no DB or Web API I only included unit tests, no integration or end-to-end tests.
3. Each order can have multiple sandwiches. When scheduling tasks each sandwich in an order is made before the order is served
4. The output format of the schedule has been changed slightly. The text for sandwich making tasks uses this format `'Make sandwich 1 for Order 12'` and the serve task follows this format `'Serve Order 12'`. Each time a new order is processed the sandwich number restarts from 1.
5. It is possible to add drinks and snacks to the order, but they will not appear on the sandwich making schedule.
6. Code only uses modules in the Python standard library. There are no extra installation requirements beyond a standard Python installation.

## Usage

The library uses the `CafeScheduler` class to record all orders:

```python
from sandwiches.scheduler import CafeScheduler

scheduler = CafeScheduler()
```

### Adding Orders

To add an order to the schedule:

```python
from sandwiches.scheduler import CafeScheduler
from sandwiches.constants import SANDWICH


scheduler = CafeScheduler()

scheduler.add_order(order_number=1, items=[SANDWICH])
```

You can add multiple orders to the same schedule and each order can contain multiple sandwiches:

```python
from sandwiches.scheduler import CafeScheduler
from sandwiches.constants import SANDWICH


scheduler = CafeScheduler()

scheduler.add_order(order_number=1, items=[SANDWICH, SANDWICH])
scheduler.add_order(order_number=2, items=[SANDWICH, SANDWICH, SANDWICH])
scheduler.add_order(order_number=3, items=[SANDWICH])
```

You can also add drinks and snacks to orders, but they will not appear on the sandwich making schedule:

```python
from sandwiches.scheduler import CafeScheduler
from sandwiches.constants import SANDWICH, DRINK, SNACK


scheduler = CafeScheduler()

order_items = [SANDWICH, SANDWICH, DRINK, SNACK]
scheduler.add_order(order_number=1, items=order_items)
```

### Schedule Output

To return the order as a list of `Task` objects use the `schedule()` method:

```python
from sandwiches.scheduler import CafeScheduler
from sandwiches.constants import SANDWICH


scheduler = CafeScheduler()
scheduler.add_order(order_number=1, items=[SANDWICH])

tasks = scheduler.schedule()
```

Tasks are sorted in order that they need to be completed and each task has the following attributes:

```python
order_id: int
description: str
task_type: str
start_time_seconds: int
```

You can also output the schedule as a string using the `printable_schedule()` method:

```python
from sandwiches.scheduler import CafeScheduler
from sandwiches.constants import SANDWICH


scheduler = CafeScheduler()
scheduler.add_order(order_number=1, items=[SANDWICH])

print(scheduler.printable_schedule())
```
This will output the schedule in the following format:

```csv
1.	00:00	Make sandwich 1 for Order 1
2.	02:30	Serve Order 1
3.	03:30	Take a break
```