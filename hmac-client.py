import asyncio
import websockets
import hashlib
import hmac

HOST = "localhost"
PORT = 1234
SECRET_KEY = b"supersecret"
MESSAGE = "Hello from Marian"

def generate_hmac(message, key):
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

async def connect_to_server():
    uri = f"ws://{HOST}:{PORT}"
    async with websockets.connect(uri) as websocket:
        welcome_message = await websocket.recv()
        print(f"Сервер: {welcome_message}")

        message_hmac = generate_hmac(MESSAGE, SECRET_KEY)
        client_data = f"{MESSAGE},{message_hmac}"

        await websocket.send(client_data)

        response = await websocket.recv()
        print(f"Сервер: {response}")

asyncio.run(connect_to_server())
