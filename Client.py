import socket
import os
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def file2server(filename, sock):
    with open(filename, 'rb') as f:
        bytesToSend = f.read(1024)
        sock.send(bytesToSend)
        while bytesToSend != b'':
            print (bytesToSend)
            bytesToSend = f.read(1024)
            sock.send(bytesToSend)
    confirm = sock.recv(1024).decode()
    print(confirm)
    sock.close()
    
def sendfile(filename, s):
    print (filename)
    # if not os.path.isfile(filename): return -1
    s.send((filename).encode())
    print (filename.split(' ')[1])
    time.sleep(3)
    s.send(str(os.path.getsize(filename.split(' ')[1])).encode())
    file2server(filename.split(' ')[1], s)
    # return 0

def getFiles(s):
    print ('try get files')
    s.send('dir'.encode())
    filelist = s.recv(2048).decode().split("#")
    for f in filelist: print(f)
    

def Main():
    host = '127.0.0.1'
    port = 5000

    

    while True:

        s = socket.socket()
        s.connect((host, port))

        # cls()  

        print ('-----AWESOME FTP CLIENT ver. 1.3.3.7-----')
        print ('host: {} | port: {}'.format(host, port))
        print ('-'*41)
        
        getFiles(s)

        print ('-'*41)
        

        mode = input("enter command? -> ")

        if mode == 'help':
            print ('help shows this message')
            print ('exit to exit')
            # print ('ls to show directory')
            print ('put [filename] to upload file on server')
            print ('get [filename] to download file from serever')
            print ('cls to clear terminal')

        elif mode == 'cls':
            cls()
            continue

        elif mode == 'exit':
            break

        # if mode == 'ls':
        #     getFiles(s)
        #     continue

        elif mode[:3] == 'put':
            # filename = input("Filename? -> ")
            sendfile(mode, s)

        elif mode[:3] == 'get':
            print (mode)
            # filename = input("Filename? -> ")
            s.send(mode.encode())
            data = s.recv(1024).decode()
            filename = mode.split(' ')[1]
            print (filename)
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

        else:
            continue

        s.close()



if __name__ == '__main__':
    Main()