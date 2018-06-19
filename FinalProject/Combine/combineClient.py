import socket
import threading
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)
import time
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
import textwrap


# 寫檔用
writeMsg = ""

class NotOnlineWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 設定文字和按鈕
        okButton = QPushButton("確定")
        leavemsg = QLabel("\tBroken line, You can't chat!")


        #設定layput方式
        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(leavemsg)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox2);
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        #設定視窗參數
        self.setFixedSize(300, 150)
        self.setWindowTitle(' ')

        okButton.clicked.connect(self.checkLeave)

    # 確定要離開
    def checkLeave(self,evnt):
        global isLeave
        isLeave = 1
        myPanel.close()
        app.closeAllWindows()
        self.close()


class RemindWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # 設定文字和按鈕
        outdoorButton = QPushButton("出去吃")
        selfCookButton = QPushButton("自己煮")
        cancelButton = QPushButton("取消")
        self.leavemsg = QLabel("\t12點該吃飯囉！\n      想出去吃還是自己煮呢？")


        #設定layput方式
        hbox = QHBoxLayout()
        hbox.addWidget(outdoorButton)
        hbox.addWidget(selfCookButton)
        hbox.addWidget(cancelButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.leavemsg)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox2);
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        #設定視窗參數
        self.setFixedSize(300, 150)
        self.setWindowTitle(' ')

        outdoorButton.clicked.connect(self.checkOutdoor)
        selfCookButton.clicked.connect(self.checkSelfCook)
        cancelButton.clicked.connect(self.checkCancel)

    # 確認出去吃
    def checkOutdoor(self,evnt):
        str = "出去吃"
        myPanel.sock.send(str.encode())
        self.close()

    # 確認自己煮
    def checkSelfCook(self,evnt):
        str = "自己煮"
        myPanel.sock.send(str.encode())
        self.close()

    # 取消
    def checkCancel(self,evnt):
        self.close()

class CheckLeaveWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 設定文字和按鈕
        okButton = QPushButton("確定")
        cancelButton = QPushButton("取消")
        leavemsg = QLabel("\t確定要離開聊天室嗎?")


        #設定layput方式
        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(leavemsg)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox2);
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        #設定視窗參數
        self.setFixedSize(300, 150)
        self.setWindowTitle(' ')

        okButton.clicked.connect(self.checkLeave)
        cancelButton.clicked.connect(self.checkNLeave)

    # 確定要離開
    def checkLeave(self,evnt):
        global isLeave
        isLeave = 1
        myPanel.close()
        app.closeAllWindows()
        self.close()

    # 不要離開
    def checkNLeave(self,evnt):
        self.close()

