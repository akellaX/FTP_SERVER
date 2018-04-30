import socket
import threading
import os
import time


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
        sock.send("ERR ".decode())

    sock.close()

def downloadFile(name, sock):
    # TODO: проерка название файла на повторы
    filename = sock.recv(1024).decode()
    filesize = int(sock.recv(1024).decode())
    f = open('new_' + filename, 'wb')
    data = sock.recv(1024)
    totalRecv = len(data)
    f.write(data)
    while totalRecv < filesize:
        data = sock.recv(1024)
        totalRecv += len(data)
        f.write(data)
        print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
    print("Download Complete!")
    sock.send("COMPLETE".encode())
    f.close()
    sock.close()

def sendListFiles(name, sock):
    filelist = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
    filelist = "#".join(filelist)
    print(filelist)
    sock.send(filelist.encode())

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
        # t = threading.Thread(target=downloadFile, args=("DownloadThread", c))
        t = threading.Thread(target=sendListFiles, args=("ListThread", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()