import requests as rq

base_url = "https://api.telegram.org/bot"
bot_token = "5285834737:AAEQ5sIkdX2bdcAd6HQSjN1xzemp5UyMxgA"

api_url= base_url + bot_token

get_upd_url=api_url + "/getUpdates?offset=0&"
print(api_url)
#res=

import requests as rq
import warnings
import json
from pandas.io.json import json_normalize
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
import time
warnings.filterwarnings("ignore")
desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 5000)


def joinCol(A,a,B,b):
    try:
        A[a]=B[b]
    except: pass

db_login = "globalvisor"
db_password="Sinhrofazatron1"
#db_host = "globalvisor.c9vo7crlmoq9.us-west-2.rds.amazonaws.com"
db_host = "rc1b-21imrctq167tcobb.mdb.yandexcloud.net"
#db_host = "127.0.0.1"
db_port = "6432"
#db_name = "postgres"
db_name = "telegramlogistics"

db_string = "postgresql://" + db_login + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name

engine = create_engine(db_string)
while 1<2:
    time.sleep(0.1)
    dfMain = pd.DataFrame(data=[],
                          columns=["update_id", "message_id", "username","first_name","last_name","inlinequery_id", "callbackquery_id", "message_from_id",
                                   "message_chat_id", "message_text", "message_date", "latitude", "longitude"])

    offset = (pd.read_sql_query('select max(update_id) from public.log_chat', con=engine)).iloc[0,0]+1

    token = '5285834737:AAEQ5sIkdX2bdcAd6HQSjN1xzemp5UyMxgA'
    chat_id = '526697170'
    baseUrl = 'https://api.telegram.org/bot' + token + '/'
    jsonbody = '{"offset":'+str(offset)+',"allowed_updates":["message","edited_message","callback_query","inline_query","chosen_inline_result"]}'
    headers = {'content-type': 'application/json'}
    try:
        res = rq.post(baseUrl+'getUpdates', data = jsonbody, headers=headers ,verify=False)

        res = json.loads(res.text)
        #print(res)
        df = json_normalize(res["result"])
        #print (df)

        if df.__len__()>0:
            joinCol(dfMain, "update_id", df, "update_id")
            joinCol(dfMain, "message_id", df, "message.message_id")
            joinCol(dfMain, "message_from_id", df, "message.from.id")
            joinCol(dfMain, "message_chat_id", df, "message.chat.id")
            joinCol(dfMain, "username", df, "message.chat.username")
            joinCol(dfMain, "first_name", df, "message.chat.first_name")
            joinCol(dfMain, "last_name", df, "message.chat.last_name")
            joinCol(dfMain, "message_text", df, "message.text")
            joinCol(dfMain, "message_date", df, "message.date")
            joinCol(dfMain, "latitude", df, "message.location.latitude")
            joinCol(dfMain, "longitude", df, "message.location.longitude")
            try:
                dfMain["message_date"] = pd.to_datetime(dfMain['message_date'], unit='s') + dt.timedelta(hours=3)
            except: pass
            print(dfMain)
            dfMain.to_sql(name='log_chat', con=engine, schema='public', if_exists='append',index=False)
        dfMain = None
        offset = None
        df = None
        res= None
    except Exception as inst:
        print(inst)
        pass
