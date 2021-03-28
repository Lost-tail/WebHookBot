import requests
import random
from bs4 import BeautifulSoup
from db_handler import DataBase
from TlgBot import Bot
from answers import target
from config import token


class Target(DataBase):
    
    def __init__(self):
        self.bot = Bot(token)
        
    def message_response(self, message):
        chat_id = message['chat']['id']
        status = self.get_status()
        if message['text']=='/start':
            self.drop_status()
            text = 'some answer1'
            reply = self.bot.make_keyboard(['butt1', 'butt2'])
            self.add_status('1')
            return self.bot.send_message(chat_id, text, reply)
        elif status=='done':
            return self.bot.send_message(chat_id, self.get_synonum(message['text']))
        elif status=='manual':
            return self.bot.send_message(chat_id, '')
        elif status=='data':
            text = """some answer2"""
            self.add_status('done')
            return self.bot.send_message(chat_id, text)
        else:
            return self.bot.send_message(chat_id, target[random.randint(0,len(target)-1)])
            
        
    def keyboard_response(self, callback):
        chat_id = callback['from']['id']
        data = callback['data']
        status = self.get_status()
        if status=='1':
            if data == 'butt1':
                text = """some answer3"""
            elif data == 'butt2':
                text = """some answer4"""
            reply = self.bot.make_keyboard(['butt3', 'butt4', 'butt5'])
            self.add_status('2')
            return self.bot.send_message(chat_id, text, reply)
        
        elif status=='2':
            if data == 'butt3':
                text = """some answer5"""
                self.add_status('done')
                reply = None
            elif data == 'butt4':
                text = """some answer6"""
                reply = self.bot.make_keyboard(['butt6', 'butt7'])
            elif data == 'butt5':
                text = """some answer7"""
                self.add_status('data')
                reply = None
            elif data == 'butt7':
                text = """some answer8"""
                self.add_status('done')
                reply = None
            return self.bot.send_message(chat_id, text, reply)
            
        return self.bot.send_message(chat_id, 'Я запутался, давай начнем сначала. Набери /start')
      
    def get_synonum(self, text):
        synonums = []
        header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
        for word in text.split(' '):
            if word:
                try:
                    request = requests.get('https://rifme.net/r/{}/0'.format(word.replace(',','')), headers=header)
                    soup = BeautifulSoup(request.text,'html.parser')
                    data = soup.find('ul', {'class': 'rifmypodryad'}).text.split(' ')[:-1]
                    synonums.append(data[random.randint(0,len(data)-1)])
                except:
                    synonums.append('Не нашел')
        return ' '.join(synonums)
            
            
