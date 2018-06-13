import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)
from pymongo import MongoClient
import time


class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.link_to_server('192.168.43.50', 5550) # 連線~~
        self.setupUi()
        self.show()

        th1 = threading.Thread(target=self.sendThreadFunc)
        th2 = threading.Thread(target=self.recvThreadFunc)
        threads = [th1, th2]
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join

        self.client = MongoClient('localhost', 27017)  # 比较常用
        self.database = self.client["ChatRoom"]  # SQL: Database Name
        self.collection = self.database["user"]
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
        self.setWindowTitle("Chat Application")

        self.labe_Number_of_people = QLabel()
        self.labe_Number_of_people.setText("目前聊天室有0人")         #目前人數lable

        self.label = QLabel()
        self.label.setText("Nickname: ")

        self.labe2 = QLabel()
        self.labe2.setText("Change Password: ") #show Password lable


        self.button_Login = QPushButton()
        self.button_Login.setText("Login")
        self.button_Login.setStyleSheet("background-color: yellow")#button yellow
        self.change_P = QPushButton()
        self.change_P.setText("update password")
        self.change_P.setStyleSheet("background-color: red")#button yellow

        self.button_cancel = QPushButton()
        self.button_cancel.setText("Send")

        self.button_cancel = QPushButton("Send") # b3不可按
        self.button_cancel.setStyleSheet("background-color: yellow")#button yellow
        self.button_cancel.setEnabled(False)
        self.button_Login.setEnabled(True)

        self.name = QLineEdit()
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.Password)#讓輸入的字變成 ***
        self.change_passwd = QLineEdit()
        self.change_passwd.setEchoMode(QLineEdit.Password)#讓輸入的字變成 ***
        self.showchat = QTextEdit()#show內容
        self.chat = QLineEdit()#輸入內容


        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(self.labe_Number_of_people, 0, 1)        #秀出目前人數
        grid.addWidget(self.label, 1, 0)
        grid.addWidget(self.name, 1, 1)
        grid.addWidget(self.passwd, 1, 2)
        grid.addWidget(self.button_Login, 1, 3)
        grid.addWidget(self.labe2, 2, 0)
        grid.addWidget(self.change_passwd, 2, 2)
        grid.addWidget(self.change_P, 2, 3)
        grid.addWidget(self.showchat, 4, 0, 3, 3)
        grid.addWidget(self.chat, 6, 0, 5, 3)
        grid.addWidget(self.button_cancel, 7, 0, 6, 3)


        self.setLayout(grid)
        self.button_Login.clicked.connect(self.login)
        self.change_P.clicked.connect(self.change_pwd)
        self.button_cancel.clicked.connect(self.showText)

    def login(self):
        # 取得 輸入的 nickname
        text1 = self.name.text()
        text2 = self.passwd.text()
        find = False
        for user in self.collection.find():
            if(user['uname']==text1):
                find = True
                if(user['upwd']==text2):
                    self.name.setEnabled(False)
                    self.passwd.setEnabled(False)
                    self.button_cancel.setEnabled(True)
                    self.button_Login.setEnabled(False)
                    self.sock.send(text1.encode())
                    self.labe_Number_of_people.setText("目前聊天室有1人")
                else:
                    self.showchat.append("密碼輸入錯誤!")
                    self.name.setText("")
                    self.passwd.setText("")
        if(find == False):
            self.showchat.append("無此使用者!")
            self.name.setText("")
            self.passwd.setText("")

    def showText(self):
        #　將值傳給server
        self.sock.send(self.chat.text().encode())
        #  同時將自己輸入的值印在chat上
        st = time.localtime(time.time())
        times = time.strftime('[%H:%M:%S]', st)
        self.showchat.append("\t\t" + self.chat.text() + " : You " + times)
        self.chat.setText("")

    def change_pwd(self):
        if(self.button_Login.isEnabled()):
            self.showchat.append("尚未登入!")
        else:
            text1 = self.name.text()
            user = self.collection.find_one({'uname':text1})
            text2 = self.change_passwd.text()
            user['upwd'] = text2
            self.collection.save(user)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myPanel = MainWindow()
    sys.exit(app.exec_())
