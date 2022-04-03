import requests as rq
import warnings
import json
from pandas.io.json import json_normalize
import pandas as pd
import datetime as dt
from  sqlalchemy import create_engine
import time
warnings.filterwarnings("ignore")
desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 5000)

#database creds
db_login = "globalvisor"
db_password="Sinhrofazatron1"
db_host = "rc1b-21imrctq167tcobb.mdb.yandexcloud.net"
db_port = "6432"
db_name = "telegramlogistics"


#telegram bot config
token = '5285834737:AAEQ5sIkdX2bdcAd6HQSjN1xzemp5UyMxgA'
chat_id = '526697170'
baseUrl = 'https://api.telegram.org/bot' + token + '/'
headers = {'content-type': 'application/json'}
def joinCol(A,a,B,b):
    try:
        A[a]=B[b]
    except: pass


sql =''' SELECT 
	a.update_id, 
	a.message_id, 
	a.message_from_id, 
	a.message_chat_id, 
	a.inlinequery_id, 
	a.callbackquery_id, 
	a.username, 
	a.first_name, 
	a.last_name, 
	a.message_text, 
	a.message_date, 
	a.latitude, 
	a.longitude, 
	a.processed,
	b.status,
	b.role_id,
	b.company_id,
	b.is_active,
	b.registration_code
FROM public.log_chat a left join public.users b on a.message_from_id = b.user_id 
where a.processed is null
order by update_id desc
'''
db_string = "postgresql://" + db_login + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name

engine = create_engine(db_string)






def processed(update_id):
    sql = ''' update public.log_chat 
              set processed=1 
              where update_id= '''+ str(update_id)
    connection = engine.connect()
    connection.execute(sql)

def addUser(dfAddUser):
    dfAddUser.rename(columns={ 'message_from_id': 'user_id', 'message_date':'first_message_time'},  inplace=True)
    dfAddUser['status']=0
    dfAddUser.to_sql(name='users', con=engine, schema='public', if_exists='append', index=None)

def updateStatus(status,chat_id):

    sql = ''' update public.users 
                  set status='''+ str(status) + ''' 
                  where user_id= ''' + str(chat_id)
    connection = engine.connect()
    connection.execute(sql)



while 1<2:
    time.sleep(0.1)
    replies = pd.read_sql_query(sql,con=engine)
    #print(replies)

    if len(replies) > 0:
        for i in range(0,len(replies)):
                if replies.iloc[i,14] == None:  # статус когда пишет первый раз

                    print(replies.iloc[i, 14])
                    message_choise = 'Добрый день,' + str(replies.iloc[i, 7]) + '! Добро пожаловать, вот вам смайлик :)'
                    body1 = {"chat_id": str(replies.iloc[i, 2]), "text": message_choise}
                    rq.post(baseUrl + 'sendMessage', json=body1, headers=headers, verify=False)
                    dfAddUser = replies.loc[[i], ['username', 'message_from_id', 'first_name', 'last_name', 'message_date']]
                    addUser(dfAddUser)
                    updateStatus(0, replies.iloc[i, 2])

                    #dfAddUser['message_from_id'] = int(dfAddUser.loc[0,'message_from_id'])

                    processed(replies.iloc[i, 0])
                elif replies.iloc[i, 14] == 0:  # статус когда не авторизован
                    message_choise = 'Эхо: ' + replies.iloc[i, 9]
                    body1 = {"chat_id": str(replies.iloc[i, 2]), "text": message_choise}
                    print(str(replies.iloc[i, 6])+ ', ' + replies.iloc[i, 9])
                    rq.post(baseUrl + 'sendMessage', json=body1, headers=headers, verify=False)
                    processed(replies.iloc[i, 0])


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