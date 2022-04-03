import requests as rq
import pandas as pd
import json
from pandas.io.json import json_normalize
import db_api

base_url = "https://api.telegram.org/bot"
bot_token = "5285834737:AAEQ5sIkdX2bdcAd6HQSjN1xzemp5UyMxgA"
api_url= base_url + bot_token

def joinCol(A,a,B,b):
    try:
        A[a]=B[b]
    except: pass



def get_updates():
    offset = db_api.get_offset()
    jsonbody = '{"offset":'+str(offset)+',"allowed_updates":["message","edited_message","callback_query","inline_query","chosen_inline_result"]}'
    headers = {'content-type': 'application/json'}
    res = rq.post(api_url + '/getUpdates', data=jsonbody, headers=headers, verify=False)

    res = json.loads(res.text)
    # print(res)
    df = json_normalize(res["result"])

    return df

def send_message(chat_id,message):
    headers = {'content-type': 'application/json'}
    body = {"chat_id": str(chat_id), "text": message}
    rq.post(api_url + '/sendMessage', json=body, headers=headers, verify=False)
