from flask import Flask,request,make_response
from config import token
from TlgBot import Bot
from db_handler import DataBase
from target import Target
from answers import stranger
import requests
import random

app = Flask(__name__)
token = token
Bot = Bot(token)
db = DataBase()
target = Target()

@app.route('/{}'.format(token),methods=["POST"])
def make_resp():
    result = request.json
    print(result)
    target_name = 'tail43'
    boss = 'L_tail'
    callback = result.get('callback_query')
    if callback:
        try:
            db.add_user(callback['from']['username'], callback['from']['id'])
        except:
            pass
        try:
            text = callback['from']['username']+'(button): '+callback['data']
            Bot.send_message(db.get_chat_id(boss), text)
        except:
            pass
        return target.keyboard_response(callback).json()
    try:
        message = result['message']
        chat_text = result['message']['text']
        chat_id = result['message']['chat']['id']
        username = result['message']['chat']['username']
    except:
        chat_text = ''
        chat_id = result['my_chat_member']['chat']['id']
        username = result['my_chat_member']['chat']['username']
        message = {'chat':{'id':chat_id}}
    try:
        db.add_user(username, chat_id)
    except:
        pass
        
    if username!=boss:
        try:
            text = username+': '+chat_text
            Bot.send_message(db.get_chat_id(boss), text)
        except:
            pass
    if username==target_name:
        return target.message_response(message).json()
    
    if username==boss and message:
        if chat_text.startswith('send'):
            to_user = db.get_chat_id(chat_text.split(' ')[1])
            text = chat_text.split(' ')[2]
            return Bot.send_message(to_user, text).json()
        elif chat_text.startswith('set'):
            db.add_status(chat_text.split(' ')[1])
        elif chat_text.startswith('drop'):
            db.drop_status()
        elif chat_text.startswith('show'):
            return Bot.send_message(db.get_chat_id(boss), db.get_status()).json()
    text = stranger[random.randint(0,len(stranger)-1)]
    return Bot.send_message(chat_id, text).json()
if __name__=='__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('webhook_cert.pem','webhook_pkey.pem'))
