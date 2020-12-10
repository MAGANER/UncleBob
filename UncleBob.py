import requests
import random
import sys

class Bot:
	def __init__(self):
		self.url = input("enter your url:")
		
	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		resp = requests.get(self.url + method, params)
		result_json = resp.json()['result']
		return result_json
	
	def get_last_update(self):
		get_result = self.get_updates()

		if len(get_result) > 0:
			last_update = get_result[-1]
		else:
			last_update = get_result[len(get_result)]

		return last_update
	
	def send_message(self, chat_id, text):
		params = {'chat_id': chat_id, 'text': text}
		method = 'sendMessage'
		resp = requests.post(self.url + method, params)
		return resp

class UncleBob(Bot):
	def __init__(self):
		Bot.__init__(self)
		self.last_update = 0
		
		self.last_update_id = -1
		self.last_message_id= -1
		self.last_chat_text = ""
		self.last_message   = ""
		self.last_chat_id   = -1
		self.last_chat_name = ""
		self.curr_message_id= -1
		
		self.pizda_counter  = 0
	
		
		self.started 		= False
		self.beer_counter   = True
		
		self.actions = {
						"будешь пиво?":  self.wanna_beer,
						"пизда":         self.pizda,
						"команды":       self.show_commands,
						"да":            self.say_yes,
						"соси":			 self.say_get_off,
						"привет":		 self.say_hello
					}
					
	def wanna_beer(self):
		data = ["кнч","nalivay","да","охота крепкое"]
		self.send_message(self.last_chat_id,random.choice(data))
	def pizda(self):
		if self.pizda_counter == 0:
			self.send_message(self.last_chat_id,"пизда, ага")
			self.pizda_counter = self.pizda_counter + 1
		if self.pizda_counter > 0:
			self.send_message(self.last_chat_id,"да, да пизда")
			self.pizda_counter = self.pizda_counter + 1
		if self.pizda_counter == 5:
			self.send_message(self.last_chat_id,"пошёл на хуй "+self.last_chat_name)
			self.pizda_counter = 0
	def show_commands(self):
		self.send_message(self.last_chat_id,"что я могу")
		for i in self.actions.keys():
			self.send_message(self.last_chat_id,i)
	def say_yes(self):
		data = ["так блять да","пизда","наверное","да это нет?"]
		self.send_message(self.last_chat_id,random.choice(data))
	def say_get_off(self):
		data = ["сам соси","обосрись и здохни"]
		self.send_message(self.last_chat_id,random.choice(data)+" "+ self.last_chat_name)
	def say_hello(self):
		data = ["zdorovo","hi"]
		self.send_message(self.last_chat_id,random.choice(data)+" "+ self.last_chat_name)
	def say_random_bull_shit(self):
		if "пиво" in self.last_message and self.beer_counter:
			data = ("кто-то сказал пиво?","а мне?","Пиво(!)")
			self.send_message(self.last_chat_id,random.choice(data))
			self.beer_counter = False
		if "пиво" not in self.last_message:
			self.beer_counter = True
	
	
	def is_talking_to_myself(self,text):
		return "/дядька" in text
	def get_command(self,text):
		return text[6:]
	
	
	def update_me(self):
		Bot.get_updates(self)
		self.last_update = Bot.get_last_update(self)
		
		self.last_update_id = self.last_update['update_id']
		if "message" in self.last_update.keys():
			self.last_chat_text = self.last_update['message']['text']
			self.last_chat_id   = self.last_update['message']['chat']['id']
			self.last_chat_name = self.last_update['message']['from']['first_name']
			self.curr_message_id= self.last_update['message']['message_id']
		
		if "text" in self.last_update["message"]:
			self.last_message = self.last_update["message"]["text"]

	def send_start_message(self):
		if self.started == False:
			self.send_message(self.last_chat_id,"готов трахать ваш мозг")
			self.started = True	
	def run(self):
		self.send_start_message()
		if self.is_talking_to_myself(self.last_chat_text) and self.last_message_id != self.curr_message_id:
			command = self.get_command(self.last_chat_text)[1:]
			command = command[1:]
			print(command)
			if command in self.actions.keys():
				self.actions[command]()
			else:
				self.send_message(self.last_chat_id,"сукаблячёэто "+command)
			self.last_message_id = self.curr_message_id
		self.say_random_bull_shit()
	

bot = UncleBob()
def main(bot):
	while True:
		bot.update_me()
		bot.run()
		
if __name__ == '__main__':  
	try:
		main(bot)
	except KeyboardInterrupt:
		bot.send_message(bot.last_chat_id,"ааа, меня заебаобалоооо")
		exit()
	






