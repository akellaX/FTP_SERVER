import socket
import os
import time

def file2server(filename, sock):
    with open(filename, 'rb') as f:
        bytesToSend = f.read(1024)
        sock.send(bytesToSend)
        while bytesToSend != "":
            bytesToSend = f.read(1024)
            sock.send(bytesToSend)
    confirm = sock.recv(1024).decode()
    print(confirm)
    sock.close()
    
def sendfile(filename, s):
    if not os.path.isfile(filename): return -1
    s.send(filename.encode())
    s.send(str(os.path.getsize(filename)).encode())
    file2server(filename, s)
    return 0

def getFiles(s):
    filelist = s.recv(2048).decode().split("#")
    print(filelist)
    

def Main():
    host = '127.0.0.1'
    port = 5000
    mode = 'getfiles'

    s = socket.socket()
    s.connect((host, port))



    filename = input("Filename? -> ")

    if filename != 'q' and mode == 'getfiles':
        getFiles(s)

    if filename != 'q' and mode == 'upload':
        sendfile(filename, s)

    if filename != 'q' and mode == 'download':
        s.send(filename.encode())
        data = s.recv(1024).decode()
        print(data)
        if data[:6] == 'EXISTS':
            filesize = int(data[6:])
            message = input("File exists, " + str(filesize) + "Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                message = 'OK'
                s.send(message.encode())
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
                print("Download Complete!")
                f.close()
        else:
            print("File Does Not Exist!")

    s.close()


if __name__ == '__main__':
    Main()