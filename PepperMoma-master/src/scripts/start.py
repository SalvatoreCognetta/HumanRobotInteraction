import sys, os, time

try:
    sys.path.insert(0, os.getenv('MODIM_HOME')+'/src/GUI')
except Exception as e:
    print "Please set MODIM_HOME environment variable to MODIM folder."
    sys.exit(1)

import ws_client
from ws_client import *

def intStart():

	while True:
		im.init()
		flag = False
		flag2 = False
		flagP = False
		detected = False

		im.executeModality('TEXT_default','Waiting for a human')

		#Checking if human stay in front of Pepper more than 2 seconds
		im.robot.startSensorMonitor()
		while not flagP:
			while not detected:
				p = im.robot.sensorvalue() #p is the array with data of all the sensors
				detected = p[1] > 0.0 and p[1] < 1.0 #p[1] is the Front sonar
			if detected:
				print('*Person Detected*')
				time.sleep(2)
				p = im.robot.sensorvalue()
				detected = p[1] > 0.0 and p[1] < 1.0
				if detected:
					print('*Person still there*')
					flagP = True
				else:
					print('*Person gone*')
		im.robot.stopSensorMonitor()

		#Starting the script when human stays 2+ seconds
		im.execute('welcome')
		a0 = im.ask('welcome', timeout=999)

		#If it is the first time for the visitor, explain history	
		if a0 == 'story':
			im.execute(a0)
			im.execute('introtour')
			t0 = im.ask('introtour',timeout=999)
			
			#Ask if the new visitor wants a tour
			if t0 == 'tour':
				im.execute('tour1')
				im.execute('tour1map')
				time.sleep(3)
				im.execute('tour2')
				im.execute('tour2map')
				time.sleep(3)
				im.execute('tour3')
				im.execute('tour3map')
				time.sleep(3)

		else:
			im.executeModality('TTS','Fine, we have an expert here!')

		#Main loop of the project, it returns over the map to ask for works
		while not flag:

			#If it is the first time that the user view the map, some specific words are shown
			if not flag2: 		
				im.executeModality('TTS','This is the full map of the museum. Are you interested in any particular work?')
				im.executeModality('TEXT_default','Are you interested in any particular work?')	
				flag2 = True	
			#Otherwise Pepper TTS and the html change
			else:
				im.executeModality('TEXT_default','Are you interested in any other work?')
				im.executeModality('TTS','Are you interested in any other work?')
					
			a = im.ask('fullmap',timeout=5)

			while a=='timeout':
				im.executeModality('TTS','I did not understand, can you repeat please? You can also use buttons on the tablet.')
				a = im.ask('fullmap',timeout=5)
				if flag2:			
					im.executeModality('TEXT_default','Are you interested in any other work?')
					im.executeModality('TTS','Are you interested in any other work?')

			#Checking if user want to stop the trip
			if a=='goodbye':
				flag=True
				im.execute('goodbye')
				break		
			else:
				im.execute(a)
				a2 = im.ask(a,timeout=999)
				
				#Checking if user does not want directions				
				if a2=='fullmap':		
					im.execute(a2)
				else: 
					im.execute(a2)
					time.sleep(4)	
					im.execute('fullmap')
			
		time.sleep(6)

if __name__ == "__main__":
	mws = ModimWSClient()
	mws.setDemoPathAuto(__file__)
	mws.run_interaction(intStart)
