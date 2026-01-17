import threading
import time

class Pot:
    def __init__(self, capacity, total_savages, total_rounds):
        self.capacity = capacity      # порций в кастрюле
        self.pot = 0                  # текущее количество порций
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.served = set()           # дикари, которые уже поели в текущем раунде
        self.total_savages = total_savages
        self.round = 0
        self.total_rounds = total_rounds
        self.finished = False         # флаг окончания программы

    def eat(self, savage_id):
        with self.not_empty:
            while savage_id in self.served and not self.finished:
                self.not_empty.wait()

            if self.finished:
                return

            while self.pot == 0:
                # кастрюля пуста — вызываем повара
                self.round += 1
                if self.round > self.total_rounds:
                    self.finished = True
                    self.not_empty.notify_all()
                    return

                print(f"\nРаунд {self.round}: Повар наполняет кастрюлю ({self.capacity} порций)")
                self.pot = self.capacity
                self.served.clear()  # новый раунд — все дикари могут есть снова
                self.not_empty.notify_all()

            # дикарь берет порцию
            self.pot -= 1
            self.served.add(savage_id)
            print(f"Дикарь {savage_id} взял порцию, осталось {self.pot}. Уже поели: {sorted(self.served)}")

            self.not_empty.notify_all()

def savage_thread(pot, savage_id):
    while not pot.finished:
        time.sleep(0.05)  # имитация задержки
        pot.eat(savage_id)

if __name__ == "__main__":
    NUM_SAVAGES = 10
    POT_CAPACITY = 5
    TOTAL_ROUNDS = 2  # задаём количество раундов
    pot = Pot(POT_CAPACITY, NUM_SAVAGES, TOTAL_ROUNDS)

    threads = []
    for i in range(NUM_SAVAGES):
        t = threading.Thread(target=savage_thread, args=(pot, i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\nВсе раунды завершены. Каждый дикарь поел поровну.")
