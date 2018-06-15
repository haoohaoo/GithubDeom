import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,QTextEdit, QGridLayout, QApplication)


class newWindow(QWidget):
        def __init__(self):
            super(self.__class__, self).__init__()
            self.setupUi()
        def setupUi(self):
            self.resize(100,100)
            self.setWindowTitle("new Windows")
            grid = QVBoxLayout()



class MainWindow(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi()
        self.show()


    def setupUi(self):
        self.resize(300,300)
        self.setWindowTitle("Multiple Windows")


        self.button = QPushButton()
        self.button.setText("Add Windows")


        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(self.button, 1, 1,1,4) #login_button

        self.setLayout(grid)
        self.button.clicked.connect(self.addWindows)

    def addWindows(self):
        tempWindows.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myPanel = MainWindow()
    tempWindows = newWindow()
    sys.exit(app.exec_())
