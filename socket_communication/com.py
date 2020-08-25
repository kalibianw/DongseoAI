# server ip: 192.168.43.5

import socket
import threading
from spam_ai.use_model import is_spam


def binder(client_socket, addr):
    print("Connected by ", addr)
    try:
        while True:
            data = client_socket.recv(4)
            length = int.from_bytes(data, "little")
            data = client_socket.recv(length)
            msg = data.decode()
            # print("Received from ", addr, msg)
            print(msg)
            print(type(msg))
            result = is_spam(msg)       # if result is True: spam, else: ham
            if result is True:
                print("Spam")
            elif result is False:
                print("Ham")
            msg = "echo: " + msg
            data = msg.encode()
            length = len(data)
            client_socket.sendall(length.to_bytes(4, byteorder="little"))

            client_socket.sendall(data)
            client_socket.close()

    except Exception as e:
        print(e)
        print("Except: ", addr)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", 9999))
server_socket.listen()

try:
    while True:

        client_socket, addr = server_socket.accept()

        print(addr)
        th = threading.Thread(target=binder, args=(client_socket, addr))

        th.start()

except:
    print("server")

finally:
    server_socket.close()
