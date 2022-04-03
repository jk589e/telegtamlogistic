from sqlalchemy import create_engine
import pandas as pd

db_login = "globalvisor"
db_password="Sinhrofazatron1"
db_host = "rc1b-21imrctq167tcobb.mdb.yandexcloud.net"
#db_host = "127.0.0.1"
db_port = "6432"
#db_name = "postgres"
db_name = "telegramlogistics"

db_string = "postgresql://" + db_login + ":" + db_password + "@" + db_host + ":" + db_port + "/" + db_name

engine = create_engine(db_string)



def get_offset(): #get the last update_id from log table
    offset = (pd.read_sql_query('select max(update_id) from public.log_chat', con=engine)).iloc[0,0]+1
    return offset

def processed(update_id): #flag current log message
    sql = ''' update public.log_chat 
              set processed=1 
              where update_id= '''+ str(update_id)
    connection = engine.connect()
    connection.execute(sql)

def addUser(dfAddUser): # add new user to user tables
    dfAddUser.rename(columns={ 'message_from_id': 'user_id', 'message_date':'first_message_time'},  inplace=True)
    dfAddUser['status']=0
    dfAddUser.to_sql(name='users', con=engine, schema='public', if_exists='append', index=None)

def get_replies():
    sql = ''' SELECT 
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
    return pd.read_sql_query(sql,con=engine)

def updateStatus(status,chat_id):

    sql = ''' update public.users 
                  set status='''+ str(status) + ''' 
                  where user_id= ''' + str(chat_id)
    connection = engine.connect()
    connection.execute(sql)
