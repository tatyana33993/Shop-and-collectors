#!/usr/bin/env python
import socket
import rsa

codes = []

if __name__ == '__main__':
    pubkey, privkey = rsa.newkeys(512)

    publicKeyPkcs1PEM = pubkey.save_pkcs1().decode()
    with open('private.pem', mode='wb') as privatefile:
        privatefile.write(publicKeyPkcs1PEM.encode())

    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()
    print(f'connected: {addr}')

    data = conn.recv(1024)
    dec_codes = rsa.decrypt(data, privkey).decode()
    print(dec_codes)
    codes = [int(x) for x in dec_codes.split(' ')]

    while True:
        data = conn.recv(1024)
        if not data:
            continue
        dec_code = rsa.decrypt(data, privkey).decode()
        print(dec_code)
        if int(dec_code) in codes:
            print('Инкассация выезжает')

    conn.close()
