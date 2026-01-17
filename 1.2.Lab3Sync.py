import threading
import time

counter = 0
N_THREADS = 10

lock = threading.Lock()
condition = threading.Condition(lock)
turn = 0   # очередь потоков по номеру


def worker(thread_id):
    global counter, turn

    with condition:                      # <— lock захвачен
        while turn != thread_id:
            condition.wait()             # <— поток ждет своей очереди

        # === КРИТИЧЕСКАЯ СЕКЦИЯ (ПОД LOCK) ===
        counter += 1
        print(f"[Lock Thread {thread_id + 1}] counter = {counter}")

        # передаём ход следующему потоку
        turn += 1
        condition.notify_all()           # <— разбудить тот, кто следующий


def main():
    threads = []

    for i in range(N_THREADS):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nГотово. Итоговый counter =", counter)


if __name__ == "__main__":
    main()
