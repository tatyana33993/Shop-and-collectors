#!/usr/bin/env python
import socket
import rsa
from threading import Thread
import time
import random

input_code = 0


def get_codes():
    codes = []
    for i in range(7):
        codes.append(random.randint(1, 1000000))
    return codes


def worker():
    global input_code
    codes = get_codes()
    print(f'Коды для вызова инкассации: {codes}')

    with open('private.pem', mode='rb') as privatefile:
        keydata = privatefile.read()
    pubkey = rsa.PublicKey.load_pkcs1(keydata)

    sock = socket.socket()
    sock.connect(('localhost', 9090))

    str_codes = str(codes)
    enc_codes = rsa.encrypt(str_codes[1:len(str_codes) - 1].replace(',', '').encode(), pubkey)
    sock.send(enc_codes)

    t = time.time()
    while True:
        if time.time() - t > 30:
            if input_code != 0:
                enc_input_code = rsa.encrypt(str(input_code).encode(), pubkey)
                sock.send(enc_input_code)
                input_code = 0
            else:
                while True:
                    random_code = random.randint(1, 1000000)
                    if random_code not in codes:
                        enc_input_code = rsa.encrypt(str(random_code).encode(), pubkey)
                        sock.send(enc_input_code)
                        break
            t = time.time()


if __name__ == '__main__':
    Thread(target=worker).start()

    while True:
        str_input_code = input('>>')
        input_code = int(str_input_code)
