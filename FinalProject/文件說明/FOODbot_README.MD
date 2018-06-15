用了什麼技術?
使用者輸入文字，傳給bot server，呼叫外部檔案 

達到那些目的 

透過使用者輸入菜色，來讓使用者知道這道菜的作法以及食材，即使使用者不知道要吃什麼，也能自動推薦。	

那些功能	
檔案: FoodData.xlsx (食譜資料) FoodBotServer.py Client.py (老師上課範例)  
使用者不知道要吃什麼， 在client端輸入 “吃什麼?” 的關鍵字， BOT接收到關鍵字後，從食譜(FoodData.xlsx)中隨機取出一道菜名，再傳給client。 	  
使用者知道要吃什麼(XXX)，但不知道食材， 在client端輸入 “XXX食材是?” 的關鍵字， BOT接收到關鍵字後，從食譜(FoodData.xlsx)中找到XXX，再取出XXX的食材後，回傳給client。	  
使用者知道要吃什麼(yyy)，但不知道做法， 在client端輸入 “yyy做法是?” 的關鍵字， BOT接收到關鍵字後，從食譜(FoodData.xlsx)中找到yyy，再取出yy的作法後，回傳給client。  
使用者亂輸入的話，則回傳 "我的菜單沒有	  
