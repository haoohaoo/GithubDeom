import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)



class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi()
        self.show()

    def hello(self):
        self.line_hello.setText("hello")

    def cancel(self):
        self.line_hello.setText("")

    def setupUi(self):
        self.resize(500,500)
        self.setWindowTitle("Chat Application")

        self.label = QLabel()
        self.label.setText("Nickname: ")


        self.button_Login = QPushButton()
        self.button_Login.setText("Login")

        self.button_cancel = QPushButton()
        self.button_cancel.setText("Send")

        self.name = QLineEdit()
        self.showchat = QTextEdit()#show內容
        self.chat = QLineEdit()#輸入內容


        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.label, 1, 0)
        grid.addWidget(self.name, 1, 1)
        grid.addWidget(self.button_Login, 1, 2)
        grid.addWidget(self.showchat, 3, 0, 3, 3)
        grid.addWidget(self.chat, 5, 0, 5, 3)
        grid.addWidget(self.button_cancel, 6, 0, 6, 3)


        self.setLayout(grid)
        self.button_Login.clicked.connect(self.hello)
        self.button_cancel.clicked.connect(self.cancel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())
