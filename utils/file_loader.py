from equipment.helmet import Helmet
from equipment.jacket import Jacket
from equipment.gloves import Gloves
from equipment.boots import Boots
from typing import List
from equipment.equipment import Equipment
#полиморфизм
def load_equipment_from_file(file_path: str) -> List[Equipment]:
    equipment_list = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) != 4:
                    continue

                eq_type, name, price, weight = parts
                price = float(price)
                weight = float(weight)

                eq_type = eq_type.lower()
                if eq_type == "helmet":
                    equipment_list.append(Helmet(name, price, weight))
                elif eq_type == "jacket":
                    equipment_list.append(Jacket(name, price, weight))
                elif eq_type == "gloves":
                    equipment_list.append(Gloves(name, price, weight))
                elif eq_type == "boots":
                    equipment_list.append(Boots(name, price, weight))
    except FileNotFoundError:
        print("Файл не найден!")
    return equipment_list
