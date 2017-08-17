
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


TOKEN = '387192003:AAHGcS6V3K29zWdhMPbK-Wy6W3VVKr3YWcQ'


# In[3]:


bot = telepot.Bot(TOKEN)
#{chatid:[[+-,money,event],[+-,money,even],[+-,money,even]]}
moneydict={}
#{idtousername:{data:[1,]}} 0:未確認 1：確認 2：還款確認 pop:還款完成
lenddict={}

def print_msg(msg):
    print(json.dumps(msg, indent=4))
    
def on_chat(msg):
    header = telepot.glance(msg, flavor="chat")
    print_msg(msg)
    data=""
    if header[0] == "text":
        text = msg["text"]
        # command
        if text.startswith("/"):
            command = text.lstrip("/")
            
            if command == "start":
                text = "OK， {}\n你準備好了...... 讓我們開始記帳吧"
                bot.sendMessage(header[2], text.format(msg["from"]["first_name"]))
                bot.sendMessage(header[2], "記帳請依序輸入 /add +(收入)or-（支出） 金額 事件")
                bot.sendMessage(header[2], "請輸入/list查看帳本，輸入/total 獲取總資產")
                bot.sendMessage(header[2], "借款請依序輸入 /lend @欠款人 金額 事件")
                bot.sendMessage(header[2], "查看借貸請輸入 /ldict @username")
                
            elif command[:3] == "add":
                #data=[+-,money,event]
                data=command[3:].split()
                if data[0] == '+' or data[0]=='-':
                    try:
                        int(data[1])
                        bot.sendMessage(header[2],"增加收支細項"+str(data[2]))
                        if header[2] in moneydict:
                            moneydict[header[2]].append(data)
                        else:
                            moneydict[header[2]]=[data]
                        bot.sendMessage(header[2],"收支帳本"+str(moneydict[header[2]]))
                    except:
                        bot.sendMessage(header[2],"請符合格式ouo")
                else:
                    bot.sendMessage(header[2],"請符合格式ouo")
            elif command[:4] == "lend":
                data=command[4:].split()
                bot.sendMessage(header[2],"借款給 "+str(data[0])+" "+str(data[1])+"元")
                if msg["from"]["username"]+"to"+str(data[0][1:]) in lenddict:
                    lenddict[str(msg["from"]["username"])+"to"+str(data[0][1:])][msg["date"]]=[0,str(data[1])]
                else:
                    lenddict[str(msg["from"]["username"])+"to"+str(data[0][1:])]={msg["date"]:[0,str(data[1])]}

                bot.sendMessage(header[2],"請借款人 "+str(data[0])+" 回傳 /borrow @"+str(msg["from"]["username"])+" "+str(msg["date"])+" 驗證")
                #bot.sendMessage(header[2],str(lenddict))

                '''
                if str(msg["from"]["username"])+"to"+str(data[0]) in lenddict:
                    lenddict[str(msg["from"]["username"])+"to"+str(data[0])]={msg[data]:0}
                    bot.sendMessage(header[2],0)
                else:
                    lenddict[str(msg["from"]["username"])+"to"+str(data[0])]={msg[data]:0}
                '''    
            #commond: /borrow @username date
            elif command[:6] == "borrow":
                data=command[6:].split()
                lenddict[data[0][1:]+"to"+msg["from"]["username"]][int(data[1])][0]=1
                #bot.sendMessage(header[2],str(lenddict))
                bot.sendMessage(header[2],"提醒：輸入 /payback " + data[0] + " " +data[1]+" 還款")
                
            #commond: /payback @username date
            elif command[:7] == "payback":
                data=command[7:].split()
                lenddict[data[0][1:]+"to"+msg["from"]["username"]][int(data[1])][0]=2
                bot.sendMessage(header[2],"請 "+data[0]+" 確認 @"+str(msg["from"]["username"])+" 是否還款，並輸入 /payok @"+msg["from"]["username"]+" "+str(data[1])+" 確認")
                
            #commond: /payok @username date
            elif command[:5] == "payok":
                data=command[5:].split()
                lenddict[msg["from"]["username"]+"to"+data[0][1:]].pop(int(data[1]))
                bot.sendMessage(header[2],"還款確認完成><資料已核銷")
                
            elif command == "list":
                for i in range(len(moneydict[header[2]])):
                    bot.sendMessage(header[2],"收支帳本"+str(moneydict[header[2]][i]))
                    
            # /ldict @username
            elif command[:5] == "ldict":
                data=command[5:].split()
                if msg["from"]["username"]+"to"+data[0][1:] in lenddict:
                #for i in lenddict[msg["from"]["username"]+"to"+data[0][1:]]:
                    for i in lenddict[msg["from"]["username"]+"to"+data[0][1:]]:
                        if lenddict[msg["from"]["username"]+"to"+data[0][1:]][i][0]==0:
                            bot.sendMessage(header[2]," 欠款待確認，欠"+str(lenddict[msg["from"]["username"]+"to"+data[0][1:]][i][1])+"元")
                        elif lenddict[msg["from"]["username"]+"to"+data[0][1:]][i][0]==1:
                            bot.sendMessage(header[2]," 欠款確認，欠"+str(lenddict[msg["from"]["username"]+"to"+data[0][1:]][i][1])+"元")
                        elif lenddict[msg["from"]["username"]+"to"+data[0][1:]][i][0]==2:
                            bot.sendMessage(header[2]," 還款待確認，欠"+str(lenddict[msg["from"]["username"]+"to"+data[0][1:]][i][1])+"元")
                else:
                    bot.sendMessage(header[2],str(data[0])+" 暫無欠您的款項")
                    
            elif command[:5] == "total":
                s=0
                for i in range(len(moneydict[msg['chat']['id']])):
                    if moneydict[msg['chat']['id']][i][0]=='+':
                        try:
                            s+=int(moneydict[msg['chat']['id']][i][1])
                        except:
                            pass
                    else:
                        try:
                            s-=int(moneydict[msg['chat']['id']][i][1])
                        except:
                            pass
                bot.sendMessage(header[2],str(msg['chat']['id'])+"總資產："+str(s))
        # other msg
        else: 
            # 我覺得不行！
            image_url = "https://cdn.pixabay.com/photo/2016/03/22/23/45/money-1273908_960_720.jpg"
            bot.sendPhoto(header[2], image_url)
            bot.sendMessage(header[2],"輸入/start查看指令")
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




