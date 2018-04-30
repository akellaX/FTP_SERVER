import socket
import threading
import os

def RetrFile(sock, filename):
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

def downloadFile(sock, filename):
    # TODO: проерка название файла на повторы
    print (filename)
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

def sendListFiles(sock):
    filelist = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
    filelist = "#".join(filelist)
    print(filelist)
    sock.send(filelist.encode())

def listenCommand(name, sock):
    while True:
        command = sock.recv(1024).decode()
        print (command)
        command = command.split(" ")
        print(command)
        if command[0].lower() == 'dir':
            sendListFiles(sock)
        elif command[0].lower() == 'get':
            RetrFile(sock, command[1])
        elif command[0].lower() == 'put':
            downloadFile(sock, command[1])
        elif command[0].lower() == 'close':
            break
        else:
            print ('no such command')



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
        t = threading.Thread(target=listenCommand, args=("listenThread", c))
        t.start()

    s.close()


if __name__ == '__main__':
    Main()