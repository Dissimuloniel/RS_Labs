import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Сервер запущен и ожидает подключения...")

while True:
    conn, addr = server.accept()
    print(f"Подключен клиент: {addr}")

    data = conn.recv(1024).decode()

    if data:
        print("Получен запрос:", data)

        # обработка запроса
        response = f"Сервер получил сообщение: {data.upper()}"

        conn.send(response.encode())

    conn.close()
