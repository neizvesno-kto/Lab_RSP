import socket
import threading
import struct

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002

RELAY_HOST = "127.0.0.1"
RELAY_PORT = 6002

# UDP
MCAST_GRP = '233.0.0.1'
MCAST_PORT = 1502


def udp_listener():
    """Принимает UDP сообщения"""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp.bind(('', MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    udp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, _ = udp.recvfrom(4096)
        text = data.decode()
        print("\n[RELAY] UDP получено сообщение:\n", text)


def handle_final_client(conn, addr, server_socket):
    print(f"[RELAY] Final client connected: {addr}")
    while True:
        data = server_socket.recv(4096)
        if not data:
            break
        conn.sendall(data)
    conn.close()


def relay_server(server_socket):
    # TCP сервер для клиентов
    relay = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay.bind((RELAY_HOST, RELAY_PORT))
    relay.listen()

    print(f"[RELAY] Relay node running {RELAY_HOST}:{RELAY_PORT}")

    # Запуск UDP поток
    threading.Thread(target=udp_listener, daemon=True).start()

    while True:
        final_conn, final_addr = relay.accept()
        threading.Thread(
            target=handle_final_client,
            args=(final_conn, final_addr, server_socket)
        ).start()


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_HOST, SERVER_PORT))

    keyword = input("Введите слово для фильтрации: ")
    server_socket.send(keyword.encode())

    relay_server(server_socket)


if __name__ == "__main__":
    main()
