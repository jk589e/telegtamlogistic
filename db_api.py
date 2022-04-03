from sqlalchemy import create_engine
import pandas as pd

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



def get_offset():

    offset = (pd.read_sql_query('select max(update_id) from public.log_chat', con=engine)).iloc[0,0]+1


    return offset
