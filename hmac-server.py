import asyncio
import websockets
import hashlib
import hmac

HOST = "localhost"
PORT = 1234
SECRET_KEY = b"supersecret"

def generate_hmac(message, key):
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

async def handle_client(websocket):
    print("Клиент подключился.")
    
    await websocket.send("Добро пожаловать на сервер HMAC!")

    data = await websocket.recv()
    message, received_hmac = data.split(",")

    expected_hmac = generate_hmac(message, SECRET_KEY)

    if hmac.compare_digest(received_hmac, expected_hmac):
        response = "Аутентификация успешна!"
    else:
        response = "Ошибка аутентификации!"
    
    await websocket.send(response)
    print(f"Клиент отправил: {message}")
    print(f"Ожидаемый HMAC: {expected_hmac}")
    print(f"Полученный HMAC: {received_hmac}")

async def main():
    server = await websockets.serve(handle_client, HOST, PORT)
    print(f"Сервер запущен на {HOST}:{PORT}")
    await server.wait_closed()

asyncio.run(main())