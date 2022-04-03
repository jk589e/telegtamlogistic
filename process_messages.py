import warnings
import pandas as pd
import time

#import from local files
import api_telegram
import db_api


warnings.filterwarnings("ignore")
desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 5000)


while 1<2:
    time.sleep(0.1)
    replies = db_api.get_replies()
    #print(replies)

    if len(replies) > 0:
        for i in range(0,len(replies)):
            status = replies.iloc[i,14]
            chat_id = replies.iloc[i, 2]
            update_id = replies.iloc[i, 0]
            message_text = replies.iloc[i, 9]
            try:
                if status == None:  # unknown chat_id
                    print(status)
                    message = 'Добрый день,' + str(replies.iloc[i, 7]) + '! Добро пожаловать, вот вам смайлик :)' # text to send
                    api_telegram.send_message(chat_id=chat_id, message=message) # func to send text to telegram
                    dfAddUser = replies.loc[[i], ['username', 'message_from_id', 'first_name', 'last_name', 'message_date']]
                    db_api.addUser(dfAddUser) # add new user to table in database
                    db_api.updateStatus(0, chat_id) # change status to unauthorized
                    db_api.processed(update_id) # process row in log table
                elif status == 0:  # статус когда не авторизован
                    message = 'Эхо: ' + message_text
                    print(str(replies.iloc[i, 6])+ ', ' + message_text)
                    api_telegram.send_message(chat_id=chat_id, message=message)  # func to send text to telegram
                    db_api.processed(update_id)
            except: pass

'''
                elif replies.iloc[i,3] == 1: # основной статус
                    message_choise = 'Добрый день,'+ replies.iloc[i,4] +'! Выберите сектор'
                    buttons = getRegions()  #[['Сумма рейсов', 'Маржа по рейсам']]
                    reply_markap = {'keyboard': buttons, 'resize_keyboard': True, 'one_time_keyboard': True}
                    body1 = {"chat_id": str(replies.iloc[i, 1]), "text": message_choise, "reply_markup" : reply_markap }

                    rq.post(baseUrl + 'sendMessage', json=body1, headers=headers, verify=False)
                    marked(replies.iloc[i, 0])
                    updateStatus(2,replies.iloc[i, 1])
                elif replies.iloc[i, 3] == 2: # статус выбора показателя
                    if replies.iloc[i, 2] == 'Крафтер ТЭК':
                        getMainReport()
                        f = {'document': open(r'c:\some_files\Продажи по дням Крафтер ТЭК.PDF','rb')}
                        body = {"chat_id": str(replies.iloc[i, 1])}
                        rq.post(url=baseUrl + 'sendDocument', data=body, files=f, verify=False)

                    elif replies.iloc[i, 2] != 'Крафтер ТЭК':
                        region =replies.iloc[i, 2]
                        getRegionReport(region)
                        f = {'document': open(r'c:\some_files\Продажи по дням '+region+'.PDF', 'rb')}
                        body = {"chat_id": str(replies.iloc[i, 1])}
                        rq.post(url=baseUrl + 'sendDocument', data=body, files=f, verify=False)




                    updateStatus(1, replies.iloc[i, 1])
                    marked(replies.iloc[i, 0])
'''