class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.link_to_server('127.0.0.1', 5550) # 連線~~
        self.setupUi()

        self.show()

        th1 = threading.Thread(target=self.sendThreadFunc)
        #th2 = threading.Thread(target=self.recvThreadFunc)
        #threads = [th1, th2]
        threads = [th1]
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join

        self.eating = eatingThread()
        self.eating.sec_changed_signal.connect(self.EatingRemained)
        self.eating.start()

        self.recvThread = GetMessage()
        self.recvThread.isbrokenet.connect(self.BrokenNetwork)
        self.recvThread.start()

        self.flagofbreaknet = 0

    def BrokenNetwork(self,flag):
        if self.flagofbreaknet == 0:
            if flag == 0:
                breakline.show()
                self.flagofbreaknet = 1

    def EatingRemained(self,flag):
        if flag == 1:
            remindWindows.show()

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

    '''def recvThreadFunc(self):
        global writeMsg
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                t = otherword.decode()
                self.showchat.append(t)
                writeMsg += "\n" + t # 寫檔用
                if(" people in the chat room"in t):
                    print("有人進出")
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
                self.online.show()'''


    def setupUi(self):
        self.resize(700,700)
        self.setWindowTitle("ChatRoom")

        self.labe_Number_of_people = QLabel()
        self.labe_Number_of_people.setStyleSheet("color: rgb(255,255,255)")
        self.labe_Number_of_people.setFont(QFont('consolas',14,weight=QFont.Bold))
        #self.labe_Number_of_people.setStyleSheet("background-color: rgb(153, 153, 153)")
        self.labe_Number_of_people.setText("\t目前聊天室有0人！")         #目前人數lable
        self.label = QLabel()
        self.label.setText("Chat Name: ")
        self.label.setFont(QFont('consolas',12))


        self.button_Login = QPushButton()
        self.button_Login.setText("Enter")
        self.button_Login.setStyleSheet("background-color: rgb(102, 153, 255)")
        self.button_Login.setFont(QFont('consolas',12))

        self.button_clear = QPushButton()
        self.button_clear.setText("Clear")
        self.button_clear.setStyleSheet("background-color: rgb(102, 153, 255)")
        self.button_clear.setFont(QFont('consolas',12))

        self.button_send = QPushButton()
        self.button_send.setFont(QFont('consolas',12))

        self.button_send = QPushButton("Send") # b3不可按
        self.button_send.setStyleSheet("background-color: rgb(153, 153, 153)")
        self.button_send.setText("Send")
        self.button_send.setStyleSheet("background-color: rgb(102, 153, 255)")
        self.button_send.setEnabled(False)
        self.button_send.setFont(QFont('consolas',12))
        self.button_Login.setEnabled(True)

        self.name = QLineEdit()
        self.name.setStyleSheet("color: rgb(192,192,192)")
        self.name.setFont(QFont('consolas', 12))
        self.showchat = QTextEdit()#show內容
        self.chat = QLineEdit()#輸入內容
        self.chat.setStyleSheet("color: rgb(192,192,192)")
        self.chat.setText("輸入發送內容，空白時無法發送")
        self.chat.setEnabled(False)
        self.chat.setFont(QFont('consolas',12))


        #設定showchar的滾動條
        self.showchat.setLineWrapMode(QTextEdit.NoWrap)
        self.showchat.setFont(QFont('consolas',12))

        #設定顏色
        self.showchat.setStyleSheet("background-color: rgb(255,255,255)")
        self.chat.setStyleSheet("background-color: rgb(255,255,255)")
        self.name.setStyleSheet("background-color: rgb(255,255,255)")

        grid = QGridLayout()
        #grid.setSpacing(11)
        grid.addWidget(self.labe_Number_of_people, 0, 1, 1,3)        #秀出目前人數
        grid.addWidget(self.label, 1, 0,1,1)
        grid.addWidget(self.name, 1, 1,1,2)
        grid.addWidget(self.button_Login, 1, 3,1,1)
        grid.addWidget(self.button_clear, 1, 4,1,1)
        grid.addWidget(self.showchat, 2, 0, 5, 5)
        grid.addWidget(self.chat, 7, 0, 1, 4)
        grid.addWidget(self.button_send, 7, 4, 1, 1)


        self.setLayout(grid)
        self.button_Login.clicked.connect(self.login)
        self.button_send.clicked.connect(self.showText)
        self.button_clear.clicked.connect(self.clearName)

        self.name.installEventFilter(self)
        self.chat.installEventFilter(self)
        #self.name.clicked.connect(self.nameclear)
        #self.chat.clicked.connect(self.chatclear)

        # set black background
        #p = self.palette()
        #p.setColor(self.backgroundRole(), red)
        self.setStyleSheet("background-color:rgb(153,153,153);")
        self.show()

    def login(self):
        # 取得 輸入的 nickname
        text1 = self.name.text()
        #print("name="+text1)
        if((len(text1)<=5)&(text1!="")&(text1!="請輸入暱稱，至多5個字元")):
            self.name.setEnabled(False)
            self.chat.setEnabled(True)
            self.button_send.setEnabled(True)
            self.button_clear.setEnabled(False)
            self.button_Login.setEnabled(False)
            self.chat.setText("輸入發送內容，空白時無法發送")
            self.chat.setStyleSheet("color: rgb(192,192,192);background-color: rgb(255,255,255)")
            self.sock.send(text1.encode())
        else:
            nameInputWindow.show()

    def showText(self):
        #　將值傳給server
        if((len(self.chat.text())<=200)&(self.chat.text()!="")&(self.chat.text()!="輸入發送內容，空白時無法發送")):
            self.sock.send(self.chat.text().encode())
            #  同時將自己輸入的值印在chat上
            st = time.localtime(time.time())
            times = time.strftime('[%H:%M:%S]', st)
            user = "You"
            prefix = "                         " + times +" "+ user + ": "
            preferredWidth = 51
            text = self.chat.text()
            wrapper = textwrap.TextWrapper(initial_indent= prefix, width=preferredWidth,
                                           subsequent_indent=' ' * (len(prefix)))
            msg = wrapper.fill(text)
            self.showchat.append(msg)
            global writeMsg
            writeMsg += "\n\t" + times + self.chat.text() + " : You "  # 寫檔用
            self.chat.setText("")
        else:
            inputWindow.show()

    def saveMSG(self):
        global writeMsg
        print("writeMSG = ")
        print(writeMsg)
        path = "ChatRoom"
        st = time.localtime(time.time())
        times = time.strftime('%Y_%m_%d_%H_%M', st)
        if not os.path.isdir(path):
            os.mkdir(path)
        file = open(path + "\\" + times + ".txt", "w")
        file.writelines(writeMsg)
        # 關閉檔案
        file.close()

    def closeEvent(self, event):
        if(isLeave == 1):
            self.saveMSG()
            event.accept()
        else:
            LWindows.show()
            event.ignore()

    def clearName(self):
        self.name.setText("請輸入暱稱，至多5個字元")
        self.name.setStyleSheet("color: rgb(192,192,192)")

    def eventFilter(self, QObject, QEvent):
        if QEvent.type() == QEvent.MouseButtonPress:
            if QObject==self.name:
                if self.name.text() == "請輸入暱稱，至多5個字元":
                        self.name.setText("")
                        self.name.setStyleSheet("color: rgb(0,0,0);background-color: rgb(255,255,255)")
            if QObject==self.chat:
                if self.chat.text() == "輸入發送內容，空白時無法發送":
                    if self.chat.isEnabled()==True:
                        self.chat.setText("")
                        self.chat.setStyleSheet("color: rgb(0,0,0);background-color: rgb(255,255,255)")
        if QEvent.type() == QEvent.FocusOut:
            if QObject==self.name:
                if self.name.text()=="":
                    self.name.setText("請輸入暱稱，至多5個字元")
                    self.name.setStyleSheet("color: rgb(192,192,192);background-color: rgb(255,255,255)")
            if QObject==self.chat:
                if self.chat.text() == "":
                    self.chat.setText("輸入發送內容，空白時無法發送")
                    self.chat.setStyleSheet("color: rgb(192,192,192);background-color: rgb(255,255,255)")
        return super(QWidget, self).eventFilter(QObject, QEvent)


