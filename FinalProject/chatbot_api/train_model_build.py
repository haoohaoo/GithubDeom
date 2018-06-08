# 引入 ChatBot
from chatterbot import ChatBot

# 建立一個 ChatBot 物件
chatbot = ChatBot(
    'Ron Obvious',
    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
)

# 基於簡體中文的自動學習套件
chatbot.train("chatterbot.corpus.chinese")

# 載入(簡體)中文的基本語言庫
chatbot.train("chatterbot.corpus.chinese")

# 載入(簡體)中文的問候語言庫
chatbot.train("chatterbot.corpus.chinese.greetings")

# 載入(簡體)中文的對話語言庫
chatbot.train("chatterbot.corpus.chinese.conversations")
