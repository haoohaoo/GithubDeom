import socket
import threading
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)
#from pymongo import MongoClient
import time


class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.link_to_server('127.0.0.1', 5550) # 連線~~
        self.setupUi()

        self.show()

        th1 = threading.Thread(target=self.sendThreadFunc)
        th2 = threading.Thread(target=self.recvThreadFunc)
        threads = [th1, th2]
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join

    # 連線~~
    def link_to_server(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

    def sendThreadFunc(self):
        while True:
            try:
                myword = input()
                self.sock.send(myword.encode())
            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                t = otherword.decode()
                self.showchat.append(t)
                if(" people in the chat room"in t):
                    size = len(t)-32
                    a = 0
                    for i in range(size):
                        b = size-i-1
                        if(b<=0):
                            a += (int(t[8]))
                        else:
                            a += (int(t[8]))*(10^(size-i-1))
                    self.labe_Number_of_people.setText("目前聊天室有" + str(a) + "人")

            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')


    def setupUi(self):
        self.resize(500,500)
        self.setWindowTitle("ChatRoom")

        self.labe_Number_of_people = QLabel()
        self.labe_Number_of_people.setStyleSheet("color: rgb(255,255,255)")
        self.labe_Number_of_people.setFont(QFont('SansSerif', 14))
        self.labe_Number_of_people.setText("目前聊天室有0人")         #目前人數lable

        self.label = QLabel()
        self.label.setText("Chat Name: ")


        self.button_Login = QPushButton()
        self.button_Login.setText("Enter")
        self.button_Login.setStyleSheet("background-color: rgb(255, 189, 255)")

        self.button_clear = QPushButton()
        self.button_clear.setText("Clear")
        self.button_clear.setStyleSheet("background-color: rgb(255, 189, 255)")

        self.button_cancel = QPushButton()
        self.button_cancel.setText("Send")

        self.button_cancel = QPushButton("Send") # b3不可按
        self.button_cancel.setStyleSheet("background-color: rgb(255, 189, 255)")
        self.button_cancel.setEnabled(False)
        self.button_Login.setEnabled(True)

        self.name = QLineEdit()
        self.showchat = QTextEdit()#show內容
        self.chat = QLineEdit()#輸入內容

        #設定顏色
        self.showchat.setStyleSheet("background-color: rgb(255,255,255)")
        self.chat.setStyleSheet("background-color: rgb(255,255,255)")
        self.name.setStyleSheet("background-color: rgb(255,255,255)")

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(self.labe_Number_of_people, 0, 1)        #秀出目前人數
        grid.addWidget(self.label, 1, 0)
        grid.addWidget(self.name, 1, 1)
        grid.addWidget(self.button_Login, 1, 3)
        grid.addWidget(self.button_clear, 1, 4)
        grid.addWidget(self.showchat, 4, 0, 3, 5)
        grid.addWidget(self.chat, 6, 0, 3, 4)
        grid.addWidget(self.button_cancel, 7, 4, 1, 1)


        self.setLayout(grid)
        self.button_Login.clicked.connect(self.login)
        self.button_cancel.clicked.connect(self.showText)

        # set black background
        #p = self.palette()
        #p.setColor(self.backgroundRole(), red)
        self.setStyleSheet("background-color:rgb(153,153,153);")

    def login(self):
        # 取得 輸入的 nickname
        text1 = self.name.text()
        find = False
        self.name.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_Login.setEnabled(False)
        self.sock.send(text1.encode())

    def showText(self):
        #　將值傳給server
        self.sock.send(self.chat.text().encode())
        #  同時將自己輸入的值印在chat上
        st = time.localtime(time.time())
        times = time.strftime('[%H:%M:%S]', st)
        self.showchat.append("\t" + times + self.chat.text() + " : You " )
        self.chat.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myPanel = MainWindow()
    sys.exit(app.exec_())
