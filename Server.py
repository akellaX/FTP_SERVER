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

def downloadFile(name, sock):
    # TODO: проерка название файла на повторы
    filename = sock.recv(1024).decode()
    filesize = sock.recv(1024).decode()
    print(filename)
    print(filesize)
    # f = open('new_' + filename, 'wb')
    # data = sock.recv(1024)
    # totalRecv = len(data)
    # f.write(data)
    # while totalRecv < filesize:
    #     data = sock.recv(1024)
    #     totalRecv += len(data)
    #     f.write(data)
    #     print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
    # print("Download Complete!")
    # f.close()
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
        # t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t = threading.Thread(target=downloadFile, args=("DownloadThread", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()