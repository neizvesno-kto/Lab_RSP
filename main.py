from rider import Rider
from utils.file_loader import load_equipment_from_file
from menu import Menu

def main():
    rider = Rider("Иван")
    equipment_list = load_equipment_from_file("resources/equipment.txt")

    for eq in equipment_list:
        rider.add_equipment(eq)

    menu = Menu(rider)
    menu.start()

if __name__ == "__main__":
    main()
