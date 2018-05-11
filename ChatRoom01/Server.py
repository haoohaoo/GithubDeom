# -*- encoding: utf-8 -*-
import socket
import threading
from time import gmtime, strftime

class Server:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.bind((host, port))
        self.sock.listen(5)
        print('Server', socket.gethostbyname(host), 'listening ...')
        self.mylist = list()

    def checkConnection(self):
        connection, addr = self.sock.accept()
        print('Accept a new connection', connection.getsockname(), connection.fileno())

        try:
            buf = connection.recv(1024).decode()
            if buf == '1':
                # start a thread for new connection
                connection.send(b'Welcome to chat room!\nPleace input your nick name:')
                nickname = connection.recv(1024).decode()
                connection.send(b'Now lets chat'+nickname)
                mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno(),nickname))
                mythread.setDaemon(True)
                mythread.start()

            else:
                connection.send(b'please go out!')
                connection.close()
        except:
            pass

    # send whatToSay to every except people in exceptNum
    def tellOthers(self, exceptNum, whatToSay,nickname):
        for c in self.mylist:
            if c.fileno() != exceptNum:
                massage = (nickname+ ":" +whatToSay);
                try:
                    c.send(massage.encode())
                except:
                    pass

    def subThreadIn(self, myconnection, connNumber,nickname):
        self.mylist.append(myconnection)
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    self.tellOthers(connNumber, recvedMsg,nickname)
                else:
                    pass

            except (OSError, ConnectionResetError):
                try:
                    self.mylist.remove(myconnection)
                except:
                    pass

                myconnection.close()
                return


def main():
    s = Server('140.138.145.24', 5550)
    while True:
        s.checkConnection()


if __name__ == "__main__":
    main()

