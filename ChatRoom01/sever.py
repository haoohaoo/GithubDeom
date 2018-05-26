# -*- encoding: utf-8 -*-
import socket
import threading
import time
from time import gmtime, strftime
a = 0
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
                mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
                mythread.setDaemon(True)
                mythread.start()

            else:
                connection.send(b'please go out!')
                connection.close()
        except:
            pass

    def subThreadIn(self, myconnection, connNumber):
        myconnection.send(b'Welcome to chat room!\nPleace input your nick name:')
        nickname = myconnection.recv(1024).decode()
        massage = ("Now lets chat, " +nickname)
        self.mylist.append(myconnection)
        myconnection.send(massage.encode())
        massage1 = ("\t\tSYSTEM: "+nickname+ " in the chat room")
        global a
        a+=1
        for c in self.mylist:
            if c.fileno() != connNumber:
                try:
                    c.send(massage1.encode())
                except:
                    pass
                massage2 = ("\t\tSYSTEM: " + str(a) + " people in the chat room")
                c.send(massage2.encode())
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    self.tellOthers(connNumber, recvedMsg,nickname)
                else:
                    pass

            except (OSError, ConnectionResetError):
                try:
                    # 將總數-1
                    a-=1
                    # 在server 印出誰離開
                    print('One connecting is leave', myconnection.getsockname(), myconnection.fileno())
                    #在其他client 告知誰離開
                    for c in self.mylist:
                        if c.fileno() != connNumber:
                            try:
                                c.send(b'\t\tSYSTEM: ' + nickname.encode()+b' is leave chat room')
                                c.send(b'\t\tSYSTEM: ' + str(a).encode() +b' people in the chat room')
                            except:
                                pass


                    self.mylist.remove(myconnection)
                except:
                    pass

                myconnection.close()
                return

    # send whatToSay to every except people in exceptNum
    def tellOthers(self, exceptNum, whatToSay,nickname):
        for c in self.mylist:
            if c.fileno() != exceptNum:
                st = time.localtime(time.time())
                times = time.strftime('[%H:%M:%S]', st)
                massage = (nickname+ ":" +whatToSay + "     " + times)
                try:
                    c.send(massage.encode())
                except:
                    pass

def main():
    s = Server('127.0.0.1', 5550)
    while True:
        s.checkConnection()


if __name__ == "__main__":
    main()

