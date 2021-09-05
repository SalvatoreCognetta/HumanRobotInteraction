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
		def __init__(self, name, img_path, price, description):
			self.name = name
			self.img_path = img_path
			self.price = price
			self.description = description
		def __str__(self):
			return '{ ' + self.name + ', ' + \
				self.img_path + ', ' +  self.price + \
				', ' + self.description + ' }'

	class Customer(object):
		id_counter = 0
		def __init__(self, food_list= None, payed = None, review = None):
			self.id = self.id_counter
			self.food_list = food_list
			self.payed = payed
			self.review = review
			self.id_counter += 1

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

		while a!='goodbye':

			if(a=='welcome'):
				a = im.ask('welcome', timeout=999)

			elif(a=='menu'):
				im.execute(a)
				im.executeModality('TTS','Fine, let me show what is in our menu!')
				food_no = 0
				food_list = list(MENU.keys())
				while a!='welcome':
					food = MENU[food_list[food_no]]
					im.executeModality('TEXT',food.name.upper() + ' - '+ food.price)
					im.executeModality('IMAGE',food.img_path)
					im.executeModality('TTS',food.description)
					im.executeModality('BUTTONS', [('prev', 'Previous'),  ('welcome', 'Main Page'), ('next', 'Next')])
					im.executeModality('ASR',{'next': ['next', 'go on', 'next dish'], 'prev': ['previous', 'go back','previous dish'], 'welcome': ['main page', 'go main page','go home', 'stop']})
					# im.robot.bm_service = im.robot.session.service("ALBackgroundMovement") # gives error
					# im.executeModality('GESTURE',random.choice(GESTURES)) # gives error
					a = im.ask(None, timeout=999)
					if (a=='next'): food_no+=1
					elif (a=='prev'): food_no-=1
					food_no = min(len(food_list)-1,max(0,food_no))

			elif(a=='order'):
				a = im.ask(a, timeout=999)

			elif(a=='checkout'):
				a = im.ask(a, timeout=999)

			elif(a=='book'):
				a = im.ask(a, timeout=999)

			elif(a=='review'):
				a = im.ask(a, timeout=999)
			
			elif(a=='goodbye'):
				a = im.ask(a, timeout=999)
				time.sleep(4)

			HISTORY[c.id] = c


if __name__ == "__main__":
	mws = ModimWSClient()
	# Local execution
	mws.setDemoPathAuto(__file__)
	#tablet_service.showWebview("http://192.18.0.1/apps/<your_app>/<your_demo>/index.html")
	mws.run_interaction(task)
