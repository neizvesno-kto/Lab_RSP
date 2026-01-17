import threading
import time

# Параметры
NUM_INC_THREADS = 5
NUM_DEC_THREADS = 5
ITERATIONS = 100

# Общий счётчик
counter = 0
lock = threading.RLock()  # ReentrantLock Используется чтобы защитить счётчик от одновременного изменения потоками.


# Поток инкрементации
def inc_thread():
    global counter
    for _ in range(ITERATIONS):
        with lock:
            counter += 1
            print(f"[INC {threading.current_thread().name}] Промежуточный счётчик: {counter}")


# Поток декрементации
def dec_thread():
    global counter
    for _ in range(ITERATIONS):
        with lock:
            counter -= 1
            print(f"[DEC {threading.current_thread().name}] Промежуточный счётчик: {counter}")


# Основная функция
def main():
    global counter
    print("=== Запуск: С ReentrantLock ===")
    print(f"Ожидаемое значение счётчика: 0")
    print(f"Потоки инкрементации: {NUM_INC_THREADS}, потоки декрементации: {NUM_DEC_THREADS}")
    print(f"Итераций на поток: {ITERATIONS}\n")

    threads = []

    start_time = time.time()

    # Создаём потоки увеличения
    for _ in range(NUM_INC_THREADS):
        t = threading.Thread(target=inc_thread)
        threads.append(t)
        t.start()

    # Создаём потоки уменьшения
    for _ in range(NUM_DEC_THREADS):
        t = threading.Thread(target=dec_thread)
        threads.append(t)
        t.start()

    # Ждём завершения всех потоков
    for t in threads:
        t.join()

    end_time = time.time()

    print(f"\nИтоговый счётчик: {counter}")
    print(f"Время выполнения: {end_time - start_time:.4f} сек")
    if counter == 0:
        print(" Все потоки синхронизированы — результат правильный.")
    else:
        print(" Результат неправильный — гонка потоков!")


if __name__ == "__main__":
    main()
