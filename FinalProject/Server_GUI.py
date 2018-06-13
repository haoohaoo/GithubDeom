import socket
import threading
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)
#from InitDB import DataBaseChatRoom as db
import socket
import threading
import time
from pymongo import MongoClient
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
        massage1 = ("SYSTEM: "+nickname+ " in the chat room")
        global a
        a+=1
        myconnection.send(("SYSTEM: " + str(a) + " people in the chat room").encode())
        for c in self.mylist:
            if c.fileno() != connNumber:
                try:
                    c.send(massage1.encode())
                except:
                    pass
                massage2 = ("SYSTEM: " + str(a) + " people in the chat room")
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
                                c.send("SYSTEM: " + nickname.encode()+"b is leave chat room")
                                c.send("SYSTEM: " + str(a) + " people in the chat room")
                                #Client_GUI.MainWindow.labe_Number_of_people.setText("目前聊天室有" + str(a) + "人")
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

# def main():
#     s = Server('140.138.145.25', 5550)
#     while True:
#         s.checkConnection()

##########################

class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.client = MongoClient('localhost', 27017)  # 比较常用
        self.database = self.client["ChatRoom"]  # SQL: Database Name
        self.collection = self.database["user"]
        # s = Server('140.138.145.25', 5550)
        # while True:
        #     s.checkConnection() # 連線~~
        self.setupUi()
        self.show()
        th1 = threading.Thread(target=self.connect)
        th1.setDaemon(True)
        th1.start()
        th1.join

    def setupUi(self):
        self.resize(500,400)
        self.setWindowTitle("Chat Application")

        self.label = QLabel()               #show name lable
        self.label.setText("Nickname: ")

        self.labe2 = QLabel()               #show Password lable
        self.labe2.setText("Password: ")


        self.button_Login = QPushButton()
        self.button_Login.setStyleSheet("background-color: yellow")#button yellow
        self.button_Login.setText("Add")

        self.button_cancel = QPushButton()
        self.button_cancel.setStyleSheet("background-color: yellow")#button yellow
        self.button_cancel.setText("Del")

        #self.button_cancel = QPushButton("Send") # b3不可按
        #self.button_cancel.setEnabled(False)
        #self.button_Login.setEnabled(True)

        self.name = QLineEdit()
        self.Password = QLineEdit()
        self.Password.setEchoMode(QLineEdit.Password)#讓輸入的字變成 ***

        self.showchat = QTextEdit()#show內容
        self.chat = QLineEdit()#輸入內容

        self.passwprd = QLineEdit()

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(49, 39, 201, 211))
        self.groupBox.setObjectName("groupBox")
        i = 0
        for user in self.collection.find():
            i += 1
            self.checkBox = QtWidgets.QCheckBox(self.groupBox)
            self.checkBox.setGeometry(QtCore.QRect(30, 0 + i * 30, 85, 19))
            self.checkBox.setObjectName(user['uname'])
            self.checkBox.setText(user['uname'])

        #th_for_users = threading.Thread(target=self.users)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(self.label, 0, 1)    #name_lable
        grid.addWidget(self.name, 0, 2)     #name input

        grid.addWidget(self.labe2, 0, 3)    #password_lable
        grid.addWidget(self.Password, 0, 4) #password_lable

        grid.addWidget(self.button_Login, 1, 1,1,4) #login_button
        grid.addWidget(self.groupBox, 4, 0, 6, 5)

        #grid.addWidget(self.showchat, 4, 0, 6, 5)   #showchat
        #grid.addWidget(self.chat, 5, 0, 5, 5)
        grid.addWidget(self.button_cancel, 8, 0, 5, 5)

        self.setLayout(grid)
        self.button_Login.clicked.connect(self.login)
        self.button_cancel.clicked.connect(self.delete)


    def login(self):
        # 取得 輸入的 nickname
        text1=self.name.text()
        text2=self.Password.text()
        self.collection.insert_one({'uname': text1, 'upwd': text2})
        self.name.setText("")
        self.Password.setText("")

        i = 0;
        for a in self.groupBox.findChildren(QtWidgets.QCheckBox):
            i += 1

        self.newCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.newCheckBox.setGeometry(QtCore.QRect(30,1 + i * 30, 85, 19))
        self.newCheckBox.setObjectName(text1)
        self.newCheckBox.setText(text1)

        self.show()


    def delete(self):
        i=0;
        for a in self.groupBox.findChildren(QtWidgets.QCheckBox):
            i+=1
            a.setGeometry(QtCore.QRect(30, 0 + i * 30, 85, 19))
            if(a.isChecked()):
                #print(a.text())
                i-=1
                self.collection.delete_one({'uname': a.text()})
                a.deleteLater()
        self.show()

    def connect(self):
        s = Server('192.168.43.50', 5550)
        while True:
            s.checkConnection()


# class DataBaseChatRoom:
#     def __init__(self):
#         self.client = MongoClient('localhost', 27017)  # 比较常用
#         self.database = self.client["ChatRoom"]  # SQL: Database Name
#         self.collection = self.database["user"]  # SQL: Table Name
#
#     def loadData(self):
#         pass
#         return None
#
#     # delete user by uname
#     # dbChatRoom.deleteUser(['A'])
#     def deleteUser(self, username):
#         self.collection.DataBaseChatRoom.delete_one({'uname':username})
#         pass
#         return 'successful'
#
#     # insert user
#     # dbChatRoom.insertUser(uname='A', upwd='A')
#     def insertUser(self, username, userkey):
#         self.collection.insert_one({'uname': username, 'upwd': userkey})
#         pass
#         return 'successful'
#
#     def updataUser(self, username, userkey):
#         self.collection.ChatRoom.user.save({'uname': username, 'upwd': userkey})
#         pass
#         return 'successful'
#
#     # check checkUserExist
#     def checkUserExist(self, uname='A'):
#         pass
#         return False
#
#     # query user bu uname
#     # dbChatRoom.queryByuname(uname='A', upwd='A')
#     def queryByuname(self, uname='A', upwd='A'):
#         pass
#         return False
#
#     # Init database
#     # dbChatRoom.Initdatabase()
#     def Initdatabase(self):
#         userList = []
#         # userList.append({'uname': 'A', 'upwd': 'A'})
#         # userList.append({'uname': 'B', 'upwd': 'B'})
#         # userList.append({'uname': 'C', 'upwd': 'C'})
#         # userList.append({'uname': 'D', 'upwd': 'D'})
#         # userList.append({'uname': 'E', 'upwd': 'E'})
#         self.collection.insert_many(userList)
#
#     def colseClient(self):
#         self.client.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myPanel = MainWindow()
    sys.exit(app.exec_())
