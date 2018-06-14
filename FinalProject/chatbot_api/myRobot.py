# 引入 ChatBot
from chatterbot import ChatBot
from hanziconv import HanziConv

chatbot = ChatBot(
    'Ron Obvious',
    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
)

response = ""
print("開始聊天!!\n")
for i in range(10):
    s = input("user: ")
    response = chatbot.get_response(s).text
    print(HanziConv.toTraditional("\t\t" + response + ": Robot"))

print("\n"+"結束聊天!!")
