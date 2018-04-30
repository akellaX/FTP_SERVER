# import socket
# import os
# import threading
#
# def RetrFile(name, sock):
#     filename = sock.recv(1024)
#     if os.path.isfile(filename):
#         sock.send("Exists " + str(os.path.getsize(filename)))
#         userResponse = sock.recv(1024)
#         if userResponse[:2] == 'OK' :
#             with open(filename, 'rb') as f:
#                 bytesToSend = f.read(1024)
#                 sock.send(bytesToSend)
#                 while bytesToSend != '':
#                     bytesToSend = f.read(1024)
#                     sock.send(bytesToSend)
#     else:
#         sock.send("ERROR")
#
#     sock.close()
#
# def Main():
#     host = '127.0.0.1'
#     port = 5000
#
#     s = socket.socket()
#     s.bind((host, port))
#
#     s.listen(5)
#
#     print("SERVER STARTED")
#
#     while True:
#         c, addr = s.accept()
#         print('client connected i:<' + str(addr) + '>')
#         t = threading.Thread(target=RetrFile, args=("RetrThread", c))
#         t.start()
#
#     s.close()
#
#
# if __name__ == '__main__':
#     Main()

import socket
import threading
import os


def RetrFile(name, sock):
    filename = sock.recv(1024).decode()
    if os.path.isfile(filename):
        sock.send(("EXISTS " + str(os.path.getsize(filename))).encode())
        userResponse = sock.recv(1024).decode()
        print(userResponse)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ").decode()

    sock.close()


def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)

    print("Server Started.")
    while True:
        c, addr = s.accept()
        print("client connedted ip:<" + str(addr) + ">")
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()