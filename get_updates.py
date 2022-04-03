
import warnings
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
import time

#import from local files
import api_telegram
import db_api

warnings.filterwarnings("ignore")
desired_width = 1000
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 5000)


def joinCol(A,a,B,b):
    try:
        A[a]=B[b]
    except: pass

engine = create_engine(db_api.db_string)


while 1<2:
    time.sleep(0.1)
    dfMain = pd.DataFrame(data=[],
                          columns=["update_id", "message_id", "username","first_name","last_name","inlinequery_id", "callbackquery_id", "message_from_id",
                                   "message_chat_id", "message_text", "message_date", "latitude", "longitude"])
    try:

        df = api_telegram.get_updates() # get updates from telegram


        if df.__len__()>0: # if new messages exist
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
            dfMain.to_sql(name='log_chat', con=engine, schema='public', if_exists='append',index=False) # write log to database
        dfMain = None
        offset = None
        df = None
        res= None
    except Exception as inst:
        print(inst)
        pass
