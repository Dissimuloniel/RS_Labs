import socket
import threading

BUFFER_SIZE = 1024

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            print(data.decode())
        except:
            break

    print("Соединение закрыто")
    conn.close()

def send_messages(conn, username):
    while True:
        message = input()
        full_message = f"{username}: {message}"
        try:
            conn.send(full_message.encode())
        except:
            break

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    print(f"Ожидание подключения на порту {port}...")
    conn, addr = server.accept()
    print(f"Подключён пользователь: {addr}")
    return conn

def connect_to_peer(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print("Успешное подключение")
    return client

def main():
    username = input("Введите ваше имя: ")
    listen_port = int(input("Введите порт для прослушивания: "))

    # запускаем сервер
    server_thread = threading.Thread(
        target=lambda: None
    )
    connection = None
    choice = input(
        "Подключиться к другому пользователю? (y/n): "
    ).lower()
    if choice == "y":
        ip = "127.0.0.1"
        port = int(input("Введите порт второго пользователя: "))
        connection = connect_to_peer(ip, port)
    else:
        connection = start_server(listen_port)
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(connection,),
        daemon=True
    )
    receive_thread.start()
    send_messages(connection, username)

if __name__ == "__main__":
    main()
