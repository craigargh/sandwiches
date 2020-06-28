from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    order_id: int
    items: List[str]


@dataclass
class Task:
    order_id: int
    description: str
    task_type: str
    start_time_seconds: int = None
