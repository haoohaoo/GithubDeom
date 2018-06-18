# -*- encoding: utf-8 -*-
import socket
import threading
import time
from chatterbot import ChatBot
from hanziconv import HanziConv

#fooddata
from xlrd import open_workbook
import random
wb = open_workbook('FoodData.xlsx')#read
sheel_1 = wb.sheet_by_index(0)# 獲取工作表的方法之一，用下標。

a = 0
temp_a = 0

class Server:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.bind((host, port))
        self.sock.listen(5)
        print('Server', socket.gethostbyname(host), 'listening ...')
        self.mylist = list()

        #設定聊天機器人
        self.chatterbot = ChatBot(
            'Ron Obvious',
            trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
        )

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
        global temp_a
        a += 1
        temp_a = a
        myconnection.send(("SYSTEM: " + str(a) + " people in the chat room").encode())
        for c in self.mylist:
            if c.fileno() != connNumber:
                try:
                    c.send(massage1.encode())
                except:
                    pass
                massage2 = ("SYSTEM: " + str(a) + " people in the chat room")
                c.send(massage2.encode())

        # 開始對話
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()#抓輸入

                if recvedMsg:
                    self.tellOthers(connNumber, recvedMsg,nickname)

                    # 將訊息給 bot
                    botMsg = self.littleBot(recvedMsg)
                    random_value = random.randint(3, 9)
                    if random_value % 3 == 0:
                        #先送一份給自己
                        st = time.localtime(time.time())
                        times = time.strftime('[%H:%M:%S]', st)
                        massage = ("bot"+ ":  " +botMsg + "     " + times)
                        myconnection.send(massage.encode())
                        # 傳給其他人
                        self.tellOthers(connNumber, botMsg,"bot")

                else:
                    pass

                #如果有人tag小廚師
                if recvedMsg.find("@小廚師",0,4)!= -1:
                    self.tellOthers(connNumber, self.littleChef(recvedMsg,myconnection),"小廚師")


            except (OSError, ConnectionResetError):
                try:
                    # 將總數-1
                    a-=1
                    # 在server 印出誰離開
                    print('One connecting is leave', myconnection.getsockname(), myconnection.fileno())
                    #在其他client 告知誰離開
                    for c in self.mylist:
                        if c.fileno() != connNumber:
                            print("OK!")
                            try:
                                print("in try")
                                msg = "SYSTEM: " + nickname+" is leave chat room"
                                c.send(msg.encode())
                                msg = "SYSTEM: " + str(a) + " people in the chat room"
                                c.send(msg.encode())
                            except:
                                print("in except")
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
                massage = (nickname+ ":  " +whatToSay + "     " + times)
                try:
                    c.send(massage.encode())
                except:
                    pass

    # 小廚師回話
    def littleChef(self,recvedMsg,myconnection):
        print("in littleChef")
        idontknow="想吃什麼"
        whatingredients="食材是"
        howtocook="做法是"
        x= recvedMsg.find(idontknow,len(recvedMsg)-5,len(recvedMsg)-1)        #判斷有沒有"想吃什麼?"這個詞
        y= recvedMsg.find(whatingredients,len(recvedMsg)-4,len(recvedMsg)-1)  #判斷有沒有"食材是?"這個詞
        z= recvedMsg.find(howtocook,len(recvedMsg)-4,len(recvedMsg)-1)        #判斷有沒有"做法是?"這個詞

        returnValue = ""

        if x != -1:#output"吃什麼?
            returnValue = sheel_1.cell_value(rowx=random.randint(1,100),colx=0 )
            #myconnection.send( p.encode() )
        elif y!= -1 :
            get = ''
            get= recvedMsg[4:len(recvedMsg)-4]
            for sheet in wb.sheets():#搜尋excel
                for rowidx in range(sheet.nrows):
                    row = sheet.row(rowidx)
                    for colidx, cell in enumerate(row):
                        if cell.value == get:
                            print (colidx)
                            print(rowidx)
                            returnValue=sheel_1.cell_value(rowx=rowidx,colx=1 )
                            #myconnection.send(q.encode() )#output"食材是?"
        elif z!=-1 :
            gets = ''
            gets = recvedMsg[4:len(recvedMsg) - 4]
            for sheet in wb.sheets():#搜尋excel
                for rowidx in range(sheet.nrows):
                    row = sheet.row(rowidx)
                    for colidx, cell in enumerate(row):
                        if cell.value == gets:
                            print (colidx)
                            print(rowidx)
                            returnValue=sheel_1.cell_value(rowx=rowidx,colx=2 )
        else :
            returnValue='我的菜單沒有'

         #先送一份給自己
        st = time.localtime(time.time())
        times = time.strftime('[%H:%M:%S]', st)
        massage = ("小廚師"+ ":  " +returnValue + "     " + times)
        myconnection.send(massage.encode())

        return returnValue

    def littleBot(self,recvedMsg):
        return HanziConv.toTraditional(self.chatterbot.get_response(recvedMsg).text)

def main():
    s = Server('127.0.0.1', 5550)
    while True:
        s.checkConnection()


if __name__ == "__main__":
    main()

