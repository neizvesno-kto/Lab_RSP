from rider import Rider

class Menu:
    def __init__(self, rider: Rider):
        self.rider = rider

    def start(self):
        while True:
            print("\n--- МЕНЮ ---")
            print("1. Показать экипировку")
            print("2. Посчитать общую стоимость")
            print("3. Сортировать по весу")
            print("4. Найти по диапазону цены")
            print("0. Выход")
            choice = input("Ваш выбор: ")

            if choice == "1":
                self.rider.show_equipment()
            elif choice == "2":
                print(f"Общая стоимость: {self.rider.total_cost():.2f} $")
            elif choice == "3":
                self.rider.sort_by_weight()
                print("Сортировка по весу выполнена.")
            elif choice == "4":
                min_p = float(input("Мин. цена: "))
                max_p = float(input("Макс. цена: "))
                found = self.rider.find_by_price_range(min_p, max_p)
                if found:
                    for eq in found:
                        print(eq)
                else:
                    print("Нет элементов в этом диапазоне.")
            elif choice == "0":
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор!")
