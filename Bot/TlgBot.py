import time
import requests
import json

class Bot():
    
    def __init__(self,token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.status = None
   
    
    def send_message(self,chat,text, reply=None):
        params = {'chat_id':chat,'text':text}
        method='sendMessage'
        if reply:
            params['reply_markup'] = reply
        resp=requests.post(self.api_url+method,params)
        return resp
    
    def send_answer(self):
        return 'Ok', 200
    
    def make_keyboard(self, buttons):
        keyboard = [[{'text': x, 'callback_data': x}] for x in buttons]
        return json.dumps({'inline_keyboard':keyboard})
    
    def make_large_keyboard(self, buttons):
        keyboard = [[{'text': x, 'callback_data': x} for x in button] for button in buttons]
        return json.dumps({'inline_keyboard':keyboard})
    
    def answer_button(self, query_id):
        method='answerCallbackQuery'
        text = 'Ваш e-mail создан!'
        params = {'callback_query_id':query_id, 'text':text, 'show_alert':True}
        resp=requests.post(self.api_url+method,params)
        return resp

