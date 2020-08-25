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
                result = str(1)
            elif result is False:
                print("Ham")
                result = str(0)
            # msg = "echo: " + msg
            # data = msg.encode()
            length = len(result)
            print("Sending length.to_bytes")
            client_socket.sendall(length.to_bytes(4, byteorder="little"))
            print("Sending result.encode()")
            client_socket.sendall(result.encode())
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
