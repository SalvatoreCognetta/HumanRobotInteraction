import sys, os, time

try:
	sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
	print "Please set MODIM_HOME environment variable to MODIM folder."
	sys.exit(1)

import ws_client
from ws_client import *


def task():

	import csv, random

	GESTURES = ['animations/Stand/Gestures/Hey_'+str(i) for i in range(1,6)]

	class Food(object):
		def __init__(self, name, img_path, price, description, quantity=0):
			self.name = name
			self.img_path = img_path
			self.price = price
			self.description = description
			self.quantity = quantity
		# def __str__(self):
		# 	return self.__dict__ # CODE EXECTUTION ERROR: __str__ returned non-string (type dict)
		# Use vars(a), where a = Food()

	class Customer(object):
		id_counter = 0
		def __init__(self, food_list = {}, payed = False, review = None):
			self.id = self.id_counter
			self.food_list = food_list
			self.payed = payed
			self.review = review
			self.id_counter += 1
		# def __str__(self):
		# 	return self.__dict__ # CODE EXECTUTION ERROR: __str__ returned non-string (type dict)
		# Use vars(a), where a = Customer()


	MENU = dict()

	with open(os.path.join(os.path.expanduser("~"),'playground/html/src/waiter/menu.csv')) as f:                                                                                          
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			MENU[row[0]] = Food(*row)

	print(MENU)

	HISTORY = dict()

	while True:
		im.init()
		detected_person = False
		detected_person_confirm = False
		im.executeModality('TEXT_default','Waiting for a human!')

		#Checking if human stay in front of Pepper more than 2 seconds
		im.robot.startSensorMonitor()
		while not detected_person:
			while not detected_person_confirm:
				p = im.robot.sensorvalue() # p is the array with data of all the sensors
				detected_person_confirm = p[1] > 0.0 and p[1] < 1.0 # p[1] is the Front sonar
			if detected_person_confirm:
				print('*Person detected_person_confirm*')
				time.sleep(2)
				p = im.robot.sensorvalue()
				detected_person_confirm = p[1] > 0.0 and p[1] < 1.0
				if detected_person_confirm:
					print('*Person still there*')
					detected_person = True
				else:
					print('*Person gone*')
		
		im.robot.stopSensorMonitor()

		a = 'welcome'
		c = Customer() # instantiate new customer
		c.food_list = MENU
		while a not in ['goodbye', 'timeout']:
			# state machine

			if(a=='welcome'):
				# welcoming the customer and asks if needs help
				# flow input: menu/order/checkout/book(maybe -> see book state)
				# flow output: food description
				a = im.ask('welcome', timeout=20)

			elif(a=='menu'):
				# the customer can swipe the foods while pepper
				# gives a description and the price
				# flow input: prev/ main page/ next
				# flow output: food description
				im.execute(a)
				food_no = 0
				food_list = list(MENU.keys())
				while a!='welcome':
					food = MENU[food_list[food_no]]
					im.executeModality('TEXT',food.name.upper() + ' - $'+ str(food.price) + '<br><i><font size="3">'+ food.description + '</font></i>')
					im.executeModality('IMAGE',food.img_path)
					im.executeModality('BUTTONS', [('prev', 'Previous'),  ('welcome', 'Main Page'), ('next', 'Next')])
					im.executeModality('ASR',{'next': ['next', 'go on', 'next dish'], 'prev': ['previous', 'go back','previous dish'], 'welcome': ['main page', 'go main page','go home', 'stop']})
					im.executeModality('TTS',food.description)
					# im.robot.bm_service = im.robot.session.service("ALBackgroundMovement") # gives error
					# im.executeModality('GESTURE',random.choice(GESTURES)) # gives error
					a = im.ask(None, timeout=20)
					if (a=='next'): food_no+=1
					elif (a=='prev'): food_no-=1
					food_no = food_no % len(food_list)

			elif (a == 'order'):
				
				# pagine:
				#	- elenco menu
				#	- specifica quantita
				im.execute(a)
				im.executeModality('BUTTONS', [(key, MENU[key].name.upper()) for key in MENU] + [('review_order', 'Review order')])
				im.executeModality('TTS', 'Choose your dishes')

				a = chosen_food = im.ask(None, timeout=20)
				while a not in ['order', 'review_order']:
					# print "Food selected: " + str(chosen_food)
					food = MENU[chosen_food]

					food_quantity = c.food_list[chosen_food].quantity
					im.executeModality('TEXT',food.name.upper() + ' - $'+ str(food.price) + '<br><i><font size="3">'+ food.description + '</font></i>')
					im.executeModality('IMAGE',food.img_path)
					im.executeModality('BUTTONS', [('minus', '-'),  ('food_quantity', str(food_quantity)),  ('plus', '+'), ('order', 'Continue'), ('review_order', 'Review order')])
					im.executeModality('ASR',{'minus': ['remove', 'delete', 'remove ' + food.name], 'plus': ['add', 'add ' + food.name], 'order': ['continue', 'continue order'], 'review_order': ['check order', 'review order']})

					a = im.ask(None, timeout=20)
					if a == 'minus':
						food_quantity -= 1 if food_quantity > 0 else 0
					elif a == 'plus':
						food_quantity += 1
					c.food_list[chosen_food].quantity = food_quantity

			elif (a == 'review_order'):
				# gives a summary of the food ordered then asks 
				# if the customer want to change the order or
				# flow output: success page and thanks
				#	- resoconto (modifica/conferma)
				# informiamo utente dell'id
				im.execute(a)

				order_table = "<table class='styled-table'> <thead> <tr> <th>Dish</th> <th>Quantity</th> </tr> </thead> <tbody>"
				for key in c.food_list:
					food = c.food_list[key]
					if food.quantity > 0:
						order_table += '<tr>'
						order_table += '<td>'+str(food.name.upper())+'</td>'
						order_table += '<td>'+str(food.quantity)+'</td>'
						order_table += '</tr>'
				order_table += '</tbody> </table>'
				im.executeModality('TEXT', order_table)

				im.executeModality('BUTTONS', [('order', 'Modify order'), ('confirm_order', 'Confirm order')])
				im.executeModality('TTS','This is your order, modify it or send to the cuisine.')
				im.executeModality('ASR', {'order': ['modify', 'modify order'], 'confirm_order': ['confirm', 'confirm order', 'complete order', 'send order']})
				
				a = im.ask(None, timeout=100)

				if a == 'confirm_order':
					text = 'Your identification number is ' + str(c.id) + '. Use it for checkout.'
					im.executeModality('TEXT', text)
					im.executeModality('TTS', text)
					im.executeModality('BUTTONS', [('welcome', 'Main page')])
					im.executeModality('ASR',{'welcome': ['main page', 'go main page','go home']})
					
					a = im.ask(None, timeout=50)
					

			elif(a=='checkout'):
				# gives a summary of the food ordered then asks 
				# the type of payment or may display a fake QR code 
				# saying to scan and go paying, after few seconds 
				# shows a success page and thanks the customer
				# flow input: go pay
				# flow output: success page and thanks
				im.execute(a)
				im.executeModality('BUTTONS', [(str(id),str(id)) for id in HISTORY.keys()])
				im.executeModality('ASR', {str(id):[str(id)] for id in HISTORY.keys()})
				a = im.ask(None, timeout=15)
				if(a!='timeout'):
					c = HISTORY[int(a)]
					im.executeModality('TEXT','Thanks!')
					im.executeModality('TTS','Thanks!')
					time.sleep(1)
					im.executeModality('TEXT','Please review your order and proceed <br> with payment or request assistance!')
					im.executeModality('TTS','Please review your order and proceed with payment or request assistance!')
					time.sleep(1)
					im.executeModality('TEXT_title','Order review: Table #'+str(c.id))
					
					total = 0
					order_table = "<table class='styled-table'> <thead> <tr> <th>Dish</th> <th>Quantity</th> <th>Price</th> </tr> </thead> <tbody>"
					for key in c.food_list:
						food = c.food_list[key]
						if food.quantity > 0:
							total += int(food.quantity)*int(food.price)
							order_table += '<tr>'
							order_table += '<td>'+str(food.name.upper())+'</td>'
							order_table += '<td>'+str(food.quantity)+'</td>'
							order_table += '<td>$ '+str(int(food.quantity)*int(food.price))+'</td>'
							order_table += '</tr>'
					order_table += "<tr> <td colspan='3'>Total: $"+str(total)+"</td> </tr>"
					order_table += '</tbody> </table>'

					im.executeModality('TEXT',order_table)
					im.executeModality('BUTTONS', [('help', 'Help'),  ('welcome', 'Main Page'), ('pay', 'Payment')])
					im.executeModality('ASR',{'help': ['help', 'assistance', 'help me'], 'pay': ['pay', 'payment','proceed'], 'welcome': ['main page', 'go main page','go home', 'stop']})
					a = im.ask(None, timeout=15)

			elif(a=='pay'):
				# tell the customer to scan the qr code and pay
				# flow input: go back to main
				a = im.ask(a, timeout=3)
				if(a=='timeout'):
					im.executeModality('TEXT','Please wait for the transition to end..')
					im.executeModality('ASR', {})
					im.executeModality('BUTTONS', [])
					time.sleep(2)
					c.payed = True
					a = 'goodbye'
					im.executeModality('TEXT','The payment was successful, <br> you will be redirected in few seconds..')
					im.executeModality('TTS','The payment was successful, you will be redirected in few seconds..')
					time.sleep(2)

			elif(a=='review'):
				# flow input: 1 - 5 satisfaction rating
				im.executeModality('TEXT_title', 'Questionnaire!')
				im.executeModality('TEXT', 'Please select your table number!')
				im.executeModality('TTS', 'Please select your table number!')
				im.executeModality('BUTTONS', [(str(id),str(id)) for id in HISTORY.keys()])
				im.executeModality('ASR', {str(id):[str(id)] for id in HISTORY.keys()})
				a = im.ask(None, timeout=15)
				if(a!='timeout'):
					c = HISTORY[int(a)]
					time.sleep(1)
					a = im.ask(a, timeout=15)
					im.logenable() # Activating log to store the answers
					q = dict()
					for t in ['l','i']:
						for i in range(1,6):
							a = im.ask(t+str(i), timeout=15)
							im.logdata(t+str(i)+': '+a)
							q[t+str(i)] = a
					c.review = q
					im.logclose()
					a = 'welcome'
					im.executeModality('TEXT','Thank you! The questionnaire was successful! <br> You will be redirected in few seconds..')
					im.executeModality('TTS','Thank you! The questionnaire was successful!')
					time.sleep(3)
				
			elif(a=='help'):
				# advice the customer that he will receive assistance soon
				# flow input: go back to main
				a = im.ask(a, timeout=15)
			
			if(a=='goodbye'):
				# flow input: confirmation/ give a rating/ main page
				a = im.ask(a, timeout=15)
				if(a=='goodbye' or a=='timeout'): # goodbye confirmation then wait for the customer to go away
					im.executeModality('TEXT_title','Goodbye!')
					im.executeModality('ASR', {})
					im.executeModality('BUTTONS', [])
					im.executeModality('TEXT',"See you soon at Pepper's!")
					im.executeModality('TTS',"See you soon at Pepper's!")
					time.sleep(4)

			print(c)
			HISTORY[c.id] = c


if __name__ == "__main__":
	mws = ModimWSClient()
	# Local execution
	mws.setDemoPathAuto(__file__)
	#tablet_service.showWebview("http://192.18.0.1/apps/<your_app>/<your_demo>/index.html")
	mws.run_interaction(task)
