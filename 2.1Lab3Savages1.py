import threading
import time
import random

class Pot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.servings = capacity
        self.lock = threading.Lock()

    def get_serving(self, savage_id):
        with self.lock:
            if self.servings == 0:
                print("Повар наполняет кастрюлю")
                self.servings = self.capacity
            self.servings -= 1
            print(f"Дикарь {savage_id} взял порцию, осталось {self.servings}")

def savage(pot, savage_id, eat_twice=False):
    times = 2 if eat_twice else 1
    for _ in range(times):
        pot.get_serving(savage_id)
        time.sleep(0.01)  # время на поедание

def main():
    N_pot = 5
    savage_ids = list(range(5))
    pot = Pot(N_pot)

    # случайный порядок дикарей
    random.shuffle(savage_ids)

    # случайно выбираем дикаря, который съест 2 порции
    lucky_savage = random.choice(savage_ids)

    threads = []
    for savage_id in savage_ids:
        eat_twice = (savage_id == lucky_savage)
        t = threading.Thread(target=savage, args=(pot, savage_id, eat_twice))
        threads.append(t)
        t.start()
        time.sleep(0.01)  # контроль очередности

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
