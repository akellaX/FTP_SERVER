import socket


def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    filename = input("Filename? -> ")
    if filename != 'q':
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