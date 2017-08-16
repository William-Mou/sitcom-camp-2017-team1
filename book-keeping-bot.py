
# coding: utf-8

# In[1]:


import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from random import choice
import json


# In[2]:


TOKEN = '387192003:AAErN1lifsXEVv-26nJL6A9wprl7oxiq-Wc'


# In[3]:


bot = telepot.Bot(TOKEN)
moneydict={}
#{ID:[+-,money,event][+-,money,even][+-,money,even]}
def print_msg(msg):
    print(json.dumps(msg, indent=4))
    
def on_chat(msg):
    header = telepot.glance(msg, flavor="chat")
    print_msg(msg)

    if header[0] == "text":
        text = msg["text"]
        # command
        if text.startswith("/"):
            command = text.lstrip("/")
            
            if command == "start":
                text = "OK， {}\n你準備好了...... 讓我們開始記帳吧"
                bot.sendMessage(header[2], text.format(msg["from"]["first_name"]))
                bot.sendMessage(header[2], "記帳請依序輸入 /add +(收入)or-（支出） 數字（金額） 事件")
            elif command[:3] == "add":
                #data=[+-,money,event]
                data=command[3:].split()
                bot.sendMessage(header[2],"增加收支細項"+str(data[2]))
                if header[2] in moneydict:
                    moneydict[header[2]].append(data)
                else:
                    moneydict[header[2]]=[data]
                bot.sendMessage(header[2],"收支帳本"+str(moneydict[header[2]]))
                
            elif command == "list":
                for i in range(len(moneydict[header[2]])):
                    bot.sendMessage(header[2],"收支帳本"+str(moneydict[header[2]][i]))
        # other msg
        else: 
            # 我覺得不行！
            image_url = "https://cdn.pixabay.com/photo/2016/03/22/23/45/money-1273908_960_720.jpg"
            bot.sendPhoto(header[2], image_url)
'''
            # 回應按鈕
            replyKeyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="在一個穩定的發揮後，卻得到一個這樣的反饋。我覺得有點失控",
                        callback_data="test"
                    )
                ]
            ])
            bot.sendMessage(header[2], text="選擇回應", reply_markup=replyKeyboard)
'''


MessageLoop(bot, {
    'chat': on_chat,
    #'callback_query': on_callback_query,
}).run_as_thread()

print('Listening ...')


# In[ ]:




