食物回話功能

檔案: FoodData.xlsx (食譜資料)
      FoodBotServer.py 
      Client.py (老師上課範例)

 

使用者不知道要吃什麼，
在client端輸入 “吃什麼?” 的關鍵字，
BOT接收到關鍵字後，從食譜(FoodData.xlsx)中隨機取出一道菜名，再傳給client。

使用者知道要吃什麼(XXX)，但不知道食材，
在client端輸入 “XXX食材是?” 的關鍵字，
BOT接收到關鍵字後，從食譜(FoodData.xlsx)中找到XXX，再取出XXX的食材後，回傳給client。

使用者知道要吃什麼(yyy)，但不知道做法，
在client端輸入 “yyy做法是?” 的關鍵字，
BOT接收到關鍵字後，從食譜(FoodData.xlsx)中找到yyy，再取出yy的作法後，回傳給client。

使用者亂輸入的話，則回傳 "我的菜單沒有" 

