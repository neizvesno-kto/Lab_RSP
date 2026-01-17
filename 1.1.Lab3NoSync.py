import threading
import time

counter = 0
ITERATIONS = 100
N_INC_THREADS = 5
N_DEC_THREADS = 5

lock = threading.Lock()
print_lock = threading.Lock()   # <<< новый лок для печати


def increment_no_lock():
    global counter
    for i in range(ITERATIONS):
        value = counter
        value += 1
        counter = value

        if i % 10 == 0:
            with print_lock:
                print(f"[NoSync INC] Промежуточный счётчик: {counter}")

        time.sleep(0.00005)


def decrement_no_lock():
    global counter
    for i in range(ITERATIONS):
        value = counter
        value -= 1
        counter = value

        if i % 10 == 0:
            with print_lock:
                print(f"[NoSync DEC] Промежуточный счётчик: {counter}")

        time.sleep(0.00005)


def increment_lock():
    global counter
    for i in range(ITERATIONS):
        with lock:
            counter += 1

        if i % 10 == 0:
            with print_lock:
                print(f"[Lock INC] Промежуточный счётчик: {counter}")

        time.sleep(0.00005)


def decrement_lock():
    global counter
    for i in range(ITERATIONS):
        with lock:
            counter -= 1

        if i % 10 == 0:
            with print_lock:
                print(f"[Lock DEC] Промежуточный счётчик: {counter}")

        time.sleep(0.00005)


def run_demo(variant):
    global counter
    counter = 0
    threads = []

    if variant == "1":
        inc_func, dec_func = increment_no_lock, decrement_no_lock
        title = "NoSync (гонка потоков)"
    elif variant == "2":
        inc_func, dec_func = increment_lock, decrement_lock
        title = "Sync (Lock)"
    else:
        print("Неверный вариант")
        return

    with print_lock:
        print(f"\n=== Запуск: {title} ===\n")

    start = time.time()

    for _ in range(N_INC_THREADS):
        t = threading.Thread(target=inc_func)
        threads.append(t)
        t.start()

    for _ in range(N_DEC_THREADS):
        t = threading.Thread(target=dec_func)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time()

    with print_lock:
        print(f"\nИтоговый счётчик: {counter}")
        print(f"Время выполнения: {end - start:.4f} сек")
        print("="*50)


def main():
    while True:
        print("\nВыберите вариант:")
        print("1 — NoSync (гонка) Гонка потоков, операции мешают друг другу")
        print("2 — Sync (Lock) Синхронизация решает проблему гонки")
        print("0 — Выход")
        choice = input("Введите вариант: ").strip()
        if choice == "0":
            break
        run_demo(choice)


if __name__ == "__main__":
    main()
