#!/usr/bin/env python
# PAP client
import asyncio
import websockets
import hashlib


def gen_sha256_hmac(message, key):
    '''
    Source: https://ru.wikipedia.org/wiki/HMAC
    '''

    blocksize = 64

    # aka ipad
    trans_5C = bytes((x ^ 0x5C) for x in range(256))

    # aka opad
    trans_36 = bytes((x ^ 0x36) for x in range(256))

    key_hex = key.encode().hex()[2:]

    # Convert hex key to bytes object
    key_bytes = bytes.fromhex(key_hex)

    # Add a zero-bytes padding to apply to blocksize
    key_bytes = key_bytes.ljust(blocksize, b'\0')

    # Xor each byte with 0x36 constant
    xored_key_bytes_ipad = key_bytes.translate(trans_36)

    # H( ( K ⊕  ipad ) || text ) with SHA-256
    h1 = hashlib.sha256(xored_key_bytes_ipad + message.encode())

    # Xor each byte with 0x5C constant
    xored_key_bytes_opad = key_bytes.translate(trans_5C)

    # H( ( K ⊕ opad ) || H(...) ) with SHA-256
    return hashlib.sha256(xored_key_bytes_opad + h1.digest()).hexdigest()


async def try_auth():
    uri = "ws://localhost:1234"
    async with websockets.connect(uri) as websocket:
        shared_key = "supersecret"
        message = "Hello from Marian"

        welcome_message = await websocket.recv()
        print(f"Server answered: {welcome_message}")

        message_HMAC = gen_sha256_hmac(message, shared_key)

        print(f"I send message '{message}' with HMAC '{message_HMAC}' based on password '{shared_key}'")
        client_data = f"{message},{message_HMAC}"
        await websocket.send(client_data)

        answer = await websocket.recv()
        print(answer)

# Запускаем event loop правильно для Python 3.11+
asyncio.run(try_auth())
