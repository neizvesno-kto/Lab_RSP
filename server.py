import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5002
MESSAGE_FILE = "messages.txt"

# UDP 224–239
MCAST_GRP = "233.0.0.1"
MCAST_PORT = 1502


def load_messages():
    try:
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def filter_messages(messages, keyword):
    if not keyword:
        return messages
    return [msg for msg in messages if keyword.lower() in msg.lower()]


def udp_multicast_sender():
    """ВСЕ сообщения UDP multicast"""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    while True:
        try:
            messages = load_messages()
            if not messages:
                msg = "Нет сообщений"
            else:
                msg = "\n".join(messages)

            udp.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
            print("[SERVER] UDP multicast отправлен")
        except Exception as e:
            print("UDP Error:", e)

        time.sleep(10)


def handle_client(conn, addr):
    print(f"[SERVER] Connected: {addr}")

    keyword = conn.recv(1024).decode().strip()
    print(f"[SERVER] Filter keyword from {addr}: '{keyword}'")

    while True:
        all_messages = load_messages()
        filtered = filter_messages(all_messages, keyword)
        last_5 = filtered[-5:]

        data_to_send = "\n".join(last_5) if last_5 else "Нет сообщений"
        conn.sendall(data_to_send.encode())

        time.sleep(2)


def start_server():
    # Запуск UDP поток
    threading.Thread(target=udp_multicast_sender, daemon=True).start()

    # TCP сервер
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] Server running {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()