class tooManyInput(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # 設定文字和按鈕
        okButton = QPushButton("確定")
        inputmsg = QLabel("\t最多輸入200個字")


        #設定layput方式
        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(inputmsg)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox2);
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        #設定視窗參數
        self.setFixedSize(300, 150)
        self.setWindowTitle(' ')

        okButton.clicked.connect(self.chlickLeave)



    # 確定並關閉視窗和清空字串
    def chlickLeave(self,evnt):
        myPanel.chat.setText("")
        self.close()

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)

class tooManyChar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 設定文字和按鈕
        okButton = QPushButton("確定")
        inputmsg = QLabel("\t最多輸入5個字元")


        #設定layput方式
        hbox = QHBoxLayout()
        hbox.addWidget(okButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(inputmsg)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox2);
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        #設定視窗參數
        self.setFixedSize(300, 150)
        self.setWindowTitle(' ')

        okButton.clicked.connect(self.chlickLeave)

    # 確定並關閉視窗和清空字串
    def chlickLeave(self,evnt):
        myPanel.name.setText("")
        self.close()

# 提醒中餐午餐用
class eatingThread(QThread):
    sec_changed_signal = pyqtSignal(int) # 信号类型：int
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        while True:
            st = time.localtime(time.time())
            times = time.strftime('%H%S', st)
            if times == "1201":
                remindWindows.leavemsg.setText("\t12點該吃飯囉！\n      想出去吃還是自己煮呢？")
                self.sec_changed_signal.emit(1)  #发射信号
                time.sleep(3600*4) # 休息4小時
            elif times == "1801":
                remindWindows.leavemsg.setText("\t18點該吃飯囉！\n      想出去吃還是自己煮呢？")
                self.sec_changed_signal.emit(1)  #发射信号
                time.sleep(3600*4) # 休息4小時
            else:
                self.sec_changed_signal.emit(0)  #发射信号
            time.sleep(1)


class GetMessage(QThread):
    isbrokenet = pyqtSignal(int) # 信号类型：int
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        global writeMsg
        while True:
            try:
                otherword = myPanel.sock.recv(1024) # socket.recv(recv_size)
                t = otherword.decode()
                myPanel.showchat.append(t)
                writeMsg += "\n" + t # 寫檔用
                if(" people in the chat room"in t):
                    print("有人進出")
                    size = len(t)-32
                    a = 0
                    for i in range(size):
                        b = size-i-1
                        if(b<=0):
                            a += (int(t[8]))
                        else:
                            a += (int(t[8]))*(10^(size-i-1))
                    myPanel.labe_Number_of_people.setText("\t目前聊天室有" + str(a) + "人！")
                self.isbrokenet.emit(1)  #发射信号

            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                self.isbrokenet.emit(0)  #发射信号
                print('Server is closed!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myPanel = MainWindow()
    # 確認關閉視窗 用~~
    LWindows = CheckLeaveWindows()
    isLeave = 0
    # 午餐晚餐提醒視窗
    remindWindows = RemindWindows()
    # 超過200字的視窗
    inputWindow = tooManyInput()
    nameInputWindow = tooManyChar()
    # 斷網提示用
    breakline = NotOnlineWindows()

    sys.exit(app.exec_())

