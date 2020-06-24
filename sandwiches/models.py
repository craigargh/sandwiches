from dataclasses import dataclass
from typing import List


@dataclass
class FoodItem:
    item_type: str


@dataclass
class Order:
    order_id: int
    items: List[FoodItem]


@dataclass
class Task:
    order_id: int
    description: str
    start_time_seconds: int
