import socket

HOST = "127.0.0.1"
PORT = 6002   # подключаемся к реле


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print("Connected to relay server.")
    #каждый новый клиент получает временный порт TCP
    while True:
        data = client.recv(4096).decode()
        print("\n--- Последние сообщения ---")
        print(data)


if __name__ == "__main__":
    main()
