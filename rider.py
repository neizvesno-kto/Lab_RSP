from typing import List
from equipment.equipment import Equipment

class Rider:
    def __init__(self, name: str):
        self._name = name
        self._equipment_list: List[Equipment] = []
    #Полиморфизм
    def add_equipment(self, item: Equipment):
        self._equipment_list.append(item)

    def total_cost(self) -> float:
        return sum(item.price for item in self._equipment_list)

    def sort_by_weight(self):
        self._equipment_list.sort(key=lambda e: e.weight)

    def find_by_price_range(self, min_price: float, max_price: float) -> List[Equipment]:
        return [e for e in self._equipment_list if min_price <= e.price <= max_price]
    #Инкапсуляция
    def show_equipment(self):
        for item in self._equipment_list:
            print(item)
