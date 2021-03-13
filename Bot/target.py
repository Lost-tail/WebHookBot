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
            text = 'Псс... Это ведь ты, Оля Олеговна? У меня для тебя кое что есть.'
            reply = self.bot.make_keyboard(['Да, это я', 'Нет, ты ошибся'])
            self.add_status('1')
            return self.bot.send_message(chat_id, text, reply)
        elif status=='done':
            return self.bot.send_message(chat_id, self.get_synonum(message['text']))
        elif status=='manual':
            return self.bot.send_message(chat_id, '')
        elif status=='data':
            text = """Бесстрашный ты мой спаситель) Когда придешь на место, поднимись на второй этаж, не мерзни. 
Развлечь тебя? Я умею рифмовать покруче рэперов) Напиши любое слово, желательно, чтобы оно существовало)"""
            self.add_status('done')
            return self.bot.send_message(chat_id, text)
        else:
            return self.bot.send_message(chat_id, target[random.randint(0,len(target)-1)])
            
        
    def keyboard_response(self, callback):
        chat_id = callback['from']['id']
        data = callback['data']
        status = self.get_status()
        if status=='1':
            if data == 'Да, это я':
                text = """Пришлось использовать посредника, чтобы найти тебя. Только ты можешь мне помочь. Мой хозяин сказал, что не отпустит меня пить пиво пока я не уговорю тебя придти 15.04.21 в 18:00 сюда https://goo.gl/maps/7yNcv1UGkSWycrXB7, представляешь?? Так жестоко((
Возможно тебе немного страшно, но если ты не придешь, одним счастливым ботом станет меньше(
Не переживай, хозяин не злой, почти. 
И да, хозяин предпринял все, чтобы ты не узнала, кто он до встречи)
Так что, ты спасешь меня?)"""
            elif data == 'Нет, ты ошибся':
                text = """Я знаю, что это ты, Оля))
Пришлось использовать посредника, чтобы найти тебя. Только ты можешь мне помочь. Мой хозяин сказал, что не отпустит меня пить пиво пока я не уговорю тебя придти 15.04.21 в 18:00 сюда https://goo.gl/maps/7yNcv1UGkSWycrXB7, представляешь?? Так жестоко((
Возможно тебе немного страшно, но если ты не придешь, одним счастливым ботом станет меньше(
Не переживай, хозяин не злой, почти. 
И да, хозяин предпринял все, чтобы ты не узнала, кто он до встречи)
Так что, ты спасешь меня?)"""
            reply = self.bot.make_keyboard(['Испытать судьбу', 'Упустить шанс', 'Перенести на другое время'])
            self.add_status('2')
            return self.bot.send_message(chat_id, text, reply)
        
        elif status=='2':
            if data == 'Испытать судьбу':
                text = """Бесстрашный ты мой спаситель) Когда придешь на место, поднимись на второй этаж, не мерзни. 
Развлечь тебя? Я умею рифмовать покруче рэперов) Напиши любое слово, желательно, чтобы оно существовало)"""
                self.add_status('done')
                reply = None
            elif data == 'Упустить шанс':
                text = """Знаю, это страшно. Но маньяки не создают ботов) (Наверное)
Ладно, подскажу тебе. Ты знакома с хозяином. Давай же, настало время отбросить страхи!) Так что, поможешь мне?)"""
                reply = self.bot.make_keyboard(['Испытать судьбу', 'Нет'])
            elif data == 'Перенести на другое время':
                text = """Альтернативные варианты таинственной встречи"""
                self.add_status('3')
                reply = self.bot.make_large_keyboard([['15.03 16:00', '15.03 17:00','15.03 18:00'],['15.03 19:00','15.03 20:00','20.03 16:00'], ['20.03 17:00','20.03 18:00','20.03 19:00'], ['20.03 20:00', '21.03 16:00', '21.03 17:00'],['21.03 18:00','21.03 19:00','21.03 20:00'], ['Не устраивают варианты']])
            elif data == 'Нет':
                text = """Разбиваешь мое роботизированное сердце. Если передумаешь, напиши /start. 
Развлечь тебя? Я умею рифмовать покруче рэперов) Напиши любое слово, желательно, чтобы оно существовало)"""
                self.add_status('done')
                reply = None
            return self.bot.send_message(chat_id, text, reply)
            
        elif status=='3':
            if data == 'Не устраивают варианты':
                text = """Напиши свою дату одним предложением (только не вторник, пожалуйста))"""
                self.add_status('data')
            else:
                text = """Бесстрашный ты мой спаситель) Когда придешь на место, поднимись на второй этаж, не мерзни. 
Развлечь тебя? Я умею рифмовать покруче рэперов) Напиши любое слово, желательно, чтобы оно существовало)"""
                self.add_status('done')
            return self.bot.send_message(chat_id, text)
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
        return str(synonums)
            
            