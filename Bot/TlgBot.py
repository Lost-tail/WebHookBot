import time
import requests
import json

class Bot:
    
    def __init__(self,token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.status = None
        self.name = 'Еще нет мыла? Пиши e-mail'
        self.domain = ''
    
    def send_message(self,chat,text):
        params = {'chat_id':chat,'text':text}
        method='sendMessage'
        if self.status=='dom':
            reply = json.dumps({'inline_keyboard': [[{'text': 'domain1', 'callback_data': 'domain1'},{'text': 'domain2', 'callback_data': 'domain2'}],[{'text': 'domain3', 'callback_data': 'domain3'},{'text': 'domain4', 'callback_data': 'domain4'}]]})
            params['reply_markup'] = reply
        resp=requests.post(self.api_url+method,params)
        return resp
    
    def answer_button(self, query_id):
        method='answerCallbackQuery'
        text = 'Ваш e-mail создан!'
        params = {'callback_query_id':query_id, 'text':text, 'show_alert':True}
        resp=requests.post(self.api_url+method,params)
        return resp
