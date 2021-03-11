from flask import Flask,request,make_response
from config import token
from TlgBot import Bot
import requests

app = Flask(__name__)
token = token
Bot = Bot(token)

@app.route('/{}'.format(token),methods=["POST"])
def make_resp():
    result = request.json
    print(result)
    callback = result.get('callback_query')
    if callback:
        Bot.status = None
        Bot.domain = callback['data']
        return Bot.answer_button(callback['id']).json()
    try:
    	chat_text = result['message']['text']
    	chat_id = result['message']['chat']['id']
    except:
	chat_text = ''
	chat_id = result['my_chat_member']['chat']['id']
    if Bot.status=='name':
        Bot.name = chat_text
        Bot.status = 'dom'
        text = 'Выбери домен из списка'
        return Bot.send_message(chat_id,text).json()
    
    if chat_text=='e-mail':
        Bot.status = 'name'
        text = 'Напиши название'
    elif chat_text.lower()=='show':
        if Bot.domain:
            text = Bot.name+'@'+Bot.domain
        else:
            text = Bot.name
    else:
        if Bot.status=='dom':
            text = 'Выбери домен из списка'
        else:
            Bot.status = None
            text = 'Привет! Хочешь e-mail? Напиши e-mail\nПоказать ваш e-mail? Напиши show'
    return Bot.send_message(chat_id,text).json()

if __name__=='__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('webhook_cert.pem','webhook_pkey.pem'))
